#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ergentics, LLC -- [G4N] Round-1 independent [X] re-check of [GB] findings
"""Zero-dependency Python 3.12 verifier for [GB] Round-1 new negatives (NEG-W25..W30)."""

from __future__ import annotations

import cmath
import math
from fractions import Fraction


def check_neg_w25_holonomy_sign() -> bool:
    """Verify Berry/Montgomery physical rotation (+90 deg paper chart vs -90 deg G4N chart)."""
    r_j = math.sqrt(2.0)
    rt2 = math.sqrt(2.0)
    rt6 = math.sqrt(6.0)

    def to_rho(z1: complex, z2: complex) -> tuple[complex, complex, complex]:
        return (z1 / rt2 + z2 / rt6, -z1 / rt2 + z2 / rt6, -2.0 * z2 / rt6)

    def paper_chart(th0: float, theta: float, phi: float) -> tuple[complex, complex, complex]:
        z1 = r_j * math.cos(0.5 * theta) * cmath.exp(1j * (th0 + 0.5 * phi))
        z2 = r_j * math.sin(0.5 * theta) * cmath.exp(1j * (th0 - 0.5 * phi))
        return to_rho(z1, z2)

    def g4n_chart(th0: float, beta: float, chi: float) -> tuple[complex, complex, complex]:
        wp = r_j * math.cos(0.5 * beta) * cmath.exp(1j * (th0 + 0.5 * chi))
        wm = r_j * math.sin(0.5 * beta) * cmath.exp(1j * (th0 - 0.5 * chi))
        return to_rho((wp + wm) / rt2, (wp - wm) / (1j * rt2))

    def max_step_spin(chart_fn, angle: float, sweep: float, steps: int = 20000) -> float:
        worst = 0.0
        for k in range(steps):
            a = sweep * k / steps
            b = sweep * (k + 1) / steps
            ra = chart_fn(-0.5 * math.cos(angle) * a, angle, a)
            rb = chart_fn(-0.5 * math.cos(angle) * b, angle, b)
            lz = sum(((0.5 * (u + v)).conjugate() * (v - u)).imag for u, v in zip(ra, rb))
            worst = max(worst, abs(lz))
        return worst

    th = math.pi / 3.0
    # WP030 chart: d(th0)/dPhi = -cos(Th)/2 -> Delta th0 = -90 deg, plus e^(+-i pi) = -1 (+180 deg) -> +90 deg
    dth0_paper = -0.5 * math.cos(th) * (2.0 * math.pi)
    p0, p1 = paper_chart(0.0, th, 0.0), paper_chart(dth0_paper, th, 2.0 * math.pi)
    rot_paper = [math.degrees(cmath.phase(b / a)) for a, b in zip(p0, p1)]
    lz_paper = max_step_spin(paper_chart, th, 2.0 * math.pi)

    # G4N equilateral-pole chart: beta=pi/3, chi: 0 -> -2pi -> Delta th0 = +90 deg, plus +180 deg -> -90 deg
    dth0_g4n = -0.5 * math.cos(th) * (-2.0 * math.pi)
    g0, g1 = g4n_chart(0.0, th, 0.0), g4n_chart(dth0_g4n, th, -2.0 * math.pi)
    rot_g4n = [math.degrees(cmath.phase(b / a)) for a, b in zip(g0, g1)]
    lz_g4n = max_step_spin(g4n_chart, th, -2.0 * math.pi)

    # Continuity check at Theta -> 0+: physical rotation vanishes while chart angle -> -180 deg
    eps_th = 1.0e-5
    c0 = paper_chart(0.0, eps_th, 0.0)
    c1 = paper_chart(-math.pi * math.cos(eps_th), eps_th, 2.0 * math.pi)
    rot_tiny = math.degrees(cmath.phase(c1[0] / c0[0]))

    ok = (
        abs(math.degrees(dth0_paper) + 90.0) < 1e-12
        and all(abs(r - 90.0) < 1e-12 for r in rot_paper)
        and abs(math.degrees(dth0_g4n) - 90.0) < 1e-12
        and all(abs(r + 90.0) < 1e-12 for r in rot_g4n)
        and lz_paper < 1e-11
        and lz_g4n < 1e-11
        and abs(rot_tiny) < 1e-7
    )
    print(
        f"[{'PASS' if ok else 'FAIL'}] NEG-W25 holonomy sign: "
        f"paper chart dth0={math.degrees(dth0_paper):+.1f} deg, phys={rot_paper[0]:+.4f} deg "
        f"(|Lz|<={lz_paper:.1e}); G4N phys={rot_g4n[0]:+.4f} deg; Th->0+ phys={rot_tiny:+.2e} deg"
    )
    return ok


def check_neg_w26_rounding_order() -> bool:
    """Verify WP030 §1.1 evaluation-order dependence and eps=1e-8 48% cancellation error."""
    mu = 3.986004418e14
    r_orb = 7.0e6
    span = 100.0
    ex = -(mu / 3.0) * 2.0 * span**2 * (3.0 * r_orb**2 - span**2) / (
        r_orb**2 * (r_orb**2 - span**2) ** 2
    )
    v_factored = -(mu / 3.0) * (1.0 / (r_orb + span) ** 2 + 1.0 / (r_orb - span) ** 2 - 2.0 / r_orb**2)
    v_mean_sub = (
        -(mu / (r_orb + span) ** 2) - (mu / r_orb**2) - (mu / (r_orb - span) ** 2)
    ) / 3.0 + mu / r_orb**2
    e_factored = abs(v_factored - ex) / abs(ex)
    e_mean_sub = abs(v_mean_sub - ex) / abs(ex)

    def rel_err_unit(eps: float) -> float:
        ex_u = -(1.0 / 3.0) * 2.0 * eps**2 * (3.0 - eps**2) / ((1.0 - eps**2) ** 2)
        nv_u = -(1.0 / 3.0) * (1.0 / (1.0 + eps) ** 2 + 1.0 / (1.0 - eps) ** 2 - 2.0)
        return abs(nv_u - ex_u) / abs(ex_u)

    r_1e7 = rel_err_unit(1.0e-7)
    r_1e8 = rel_err_unit(1.0e-8)
    r_5e9 = rel_err_unit(5.0e-9)

    ok = (
        abs(e_factored - 5.75e-8) < 1e-9
        and abs(e_mean_sub - 3.46e-7) < 2e-9
        and abs(r_1e7 - 8.20e-3) < 2e-5
        and abs(r_1e8 - 0.4803) < 1e-3
        and abs(r_5e9 - 1.0) < 1e-12
    )
    print(
        f"[{'PASS' if ok else 'FAIL'}] NEG-W26 rounding order: "
        f"factored={e_factored:.2e}, mean-sub={e_mean_sub:.2e}; "
        f"eps=1e-7 -> {r_1e7:.2e}, eps=1e-8 -> {r_1e8:.2%}, eps=5e-9 -> {r_5e9:.0%}"
    )
    return ok


def check_neg_w27_conventions_and_g4_invariance() -> bool:
    """Verify R_E convention, WP031 I0=(2/3)ML^2 vs ML^2, and I0-invariant Theorem G4 heat floor."""
    mu = 3.986004418e14
    r_e_mean = 6_371_000.0
    r_e_eq = 6_378_137.0
    alt_mean_km = (6_800_000.0 - r_e_mean) / 1e3
    alt_eq_km = (6_800_000.0 - r_e_eq) / 1e3

    rp = r_e_eq + 600_000.0
    ecc = 0.25
    p_slr = rp * (1.0 + ecc)
    a_sma = rp / (1.0 - ecc)
    t_orb = 2.0 * math.pi * math.sqrt(a_sma**3 / mu)
    om_max = math.sqrt(mu * p_slr) / (rp**2)
    w_spin = 2.0 * om_max
    mass = 1_000.0
    span = 20_000.0
    loss = 1.0 / 0.88 - 0.80  # 37/110

    # P_orb,full = 3 * mu * I0 * (3e + e^3) / (p^3 * T_orb)
    p_orb_23 = 3.0 * mu * ((2.0 / 3.0) * mass * span**2) * (3.0 * ecc + ecc**3) / (p_slr**3 * t_orb)
    p_orb_ml2 = 3.0 * mu * (mass * span**2) * (3.0 * ecc + ecc**3) / (p_slr**3 * t_orb)

    # Consistent-I0 heat-to-orbital power ratio at q -> 0+ and q = 0.5, 0.8, 0.9
    def p_heat(i0: float, q: float) -> float:
        return loss * (q / (math.pi * (1.0 - q * q) ** 1.5)) * i0 * (w_spin**3)

    r_floor_ml2 = (loss * (mass * span**2) * (w_spin**3) / math.pi) / p_orb_ml2
    r_floor_23 = (loss * ((2.0 / 3.0) * mass * span**2) * (w_spin**3) / math.pi) / p_orb_23
    r_mixed_g4n = (loss * (mass * span**2) * (w_spin**3) / math.pi) / p_orb_23

    ph_q50_ml2 = p_heat(mass * span**2, 0.5)
    ph_q50_23 = p_heat((2.0 / 3.0) * mass * span**2, 0.5)
    ratio_q50_consistent = ph_q50_ml2 / (0.5 * p_orb_ml2)

    ok = (
        abs(alt_mean_km - 429.0) < 1e-9
        and abs(alt_eq_km - 421.863) < 1e-6
        and abs(p_orb_23 - 41.1877) < 1e-3
        and abs(p_orb_ml2 - 61.7815) < 1e-3
        and abs(r_floor_ml2 - r_floor_23) < 1e-12
        and abs(r_floor_ml2 - 9.8468) < 1e-3
        and abs(r_mixed_g4n - 14.7702) < 1e-3
        and abs(ratio_q50_consistent - 15.1601) < 1e-3
        and abs(ph_q50_ml2 - 468.25) < 0.1
        and abs(ph_q50_23 - 312.17) < 0.1
    )
    print(
        f"[{'PASS' if ok else 'FAIL'}] NEG-W27 conventions & G4 ratio: "
        f"rp=6800km alt={alt_mean_km:.1f}/{alt_eq_km:.1f} km; "
        f"P_orb={p_orb_23:.2f} W (2/3 ML^2) vs {p_orb_ml2:.2f} W (ML^2); "
        f"consistent-I0 floor={r_floor_ml2:.2f}x (q=0.5: {ratio_q50_consistent:.2f}x, "
        f"heat={ph_q50_23:.1f}/{ph_q50_ml2:.1f} W; mixed-I0 was {r_mixed_g4n:.2f}x)"
    )
    return ok


def check_neg_w30_sen_exponents() -> bool:
    """Verify exact rational relation between WP034 (106/45) and WP035 (167/90, alpha=257/90)."""
    c_local = Fraction(212, 45)         # Sen (2013) per ln(a), a ~ sqrt(A)
    wp034_mixed = c_local / 2           # 106/45 per ln(A) at fixed s_b
    wp034_singlet = (c_local - 3) / 2   # 77/90 per ln(A)
    measure_shift = Fraction(1, 2)      # (4 pi s_b)^(-1/2) ds_b
    wp035_micro = wp034_mixed - measure_shift
    wp035_alpha = wp035_micro + 1
    sen_alpha_if_direct = wp034_mixed + 1

    ok = (
        wp034_mixed == Fraction(106, 45)
        and wp034_singlet == Fraction(77, 90)
        and wp035_micro == Fraction(167, 90)
        and wp035_alpha == Fraction(257, 90)
        and sen_alpha_if_direct == Fraction(151, 45)
    )
    print(
        f"[{'PASS' if ok else 'FAIL'}] NEG-W30 Sen exponents: "
        f"WP034 fixed-s_b={wp034_mixed}, measure(-1/2) -> WP035 micro={wp035_micro}, "
        f"alpha={wp035_alpha} (direct Sen alpha={sen_alpha_if_direct})"
    )
    return ok


def main() -> int:
    results = [
        check_neg_w25_holonomy_sign(),
        check_neg_w26_rounding_order(),
        check_neg_w27_conventions_and_g4_invariance(),
        check_neg_w30_sen_exponents(),
    ]
    passed = sum(results)
    print(f"Summary: {passed}/{len(results)} [G4N] Round-1 [X] gates PASS")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
