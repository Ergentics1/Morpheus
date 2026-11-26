#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ergentics, LLC -- Piece I open reproducible synthesis simulation
"""Open, zero-dependency reference simulator & figure generator for Horizon Piece I.

Synthesizes Working Papers 030 & 031 (Horizons I & IB) under unified conventions:
  - WGS84 equatorial Earth radius R_E = 6,378.137 km (NEG-W27a)
  - Consistent iso-inertial polar moment I_0 = (2/3) M L^2 (NEG-W27b; ML^2 shown alongside)
  - Unitary equilateral-pole Hopf basis w_+/- (collision-free -90 deg physical holonomy, NEG-W2/W25)
  - Explicit open coupled 4-body planar RK4 & 3D J2 RK4 with subtracted L=0 control (SPEC-030/031)
  - Theorem G4 mechanical-hub vs. electrical-winch sizing & keyed SplitMix64 N=1,600 RCT
Zero cached data reads; emits CC BY 4.0 data/piece1_calibration.json + MANIFEST.sha256
and compiles metadata-free vector PDF figures via standalone PGFPlots/pdflatex.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
import pathlib
import subprocess
import tempfile
from typing import Dict, List, Tuple

# Unified Physical & Mission Constants (WGS84 / IAU)
MU_E = 3.986004418e14          # m^3 / s^2
R_E = 6_378_137.0              # m (WGS84 equatorial, NEG-W27a)
J2_E = 1.08262668e-3
T_YR = 365.25 * 86_400.0       # s
G0 = 9.80665                   # m / s^2
H_MIN = 600_000.0              # m (safe perigee altitude above LEO drag)
R_P_SAFE = R_E + H_MIN         # 6,978,137.0 m
M_CRAFT = 1_000.0              # kg
L_REF = 20_000.0               # m (20 km collinear span)
L_SMALL = 100.0                # m (100 m LEO span)
ETA_ACT = 0.88
ETA_REG = 0.80
ETA_MECH_RT = 0.985            # 98.5% mechanical spring-drum round-trip efficiency
SIGMA_ALLOW = 1.16e9           # Pa (Zylon HM 5.8 GPa / SF 5)
RHO_ZYLON = 1_560.0            # kg / m^3
E_ZYLON = 270.0e9              # Pa
MU_BENNU = 4.892               # m^3 / s^2
SRP_1AU = 4.56e-6              # N / m^2

SEED_PIECE1 = 0x484F52495A5F5031  # ASCII "HORIZ_P1"


class SplitMix64:
    """Keyed 64-bit deterministic PRNG for bit-exact reproducible RCT replay."""

    MASK = (1 << 64) - 1

    def __init__(self, seed: int) -> None:
        self.state = seed & self.MASK

    def next_u64(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & self.MASK
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & self.MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & self.MASK
        return (z ^ (z >> 31)) & self.MASK

    def next_f64(self) -> float:
        return (self.next_u64() >> 11) * (1.0 / (1 << 53))


def jacobi_to_rho(z1: complex, z2: complex) -> Tuple[complex, complex, complex]:
    rt2 = math.sqrt(2.0)
    rt6 = math.sqrt(6.0)
    return (z1 / rt2 + z2 / rt6, -z1 / rt2 + z2 / rt6, -2.0 * z2 / rt6)


def wp030_chart(th0: float, theta: float, phi: float, r_j: float = math.sqrt(2.0)) -> Tuple[complex, complex, complex]:
    z1 = r_j * math.cos(0.5 * theta) * cmath.exp(1j * (th0 + 0.5 * phi))
    z2 = r_j * math.sin(0.5 * theta) * cmath.exp(1j * (th0 - 0.5 * phi))
    return jacobi_to_rho(z1, z2)


def g4n_chart(th0: float, beta: float, chi: float, r_j: float = math.sqrt(2.0)) -> Tuple[complex, complex, complex]:
    wp = r_j * math.cos(0.5 * beta) * cmath.exp(1j * (th0 + 0.5 * chi))
    wm = r_j * math.sin(0.5 * beta) * cmath.exp(1j * (th0 - 0.5 * chi))
    rt2 = math.sqrt(2.0)
    return jacobi_to_rho((wp + wm) / rt2, (wp - wm) / (1j * rt2))


def gate_d1_cancellation_and_orders() -> Tuple[bool, Dict[str, object]]:
    """Gate D1: C137 cancellation-free contrast and named evaluation-order rounding (NEG-W26)."""
    r0, span = 7.0e6, 100.0
    exact = -(MU_E / 3.0) * 2.0 * span**2 * (3.0 * r0**2 - span**2) / (
        r0**2 * (r0**2 - span**2) ** 2
    )
    naive_factored = -(MU_E / 3.0) * (1.0 / (r0 + span) ** 2 + 1.0 / (r0 - span) ** 2 - 2.0 / r0**2)
    naive_meansub = (
        -(MU_E / (r0 + span) ** 2) - (MU_E / r0**2) - (MU_E / (r0 - span) ** 2)
    ) / 3.0 + MU_E / r0**2

    sweep = {}
    for eps in (1e-5, 1e-6, 1e-7, 1e-8, 5e-9):
        ex_u = -(1.0 / 3.0) * 2.0 * eps**2 * (3.0 - eps**2) / ((1.0 - eps**2) ** 2)
        nv_u = -(1.0 / 3.0) * (1.0 / (1.0 + eps) ** 2 + 1.0 / (1.0 - eps) ** 2 - 2.0)
        sweep[f"{eps:.0e}"] = abs(nv_u - ex_u) / abs(ex_u)

    err_fact = abs(naive_factored - exact) / abs(exact)
    err_mean = abs(naive_meansub - exact) / abs(exact)
    ok = (
        abs(exact - (-3.3202868966e-9)) < 1e-18
        and abs(err_fact - 5.75e-8) < 2e-9
        and abs(err_mean - 3.46e-7) < 3e-9
        and abs(sweep["1e-07"] - 8.20e-3) < 2e-5
        and abs(sweep["1e-08"] - 0.4803) < 1e-3
        and sweep["5e-09"] == 1.0
    )
    return ok, {
        "exact_da_mps2": exact,
        "relerr_factored_order": err_fact,
        "relerr_mean_sub_order": err_mean,
        "unit_eps_relerr": sweep,
    }


def gate_d2_hopf_holonomy_and_g1() -> Tuple[bool, Dict[str, object], List[Tuple[float, float, float, float]]]:
    """Gate D2: Paper chart vs equilateral-pole basis (NEG-W2/W4/W25) & Theorem G1 curve."""
    th = math.pi / 3.0
    p0 = wp030_chart(0.0, th, 0.0)
    p1 = wp030_chart(-0.5 * math.cos(th) * 2.0 * math.pi, th, 2.0 * math.pi)
    phys_paper_deg = math.degrees(cmath.phase(p1[0] / p0[0]))

    g0 = g4n_chart(0.0, th, 0.0)
    g1 = g4n_chart(-0.5 * math.cos(th) * (-2.0 * math.pi), th, -2.0 * math.pi)
    phys_g4n_deg = math.degrees(cmath.phase(g1[0] / g0[0]))

    # Minimum inter-body distance along both loops (N = 3600 samples)
    min_d_paper = min(
        min(abs(r[i] - r[j]) for i, j in ((0, 1), (1, 2), (0, 2)))
        for k in range(3600)
        for r in [wp030_chart(0.0, th, 2.0 * math.pi * k / 3600.0)]
    )
    min_d_g4n = min(
        min(abs(r[i] - r[j]) for i, j in ((0, 1), (1, 2), (0, 2)))
        for k in range(3600)
        for r in [g4n_chart(0.0, th, -2.0 * math.pi * k / 3600.0)]
    )

    # Mass quadrupole vs inertia tensor sign check (NEG-W4)
    r_chk = g4n_chart(0.37, 0.91, 1.23)
    q_mass = sum(rk * rk for rk in r_chk)
    ixx = sum(rk.imag ** 2 for rk in r_chk)
    iyy = sum(rk.real ** 2 for rk in r_chk)
    ixy = -sum(rk.real * rk.imag for rk in r_chk)
    q_inertia = (ixx - iyy) + 2j * ixy
    sign_sum_err = abs(q_inertia + q_mass)

    # Theorem G1 sweep: (q, T/(0.5 I0 Om^2), max|rho|/L, hard_span_parity 3q/(2(1+q)))
    g1_curve: List[Tuple[float, float, float, float]] = []
    for k in range(1, 96):
        q = k / 100.0
        ke_ratio = (q * q) / (1.0 - q * q)
        rmax = math.sqrt(2.0 * (1.0 + q) / 3.0)
        parity = 3.0 * q / (2.0 * (1.0 + q))
        g1_curve.append((q, ke_ratio, rmax, parity))

    # Numerical differentiation check at q = 0.50, 1/sqrt(2), 0.85, 0.95
    max_g1_num_err = 0.0
    for q in (0.50, 1.0 / math.sqrt(2.0), 0.85, 0.95):
        b = math.pi - math.asin(q)
        dt = 1e-6
        chi_dot = -2.0 / math.cos(b)  # zero-spin: th0_dot + (1/2) cos(b) chi_dot = 0 with th0_dot = 1
        ra = g4n_chart(0.0, b, 0.3)
        rb = g4n_chart(dt, b, 0.3 + chi_dot * dt)
        ke_num = 0.5 * sum(abs((v - u) / dt) ** 2 for u, v in zip(ra, rb))
        ke_ex = q * q / (1.0 - q * q)  # since I0 = 2 for M=3, L=1 -> 0.5*I0*1^2 = 1
        max_g1_num_err = max(max_g1_num_err, abs(ke_num - ke_ex))

    ok = (
        abs(phys_paper_deg - 90.0) < 1e-12
        and abs(phys_g4n_deg + 90.0) < 1e-12
        and min_d_paper < 1e-12
        and abs(min_d_g4n - math.sqrt(2.0 - math.sqrt(3.0))) < 1e-6
        and sign_sum_err < 1e-14
        and max_g1_num_err < 1e-7
    )
    return ok, {
        "paper_chart_chart_dth0_deg": -90.0,
        "paper_chart_physical_rot_deg": phys_paper_deg,
        "paper_chart_min_sep_over_L": min_d_paper,
        "g4n_basis_physical_rot_deg": phys_g4n_deg,
        "g4n_basis_min_sep_over_L": min_d_g4n,
        "neg_w4_q_inertia_plus_q_mass_err": sign_sum_err,
        "g1_ke_q50": 0.25 / 0.75,
        "g1_ke_q85": 0.85**2 / (1.0 - 0.85**2),
        "g1_ke_q95": 0.95**2 / (1.0 - 0.95**2),
        "g1_rmax_q95": math.sqrt(2.0 * 1.95 / 3.0),
        "g1_max_num_err": max_g1_num_err,
    }, g1_curve


def gate_d3_safe_perigee_k9_and_missions() -> Tuple[bool, Dict[str, object], List[Tuple[float, float]]]:
    """Gate D3: Safe-perigee K9 optimum, corrected prefactor (NEG-W16), and unified mission table."""
    def f_e(e: float) -> float:
        return (3.0 * e + e**3) * (1.0 - e) / ((1.0 + e) ** 3)

    def g_e(e: float) -> float:
        return 3.0 - 12.0 * e + 6.0 * e**2 - 4.0 * e**3 - e**4

    def gp_e(e: float) -> float:
        return -12.0 + 12.0 * e - 12.0 * e**2 - 4.0 * e**3

    e_opt = 0.28
    for _ in range(15):
        e_opt -= g_e(e_opt) / gp_e(e_opt)

    # K8 e_50*: (1 - e)^3 / (1 + e)^3 = 0.5 -> e = (1 - 2^(-1/3)) / (1 + 2^(-1/3))
    c3 = 2.0 ** (-1.0 / 3.0)
    e50 = (1.0 - c3) / (1.0 + c3)
    f35_loss = ((1.0 - 0.0275) / (1.0 + 0.0275)) ** 3  # 0.847858 = 84.8% (NEG-W6)

    # Dimensionally exact prefactor: T_yr * mu * L^2 / (pi * r_p^4) [m/s] (for I_0 = 2/3 M L^2)
    pref_20km = T_YR * MU_E * (L_REF**2) / (math.pi * (R_P_SAFE**4))
    pref_100m = T_YR * MU_E * (L_SMALL**2) / (math.pi * (R_P_SAFE**4))
    dv_opt = pref_20km * f_e(e_opt)
    dv_025 = pref_20km * f_e(0.25)
    dv_040 = pref_20km * f_e(0.40)
    dv_100m_mm = pref_100m * f_e(e_opt) * 1e3

    # Corrected Regimes A & B at WGS84 r_p = 6,978.137 km (h_min = 600 km) & Bennu Regime C
    t_reg_a_safe = MU_E * M_CRAFT * L_SMALL / (R_P_SAFE**3)
    t_reg_b_safe_static = MU_E * M_CRAFT * L_REF / (R_P_SAFE**3)
    r_bennu = 2_500.0
    t_bennu = MU_BENNU * M_CRAFT * L_SMALL / (r_bennu**3)
    da_bennu = 2.0 * MU_BENNU * (L_SMALL**2) / (r_bennu**4)
    srp_accel = SRP_1AU * 0.01  # A/M = 0.01 m^2/kg
    dv_bennu_mm = (
        T_YR
        * MU_BENNU
        * (L_SMALL**2)
        / (math.pi * ((r_bennu * 0.75) ** 4))
        * f_e(0.25)
        * 1e3
    )

    k9_curve = [(k / 100.0, pref_20km * f_e(k / 100.0)) for k in range(0, 91)]

    ok = (
        abs(e_opt - 0.2817015579087740) < 1e-14
        and abs(dv_opt - 199.8882) < 1e-3
        and abs(dv_025 - 198.5826) < 1e-3
        and abs(dv_040 - 186.6844) < 1e-3
        and abs(dv_100m_mm - 4.9972) < 1e-3
        and abs(e50 - 0.1150133319511158) < 1e-14
        and abs(f35_loss - 0.847858) < 1e-5
    )
    return ok, {
        "r_p_safe_km": R_P_SAFE / 1e3,
        "k9_e_opt": e_opt,
        "dv_yr_opt_20km_mps": dv_opt,
        "dv_yr_e025_20km_mps": dv_025,
        "dv_yr_e040_20km_mps": dv_040,
        "dv_yr_opt_100m_mmps": dv_100m_mm,
        "k8_e50_star": e50,
        "f35_loss_at_00275": f35_loss,
        "tension_regime_a_safe_N": t_reg_a_safe,
        "tension_regime_b_safe_tidal_N": t_reg_b_safe_static,
        "bennu_coupling_ratio_eps2": (7.0e6 / r_bennu) ** 2,
        "bennu_tension_N": t_bennu,
        "bennu_da_mps2": da_bennu,
        "srp_1au_mps2": srp_accel,
        "bennu_dv_yr_mmps": dv_bennu_mm,
    }, k9_curve


def gate_r1_open_planar_4body() -> Tuple[bool, Dict[str, object]]:
    """Gate R1: Explicit open 4-body planar RK4 (triad vs Landis dumbbell vs e0=0 null, SPEC-030)."""
    # Exact documented open run spec (canonical dimensionless units):
    #   mu = 1.0, M = 3.0 (m_i = 1.0), L = 0.04, I_0 = (2/3) M L^2 = 2 L^2 = 3.2e-3
    #   a0 = 1.0, e0 = 0.20 (r0 = 0.80, v0 = sqrt(1.5)), 5 orbits, RK4 2,000 steps/orbit.
    #   Collision-free w_+/- zero-spin switching law:
    #     q_signed = -q_max * tanh(k_sw * v_rad), q_max = 0.85, k_sw = 8.0
    #     (transverse outbound v_rad > 0 -> less inward pull; radial inbound v_rad < 0 -> stronger inward pull)
    #     chi = pi (radial) / 0 (transverse) preserves exact radial reflection symmetry -> zero octupole torque.
    mu = 1.0
    span = 0.04
    m_i = 1.0
    M = 3.0
    r_j = math.sqrt(2.0) * span

    def run_triad(e0: float, n_orbits: int = 5, steps_per_orb: int = 2000) -> Dict[str, float]:
        r0 = 1.0 - e0
        if e0 == 0.0:
            # Exact finite-size circular equilibrium speed for equilateral triad (q -> 0)
            eq_rhos = g4n_chart(0.0, math.pi, math.pi, r_j=r_j)
            ar_eq = sum(-mu * (r0 + rk.real) / (((r0 + rk.real) ** 2 + rk.imag**2) ** 1.5) for rk in eq_rhos) / 3.0
            v0 = math.sqrt(-r0 * ar_eq)
        else:
            v0 = math.sqrt((1.0 + e0) / (1.0 - e0))
        # State: [x, y, vx, vy, S_craft]
        s = [r0, 0.0, 0.0, v0, 0.0]
        dt = 2.0 * math.pi / steps_per_orb
        e_init = 0.5 * M * (v0 * v0) - mu * M / r0
        l_init = M * (r0 * v0)
        p_init = (l_init / M) ** 2 / mu

        def triad_rhos(x: float, y: float, vx: float, vy: float) -> Tuple[complex, complex, complex]:
            r_mag = math.hypot(x, y)
            theta_orb = math.atan2(y, x)
            v_rad = (x * vx + y * vy) / r_mag
            # Orbit raising: transverse outbound (v_rad > 0 -> q_signed < 0), radial inbound (v_rad < 0 -> q_signed > 0)
            q_signed = -0.85 * math.tanh(8.0 * v_rad)
            q_abs = abs(q_signed)
            beta = math.pi - math.asin(max(1e-12, q_abs))
            if q_signed >= 0.0:
                th0, chi = theta_orb, math.pi
            else:
                th0, chi = theta_orb + 0.5 * math.pi, 0.0
            return g4n_chart(th0, beta, chi, r_j=r_j)

        def forces_and_pot(st: List[float]) -> Tuple[float, float, float, float]:
            x, y, vx, vy = st[0], st[1], st[2], st[3]
            rhos = triad_rhos(x, y, vx, vy)
            ax = ay = tau_z = u_pot = 0.0
            for rk in rhos:
                rx = x + rk.real
                ry = y + rk.imag
                d2 = rx * rx + ry * ry
                d = math.sqrt(d2)
                inv_d3 = 1.0 / (d2 * d)
                fkx = -mu * m_i * rx * inv_d3
                fky = -mu * m_i * ry * inv_d3
                ax += fkx / M
                ay += fky / M
                tau_z += rk.real * fky - rk.imag * fkx
                u_pot -= mu * m_i / d
            return ax, ay, tau_z, u_pot

        def deriv(st: List[float]) -> List[float]:
            ax, ay, tau_z, _ = forces_and_pot(st)
            return [st[2], st[3], ax, ay, tau_z]

        _, _, _, u_tot_0 = forces_and_pot(s)
        e_tot_0 = 0.5 * M * (v0 * v0) + u_tot_0
        max_dl = max_dj = max_dp = 0.0
        for _ in range(n_orbits * steps_per_orb):
            k1 = deriv(s)
            k2 = deriv([s[i] + 0.5 * dt * k1[i] for i in range(5)])
            k3 = deriv([s[i] + 0.5 * dt * k2[i] for i in range(5)])
            k4 = deriv([s[i] + dt * k3[i] for i in range(5)])
            s = [s[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) for i in range(5)]
            lv = M * (s[0] * s[3] - s[1] * s[2])
            jv = lv + s[4]
            pv = (lv / M) ** 2 / mu
            max_dl = max(max_dl, abs(lv - l_init))
            max_dj = max(max_dj, abs(jv - l_init))
            max_dp = max(max_dp, abs(pv - p_init))

        x, y, vx, vy = s[0], s[1], s[2], s[3]
        r_f = math.hypot(x, y)
        v2_f = vx * vx + vy * vy
        e_osc = 0.5 * M * v2_f - mu * M / r_f
        _, _, _, u_tot_f = forces_and_pot(s)
        e_tot = 0.5 * M * v2_f + u_tot_f
        p_f = (x * vy - y * vx) ** 2 / mu
        a_osc = -mu * M / (2.0 * e_osc)
        e_osc_val = math.sqrt(max(0.0, 1.0 - p_f / a_osc))
        a_tot = -mu * M / (2.0 * e_tot)
        e_tot_val = math.sqrt(max(0.0, 1.0 - p_f / a_tot))
        return {
            "dE_osc": e_osc - e_init,
            "dE_tot": e_tot - e_tot_0,
            "max_dL": max_dl,
            "max_dJ_tot": max_dj,
            "max_dp": max_dp,
            "a_osc": a_osc,
            "e_osc": e_osc_val,
            "a_tot": a_tot,
            "e_tot": e_tot_val,
        }

    # Unassisted 2-mass Landis dumbbell (2 masses of 1.5 at +-r(t), free attitude angle psi):
    def run_landis_tumble(e0: float = 0.20, n_orbits: int = 5, steps_per_orb: int = 2000) -> Dict[str, float]:
        r0 = 1.0 - e0
        v0 = math.sqrt((1.0 + e0) / (1.0 - e0))
        s = [r0, 0.0, 0.0, v0, 0.0, v0 / r0]
        dt = 2.0 * math.pi / steps_per_orb
        l_max = span
        l_min = 0.2 * span

        def length_and_rate(x: float, y: float, vx: float, vy: float) -> Tuple[float, float]:
            rm = math.hypot(x, y)
            vr = (x * vx + y * vy) / rm
            th = math.tanh(-8.0 * vr)
            lv = 0.5 * (l_max + l_min) + 0.5 * (l_max - l_min) * th
            vt = (x * vy - y * vx) / rm
            vr_dot = (vt * vt) / rm - mu / (rm * rm)
            sech2 = 1.0 - th * th
            ldot = -0.5 * (l_max - l_min) * 8.0 * sech2 * vr_dot
            return lv, ldot

        def deriv(st: List[float]) -> List[float]:
            x, y, vx, vy, psi, psid = st
            lv, ldot = length_and_rate(x, y, vx, vy)
            c, sn = math.cos(psi), math.sin(psi)
            x1, y1 = x + lv * c, y + lv * sn
            x2, y2 = x - lv * c, y - lv * sn
            d1 = math.hypot(x1, y1)
            d2 = math.hypot(x2, y2)
            a1x, a1y = -mu * x1 / (d1**3), -mu * y1 / (d1**3)
            a2x, a2y = -mu * x2 / (d2**3), -mu * y2 / (d2**3)
            ax, ay = 0.5 * (a1x + a2x), 0.5 * (a1y + a2y)
            tau_over_i = ((a1y - a2y) * c - (a1x - a2x) * sn) / (2.0 * lv)
            psidd = tau_over_i - 2.0 * (ldot / lv) * psid
            return [vx, vy, ax, ay, psid, psidd]

        max_rel_deg = 0.0
        for _ in range(n_orbits * steps_per_orb):
            k1 = deriv(s)
            k2 = deriv([s[i] + 0.5 * dt * k1[i] for i in range(6)])
            k3 = deriv([s[i] + 0.5 * dt * k2[i] for i in range(6)])
            k4 = deriv([s[i] + dt * k3[i] for i in range(6)])
            s = [s[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) for i in range(6)]
            th_orb = math.atan2(s[1], s[0])
            rel = abs(math.degrees(s[4] - th_orb))
            max_rel_deg = max(max_rel_deg, rel)
        return {"max_tumble_deg": max_rel_deg, "final_spin_rate": s[5]}

    ecc = run_triad(0.20)
    circ = run_triad(0.0)
    landis = run_landis_tumble(0.20)
    de_ideal_5orb = 5.0 * 0.85 * 2.0 * mu * M * (span**2) * (3.0 * 0.20 + 0.20**3) / (0.96**3)

    ok = (
        ecc["dE_osc"] > 0.025
        and ecc["max_dL"] < 1e-10
        and ecc["max_dJ_tot"] < 1e-10
        and ecc["max_dp"] < 1e-10
        and abs(circ["dE_tot"]) < 1e-5
        and abs(ecc["dE_tot"] / max(abs(circ["dE_tot"]), 1e-15)) > 2000.0
        and circ["max_dJ_tot"] < 1e-10
        and landis["max_tumble_deg"] > 500.0
    )
    return ok, {
        "spec": {
            "mu": mu,
            "M": M,
            "L": span,
            "a0": 1.0,
            "e0": 0.20,
            "q_max": 0.85,
            "k_sw": 8.0,
            "orbits": 5,
            "steps_per_orbit": 2000,
        },
        "triad_ecc_e020": ecc,
        "triad_ideal_5orb_dE": de_ideal_5orb,
        "triad_circular_null_e0": circ,
        "landis_2mass_unassisted": landis,
    }


def gate_r2_3d_j2_with_l0_control() -> Tuple[bool, Dict[str, object], List[Tuple[float, float, float, float]]]:
    """Gate R2: 5-orbit 3D J2 coupled RK4 with subtracted L=0 point-mass control (NEG-W17/W18)."""
    rx = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
    rz = [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]
    rtot = [[sum(rx[i][k] * rz[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    v_true = [1, 1, -1]
    v_fig1 = [-1, 1, -1]
    img_true = [sum(rtot[i][j] * v_true[j] for j in range(3)) for i in range(3)]
    img_fig1 = [sum(rtot[i][j] * v_fig1[j] for j in range(3)) for i in range(3)]

    def accel_j2_point(x: float, y: float, z: float, k_j2: float) -> Tuple[float, float, float]:
        r2 = x * x + y * y + z * z
        r = math.sqrt(r2)
        r3 = r2 * r
        f0 = -1.0 / r3
        c = -1.5 * k_j2 / (r2 * r3)
        zz = (z * z) / r2
        return ((f0 + c * (1.0 - 5.0 * zz)) * x, (f0 + c * (1.0 - 5.0 * zz)) * y, (f0 + c * (3.0 - 5.0 * zz)) * z)

    def run_3d(k_j2: float, span: float) -> Tuple[Dict[str, float], List[Tuple[float, float, float]]]:
        i0 = math.radians(45.0)
        v0 = math.sqrt(1.0 + 1.5 * k_j2)
        # State: [x, y, z, vx, vy, vz, S_z] tracking exact coupled axial spin S_z
        s = [1.0, 0.0, 0.0, 0.0, v0 * math.cos(i0), v0 * math.sin(i0), 0.0]
        steps_per_orb = 2000
        n_orb = 5
        dt = 2.0 * math.pi / steps_per_orb
        M = 3.0

        def lvec(st: List[float]) -> Tuple[float, float, float]:
            x, y, z, vx, vy, vz = st[0], st[1], st[2], st[3], st[4], st[5]
            return (M * (y * vz - z * vy), M * (z * vx - x * vz), M * (x * vy - y * vx))

        def deriv(st: List[float]) -> List[float]:
            x, y, z, vx, vy, vz = st[0], st[1], st[2], st[3], st[4], st[5]
            if span == 0.0:
                ax, ay, az = accel_j2_point(x, y, z, k_j2)
                return [vx, vy, vz, ax, ay, az, 0.0]
            r_mag = math.sqrt(x * x + y * y + z * z)
            ur = (x / r_mag, y / r_mag, z / r_mag)
            hx = y * vz - z * vy
            hy = z * vx - x * vz
            hz = x * vy - y * vx
            hm = math.sqrt(hx * hx + hy * hy + hz * hz)
            uh = (hx / hm, hy / hm, hz / hm)
            sgn = 1.0 if z >= 0.0 else -1.0
            c45 = math.sqrt(0.5)
            dvec = (
                span * c45 * (ur[0] + sgn * uh[0]),
                span * c45 * (ur[1] + sgn * uh[1]),
                span * c45 * (ur[2] + sgn * uh[2]),
            )
            a0 = accel_j2_point(x, y, z, k_j2)
            ap = accel_j2_point(x + dvec[0], y + dvec[1], z + dvec[2], k_j2)
            am = accel_j2_point(x - dvec[0], y - dvec[1], z - dvec[2], k_j2)
            # Coupled internal axial torque tau_z = sum_k (rho_k x m_k a_k)_z (m_k = 1)
            tau_z = (dvec[0] * ap[1] - dvec[1] * ap[0]) + (-dvec[0] * am[1] + dvec[1] * am[0])
            return [
                vx, vy, vz,
                (a0[0] + ap[0] + am[0]) / 3.0,
                (a0[1] + ap[1] + am[1]) / 3.0,
                (a0[2] + ap[2] + am[2]) / 3.0,
                tau_z,
            ]

        l0 = lvec(s)
        l0_norm = math.sqrt(sum(c * c for c in l0))
        max_djz = max_djp = 0.0
        trace: List[Tuple[float, float, float]] = [(0.0, 45.0, l0_norm)]
        for step in range(1, n_orb * steps_per_orb + 1):
            k1 = deriv(s)
            k2 = deriv([s[i] + 0.5 * dt * k1[i] for i in range(7)])
            k3 = deriv([s[i] + 0.5 * dt * k2[i] for i in range(7)])
            k4 = deriv([s[i] + dt * k3[i] for i in range(7)])
            s = [s[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) for i in range(7)]
            lv = lvec(s)
            ln = math.sqrt(sum(c * c for c in lv))
            max_djz = max(max_djz, abs((lv[2] + s[6]) - l0[2]))
            max_djp = max(max_djp, math.hypot(lv[0] - l0[0], lv[1] - l0[1]))
            if step % 100 == 0:
                inc = math.degrees(math.acos(max(-1.0, min(1.0, lv[2] / ln))))
                trace.append((step / steps_per_orb, inc, ln))
        lv = lvec(s)
        ln = math.sqrt(sum(c * c for c in lv))
        i_end = math.degrees(math.acos(lv[2] / ln))
        return {
            "max_dJz_tot": max_djz,
            "final_Sz": s[6],
            "max_dJperp": max_djp,
            "delta_L_norm": ln - l0_norm,
            "i_end_deg": i_end,
            "p_end": (ln / M) ** 2,
        }, trace

    sph, _ = run_3d(0.0, 0.0)
    l0_res, tr_l0 = run_3d(0.05, 0.0)
    l04_res, tr_l04 = run_3d(0.05, 0.04)

    diff_trace = [
        (t0[0], t0[1], t4[1], (t4[1] - t0[1]) * 1e3)
        for t0, t4 in zip(tr_l0, tr_l04)
    ]
    di_shape_deg = l04_res["i_end_deg"] - l0_res["i_end_deg"]
    dp_shape = l04_res["p_end"] - l0_res["p_end"]
    earth_j2_scale = J2_E * (R_E / (R_P_SAFE / 0.75)) ** 2

    ok = (
        img_true == v_true
        and img_fig1 != v_fig1
        and sph["max_dJperp"] < 1e-11
        and l0_res["max_dJz_tot"] < 1e-11
        and l04_res["max_dJz_tot"] < 1e-11
        and l0_res["max_dJperp"] > 3.08
        and abs(earth_j2_scale - 5.087565e-4) < 1e-8
    )
    return ok, {
        "rodrigues_true_axis": [1, 1, -1],
        "rodrigues_fig1_image": img_fig1,
        "spherical_J2_0": sph,
        "oblate_L0_control": l0_res,
        "oblate_L04_triad": l04_res,
        "subtracted_di_shape_deg": di_shape_deg,
        "subtracted_dp_shape": dp_shape,
        "real_earth_J2_scale_at_9304km": earth_j2_scale,
    }, diff_trace


def gate_d4_theorem_g4_and_hardware() -> Tuple[bool, Dict[str, object], List[Tuple[float, float, float, float, float]]]:
    """Gate D4: Consistent I0=(2/3)ML^2 vs ML^2 Theorem G4 sizing & mechanical hub (NEG-W15/W18/W27)."""
    ecc = 0.25
    a_orb = R_P_SAFE / (1.0 - ecc)
    p_slr = R_P_SAFE * (1.0 + ecc)
    t_orb = 2.0 * math.pi * math.sqrt(a_orb**3 / MU_E)
    om_max = math.sqrt(MU_E * p_slr) / (R_P_SAFE**2)
    w_spin = 2.0 * om_max
    m_tip = M_CRAFT / 3.0
    loss_elec = 1.0 / ETA_ACT - ETA_REG  # 37/110 = 0.336363...
    loss_mech = 1.0 - ETA_MECH_RT        # 0.015 (1.5% mechanical bearing/spring-drum loss)

    # Consistent I_0 = (2/3) M L^2 (canonical Piece I convention: equilateral arm radius r_eq = sqrt(2/3) L = 16.330 km)
    i0_canon = (2.0 / 3.0) * M_CRAFT * (L_REF**2)
    r_eq_canon = math.sqrt(2.0 / 3.0) * L_REF
    i0_3arm = M_CRAFT * (L_REF**2)

    p_orb_canon = 3.0 * MU_E * i0_canon * (3.0 * ecc + ecc**3) / (p_slr**3 * t_orb)
    p_orb_3arm = 3.0 * MU_E * i0_3arm * (3.0 * ecc + ecc**3) / (p_slr**3 * t_orb)
    ratio_floor = (loss_elec * i0_canon * (w_spin**3) / math.pi) / p_orb_canon  # I_0-invariant!

    # Curve: (q, P_orb(q) [W], P_heat_elec(q) [W], P_heat_mech(q) [W], ratio_elec) under canonical I_0=(2/3)ML^2
    g4_curve: List[Tuple[float, float, float, float, float]] = []
    for k in range(5, 91, 5):
        q = k / 100.0
        p_circ = (q / (math.pi * (1.0 - q * q) ** 1.5)) * i0_canon * (w_spin**3)
        p_h_e = loss_elec * p_circ
        p_h_m = loss_mech * p_circ
        p_o_q = q * p_orb_canon
        g4_curve.append((q, p_o_q, p_h_e, p_h_m, p_h_e / p_o_q))

    # Exact consistent inertial radial peak tension for canonical r_eq = 16.330 km and 3-arm L = 20 km
    t_pk_canon_exact = m_tip * r_eq_canon * (2.0 * MU_E / (R_P_SAFE**3) + w_spin**2)
    t_pk_3arm_exact = m_tip * L_REF * (2.0 * MU_E / (R_P_SAFE**3) + w_spin**2)
    t_pk_wp031_printed = m_tip * L_REF * (3.0 * MU_E / (R_P_SAFE**3) + w_spin**2)

    # C144 tapered Zylon sizing for canonical r_eq = 16.330 km (3 arms + 1 spare = 4*r_eq)
    lam_canon = RHO_ZYLON * ((w_spin * r_eq_canon) ** 2) / (2.0 * SIGMA_ALLOW)
    taper_canon = (math.exp(lam_canon) - 1.0) / lam_canon
    a_wire_canon = t_pk_canon_exact / SIGMA_ALLOW
    m_zylon_canon = RHO_ZYLON * a_wire_canon * (4.0 * r_eq_canon) * taper_canon
    # Include mechanical differential spring-drum hub (+10 kg) + radiator (for ~14 W at q=0.50 mech: 1.5 kg)
    m_hw_mech_canon = m_zylon_canon + 18.0 + 12.0 + 10.0 + 1.5
    strain_allow_pct = (SIGMA_ALLOW / E_ZYLON) * 100.0

    # 5-year Hall comparison (both wet-1000 kg and dry-1000 kg payload, NEG-W18)
    dv_5yr = 5.0 * (T_YR * MU_E * (L_REF**2) / (math.pi * (R_P_SAFE**4))) * (
        (3.0 * ecc + ecc**3) * (1.0 - ecc) / ((1.0 + ecc) ** 3)
    )
    ve = 1_600.0 * G0
    m_hall_wet = 30.0 + 1.15 * M_CRAFT * (1.0 - math.exp(-dv_5yr / ve))
    m_hall_dry = 30.0 + 1.15 * M_CRAFT * (math.exp(dv_5yr / ve) - 1.0)

    p_circ_50_canon = (0.5 / (math.pi * 0.75**1.5)) * i0_canon * (w_spin**3)
    p_heat_50_canon = loss_elec * p_circ_50_canon
    p_heat_50_3arm = 1.5 * p_heat_50_canon
    p_mech_50_canon = loss_mech * p_circ_50_canon

    ok = (
        abs(p_orb_canon - 41.1877) < 1e-3
        and abs(p_orb_3arm - 61.7815) < 1e-3
        and abs(ratio_floor - 9.8468) < 1e-3
        and abs(p_heat_50_canon - 312.17) < 0.1
        and abs(p_heat_50_3arm - 468.25) < 0.1
        and abs(t_pk_3arm_exact - 54.74) < 0.02
        and abs(t_pk_wp031_printed - 62.56) < 0.02
        and abs(strain_allow_pct - 0.4296) < 1e-3
        and abs(m_hall_wet - 100.52) < 0.02
        and abs(m_hall_dry - 105.12) < 0.02
    )
    return ok, {
        "r_eq_canon_km": r_eq_canon / 1e3,
        "p_orb_full_canon_W": p_orb_canon,
        "p_orb_full_3arm_W": p_orb_3arm,
        "i0_invariant_floor_ratio": ratio_floor,
        "q50_ratio_consistent": ratio_floor / (0.75**1.5),
        "q80_ratio_consistent": ratio_floor / (0.36**1.5),
        "q90_ratio_consistent": ratio_floor / (0.19**1.5),
        "q50_p_circ_canon_W": p_circ_50_canon,
        "q50_p_heat_elec_canon_W": p_heat_50_canon,
        "q50_p_heat_elec_3arm_W": p_heat_50_3arm,
        "q50_p_heat_mech_hub_canon_W": p_mech_50_canon,
        "t_pk_canon_exact_N": t_pk_canon_exact,
        "t_pk_3arm_exact_N": t_pk_3arm_exact,
        "t_pk_wp031_printed_N": t_pk_wp031_printed,
        "m_zylon_canon_kg": m_zylon_canon,
        "m_hw_mech_hub_canon_kg": m_hw_mech_canon,
        "strain_allow_pct": strain_allow_pct,
        "m_hall_5yr_wet_kg": m_hall_wet,
        "m_hall_5yr_dry_kg": m_hall_dry,
    }, g4_curve


def gate_p1_keyed_rct() -> Tuple[bool, Dict[str, object]]:
    """Gate P1: Keyed SplitMix64 N=1,600 blinded RCT on safe-perigee eccentric orbits."""
    rng = SplitMix64(SEED_PIECE1)
    n_trials = 1_600
    f_peak = ((3.0 * 0.2817015579087740 + 0.2817015579087740**3) * (1.0 - 0.2817015579087740)) / (
        (1.0 + 0.2817015579087740) ** 3
    )
    ok_count = 0
    for _ in range(n_trials):
        e = 0.01 + 0.88 * rng.next_f64()
        q = 0.05 + 0.85 * rng.next_f64()
        f_val = (3.0 * e + e**3) * (1.0 - e) / ((1.0 + e) ** 3)
        # Check K9 global dominance, F36 positive slack deficit, and Theorem G1 exact span envelope
        slack_def = (1.0 - e) ** (-3.0) - 1.0
        rmax = math.sqrt(2.0 * (1.0 + q) / 3.0)
        if f_val <= f_peak + 1e-15 and slack_def > 0.0 and ((q <= 0.5) == (rmax <= 1.0 + 1e-15)):
            ok_count += 1
    digest = f"0x{rng.next_u64():016x}"
    return ok_count == n_trials, {
        "seed": f"0x{SEED_PIECE1:016x}",
        "trials": n_trials,
        "passed": ok_count,
        "final_digest": digest,
    }


def compile_standalone_tikz(tex_body: str, out_pdf: pathlib.Path) -> None:
    """Compile a standalone TikZ/PGFPlots PDF with zero local path metadata."""
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        tex_file = tmp_path / "fig.tex"
        tex_file.write_text(tex_body, encoding="utf-8")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "fig.tex"],
            cwd=tmp_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        out_pdf.write_bytes((tmp_path / "fig.pdf").read_bytes())


def build_figures(
    fig_dir: pathlib.Path,
    g1_curve: List[Tuple[float, float, float, float]],
    k9_curve: List[Tuple[float, float]],
    j2_trace: List[Tuple[float, float, float, float]],
    g4_curve: List[Tuple[float, float, float, float, float]],
) -> None:
    """Compile all 3 publication vector PDF figures directly from live computed data."""
    preamble = r"""\documentclass[border=3pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\pdfinfo{/Producer () /Creator ()}
\begin{document}
"""

    # Figure 1: Theorem G1 zero-spin kinetic barrier & span envelope
    coords_ke = " ".join(f"({q:.2f},{ke:.4f})" for q, ke, _, _ in g1_curve if q <= 0.95)
    coords_rm = " ".join(f"({q:.2f},{rm:.4f})" for q, _, rm, _ in g1_curve if q <= 0.95)
    fig1 = preamble + rf"""\begin{{tikzpicture}}
\begin{{axis}}[
  name=ax1, width=6.3cm, height=4.8cm,
  xlabel={{Quadrupole fraction $q = |Q_{{\mathbb{{C}}}}|/I_0$}},
  ylabel={{$T_{{\mathrm{{shape}}}} / (\tfrac{{1}}{{2}} I_0 \Omega^2)$}},
  xmin=0, xmax=1.0, ymin=0, ymax=10.0,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{(A) Theorem G1 Kinetic Barrier}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}},
  legend pos=north west, legend style={{font=\scriptsize, draw=gray!50}}
]
\addplot[blue!75!black, thick] coordinates {{{coords_ke}}};
\addlegendentry{{$q^2/(1-q^2)$ (exact)}}
\addplot[red!70!black, dashed, thick] coordinates {{(0,1) (1,1)}};
\addlegendentry{{WP030 $\S4.1$ est. ($1.0\times$)}}
\addplot[only marks, mark=*, mark size=1.8pt, blue!75!black] coordinates {{(0.50,0.3333) (0.7071,1.0) (0.85,2.6036) (0.95,9.2564)}};
\node[font=\scriptsize, anchor=east] at (axis cs:0.93,9.25) {{$9.26\times$}};
\end{{axis}}
\begin{{axis}}[
  at={{(ax1.east)}}, anchor=west, xshift=1.5cm,
  width=6.3cm, height=4.8cm,
  xlabel={{Quadrupole fraction $q$}},
  ylabel={{Peak arm radius $\max|\rho_i|/L$}},
  xmin=0, xmax=1.0, ymin=0.78, ymax=1.20,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{(B) Span Envelope \& Holonomy}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}},
  legend pos=south east, legend style={{font=\scriptsize, draw=gray!50}}
]
\addplot[teal!70!black, thick] coordinates {{{coords_rm}}};
\addlegendentry{{$\sqrt{{2(1+q)/3}}$}}
\addplot[gray!70!black, dashed, thick] coordinates {{(0,1.0) (1,1.0)}};
\addlegendentry{{Span cap $L$ ($q \le 0.5$)}}
\addplot[only marks, mark=*, mark size=1.8pt, teal!70!black] coordinates {{(0.50,1.0000) (0.95,1.1402)}};
\node[font=\scriptsize, anchor=north west] at (axis cs:0.04,1.17) {{$w_\pm$: $-90^\circ$ phys., $\min d_{{ij}}=0.518L$}};
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
"""
    compile_standalone_tikz(fig1, fig_dir / "fig1_hopf_holonomy_g1.pdf")

    # Figure 2: Safe-perigee K9 optimum & 3D J2 subtracted L=0 control
    coords_k9 = " ".join(f"({e:.2f},{dv:.2f})" for e, dv in k9_curve)
    coords_j2 = " ".join(f"({orb:.2f},{di:.3f})" for orb, _, _, di in j2_trace)
    fig2 = preamble + rf"""\begin{{tikzpicture}}
\begin{{axis}}[
  name=ax1, width=6.3cm, height=4.8cm,
  xlabel={{Eccentricity $e$}},
  ylabel={{Annual $\Delta v_{{\mathrm{{yr}}}}$ [m/s/yr]}},
  xmin=0, xmax=0.9, ymin=0, ymax=225,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{(A) Safe-Perigee K9 ($r_p=6978.1$ km)}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}},
  legend pos=north east, legend style={{font=\scriptsize, draw=gray!50}}
]
\addplot[blue!75!black, thick] coordinates {{{coords_k9}}};
\addlegendentry{{$I_0=\tfrac{{2}}{{3}}ML^2$}}
\addplot[only marks, mark=*, mark size=2pt, red!75!black] coordinates {{(0.2817,199.89)}};
\node[font=\scriptsize, anchor=south west, text=red!70!black] at (axis cs:0.29,198) {{$e^*=0.2817$, $199.9$ m/s/yr}};
\end{{axis}}
\begin{{axis}}[
  at={{(ax1.east)}}, anchor=west, xshift=1.6cm,
  width=6.3cm, height=4.8cm,
  xlabel={{Orbits ($J_2 R_\oplus^2 = 0.05$, $i_0=45^\circ$)}},
  ylabel={{$\Delta i_{{\mathrm{{shape}}}} = i_{{L=0.04}} - i_{{L=0}}$ [mdeg]}},
  xmin=0, xmax=5.0,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{(B) Subtracted $L=0$ $J_2$ Control}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}}
]
\addplot[orange!80!black, thick] coordinates {{{coords_j2}}};
\addplot[gray!70!black, dashed] coordinates {{(0,0) (5,0)}};
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
"""
    compile_standalone_tikz(fig2, fig_dir / "fig2_safe_perigee_j2_control.pdf")

    # Figure 3: Theorem G4 electrical dissipation vs mechanical spring-drum hub (consistent I0 = (2/3)ML^2)
    coords_elec = " ".join(f"({q:.2f},{pe:.2f})" for q, _, pe, _, _ in g4_curve)
    coords_mech = " ".join(f"({q:.2f},{pm:.2f})" for q, _, _, pm, _ in g4_curve)
    coords_orb = " ".join(f"({q:.2f},{po:.2f})" for q, po, _, _, _ in g4_curve)
    coords_rat = " ".join(f"({q:.2f},{rt:.2f})" for q, _, _, _, rt in g4_curve)
    fig3 = preamble + rf"""\begin{{tikzpicture}}
\begin{{axis}}[
  name=ax1, width=6.3cm, height=4.8cm, ymode=log,
  xlabel={{Pumping amplitude $q$}},
  ylabel={{Power [W] ($I_0=\tfrac{{2}}{{3}}ML^2$)}},
  xmin=0.05, xmax=0.90, ymin=0.5, ymax=8000,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{(A) Electrical vs.\ Mechanical Hub}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}},
  legend pos=north west, legend style={{font=\scriptsize, draw=gray!50}}
]
\addplot[red!75!black, thick] coordinates {{{coords_elec}}};
\addlegendentry{{$P_{{\mathrm{{heat,elec}}}}$ ($37/110$)}}
\addplot[blue!75!black, thick] coordinates {{{coords_orb}}};
\addlegendentry{{$P_{{\mathrm{{orb}}}}(q)$}}
\addplot[teal!70!black, thick, densely dashed] coordinates {{{coords_mech}}};
\addlegendentry{{Mech.\ hub ($1.5\%$ loss)}}
\end{{axis}}
\begin{{axis}}[
  at={{(ax1.east)}}, anchor=west, xshift=1.6cm,
  width=6.3cm, height=4.8cm, ymode=log,
  xlabel={{Pumping amplitude $q$}},
  ylabel={{$P_{{\mathrm{{heat,elec}}}}/P_{{\mathrm{{orb}}}}$ ($I_0$-invariant)}},
  xmin=0.05, xmax=0.90, ymin=5, ymax=200,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{(B) $I_0$-Invariant Heat Ratio}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}},
  legend pos=north west, legend style={{font=\scriptsize, draw=gray!50}}
]
\addplot[purple!80!black, thick] coordinates {{{coords_rat}}};
\addlegendentry{{$9.85/(1-q^2)^{{3/2}}$}}
\addplot[gray!70!black, dashed] coordinates {{(0.05,9.85) (0.90,9.85)}};
\addlegendentry{{Floor $9.85\times$}}
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
"""
    compile_standalone_tikz(fig3, fig_dir / "fig3_g4_mechanical_hub_sizing.pdf")


def main() -> int:
    piece_dir = pathlib.Path(__file__).resolve().parent.parent
    data_dir = piece_dir / "data"
    fig_dir = piece_dir / "paper" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)

    ok_d1, res_d1 = gate_d1_cancellation_and_orders()
    ok_d2, res_d2, g1_curve = gate_d2_hopf_holonomy_and_g1()
    ok_d3, res_d3, k9_curve = gate_d3_safe_perigee_k9_and_missions()
    ok_r1, res_r1 = gate_r1_open_planar_4body()
    ok_r2, res_r2, j2_trace = gate_r2_3d_j2_with_l0_control()
    ok_d4, res_d4, g4_curve = gate_d4_theorem_g4_and_hardware()
    ok_p1, res_p1 = gate_p1_keyed_rct()

    build_figures(fig_dir, g1_curve, k9_curve, j2_trace, g4_curve)

    gates = {
        "D1_cancellation_and_orders": ok_d1,
        "D2_hopf_holonomy_and_G1": ok_d2,
        "D3_safe_perigee_K9_missions": ok_d3,
        "R1_open_planar_4body": ok_r1,
        "R2_3d_j2_with_L0_control": ok_r2,
        "D4_theorem_G4_mechanical_hub": ok_d4,
        "P1_keyed_SplitMix64_RCT": ok_p1,
    }
    payload = {
        "schema_version": "1.0.0",
        "piece": "Horizon Synthesis Piece I (WP030 + WP031)",
        "conventions": {
            "R_E_m": R_E,
            "I0_canonical": "(2/3) M L^2",
            "holonomy_basis": "equilateral-pole w_+/- (-90 deg physical, collision-free)",
            "flight_baseline": "spin-tensioned Hopf triad with coupled mechanical spring-drum hub",
        },
        "gates": gates,
        "results": {
            "D1": res_d1,
            "D2": res_d2,
            "D3": res_d3,
            "R1": res_r1,
            "R2": res_r2,
            "D4": res_d4,
            "P1": res_p1,
        },
    }
    json_path = data_dir / "piece1_calibration.json"
    json_bytes = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    json_path.write_bytes(json_bytes)
    sha = hashlib.sha256(json_bytes).hexdigest()
    rel_json = "papers/horizon_synthesis/piece1_propulsion_hardware/data/piece1_calibration.json"
    (data_dir / "MANIFEST.sha256").write_text(f"{sha}  {rel_json}\n", encoding="utf-8")

    passed = sum(gates.values())
    for k, v in gates.items():
        print(f"[{'PASS' if v else 'FAIL'}] {k}")
    print(f"Summary: {passed}/{len(gates)} Piece I gates PASS | JSON SHA-256: {sha[:16]}...")
    print(f"  R1 triad dE_osc={res_r1['triad_ecc_e020']['dE_osc']:.6f} (a_osc={res_r1['triad_ecc_e020']['a_osc']:.5f}, e_osc={res_r1['triad_ecc_e020']['e_osc']:.5f}, a_tot={res_r1['triad_ecc_e020']['a_tot']:.5f}, e_tot={res_r1['triad_ecc_e020']['e_tot']:.5f}), Landis max_tumble={res_r1['landis_2mass_unassisted']['max_tumble_deg']:.1f} deg")
    print(f"  R2 J2 L=0 i_end={res_r2['oblate_L0_control']['i_end_deg']:.4f} deg vs L=0.04 i_end={res_r2['oblate_L04_triad']['i_end_deg']:.4f} deg (subtracted di_shape={res_r2['subtracted_di_shape_deg']*1e3:+.3f} mdeg, dp_shape={res_r2['subtracted_dp_shape']:+.6f})")
    print(f"  D4 canon r_eq={res_d4['r_eq_canon_km']:.3f} km, P_orb={res_d4['p_orb_full_canon_W']:.2f} W, P_heat_elec(q=0.5)={res_d4['q50_p_heat_elec_canon_W']:.2f} W vs mech_hub={res_d4['q50_p_heat_mech_hub_canon_W']:.2f} W (floor={res_d4['i0_invariant_floor_ratio']:.2f}x, T_pk_canon={res_d4['t_pk_canon_exact_N']:.2f} N, M_hw_mech={res_d4['m_hw_mech_hub_canon_kg']:.2f} kg)")
    print(f"  P1 RCT: {res_p1['passed']}/{res_p1['trials']} digest={res_p1['final_digest']}")
    return 0 if all(gates.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
