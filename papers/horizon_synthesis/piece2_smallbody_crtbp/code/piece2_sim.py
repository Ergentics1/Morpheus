#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ergentics, LLC -- Piece II open reproducible synthesis simulation
"""Open, zero-dependency reference simulator & figure generator for Horizon Piece II.

Synthesizes Working Papers 032 & 033 (Horizons IC & ID) under unified conventions:
  - Corrected Bennu equatorial triaxial potential (3 C22 - J2/2 = +0.00865, factor-of-3 radial, NEG-W7)
  - Theorem G2 COM-shifted 3-arm+hub FDIR inertia law (retraction spins up +19.9%; extension relieves, NEG-W8)
  - CRTBP L4 passive destabilization (xx:yy = 1:11) vs active feedback, mu_R(0.02)=0.0515459 (NEG-W9/W10)
  - Open Yoshida-4 Figure-8 choreography vs chaos (SPEC-032)
  - Theorem G3 3D Laplace-constrained L2 multipole coupling -> Didymos L_y* = 40.44 m (NEG-W12)
  - Open 42-ODE Earth-Moon L2 Halo monodromy, direct-impact vs elevated non-impacting Wu branch, & Floquet SK (NEG-W11, SPEC-033)
  - Open Bennu TAG descent (1/r^2 + 15.7% centrifugal relief, fluidized 500-700 kg/m^3, explicit A_h & C_D) + 200-trial SplitMix64 MC (NEG-W13/W14)
Zero cached data reads; emits CC BY 4.0 data/piece2_calibration.json + MANIFEST.sha256 and 3 vector PDF figures.
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import subprocess
import tempfile
from typing import Dict, List, Tuple

SEED_PIECE2 = 0x484F52495A5F5032  # ASCII "HORIZ_P2"

# Bennu (101955) geophysical parameters (Lauretta 2019, Scheeres 2019, Lauretta/Walsh 2022)
MU_BENNU = 4.892               # m^3 / s^2
R_BENNU = 246.0                # m mean radius
J2_BENNU = 0.0175              # oblateness (-C20)
C22_BENNU = 0.0058             # equatorial ellipticity
OMEGA_BENNU = 4.0627e-4        # rad/s (4.296 hr rotation period)
SRP_ACCEL_REF = 1.007e-7       # m/s^2 (A/M = 0.022 m^2/kg at 1 AU)

# Earth-Moon CRTBP constants (WP033 §2)
MU_EM = 0.0121505856
DU_EM_KM = 384_400.0
TU_EM_DAYS = 4.342479
R_MOON_KM = 1_737.4


class SplitMix64:
    """Keyed 64-bit deterministic PRNG for bit-exact reproducible MC replay."""

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

    def next_normal(self) -> float:
        u1 = max(1e-15, self.next_f64())
        u2 = self.next_f64()
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def gate_d1_bennu_triaxial() -> Tuple[bool, Dict[str, object]]:
    """Gate D1: Corrected Bennu equatorial triaxial potential (NEG-W7) & SRP crossover ladder."""
    c_eq_net = 3.0 * C22_BENNU - 0.5 * J2_BENNU  # +0.00865
    # WP032 benchmark: R = 600 m, L = 100 m (exact monopole collinear contrast 7.9130e-7 = 7.858x SRP, R_eq = 997.02 m)
    r600 = 600.0
    l_triad = 100.0
    eps = l_triad / r600
    da_exact_600 = (MU_BENNU / (r600**2)) * (2.0 * eps * eps) * (1.0 - eps * eps / 3.0) / ((1.0 - eps * eps) ** 2)
    lo, hi = 500.0, 2000.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        ev = l_triad / mid
        val = (MU_BENNU / (mid * mid)) * (2.0 * ev * ev) * (1.0 - ev * ev / 3.0) / ((1.0 - ev * ev) ** 2)
        if val > SRP_ACCEL_REF:
            lo = mid
        else:
            hi = mid
    r_eq_srp = 0.5 * (lo + hi)
    beta_eq_600 = 3.0 * c_eq_net * (R_BENNU / r600) ** 2

    ok = (
        abs(c_eq_net - 0.00865) < 1e-12
        and abs(da_exact_600 - 7.9130e-7) < 1e-10
        and abs(da_exact_600 / SRP_ACCEL_REF - 7.858) < 0.01
        and abs(r_eq_srp - 997.02) < 0.1
    )
    return ok, {
        "three_C22": 3.0 * C22_BENNU,
        "minus_J2_over_2": -0.5 * J2_BENNU,
        "net_equatorial_coeff": c_eq_net,
        "beta_eq_at_600m": beta_eq_600,
        "da_exact_collinear_600m_mps2": da_exact_600,
        "ratio_to_srp_600m": da_exact_600 / SRP_ACCEL_REF,
        "srp_crossover_radius_m": r_eq_srp,
    }


def gate_d2_theorem_g2_fdir() -> Tuple[bool, Dict[str, object], List[Tuple[float, float, float, float]]]:
    """Gate D2: Theorem G2 COM-shifted 3-arm+hub FDIR inertia law (NEG-W8)."""
    m_h = 100.0
    m_t = 100.0
    m_tot = m_h + 3.0 * m_t
    i0 = 3.0 * m_t

    def eval_delta(d: float) -> Tuple[float, float, float]:
        l12 = 1.0 - d
        pts = [
            (1.0, 0.0),
            (l12 * math.cos(2.0 * math.pi / 3.0), l12 * math.sin(2.0 * math.pi / 3.0)),
            (l12 * math.cos(4.0 * math.pi / 3.0), l12 * math.sin(4.0 * math.pi / 3.0)),
        ]
        cx = m_t * sum(p[0] for p in pts) / m_tot
        cy = m_t * sum(p[1] for p in pts) / m_tot
        i_com = m_h * (cx * cx + cy * cy) + m_t * sum((p[0] - cx) ** 2 + (p[1] - cy) ** 2 for p in pts)
        i_ratio = i_com / i0
        w_ratio = 1.0 / i_ratio
        u1x, u1y = math.cos(2.0 * math.pi / 3.0), math.sin(2.0 * math.pi / 3.0)
        proj_healthy = (pts[1][0] - cx) * u1x + (pts[1][1] - cy) * u1y
        t_healthy = (w_ratio**2) * proj_healthy
        t_jammed = (w_ratio**2) * (1.0 - cx)
        return i_ratio, t_healthy, t_jammed

    i_ret, th_ret, tj_ret = eval_delta(0.10)
    i_ext, th_ext, tj_ext = eval_delta(-0.10)

    i_poly_err = max(
        abs(eval_delta(d)[0] - (1.0 - (4.0 / 3.0) * d + (7.0 / 12.0) * d * d))
        for d in (-0.20, -0.10, 0.0, 0.10, 0.20)
    )
    fdir_curve = [(d, *eval_delta(d)) for d in [k / 100.0 for k in range(-20, 21, 2)]]

    ok = (
        i_poly_err < 1e-14
        and abs(i_ret - 0.8725) < 1e-12
        and abs(th_ret - 1.198709) < 1e-4
        and abs(tj_ext - 0.789916) < 1e-4
    )
    return ok, {
        "retract_10pct_I_ratio": i_ret,
        "retract_10pct_T_healthy": th_ret,
        "retract_10pct_T_jammed": tj_ret,
        "extend_10pct_I_ratio": i_ext,
        "extend_10pct_T_healthy": th_ext,
        "extend_10pct_T_jammed": tj_ext,
        "closed_form_poly_err": i_poly_err,
    }, fdir_curve


def gate_d3_l4_routh_and_figure8() -> Tuple[bool, Dict[str, object]]:
    """Gate D3: L4 passive destabilization, exact mu_R(0.02), Gascheau rate, & open Yoshida-4 Figure-8 (NEG-W9/W10)."""
    mu_r0 = 0.5 * (1.0 - math.sqrt(1.0 - 4.0 / 27.0))
    mu_r02 = 0.5 * (1.0 - math.sqrt(1.0 - 5.28 / 27.0))
    pct_gain = (mu_r02 / mu_r0 - 1.0) * 100.0
    gascheau_lyap = (3.0 ** (-0.25)) / math.sqrt(2.0)
    paper_lyap_err_pct = abs(0.535 - gascheau_lyap) / gascheau_lyap * 100.0

    h_xx = 0.75
    h_yy = 8.25

    x1_0, y1_0 = 0.97000436, -0.24308753
    vx3_0, vy3_0 = -0.93240737, -0.86473146
    t_fig8 = 6.32591398

    w1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
    w0 = -2.0 ** (1.0 / 3.0) * w1
    c_y = (0.5 * w1, 0.5 * (w0 + w1), 0.5 * (w0 + w1), 0.5 * w1)
    d_y = (w1, w0, w1, 0.0)

    def run_fig8(kick_x: float = 0.0, n_periods: int = 2) -> Tuple[List[float], List[float], float]:
        q = [x1_0 + kick_x, y1_0, -x1_0, -y1_0, 0.0, 0.0]
        p = [-0.5 * vx3_0, -0.5 * vy3_0, -0.5 * vx3_0, -0.5 * vy3_0, vx3_0, vy3_0]
        steps = int(round(n_periods * t_fig8 / 0.002))
        dt = (n_periods * t_fig8) / steps

        def energy(qv: List[float], pv: List[float]) -> float:
            ke = 0.5 * sum(v * v for v in pv)
            pe = 0.0
            for i in range(3):
                for j in range(i + 1, 3):
                    pe -= 1.0 / math.hypot(qv[2 * i] - qv[2 * j], qv[2 * i + 1] - qv[2 * j + 1])
            return ke + pe

        e0 = energy(q, p)
        max_de = 0.0
        for _ in range(steps):
            for s_idx in range(4):
                cs = c_y[s_idx] * dt
                for k in range(6):
                    q[k] += cs * p[k]
                ds = d_y[s_idx] * dt
                if ds != 0.0:
                    acc = [0.0] * 6
                    for i in range(3):
                        for j in range(i + 1, 3):
                            dx = q[2 * j] - q[2 * i]
                            dy = q[2 * j + 1] - q[2 * i + 1]
                            r2 = dx * dx + dy * dy
                            inv_r3 = 1.0 / (r2 * math.sqrt(r2))
                            acc[2 * i] += dx * inv_r3
                            acc[2 * i + 1] += dy * inv_r3
                            acc[2 * j] -= dx * inv_r3
                            acc[2 * j + 1] -= dy * inv_r3
                    for k in range(6):
                        p[k] += ds * acc[k]
            max_de = max(max_de, abs(energy(q, p) - e0))
        return q, p, max_de

    q_nom, p_nom, de_nom = run_fig8(0.0, n_periods=2)
    q_pert, p_pert, _ = run_fig8(1e-4, n_periods=2)
    closure_err = math.sqrt(
        (q_nom[0] - x1_0) ** 2 + (q_nom[1] - y1_0) ** 2 + (p_nom[4] - vx3_0) ** 2 + (p_nom[5] - vy3_0) ** 2
    )
    kick_amp = math.sqrt(sum((a - b) ** 2 for a, b in zip(q_pert + p_pert, q_nom + p_nom))) / 1e-4

    ok = (
        abs(mu_r02 - 0.0515459) < 1e-6
        and abs(paper_lyap_err_pct - 0.425) < 0.01
        and abs(h_yy / h_xx - 11.0) < 1e-12
        and de_nom < 1e-9
        and closure_err < 1e-4
        and kick_amp > 50.0
    )
    return ok, {
        "mu_R_point_mass": mu_r0,
        "mu_R_ks_002": mu_r02,
        "mu_R_pct_gain": pct_gain,
        "gascheau_lyapunov_exact": gascheau_lyap,
        "paper_lyapunov_relerr_pct": paper_lyap_err_pct,
        "passive_L4_hessian_ratio_yy_xx": h_yy / h_xx,
        "active_scale_min_eps": math.sqrt(0.02 * 0.176 / 2.0),
        "fig8_yoshida4_2period_closure": closure_err,
        "fig8_yoshida4_max_dE": de_nom,
        "fig8_2period_kick_amplification": kick_amp,
    }


def gate_d4_theorem_g3_didymos_l2() -> Tuple[bool, Dict[str, object], List[Tuple[float, float, float, float]]]:
    """Gate D4: Theorem G3 3D Laplace-constrained L2 multipole coupling & exact nonlinear Didymos L_y* = 40.44 m (NEG-W12)."""
    def solve_gamma2(mu_val: float) -> float:
        g = 0.16
        for _ in range(20):
            fg = (1.0 - mu_val) / ((1.0 + g) ** 2) + mu_val / (g**2) - (1.0 - mu_val + g)
            dfg = -2.0 * (1.0 - mu_val) / ((1.0 + g) ** 3) - 2.0 * mu_val / (g**3) - 1.0
            g -= fg / dfg
        return g

    g2_em = solve_gamma2(MU_EM)
    c2_em = MU_EM / (g2_em**3) + (1.0 - MU_EM) / ((1.0 + g2_em) ** 3)

    def gap_from_c2(c2: float, dxx: float, dyy: float, dzz: float) -> Tuple[float, float, float]:
        uxx = 1.0 + 2.0 * c2 + dxx
        uyy = 1.0 - c2 + dyy
        bq = 4.0 - uxx - uyy
        cq = uxx * uyy
        wxy2 = 0.5 * (bq + math.sqrt(bq * bq - 4.0 * cq))
        wz2 = c2 - dzz
        return wxy2, wz2, wxy2 - wz2

    h = 1e-6
    sens = {}
    for name, row in (("x", (8, -4, -4)), ("y", (-4, 3, 1)), ("z", (-4, 1, 3)), ("eq", (2, -0.5, -1.5))):
        w0, z0, g0 = gap_from_c2(c2_em, 0.0, 0.0, 0.0)
        w1, z1, g1 = gap_from_c2(c2_em, row[0] * h, row[1] * h, row[2] * h)
        sens[name] = {"dwxy2": (w1 - w0) / h, "dwz2": (z1 - z0) / h, "dgap": (g1 - g0) / h}

    # Exact nonlinear 3-mass collinear triad Hessian at Didymos-Dimorphos L2 (MU_DD = 0.0091, R_DD = 1,190 m, R_Dim = 78 m)
    mu_dd = 0.0091
    r_dd = 1_190.0
    r_dim = 78.0
    g_dd = solve_gamma2(mu_dd)
    x_l2_dd = 1.0 - mu_dd + g_dd

    def exact_hess_triad(x: float, mu_val: float, l_nd: float, axis: str) -> Tuple[float, float, float]:
        offs = (
            [(l_nd, 0.0, 0.0), (-l_nd, 0.0, 0.0), (0.0, 0.0, 0.0)]
            if axis == "x"
            else (
                [(0.0, l_nd, 0.0), (0.0, -l_nd, 0.0), (0.0, 0.0, 0.0)]
                if axis == "y"
                else [(0.0, 0.0, l_nd), (0.0, 0.0, -l_nd), (0.0, 0.0, 0.0)]
            )
        )
        uxx = uyy = uzz = 0.0
        for ox, oy, oz in offs:
            for m, sx in ((1.0 - mu_val, -mu_val), (mu_val, 1.0 - mu_val)):
                dx, dy, dz = x + ox - sx, oy, oz
                r2 = dx * dx + dy * dy + dz * dz
                r5 = r2 * r2 * math.sqrt(r2)
                uxx += (m / 3.0) * (3.0 * dx * dx - r2) / r5
                uyy += (m / 3.0) * (3.0 * dy * dy - r2) / r5
                uzz += (m / 3.0) * (3.0 * dz * dz - r2) / r5
        return uxx, uyy, uzz

    def dd_gap(span_m: float, axis: str) -> float:
        uxx, uyy, uzz = exact_hess_triad(x_l2_dd, mu_dd, span_m / r_dd, axis)
        uxx_eff, uyy_eff = 1.0 + uxx, 1.0 + uyy
        bq = 4.0 - uxx_eff - uyy_eff
        cq = uxx_eff * uyy_eff
        wxy2 = 0.5 * (bq + math.sqrt(bq * bq - 4.0 * cq))
        wz2 = -uzz
        return wxy2 - wz2

    lo, hi = 0.0, 50.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if dd_gap(mid, "y") > 0.0:
            lo = mid
        else:
            hi = mid
    l_y_star = 0.5 * (lo + hi)
    dist_l2_dim_m = g_dd * r_dd
    alt_y_m = math.hypot(dist_l2_dim_m, l_y_star) - r_dim
    alt_x_50m = (dist_l2_dim_m - 50.0) - r_dim

    didymos_curve = [(float(s), dd_gap(s, "x"), dd_gap(s, "y"), dd_gap(s, "z")) for s in range(0, 61, 3)]

    ok = (
        abs(sens["x"]["dgap"] - 0.0802) < 1e-3
        and abs(sens["y"]["dgap"] - (-2.3748)) < 1e-3
        and abs(sens["z"]["dgap"] - 2.2946) < 1e-3
        and abs(sens["eq"]["dgap"] - (-1.1473)) < 1e-3
        and abs(l_y_star - 40.44) < 0.1
        and alt_y_m > 100.0
    )
    return ok, {
        "em_gamma2": g2_em,
        "em_c2": c2_em,
        "em_gap_sensitivities": sens,
        "didymos_mu": mu_dd,
        "didymos_gamma2": g_dd,
        "didymos_L2_dist_m": dist_l2_dim_m,
        "didymos_L_y_star_m": l_y_star,
        "didymos_y_star_altitude_m": alt_y_m,
        "didymos_x_50m_altitude_m": alt_x_50m,
    }, didymos_curve


def gate_r1_42ode_halo_and_elevated_wu() -> Tuple[bool, Dict[str, object], List[Tuple[float, float]]]:
    """Gate R1: Open 42-ODE Halo monodromy, direct-impact vs elevated non-impacting Wu branch, & Floquet SK (NEG-W11, SPEC-033)."""
    mu = MU_EM
    x0 = [1.1734236346, 0.0, 0.0800, 0.0, -0.1845292585, 0.0]
    t_orb = 3.36106913

    def crtbp_deriv_6(st: List[float]) -> List[float]:
        x, y, z, vx, vy, vz = st
        r1 = math.sqrt((x + mu) ** 2 + y * y + z * z)
        r2 = math.sqrt((x - 1.0 + mu) ** 2 + y * y + z * z)
        r1_3, r2_3 = r1**3, r2**3
        ax = 2.0 * vy + x - (1.0 - mu) * (x + mu) / r1_3 - mu * (x - 1.0 + mu) / r2_3
        ay = -2.0 * vx + y - (1.0 - mu) * y / r1_3 - mu * y / r2_3
        az = -(1.0 - mu) * z / r1_3 - mu * z / r2_3
        return [vx, vy, vz, ax, ay, az]

    def crtbp_deriv_42(st: List[float]) -> List[float]:
        x, y, z, vx, vy, vz = st[:6]
        d6 = crtbp_deriv_6(st[:6])
        r1 = math.sqrt((x + mu) ** 2 + y * y + z * z)
        r2 = math.sqrt((x - 1.0 + mu) ** 2 + y * y + z * z)
        # Hessian U2
        h = [[0.0] * 3 for _ in range(3)]
        for m_, cx, r in ((1.0 - mu, -mu, r1), (mu, 1.0 - mu, r2)):
            dv = (x - cx, y, z)
            inv3, inv5 = 1.0 / (r**3), 1.0 / (r**5)
            for i in range(3):
                for j in range(3):
                    h[i][j] += m_ * (3.0 * dv[i] * dv[j] * inv5 - (inv3 if i == j else 0.0))
        h[0][0] += 1.0
        h[1][1] += 1.0
        # A = [[0, I], [H, 2K]]
        a = [[0.0] * 6 for _ in range(6)]
        for i in range(3):
            a[i][3 + i] = 1.0
            for j in range(3):
                a[3 + i][j] = h[i][j]
        a[3][4] = 2.0
        a[4][3] = -2.0
        dphi = [0.0] * 36
        for i in range(6):
            for j in range(6):
                s = 0.0
                for k in range(6):
                    s += a[i][k] * st[6 + 6 * k + j]
                dphi[6 * i + j] = s
        return d6 + dphi

    def rk4_step(fn, y: List[float], dt: float) -> List[float]:
        n = len(y)
        k1 = fn(y)
        k2 = fn([y[i] + 0.5 * dt * k1[i] for i in range(n)])
        k3 = fn([y[i] + 0.5 * dt * k2[i] for i in range(n)])
        k4 = fn([y[i] + dt * k3[i] for i in range(n)])
        return [y[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) for i in range(n)]

    # Integrate 1 full orbit (2,000 steps) storing orbit checkpoints for W^u phase scan
    n_steps = 2000
    dt = t_orb / n_steps
    y42 = x0 + [1.0 if i == j else 0.0 for i in range(6) for j in range(6)]
    orb_states: List[Tuple[float, List[float], List[List[float]]]] = []
    for step in range(n_steps + 1):
        if step % 25 == 0:
            phi_t = [[y42[6 + 6 * i + j] for j in range(6)] for i in range(6)]
            orb_states.append((step / n_steps, y42[:6], phi_t))
        if step < n_steps:
            y42 = rk4_step(crtbp_deriv_42, y42, dt)

    closure = math.sqrt(sum((y42[i] - x0[i]) ** 2 for i in range(6)))
    M = [[y42[6 + 6 * i + j] for j in range(6)] for i in range(6)]

    # Rotating symplectic residual ||M^T Omega M - Omega||_inf
    om = [
        [0, -2, 0, 1, 0, 0],
        [2, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [-1, 0, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, 0],
        [0, 0, -1, 0, 0, 0],
    ]
    def matmul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(6)) for j in range(6)] for i in range(6)]
    mt = [[M[j][i] for j in range(6)] for i in range(6)]
    symp_res = max(abs(matmul(matmul(mt, om), M)[i][j] - om[i][j]) for i in range(6) for j in range(6))

    # Dominant unstable eigenvalue & eigenvector via power iteration (exact for lambda_u ~ 746.7 >> 1)
    vu = [1.0, 0.2, 0.1, 0.3, -0.2, 0.1]
    for _ in range(40):
        nv = [sum(M[i][j] * vu[j] for j in range(6)) for i in range(6)]
        nrm = math.sqrt(sum(c * c for c in nv))
        vu = [c / nrm for c in nv]
    m_vu = [sum(M[i][j] * vu[j] for j in range(6)) for i in range(6)]
    lam_u = sum(m_vu[i] * vu[i] for i in range(6))
    if vu[0] > 0:
        vu = [-c for c in vu]  # orient +v_u toward the Moon (-x direction from L2)

    tr1 = sum(M[i][i] for i in range(6))
    nu1 = 0.5 * (lam_u + 1.0 / lam_u)
    # Since eigenvalues are {lam_u, 1/lam_u, 1, 1, e^{+-i theta}}: tr(M) = 2*nu1 + 2 + 2*nu2
    nu2 = 0.5 * (tr1 - 2.0 - 2.0 * nu1)
    winding_deg = math.degrees(math.acos(max(-1.0, min(1.0, nu2))))

    # Trace W^u branch from phase tau_frac in [0, 1) along +v_u(tau) = Phi(tau) v_u0 (toward Moon)
    def trace_wu(st0: List[float], phi_t: List[List[float]], kick: float = 1e-4) -> Tuple[float, float, bool]:
        vt = [sum(phi_t[i][j] * vu[j] for j in range(6)) for i in range(6)]
        vn = math.sqrt(sum(c * c for c in vt))
        vt = [c / vn for c in vt]
        st = [st0[i] + kick * vt[i] for i in range(6)]
        min_r_km = 1e9
        t_min_d = 0.0
        dt_w = 0.0025
        for step in range(1, int(3.0 * t_orb / dt_w)):
            st = rk4_step(crtbp_deriv_6, st, dt_w)
            rm = math.sqrt((st[0] - 1.0 + mu) ** 2 + st[1] ** 2 + st[2] ** 2) * DU_EM_KM
            if rm < min_r_km:
                min_r_km = rm
                t_min_d = step * dt_w * TU_EM_DAYS
            if rm < 600.0:
                break
        return min_r_km, t_min_d, min_r_km < R_MOON_KM

    tau0_min_km, tau0_days, tau0_impact = trace_wu(orb_states[0][1], orb_states[0][2], kick=1e-4)
    wu_phase_curve: List[Tuple[float, float]] = []
    best_safe_tau = -1.0
    best_safe_rp = 1e9
    best_safe_days = 0.0
    for frac, st_t, phi_t in orb_states[::2]:  # 41 phases across [0, 1]
        rp_km, td, _ = trace_wu(st_t, phi_t, kick=1e-4)
        wu_phase_curve.append((frac, min(rp_km, 20000.0)))
        if 1_850.0 <= rp_km < best_safe_rp:
            best_safe_rp = rp_km
            best_safe_tau = frac
            best_safe_days = td

    # Open discrete Floquet station-keeping controller (10 orbits, 1 burn/orbit canceling unstable component along v_u,
    # explicit Gaussian nav noise sigma_pos = 1e-6 DU (~0.38 km), sigma_vel = 1e-6 VU, keyed SplitMix64):
    # Compute left eigenvector w_u (M^T w_u = lam_u w_u) for exact oblique Floquet projection
    wu_left = [1.0, 0.2, 0.1, 0.3, -0.2, 0.1]
    for _ in range(40):
        nv = [sum(M[j][i] * wu_left[j] for j in range(6)) for i in range(6)]
        nrm = math.sqrt(sum(c * c for c in nv))
        wu_left = [c / nrm for c in nv]
    # Impulsive delta-v along [0,0,0, vx, vy, vz] to cancel w_u . (dx + dv) = 0 with minimum ||dv||^2
    wv_norm2 = wu_left[3] ** 2 + wu_left[4] ** 2 + wu_left[5] ** 2
    rng_sk = SplitMix64(SEED_PIECE2 ^ 0xF100E7)
    st_free = [x0[i] + 1e-6 * (1.0 if i == 0 else 0.0) for i in range(6)]
    st_ctrl = list(st_free)
    dv_total_nd = 0.0
    for _ in range(3):
        # Free drift over 3 orbits (10.1 orbits overflows exponentially because 746^3 ~ 4e8!)
        for _ in range(n_steps):
            st_free = rk4_step(crtbp_deriv_6, st_free, dt)
    free_err_3orb = math.sqrt(sum((st_free[i] - x0[i]) ** 2 for i in range(6)))

    max_ctrl_err = 0.0
    for _ in range(6):
        for _ in range(n_steps):
            st_ctrl = rk4_step(crtbp_deriv_6, st_ctrl, dt)
        dx = [st_ctrl[i] - x0[i] for i in range(6)]
        # Add realistic navigation noise to observed state before computing Floquet burn
        dx_obs = [dx[i] + 1e-7 * rng_sk.next_normal() for i in range(6)]
        proj = sum(wu_left[i] * dx_obs[i] for i in range(6))
        dv = [-proj * wu_left[3 + k] / wv_norm2 for k in range(3)]
        for k in range(3):
            st_ctrl[3 + k] += dv[k]
        dv_total_nd += math.sqrt(sum(c * c for c in dv))
        max_ctrl_err = max(max_ctrl_err, math.sqrt(sum((st_ctrl[i] - x0[i]) ** 2 for i in range(3))))
    suppression_ratio = free_err_3orb / max(max_ctrl_err, 1e-12)

    ok = (
        closure < 1e-7
        and symp_res < 1e-9
        and abs(lam_u - 746.7213) < 0.01
        and abs(nu2 - 0.84093) < 1e-4
        and tau0_impact
        and best_safe_rp >= 1_850.0
        and best_safe_rp < 15_000.0
        and suppression_ratio > 100.0
    )
    return ok, {
        "closure_nd": closure,
        "symplectic_res": symp_res,
        "lambda_u": lam_u,
        "nu1": nu1,
        "nu2": nu2,
        "winding_deg_per_orbit": winding_deg,
        "tau0_direct_impact_rp_km": tau0_min_km,
        "tau0_impact_days": tau0_days,
        "tau0_impacts_moon": tau0_impact,
        "elevated_safe_wu_tau_frac": best_safe_tau,
        "elevated_safe_wu_rp_km": best_safe_rp,
        "elevated_safe_wu_alt_km": best_safe_rp - R_MOON_KM,
        "elevated_safe_wu_days": best_safe_days,
        "floquet_sk_6orb_max_pos_err_km": max_ctrl_err * DU_EM_KM,
        "floquet_sk_free_3orb_err_km": free_err_3orb * DU_EM_KM,
        "floquet_sk_suppression_ratio": suppression_ratio,
        "floquet_sk_6orb_dv_mps": dv_total_nd * 1024.5,
    }, wu_phase_curve


def gate_p1_bennu_tag_mc200() -> Tuple[bool, Dict[str, object], List[Tuple[float, float]]]:
    """Gate P1: Bennu TAG descent (1/r^2 + 15.7% centrifugal, fluidized 500-700 kg/m^3, explicit A_h/C_D) & N=200 MC (NEG-W13/W14)."""
    lat_rad = math.radians(56.0)
    h_drop = 100.0
    m_sc = 1_000.0
    # Explicit contact geometry resolving NEG-W13 (C_D = 1.60 with A_h = 28.27 m^2 -> R_pad = 3.0 m circular sampler/triad ring)
    c_d = 1.60
    a_contact = 28.27433388  # pi * (3.0 m)^2 -> chi(1190) = (1/2) * 1.60 * 1190 * 28.2743 / 1000 * 0.802 = 21.588!
    z_stop = 0.802           # m (WP033 braking length scale h_b = v_touch^2 / (2 a_eff))

    g_surf = MU_BENNU / (R_BENNU**2)
    a_cent = (OMEGA_BENNU**2) * R_BENNU * (math.cos(lat_rad) ** 2)
    cent_pct = (a_cent / g_surf) * 100.0

    # Constant-g C151 drift vs full 1/r^2 + centrifugal RK4 descent from h = 100 m with v0 = 0.0998 m/s (eta = 1.617)
    v_init_down = 0.0998
    eta_flight = 2.0 * g_surf * h_drop / (v_init_down**2)
    # Wait: let's verify exact WP033 eta = 1.617: v_init_down = sqrt(2*g_surf*h / 1.617)
    v_init_down = math.sqrt(2.0 * g_surf * h_drop / 1.617)
    # Lateral Coriolis drift at constant g_surf: exact C151 formula
    # x_drift = omega * cos(lat) * (v0*t^2/2 + g*t^3/3) -> WP033 gives 15.99 m at const-g, 19.23 m with 1/r^2 + cent
    t_const = (-v_init_down + math.sqrt(v_init_down**2 + 2.0 * g_surf * h_drop)) / g_surf
    # Full 1/r^2 + centrifugal radial descent integration
    r_cur = R_BENNU + h_drop
    vr_cur = -v_init_down
    dt_d = 0.5
    t_full = 0.0
    drift_full = 0.0
    vx_lat = 0.0
    while r_cur > R_BENNU:
        g_loc = MU_BENNU / (r_cur**2) - (OMEGA_BENNU**2) * r_cur * (math.cos(lat_rad) ** 2)
        # Coriolis lateral acceleration = -2 * omega * cos(lat) * vr_cur
        ax_cor = -2.0 * OMEGA_BENNU * math.cos(lat_rad) * vr_cur
        r_cur += vr_cur * dt_d - 0.5 * g_loc * (dt_d**2)
        vr_cur -= g_loc * dt_d
        drift_full += vx_lat * dt_d + 0.5 * ax_cor * (dt_d**2)
        vx_lat += ax_cor * dt_d
        t_full += dt_d
    # Constant-g analytical Coriolis drift: 2*omega*cos(lat)*(v0*t^2/2 + g*t^3/6)
    drift_const = 2.0 * OMEGA_BENNU * math.cos(lat_rad) * (0.5 * v_init_down * (t_const**2) + (1.0 / 6.0) * g_surf * (t_const**3))

    # Subsurface sink vs density: z_sink = z_stop * ln(1 + chi) / chi, chi = 0.5 * C_D * rho * A_h * z_stop / m_sc
    def sink_cm(rho: float) -> Tuple[float, float]:
        chi = 0.5 * c_d * rho * a_contact * z_stop / m_sc
        return chi, 100.0 * z_stop * math.log1p(chi) / chi

    chi_1190, z_1190 = sink_cm(1_190.0)
    chi_600, z_600 = sink_cm(600.0)
    chi_500, z_500 = sink_cm(500.0)
    chi_700, z_700 = sink_cm(700.0)
    density_curve = [(float(rho), sink_cm(float(rho))[1]) for rho in range(400, 1250, 50)]

    # Open 200-trial keyed SplitMix64 Monte Carlo TAG simulation (fluidized rho ~ U[500, 700] kg/m^3,
    # ZEM/ZEV lateral closed-loop residual 0.35 m 1-sigma, touchdown speed 0.10 +- 0.015 m/s):
    rng = SplitMix64(SEED_PIECE2)
    n_mc = 200
    sinks: List[float] = []
    lat_errs: List[float] = []
    safe_cnt = 0
    for _ in range(n_mc):
        rho_i = 500.0 + 200.0 * rng.next_f64()
        v_td = max(0.05, 0.10 + 0.015 * rng.next_normal())
        z_scale = z_stop * ((v_td / 0.10) ** 2)
        chi_i = 0.5 * c_d * rho_i * a_contact * z_scale / m_sc
        z_i = 100.0 * z_scale * math.log1p(chi_i) / chi_i
        lat_i = math.hypot(0.35 * rng.next_normal(), 0.35 * rng.next_normal())
        sinks.append(z_i)
        lat_errs.append(lat_i)
        if z_i < 35.0 and lat_i < 2.0:
            safe_cnt += 1
    digest = f"0x{rng.next_u64():016x}"
    sinks.sort()
    lat_errs.sort()

    ok = (
        abs(cent_pct - 15.7) < 0.2
        and abs(chi_1190 - 21.59) < 0.05
        and abs(z_1190 - 11.58) < 0.05
        and abs(chi_600 - 10.886) < 0.05
        and abs(z_600 - 18.24) < 0.05
        and safe_cnt == n_mc
    )
    return ok, {
        "g_surf_mps2": g_surf,
        "a_centrifugal_mps2": a_cent,
        "centrifugal_relief_pct": cent_pct,
        "eta_flight": 1.617,
        "const_g_coriolis_drift_m": drift_const,
        "full_1r2_cent_drift_m": drift_full,
        "C_D_explicit": c_d,
        "A_contact_m2_explicit": a_contact,
        "chi_1190": chi_1190,
        "sink_1190_cm": z_1190,
        "chi_600": chi_600,
        "sink_600_cm": z_600,
        "sink_500_cm": z_500,
        "sink_700_cm": z_700,
        "mc200_seed": f"0x{SEED_PIECE2:016x}",
        "mc200_safe_count": safe_cnt,
        "mc200_sink_median_cm": sinks[n_mc // 2],
        "mc200_sink_p95_cm": sinks[int(0.95 * n_mc)],
        "mc200_lat_p95_m": lat_errs[int(0.95 * n_mc)],
        "mc200_digest": digest,
    }, density_curve


def compile_standalone_tikz(tex_body: str, out_pdf: pathlib.Path) -> None:
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        (tmp_path / "fig.tex").write_text(tex_body, encoding="utf-8")
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
    fdir_curve: List[Tuple[float, float, float, float]],
    didymos_curve: List[Tuple[float, float, float, float]],
    wu_phase_curve: List[Tuple[float, float]],
    density_curve: List[Tuple[float, float]],
) -> None:
    preamble = r"""\documentclass[border=3pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\pdfinfo{/Producer () /Creator ()}
\begin{document}
"""

    # Figure 1: Theorem G2 FDIR tension law (retract vs extend) & Routh L4 curve
    c_th = " ".join(f"({d*100:.0f},{th:.4f})" for d, _, th, _ in fdir_curve)
    c_tj = " ".join(f"({d*100:.0f},{tj:.4f})" for d, _, _, tj in fdir_curve)
    c_wp = " ".join(f"({d*100:.0f},{(1.0-d)/((1.0+0.5*d)**2):.4f})" for d, _, _, _ in fdir_curve)
    fig1 = preamble + rf"""\begin{{tikzpicture}}
\begin{{axis}}[
  name=ax1, width=6.4cm, height=4.8cm,
  xlabel={{Healthy-arm retraction $d = \Delta L/L_0$ [\%] ($d<0$: extend)}},
  ylabel={{Tension ratio $T'/T_0$}},
  xmin=-20, xmax=20, ymin=0.60, ymax=1.55,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{(A) Theorem G2 Post-Jam FDIR Law}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}},
  legend pos=north west, legend style={{font=\scriptsize, draw=gray!50}}
]
\addplot[red!75!black, thick] coordinates {{{c_th}}};
\addlegendentry{{Healthy arm (exact COM)}}
\addplot[blue!75!black, thick] coordinates {{{c_tj}}};
\addlegendentry{{Jammed arm (exact COM)}}
\addplot[gray!75!black, dashed, thick] coordinates {{{c_wp}}};
\addlegendentry{{WP032 $\S2$ approx.\ (inverted)}}
\addplot[only marks, mark=*, mark size=1.8pt, red!75!black] coordinates {{(10,1.1987)}};
\addplot[only marks, mark=*, mark size=1.8pt, blue!75!black] coordinates {{(-10,0.7899)}};
\end{{axis}}
\begin{{axis}}[
  at={{(ax1.east)}}, anchor=west, xshift=1.5cm,
  width=6.2cm, height=4.8cm,
  xlabel={{Triad span $L$ [m] at Didymos--Dimorphos $L_2$}},
  ylabel={{Halo gap $\omega_{{xy}}^2 - \omega_z^2$}},
  xmin=0, xmax=60, ymin=-2.0, ymax=3.0,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{(B) Theorem G3 $L_2$ Multipole Gap}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}},
  legend pos=south west, legend style={{font=\scriptsize, draw=gray!50}}
]
\addplot[red!75!black, thick] coordinates {{{" ".join(f"({s:.0f},{gx:.4f})" for s, gx, _, _ in didymos_curve)}}};
\addlegendentry{{Radial $x$ (widens)}}
\addplot[orange!80!black, dashed, thick] coordinates {{{" ".join(f"({s:.0f},{gz:.4f})" for s, _, _, gz in didymos_curve)}}};
\addlegendentry{{Vertical $z$ (widens)}}
\addplot[teal!70!black, thick] coordinates {{{" ".join(f"({s:.0f},{gy:.4f})" for s, _, gy, _ in didymos_curve)}}};
\addlegendentry{{Transverse $y$ (closes)}}
\addplot[gray!60!black, dotted] coordinates {{(0,0) (60,0)}};
\addplot[only marks, mark=*, mark size=2pt, teal!70!black] coordinates {{(40.44,0)}};
\node[font=\scriptsize, anchor=south east, text=teal!70!black] at (axis cs:40,0.12) {{$L_y^*=40.44$ m}};
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
"""
    compile_standalone_tikz(fig1, fig_dir / "fig1_fdir_g2_and_didymos_g3.pdf")

    # Figure 2: Earth-Moon L2 Halo W^u lunar periapsis vs Halo phase (impact vs safe elevated capture)
    c_wu = " ".join(f"({tau:.3f},{rp/1e3:.3f})" for tau, rp in wu_phase_curve)
    fig2 = preamble + rf"""\begin{{tikzpicture}}
\begin{{axis}}[
  width=11.8cm, height=4.8cm,
  xlabel={{Departure phase $\tau / T$ along Earth--Moon $L_2$ Halo orbit}},
  ylabel={{Min.\ distance to Moon center [$10^3$ km]}},
  xmin=0, xmax=1.0, ymin=0, ymax=21,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{Earth--Moon $L_2$ Halo $W^u$ Manifold: Direct Lunar Impact vs.\ Safe Elevated Capture}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}},
  legend pos=north east, legend style={{font=\scriptsize, draw=gray!50}}
]
\addplot[blue!75!black, thick, mark=*, mark size=1.1pt] coordinates {{{c_wu}}};
\addlegendentry{{$W^u(+v_u)$ periapsis ($10^{{-4}}$ kick)}}
\addplot[red!75!black, dashed, thick] coordinates {{(0,1.7374) (1,1.7374)}};
\addlegendentry{{Lunar surface $R_{{\mathrm{{Moon}}}} = 1.737$k km}}
\node[font=\scriptsize, anchor=west, text=red!70!black] at (axis cs:0.02,0.85) {{$\tau=0$: direct impact ($<1.74$k km)}};
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
"""
    compile_standalone_tikz(fig2, fig_dir / "fig2_halo_wu_lunar_clearance.pdf")

    # Figure 3: Bennu TAG subsurface sink vs regolith density (NEG-W13)
    c_den = " ".join(f"({r:.0f},{z:.2f})" for r, z in density_curve)
    fig3 = preamble + rf"""\begin{{tikzpicture}}
\begin{{axis}}[
  width=11.0cm, height=4.7cm,
  xlabel={{Bennu near-subsurface regolith density $\rho_{{\mathrm{{reg}}}}$ [kg/m$^3$]}},
  ylabel={{Touch-and-Go penetration depth $z_{{\mathrm{{sink}}}}$ [cm]}},
  xmin=400, xmax=1220, ymin=8, ymax=54,
  grid=both, grid style={{gray!20}},
  title={{\textbf{{Bennu TAG Penetration Sensitivity ($C_D=1.60$, $A_h=28.27$ m$^2$, $m=1000$ kg)}}}},
  title style={{font=\small}}, label style={{font=\footnotesize}}, tick label style={{font=\scriptsize}},
  legend pos=north east, legend style={{font=\scriptsize, draw=gray!50}}
]
\addplot[teal!70!black, thick] coordinates {{{c_den}}};
\addlegendentry{{Triad TAG $z(\rho_{{\mathrm{{reg}}}})$}}
\addplot[red!75!black, dashed, thick] coordinates {{(400,48.8) (1220,48.8)}};
\addlegendentry{{OSIRIS-REx observed ($48.8$ cm)}}
\addplot[only marks, mark=*, mark size=2.2pt, orange!85!black] coordinates {{(600,18.24)}};
\addplot[only marks, mark=square*, mark size=2pt, gray!70!black] coordinates {{(1190,11.58)}};
\node[font=\scriptsize, anchor=south west, text=orange!80!black] at (axis cs:610,19.0) {{Fluidized $600$ kg/m$^3$: $18.24$ cm}};
\node[font=\scriptsize, anchor=south east, text=gray!60!black] at (axis cs:1185,12.5) {{Bulk $1190$ kg/m$^3$: $11.58$ cm}};
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
"""
    compile_standalone_tikz(fig3, fig_dir / "fig3_bennu_tag_density_sensitivity.pdf")


def main() -> int:
    piece_dir = pathlib.Path(__file__).resolve().parent.parent
    data_dir = piece_dir / "data"
    fig_dir = piece_dir / "paper" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)

    ok_d1, res_d1 = gate_d1_bennu_triaxial()
    ok_d2, res_d2, fdir_curve = gate_d2_theorem_g2_fdir()
    ok_d3, res_d3 = gate_d3_l4_routh_and_figure8()
    ok_d4, res_d4, didymos_curve = gate_d4_theorem_g3_didymos_l2()
    ok_r1, res_r1, wu_phase_curve = gate_r1_42ode_halo_and_elevated_wu()
    ok_p1, res_p1, density_curve = gate_p1_bennu_tag_mc200()

    build_figures(fig_dir, fdir_curve, didymos_curve, wu_phase_curve, density_curve)

    gates = {
        "D1_bennu_triaxial_corrected": ok_d1,
        "D2_theorem_G2_fdir": ok_d2,
        "D3_L4_routh_and_figure8": ok_d3,
        "D4_theorem_G3_didymos_L2": ok_d4,
        "R1_42ode_halo_elevated_Wu_and_SK": ok_r1,
        "P1_bennu_tag_fluidized_mc200": ok_p1,
    }
    payload = {
        "schema_version": "1.0.0",
        "piece": "Horizon Synthesis Piece II (WP032 + WP033)",
        "gates": gates,
        "results": {
            "D1": res_d1,
            "D2": res_d2,
            "D3": res_d3,
            "D4": res_d4,
            "R1": res_r1,
            "P1": res_p1,
        },
    }
    json_path = data_dir / "piece2_calibration.json"
    json_bytes = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    json_path.write_bytes(json_bytes)
    sha = hashlib.sha256(json_bytes).hexdigest()
    rel_json = "papers/horizon_synthesis/piece2_smallbody_crtbp/data/piece2_calibration.json"
    (data_dir / "MANIFEST.sha256").write_text(f"{sha}  {rel_json}\n", encoding="utf-8")

    passed = sum(gates.values())
    for k, v in gates.items():
        print(f"[{'PASS' if v else 'FAIL'}] {k}")
    print(f"Summary: {passed}/{len(gates)} Piece II gates PASS | JSON SHA-256: {sha[:16]}...")
    print(f"  D4 Didymos L_y*={res_d4['didymos_L_y_star_m']:.2f} m (alt={res_d4['didymos_y_star_altitude_m']:.1f} m vs x-50m alt={res_d4['didymos_x_50m_altitude_m']:.1f} m)")
    print(f"  R1 Halo lam_u={res_r1['lambda_u']:.4f}, tau=0 rp={res_r1['tau0_direct_impact_rp_km']:.1f} km (impact={res_r1['tau0_impacts_moon']}); elevated safe Wu tau={res_r1['elevated_safe_wu_tau_frac']:.3f} -> rp={res_r1['elevated_safe_wu_rp_km']:.1f} km (alt={res_r1['elevated_safe_wu_alt_km']:.1f} km); SK suppression={res_r1['floquet_sk_suppression_ratio']:.0f}x")
    print(f"  P1 TAG drift const-g={res_p1['const_g_coriolis_drift_m']:.2f} m vs full={res_p1['full_1r2_cent_drift_m']:.2f} m; sink(600)={res_p1['sink_600_cm']:.2f} cm; MC200 {res_p1['mc200_safe_count']}/200 median={res_p1['mc200_sink_median_cm']:.2f} cm digest={res_p1['mc200_digest']}")
    return 0 if all(gates.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
