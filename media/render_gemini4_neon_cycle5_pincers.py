#!/usr/bin/env python3
"""
Morpheus — Gemini 4 Neon ADPIE Cycle 5 Creative Featurette Generator (~3:30)
"The Three-Pincer Symphony: Chasing a Musical Universe Through p-adic Trees,
 Modular Forms, and Class Field Towers"

License: MIT (Code Model). Rendered media assets: CC BY 4.0.

First-principles generator (ZERO reads of cached upstream `code/` or `data/` JSONs):
  - Exact 64-pt Gauss-Legendre Poitou-Odlyzko Three-Pincer matrix (Theorem D: n = 6..15)
  - Exact exhaustive genus-13 Shimura curve census (19 pairs incl. NEG-E10 X_0^690(1))
  - Exact Hamilton trace obstruction tau(gamma_0^k) = tr^2/det vs. compact bound [0, 4]
  - Exact F_8 arithmetic & PGL_2(F_8) order-3 free action (3 orbits of 3 on P^1(F_8))
  - Exact Tonnetz spectrum vs. quintic near-miss d_F = 106069 Brandt eigenvalues
  - Three-voice harmonized ensemble (British Lead Educator en-GB, Deep Baritone Formal
    Oracle flite-rms, Harmonic Counterpoint Detective en-US) blended with a live 18-band
    SciPy stereo channel vocoder + procedural neo-Riemannian Rhodes/cello/bell score.
"""

from __future__ import annotations

import argparse
import html
import math
import multiprocessing as mp
import os
import struct
import subprocess
import tempfile
import wave
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import cairo
import gi
import numpy as np
from scipy import signal

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo  # noqa: E402

# ---------------------------------------------------------------------------
# Master Video/Audio Constants & Observatory Neon Palette
# ---------------------------------------------------------------------------

WIDTH = 1920
HEIGHT = 1080
FPS = 24
SAMPLE_RATE = 48000

# Astral Observatory dark palette (distinct from Cycle 4's electric navy)
C_BG_DEEP = (0.018, 0.022, 0.048, 1.0)
C_BG_MID = (0.045, 0.058, 0.118, 1.0)
C_GRID = (0.125, 0.165, 0.285, 0.22)
C_PANEL = (0.042, 0.056, 0.112, 0.90)
C_PANEL_BORDER = (0.210, 0.285, 0.460, 0.52)

C_CYAN = (0.050, 0.920, 1.000, 1.0)      # Pincer 1 (Base field F) & Lean 4
C_MAGENTA = (0.980, 0.220, 0.620, 1.0)   # Pincer 2 (Wide Hilbert class field H_F)
C_GOLD = (1.000, 0.760, 0.140, 1.0)      # Pincer 3 (Decomposition field L_v) & Tonnetz
C_EMERALD = (0.160, 0.940, 0.580, 1.0)   # Verified PASS / Survivors / Resolution
C_CRIMSON = (1.000, 0.300, 0.340, 1.0)   # NEG-E10 / Cutoff wall / Obstruction
C_VIOLET = (0.680, 0.480, 1.000, 1.0)    # Pure Rust Manin T_2 & 2-adic tree
C_WHITE = (0.955, 0.968, 1.000, 1.0)
C_SLATE = (0.650, 0.715, 0.840, 1.0)
C_DIM = (0.390, 0.455, 0.585, 1.0)

PI = math.pi
GAMMA_EULER = 0.577215664901532860606512090082402431


# ---------------------------------------------------------------------------
# Easing & Geometry Utilities
# ---------------------------------------------------------------------------

def clamp01(x: float) -> float:
    return 0.0 if x <= 0.0 else (1.0 if x >= 1.0 else x)


def smoothstep(t: float) -> float:
    u = clamp01(t)
    return u * u * (3.0 - 2.0 * u)


def ease_out_cubic(t: float) -> float:
    u = 1.0 - clamp01(t)
    return 1.0 - u * u * u


def ease_in_out_cubic(t: float) -> float:
    u = clamp01(t)
    return 4.0 * u * u * u if u < 0.5 else 1.0 - ((-2.0 * u + 2.0) ** 3) / 2.0


def seg_prog(t: float, t0: float, t1: float) -> float:
    if t1 <= t0:
        return 1.0 if t >= t0 else 0.0
    return clamp01((t - t0) / (t1 - t0))


def scene_alpha(t: float, t0: float, t1: float, fade_in: float = 0.60, fade_out: float = 0.60) -> float:
    if t < t0 or t > t1:
        return 0.0
    a_in = smoothstep((t - t0) / fade_in) if fade_in > 0 else 1.0
    a_out = smoothstep((t1 - t) / fade_out) if fade_out > 0 else 1.0
    return min(a_in, a_out)


# ---------------------------------------------------------------------------
# First-Principles Mathematics Core (Zero Cached Data Reads)
# ---------------------------------------------------------------------------

def compute_cycle5_math() -> Dict[str, object]:
    """Compute every single Cycle 5 mathematical object live from first principles."""
    # 1. Exact 64-pt Gauss-Legendre Poitou-Odlyzko engine (Theorem D)
    t64, w64 = np.polynomial.legendre.leggauss(64)

    def h1(u):
        return ((2.0 - u) * (1.0 + 0.5 * np.cos(PI * u)) / 3.0) + np.sin(PI * u) / (2.0 * PI)

    def poitou(b: float):
        u = 1.0 + t64
        x = b * u
        g = h1(u)
        i_sinh = float(np.sum(w64 * b * (1.0 - g) / np.sinh(x)))
        i_tail = math.log((math.exp(2.0 * b) + 1.0) / (math.exp(2.0 * b) - 1.0)) if b < 18.0 else 2.0 * math.exp(-2.0 * b)
        log_b = GAMMA_EULER + math.log(4.0 * PI) - i_sinh - i_tail
        log_a = log_b + float(np.sum(w64 * b * g / (2.0 * np.cosh(0.5 * x) ** 2)))
        e_val = 8.0 * b / 3.0
        def fq(q):
            lq = math.log(q)
            s, m = 0.0, 1
            while m * lq < 2.0 * b:
                s += (4.0 * lq / (1.0 + q**m)) * float(h1(m * lq / b))
                m += 1
            return s
        return (b, log_a, log_b, e_val, fq(2), fq(4))

    grid = [poitou(0.5 + 0.05 * i) for i in range(231)]

    def best_lb(deg: float, rho1: float, cf2: float, cf4: float) -> float:
        return max(rho1 * lA + (1.0 - rho1) * lB - E / deg + cf2 * f2 + cf4 * f4 for _, lA, lB, E, f2, f4 in grid)

    def ub_log(n: int, u: int, mode: str) -> float:
        c = 4.5 * u if mode == "even" else ((27.0 / 8.0) * u if mode == "odd_A" else 2.0 * u)
        return (2.0 / 3.0) * math.log(4.0 * PI * PI) + (2.0 / (3.0 * n)) * math.log(c)

    # Build full (n, k) cell table for n = 6..14:
    # Classify each (n, k) by which pincer finishes it off:
    #   "P1": killed by Pincer 1 (F itself, even for h_F=1)
    #   "P3": killed by Pincer 2 (h_F>=2) AND Pincer 3 (L_v / codim-j subfield for h_F=1)
    #   "ALIVE_H1": survives ONLY with h_F = 1 (Pincer 2 killed h_F >= 2!)
    #   "ALIVE_ANY": survives for h_F = 1 and h_F >= 2
    pincer_grid: Dict[Tuple[int, int], Dict[str, object]] = {}
    for n in range(6, 15):
        modes = ["even"] if n % 2 == 0 else ["odd_A", "odd_B"]
        for k in range(n):
            u = 1 << k
            worst_h1_margin = 1e9
            worst_h2_margin = 1e9
            worst_f_margin = 1e9
            ub_max = 0.0
            for mode in modes:
                ub = ub_log(n, u, mode)
                ub_max = max(ub_max, math.exp(ub))
                cf2_f = (2.0 if mode == "odd_A" else 1.0) / n
                lb_f = best_lb(float(n), 1.0, cf2_f, 0.0)
                sub_h1 = -1e9
                for j in range(1, k + 1):
                    r1_min = math.ceil(n * ((1 << (k - j)) - 1) / ((1 << k) - 1)) if j < k else 0
                    rho1 = r1_min / n
                    cf4 = (2.0 if mode == "odd_A" else 1.0) / (2.0 * n)
                    sub_h1 = max(sub_h1, best_lb(float(n * (1 << j)), rho1, 0.0, cf4))
                if k == 0:
                    lb_h1 = lb_f
                else:
                    cf4_ex = (1.0 / (2.0 * n)) if mode == "odd_A" else 0.0
                    b1 = best_lb(float(n * u), 0.0, 1.0 / n, cf4_ex)
                    lb_fv1 = max(lb_f, b1, sub_h1)
                    b2_lv = best_lb(float(n * (u // 2)), 0.0, 1.0 / n, cf4_ex)
                    b2_h = best_lb(float(n * u), 0.0, 0.0, (2.0 if mode == "odd_A" else 1.0) / (2.0 * n))
                    lb_fv2 = max(lb_f, b2_lv, b2_h, sub_h1)
                    lb_h1 = min(lb_fv1, lb_fv2)
                lb_h2 = lb_f
                for j in range(0, k + 1):
                    rho1 = 1.0 if j == 0 else (0.0 if j == k else math.ceil(n * ((1 << (k - j)) - 1) / ((1 << k) - 1)) / n)
                    lb_h2 = max(lb_h2, best_lb(float(2 * n * (1 << j)), rho1, 0.0, 0.0))
                worst_f_margin = min(worst_f_margin, math.exp(lb_f) - math.exp(ub))
                worst_h1_margin = min(worst_h1_margin, math.exp(lb_h1) - math.exp(ub))
                worst_h2_margin = min(worst_h2_margin, math.exp(lb_h2) - math.exp(ub))
            if worst_f_margin > 0:
                status = "P1"
            elif worst_h1_margin > 0 and worst_h2_margin > 0:
                status = "P3"
            elif worst_h2_margin > 0:
                status = "ALIVE_H1"
            else:
                status = "ALIVE_ANY"
            pincer_grid[(n, k)] = {
                "u": u,
                "status": status,
                "ub": ub_max,
                "m_f": worst_f_margin,
                "m_h1": worst_h1_margin,
                "m_h2": worst_h2_margin,
            }

    # Exact n=6, u=16, h_F=1 L_v curve vs b in [4.2, 7.5] + exact peak at b = 6.00
    ub_6_16 = math.exp(ub_log(6, 16, "even"))
    lv_curve = []
    for i in range(67):
        b = 4.2 + 0.05 * i
        _, _, lB, E, f2, _ = poitou(b)
        lv_curve.append((b, math.exp(lB - E / 48.0 + f2 / 6.0)))
    _, _, lB6, E6, f2_6, _ = poitou(6.0)
    lv_peak_6 = math.exp(lB6 - E6 / 48.0 + f2_6 / 6.0)

    # 2. Exact exhaustive genus-13 Shimura curve census (19 pairs incl. NEG-E10 D=690, N=1)
    def is_prime(num: int) -> bool:
        return num >= 2 and all(num % d != 0 for d in range(2, int(num**0.5) + 1))

    def k4(p: int) -> int:
        return 0 if p == 2 else (1 if p % 4 == 1 else -1)

    def k3(p: int) -> int:
        return 0 if p == 3 else (1 if p % 3 == 1 else -1)

    odd_p = [p for p in range(3, 1002, 2) if is_prime(p)]
    d_cands = []

    def gen_d(idx: int, cnt: int, D: int, phi: int, e2: int, e3: int):
        if cnt >= 2 and cnt % 2 == 0:
            d_cands.append((D, phi, e2, e3))
        for i in range(idx, len(odd_p)):
            p = odd_p[i]
            if phi * (p - 1) > 1000:
                break
            gen_d(i + 1, cnt + 1, D * p, phi * (p - 1), e2 * (1 - k4(p)), e3 * (1 - k3(p)))

    gen_d(0, 1, 2, 1, 1, 2)
    shimura_19 = []
    for D, phiD, e2D, e3D in d_cands:
        for N in range(1, 1000 // phiD + 1, 2):
            if math.gcd(D, N) != 1:
                continue
            tmp, psiN, e2N, e3N = N, 1, 1, 1
            d = 3
            while d * d <= tmp:
                if tmp % d == 0:
                    k, pk = 0, 1
                    while tmp % d == 0:
                        if k >= 1:
                            pk *= d
                        tmp //= d
                        k += 1
                    psiN *= pk * (d + 1)
                    e2N *= 1 + k4(d)
                    e3N *= (1 if k == 1 else 0) if d == 3 else (1 + k3(d))
                d += 2
            if tmp > 1:
                psiN *= tmp + 1
                e2N *= 1 + k4(tmp)
                e3N *= 1 if tmp == 3 else (1 + k3(tmp))
            if phiD * psiN <= 1000:
                e2, e3 = e2D * e2N, e3D * e3N
                if 12 + phiD * psiN - 3 * e2 - 4 * e3 == 12 * 13:
                    shimura_19.append((D, N, phiD, psiN, e2, e3))
    shimura_19.sort(key=lambda r: (r[2], r[0], r[1]))

    # 3. Exact P^1(F_8) 3 orbits of size 3 under M = [[0, 1], [1, 1]]
    def f8_mul(a: int, b: int) -> int:
        p = 0
        for i in range(3):
            if b & (1 << i):
                p ^= a << i
        if p & 16:
            p ^= 0b1011 << 1
        if p & 8:
            p ^= 0b1011
        return p & 7

    def f8_inv(a: int) -> int:
        a2 = f8_mul(a, a)
        a4 = f8_mul(a2, a2)
        return f8_mul(a2, a4)

    def p1_act(pt: int) -> int:
        if pt == 8:
            return 0
        den = pt ^ 1
        return 8 if den == 0 else f8_inv(den)

    visited = set()
    f8_orbits = []
    for pt in [8, 0, 1, 2, 3, 4, 5, 6, 7]:
        if pt in visited:
            continue
        orb = [pt, p1_act(pt), p1_act(p1_act(pt))]
        for x in orb:
            visited.add(x)
        f8_orbits.append(orb)

    # 4. Exact 24-vertex Tonnetz PLR adjacency graph & eigenvalues vs. quintic near-miss d_F = 106069
    # Vertices 0..23 interleaved around circle: 2*k = Major(k), 2*k+1 = Minor(k)
    A_X = np.zeros((24, 24), dtype=np.float64)
    tonnetz_edges: List[Tuple[int, int]] = []
    for r in range(12):
        u_maj = 2 * r
        for shift in (0, 4, 9):  # P: +0, L: +4, R: +9 (mod 12)
            v_min = 2 * ((r + shift) % 12) + 1
            A_X[u_maj, v_min] = 1.0
            A_X[v_min, u_maj] = 1.0
            tonnetz_edges.append((u_maj, v_min))
    eigs_X_all = np.linalg.eigvalsh(A_X)
    eigs_X_pos = sorted([float(v) for v in eigs_X_all if v > 1e-6], reverse=True)
    # Exact Brandt polynomial of d_F = 106069: t(t-3)(t+1)(t^4+3t^3-4t-1)(t^5-t^4-8t^3+8t^2+15t-16)
    r4 = np.roots([1, 3, 0, -4, -1]).real
    r5 = np.roots([1, -1, -8, 8, 15, -16]).real
    eigs_106069 = sorted([3.0, 0.0, -1.0] + list(r4) + list(r5), reverse=True)
    eigs_106069_abs = sorted([abs(v) for v in eigs_106069], reverse=True)

    return {
        "pincer_grid": pincer_grid,
        "ub_6_16": ub_6_16,
        "lv_curve": lv_curve,
        "lv_peak_6": lv_peak_6,
        "shimura_19": shimura_19,
        "f8_orbits": f8_orbits,
        "tonnetz_edges": tonnetz_edges,
        "eigs_X_pos": eigs_X_pos,
        "eigs_106069": eigs_106069,
        "eigs_106069_abs": eigs_106069_abs,
    }


# ---------------------------------------------------------------------------
# Multi-Voice Harmonized Speech + Procedural Neo-Riemannian Audio Engine
# ---------------------------------------------------------------------------

@dataclass
class VoiceCue:
    chapter: int
    speaker: str  # "gb" (British Educator), "rms" (Baritone Oracle), "us" (Counterpoint Detective)
    text: str
    chord_midi: Tuple[int, ...]
    vocoder_wet: float
    pan: float
    gap_after: float = 0.70


SCRIPT_CUES: List[VoiceCue] = [
    # Chapter 0: Overture — The Musical Universe & The Shimura Question
    VoiceCue(0, "gb", "Welcome back to Morpheus. Twenty-four musical triads form a Ramanujan honeycomb that sings forever without repeating.", (60, 64, 67, 71), 0.16, 0.0, 0.75),
    VoiceCue(0, "gb", "In Prime Cadences, a deeper question remained: could this musical universe actually be a Shimura curve from number theory?", (57, 60, 64, 69), 0.16, 0.0, 0.85),
    VoiceCue(0, "rms", "Seven arithmetic obstructions stood unverified. Cycle Five resolves all seven, uncovers a hidden curve, and proves Theorem D.", (53, 57, 60, 65), 0.22, -0.05, 1.05),

    # Chapter 1: Prop 7.3, Lem 7.14 & Prop 7.17 — Trace Shockwave, 2-Adic Doubling & F_8 Orbits
    VoiceCue(1, "gb", "First, test the closed musical loop P L R L P R P L inside the two-adic Bruhat-Tits tree.", (62, 65, 69, 72), 0.16, 0.0, 0.60),
    VoiceCue(1, "rms", "Its trace invariant is seven thousand two hundred twenty-five over two hundred fifty-six: twenty-eight point two two, shattering the compact quaternion ceiling of four.", (53, 56, 60, 65), 0.24, -0.06, 0.75),
    VoiceCue(1, "gb", "What if the group has torsion? Lemma seven-point-fourteen proves every fixed two-adic disc doubles in slope, forcing free action over Q two.", (56, 60, 63, 68), 0.18, 0.0, 0.65),
    VoiceCue(1, "us", "Only over larger residue fields like F eight can torsion slip past: fifty-six elements of order three spin all nine projective points in three synchronized free orbits.", (63, 67, 70, 74), 0.22, 0.12, 0.95),

    # Chapter 2: NEG-E10 Detective Story — The Missing Curve X_0^690(1) & Zero-PARI Pure-Rust Manin T_2
    VoiceCue(2, "us", "Next, we audited every genus-thirteen Shimura curve over the rationals — and our exhaustive sweep tripped a silent alarm.", (52, 55, 59, 66), 0.18, 0.10, 0.65),
    VoiceCue(2, "gb", "The baseline script stopped at Euler phi equal to one hundred sixty-eight. Just eight steps past that wall sits a ghost curve: D equals six hundred ninety, with phi one hundred seventy-six and exact genus thirteen.", (52, 55, 59, 64), 0.18, 0.0, 0.75),
    VoiceCue(2, "rms", "Erratum NEG-E10 logged: nineteen curves, not eighteen. Does the missing curve match our musical Tonnetz?", (48, 52, 55, 62), 0.24, -0.06, 0.65),
    VoiceCue(2, "us", "Without calling PARI, our pure Rust engine built Manin modular symbols at level three hundred forty-five. Dimension forty-five. Rank of T two to the fourth minus four T two squared plus I: forty-five out of forty-five.", (55, 59, 62, 66), 0.20, 0.10, 0.70),
    VoiceCue(2, "gb", "Full rank! Theorem seven-point-eleven still stands — now verified across all nineteen curves.", (55, 59, 62, 67), 0.20, 0.0, 0.95),

    # Chapter 3: Prop 7.18 & Quintic Near-Miss d_F = 106069 — The Brandt Orchestra
    VoiceCue(3, "gb", "Moving to higher number fields, we rebuilt every Brandt matrix from scratch across quadratics, cubics, quartics, and the eerie degree-five near-miss of discriminant one hundred six thousand and sixty-nine.", (57, 60, 64, 67), 0.16, 0.0, 0.70),
    VoiceCue(3, "us", "It has the exact same twenty-four vertices, the exact same three-regularity, and genus thirteen. Listen closely: its eigenvalues miss the Tonnetz golden chord of two cosine pi over twelve.", (57, 61, 64, 68), 0.22, 0.10, 1.00),

    # Chapter 4: CLIMAX — Novelty 3: Theorem D (The Three-Pincer Hilbert Class Field Obstruction)
    VoiceCue(4, "gb", "Now comes Cycle Five's centerpiece: Theorem D. Prior Odlyzko bounds stopped at degree fourteen because the narrow-class ratio u could grow up to two to the n minus one.", (50, 53, 57, 64), 0.16, 0.0, 0.70),
    VoiceCue(4, "gb", "Our breakthrough: large u is never free. Class field theory builds an unramified Hilbert tower with the exact same root discriminant, unlocking three simultaneous pincers.", (58, 62, 65, 69), 0.18, 0.0, 0.75),
    VoiceCue(4, "rms", "Pincer One: base field and odd-degree Hilbert reciprocity crush small u, plus a single witness at b equals four-point-two seals all degrees fifteen and above.", (50, 53, 57, 62), 0.25, -0.06, 0.65),
    VoiceCue(4, "rms", "Pincer Two: the wide Hilbert class field and F two subspace averaging annihilate every wide class number two or higher from degree seven upward.", (54, 57, 61, 66), 0.25, -0.06, 0.65),
    VoiceCue(4, "rms", "Pincer Three: for class number one, the decomposition field L v of degree n u over two slams the final gate shut. Degrees nine through fourteen: zero survivors!", (57, 61, 64, 69), 0.26, -0.06, 0.80),
    VoiceCue(4, "us", "Even in degree six, L v of degree forty-eight kills u equals sixteen by zero-point-zero-one-three-six — thirteen orders of magnitude above quadrature error — collapsing the sextic search space by two-point-five times.", (62, 66, 69, 73), 0.20, 0.10, 0.95),

    # Chapter 5: Four-Plane Verification Finale
    VoiceCue(5, "gb", "Every bound, every curve, and every proof stands independently verified across four code planes with zero cached data reads: thirty-three Lean four kernel theorems, Swift-plus-plus at zero-point-zero delta, pure Rust Manin symbols, and from-scratch PARI Brandt graphs.", (60, 64, 67, 74), 0.18, 0.0, 0.80),
    VoiceCue(5, "rms", "Morpheus Cycle Five: from music to modular forms to class field towers — open source, audit forward, and ready to reconcile.", (60, 64, 67, 71), 0.24, 0.0, 1.80),
]


def midi_to_hz(m: float) -> float:
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))


def synthesize_tts_raw(speaker: str, text: str) -> np.ndarray:
    """Synthesize clean mono float32 audio at SAMPLE_RATE (48 kHz) via pico2wave or flite."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        wav_path = tf.name
    try:
        if speaker == "gb":
            subprocess.run(["pico2wave", "-l", "en-GB", "-w", wav_path, text], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif speaker == "us":
            subprocess.run(["pico2wave", "-l", "en-US", "-w", wav_path, text], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif speaker == "rms":
            subprocess.run(["flite", "-voice", "rms", "-t", text, "-o", wav_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            raise ValueError(f"Unknown speaker {speaker}")

        with wave.open(wav_path, "rb") as wf:
            sr = wf.getframerate()
            n_frames = wf.getnframes()
            raw = wf.readframes(n_frames)
            audio = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

    # Trim leading/trailing silence tightly
    abs_a = np.abs(audio)
    nz = np.where(abs_a > 0.012)[0]
    if len(nz) > 0:
        pad = int(0.04 * sr)
        audio = audio[max(0, nz[0] - pad) : min(len(audio), nz[-1] + pad)]

    # Resample cleanly to 48 kHz
    if sr != SAMPLE_RATE:
        g = math.gcd(sr, SAMPLE_RATE)
        audio = signal.resample_poly(audio, SAMPLE_RATE // g, sr // g)

    # Gentle speaker-tailored polish EQ
    if speaker == "rms":
        # Warm baritone presence, tame harsh flite high-end fizz
        b_lp, a_lp = signal.butter(2, 5200.0 / (SAMPLE_RATE / 2.0), btype="low")
        audio = signal.lfilter(b_lp, a_lp, audio)
        b_hp, a_hp = signal.butter(2, 85.0 / (SAMPLE_RATE / 2.0), btype="high")
        audio = signal.lfilter(b_hp, a_hp, audio)
    else:
        b_hp, a_hp = signal.butter(2, 110.0 / (SAMPLE_RATE / 2.0), btype="high")
        audio = signal.lfilter(b_hp, a_hp, audio)

    # RMS normalize to consistent broadcast speech loudness
    rms = math.sqrt(float(np.mean(audio * audio)) + 1e-12)
    audio = audio * (0.19 / rms)
    return np.clip(audio, -0.92, 0.92)


def harmonize_voice_vocoder(dry: np.ndarray, chord_midi: Tuple[int, ...], wet: float, pan: float, is_baritone: bool) -> np.ndarray:
    """Blend intelligible dry voice with an 18-band stereo harmonic vocoder tuned to the active Tonnetz chord."""
    n = len(dry)
    t = np.arange(n, dtype=np.float64) / SAMPLE_RATE

    # Rich harmonic carrier (saw/sine hybrid voices spread across stereo field)
    carrier_l = np.zeros(n, dtype=np.float64)
    carrier_r = np.zeros(n, dtype=np.float64)
    oct_shift = -12 if is_baritone else 0
    for idx, m in enumerate(chord_midi):
        f0 = midi_to_hz(m + oct_shift)
        # Subtle detuned chorus + 4 partials
        sig_v = np.zeros(n, dtype=np.float64)
        for h in range(1, 6):
            fh = f0 * h
            if fh < 7500.0:
                sig_v += (0.55 ** (h - 1)) * np.sin(2.0 * PI * fh * t + 0.7 * idx)
        # Pan each chord tone across stereo width
        p_tone = -0.65 + 1.30 * (idx / max(1, len(chord_midi) - 1))
        gl = math.cos((p_tone + 1.0) * PI * 0.25)
        gr = math.sin((p_tone + 1.0) * PI * 0.25)
        carrier_l += sig_v * gl
        carrier_r += sig_v * gr

    # Normalize carriers
    for arr in (carrier_l, carrier_r):
        mx = float(np.max(np.abs(arr)) + 1e-12)
        arr /= mx

    # 18-band logarithmic channel vocoder (180 Hz -> 4600 Hz)
    edges = np.geomspace(180.0, 4600.0, 19)
    voc_l = np.zeros(n, dtype=np.float64)
    voc_r = np.zeros(n, dtype=np.float64)
    b_env, a_env = signal.butter(2, 32.0 / (SAMPLE_RATE / 2.0), btype="low")
    for i in range(18):
        lo = edges[i] / (SAMPLE_RATE / 2.0)
        hi = edges[i + 1] / (SAMPLE_RATE / 2.0)
        sos = signal.butter(2, [lo, hi], btype="band", output="sos")
        m_band = signal.sosfilt(sos, dry)
        env = np.maximum(0.0, signal.lfilter(b_env, a_env, np.abs(m_band)))
        voc_l += signal.sosfilt(sos, carrier_l) * env
        voc_r += signal.sosfilt(sos, carrier_r) * env

    # Match vocoder RMS to dry RMS before wet/dry blend
    v_rms = math.sqrt(float(np.mean(0.5 * (voc_l**2 + voc_r**2))) + 1e-12)
    d_rms = math.sqrt(float(np.mean(dry**2)) + 1e-12)
    if v_rms > 1e-8:
        scale = d_rms / v_rms
        voc_l *= scale
        voc_r *= scale

    # Pan dry signal gently, keep vocoder wide stereo
    dl = math.cos((pan + 1.0) * PI * 0.25) * 1.12
    dr = math.sin((pan + 1.0) * PI * 0.25) * 1.12
    out = np.zeros((n, 2), dtype=np.float64)
    out[:, 0] = (1.0 - wet) * dry * dl + wet * 1.25 * voc_l
    out[:, 1] = (1.0 - wet) * dry * dr + wet * 1.25 * voc_r
    return out


def add_rhodes_chord(buf: np.ndarray, t0: float, dur: float, notes_midi: Sequence[float], amp: float = 0.085, detune_hz: float = 0.0):
    """Synthesize warm Rhodes electric-piano chord + deep bowed cello sub-root."""
    s0 = int(t0 * SAMPLE_RATE)
    n = int(dur * SAMPLE_RATE)
    if s0 >= len(buf) or n <= 0:
        return
    n = min(n, len(buf) - s0)
    t = np.arange(n, dtype=np.float64) / SAMPLE_RATE
    atk = np.minimum(1.0, t / 0.08)
    rel = np.minimum(1.0, (dur - t) / 0.55)
    decay = np.exp(-0.42 * t)
    env = atk * np.clip(rel, 0.0, 1.0) * (0.35 + 0.65 * decay)

    left = np.zeros(n, dtype=np.float64)
    right = np.zeros(n, dtype=np.float64)
    for idx, m in enumerate(notes_midi):
        f = midi_to_hz(m) + (detune_hz * (1 if idx % 2 == 0 else -1))
        # Warm electric piano tine + fundamental
        tone = (
            1.00 * np.sin(2.0 * PI * f * t)
            + 0.28 * np.exp(-2.2 * t) * np.sin(2.0 * PI * 2.0 * f * t)
            + 0.11 * np.exp(-4.5 * t) * np.sin(2.0 * PI * 3.0 * f * t)
            + 0.04 * np.exp(-7.0 * t) * np.sin(2.0 * PI * 5.0 * f * t)
        )
        pan = -0.55 + 1.10 * (idx / max(1, len(notes_midi) - 1))
        left += tone * math.cos((pan + 1.0) * PI * 0.25)
        right += tone * math.sin((pan + 1.0) * PI * 0.25)

    # Warm bowed cello root an octave below
    f_bass = midi_to_hz(notes_midi[0] - 12.0)
    vib = 1.0 + 0.0025 * np.sin(2.0 * PI * 4.8 * t)
    bass_phase = 2.0 * PI * np.cumsum(f_bass * vib) / SAMPLE_RATE
    bass = 0.52 * (np.sin(bass_phase) + 0.24 * np.sin(2.0 * bass_phase) + 0.08 * np.sin(3.0 * bass_phase))
    bass_env = np.minimum(1.0, t / 0.35) * np.clip((dur - t) / 0.55, 0.0, 1.0)

    scale = amp / max(1.0, math.sqrt(len(notes_midi)))
    buf[s0 : s0 + n, 0] += env * left * scale + bass_env * bass * amp * 0.60
    buf[s0 : s0 + n, 1] += env * right * scale + bass_env * bass * amp * 0.60


def add_bell_ping(buf: np.ndarray, t0: float, midi_note: float, amp: float = 0.065, pan: float = 0.0, decay_rate: float = 2.6, freq_hz: float | None = None):
    """Synthesize crystalline harmonic chime for geometric events (tree branches, orbits, pincer locks)."""
    s0 = int(t0 * SAMPLE_RATE)
    dur = min(2.4, 6.0 / decay_rate)
    n = int(dur * SAMPLE_RATE)
    if s0 < 0 or s0 >= len(buf) or n <= 0:
        return
    n = min(n, len(buf) - s0)
    t = np.arange(n, dtype=np.float64) / SAMPLE_RATE
    f = freq_hz if freq_hz is not None else midi_to_hz(midi_note)
    env = np.minimum(1.0, t / 0.008) * np.exp(-decay_rate * t)
    sig = (
        1.00 * np.sin(2.0 * PI * f * t)
        + 0.32 * np.exp(-1.5 * t) * np.sin(2.0 * PI * 2.0 * f * t)
        + 0.14 * np.exp(-3.5 * t) * np.sin(2.0 * PI * 3.0 * f * t)
    ) * env * amp
    buf[s0 : s0 + n, 0] += sig * math.cos((pan + 1.0) * PI * 0.25)
    buf[s0 : s0 + n, 1] += sig * math.sin((pan + 1.0) * PI * 0.25)


def add_pincer_impact(buf: np.ndarray, t0: float, root_midi: float, amp: float = 0.16):
    """Deep cinematic harmonic lock swell + bell resonance when a Theorem D pincer snaps shut."""
    s0 = int(t0 * SAMPLE_RATE)
    dur = 1.8
    n = int(dur * SAMPLE_RATE)
    if s0 < 0 or s0 >= len(buf) or n <= 0:
        return
    n = min(n, len(buf) - s0)
    t = np.arange(n, dtype=np.float64) / SAMPLE_RATE
    f_sub = midi_to_hz(root_midi - 24.0)
    # Pitch drop sub-boom + resonant fifth chime
    sub = np.sin(2.0 * PI * f_sub * t * (1.0 + 0.18 * np.exp(-12.0 * t))) * np.exp(-2.8 * t) * np.minimum(1.0, t / 0.012)
    buf[s0 : s0 + n, 0] += sub * amp
    buf[s0 : s0 + n, 1] += sub * amp
    add_bell_ping(buf, t0, root_midi + 12.0, amp=amp * 0.55, pan=-0.35, decay_rate=1.8)
    add_bell_ping(buf, t0 + 0.03, root_midi + 19.0, amp=amp * 0.45, pan=0.35, decay_rate=1.8)


def apply_stereo_reverb(audio: np.ndarray, mix: float = 0.16) -> np.ndarray:
    """Lightweight multi-tap Schroeder stereo comb reverb for spacious observatory ambience."""
    n = len(audio)
    wet = np.zeros_like(audio)
    taps_l = [(int(0.031 * SAMPLE_RATE), 0.44), (int(0.053 * SAMPLE_RATE), 0.34), (int(0.089 * SAMPLE_RATE), 0.24), (int(0.141 * SAMPLE_RATE), 0.16)]
    taps_r = [(int(0.037 * SAMPLE_RATE), 0.44), (int(0.061 * SAMPLE_RATE), 0.34), (int(0.097 * SAMPLE_RATE), 0.24), (int(0.157 * SAMPLE_RATE), 0.16)]
    for d, g in taps_l:
        if d < n:
            wet[d:, 0] += g * audio[:-d, 0]
    for d, g in taps_r:
        if d < n:
            wet[d:, 1] += g * audio[:-d, 1]
    b, a = signal.butter(1, 3200.0 / (SAMPLE_RATE / 2.0), btype="low")
    wet[:, 0] = signal.lfilter(b, a, wet[:, 0])
    wet[:, 1] = signal.lfilter(b, a, wet[:, 1])
    return (1.0 - mix) * audio + mix * wet


def build_audio_and_timeline(math_data: Dict[str, object]) -> Tuple[np.ndarray, List[Tuple[int, float, float]], List[Tuple[float, float, VoiceCue]]]:
    """Synthesize all voice cues, auto-compute chapter boundaries, and mix procedural musical score."""
    print("  Synthesizing 3-voice harmonized ensemble (en-GB, flite-rms, en-US)...")
    raw_cues = []
    for cue in SCRIPT_CUES:
        dry = synthesize_tts_raw(cue.speaker, cue.text)
        harm = harmonize_voice_vocoder(dry, cue.chord_midi, cue.vocoder_wet, cue.pan, is_baritone=(cue.speaker == "rms"))
        raw_cues.append((cue, harm, len(dry) / SAMPLE_RATE))

    # Build auto-timed timeline starting at t = 1.6s (brief musical curtain rise)
    t_cur = 1.60
    placed: List[Tuple[float, float, VoiceCue, np.ndarray]] = []
    chap_starts: Dict[int, float] = {}
    chap_ends: Dict[int, float] = {}

    for idx, (cue, harm, dur) in enumerate(raw_cues):
        if cue.chapter not in chap_starts:
            chap_starts[cue.chapter] = 0.0 if cue.chapter == 0 else (t_cur - 0.55)
        t0 = t_cur
        t1 = t0 + dur
        placed.append((t0, t1, cue, harm))
        chap_ends[cue.chapter] = t1 + cue.gap_after
        t_cur = t1 + cue.gap_after

    total_dur = t_cur + 1.80
    chapters: List[Tuple[int, float, float]] = []
    for ch in range(6):
        c0 = chap_starts[ch]
        c1 = chap_starts[ch + 1] if (ch + 1) in chap_starts else total_dur
        chapters.append((ch, c0, c1))

    n_samples = int(math.ceil(total_dur * SAMPLE_RATE))
    music = np.zeros((n_samples, 2), dtype=np.float64)
    voices = np.zeros((n_samples, 2), dtype=np.float64)
    speech_mask = np.zeros(n_samples, dtype=np.float64)

    # Lay down harmonized voice tracks + speech envelope for smooth sidechain ducking
    for t0, t1, cue, harm in placed:
        s0 = int(t0 * SAMPLE_RATE)
        ln = min(len(harm), n_samples - s0)
        voices[s0 : s0 + ln] += harm[:ln]
        speech_mask[s0 : s0 + ln] = 1.0

    # Smooth speech ducking envelope (duck music bed -5.5 dB during narration)
    b_d, a_d = signal.butter(2, 4.5 / (SAMPLE_RATE / 2.0), btype="low")
    duck_env = np.clip(signal.filtfilt(b_d, a_d, speech_mask), 0.0, 1.0)

    # Lay down harmonic chord bed synchronized to EVERY cue's exact Tonnetz chord!
    add_rhodes_chord(music, 0.0, 2.2, (60, 64, 67, 71), amp=0.115)
    add_bell_ping(music, 0.35, 72, amp=0.06, pan=-0.3)
    add_bell_ping(music, 0.75, 76, amp=0.06, pan=0.0)
    add_bell_ping(music, 1.15, 79, amp=0.07, pan=0.3)

    for idx, (t0, t1, cue, _) in enumerate(placed):
        next_t = placed[idx + 1][0] if idx + 1 < len(placed) else total_dur
        chord_dur = max(1.8, next_t - t0 + 0.45)
        add_rhodes_chord(music, max(0.0, t0 - 0.15), chord_dur, cue.chord_midi, amp=0.095)
        # Gentle rhythmic arpeggio bells every ~1.25s following the chapter's character
        step_t = t0 + 0.35
        arp_i = 0
        while step_t < next_t - 0.4:
            note = cue.chord_midi[arp_i % len(cue.chord_midi)] + 12
            pan_a = -0.45 + 0.90 * ((arp_i % 3) / 2.0)
            add_bell_ping(music, step_t, note, amp=0.032, pan=pan_a, decay_rate=3.2)
            step_t += 1.20 if cue.chapter != 2 else 0.85
            arp_i += 1

    # Mathematical Event Sonifications (directly driven by Cycle 5 theorems!)
    # 1. Act 1 (Ch 1): Trace shockwave impact + 3-orbit P^1(F_8) polyrhythmic chimes
    c1_t0 = placed[4][0]  # tau(gamma_0) = 28.22 cue
    add_pincer_impact(music, c1_t0 + 0.45, 53, amp=0.17)
    c1_f8 = placed[6][0]  # P^1(F_8) 3 orbits cue
    orbit_notes = [(72, 76, 79), (74, 77, 81), (75, 79, 82)]
    for k in range(9):
        orb_id = k % 3
        note = orbit_notes[orb_id][(k // 3) % 3]
        add_bell_ping(music, c1_f8 + 0.8 + k * 0.42, note, amp=0.055, pan=-0.5 + 0.5 * orb_id, decay_rate=2.8)

    # 2. Act 2 (Ch 2): NEG-E10 ghost curve reveal chime + Manin rank 45/45 triumph
    add_pincer_impact(music, placed[8][0] + 2.2, 52, amp=0.14)
    add_pincer_impact(music, placed[11][0] + 0.10, 55, amp=0.16)

    # 3. Act 3 (Ch 3): Side-by-side spectral sonification: Tonnetz X golden chord vs. d=106069 detuned eigenvalues!
    c3_listen = placed[13][0]
    # Pure Tonnetz golden frequencies (scaled from 220 Hz base * (1 + eig/3))
    eigs_x = math_data["eigs_X_pos"]
    eigs_q = math_data["eigs_106069_abs"]
    for i, ev in enumerate([eigs_x[1], eigs_x[3], eigs_x[5], eigs_x[10]]):
        add_bell_ping(music, c3_listen + 1.8 + i * 0.28, 69, amp=0.055, pan=-0.45, decay_rate=1.9, freq_hz=261.63 * (1.0 + ev / 3.0))
    for i, ev in enumerate([eigs_q[1], eigs_q[3], eigs_q[5], eigs_q[10]]):
        add_bell_ping(music, c3_listen + 3.2 + i * 0.28, 69, amp=0.055, pan=0.45, decay_rate=1.9, freq_hz=261.63 * (1.0 + ev / 3.0))

    # 4. Act 4 (Ch 4): THREE PINCER LOCK IMPACTS (Theorem D climax!)
    add_pincer_impact(music, placed[16][0] + 0.12, 50, amp=0.19)  # Pincer 1
    add_pincer_impact(music, placed[17][0] + 0.12, 54, amp=0.19)  # Pincer 2
    add_pincer_impact(music, placed[18][0] + 0.12, 57, amp=0.21)  # Pincer 3!
    add_pincer_impact(music, placed[19][0] + 1.20, 62, amp=0.17)  # n=6, u=16 razor kill!

    # 5. Act 5 (Ch 5): Radiant Cmaj9 finale shimmer
    fin_t = placed[-1][1] + 0.2
    add_rhodes_chord(music, fin_t - 0.4, total_dur - fin_t + 0.4, (60, 64, 67, 71, 74), amp=0.125)
    for i, m in enumerate((72, 76, 79, 83, 86)):
        add_bell_ping(music, fin_t + i * 0.18, m, amp=0.055, pan=-0.5 + 0.25 * i, decay_rate=1.2)

    music = apply_stereo_reverb(music, mix=0.20)
    voices = apply_stereo_reverb(voices, mix=0.07)

    # Duck music bed cleanly under narration
    duck_gain = 1.0 - 0.48 * duck_env[:, None]
    mix = music * duck_gain + voices * 1.15

    # Fade in & out + soft master limiter
    fi = int(0.8 * SAMPLE_RATE)
    fo = int(1.6 * SAMPLE_RATE)
    mix[:fi] *= np.linspace(0.0, 1.0, fi)[:, None]
    mix[-fo:] *= np.linspace(1.0, 0.0, fo)[:, None]
    mix = np.tanh(mix * 1.05) * 0.92

    cue_times = [(t0, t1, cue) for t0, t1, cue, _ in placed]
    print(f"  Audio mix ready: total duration = {total_dur:.2f}s ({int(total_dur // 60)}:{total_dur % 60:04.1f}), {len(placed)} cues across 6 chapters.")
    return mix, chapters, cue_times


# ---------------------------------------------------------------------------
# PangoCairo Rendering Helpers
# ---------------------------------------------------------------------------

def draw_rounded_rect(ctx: cairo.Context, x: float, y: float, w: float, h: float, r: float):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -PI / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, PI / 2)
    ctx.arc(x + r, y + h - r, r, PI / 2, PI)
    ctx.arc(x + r, y + r, r, PI, 3 * PI / 2)
    ctx.close_path()


def draw_panel(ctx: cairo.Context, x: float, y: float, w: float, h: float, border=C_PANEL_BORDER, fill=C_PANEL, r: float = 16.0, alpha: float = 1.0):
    draw_rounded_rect(ctx, x, y, w, h, r)
    ctx.set_source_rgba(fill[0], fill[1], fill[2], fill[3] * alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(border[0], border[1], border[2], border[3] * alpha)
    ctx.set_line_width(1.6)
    ctx.stroke()


_FONT_CACHE: Dict[Tuple[str, str, float], Pango.FontDescription] = {}
_BG_CACHE: Dict[Tuple[float, float, float], cairo.ImageSurface] = {}


def draw_text(
    ctx: cairo.Context,
    text: str,
    x: float,
    y: float,
    size: float = 24.0,
    color=C_WHITE,
    bold: bool = False,
    mono: bool = False,
    align: str = "left",
    max_width: float | None = None,
    alpha: float = 1.0,
    markup: bool = False,
) -> Tuple[float, float]:
    layout = PangoCairo.create_layout(ctx)
    fam = "DejaVu Sans Mono" if mono else "DejaVu Sans"
    weight = "Bold" if bold else "Normal"
    fkey = (fam, weight, round(size, 1))
    fdesc = _FONT_CACHE.get(fkey)
    if fdesc is None:
        fdesc = Pango.FontDescription(f"{fam} {weight} {size:.1f}")
        _FONT_CACHE[fkey] = fdesc
    layout.set_font_description(fdesc)
    if max_width is not None:
        layout.set_width(int(max_width * Pango.SCALE))
        layout.set_wrap(Pango.WrapMode.WORD_CHAR)
    if align == "center":
        layout.set_alignment(Pango.Alignment.CENTER)
    elif align == "right":
        layout.set_alignment(Pango.Alignment.RIGHT)
    if markup:
        layout.set_markup(text)
    else:
        layout.set_text(text)
    w_px, h_px = layout.get_pixel_size()
    dx = x
    if align == "center" and max_width is None:
        dx = x - w_px / 2.0
    elif align == "right" and max_width is None:
        dx = x - w_px
    ctx.save()
    ctx.move_to(dx, y)
    ctx.set_source_rgba(color[0], color[1], color[2], color[3] * alpha)
    PangoCairo.show_layout(ctx, layout)
    ctx.restore()
    return float(w_px), float(h_px)


def draw_glow_circle(ctx: cairo.Context, cx: float, cy: float, r: float, color, alpha: float = 1.0, glow_scale: float = 2.6):
    pat = cairo.RadialGradient(cx, cy, r * 0.15, cx, cy, r * glow_scale)
    pat.add_color_stop_rgba(0.0, color[0], color[1], color[2], 0.55 * alpha)
    pat.add_color_stop_rgba(0.5, color[0], color[1], color[2], 0.16 * alpha)
    pat.add_color_stop_rgba(1.0, color[0], color[1], color[2], 0.0)
    ctx.new_sub_path()
    ctx.set_source(pat)
    ctx.arc(cx, cy, r * glow_scale, 0, 2 * PI)
    ctx.fill()
    ctx.new_sub_path()
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)
    ctx.arc(cx, cy, r, 0, 2 * PI)
    ctx.fill()


def _get_cached_bg(accent) -> cairo.ImageSurface:
    key = (accent[0], accent[1], accent[2])
    surf = _BG_CACHE.get(key)
    if surf is None:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        bctx = cairo.Context(surf)
        pat = cairo.RadialGradient(WIDTH * 0.50, HEIGHT * 0.44, 60.0, WIDTH * 0.50, HEIGHT * 0.50, WIDTH * 0.72)
        pat.add_color_stop_rgba(0.0, C_BG_MID[0], C_BG_MID[1], C_BG_MID[2], 1.0)
        pat.add_color_stop_rgba(1.0, C_BG_DEEP[0], C_BG_DEEP[1], C_BG_DEEP[2], 1.0)
        bctx.set_source(pat)
        bctx.paint()
        aur = cairo.RadialGradient(WIDTH * 0.78, HEIGHT * 0.22, 20.0, WIDTH * 0.78, HEIGHT * 0.22, 620.0)
        aur.add_color_stop_rgba(0.0, accent[0], accent[1], accent[2], 0.11)
        aur.add_color_stop_rgba(1.0, accent[0], accent[1], accent[2], 0.0)
        bctx.set_source(aur)
        bctx.paint()
        surf.flush()
        _BG_CACHE[key] = surf
    return surf


def draw_background(ctx: cairo.Context, t: float, accent):
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_SOURCE)
    ctx.set_source_surface(_get_cached_bg(accent), 0.0, 0.0)
    ctx.paint()
    ctx.restore()

    # Subtle drifting observatory grid
    ctx.save()
    ctx.set_source_rgba(C_GRID[0], C_GRID[1], C_GRID[2], 0.14)
    ctx.set_line_width(1.0)
    step = 84.0
    off_x = (t * 8.0) % step
    for gx in range(-1, int(WIDTH / step) + 2):
        x = gx * step + off_x
        ctx.move_to(x, 0)
        ctx.line_to(x, HEIGHT)
    for gy in range(0, int(HEIGHT / step) + 2):
        y = gy * step
        ctx.move_to(0, y)
        ctx.line_to(WIDTH, y)
    ctx.stroke()
    ctx.restore()


def draw_chrome(ctx: cairo.Context, t: float, total_dur: float, chap_idx: int, chap_title: str, accent, active_cue: VoiceCue | None, poster_banner: str | None = None):
    # Top header bar (dynamic x-offset guarantees zero collision)
    w_hdr, _ = draw_text(ctx, "MORPHEUS  ·  ADPIE CYCLE 5", 52, 25, size=14.0, color=accent, bold=True, mono=True)
    draw_text(ctx, "│", 52 + w_hdr + 18, 25, size=14.0, color=C_DIM, mono=True)
    draw_text(ctx, chap_title, 52 + w_hdr + 42, 25, size=14.0, color=C_SLATE, mono=True)
    draw_text(ctx, "ERGENTICS × GEMINI 4 NEON", WIDTH - 52, 25, size=14.0, color=C_DIM, mono=True, align="right")

    # Subtle header divider
    ctx.set_source_rgba(accent[0], accent[1], accent[2], 0.35)
    ctx.set_line_width(1.2)
    ctx.move_to(52, 56)
    ctx.line_to(WIDTH - 52, 56)
    ctx.stroke()

    # Bottom subtitle & speaker badge bar (or hero poster footer)
    bar_y = HEIGHT - 102
    draw_panel(ctx, 52, bar_y, WIDTH - 104, 68, border=(accent[0], accent[1], accent[2], 0.45), fill=(0.025, 0.035, 0.072, 0.90), r=12.0)
    if poster_banner is not None:
        draw_text(ctx, poster_banner, WIDTH / 2.0, bar_y + 21, size=18.0, color=C_GOLD, bold=True, mono=True, align="center")
    elif active_cue is not None:
        sp_meta = {
            "gb": ("EDUCATOR (en-GB)", C_CYAN),
            "rms": ("FORMAL ORACLE (baritone)", C_GOLD),
            "us": ("AUDITOR / HARMONY (en-US)", C_MAGENTA),
        }[active_cue.speaker]
        draw_rounded_rect(ctx, 68, bar_y + 18, 228, 32, 8.0)
        ctx.set_source_rgba(sp_meta[1][0], sp_meta[1][1], sp_meta[1][2], 0.18)
        ctx.fill_preserve()
        ctx.set_source_rgba(sp_meta[1][0], sp_meta[1][1], sp_meta[1][2], 0.85)
        ctx.set_line_width(1.2)
        ctx.stroke()
        draw_text(ctx, sp_meta[0], 182, bar_y + 25, size=11.0, color=sp_meta[1], bold=True, mono=True, align="center")
        draw_text(ctx, active_cue.text, 316, bar_y + 13, size=15.0, color=C_WHITE, max_width=WIDTH - 390)
    else:
        draw_text(ctx, "♪  Generative Neo-Riemannian Score — Zero Cached Data Reads  ♪", WIDTH / 2.0, bar_y + 23, size=15.5, color=C_SLATE, mono=True, align="center")

    # Progress bar along very bottom (suppressed on standalone poster)
    if poster_banner is None:
        p = clamp01(t / max(0.1, total_dur))
        ctx.set_source_rgba(0.20, 0.25, 0.38, 0.45)
        ctx.rectangle(52, HEIGHT - 22, WIDTH - 104, 4.0)
        ctx.fill()
        ctx.set_source_rgba(accent[0], accent[1], accent[2], 0.95)
        ctx.rectangle(52, HEIGHT - 22, (WIDTH - 104) * p, 4.0)
        ctx.fill()


# ---------------------------------------------------------------------------
# Six Chapter Visualizers
# ---------------------------------------------------------------------------

def draw_bruhat_tits_tree(ctx: cairo.Context, cx: float, cy: float, max_r: float, depth: int, grow: float, t: float, alpha: float):
    """Draw a radiant 3-regular Bruhat-Tits 2-adic tree blooming outward."""
    def rec(x: float, y: float, ang: float, r: float, d: int):
        if d <= 0:
            return
        lvl_prog = clamp01(grow * (depth + 1) - (depth - d))
        if lvl_prog <= 0.0:
            return
        spread = PI * 0.42 * (0.72 ** (depth - d))
        branches = [-spread, spread] if d < depth else [0.0, 2.0 * PI / 3.0, 4.0 * PI / 3.0]
        for b_off in branches:
            na = ang + b_off + 0.03 * math.sin(t * 0.9 + d)
            nx = x + r * lvl_prog * math.cos(na)
            ny = y + r * lvl_prog * math.sin(na)
            col = C_CYAN if d % 2 == 0 else C_GOLD
            ctx.set_source_rgba(col[0], col[1], col[2], (0.28 + 0.45 * (d / depth)) * alpha)
            ctx.set_line_width(1.0 + 2.0 * (d / depth))
            ctx.move_to(x, y)
            ctx.line_to(nx, ny)
            ctx.stroke()
            if lvl_prog > 0.7:
                draw_glow_circle(ctx, nx, ny, 2.2 + 2.4 * (d / depth), col, alpha=alpha * 0.85, glow_scale=2.2)
            rec(nx, ny, na, r * 0.58, d - 1)

    draw_glow_circle(ctx, cx, cy, 8.0, C_GOLD, alpha=alpha, glow_scale=3.2)
    rec(cx, cy, -PI / 2.0 + 0.12 * math.sin(t * 0.4), max_r * 0.42, depth)


def render_ch0_overture(ctx: cairo.Context, t: float, t0: float, t1: float, a: float):
    p = seg_prog(t, t0, t1)
    draw_bruhat_tits_tree(ctx, WIDTH * 0.72, HEIGHT * 0.50, 420.0, depth=5, grow=ease_out_cubic(min(1.0, p * 1.4)), t=t, alpha=a * 0.95)

    draw_panel(ctx, 76, 118, 868, 772, border=(C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.55), alpha=a)
    draw_text(ctx, "PRIME CADENCES  ·  ADPIE CYCLE 5", 118, 158, size=16.5, color=C_GOLD, bold=True, mono=True, alpha=a)
    draw_text(ctx, "The Three-Pincer\nSymphony", 114, 198, size=60.0, color=C_WHITE, bold=True, alpha=a)
    draw_text(
        ctx,
        "Chasing a 24-Triad Musical Universe Through\n2-Adic Trees, Modular Forms, and Class Field Towers",
        118, 412, size=21.0, color=C_CYAN, alpha=a,
    )

    items = [
        ("01", "All 7 remaining Section 7 geometry results verified from scratch", C_EMERALD),
        ("02", "Baseline erratum NEG-E10: the missing curve X₀⁶⁹⁰(1) caught & cleared", C_CRIMSON),
        ("03", "Zero-PARI Pure-Rust Manin modular symbols T₂ across all 19 curves", C_VIOLET),
        ("04", "Novelty 3 — Theorem D: degree bound sharpened n ≤ 14  →  n ≤ 8", C_GOLD),
    ]
    for i, (num, desc, col) in enumerate(items):
        ip = smoothstep((p - 0.25 - i * 0.14) / 0.12)
        if ip <= 0:
            continue
        yy = 524 + i * 82
        draw_rounded_rect(ctx, 118, yy, 54, 44, 10.0)
        ctx.set_source_rgba(col[0], col[1], col[2], 0.20 * a * ip)
        ctx.fill_preserve()
        ctx.set_source_rgba(col[0], col[1], col[2], 0.85 * a * ip)
        ctx.set_line_width(1.5)
        ctx.stroke()
        draw_text(ctx, num, 145, yy + 10, size=18.0, color=col, bold=True, mono=True, align="center", alpha=a * ip)
        draw_text(ctx, desc, 192, yy + 5, size=17.5, color=C_WHITE, max_width=708, alpha=a * ip)


def render_ch1_geometry(ctx: cairo.Context, t: float, t0: float, t1: float, a: float, math_data: Dict[str, object]):
    p = seg_prog(t, t0, t1)
    draw_text(ctx, "2-ADIC OBSTRUCTIONS  ·  PROPS 7.3, 7.17 · LEM 7.14 · THM 7.15", 72, 78, size=22.0, color=C_WHITE, bold=True, alpha=a)

    # Panel A: Hamilton Quaternion Sphere vs. gamma_0 = PLRLPRPL
    px, py, pw, ph = 64, 134, 565, 765
    draw_panel(ctx, px, py, pw, ph, border=(C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], 0.65), alpha=a)
    draw_text(ctx, "PROP 7.3  ·  TRACE SHOCKWAVE", px + 28, py + 24, size=16.5, color=C_CRIMSON, bold=True, mono=True, alpha=a)
    draw_text(ctx, "γ₀ = PLRLPRPL = [[5, -12], [-12, 80]]", px + 28, py + 54, size=15.5, color=C_SLATE, mono=True, alpha=a)

    cx, cy = px + pw * 0.50, py + 336
    r_bound = 74.0
    ctx.new_sub_path()
    ctx.set_source_rgba(C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.16 * a)
    ctx.arc(cx, cy, r_bound, 0, 2 * PI)
    ctx.fill()
    ctx.new_sub_path()
    ctx.set_source_rgba(C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.90 * a)
    ctx.set_line_width(2.4)
    ctx.arc(cx, cy, r_bound, 0, 2 * PI)
    ctx.stroke()
    draw_text(ctx, "Compact H×/R×\n0 ≤ τ ≤ 4", cx, cy - 22, size=14.0, color=C_CYAN, bold=True, align="center", alpha=a)

    # Expanding shockwave shattering tau = 4 out to tau = 28.22
    sp = smoothstep((p - 0.18) / 0.25)
    if sp > 0:
        r_shock = r_bound + sp * 104.0
        for ring in range(3):
            rr = r_shock - ring * 22.0
            if rr > r_bound:
                ctx.new_sub_path()
                ctx.set_source_rgba(C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], (0.85 - ring * 0.25) * a * sp)
                ctx.set_line_width(2.8 - ring * 0.7)
                ctx.arc(cx, cy, rr, 0, 2 * PI)
                ctx.stroke()
        draw_glow_circle(ctx, cx + r_shock * 0.70, cy - r_shock * 0.70, 8.0, C_CRIMSON, alpha=a * sp)
        draw_panel(ctx, px + 26, py + 88, 362, 46, border=(C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], 0.75), fill=(0.14, 0.03, 0.06, 0.92), r=10.0, alpha=a * sp)
        draw_text(ctx, "τ(γ₀) = 7225/256 ≈ 28.22 ≫ 4", px + 40, py + 101, size=13.8, color=C_CRIMSON, bold=True, mono=True, alpha=a * sp)

    draw_text(
        ctx,
        "Lean 4 Kernel Proof (0 sorry):\n• prop7_3_hamilton_trace_bound:\n   (2a)² ≤ 4(a² + b² + c² + d²)\n• prop7_3_gamma0_never_compact:\n   ∀ k ≥ 1, tr(γ₀ᵏ)² > 4 det(γ₀ᵏ)\n\n→ Rules out ALL torsion-free\n   arithmetic uniformisations!",
        px + 28, py + 536, size=15.0, color=C_WHITE, mono=True, alpha=a,
    )

    # Panel B: Lemma 7.14 — 2-Adic Slope Doubling vs. Control Disc
    bx, by, bw, bh = 656, 134, 580, 765
    draw_panel(ctx, bx, by, bw, bh, border=(C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.60), alpha=a)
    draw_text(ctx, "LEM 7.14 & THM 7.15  ·  2-ADIC VALUATION", bx + 28, by + 24, size=16.0, color=C_CYAN, bold=True, mono=True, alpha=a)
    draw_text(ctx, "Quotient z ↦ z² around fixed vs. control disc", bx + 28, by + 54, size=15.5, color=C_SLATE, alpha=a)

    gx0, gy0, gw, gh = bx + 64, by + 444, bw - 104, 290
    ctx.set_source_rgba(C_SLATE[0], C_SLATE[1], C_SLATE[2], 0.55 * a)
    ctx.set_line_width(1.6)
    ctx.move_to(gx0, gy0)
    ctx.line_to(gx0 + gw, gy0)
    ctx.move_to(gx0, gy0)
    ctx.line_to(gx0, gy0 - gh)
    ctx.stroke()
    draw_text(ctx, "v₂(z − c)", gx0 + gw - 74, gy0 + 12, size=13.5, color=C_SLATE, mono=True, alpha=a)
    draw_text(ctx, "v₂(z² − c²)", gx0 - 10, gy0 - gh - 26, size=13.5, color=C_SLATE, mono=True, alpha=a)

    lp = smoothstep((p - 0.42) / 0.22)
    mid_x = gx0 + gw * 0.48
    mid_y = gy0 - gh * 0.60
    if lp > 0:
        ctx.set_source_rgba(C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.95 * a)
        ctx.set_line_width(4.0)
        ctx.move_to(gx0 + 18, gy0 - 12)
        ctx.line_to(gx0 + 18 + (mid_x - gx0 - 18) * lp, gy0 - 12 + (mid_y - (gy0 - 12)) * lp)
        ctx.stroke()
        ctx.set_source_rgba(C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.95 * a)
        ctx.set_line_width(3.5)
        ctx.move_to(mid_x, mid_y)
        ctx.line_to(mid_x + (gw * 0.48) * lp, mid_y - (gh * 0.28) * lp)
        ctx.stroke()
        draw_text(ctx, "FIXED DISC\nslope = 2\nv(z²-c²) = 2v(z-c)", gx0 + 22, gy0 - gh + 16, size=13.5, color=C_CYAN, bold=True, mono=True, alpha=a * lp)
        draw_text(ctx, "CONTROL (RCT-2)\nslope = 1\nv(z²-c²) = v(z-c) + v(2c)", mid_x + 4, mid_y + 24, size=12.5, color=C_GOLD, bold=True, mono=True, alpha=a * lp)

    draw_text(
        ctx,
        "At q = 2 (F_v ≅ Q₂), valence count:\n   q + 1 = 3·|Γ_x| + r = 3\n   ⇒ |Γ_x| = 1,  r = 0  (Thm 7.15)\n\nLean 4 Kernel Proofs:\n• lem7_14_ultrametric_doubling\n• lem7_14_control_slope_one\n• thm7_15_q2_free_action",
        bx + 28, by + 516, size=15.0, color=C_WHITE, mono=True, alpha=a,
    )

    # Panel C: Prop 7.17 — P^1(F_8) 9 points in 3 synchronized free orbits
    rx, ry, rw, rh = 1264, 134, 592, 765
    draw_panel(ctx, rx, ry, rw, rh, border=(C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.65), alpha=a)
    draw_text(ctx, "PROP 7.17(b)  ·  PGL₂(F₈) TORSION", rx + 28, ry + 24, size=16.5, color=C_GOLD, bold=True, mono=True, alpha=a)
    draw_text(ctx, "M = [[0, 1], [1, 1]]  ·  3 free orbits on P¹(F₈)", rx + 28, ry + 54, size=13.5, color=C_SLATE, mono=True, alpha=a)

    ocx, ocy = rx + rw * 0.50, ry + 308
    orbits = math_data["f8_orbits"]
    labels_f8 = ["0", "1", "α", "α+1", "α²", "α²+1", "α²+α", "α²+α+1", "∞"]
    orb_colors = [C_CYAN, C_GOLD, C_MAGENTA]
    orb_radii = [164.0, 114.0, 62.0]
    fp = smoothstep((p - 0.65) / 0.25)
    angle_rot = t * 0.55
    for oi, orb in enumerate(orbits):
        col = orb_colors[oi]
        rad = orb_radii[oi]
        pts_xy = []
        for k in range(3):
            ang = angle_rot * (1 if oi % 2 == 0 else -1) + oi * 0.52 + k * (2.0 * PI / 3.0)
            pts_xy.append((ocx + rad * math.cos(ang), ocy + rad * math.sin(ang)))
        ctx.set_source_rgba(col[0], col[1], col[2], (0.30 + 0.58 * fp) * a)
        ctx.set_line_width(2.2)
        for k in range(3):
            p1 = pts_xy[k]
            p2 = pts_xy[(k + 1) % 3]
            ctx.move_to(*p1)
            ctx.line_to(*p2)
        ctx.stroke()
        for k in range(3):
            x, y = pts_xy[k]
            lbl = labels_f8[orb[k]]
            pill_w = max(32.0, len(lbl) * 8.2 + 16.0)
            pill_h = 24.0
            draw_rounded_rect(ctx, x - pill_w * 0.5, y - pill_h * 0.5, pill_w, pill_h, 12.0)
            ctx.set_source_rgba(0.03, 0.04, 0.09, 0.94 * a)
            ctx.fill_preserve()
            ctx.set_source_rgba(col[0], col[1], col[2], (0.65 + 0.35 * fp) * a)
            ctx.set_line_width(1.8)
            ctx.stroke()
            draw_text(ctx, lbl, x, y - 8, size=10.5, color=col, bold=True, mono=True, align="center", alpha=a)

    draw_text(
        ctx,
        "Exhaustive 504-Element Census:\n• |PGL₂(F₈)| = 504  (C++20 / Swift / Rust)\n• Order-3 elements: 56 / 56 act FREELY\n• Zero fixed points on P¹(F₈)\n• Lean 4: prop7_17_f8_order3_free\n• q = 4: off-core only (|Γ_x|=1, r=2)\n• e_v = 2: a + 2b = 2 ⇒ (2,0) ∨ (0,1)",
        rx + 28, ry + 536, size=15.0, color=C_WHITE, mono=True, alpha=a,
    )


def render_ch2_neg_e10_manin(ctx: cairo.Context, t: float, t0: float, t1: float, a: float, math_data: Dict[str, object]):
    p = seg_prog(t, t0, t1)
    draw_text(ctx, "THE MISSING CURVE DETECTIVE STORY  ·  THM 7.11 & NEG-E10", 72, 78, size=22.0, color=C_WHITE, bold=True, alpha=a)

    # Left big plot: All 19 genus-13 Shimura curves plotted by phi(D) vs M = DN/2, with red cutoff wall at phi = 168!
    px, py, pw, ph = 64, 134, 1120, 765
    draw_panel(ctx, px, py, pw, ph, border=(C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], 0.55), alpha=a)
    draw_text(ctx, "EXHAUSTIVE GENUS-13 SHIMURA CENSUS  (2 | D,  φ(D)·ψ(N) ≤ 1000)", px + 30, py + 24, size=17.0, color=C_CYAN, bold=True, mono=True, alpha=a)

    x0, y0, gw, gh = px + 90, py + 660, pw - 145, 535
    ctx.set_source_rgba(C_SLATE[0], C_SLATE[1], C_SLATE[2], 0.55 * a)
    ctx.set_line_width(1.6)
    ctx.move_to(x0, y0)
    ctx.line_to(x0 + gw, y0)
    ctx.move_to(x0, y0)
    ctx.line_to(x0, y0 - gh)
    ctx.stroke()

    def map_x(phi_v: float) -> float:
        return x0 + (phi_v / 192.0) * gw

    def map_y(m_v: float) -> float:
        return y0 - ((m_v - 80.0) / 290.0) * gh

    for pv in [0, 40, 80, 120, 160, 176]:
        xx = map_x(pv)
        ctx.set_source_rgba(C_GRID[0], C_GRID[1], C_GRID[2], 0.35 * a)
        ctx.move_to(xx, y0)
        ctx.line_to(xx, y0 - gh)
        ctx.stroke()
        draw_text(ctx, str(pv), xx, y0 + 12, size=13.5, color=C_SLATE if pv != 176 else C_CRIMSON, bold=(pv == 176), mono=True, align="center", alpha=a)
    draw_text(ctx, "Euler φ(D)", x0 + gw * 0.5, y0 + 44, size=15.0, color=C_SLATE, mono=True, align="center", alpha=a)
    for mv in [100, 160, 220, 280, 345]:
        yy = map_y(mv)
        ctx.set_source_rgba(C_GRID[0], C_GRID[1], C_GRID[2], 0.35 * a)
        ctx.move_to(x0, yy)
        ctx.line_to(x0 + gw, yy)
        ctx.stroke()
        draw_text(ctx, str(mv), x0 - 12, yy - 9, size=13.5, color=C_SLATE if mv != 345 else C_CRIMSON, bold=(mv == 345), mono=True, align="right", alpha=a)
    draw_text(ctx, "Level M = DN/2", x0 - 10, y0 - gh - 28, size=14.0, color=C_SLATE, mono=True, alpha=a)

    # Red cutoff wall at phi = 168 (12 * 14 from shimura_multi.py:17)
    wx = map_x(168.0)
    wall_p = smoothstep((p - 0.14) / 0.14)
    if wall_p > 0:
        ctx.save()
        ctx.set_dash([10.0, 7.0])
        ctx.set_source_rgba(C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], 0.90 * a * wall_p)
        ctx.set_line_width(2.6)
        ctx.move_to(wx, y0)
        ctx.line_to(wx, y0 - gh * wall_p)
        ctx.stroke()
        ctx.restore()
        draw_text(ctx, "shimura_multi.py:17\ncutoff  φ ≤ 168", wx - 12, y0 - gh + 10, size=14.0, color=C_CRIMSON, bold=True, mono=True, align="right", alpha=a * wall_p)

    # Plot the 18 known curves + reveal the 19th NEG-E10 curve at (phi=176, M=345)!
    shim19 = math_data["shimura_19"]
    rev18 = smoothstep(p / 0.24)
    rev_ghost = smoothstep((p - 0.32) / 0.18)
    for idx, (D, N, phiD, psiN, e2, e3) in enumerate(shim19):
        M = (D * N) // 2
        cx, cy = map_x(phiD), map_y(M)
        if D == 690:
            if rev_ghost > 0:
                pulse = 1.0 + 0.18 * math.sin(t * 5.0)
                draw_glow_circle(ctx, cx, cy, 13.0 * pulse * rev_ghost, C_CRIMSON, alpha=a * rev_ghost, glow_scale=3.8)
                draw_glow_circle(ctx, cx, cy, 6.0 * rev_ghost, C_GOLD, alpha=a * rev_ghost, glow_scale=1.6)
                bx_e, by_e, bw_e, bh_e = map_x(46.0), map_y(265.0), 386.0, 122.0
                ctx.set_source_rgba(C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], 0.85 * a * rev_ghost)
                ctx.set_line_width(2.0)
                ctx.move_to(bx_e + bw_e, by_e + 16.0)
                ctx.line_to(cx - 14.0, cy + 6.0)
                ctx.stroke()
                draw_panel(ctx, bx_e, by_e, bw_e, bh_e, border=C_CRIMSON, fill=(0.12, 0.03, 0.06, 0.94), r=12.0, alpha=a * rev_ghost)
                draw_text(ctx, "NEG-E10: X₀⁶⁹⁰(1) FOUND!", bx_e + 20, by_e + 14, size=15.5, color=C_GOLD, bold=True, mono=True, alpha=a * rev_ghost)
                draw_text(ctx, "D = 2·3·5·23 = 690,  N = 1\nφ(690) = 176 > 168,  e₂=0, e₃=8\ng = 1 + 176/12 - 8/3 = 13", bx_e + 20, by_e + 44, size=13.5, color=C_WHITE, mono=True, alpha=a * rev_ghost)
        else:
            if rev18 > 0:
                tf = (e2 == 0 and e3 == 0)
                col = C_CYAN if tf else C_GOLD
                draw_glow_circle(ctx, cx, cy, 6.8 * rev18, col, alpha=a * 0.90, glow_scale=2.1)
                if D in (546, 570, 302, 334):
                    draw_text(ctx, f"D={D}", cx - 10, cy - 26, size=12.5, color=col, mono=True, align="right", alpha=a * rev18)

    # Legend inside plot
    draw_glow_circle(ctx, x0 + 28, y0 - gh + 28, 6.5, C_CYAN, alpha=a)
    draw_text(ctx, "11 torsion-free pairs (e₂=e₃=0)", x0 + 48, y0 - gh + 18, size=14.0, color=C_WHITE, mono=True, alpha=a)
    draw_glow_circle(ctx, x0 + 28, y0 - gh + 56, 6.5, C_GOLD, alpha=a)
    draw_text(ctx, "7 known torsion pairs (φ ≤ 168)", x0 + 48, y0 - gh + 46, size=14.0, color=C_WHITE, mono=True, alpha=a)
    draw_glow_circle(ctx, x0 + 28, y0 - gh + 84, 6.5, C_CRIMSON, alpha=a)
    draw_text(ctx, "1 omitted curve: D=690, N=1 (NEG-E10)", x0 + 48, y0 - gh + 74, size=14.0, color=C_CRIMSON, bold=True, mono=True, alpha=a)

    # Right panel: Zero-PARI Pure-Rust Manin Modular Symbols T_2 Verdict!
    rx, ry, rw, rh = 1212, 134, 644, 765
    draw_panel(ctx, rx, ry, rw, rh, border=(C_VIOLET[0], C_VIOLET[1], C_VIOLET[2], 0.70), alpha=a)
    draw_text(ctx, "ZERO-PARI PURE-RUST MANIN T₂", rx + 28, ry + 26, size=17.5, color=C_VIOLET, bold=True, mono=True, alpha=a)
    draw_text(ctx, "rust/src/section7_cycle5.rs  (zero external crates)", rx + 28, ry + 56, size=14.0, color=C_SLATE, mono=True, alpha=a)

    mp_prog = smoothstep((p - 0.58) / 0.20)
    mx0, my0, msz = rx + 32, ry + 114, 210
    cell = msz / 15.0
    for r in range(15):
        for c in range(15):
            active = ((r * 7 + c * 11 + 3) % 5 == 0) or (r == c)
            if r == c and mp_prog > (r / 15.0):
                col = C_EMERALD
                al = 0.92
            elif active:
                col = C_VIOLET
                al = 0.35 + 0.30 * mp_prog
            else:
                col = C_GRID
                al = 0.14
            ctx.set_source_rgba(col[0], col[1], col[2], al * a)
            ctx.rectangle(mx0 + c * cell + 1, my0 + r * cell + 1, cell - 2, cell - 2)
            ctx.fill()

    draw_text(
        ctx,
        "M = 345  (D = 690, N = 1)\n\n"
        "M₂(Γ₀(345))⁻  over  F₁₀₀₀₀₀₃\n"
        "• Manin dim  = 45\n"
        "• tr(T₂)     ≡ -5  (mod q)\n"
        "• rank(P_X)  = 45 / 45",
        mx0 + msz + 24, my0 + 18, size=14.0, color=C_WHITE, mono=True, alpha=a * max(0.3, mp_prog),
    )

    verdict_p = smoothstep((p - 0.78) / 0.14)
    draw_panel(ctx, rx + 28, ry + 372, rw - 56, 360, border=(C_EMERALD[0], C_EMERALD[1], C_EMERALD[2], 0.75), fill=(0.03, 0.10, 0.08, 0.90), r=14.0, alpha=a * max(0.25, verdict_p))
    draw_text(ctx, "DUAL VERDICT: THM 7.11 STANDS", rx + 52, ry + 394, size=18.5, color=C_EMERALD, bold=True, mono=True, alpha=a * max(0.25, verdict_p))
    draw_text(
        ctx,
        "1. Pure Rust (ZERO PARI):\n"
        "   Full rank of T₂⁴ - 4T₂² + I on ALL\n"
        "   18 distinct levels (all 19 curves)!\n\n"
        "2. From-Scratch PARI/GP:\n"
        "   dim S₂^{345-new}(Γ₀(345)) = 15\n"
        "   charpoly(T₂) mod (t⁴ - 4t² + 1) =\n"
        "     3t³ + t² + 21t + 7  ≠  0\n"
        "   + all 4 Γ_H variants excluded!\n\n"
        "Paper erratum queued: 18 → 19 pairs.",
        rx + 52, ry + 436, size=14.5, color=C_WHITE, mono=True, alpha=a * max(0.25, verdict_p),
    )


def render_ch3_brandt_106069(ctx: cairo.Context, t: float, t0: float, t1: float, a: float, math_data: Dict[str, object]):
    p = seg_prog(t, t0, t1)
    draw_text(ctx, "THE BRANDT ORCHESTRA  ·  PROP 7.18 & QUINTIC NEAR-MISS d = 106069", 72, 78, size=22.0, color=C_WHITE, bold=True, alpha=a)

    # Top half: Real 24-vertex PLR Tonnetz Dual X vs. 24-vertex bipartite 3-regular Quintic 106069
    draw_panel(ctx, 64, 134, 880, 410, border=(C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.60), alpha=a)
    draw_text(ctx, "TONNETZ DUAL X  (24 triads, 3-regular, g = 13)", 94, 158, size=16.5, color=C_GOLD, bold=True, mono=True, alpha=a)
    cx1, cy1 = 504, 355
    for u_v, v_v in math_data["tonnetz_edges"]:
        a1 = 2.0 * PI * u_v / 24.0 + t * 0.14
        a2 = 2.0 * PI * v_v / 24.0 + t * 0.14
        ctx.set_source_rgba(C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.44 * a)
        ctx.set_line_width(1.7)
        ctx.move_to(cx1 + 142 * math.cos(a1), cy1 + 142 * math.sin(a1))
        ctx.line_to(cx1 + 142 * math.cos(a2), cy1 + 142 * math.sin(a2))
        ctx.stroke()
    for k in range(24):
        ang = 2.0 * PI * k / 24.0 + t * 0.14
        draw_glow_circle(ctx, cx1 + 142 * math.cos(ang), cy1 + 142 * math.sin(ang), 5.5, C_GOLD if k % 2 == 0 else C_CYAN, alpha=a)

    draw_panel(ctx, 976, 134, 880, 410, border=(C_MAGENTA[0], C_MAGENTA[1], C_MAGENTA[2], 0.60), alpha=a)
    draw_text(ctx, "QUINTIC NEAR-MISS d_F = 106069  (D'' = p₁₃, 24 vertices, g = 13)", 1004, 158, size=14.6, color=C_MAGENTA, bold=True, mono=True, alpha=a)
    cx2, cy2 = 1416, 355
    for k in range(24):
        ang = 2.0 * PI * k / 24.0 - t * 0.14
        x1, y1 = cx2 + 142 * math.cos(ang), cy2 + 142 * math.sin(ang)
        for step in (1, 5 if k % 2 == 0 else -5):
            ang2 = 2.0 * PI * ((k + step) % 24) / 24.0 - t * 0.14
            x2, y2 = cx2 + 142 * math.cos(ang2), cy2 + 142 * math.sin(ang2)
            ctx.set_source_rgba(C_MAGENTA[0], C_MAGENTA[1], C_MAGENTA[2], 0.42 * a)
            ctx.set_line_width(1.7)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()
    for k in range(24):
        ang = 2.0 * PI * k / 24.0 - t * 0.14
        draw_glow_circle(ctx, cx2 + 142 * math.cos(ang), cy2 + 142 * math.sin(ang), 5.5, C_MAGENTA if k % 2 == 0 else C_VIOLET, alpha=a)

    # Bottom Spectral Comparator
    sx, sy, sw, sh = 64, 570, 1792, 330
    draw_panel(ctx, sx, sy, sw, sh, border=(C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.55), alpha=a)
    draw_text(ctx, "SPECTRAL FINGERPRINT  |λ| ∈ [0, 3]  —  WHY 106069 MISSES X  (t⁴ − 4t² + 1 ∤ charpoly)", sx + 30, sy + 20, size=16.5, color=C_CYAN, bold=True, mono=True, alpha=a)

    lx0, lw = sx + 178, sw - 230
    y_ton = sy + 120
    y_106 = sy + 196

    def mx(val: float) -> float:
        return lx0 + (val / 3.08) * lw

    for y_row, lbl, col in [(y_ton, "Tonnetz X", C_GOLD), (y_106, "d = 106069", C_MAGENTA)]:
        ctx.set_source_rgba(C_SLATE[0], C_SLATE[1], C_SLATE[2], 0.45 * a)
        ctx.set_line_width(2.0)
        ctx.move_to(lx0, y_row)
        ctx.line_to(lx0 + lw, y_row)
        ctx.stroke()
        draw_text(ctx, lbl, lx0 - 18, y_row - 10, size=14.5, color=col, bold=True, mono=True, align="right", alpha=a)

    # Highlight required golden eigenvalues 2cos(pi/12) = 1.9319 and 2cos(5pi/12) = 0.5176
    sp = smoothstep((p - 0.35) / 0.25)
    for target_v, t_lbl in [(2.0 * math.cos(PI / 12.0), "2cos(π/12) ≈ 1.932"), (2.0 * math.cos(5.0 * PI / 12.0), "2cos(5π/12) ≈ 0.518")]:
        tx = mx(target_v)
        ctx.save()
        ctx.set_dash([6.0, 5.0])
        ctx.set_source_rgba(C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.78 * a * sp)
        ctx.set_line_width(2.0)
        ctx.move_to(tx, sy + 72)
        ctx.line_to(tx, sy + 236)
        ctx.stroke()
        ctx.restore()
        draw_text(ctx, t_lbl, tx, sy + 52, size=13.0, color=C_GOLD, bold=True, mono=True, align="center", alpha=a * sp)

    for ev in math_data["eigs_X_pos"]:
        draw_glow_circle(ctx, mx(ev), y_ton, 7.8, C_GOLD, alpha=a)
    for ev in math_data["eigs_106069_abs"]:
        draw_glow_circle(ctx, mx(ev), y_106, 7.8, C_MAGENTA, alpha=a)

    draw_text(
        ctx,
        "From-scratch PARI Brandt audit: ALL 118 split-2 quadratics (D = 41, 137 torsion) + ALL 13 cubic/quartic solutions\n"
        "(6 torsion; 7 torsion-free: 733, 148, 469×2, 316, 2777×2) + quintic near-miss d = 106069  →  ZERO match Tonnetz X!",
        sx + 30, sy + 258, size=14.2, color=C_EMERALD, bold=True, mono=True, alpha=a,
    )


def render_ch4_theorem_d_pincers(ctx: cairo.Context, t: float, t0: float, t1: float, a: float, math_data: Dict[str, object], cue_times: List[Tuple[float, float, VoiceCue]]):
    """CLIMAX: Live animated Three-Pincer Theorem D Matrix + Razor-Sharp n=6, u=16 L_v Zoom!"""
    t_p1 = cue_times[16][0]
    t_p2 = cue_times[17][0]
    t_p3 = cue_times[18][0]
    t_n6 = cue_times[19][0]

    p1_prog = smoothstep((t - t_p1) / 1.4)
    p2_prog = smoothstep((t - t_p2) / 1.4)
    p3_prog = smoothstep((t - t_p3) / 1.6)
    n6_prog = smoothstep((t - t_n6) / 1.4)

    draw_text(ctx, "NOVELTY 3: THEOREM D  ·  THREE-PINCER HILBERT CLASS FIELD OBSTRUCTION", 72, 78, size=22.0, color=C_GOLD, bold=True, alpha=a)

    # Left Main Panel: 2D Constraint Grid over degree n in [6..15] (columns) and u = 2^k (rows k = 0..8)
    gx, gy, gw, gh = 64, 134, 1170, 765
    draw_panel(ctx, gx, gy, gw, gh, border=(C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.65), alpha=a)
    draw_text(ctx, "SURVIVOR LANDSCAPE  (degree n  vs.  narrow-class ratio u = h⁺/h = 2ᵏ)", gx + 28, gy + 24, size=16.5, color=C_WHITE, bold=True, mono=True, alpha=a)

    pgrid = math_data["pincer_grid"]
    col_x0, row_y0 = gx + 108, gy + 636
    cw, ch = 100.0, 56.0

    for ci, n in enumerate(range(6, 16)):
        lbl = f"n={n}" if n < 15 else "n≥15"
        col_hdr = C_EMERALD if n <= 8 else (C_CRIMSON if p3_prog > 0.5 else C_SLATE)
        draw_text(ctx, lbl, col_x0 + ci * cw + cw * 0.5, row_y0 + 16, size=16.0, color=col_hdr, bold=True, mono=True, align="center", alpha=a)

    for k in range(9):
        u = 1 << k
        yy = row_y0 - (k + 1) * ch
        draw_text(ctx, f"u={u}", col_x0 - 16, yy + 17, size=14.0, color=C_SLATE, mono=True, align="right", alpha=a)

    for ci, n in enumerate(range(6, 16)):
        for k in range(9):
            if n < 15 and k >= n:
                continue
            xx = col_x0 + ci * cw + 4
            yy = row_y0 - (k + 1) * ch + 4
            w_c, h_c = cw - 8, ch - 8

            if n == 15:
                killed = p1_prog > 0.25
                fill = (C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.25 + 0.45 * p1_prog) if killed else (0.14, 0.18, 0.28, 0.55)
                bdr = C_CYAN if killed else C_DIM
                tag = "b=4.2" if killed else "OPEN"
            else:
                info = pgrid[(n, k)]
                st = info["status"]
                if st == "P1" and p1_prog > 0.20:
                    fill = (C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.30 + 0.40 * p1_prog)
                    bdr = C_CYAN
                    tag = "P1 ✕"
                elif st == "P3" and p3_prog > 0.20:
                    fill = (C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.30 + 0.45 * p3_prog)
                    bdr = C_GOLD
                    tag = "P3 ✕"
                elif st == "ALIVE_H1" and p2_prog > 0.20:
                    fill = (C_EMERALD[0], C_EMERALD[1], C_EMERALD[2], 0.26)
                    bdr = C_EMERALD
                    tag = "h=1"
                elif st == "ALIVE_ANY":
                    fill = (C_EMERALD[0], C_EMERALD[1], C_EMERALD[2], 0.38)
                    bdr = C_EMERALD
                    tag = "OPEN"
                elif p2_prog > 0.20 and info["m_h2"] > 0:
                    fill = (C_MAGENTA[0], C_MAGENTA[1], C_MAGENTA[2], 0.28)
                    bdr = C_MAGENTA
                    tag = "h≥2 ✕"
                else:
                    fill = (0.16, 0.20, 0.30, 0.58)
                    bdr = C_DIM
                    tag = "?"

            if n == 6 and k == 4 and n6_prog > 0.1:
                pulse = 0.65 + 0.35 * math.sin(t * 7.0)
                bdr = C_CRIMSON
                fill = (C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], 0.35 + 0.30 * pulse)
                tag = "L_v ✕!"

            draw_rounded_rect(ctx, xx, yy, w_c, h_c, 7.0)
            ctx.set_source_rgba(fill[0], fill[1], fill[2], fill[3] * a)
            ctx.fill_preserve()
            ctx.set_source_rgba(bdr[0], bdr[1], bdr[2], 0.85 * a)
            ctx.set_line_width(2.2 if (n == 6 and k == 4 and n6_prog > 0.1) else 1.2)
            ctx.stroke()
            draw_text(ctx, tag, xx + w_c * 0.5, yy + 14, size=13.0, color=C_WHITE, bold=True, mono=True, align="center", alpha=a)

    # Big red elimination bracket over n = 9..15 once Pincer 3 locks!
    if p3_prog > 0.35:
        bx1 = col_x0 + 3 * cw + 4
        bx2 = col_x0 + 10 * cw - 4
        by_b = gy + 70
        draw_rounded_rect(ctx, bx1, by_b, bx2 - bx1, 44, 10.0)
        ctx.set_source_rgba(C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], 0.22 * a * p3_prog)
        ctx.fill_preserve()
        ctx.set_source_rgba(C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], 0.92 * a * p3_prog)
        ctx.set_line_width(2.0)
        ctx.stroke()
        draw_text(ctx, "DEGREES n ≥ 9 UNCONDITIONALLY ELIMINATED  (n ≤ 14 → n ≤ 8)", (bx1 + bx2) * 0.5, by_b + 13, size=13.2, color=C_WHITE, bold=True, mono=True, align="center", alpha=a * p3_prog)

    # Clean 2-line legend strictly inside left panel
    draw_text(
        ctx,
        "P1 (Cyan): Base field F + odd reciprocity   |   P2 (Magenta): Wide HCF H_F (kills h_F ≥ 2)\n"
        "P3 (Gold): Exp-2 field L_v (kills h_F = 1)  |   Green: Surviving Open (2)  |  Crimson: Razor kill n=6, u=16",
        gx + 28, gy + 702, size=12.4, color=C_SLATE, mono=True, alpha=a,
    )

    # Right Panel: Live Razor-Sharp Zoom on n = 6, u = 16 (L_v deg 48 at b = 6.00) + Ceiling Collapse
    rx, ry, rw, rh = 1260, 134, 596, 765
    draw_panel(ctx, rx, ry, rw, rh, border=(C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.65), alpha=a)
    draw_text(ctx, "RAZOR KILL ZOOM:  n = 6,  u = 16,  h_F = 1", rx + 26, ry + 24, size=16.0, color=C_GOLD, bold=True, mono=True, alpha=a)
    draw_text(ctx, "Decomposition field L_v (deg 48, 8 norm-2 primes)", rx + 26, ry + 54, size=13.2, color=C_SLATE, mono=True, alpha=a)

    zx0, zy0, zw, zh = rx + 62, ry + 392, rw - 92, 272
    ctx.set_source_rgba(C_SLATE[0], C_SLATE[1], C_SLATE[2], 0.55 * a)
    ctx.set_line_width(1.5)
    ctx.move_to(zx0, zy0)
    ctx.line_to(zx0 + zw, zy0)
    ctx.move_to(zx0, zy0)
    ctx.line_to(zx0, zy0 - zh)
    ctx.stroke()

    def zmx(bv: float) -> float:
        return zx0 + ((bv - 4.2) / 3.3) * zw

    def zmy(rv: float) -> float:
        return zy0 - ((rv - 18.10) / 0.64) * zh

    # Y-axis reference ticks
    for rv_t in (18.2, 18.4, 18.6):
        yt = zmy(rv_t)
        draw_text(ctx, f"{rv_t:.1f}", zx0 - 8, yt - 8, size=11.0, color=C_DIM, mono=True, align="right", alpha=a)

    ub_6_16 = math_data["ub_6_16"]
    uy = zmy(ub_6_16)
    ctx.save()
    ctx.set_dash([8.0, 6.0])
    ctx.set_source_rgba(C_CRIMSON[0], C_CRIMSON[1], C_CRIMSON[2], 0.90 * a)
    ctx.set_line_width(2.2)
    ctx.move_to(zx0, uy)
    ctx.line_to(zx0 + zw, uy)
    ctx.stroke()
    ctx.restore()
    draw_text(ctx, f"UB(6, 16) = {ub_6_16:.6f}", zx0 + 10, uy - 24, size=12.8, color=C_CRIMSON, bold=True, mono=True, alpha=a)

    # Clip L_v lower-bound curve strictly inside the axes
    curve = math_data["lv_curve"]
    ctx.save()
    ctx.rectangle(zx0, zy0 - zh, zw, zh)
    ctx.clip()
    ctx.set_source_rgba(C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.96 * a)
    ctx.set_line_width(3.2)
    for idx, (bv, rv) in enumerate(curve):
        x, y = zmx(bv), zmy(rv)
        if idx == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.stroke()
    ctx.restore()

    # Peak dot at b = 6.00 + clean leader callout sitting in empty space under the arch!
    lv_peak = math_data["lv_peak_6"]
    margin_6 = lv_peak - ub_6_16
    peak_x, peak_y = zmx(6.0), zmy(lv_peak)
    draw_glow_circle(ctx, peak_x, peak_y, 7.5, C_EMERALD, alpha=a, glow_scale=3.0)

    cb_x, cb_y, cb_w, cb_h = zx0 + 178, ry + 266, 286, 84
    ctx.set_source_rgba(C_EMERALD[0], C_EMERALD[1], C_EMERALD[2], 0.72 * a)
    ctx.set_line_width(1.6)
    ctx.move_to(peak_x, peak_y + 9)
    ctx.line_to(cb_x + 98, cb_y)
    ctx.stroke()
    draw_panel(ctx, cb_x, cb_y, cb_w, cb_h, border=(C_EMERALD[0], C_EMERALD[1], C_EMERALD[2], 0.80), fill=(0.03, 0.11, 0.09, 0.94), r=10.0, alpha=a)
    draw_text(
        ctx,
        f"b = 6.00  (peak > ceiling!)\nLB = {lv_peak:.6f}\nmargin = +{margin_6:.6f}",
        cb_x + 14, cb_y + 10, size=12.6, color=C_EMERALD, bold=True, mono=True, alpha=a,
    )
    draw_text(ctx, "Poitou parameter b  ∈  [4.2, 7.5]", zx0 + zw * 0.5, zy0 + 12, size=13.0, color=C_SLATE, mono=True, align="center", alpha=a)

    # Discriminant Ceiling Collapse Summary Box
    draw_panel(ctx, rx + 26, ry + 448, rw - 52, 290, border=(C_EMERALD[0], C_EMERALD[1], C_EMERALD[2], 0.65), fill=(0.03, 0.08, 0.09, 0.92), r=14.0, alpha=a)
    draw_text(ctx, "OPEN PROBLEM (2) COLLAPSE", rx + 44, ry + 468, size=17.0, color=C_EMERALD, bold=True, mono=True, alpha=a)
    draw_text(
        ctx,
        "• Degree ceiling:  n ≤ 14  →  n ≤ 8\n"
        "• Worst n=9 kill:  +0.3392 (u=4, odd_B)\n"
        "• n = 7: h_F = 1, u ≤ 4 (d_F ≤ 1.60e8, 6.4×)\n"
        "• n = 8: h_F = 1, u ≤ 4 (d_F ≤ 2.24e9, 10.1×)\n"
        "• n = 6: u ∈ {16, 32} DEAD unconditionally\n"
        "         d_F ≤ 6.67e7  →  2.65e7  (2.52×)\n"
        "• Quad err: 4.44e-16 (3×10¹³× < margin)\n"
        "• Pure Swift vs C++20 delta:  0.000e+00",
        rx + 44, ry + 506, size=13.4, color=C_WHITE, mono=True, alpha=a,
    )


def render_ch5_finale(ctx: cairo.Context, t: float, t0: float, t1: float, a: float):
    p = seg_prog(t, t0, t1)
    draw_text(ctx, "FOUR INDEPENDENT CODE PLANES  ·  ZERO CACHED DATA READS", WIDTH / 2.0, 96, size=28.0, color=C_WHITE, bold=True, align="center", alpha=a)
    draw_text(ctx, "Audit-Forward ADPIE Cycle 5  ·  Ready for Head-to-Head Reconciliation", WIDTH / 2.0, 140, size=18.5, color=C_CYAN, mono=True, align="center", alpha=a)

    cards = [
        ("PLANE 1  ·  LEAN 4.36.0", C_CYAN, "33 / 33 THEOREMS", "Zero Mathlib · 0 sorryAx · 0 ofReduceBool\nProp 7.3, Lem 7.14, Thm 7.15, Prop 7.17,\nTheorem D core & NEG-E10 kernel-checked"),
        ("PLANE 2  ·  SWIFT++ TRIPLE-CHECK", C_GOLD, "0.000e+00 DELTA", "g++ 13.3 & clang++ 18.1 (-Werror) 33/33\nPure Swift 6.4 (16/16) × Interop (22/22)\nFrom-scratch GL-64 Poitou-Odlyzko + PGL₂(F₈)"),
        ("PLANE 3  ·  PURE RUST 1.100.0", C_VIOLET, "10 / 10 TESTS", "Zero external crates · ZERO PARI!\nManin modular symbols T₂ over F₁₀₀₀₀₀₃\nFull rank on all 18 levels (19 curves, M=345)"),
        ("PLANE 4  ·  FROM-SCRATCH PARI/GP", C_EMERALD, "19 + 4 + 13 + 1", "ergentics/shimura_brandt_xcheck.py (MIT)\nAll 19 X₀^D(N) + 4 Γ_H + 118 quadratics +\nall 13 Prop 7.18 Brandt graphs + quintic 106069"),
    ]
    cw, ch = 856, 260
    coords = [(76, 206), (988, 206), (76, 496), (988, 496)]
    for i, ((title, col, stat, body), (cx, cy)) in enumerate(zip(cards, coords)):
        cp = smoothstep((p - i * 0.12) / 0.18)
        draw_panel(ctx, cx, cy, cw, ch, border=(col[0], col[1], col[2], 0.78), alpha=a * cp)
        draw_text(ctx, title, cx + 30, cy + 24, size=17.0, color=col, bold=True, mono=True, alpha=a * cp)
        draw_text(ctx, stat, cx + cw - 30, cy + 22, size=24.0, color=C_WHITE, bold=True, mono=True, align="right", alpha=a * cp)
        draw_text(ctx, body, cx + 30, cy + 84, size=17.5, color=C_SLATE, mono=True, alpha=a * cp)

    # Footer banner
    fp = smoothstep((p - 0.55) / 0.20)
    draw_panel(ctx, 76, 790, WIDTH - 152, 134, border=(C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.65), fill=(0.04, 0.05, 0.11, 0.94), r=16.0, alpha=a * fp)
    draw_text(ctx, "MORPHEUS  ·  github.com/Ergentics1/Morpheus", WIDTH / 2.0, 814, size=25.0, color=C_GOLD, bold=True, mono=True, align="center", alpha=a * fp)
    draw_text(ctx, "Ergentics (Author) × Gemini 4 Neon (Cycle 5)  ·  MIT Code / CC BY 4.0 Media  ·  All v0.2.0 Baselines Preserved", WIDTH / 2.0, 864, size=16.5, color=C_WHITE, align="center", alpha=a * fp)


# ---------------------------------------------------------------------------
# Master Frame Renderer + Multiprocessing Pipe to FFmpeg
# ---------------------------------------------------------------------------

CHAP_META = [
    (0, "ACT I  ·  THE SHIMURA QUESTION & 2-ADIC TREE", C_GOLD),
    (1, "ACT II  ·  TRACE SHOCKWAVE, 2-ADIC DOUBLING & P¹(F₈) ORBITS", C_CYAN),
    (2, "ACT III  ·  NEG-E10: THE MISSING CURVE X₀⁶⁹⁰(1) & PURE-RUST MANIN T₂", C_CRIMSON),
    (3, "ACT IV  ·  THE BRANDT ORCHESTRA & QUINTIC NEAR-MISS d = 106069", C_MAGENTA),
    (4, "ACT V  ·  NOVELTY 3 — THEOREM D: THE THREE-PINCER OBSTRUCTION", C_GOLD),
    (5, "ACT VI  ·  FOUR-PLANE INDEPENDENT VERIFICATION FINALE", C_EMERALD),
]

_G_MATH: Dict[str, object] = {}
_G_CHAPTERS: List[Tuple[int, float, float]] = []
_G_CUES: List[Tuple[float, float, VoiceCue]] = []
_G_TOTAL_DUR: float = 1.0
_G_SURF: cairo.ImageSurface | None = None
_G_CTX: cairo.Context | None = None


def _init_worker(math_data, chapters, cue_times, total_dur):
    global _G_MATH, _G_CHAPTERS, _G_CUES, _G_TOTAL_DUR, _G_SURF, _G_CTX
    _G_MATH = math_data
    _G_CHAPTERS = chapters
    _G_CUES = cue_times
    _G_TOTAL_DUR = total_dur
    _G_SURF = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    _G_CTX = cairo.Context(_G_SURF)
    _G_CTX.set_antialias(cairo.ANTIALIAS_GOOD)


def _draw_frame_into_surface(frame_idx: int, poster_banner: str | None = None) -> cairo.ImageSurface:
    assert _G_SURF is not None and _G_CTX is not None
    ctx = _G_CTX
    t = frame_idx / FPS

    active_ch = _G_CHAPTERS[-1]
    for ch in _G_CHAPTERS:
        if ch[1] <= t < ch[2]:
            active_ch = ch
            break
    ch_id, c0, c1 = active_ch
    _, ch_title, accent = CHAP_META[ch_id]

    active_cue = None
    if poster_banner is None:
        for qt0, qt1, cue in _G_CUES:
            if qt0 - 0.10 <= t <= qt1 + 0.35:
                active_cue = cue
                break

    draw_background(ctx, t, accent)

    for cid, st, en in _G_CHAPTERS:
        al = scene_alpha(t, st - 0.25, en + 0.25, fade_in=0.55, fade_out=0.55)
        if al <= 0.005:
            continue
        if cid == 0:
            render_ch0_overture(ctx, t, st, en, al)
        elif cid == 1:
            render_ch1_geometry(ctx, t, st, en, al, _G_MATH)
        elif cid == 2:
            render_ch2_neg_e10_manin(ctx, t, st, en, al, _G_MATH)
        elif cid == 3:
            render_ch3_brandt_106069(ctx, t, st, en, al, _G_MATH)
        elif cid == 4:
            render_ch4_theorem_d_pincers(ctx, t, st, en, al, _G_MATH, _G_CUES)
        elif cid == 5:
            render_ch5_finale(ctx, t, st, en, al)

    draw_chrome(ctx, t, _G_TOTAL_DUR, ch_id, ch_title, accent, active_cue, poster_banner=poster_banner)
    _G_SURF.flush()
    return _G_SURF


def render_frame_bytes(frame_idx: int, poster_banner: str | None = None) -> bytes:
    return bytes(_draw_frame_into_surface(frame_idx, poster_banner=poster_banner).get_data())


def _render_segment(args: Tuple[int, int, int, str, Dict[str, object], list, list, float]) -> str:
    """Zero-IPC direct-to-FFmpeg segment encoder (avoids pickling 49 GB of raw BGRA frames)."""
    seg_id, f_start, f_end, seg_path, math_data, chapters, cue_times, total_dur = args
    _init_worker(math_data, chapters, cue_times, total_dur)
    ff_cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-pix_fmt", "bgra", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS),
        "-i", "-",
        "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-pix_fmt", "yuv420p", "-threads", "1",
        seg_path,
    ]
    proc = subprocess.Popen(ff_cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    n_seg = f_end - f_start
    for i, fidx in enumerate(range(f_start, f_end)):
        surf = _draw_frame_into_surface(fidx)
        proc.stdin.write(surf.get_data())
        if (i + 1) % 300 == 0 or (i + 1) == n_seg:
            print(f"    [seg {seg_id}] {i + 1}/{n_seg} frames ({100.0 * (i + 1) / n_seg:.1f}%)", flush=True)
    proc.stdin.close()
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"segment {seg_id} ffmpeg failed with exit code {ret}")
    return seg_path


def strip_png_text_chunks(png_path: str):
    """Guarantee zero PNG tEXt/iTXt/zTXt chunks for Security Hygiene compliance."""
    raw = open(png_path, "rb").read()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    out = bytearray(raw[:8])
    pos = 8
    while pos + 8 <= len(raw):
        length = struct.unpack(">I", raw[pos : pos + 4])[0]
        ctype = raw[pos + 4 : pos + 8]
        chunk = raw[pos : pos + 12 + length]
        if ctype not in (b"tEXt", b"iTXt", b"zTXt"):
            out.extend(chunk)
        pos += 12 + length
    with open(png_path, "wb") as f:
        f.write(out)


def render_poster(poster_path: str, math_data: Dict[str, object], chapters, cue_times, total_dur: float):
    """Render clean 1920x1080 hero poster showing the climactic Theorem D Three-Pincer Lock."""
    _init_worker(math_data, chapters, cue_times, total_dur)
    t_hero = cue_times[19][1] - 0.5
    frame_idx = int(t_hero * FPS)
    surf = _draw_frame_into_surface(
        frame_idx,
        poster_banner="THE THREE-PINCER SYMPHONY  ·  NOVELTY 3 (THEOREM D: n ≤ 14 → n ≤ 8)  ·  4-PLANE VERIFIED  ·  github.com/Ergentics1/Morpheus",
    )
    surf.write_to_png(poster_path)
    strip_png_text_chunks(poster_path)
    print(f"  Wrote clean zero-metadata poster to {poster_path}", flush=True)


def main():
    ap = argparse.ArgumentParser(description="Render Morpheus ADPIE Cycle 5 Three-Pincer Symphony video")
    ap.add_argument("--output", default="media/gemini4_neon_cycle5_three_pincer_symphony.mp4")
    ap.add_argument("--poster", default="media/gemini4_neon_cycle5_poster.png")
    ap.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 2))
    args = ap.parse_args()

    print("=== Morpheus ADPIE Cycle 5 Video Generator (Zero Cached Data Reads) ===", flush=True)
    print("  Computing Theorem D, 19 Shimura curves (NEG-E10), P^1(F_8), & Brandt spectra from scratch...", flush=True)
    math_data = compute_cycle5_math()
    audio, chapters, cue_times = build_audio_and_timeline(math_data)
    total_dur = len(audio) / SAMPLE_RATE
    total_frames = int(math.ceil(total_dur * FPS))

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = os.path.join(tmpdir, "audio.wav")
        pcm = np.clip(audio * 32767.0, -32768, 32767).astype(np.int16)
        with wave.open(wav_path, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(pcm.tobytes())

        n_seg = max(1, args.workers)
        seg_jobs = []
        seg_paths = []
        for si in range(n_seg):
            f0 = (si * total_frames) // n_seg
            f1 = ((si + 1) * total_frames) // n_seg
            sp = os.path.join(tmpdir, f"seg_{si}.mp4")
            seg_paths.append(sp)
            seg_jobs.append((si, f0, f1, sp, math_data, chapters, cue_times, total_dur))

        print(f"  Rendering {total_frames} frames ({total_dur:.1f}s @ {FPS}fps, {n_seg} direct-FFmpeg workers) -> {args.output}", flush=True)
        mp_ctx = mp.get_context("spawn")
        with mp_ctx.Pool(processes=n_seg) as pool:
            pool.map(_render_segment, seg_jobs)

        concat_txt = os.path.join(tmpdir, "concat.txt")
        with open(concat_txt, "w", encoding="utf-8") as cf:
            for sp in seg_paths:
                cf.write(f"file '{sp}'\n")

        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        mux_cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-i", wav_path,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", "-ar", str(SAMPLE_RATE),
            "-movflags", "+faststart",
            "-map_metadata", "-1", "-fflags", "+bitexact",
            "-shortest", args.output,
        ]
        subprocess.run(mux_cmd, check=True)

    if args.poster:
        os.makedirs(os.path.dirname(args.poster) or ".", exist_ok=True)
        render_poster(args.poster, math_data, chapters, cue_times, total_dur)

    mb = os.path.getsize(args.output) / (1024 * 1024)
    print(f"=== DONE: {args.output} ({mb:.2f} MB, {total_dur:.1f}s, metadata-stripped) ===", flush=True)


if __name__ == "__main__":
    main()
