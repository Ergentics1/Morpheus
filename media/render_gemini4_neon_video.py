#!/usr/bin/env python3
"""
Morpheus — ADPIE Cycle 4 Explanatory Video Generator (Gemini 4 Neon)
License: MIT (Code Model). Rendered media assets: CC BY 4.0.

First-principles renderer: computes the 24-triad 12-EDO Tonnetz, real prime
cadences, the 8-EDO NEG-M11 octatonic counterexample, the exact 72-edge
Hashimoto transfer-matrix winding distribution at m = 40 (54,975,717,792
primes), and Theorem C's exact 2D honeycomb cumulant curves directly from
code with zero reads of cached data files. Synthesizes frame-synchronized
stereo musical audio directly from the 12-EDO and 8-EDO pitch-class sets.

Usage:
  /usr/bin/python3 media/render_gemini4_neon_video.py --keyframes-dir /tmp/kf
  /usr/bin/python3 media/render_gemini4_neon_video.py --output media/gemini4_neon_prime_cadences.mp4 --poster media/gemini4_neon_poster.png
"""

from __future__ import annotations

import argparse
import math
import multiprocessing as mp
import os
import subprocess
import tempfile
import wave
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import cairo
import gi
import numpy as np

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo  # noqa: E402

# ---------------------------------------------------------------------------
# Video configuration & Gemini 4 Neon palette
# ---------------------------------------------------------------------------

WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION_SEC = 84.0
TOTAL_FRAMES = int(round(DURATION_SEC * FPS))
SAMPLE_RATE = 48000

C_BG_DEEP = (0.024, 0.035, 0.075, 1.0)      # #060913
C_BG_MID = (0.047, 0.075, 0.149, 1.0)       # #0C1326
C_GRID = (0.110, 0.180, 0.310, 0.24)
C_PANEL = (0.055, 0.088, 0.168, 0.88)
C_PANEL_BORDER = (0.180, 0.310, 0.480, 0.48)

C_CYAN = (0.000, 0.941, 1.000, 1.0)         # #00F0FF
C_MAGENTA = (1.000, 0.180, 0.576, 1.0)      # #FF2E93
C_GOLD = (1.000, 0.722, 0.000, 1.0)         # #FFB800
C_EMERALD = (0.173, 0.961, 0.608, 1.0)      # #2CF59B
C_CORAL = (1.000, 0.420, 0.420, 1.0)        # #FF6B6B
C_WHITE = (0.945, 0.961, 1.000, 1.0)        # #F1F5FF
C_SLATE = (0.610, 0.685, 0.820, 1.0)        # #9CAFd1
C_DIM = (0.370, 0.455, 0.595, 1.0)

PITCH_NAMES_12 = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]

# ---------------------------------------------------------------------------
# Easing helpers
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


def scene_alpha(t: float, t0: float, t1: float, fade_in: float = 0.55, fade_out: float = 0.55) -> float:
    if t < t0 or t > t1:
        return 0.0
    a_in = smoothstep((t - t0) / fade_in) if fade_in > 0 else 1.0
    a_out = smoothstep((t1 - t) / fade_out) if fade_out > 0 else 1.0
    return min(a_in, a_out)


# ---------------------------------------------------------------------------
# First-principles mathematical core (zero cached data reads)
# ---------------------------------------------------------------------------

@dataclass
class MathData:
    hex_walk: List[Tuple[int, int, str, Tuple[int, int, int], int, int]]
    wind_walk: List[Tuple[int, int, str, Tuple[int, int, int], int, int]]
    neg_m11_a: List[Tuple[int, int, int]]
    neg_m11_b: List[Tuple[int, int, int]]
    neg_m11_tune: List[int]
    w_vals: np.ndarray
    p_exact: np.ndarray
    q_gauss: np.ndarray
    q_edge4: np.ndarray
    q_edge6: np.ndarray
    total_primes_40: int
    tv_gauss: float
    tv_edge4: float
    tv_edge6: float
    jsd_gauss: float
    jsd_edge4: float
    jsd_edge6: float
    m_ex_kurt_u: float
    m_ex_kurt_v: float
    m_ex_kurt_zigzag: float


def triad_pitches(mode: int, root: int) -> Tuple[int, int, int]:
    r = root % 12
    if mode == 0:
        return (r, (r + 4) % 12, (r + 7) % 12)
    return (r, (r + 3) % 12, (r + 7) % 12)


def plr_move(mode: int, root: int, op: str) -> Tuple[int, int, int]:
    r = root % 12
    if mode == 0:
        if op == "P":
            return (1, r, -1)
        if op == "L":
            return (1, (r + 4) % 12, -1)
        if op == "R":
            return (1, (r + 9) % 12, +2)
    else:
        if op == "P":
            return (0, r, +1)
        if op == "L":
            return (0, (r + 8) % 12, +1)
        if op == "R":
            return (0, (r + 3) % 12, -2)
    raise ValueError(f"Invalid op {op}")


def build_walk(
    ops: Sequence[str], start_mode: int = 0, start_root: int = 0
) -> List[Tuple[int, int, str, Tuple[int, int, int], int, int]]:
    m, r = start_mode, start_root
    cum = 0
    out: List[Tuple[int, int, str, Tuple[int, int, int], int, int]] = []
    for op in ops:
        nm, nr, delta = plr_move(m, r, op)
        cum += delta
        out.append((m, r, op, triad_pitches(m, r), delta, cum))
        m, r = nm, nr
    assert (m, r) == (start_mode, start_root)
    assert cum % 12 == 0
    return out


def mobius_mu(n: int) -> int:
    if n <= 0:
        return 0
    mu = 1
    p = 2
    x = n
    while p * p <= x:
        if x % p == 0:
            x //= p
            if x % p == 0:
                return 0
            mu = -mu
        p += 1
    if x > 1:
        mu = -mu
    return mu


def compute_exact_m40_winding() -> Tuple[np.ndarray, np.ndarray, int]:
    ops = ["P", "L", "R"]
    edges: List[Tuple[int, int, int, int]] = []
    edge_id: Dict[Tuple[int, int], int] = {}
    for mode in (0, 1):
        for root in range(12):
            u = mode * 12 + root
            for op_idx, op in enumerate(ops):
                nm, nr, delta = plr_move(mode, root, op)
                v = nm * 12 + nr
                idx = len(edges)
                edges.append((u, v, op_idx, delta))
                edge_id[(u, op_idx)] = idx

    rev = [edge_id[(v, op_idx)] for (u, v, op_idx, _d) in edges]
    nxt_edges = [
        [edge_id[(v, op2)] for op2 in range(3) if edge_id[(v, op2)] != rev[e_idx]]
        for e_idx, (u, v, op_idx, _d) in enumerate(edges)
    ]

    m_target = 40
    divisors = [d for d in range(1, m_target + 1) if m_target % d == 0]
    off = 96
    width = 2 * off + 1
    closed_by_d: Dict[int, np.ndarray] = {d: np.zeros(width, dtype=np.int64) for d in divisors}
    rep_starts = [edge_id[(0, op_i)] for op_i in range(3)] + [edge_id[(12, op_i)] for op_i in range(3)]

    for e0 in rep_starts:
        dp = np.zeros((72, width), dtype=np.int64)
        dp[e0, off + edges[e0][3]] = 1
        for step in range(2, m_target + 1):
            ndp = np.zeros((72, width), dtype=np.int64)
            for e in range(72):
                row = dp[e]
                if not np.any(row):
                    continue
                for e2 in nxt_edges[e]:
                    s = edges[e2][3]
                    if s > 0:
                        ndp[e2, s:] += row[:-s]
                    elif s < 0:
                        ndp[e2, :s] += row[-s:]
                    else:
                        ndp[e2, :] += row
            dp = ndp
            if step in closed_by_d:
                for e_last in range(72):
                    if e0 in nxt_edges[e_last]:
                        closed_by_d[step] += 12 * dp[e_last]

    for d in divisors:
        for idx in np.nonzero(closed_by_d[d])[0]:
            assert (int(idx) - off) % 12 == 0

    w_vals = np.arange(-8, 9, dtype=np.int64)
    pi_counts = np.zeros(len(w_vals), dtype=np.int64)
    for i, w in enumerate(w_vals):
        acc = 0
        for d in divisors:
            k = m_target // d
            if w % k == 0:
                s_idx = off + 12 * int(w // k)
                if 0 <= s_idx < width:
                    acc += mobius_mu(k) * int(closed_by_d[d][s_idx])
        assert acc % m_target == 0
        pi_counts[i] = acc // m_target

    total = int(np.sum(pi_counts))
    assert total == 54975717792
    return w_vals, pi_counts, total


def compute_exact_m40_other_axes() -> Tuple[float, float]:
    ops = ["P", "L", "R"]

    def axis_m_ex_kurt(step_major: Tuple[int, int, int], div_k: int) -> float:
        edges = []
        edge_id = {}
        for mode in (0, 1):
            for root in range(12):
                u = mode * 12 + root
                for op_idx, op in enumerate(ops):
                    nm, nr, _ = plr_move(mode, root, op)
                    v = nm * 12 + nr
                    s = step_major[op_idx] if mode == 0 else -step_major[op_idx]
                    idx = len(edges)
                    edges.append((u, v, op_idx, s))
                    edge_id[(u, op_idx)] = idx
        rev = [edge_id[(v, op_idx)] for (u, v, op_idx, _s) in edges]
        nxt = [
            [edge_id[(v, o2)] for o2 in range(3) if edge_id[(v, o2)] != rev[i]]
            for i, (u, v, _o, _s) in enumerate(edges)
        ]
        m_target = 40
        divisors = [d for d in range(1, m_target + 1) if m_target % d == 0]
        max_s = max(abs(x) for x in step_major) * m_target + 4
        off = max_s
        width = 2 * off + 1
        closed = {d: np.zeros(width, dtype=np.int64) for d in divisors}
        rep_starts = [edge_id[(0, o)] for o in range(3)] + [edge_id[(12, o)] for o in range(3)]
        for e0 in rep_starts:
            dp = np.zeros((72, width), dtype=np.int64)
            dp[e0, off + edges[e0][3]] = 1
            for step in range(2, m_target + 1):
                ndp = np.zeros((72, width), dtype=np.int64)
                for e in range(72):
                    row = dp[e]
                    if not np.any(row):
                        continue
                    for e2 in nxt[e]:
                        s = edges[e2][3]
                        if s > 0:
                            ndp[e2, s:] += row[:-s]
                        elif s < 0:
                            ndp[e2, :s] += row[-s:]
                        else:
                            ndp[e2, :] += row
                dp = ndp
                if step in closed:
                    for e_last in range(72):
                        if e0 in nxt[e_last]:
                            closed[step] += 12 * dp[e_last]
        pi_raw = np.zeros(width, dtype=np.int64)
        for s_val in range(-max_s + 2, max_s - 1):
            acc = 0
            for d in divisors:
                k = m_target // d
                if s_val % k == 0:
                    sub = s_val // k
                    if -off <= sub <= off:
                        acc += mobius_mu(k) * int(closed[d][off + sub])
            pi_raw[off + s_val] = acc // m_target
        tot = float(np.sum(pi_raw))
        assert int(round(tot)) == 54975717792
        xs = (np.arange(width, dtype=np.float64) - off) / float(div_k)
        p = pi_raw.astype(np.float64) / tot
        m2 = float(np.sum(p * xs * xs))
        m4 = float(np.sum(p * (xs ** 4)))
        return 40.0 * (m4 / (m2 * m2) - 3.0)

    return axis_m_ex_kurt((-1, 2, -1), 9), axis_m_ex_kurt((0, 1, -1), 1)


def compute_all_math() -> MathData:
    hex_walk = build_walk(["P", "L", "R", "P", "L", "R"], start_mode=0, start_root=0)
    wind_walk = build_walk(["R", "L", "R", "L", "R", "L", "R", "P"], start_mode=0, start_root=0)
    assert wind_walk[-1][5] == 12

    neg_m11_a = [(0, 3, 4), (0, 5, 4), (0, 7, 4), (0, 1, 4)]
    neg_m11_b = [(2, 3, 6), (2, 5, 6), (2, 7, 6), (2, 1, 6)]
    neg_m11_tune = [3, 5, 7, 1]

    w_vals, pi_counts, total = compute_exact_m40_winding()
    p = pi_counts.astype(np.float64) / float(total)

    m = 40.0
    sig = math.sqrt(m / 24.0)
    m2 = float(np.sum(p * (w_vals.astype(np.float64) ** 2)))
    m4 = float(np.sum(p * (w_vals.astype(np.float64) ** 4)))
    m_ex_kurt_u = m * (m4 / (m2 * m2) - 3.0)

    c4 = -17.0 / (48.0 * m)
    c6 = 1469.0 / (2880.0 * m * m)
    c8 = 289.0 / (4608.0 * m * m)

    def eval_order(order: int) -> Tuple[np.ndarray, float, float]:
        w_all = np.arange(-24, 25, dtype=np.float64)
        z = w_all / sig
        z2 = z * z
        base = np.exp(-0.5 * z2)
        if order == 0:
            wt = base
        else:
            h4 = z2 * z2 - 6.0 * z2 + 3.0
            poly = 1.0 + c4 * h4
            if order >= 6:
                h6 = z2 ** 3 - 15.0 * z2 ** 2 + 45.0 * z2 - 15.0
                h8 = z2 ** 4 - 28.0 * z2 ** 3 + 210.0 * z2 ** 2 - 420.0 * z2 + 105.0
                poly = poly + c6 * h6 + c8 * h8
            wt = np.maximum(0.0, base * poly)
        wt /= np.sum(wt)
        q = wt[24 - 8 : 24 + 9]
        q_out = max(0.0, 1.0 - float(np.sum(q)))
        tv = 0.5 * (q_out + float(np.sum(np.abs(p - q))))
        mid = 0.5 * (p + q)
        jsd = 0.5 * math.log(2.0) * q_out
        for i in range(len(p)):
            if p[i] > 0.0:
                jsd += 0.5 * p[i] * math.log(p[i] / mid[i])
            if q[i] > 0.0:
                jsd += 0.5 * q[i] * math.log(q[i] / mid[i])
        return q, tv, jsd

    q0, tv0, jsd0 = eval_order(0)
    q4, tv4, jsd4 = eval_order(4)
    q6, tv6, jsd6 = eval_order(6)
    mk_v, mk_zz = compute_exact_m40_other_axes()

    return MathData(
        hex_walk=hex_walk,
        wind_walk=wind_walk,
        neg_m11_a=neg_m11_a,
        neg_m11_b=neg_m11_b,
        neg_m11_tune=neg_m11_tune,
        w_vals=w_vals,
        p_exact=p,
        q_gauss=q0,
        q_edge4=q4,
        q_edge6=q6,
        total_primes_40=total,
        tv_gauss=tv0,
        tv_edge4=tv4,
        tv_edge6=tv6,
        jsd_gauss=jsd0,
        jsd_edge4=jsd4,
        jsd_edge6=jsd6,
        m_ex_kurt_u=m_ex_kurt_u,
        m_ex_kurt_v=mk_v,
        m_ex_kurt_zigzag=mk_zz,
    )


# ---------------------------------------------------------------------------
# Musical Audio Synthesis (12-EDO & 8-EDO exact tuning, stereo Rhodes + bell)
# ---------------------------------------------------------------------------

def freq_12edo(pc: int, octave: int = 4) -> float:
    midi = 12 * (octave + 1) + (pc % 12)
    return 440.0 * (2.0 ** ((midi - 69.0) / 12.0))


def freq_8edo(pc: int, octave: int = 4) -> float:
    base_c = 261.6255653 * (2.0 ** (octave - 4))
    return base_c * (2.0 ** ((pc % 8) / 8.0))


def synth_note(freq: float, dur: float, amp: float, timbre: str = "rhodes", sr: int = SAMPLE_RATE) -> np.ndarray:
    n = int(round(dur * sr))
    if n <= 0:
        return np.zeros(0, dtype=np.float64)
    t = np.arange(n, dtype=np.float64) / sr
    if timbre == "rhodes":
        env = (1.0 - np.exp(-t / 0.014)) * np.exp(-t / (dur * 0.52 + 0.15))
        tine = 0.18 * np.exp(-t / 0.06) * np.sin(2.0 * math.pi * freq * 7.0 * t)
        sig = (
            1.00 * np.sin(2.0 * math.pi * freq * t + tine)
            + 0.28 * np.sin(2.0 * math.pi * 2.0 * freq * t) * np.exp(-t / 0.45)
            + 0.10 * np.sin(2.0 * math.pi * 3.0 * freq * t) * np.exp(-t / 0.25)
            + 0.04 * np.sin(2.0 * math.pi * 4.0 * freq * t) * np.exp(-t / 0.16)
        )
    elif timbre == "bell":
        env = (1.0 - np.exp(-t / 0.005)) * np.exp(-t / (dur * 0.38 + 0.08))
        sig = (
            1.00 * np.sin(2.0 * math.pi * freq * t)
            + 0.40 * np.sin(2.0 * math.pi * 2.0 * freq * t) * np.exp(-t / 0.18)
            + 0.16 * np.sin(2.0 * math.pi * 3.0 * freq * t) * np.exp(-t / 0.10)
        )
    else:
        att = min(0.65, dur * 0.28)
        rel = min(0.80, dur * 0.32)
        env = np.minimum(1.0, t / max(att, 1e-4)) * np.minimum(1.0, (dur - t) / max(rel, 1e-4))
        env = np.maximum(0.0, env)
        det = 1.0022
        sig = (
            0.55 * np.sin(2.0 * math.pi * freq * t)
            + 0.45 * np.sin(2.0 * math.pi * freq * det * t + 0.4)
            + 0.18 * np.sin(2.0 * math.pi * 2.0 * freq * t)
            + 0.07 * np.sin(2.0 * math.pi * 3.0 * freq * t)
        )
    fade_n = min(n, int(0.015 * sr))
    if fade_n > 1:
        env[-fade_n:] *= np.linspace(1.0, 0.0, fade_n)
    return amp * env * sig


def add_stereo(buf: np.ndarray, sig: np.ndarray, start_s: float, pan: float = 0.0) -> None:
    i0 = int(round(start_s * SAMPLE_RATE))
    if i0 >= len(buf) or len(sig) == 0:
        return
    i1 = min(len(buf), i0 + len(sig))
    seg = sig[: i1 - i0]
    angle = (pan + 1.0) * (math.pi / 4.0)
    buf[i0:i1, 0] += seg * math.cos(angle)
    buf[i0:i1, 1] += seg * math.sin(angle)


def apply_reverb(buf: np.ndarray) -> np.ndarray:
    out = buf.copy()
    taps_l = [(0.031, 0.22), (0.067, 0.16), (0.113, 0.11), (0.179, 0.07), (0.263, 0.045)]
    taps_r = [(0.037, 0.22), (0.073, 0.16), (0.127, 0.11), (0.193, 0.07), (0.281, 0.045)]
    for d, g in taps_l:
        k = int(round(d * SAMPLE_RATE))
        if k < len(buf):
            out[k:, 0] += g * buf[:-k, 0]
            out[k:, 1] += 0.35 * g * buf[:-k, 0]
    for d, g in taps_r:
        k = int(round(d * SAMPLE_RATE))
        if k < len(buf):
            out[k:, 1] += g * buf[:-k, 1]
            out[k:, 0] += 0.35 * g * buf[:-k, 1]
    return out


def synthesize_soundtrack(data: MathData, wav_path: str) -> None:
    n_samples = int(round(DURATION_SEC * SAMPLE_RATE))
    buf = np.zeros((n_samples, 2), dtype=np.float64)

    # Scene 0 (0.0 - 6.0s): Luminous Cmaj9 pad + arpeggio chimes
    for pc, octv, amp, pan in [
        (0, 3, 0.14, -0.2), (7, 3, 0.11, 0.2), (4, 4, 0.10, -0.35),
        (11, 4, 0.06, 0.35), (2, 5, 0.05, 0.0),
    ]:
        add_stereo(buf, synth_note(freq_12edo(pc, octv), 6.2, amp, "pad"), 0.2, pan)
    for k, pc in enumerate([0, 4, 7, 11, 2]):
        add_stereo(buf, synth_note(freq_12edo(pc, 5 if k < 4 else 6), 1.4, 0.07, "bell"), 1.0 + 0.22 * k, -0.3 + 0.15 * k)

    # Scene 1A (6.6 - 12.6s): C-held hexagon (P-L-R-P-L-R)
    for i, (mode, _root, _op, pitches, _d, _cum) in enumerate(data.hex_walk):
        t0 = 6.6 + i * 0.90
        pan = -0.28 if mode == 0 else 0.28
        for pc in pitches:
            add_stereo(buf, synth_note(freq_12edo(pc, 4), 1.05, 0.11, "rhodes"), t0, pan * 0.7)
        nxt = data.hex_walk[(i + 1) % len(data.hex_walk)][3]
        new_p = [x for x in nxt if x not in pitches]
        if new_p:
            add_stereo(buf, synth_note(freq_12edo(new_p[0], 5), 0.75, 0.09, "bell"), t0 + 0.05, -pan)
    for pc in (0, 4, 7):
        add_stereo(buf, synth_note(freq_12edo(pc, 4), 1.2, 0.11, "rhodes"), 12.0, 0.0)

    # Scene 1B (13.1 - 18.7s): Winding W=+1 prime cadence (R-L-R-L-R-L-R-P)
    for i, (_mode, _root, _op, pitches, _d, _cum) in enumerate(data.wind_walk):
        t0 = 13.1 + i * 0.64
        pan = -0.25 + 0.50 * (i / 7.0)
        for pc in pitches:
            add_stereo(buf, synth_note(freq_12edo(pc, 4), 0.78, 0.10, "rhodes"), t0, pan * 0.6)
        add_stereo(buf, synth_note(freq_12edo(pitches[2], 5), 0.50, 0.075, "bell"), t0 + 0.02, pan)
    for pc in (0, 4, 7):
        add_stereo(buf, synth_note(freq_12edo(pc, 4), 1.3, 0.12, "rhodes"), 18.22, 0.0)

    # Scene 2A (19.0 - 24.5s): Theorem A suspended fifth
    for pc, octv, amp, pan in [(0, 3, 0.11, -0.3), (7, 3, 0.10, 0.3), (2, 4, 0.08, 0.0)]:
        add_stereo(buf, synth_note(freq_12edo(pc, octv), 5.6, amp, "pad"), 19.0, pan)
    add_stereo(buf, synth_note(freq_12edo(7, 5), 1.1, 0.08, "bell"), 21.4, -0.25)
    add_stereo(buf, synth_note(freq_12edo(0, 6), 1.1, 0.08, "bell"), 22.0, 0.25)

    # Scene 2B (25.4 - 36.2s): NEG-M11 in EXACT 8-EDO STEREO DUALITY!
    for rep in range(3):
        for step in range(4):
            t0 = 25.4 + (rep * 4 + step) * 0.90
            m_pc = data.neg_m11_tune[step]
            add_stereo(buf, synth_note(freq_8edo(0, 3), 0.98, 0.11, "rhodes"), t0, -0.68)
            add_stereo(buf, synth_note(freq_8edo(4, 3), 0.98, 0.10, "rhodes"), t0, -0.58)
            add_stereo(buf, synth_note(freq_8edo(2, 3), 0.98, 0.11, "rhodes"), t0, 0.58)
            add_stereo(buf, synth_note(freq_8edo(6, 3), 0.98, 0.10, "rhodes"), t0, 0.68)
            add_stereo(buf, synth_note(freq_8edo(m_pc, 5), 0.85, 0.15, "bell"), t0, 0.0)
            add_stereo(buf, synth_note(freq_8edo(m_pc, 4), 0.85, 0.08, "rhodes"), t0, 0.0)

    # Scene 3 (37.0 - 47.0s): Theorem B & Corollary B.1 resolution
    for pc, octv, amp, pan in [(5, 3, 0.11, -0.3), (0, 4, 0.10, 0.0), (9, 4, 0.08, 0.3)]:
        add_stereo(buf, synth_note(freq_12edo(pc, octv), 5.0, amp, "pad"), 37.0, pan)
    for pc, octv, amp, pan in [(7, 3, 0.11, -0.3), (2, 4, 0.10, 0.0), (11, 4, 0.08, 0.3)]:
        add_stereo(buf, synth_note(freq_12edo(pc, octv), 5.2, amp, "pad"), 42.0, pan)
    for k, pc in enumerate([0, 4, 7, 12]):
        add_stereo(buf, synth_note(freq_12edo(pc % 12, 5 + (pc // 12)), 1.2, 0.085, "bell"), 42.5 + 0.12 * k, -0.3 + 0.2 * k)

    # Scene 4 (47.0 - 61.0s): Theorem C honeycomb + 6 C_6 chimes
    for pc, octv, amp, pan in [(0, 3, 0.12, -0.35), (7, 3, 0.11, 0.35), (4, 4, 0.09, -0.2), (11, 4, 0.07, 0.2)]:
        add_stereo(buf, synth_note(freq_12edo(pc, octv), 14.2, amp, "pad"), 47.0, pan)
    for k, pc in enumerate([0, 2, 4, 7, 9, 11]):
        t0 = 54.0 + k * 0.62
        add_stereo(buf, synth_note(freq_12edo(pc, 5), 1.0, 0.09, "bell"), t0, 0.55 * math.sin(k * math.pi / 3.0))

    # Scene 5 (61.0 - 75.0s): Edgeworth Ladder snaps
    for pc, octv, amp, pan in [(9, 2, 0.11, -0.3), (4, 3, 0.10, 0.3), (0, 4, 0.09, 0.0), (7, 4, 0.08, 0.2)]:
        add_stereo(buf, synth_note(freq_12edo(pc, octv), 14.2, amp, "pad"), 61.0, pan)
    for t0, pcs in [(62.8, [0, 4, 7]), (66.4, [2, 6, 9, 11]), (70.0, [0, 4, 7, 11, 2])]:
        for j, pc in enumerate(pcs):
            add_stereo(buf, synth_note(freq_12edo(pc, 5), 1.4, 0.08, "bell"), t0 + 0.06 * j, -0.35 + 0.18 * j)
            add_stereo(buf, synth_note(freq_12edo(pc, 4), 1.8, 0.08, "rhodes"), t0, 0.0)

    # Scene 6 (75.0 - 84.0s): 4-language verification chimes & final Cmaj9
    for idx, (t0, pc) in enumerate([(75.8, 0), (76.7, 4), (77.6, 7), (78.5, 11)]):
        add_stereo(buf, synth_note(freq_12edo(pc, 5), 1.3, 0.10, "bell"), t0, -0.3 + 0.2 * idx)
        add_stereo(buf, synth_note(freq_12edo(pc, 4), 1.6, 0.08, "rhodes"), t0, 0.0)
    for pc, octv, amp, pan in [
        (0, 3, 0.15, -0.25), (7, 3, 0.13, 0.25), (4, 4, 0.11, -0.35),
        (11, 4, 0.09, 0.35), (2, 5, 0.08, 0.0), (0, 6, 0.05, 0.0),
    ]:
        add_stereo(buf, synth_note(freq_12edo(pc, octv), 4.6, amp, "pad"), 79.3, pan)

    buf = apply_reverb(buf)
    fade_in = int(0.4 * SAMPLE_RATE)
    fade_out = int(1.6 * SAMPLE_RATE)
    buf[:fade_in] *= np.linspace(0.0, 1.0, fade_in)[:, None]
    buf[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)[:, None]

    peak = float(np.max(np.abs(buf)))
    if peak > 1e-6:
        buf = np.tanh(buf / (peak * 0.85)) * 0.84

    pcm = np.clip(buf * 32767.0, -32768.0, 32767.0).astype("<i2")
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm.tobytes())


# ---------------------------------------------------------------------------
# Cairo + Pango Drawing Primitives (Clean sub-paths & cached backdrop!)
# ---------------------------------------------------------------------------

def set_rgba(ctx: cairo.Context, col: Tuple[float, float, float, float], alpha_mul: float = 1.0) -> None:
    ctx.set_source_rgba(col[0], col[1], col[2], col[3] * alpha_mul)


def rounded_rect(ctx: cairo.Context, x: float, y: float, w: float, h: float, r: float) -> None:
    r = min(r, 0.5 * w, 0.5 * h)
    ctx.new_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def draw_panel(
    ctx: cairo.Context,
    x: float,
    y: float,
    w: float,
    h: float,
    alpha: float = 1.0,
    border_col: Tuple[float, float, float, float] = C_PANEL_BORDER,
    radius: float = 18.0,
    fill_col: Tuple[float, float, float, float] = C_PANEL,
    border_width: float = 1.8,
) -> None:
    rounded_rect(ctx, x, y, w, h, radius)
    set_rgba(ctx, fill_col, alpha)
    ctx.fill_preserve()
    set_rgba(ctx, border_col, alpha)
    ctx.set_line_width(border_width)
    ctx.stroke()


def draw_text(
    ctx: cairo.Context,
    markup: str,
    x: float,
    y: float,
    font_desc: str = "DejaVu Sans 22",
    color: Tuple[float, float, float, float] = C_WHITE,
    alpha: float = 1.0,
    align: str = "left",
    valign: str = "top",
    max_width: float | None = None,
    line_spacing: float = 1.24,
) -> Tuple[float, float]:
    layout = PangoCairo.create_layout(ctx)
    layout.set_font_description(Pango.FontDescription(font_desc))
    layout.set_markup(markup, -1)
    if max_width is not None:
        layout.set_width(int(max_width * Pango.SCALE))
        layout.set_wrap(Pango.WrapMode.WORD_CHAR)
    if align == "center":
        layout.set_alignment(Pango.Alignment.CENTER)
    elif align == "right":
        layout.set_alignment(Pango.Alignment.RIGHT)
    else:
        layout.set_alignment(Pango.Alignment.LEFT)
    layout.set_line_spacing(line_spacing)

    _, logical = layout.get_pixel_extents()
    tw, th = float(logical.width), float(logical.height)

    dx = x
    if max_width is not None:
        if align == "center":
            dx = x - max_width * 0.5
        elif align == "right":
            dx = x - max_width
    else:
        if align == "center":
            dx = x - tw * 0.5
        elif align == "right":
            dx = x - tw

    dy = y
    if valign == "center":
        dy = y - th * 0.5
    elif valign == "bottom":
        dy = y - th

    ctx.save()
    ctx.new_path()
    ctx.move_to(dx, dy)
    set_rgba(ctx, color, alpha)
    PangoCairo.show_layout(ctx, layout)
    ctx.restore()
    return tw, th


def draw_pill(
    ctx: cairo.Context,
    text: str,
    x: float,
    y: float,
    accent: Tuple[float, float, float, float],
    alpha: float = 1.0,
    align: str = "left",
    font: str = "DejaVu Sans Bold 13",
) -> float:
    layout = PangoCairo.create_layout(ctx)
    layout.set_font_description(Pango.FontDescription(font))
    layout.set_markup(text, -1)
    _, logical = layout.get_pixel_extents()
    pw = logical.width + 32.0
    ph = logical.height + 14.0
    px = x if align == "left" else (x - pw * 0.5 if align == "center" else x - pw)
    py = y
    rounded_rect(ctx, px, py, pw, ph, ph * 0.5)
    ctx.set_source_rgba(accent[0], accent[1], accent[2], 0.16 * alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(accent[0], accent[1], accent[2], 0.85 * alpha)
    ctx.set_line_width(1.6)
    ctx.stroke()
    draw_text(ctx, text, px + pw * 0.5, py + ph * 0.5, font, accent, alpha, "center", "center")
    return pw


def draw_glow_line(
    ctx: cairo.Context,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    col: Tuple[float, float, float, float],
    width: float = 4.0,
    alpha: float = 1.0,
) -> None:
    ctx.save()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for mult, a in [(3.4, 0.13), (1.9, 0.28), (1.0, 0.96)]:
        ctx.new_path()
        ctx.move_to(x0, y0)
        ctx.line_to(x1, y1)
        set_rgba(ctx, col, alpha * a)
        ctx.set_line_width(width * mult)
        ctx.stroke()
    ctx.restore()


def draw_glow_circle(
    ctx: cairo.Context,
    cx: float,
    cy: float,
    r: float,
    col: Tuple[float, float, float, float],
    alpha: float = 1.0,
    fill_core: bool = True,
) -> None:
    if r <= 0.1 or alpha <= 0.0:
        return
    pat = cairo.RadialGradient(cx, cy, 0.0, cx, cy, r * 2.8)
    pat.add_color_stop_rgba(0.0, col[0], col[1], col[2], 0.65 * alpha)
    pat.add_color_stop_rgba(0.38, col[0], col[1], col[2], 0.22 * alpha)
    pat.add_color_stop_rgba(1.0, col[0], col[1], col[2], 0.0)
    ctx.new_path()
    ctx.set_source(pat)
    ctx.arc(cx, cy, r * 2.8, 0, 2 * math.pi)
    ctx.fill()
    if fill_core:
        ctx.new_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        set_rgba(ctx, col, alpha)
        ctx.fill()


def build_static_bg_surface() -> cairo.ImageSurface:
    """Pre-render static obsidian radial backdrop + honeycomb mesh once per worker."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)

    pat = cairo.RadialGradient(WIDTH * 0.5, HEIGHT * 0.44, 60.0, WIDTH * 0.5, HEIGHT * 0.5, WIDTH * 0.72)
    pat.add_color_stop_rgba(0.0, C_BG_MID[0], C_BG_MID[1], C_BG_MID[2], 1.0)
    pat.add_color_stop_rgba(1.0, C_BG_DEEP[0], C_BG_DEEP[1], C_BG_DEEP[2], 1.0)
    ctx.set_source(pat)
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.fill()

    set_rgba(ctx, C_GRID, 0.52)
    ctx.set_line_width(1.0)
    R = 74.0
    dx = R * 1.5
    dy = R * math.sqrt(3.0)
    for col_i in range(-1, int(WIDTH / dx) + 2):
        for row_i in range(-1, int(HEIGHT / dy) + 2):
            cx = col_i * dx
            cy = row_i * dy + (0.5 * dy if col_i % 2 else 0.0)
            ctx.new_sub_path()
            for k in range(6):
                a0 = k * math.pi / 3.0
                px = cx + R * math.cos(a0)
                py = cy + R * math.sin(a0)
                if k == 0:
                    ctx.move_to(px, py)
                else:
                    ctx.line_to(px, py)
            ctx.close_path()
    ctx.stroke()
    return surf


_BG_CACHE: cairo.ImageSurface | None = None


def draw_background(ctx: cairo.Context, t: float, show_timeline: bool = True) -> None:
    global _BG_CACHE
    if _BG_CACHE is None:
        _BG_CACHE = build_static_bg_surface()
    ctx.set_source_surface(_BG_CACHE, 0, 0)
    ctx.paint()

    if not show_timeline:
        return

    bar_y = HEIGHT - 34.0
    ctx.new_path()
    ctx.set_source_rgba(0.18, 0.28, 0.44, 0.35)
    ctx.rectangle(72.0, bar_y, WIDTH - 144.0, 3.0)
    ctx.fill()
    prog = clamp01(t / DURATION_SEC)
    grad = cairo.LinearGradient(72.0, 0, WIDTH - 72.0, 0)
    grad.add_color_stop_rgba(0.0, C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.92)
    grad.add_color_stop_rgba(0.5, C_MAGENTA[0], C_MAGENTA[1], C_MAGENTA[2], 0.92)
    grad.add_color_stop_rgba(1.0, C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.96)
    ctx.new_path()
    ctx.set_source(grad)
    ctx.rectangle(72.0, bar_y, (WIDTH - 144.0) * prog, 3.0)
    ctx.fill()

    draw_text(ctx, "ERGENTICS  ·  MORPHEUS  ·  GEMINI 4 NEON", 72.0, HEIGHT - 23.0, "DejaVu Sans Mono 11", C_DIM, 0.92)
    mm, ss = int(t // 60), int(t % 60)
    draw_text(ctx, f"{mm:02d}:{ss:02d} / 01:24", WIDTH - 72.0, HEIGHT - 23.0, "DejaVu Sans Mono 11", C_DIM, 0.92, "right")


# ---------------------------------------------------------------------------
# Scene 0 (0.0 - 6.0s): Opening Title Card
# ---------------------------------------------------------------------------

def render_scene_0(ctx: cairo.Context, t: float) -> None:
    a = scene_alpha(t, 0.0, 6.2, fade_in=0.7, fade_out=0.7)
    if a <= 0.0:
        return

    cx, cy = WIDTH * 0.5, HEIGHT * 0.48
    p_rot = t * 0.14
    for ring_i, (rad, col, lw) in enumerate([(310, C_CYAN, 2.2), (355, C_MAGENTA, 1.4), (400, C_GOLD, 1.0)]):
        s_dir = 1 if ring_i % 2 == 0 else -1
        pts = [
            (cx + rad * math.cos(p_rot * s_dir + k * math.pi / 3.0),
             cy + rad * math.sin(p_rot * s_dir + k * math.pi / 3.0))
            for k in range(6)
        ]
        for k in range(6):
            p0, p1 = pts[k], pts[(k + 1) % 6]
            draw_glow_line(ctx, p0[0], p0[1], p1[0], p1[1], col, lw, a * 0.50)
            if ring_i == 0:
                draw_glow_circle(ctx, p0[0], p0[1], 5.0, C_CYAN if k % 2 == 0 else C_MAGENTA, a * 0.85)

    p0 = ease_out_cubic(seg_prog(t, 0.25, 1.15))
    draw_pill(ctx, "ERGENTICS  ·  MORPHEUS  ·  ADPIE CYCLE 4", cx, 210.0 + 18.0 * (1 - p0), C_CYAN, a * p0, "center", "DejaVu Sans Bold 14")

    p1 = ease_out_cubic(seg_prog(t, 0.65, 1.65))
    draw_text(ctx, "<b>PRIME CADENCES</b>", cx, 360.0 + 20.0 * (1 - p1), "DejaVu Sans 80", C_WHITE, a * p1, "center", "center")

    p2 = ease_out_cubic(seg_prog(t, 1.25, 2.25))
    draw_text(
        ctx,
        "Two Original Proofs, One Counterexample, and a 75× Precision Leap",
        cx,
        462.0 + 14.0 * (1 - p2),
        "DejaVu Serif 28",
        C_GOLD,
        a * p2,
        "center",
        "center",
    )

    w_bar = 680.0 * ease_out_cubic(seg_prog(t, 1.75, 2.75))
    if w_bar > 2.0:
        draw_glow_line(ctx, cx - w_bar * 0.5, 530.0, cx + w_bar * 0.5, 530.0, C_CYAN, 2.4, a * 0.85)

    p3 = ease_out_cubic(seg_prog(t, 2.15, 3.15))
    draw_text(
        ctx,
        "<span foreground='#00F0FF'><b>Open Problem (3)</b></span> resolved ∀<i>N</i> ≥ 5   ·   "
        "<span foreground='#FF2E93'><b>NEG-M11</b></span> 8-EDO counterexample   ·   "
        "<span foreground='#FFB800'><b>Theorem C</b></span> 6th-order <i>C</i><sub>6</sub> cumulants",
        cx,
        595.0,
        "DejaVu Sans 18",
        C_SLATE,
        a * p3,
        "center",
        "center",
        max_width=1720.0,
    )

    p4 = ease_out_cubic(seg_prog(t, 2.8, 3.8))
    draw_text(
        ctx,
        "Audit-Forward Contribution by <b>Gemini 4 Neon</b>  ·  4-Language Machine-Checked  ·  For Grok Bot Reconciliation",
        cx,
        755.0,
        "DejaVu Sans Mono 15",
        C_EMERALD,
        a * p4 * 0.94,
        "center",
        "center",
    )


# ---------------------------------------------------------------------------
# Scene 1 (6.0 - 19.0s): The Musical Graph — 12-EDO Tonnetz & Prime Cadences
# ---------------------------------------------------------------------------

def render_scene_1(ctx: cairo.Context, t: float, data: MathData) -> None:
    a = scene_alpha(t, 5.8, 19.2, fade_in=0.65, fade_out=0.65)
    if a <= 0.0:
        return

    draw_pill(ctx, "ACT 1  ·  THE 12-EDO TONNETZ HONEYCOMB", 80.0, 50.0, C_CYAN, a, "left")
    draw_text(ctx, "<b>Neo-Riemannian Prime Cadences</b>", 80.0, 102.0, "DejaVu Sans 38", C_WHITE, a)

    draw_panel(ctx, 80.0, 178.0, 1040.0, 818.0, a, C_PANEL_BORDER, 22.0)

    ox, oy = 600.0, 608.0
    step_L = 138.0
    e1 = (step_L, 0.0)
    e2 = (step_L * 0.5, -step_L * math.sqrt(3.0) / 2.0)

    in_wind = t >= 12.8
    cam_shift_p = ease_in_out_cubic(seg_prog(t, 12.6, 13.6))
    cam_dx = 225.0 * cam_shift_p
    cam_dy = 45.0 * cam_shift_p

    def p_xy(i: float, j: float) -> Tuple[float, float]:
        return (ox + i * e1[0] + j * e2[0] + cam_dx, oy + i * e1[1] + j * e2[1] + cam_dy)

    def tri_centroid(verts: Sequence[Tuple[int, int]]) -> Tuple[float, float]:
        pts = [p_xy(u, v) for u, v in verts]
        return (sum(p[0] for p in pts) / 3.0, sum(p[1] for p in pts) / 3.0)

    ctx.save()
    rounded_rect(ctx, 84.0, 182.0, 1032.0, 810.0, 20.0)
    ctx.clip()

    # Triangular pitch lattice (using exact shifted coordinates!)
    ctx.new_path()
    ctx.set_line_width(1.3)
    set_rgba(ctx, (0.24, 0.36, 0.56, 0.42), a)
    for i in range(-6, 5):
        ctx.move_to(*p_xy(i, -4))
        ctx.line_to(*p_xy(i, 5))
    for j in range(-4, 6):
        ctx.move_to(*p_xy(-6, j))
        ctx.line_to(*p_xy(5, j))
    for s in range(-8, 8):
        ctx.move_to(*p_xy(-6, s + 6))
        ctx.line_to(*p_xy(5, s - 5))
    ctx.stroke()

    c_hex_tris = [
        ("C",  0, [(0, 0), (1, 0), (0, 1)]),
        ("Cm", 1, [(0, 0), (1, 0), (1, -1)]),
        ("A♭", 0, [(0, 0), (1, -1), (0, -1)]),
        ("Fm", 1, [(0, 0), (0, -1), (-1, 0)]),
        ("F",  0, [(0, 0), (-1, 0), (-1, 1)]),
        ("Am", 1, [(0, 0), (-1, 1), (0, 1)]),
    ]
    wind_tris = [
        ("C",  0, [(0, 0), (1, 0), (0, 1)]),
        ("Am", 1, [(0, 0), (0, 1), (-1, 1)]),
        ("F",  0, [(0, 0), (-1, 1), (-1, 0)]),
        ("Dm", 1, [(-1, 1), (-1, 0), (-2, 1)]),
        ("B♭", 0, [(-1, 0), (-2, 1), (-2, 0)]),
        ("Gm", 1, [(-2, 1), (-2, 0), (-3, 1)]),
        ("E♭", 0, [(-2, 0), (-3, 1), (-3, 0)]),
        ("Cm", 1, [(-3, 1), (-3, 0), (-4, 1)]),
        ("C'", 0, [(-3, 1), (-4, 1), (-4, 2)]),
    ]

    active_tris = wind_tris if in_wind else c_hex_tris
    if not in_wind:
        step_f = clamp01((t - 6.6) / 5.4) * 6.0
        cur_idx = min(5, int(step_f))
    else:
        step_f = clamp01((t - 13.1) / 5.12) * 8.0
        cur_idx = min(8, int(step_f))

    centroids = [tri_centroid(tr[2]) for tr in active_tris]
    for idx, (lbl, mode, verts) in enumerate(active_tris):
        if idx > cur_idx:
            continue
        col = C_CYAN if mode == 0 else C_MAGENTA
        is_curr = (idx == cur_idx)
        pts = [p_xy(u, v) for u, v in verts]
        ctx.new_path()
        ctx.move_to(*pts[0])
        ctx.line_to(*pts[1])
        ctx.line_to(*pts[2])
        ctx.close_path()
        set_rgba(ctx, col, (0.34 if is_curr else 0.16) * a)
        ctx.fill_preserve()
        set_rgba(ctx, col, (0.95 if is_curr else 0.55) * a)
        ctx.set_line_width(3.0 if is_curr else 1.8)
        ctx.stroke()
        draw_text(ctx, f"<b>{lbl}</b>", centroids[idx][0], centroids[idx][1], "DejaVu Sans 17", C_WHITE if is_curr else col, a, "center", "center")

    max_seg = min(len(centroids) - 1 if in_wind else len(centroids), int(step_f))
    for k in range(max_seg):
        c0 = centroids[k]
        c1 = centroids[(k + 1) % len(centroids)] if not in_wind else centroids[k + 1]
        draw_glow_line(ctx, c0[0], c0[1], c1[0], c1[1], C_GOLD, 4.2, a * 0.95)
    frac = step_f - math.floor(step_f)
    if (not in_wind and max_seg < 6) or (in_wind and max_seg < 8):
        c0 = centroids[max_seg]
        c1 = centroids[(max_seg + 1) % len(centroids)] if not in_wind else centroids[max_seg + 1]
        draw_glow_line(ctx, c0[0], c0[1], c0[0] + (c1[0] - c0[0]) * frac, c0[1] + (c1[1] - c0[1]) * frac, C_GOLD, 4.6, a)

    # Pitch-class nodes (clean new_path() for every circle -> ZERO stray lines!)
    for i in range(-5, 4):
        for j in range(-2, 4):
            px, py = p_xy(i, j)
            if px < 105 or px > 1095 or py < 200 or py > 975:
                continue
            pc = (7 * i + 4 * j) % 12
            is_c_hub = (not in_wind and i == 0 and j == 0)
            if is_c_hub:
                draw_glow_circle(ctx, px, py, 20.0, C_GOLD, a, fill_core=True)
                draw_text(ctx, "<b>C</b>", px, py, "DejaVu Sans 15", C_BG_DEEP, a, "center", "center")
            else:
                ctx.new_path()
                ctx.arc(px, py, 15.0, 0, 2 * math.pi)
                set_rgba(ctx, (0.065, 0.105, 0.20, 0.96), a)
                ctx.fill_preserve()
                set_rgba(ctx, (0.36, 0.52, 0.74, 0.85), a)
                ctx.set_line_width(1.6)
                ctx.stroke()
                draw_text(ctx, PITCH_NAMES_12[pc], px, py, "DejaVu Sans 11", C_WHITE, a * 0.92, "center", "center")

    ctx.restore()

    # Right explanation & telemetry panels (generous spacing, zero overlap!)
    rx, rw = 1156.0, 684.0
    draw_panel(ctx, rx, 178.0, rw, 535.0, a, C_PANEL_BORDER, 22.0)

    mode_tag = "WINDING LOOP  (W = +1)" if in_wind else "HELD-NOTE HEXAGON  (W = 0)"
    draw_pill(ctx, mode_tag, rx + 32.0, 210.0, C_GOLD if in_wind else C_CYAN, a, "left", "DejaVu Sans Bold 13")

    body1 = (
        "Each neo-Riemannian move <span foreground='#00F0FF'><b>P</b></span>, "
        "<span foreground='#FF2E93'><b>L</b></span>, "
        "<span foreground='#FFB800'><b>R</b></span> shifts <b>one voice</b> "
        "by 1 or 2 semitones on the 24-triad honeycomb graph <i>X</i>."
    )
    draw_text(ctx, body1, rx + 32.0, 270.0, "DejaVu Sans 19", C_WHITE, a, max_width=rw - 64.0, line_spacing=1.34)

    body2 = (
        "A <b>prime cadence</b> is a non-backtracking primitive loop — "
        "an <i>Ihara zeta prime</i>. By Theorem 5.1, every closed loop has "
        "total voice sum divisible by <b>12</b>, defining its integer winding <i>W</i>."
    )
    draw_text(ctx, body2, rx + 32.0, 396.0, "DejaVu Sans 18", C_SLATE, a, max_width=rw - 64.0, line_spacing=1.34)

    # Clean divider above legend
    ctx.new_path()
    ctx.move_to(rx + 32.0, 560.0)
    ctx.line_to(rx + rw - 32.0, 560.0)
    set_rgba(ctx, C_PANEL_BORDER, a * 0.65)
    ctx.set_line_width(1.2)
    ctx.stroke()

    draw_glow_circle(ctx, rx + 46.0, 602.0, 7.5, C_CYAN, a)
    draw_text(ctx, "Major triad (12)", rx + 68.0, 602.0, "DejaVu Sans 16", C_WHITE, a, valign="center")
    draw_glow_circle(ctx, rx + 340.0, 602.0, 7.5, C_MAGENTA, a)
    draw_text(ctx, "Minor triad (12)", rx + 362.0, 602.0, "DejaVu Sans 16", C_WHITE, a, valign="center")
    draw_glow_circle(ctx, rx + 46.0, 650.0, 7.5, C_GOLD, a)
    draw_text(ctx, "Prime cadence path (3-regular honeycomb)", rx + 68.0, 650.0, "DejaVu Sans 16", C_GOLD, a, valign="center")

    # Bottom right telemetry card
    draw_panel(ctx, rx, 738.0, rw, 258.0, a, C_GOLD if in_wind else C_CYAN, 22.0)
    if not in_wind:
        ops_str = "P  →  L  →  R  →  P  →  L  →  R"
        cum_str = "Δ = 0 semitones   ⇒   W = 0"
        note_str = "Every triad holds pitch C = 0 (face of honeycomb)"
    else:
        deltas = [0, 2, 3, 5, 6, 8, 9, 11, 12]
        cur_d = deltas[min(cur_idx, 8)]
        ops_str = "R → L → R → L → R → L → R → P"
        cum_str = f"Δ = +{cur_d} semitones   ⇒   W = {'+1' if cur_d == 12 else f'+{cur_d}/12'}"
        note_str = "Lifts by (−4, +1) on the universal Tonnetz cover!"
    draw_text(ctx, "LIVE CADENCE TELEMETRY", rx + 32.0, 766.0, "DejaVu Sans Mono 13", C_SLATE, a)
    draw_text(ctx, f"<b>{ops_str}</b>", rx + 32.0, 810.0, "DejaVu Sans Mono 19", C_WHITE, a)
    draw_text(ctx, f"<b>{cum_str}</b>", rx + 32.0, 866.0, "DejaVu Sans Mono 19", C_GOLD if in_wind else C_CYAN, a)
    draw_text(ctx, note_str, rx + 32.0, 926.0, "DejaVu Sans 16", C_SLATE, a)


# ---------------------------------------------------------------------------
# Scene 2 (19.0 - 37.0s): Novelty 1A — Theorem A & NEG-M11 in 8-EDO
# ---------------------------------------------------------------------------

def draw_8edo_clock(
    ctx: cairo.Context,
    cx: float,
    cy: float,
    radius: float,
    held_pair: Tuple[int, int],
    moving_pc: int,
    trail_pcs: Sequence[int],
    accent: Tuple[float, float, float, float],
    title: str,
    subtitle: str,
    alpha: float,
) -> None:
    ctx.new_path()
    ctx.arc(cx, cy, radius, 0, 2 * math.pi)
    set_rgba(ctx, (0.16, 0.25, 0.42, 0.78), alpha)
    ctx.set_line_width(2.2)
    ctx.stroke()

    def pc_pos(pc: int) -> Tuple[float, float]:
        ang = -math.pi / 2.0 + (pc % 8) * (2.0 * math.pi / 8.0)
        return (cx + radius * math.cos(ang), cy + radius * math.sin(ang))

    h0, h1 = pc_pos(held_pair[0]), pc_pos(held_pair[1])
    draw_glow_line(ctx, h0[0], h0[1], h1[0], h1[1], accent, 4.2, alpha * 0.9)

    mp_pos = pc_pos(moving_pc)
    ctx.new_path()
    ctx.move_to(*h0)
    ctx.line_to(*h1)
    ctx.line_to(*mp_pos)
    ctx.close_path()
    set_rgba(ctx, accent, 0.24 * alpha)
    ctx.fill_preserve()
    set_rgba(ctx, accent, 0.95 * alpha)
    ctx.set_line_width(3.0)
    ctx.stroke()

    for k in range(len(trail_pcs) - 1):
        p0, p1 = pc_pos(trail_pcs[k]), pc_pos(trail_pcs[k + 1])
        draw_glow_line(ctx, p0[0], p0[1], p1[0], p1[1], C_GOLD, 2.8, alpha * 0.85)

    for pc in range(8):
        px, py = pc_pos(pc)
        if pc == moving_pc:
            draw_glow_circle(ctx, px, py, 19.0, C_GOLD, alpha)
            draw_text(ctx, f"<b>{pc}</b>", px, py, "DejaVu Sans Mono 16", C_BG_DEEP, alpha, "center", "center")
        elif pc in held_pair:
            draw_glow_circle(ctx, px, py, 18.0, accent, alpha)
            draw_text(ctx, f"<b>{pc}</b>", px, py, "DejaVu Sans Mono 16", C_BG_DEEP, alpha, "center", "center")
        else:
            ctx.new_path()
            ctx.arc(px, py, 15.0, 0, 2 * math.pi)
            set_rgba(ctx, (0.07, 0.11, 0.20, 0.96), alpha)
            ctx.fill_preserve()
            set_rgba(ctx, (0.30, 0.42, 0.62, 0.78), alpha)
            ctx.set_line_width(1.6)
            ctx.stroke()
            draw_text(ctx, f"{pc}", px, py, "DejaVu Sans Mono 14", C_SLATE, alpha, "center", "center")

    chord_sorted = sorted([held_pair[0], held_pair[1], moving_pc])
    draw_text(ctx, title, cx, cy - radius - 82.0, "DejaVu Sans Bold 20", accent, alpha, "center", "center")
    draw_text(ctx, subtitle, cx, cy - radius - 48.0, "DejaVu Sans Mono 14", C_SLATE, alpha, "center", "center")
    draw_text(
        ctx,
        f"Chord: <b>{{{chord_sorted[0]}, {chord_sorted[1]}, {chord_sorted[2]}}}</b>",
        cx,
        cy + radius + 54.0,
        "DejaVu Sans Mono 19",
        C_WHITE,
        alpha,
        "center",
        "center",
    )


def render_scene_2(ctx: cairo.Context, t: float, data: MathData) -> None:
    a = scene_alpha(t, 18.8, 37.2, fade_in=0.6, fade_out=0.6)
    if a <= 0.0:
        return

    # Sub-scene 2A (19.0 - 24.5s): Theorem A
    a_2a = scene_alpha(t, 18.8, 24.8, fade_in=0.55, fade_out=0.65)
    if a_2a > 0.0:
        draw_pill(ctx, "NOVELTY 1  ·  OPEN PROBLEM (3)", 80.0, 50.0, C_CYAN, a_2a)
        draw_text(ctx, "<b>Does the Melody Always Identify the Chord Loop?</b>", 80.0, 102.0, "DejaVu Sans 38", C_WHITE, a_2a)

        draw_panel(ctx, 80.0, 186.0, 1760.0, 780.0, a_2a, C_PANEL_BORDER, 24.0)

        vx, vy = 540.0, 565.0
        sep, rad = 162.0, 210.0
        for sx, col, lbl in [(-sep, C_CYAN, "<i>L</i><sub><i>h</i>₁</sub>"), (sep, C_MAGENTA, "<i>L</i><sub><i>h</i>₂</sub>")]:
            ctx.new_path()
            ctx.arc(vx + sx, vy, rad, 0, 2 * math.pi)
            set_rgba(ctx, col, 0.13 * a_2a)
            ctx.fill_preserve()
            set_rgba(ctx, col, 0.90 * a_2a)
            ctx.set_line_width(3.0)
            ctx.stroke()
            draw_text(ctx, f"<b>{lbl}</b>", vx + sx * 1.45, vy - 180.0, "DejaVu Serif 28", col, a_2a, "center", "center")

        p_int = ease_out_cubic(seg_prog(t, 20.2, 21.8))
        for dy in (-64.0, 64.0):
            draw_glow_circle(ctx, vx, vy + dy, 15.0 * p_int, C_GOLD, a_2a * p_int)
        draw_text(ctx, "<b>≤ 2</b>", vx, vy, "DejaVu Sans Mono Bold 28", C_WHITE, a_2a * p_int, "center", "center")
        draw_text(
            ctx,
            "At most 2 chords share both held notes <i>h</i>₁ ≠ <i>h</i>₂",
            vx,
            845.0,
            "DejaVu Sans 18",
            C_SLATE,
            a_2a,
            "center",
            "center",
        )

        tx = 995.0
        draw_pill(ctx, "THEOREM A  ·  UNIVERSAL ABELIAN BOUND", tx, 248.0, C_EMERALD, a_2a)
        draw_text(ctx, "<b>|<i>L</i><sub><i>h</i>₁</sub> ∩ <i>L</i><sub><i>h</i>₂</sub>|  ≤  2</b>", tx, 316.0, "DejaVu Serif 46", C_EMERALD, a_2a)
        draw_text(
            ctx,
            "Holds for <b>ALL</b> <i>N</i> ≥ 3, every 3-note chord <i>c</i>₀, and every step set <i>S</i>.",
            tx,
            422.0,
            "DejaVu Sans 20",
            C_WHITE,
            a_2a,
            max_width=780.0,
            line_spacing=1.34,
        )
        draw_text(
            ctx,
            "• Permanently eliminates <b>ALL</b> 2-moving-voice held-note collisions.\n"
            "• Leaves only <b>1-moving-voice</b> cycles (2 pitches held fixed).\n"
            "• Proved universally in Lean 4 (<tt>thmA_link_intersection_le_two</tt>).",
            tx,
            524.0,
            "DejaVu Sans 18",
            C_SLATE,
            a_2a,
            max_width=780.0,
            line_spacing=1.45,
        )
        p_hook = ease_out_cubic(seg_prog(t, 22.3, 23.4))
        draw_panel(ctx, tx, 748.0, 775.0, 126.0, a_2a * p_hook, C_MAGENTA, 16.0, border_width=2.0)
        draw_text(
            ctx,
            "<b>Wait — what about 1-moving-voice cycles for arbitrary step sets <i>S</i>?</b>",
            tx + 26.0,
            780.0,
            "DejaVu Sans 20",
            C_MAGENTA,
            a_2a * p_hook,
            max_width=720.0,
            line_spacing=1.28,
        )

    # Sub-scene 2B (24.5 - 37.0s): NEG-M11 in 8-EDO
    a_2b = scene_alpha(t, 24.4, 37.2, fade_in=0.6, fade_out=0.6)
    if a_2b > 0.0:
        draw_pill(ctx, "PLOT TWIST  ·  COUNTEREXAMPLE NEG-M11", 80.0, 50.0, C_MAGENTA, a_2b)
        draw_text(ctx, "<b>Two Disjoint 8-EDO Chord Loops. One Identical Melody.</b>", 80.0, 102.0, "DejaVu Sans 36", C_WHITE, a_2b)

        beat_f = max(0.0, (t - 25.4) / 0.90)
        beat_i = int(beat_f)
        step = beat_i % 4
        m_pc = data.neg_m11_tune[step]
        trail = [data.neg_m11_tune[k % 4] for k in range(max(1, min(5, beat_i + 1)))]
        if beat_i >= 4:
            trail = [3, 5, 7, 1, 3]

        draw_panel(ctx, 80.0, 180.0, 580.0, 695.0, a_2b, C_CYAN, 22.0)
        draw_8edo_clock(ctx, 370.0, 534.0, 190.0, (0, 4), m_pc, trail, C_CYAN, "ORBIT A  (LEFT STEREO)", "Holds tritone {0, 4} in Z₈", a_2b)

        draw_panel(ctx, 1260.0, 180.0, 580.0, 695.0, a_2b, C_MAGENTA, 22.0)
        draw_8edo_clock(ctx, 1550.0, 534.0, 190.0, (2, 6), m_pc, trail, C_MAGENTA, "ORBIT B  (RIGHT STEREO)", "Holds tritone {2, 6} in Z₈", a_2b)

        draw_panel(ctx, 695.0, 180.0, 530.0, 695.0, a_2b, C_GOLD, 22.0)
        cx_m = 960.0
        draw_pill(ctx, "SHARED UNISON TUNE", cx_m, 214.0, C_GOLD, a_2b, "center", "DejaVu Sans Bold 13")
        draw_text(
            ctx,
            "<b><i>N</i> = 8  ·  <i>S</i> = {2}  ·  <i>c</i>₀ = {0, 1, 4}</b>",
            cx_m,
            286.0,
            "DejaVu Sans Mono 17",
            C_WHITE,
            a_2b,
            "center",
            "center",
        )
        draw_text(ctx, "Orbit <i>T/I</i>({0, 1, 4})  (16 chords)", cx_m, 326.0, "DejaVu Sans 16", C_SLATE, a_2b, "center", "center")

        pill_xs = [782.0, 900.0, 1020.0, 1138.0]
        pill_y = 468.0
        for idx_p in range(3):
            draw_glow_line(ctx, pill_xs[idx_p] + 30, pill_y, pill_xs[idx_p + 1] - 30, pill_y, C_GOLD, 2.8, a_2b * 0.65)
        for idx_p in range(4):
            pc_v = data.neg_m11_tune[idx_p]
            active = (idx_p == step and t >= 25.35)
            r_p = 34.0 if active else 26.0
            if active:
                draw_glow_circle(ctx, pill_xs[idx_p], pill_y, r_p, C_GOLD, a_2b)
                draw_text(ctx, f"<b>{pc_v}</b>", pill_xs[idx_p], pill_y, "DejaVu Sans Mono 24", C_BG_DEEP, a_2b, "center", "center")
            else:
                ctx.new_path()
                ctx.arc(pill_xs[idx_p], pill_y, r_p, 0, 2 * math.pi)
                set_rgba(ctx, (0.09, 0.13, 0.22, 0.96), a_2b)
                ctx.fill_preserve()
                set_rgba(ctx, C_GOLD, 0.68 * a_2b)
                ctx.set_line_width(2.0)
                ctx.stroke()
                draw_text(ctx, f"{pc_v}", pill_xs[idx_p], pill_y, "DejaVu Sans Mono 20", C_GOLD, a_2b, "center", "center")

        draw_text(ctx, "Cyclic moving-voice melody: <b>(3, 5, 7, 1)</b>", cx_m, 554.0, "DejaVu Sans 17", C_GOLD, a_2b, "center", "center")
        draw_text(
            ctx,
            "Vertex intersection:\n<b>Orbit A ∩ Orbit B = ∅</b>",
            cx_m,
            664.0,
            "DejaVu Sans 20",
            C_WHITE,
            a_2b,
            "center",
            "center",
            line_spacing=1.35,
        )
        draw_text(
            ctx,
            "Refutes the unrestricted general-<i>S</i>\nconjecture! (Logged as <b>NEG-M11</b>)",
            cx_m,
            786.0,
            "DejaVu Sans 16",
            C_MAGENTA,
            a_2b,
            "center",
            "center",
            line_spacing=1.35,
        )

        draw_panel(ctx, 80.0, 902.0, 1760.0, 92.0, a_2b, C_PANEL_BORDER, 16.0)
        draw_text(
            ctx,
            "Listen: <span foreground='#00F0FF'>Left ear {0, 4}</span> vs <span foreground='#FF2E93'>Right ear {2, 6}</span> — disjoint 8-EDO chords — while the <span foreground='#FFB800'>center melody (3, 5, 7, 1)</span> sings in exact unison.",
            WIDTH * 0.5,
            948.0,
            "DejaVu Sans 17",
            C_WHITE,
            a_2b,
            "center",
            "center",
        )


# ---------------------------------------------------------------------------
# Scene 3 (37.0 - 47.0s): Novelty 1B — Theorem B & Corollary B.1 Classification
# ---------------------------------------------------------------------------

def render_scene_3(ctx: cairo.Context, t: float) -> None:
    a = scene_alpha(t, 36.8, 47.2, fade_in=0.6, fade_out=0.6)
    if a <= 0.0:
        return

    draw_pill(ctx, "NOVELTY 1  ·  EXACT CLASSIFICATION (ALL N ≥ 5, ALL S)", 80.0, 50.0, C_EMERALD, a)
    draw_text(ctx, "<b>Theorem B &amp; Corollary B.1: Open Problem (3) Resolved</b>", 80.0, 102.0, "DejaVu Sans 36", C_WHITE, a)

    draw_panel(ctx, 80.0, 178.0, 1760.0, 218.0, a, C_CYAN, 22.0)
    draw_text(
        ctx,
        "<b>THEOREM B (Exact Iff Boundary):</b>  A 1-moving-voice held-note collision exists across all <i>N</i> ≥ 5, all <i>S</i>, all step-free <i>C</i> ∈ {<i>T</i>, <i>T/I</i>}  <b>iff</b>",
        WIDTH * 0.5,
        214.0,
        "DejaVu Sans 19",
        C_WHITE,
        a,
        "center",
        "center",
    )
    draw_text(
        ctx,
        "<b><i>N</i> = 8<i>m</i>  (<i>m</i> ≥ 1)      ∧      <i>C</i> = <i>T/I</i>({0, <i>m</i>, 4<i>m</i>})      ∧      2<i>m</i> ∈ <i>S</i></b>",
        WIDTH * 0.5,
        290.0,
        "DejaVu Serif 30",
        C_GOLD,
        a,
        "center",
        "center",
    )
    draw_text(
        ctx,
        "Pure <i>T</i>-orbits: ZERO collisions for ALL <i>N</i> ≥ 5 and ALL <i>S</i>.  Formalized universally in Lean 4 (<tt>thmB_one_voice_necessary</tt>, <tt>thmB_octatonic_sufficient</tt>).",
        WIDTH * 0.5,
        356.0,
        "DejaVu Sans 15",
        C_SLATE,
        a,
        "center",
        "center",
    )

    cor_p = ease_out_cubic(seg_prog(t, 42.3, 43.3))
    draw_panel(ctx, 80.0, 424.0, 1760.0, 358.0, a, C_EMERALD if cor_p > 0.5 else C_MAGENTA, 22.0)

    grid_title = (
        "<b>COROLLARY B.1 ACTIVE (Half-Closed / Consecutive <i>S</i> = {1,…,<i>k</i>}):</b>  2<i>m</i> ∈ <i>S</i> ⇒ <i>m</i> ∈ <i>S</i> (forbidden gap!) ⇒ <b>0 / 10,576 COLLISIONS!</b>"
        if cor_p > 0.5
        else "<b>EXHAUSTIVE MAXIMAL-<i>S</i><sub>max</sub> SWEEP (<i>N</i> = 5…72, 10,576 Chord Classes in Rust):</b>  Only the <b>9</b> octatonic multiples 8<i>m</i> collide!"
    )
    draw_text(ctx, grid_title, WIDTH * 0.5, 464.0, "DejaVu Sans 17.5", C_EMERALD if cor_p > 0.5 else C_WHITE, a, "center", "center")

    cols = 17
    gx0, gy0 = 122.0, 512.0
    cw, ch = 98.0, 58.0
    reveal_p = clamp01((t - 37.5) / 2.2)
    for idx in range(68):
        N = 5 + idx
        r, c = idx // cols, idx % cols
        x, y = gx0 + c * cw, gy0 + r * ch
        tile_a = clamp01((reveal_p * 71.0 - idx) / 3.0) * a
        if tile_a <= 0.0:
            continue
        is_oct = (N % 8 == 0)
        if is_oct:
            col = (
                C_MAGENTA[0] * (1 - cor_p) + C_EMERALD[0] * cor_p,
                C_MAGENTA[1] * (1 - cor_p) + C_EMERALD[1] * cor_p,
                C_MAGENTA[2] * (1 - cor_p) + C_EMERALD[2] * cor_p,
                1.0,
            )
            bg_a = 0.28 + 0.14 * (1 - cor_p)
        else:
            col = C_EMERALD
            bg_a = 0.12
        rounded_rect(ctx, x, y, cw - 10.0, ch - 10.0, 9.0)
        ctx.set_source_rgba(col[0], col[1], col[2], bg_a * tile_a)
        ctx.fill_preserve()
        ctx.set_source_rgba(col[0], col[1], col[2], (0.92 if is_oct else 0.42) * tile_a)
        ctx.set_line_width(2.4 if is_oct else 1.2)
        ctx.stroke()
        draw_text(ctx, f"<b>{N}</b>" if is_oct else f"{N}", x + (cw - 10.0) * 0.5, y + (ch - 10.0) * 0.5, "DejaVu Sans Mono 15", C_WHITE if is_oct else C_SLATE, tile_a, "center", "center")

    pillars = [
        ("Pure T-Orbits", "0 Collisions  (∀N ≥ 5, ∀S)", C_CYAN),
        ("Arbitrary S (T/I)", "Exact 9 Witnesses  (8, 16, …, 72)", C_MAGENTA),
        ("Consecutive S = {1,…,k}", "0 Collisions ∀N ≥ 5  (PROVED)", C_EMERALD),
    ]
    pw = 562.0
    for i, (h_txt, b_txt, col) in enumerate(pillars):
        px = 80.0 + i * (pw + 37.0)
        draw_panel(ctx, px, 810.0, pw, 168.0, a, col, 18.0)
        draw_text(ctx, f"<b>{h_txt}</b>", px + 28.0, 842.0, "DejaVu Sans 20", col, a)
        draw_text(ctx, b_txt, px + 28.0, 898.0, "DejaVu Sans Mono 17", C_WHITE, a)


# ---------------------------------------------------------------------------
# Scene 4 (47.0 - 61.0s): Novelty 2A — Theorem C Isotropy & C_6 Flower
# ---------------------------------------------------------------------------

def render_scene_4(ctx: cairo.Context, t: float, data: MathData) -> None:
    a = scene_alpha(t, 46.8, 61.2, fade_in=0.6, fade_out=0.6)
    if a <= 0.0:
        return

    draw_pill(ctx, "NOVELTY 2  ·  THEOREM C  ·  2D HONEYCOMB CUMULANTS", 80.0, 50.0, C_GOLD, a)
    draw_text(ctx, "<b>Exact 4th-Order Isotropy &amp; 6th-Order <i>C</i><sub>6</sub> Symmetry Breaking</b>", 80.0, 102.0, "DejaVu Sans 34", C_WHITE, a)

    # Top exact formula bar (fits comfortably inside 1760px!)
    draw_panel(ctx, 80.0, 174.0, 1760.0, 102.0, a, C_GOLD, 18.0)
    draw_text(
        ctx,
        "log(<i>ρ</i>(<i>ξ</i>) / 2)  =  − <span foreground='#00F0FF'><b>¼</b></span> <i>r</i>²  −  "
        "<span foreground='#2CF59B'><b>17 / 192</b></span> <i>r</i>⁴  −  "
        "<span foreground='#FFB800'><b>( 49 / 768  +  cos(6<i>α</i>) / 23040 )</b></span> <i>r</i>⁶  +  <i>O</i>(<i>r</i>⁸)",
        WIDTH * 0.5,
        225.0,
        "DejaVu Serif 24",
        C_WHITE,
        a,
        "center",
        "center",
    )

    # Left panel: Order 4 Isotropy
    draw_panel(ctx, 80.0, 304.0, 860.0, 686.0, a, C_EMERALD, 22.0)
    lcx, lcy = 510.0, 622.0
    draw_text(ctx, "<b>ORDER 4: 100% ROTATIONAL ISOTROPY</b>", lcx, 344.0, "DejaVu Sans 20", C_EMERALD, a, "center", "center")
    draw_text(
        ctx,
        "<i>m</i> · <i>κ</i><sub>ex</sub>(<b>e</b>·<b>X</b><sub><i>m</i></sub>)  =  −17/2  =  <b>−8.500</b>   (∀<b>e</b> ∈ <i>S</i>¹)",
        lcx,
        388.0,
        "DejaVu Serif 19",
        C_WHITE,
        a,
        "center",
        "center",
    )

    R4 = 182.0
    for frac in (0.45, 0.72, 1.0, 1.18):
        ctx.new_path()
        ctx.arc(lcx, lcy, R4 * frac, 0, 2 * math.pi)
        set_rgba(ctx, C_GRID, a * 1.4)
        ctx.set_line_width(1.2)
        ctx.stroke()

    sweep4 = ease_in_out_cubic(seg_prog(t, 47.6, 52.4))
    n_pts = 180
    k_max = max(2, int(sweep4 * n_pts))
    ctx.save()
    for mult, alp in [(3.4, 0.14), (1.0, 0.96)]:
        ctx.new_path()
        for k in range(k_max + 1):
            ang = 2.0 * math.pi * (k / n_pts)
            px, py = lcx + R4 * math.cos(ang), lcy - R4 * math.sin(ang)
            if k == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        set_rgba(ctx, C_EMERALD, a * alp)
        ctx.set_line_width(4.2 * mult)
        ctx.stroke()
    ctx.restore()

    ang4 = 2.0 * math.pi * sweep4
    hx4, hy4 = lcx + R4 * math.cos(ang4), lcy - R4 * math.sin(ang4)
    draw_glow_line(ctx, lcx, lcy, hx4, hy4, C_EMERALD, 2.2, a * 0.65)
    draw_glow_circle(ctx, hx4, hy4, 7.0, C_WHITE, a)

    axes_m40 = [
        (math.pi / 6.0,     abs(data.m_ex_kurt_u),      "W = −u", C_CYAN, f"{data.m_ex_kurt_u:.3f}", (64.0, -34.0)),
        (5 * math.pi / 6.0, abs(data.m_ex_kurt_v),      "v",      C_CYAN, f"{data.m_ex_kurt_v:.3f}", (-64.0, -34.0)),
        (0.0,               abs(data.m_ex_kurt_zigzag), "4u+3v",  C_GOLD, f"{data.m_ex_kurt_zigzag:.3f}", (62.0, 6.0)),
    ]
    p_pts = ease_out_cubic(seg_prog(t, 50.8, 52.6))
    for ang_a, val_a, nm, col, vstr, (odx, ody) in axes_m40:
        rr = R4 * (val_a / 8.5)
        px, py = lcx + rr * math.cos(ang_a), lcy - rr * math.sin(ang_a)
        draw_glow_circle(ctx, px, py, 9.0 * p_pts, col, a * p_pts)
        draw_text(ctx, f"<b>{nm}</b>\n{vstr}", px + odx, py + ody, "DejaVu Sans Mono 13", col, a * p_pts, "center", "center")

    draw_text(
        ctx,
        "Resolves <b>NEG-E3</b>: Ramanujan exponential decay <i>O</i>(<i>m</i>² 2<sup>−<i>m</i>/2</sup>), zero <i>O</i>(1) offset.",
        lcx,
        932.0,
        "DejaVu Sans 14.5",
        C_SLATE,
        a,
        "center",
        "center",
        max_width=790.0,
    )

    # Right panel: Order 6 Hexagonal C_6 Symmetry Breaking
    draw_panel(ctx, 980.0, 304.0, 860.0, 686.0, a, C_GOLD, 22.0)
    rcx, rcy = 1410.0, 622.0
    draw_text(ctx, "<b>ORDER 6: HEXAGONAL <i>C</i><sub>6</sub> SYMMETRY BREAKING</b>", rcx, 344.0, "DejaVu Sans 20", C_GOLD, a, "center", "center")
    draw_text(
        ctx,
        "<i>m</i>² · <i>κ</i><sub>6</sub> / <i>κ</i><sub>2</sub>³  =  <b>(1470 + cos 6<i>α</i>) / 4</b>",
        rcx,
        388.0,
        "DejaVu Serif 19",
        C_WHITE,
        a,
        "center",
        "center",
    )

    R6_base, R6_amp = 166.0, 40.0
    ctx.save()
    ctx.new_path()
    ctx.set_dash([7.0, 6.0])
    ctx.arc(rcx, rcy, R6_base, 0, 2 * math.pi)
    set_rgba(ctx, C_SLATE, a * 0.45)
    ctx.set_line_width(1.6)
    ctx.stroke()
    ctx.restore()

    bloom = ease_out_cubic(seg_prog(t, 53.6, 58.0))
    for k in range(6):
        ang_zz = k * math.pi / 3.0
        ang_ac = ang_zz + math.pi / 6.0
        ctx.new_path()
        ctx.move_to(rcx, rcy)
        ctx.line_to(rcx + (R6_base + R6_amp + 10) * math.cos(ang_zz), rcy - (R6_base + R6_amp + 10) * math.sin(ang_zz))
        set_rgba(ctx, C_GOLD, a * 0.25 * bloom)
        ctx.set_line_width(1.5)
        ctx.stroke()

        ctx.new_path()
        ctx.move_to(rcx, rcy)
        ctx.line_to(rcx + (R6_base - R6_amp) * math.cos(ang_ac), rcy - (R6_base - R6_amp) * math.sin(ang_ac))
        set_rgba(ctx, C_CYAN, a * 0.25 * bloom)
        ctx.set_line_width(1.5)
        ctx.stroke()

    n_c6 = 240
    k_c6 = max(2, int(bloom * n_c6))
    ctx.save()
    for mult, alp in [(3.5, 0.14), (1.0, 0.98)]:
        ctx.new_path()
        for k in range(k_c6 + 1):
            ang = 2.0 * math.pi * (k / n_c6)
            rr = R6_base + R6_amp * bloom * math.cos(6.0 * ang)
            px, py = rcx + rr * math.cos(ang), rcy - rr * math.sin(ang)
            if k == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        set_rgba(ctx, C_GOLD, a * alp)
        ctx.set_line_width(4.0 * mult)
        ctx.stroke()
    ctx.restore()

    p_lbl = ease_out_cubic(seg_prog(t, 56.2, 57.8))
    if p_lbl > 0.0:
        zx, zy = rcx + (R6_base + R6_amp), rcy
        draw_glow_circle(ctx, zx, zy, 9.0, C_GOLD, a * p_lbl)
        draw_text(
            ctx,
            "<b>Zigzag (4u+3v)</b>\n<b>367.75</b>\ncos 6α = +1",
            rcx + 230.0,
            rcy - 122.0,
            "DejaVu Sans Mono 13",
            C_GOLD,
            a * p_lbl,
            "left",
            "center",
        )
        draw_glow_line(ctx, zx, zy - 10, rcx + 224.0, rcy - 92.0, C_GOLD, 1.5, a * p_lbl * 0.6)

        ang_ac = 5.0 * math.pi / 6.0
        ax, ay = rcx + (R6_base - R6_amp) * math.cos(ang_ac), rcy - (R6_base - R6_amp) * math.sin(ang_ac)
        draw_glow_circle(ctx, ax, ay, 9.0, C_CYAN, a * p_lbl)
        draw_text(
            ctx,
            "<b>Armchair (W=−u, v)</b>\n<b>367.25</b>\ncos 6α = −1",
            rcx - 398.0,
            rcy - 122.0,
            "DejaVu Sans Mono 13",
            C_CYAN,
            a * p_lbl,
            "left",
            "center",
        )
        draw_glow_line(ctx, ax - 8, ay - 6, rcx - 196.0, rcy - 108.0, C_CYAN, 1.5, a * p_lbl * 0.6)

    draw_text(
        ctx,
        "Modulation magnified for clarity: exact splitting <b>1469/4 = 367.25</b> vs <b>1471/4 = 367.75</b>.",
        rcx,
        932.0,
        "DejaVu Sans 14.5",
        C_SLATE,
        a,
        "center",
        "center",
        max_width=790.0,
    )


# ---------------------------------------------------------------------------
# Scene 5 (61.0 - 75.0s): Novelty 2B — Edgeworth Ladder at m = 40
# ---------------------------------------------------------------------------

def render_scene_5(ctx: cairo.Context, t: float, data: MathData) -> None:
    a = scene_alpha(t, 60.8, 75.2, fade_in=0.6, fade_out=0.6)
    if a <= 0.0:
        return

    draw_pill(ctx, "NOVELTY 2  ·  CORRESPONDENCE LADDER AT m = 40", 80.0, 50.0, C_CYAN, a)
    draw_text(ctx, "<b>54,975,717,792 Prime Cadences:  1×  →  10.9×  →  75.3×</b>", 80.0, 102.0, "DejaVu Sans 37", C_WHITE, a)

    p_g0 = ease_out_cubic(seg_prog(t, 62.6, 63.6))
    p_g4 = ease_out_cubic(seg_prog(t, 66.2, 67.2))
    p_g6 = ease_out_cubic(seg_prog(t, 69.8, 70.8))

    draw_panel(ctx, 80.0, 178.0, 1140.0, 488.0, a, C_PANEL_BORDER, 22.0)
    gx, gy, gw, gh = 158.0, 228.0, 1020.0, 376.0

    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        yy = gy + gh * (1.0 - frac)
        ctx.new_path()
        ctx.move_to(gx, yy)
        ctx.line_to(gx + gw, yy)
        set_rgba(ctx, C_GRID, a * 1.2)
        ctx.set_line_width(1.1)
        ctx.stroke()
        draw_text(ctx, f"{0.32 * frac:.2f}", gx - 14.0, yy, "DejaVu Sans Mono 12", C_DIM, a, "right", "center")

    w_min, w_max = -5, 5

    def wx(wf: float) -> float:
        return gx + gw * ((wf - (w_min - 0.65)) / ((w_max + 0.65) - (w_min - 0.65)))

    def py_hist(prob: float) -> float:
        return gy + gh * (1.0 - prob / 0.32)

    bar_w = gw / 12.6 * 0.62
    for w_i in range(w_min, w_max + 1):
        prob = float(data.p_exact[w_i + 8])
        bx = wx(float(w_i)) - bar_w * 0.5
        by = py_hist(prob)
        rounded_rect(ctx, bx, by, bar_w, (gy + gh) - by, 5.0)
        set_rgba(ctx, (0.28, 0.44, 0.68, 0.36), a)
        ctx.fill_preserve()
        set_rgba(ctx, (0.58, 0.74, 0.96, 0.74), a)
        ctx.set_line_width(1.6)
        ctx.stroke()
        draw_text(ctx, f"{w_i:+d}" if w_i != 0 else "0", wx(float(w_i)), gy + gh + 20.0, "DejaVu Sans Mono 13", C_SLATE, a, "center", "center")

    draw_text(ctx, "Exact prime winding distribution <i>P</i><sub>40</sub>(<i>w</i>)", gx + 8.0, gy - 12.0, "DejaVu Sans 16", C_SLATE, a, "left", "bottom")

    sig = math.sqrt(40.0 / 24.0)
    c4 = -17.0 / (48.0 * 40.0)
    c6 = 1469.0 / (2880.0 * 1600.0)
    c8 = 289.0 / (4608.0 * 1600.0)

    def draw_curve(order: int, col: Tuple[float, float, float, float], prog: float, lw: float) -> None:
        if prog <= 0.0:
            return
        w_int = np.arange(-24, 25, dtype=np.float64)

        def eval_raw(arr: np.ndarray) -> np.ndarray:
            z = arr / sig
            z2 = z * z
            b = np.exp(-0.5 * z2)
            if order == 0:
                return b
            h4 = z2 * z2 - 6.0 * z2 + 3.0
            poly = 1.0 + c4 * h4
            if order >= 6:
                h6 = z2 ** 3 - 15.0 * z2 ** 2 + 45.0 * z2 - 15.0
                h8 = z2 ** 4 - 28.0 * z2 ** 3 + 210.0 * z2 ** 2 - 420.0 * z2 + 105.0
                poly = poly + c6 * h6 + c8 * h8
            return np.maximum(0.0, b * poly)

        zn = float(np.sum(eval_raw(w_int)))
        xs = np.linspace(w_min - 0.4, w_max + 0.4, 240)
        ys = eval_raw(xs) / zn
        k_lim = max(2, int(prog * len(xs)))
        ctx.save()
        for m_w, alp in [(2.8, 0.16), (1.0, 0.96)]:
            ctx.new_path()
            for k in range(k_lim):
                px, py = wx(float(xs[k])), py_hist(float(ys[k]))
                if k == 0:
                    ctx.move_to(px, py)
                else:
                    ctx.line_to(px, py)
            set_rgba(ctx, col, a * alp)
            ctx.set_line_width(lw * m_w)
            ctx.stroke()
        ctx.restore()

    draw_curve(0, C_CORAL, p_g0, 2.6)
    draw_curve(4, C_GOLD, p_g4, 3.0)
    draw_curve(6, C_CYAN, p_g6, 3.6)

    # Bottom zoomed residual panel
    draw_panel(ctx, 80.0, 692.0, 1140.0, 300.0, a, C_PANEL_BORDER, 22.0)
    rx0, ry0, rw0, rh0 = 158.0, 742.0, 1020.0, 214.0
    rmid = ry0 + rh0 * 0.5
    max_res = 0.011

    draw_text(
        ctx,
        "<b>ZOOMED RESIDUAL</b>  <i>P</i><sub>40</sub>(<i>w</i>) − <i>Q</i>(<i>w</i>)   (±0.011 scale — watch the error flatten!)",
        rx0,
        ry0 - 14.0,
        "DejaVu Sans 16",
        C_WHITE,
        a,
        "left",
        "bottom",
    )
    ctx.new_path()
    ctx.move_to(rx0, rmid)
    ctx.line_to(rx0 + rw0, rmid)
    set_rgba(ctx, C_SLATE, a * 0.55)
    ctx.set_line_width(1.4)
    ctx.stroke()
    for val_r in (-0.010, 0.0, 0.010):
        yy = rmid - (val_r / max_res) * (rh0 * 0.45)
        draw_text(ctx, f"{val_r:+.3f}", rx0 - 14.0, yy, "DejaVu Sans Mono 11", C_DIM, a, "right", "center")

    def draw_residual_series(q_arr: np.ndarray, col: Tuple[float, float, float, float], prog: float, lw: float) -> None:
        if prog <= 0.0:
            return
        pts = [
            (wx(float(w_i)), rmid - (float(data.p_exact[w_i + 8] - q_arr[w_i + 8]) / max_res) * (rh0 * 0.45))
            for w_i in range(w_min, w_max + 1)
        ]
        for k in range(len(pts) - 1):
            draw_glow_line(ctx, pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], col, lw, a * prog)
        for px, py in pts:
            draw_glow_circle(ctx, px, py, 5.2, col, a * prog)

    draw_residual_series(data.q_gauss, C_CORAL, p_g0 * (0.45 if p_g6 > 0.5 else 1.0), 2.5)
    draw_residual_series(data.q_edge4, C_GOLD, p_g4 * (0.65 if p_g6 > 0.5 else 1.0), 2.8)
    draw_residual_series(data.q_edge6, C_CYAN, p_g6, 3.4)

    # Right column: Live Correspondence Ladder Scorecard
    sx, sw = 1254.0, 586.0
    cards = [
        ("C-2  ·  GAUSSIAN  O(1/m)", f"TV  = {data.tv_gauss:.4e}   (1.0×)", f"JSD = {data.jsd_gauss:.4e}", C_CORAL, p_g0, 1.0 / 75.3),
        ("C-2' ·  4TH EDGEWORTH  O(1/m²)", f"TV  = {data.tv_edge4:.4e}   ({data.tv_gauss/data.tv_edge4:.1f}×)", f"JSD = {data.jsd_edge4:.4e}   ({data.jsd_gauss/data.jsd_edge4:.1f}×)", C_GOLD, p_g4, (data.tv_gauss / data.tv_edge4) / 75.3),
        ("C-2'' · 6TH EDGEWORTH  O(1/m³)", f"TV  = {data.tv_edge6:.4e}   ({data.tv_gauss/data.tv_edge6:.1f}×)", f"JSD = {data.jsd_edge6:.4e}   ({data.jsd_gauss/data.jsd_edge6:.1f}×)", C_CYAN, p_g6, 1.0),
    ]
    for i, (title, tv_s, jsd_s, col, prog, bar_frac) in enumerate(cards):
        cy_c = 178.0 + i * 226.0
        ca = a * (0.25 + 0.75 * prog)
        draw_panel(ctx, sx, cy_c, sw, 200.0, ca, col if prog > 0.2 else C_PANEL_BORDER, 20.0, border_width=2.4 if prog > 0.5 else 1.4)
        draw_text(ctx, f"<b>{title}</b>", sx + 28.0, cy_c + 24.0, "DejaVu Sans 18", col, ca)
        draw_text(ctx, f"<b>{tv_s}</b>", sx + 28.0, cy_c + 66.0, "DejaVu Sans Mono 19", C_WHITE, ca)
        draw_text(ctx, jsd_s, sx + 28.0, cy_c + 106.0, "DejaVu Sans Mono 16", C_SLATE, ca)
        bx0, by0, bw0 = sx + 28.0, cy_c + 154.0, sw - 56.0
        rounded_rect(ctx, bx0, by0, bw0, 16.0, 8.0)
        set_rgba(ctx, (0.12, 0.18, 0.30, 0.8), ca)
        ctx.fill()
        rounded_rect(ctx, bx0, by0, max(14.0, bw0 * bar_frac * prog), 16.0, 8.0)
        set_rgba(ctx, col, ca)
        ctx.fill()

    draw_panel(ctx, sx, 858.0, sw, 134.0, a * p_g6, C_EMERALD, 18.0)
    draw_text(
        ctx,
        "<b>Audit Catch (NEG-E9):</b> Clipped Edgeworth tails vanish at <i>w</i> = ±5.\nReplaced partial KL with exact bounded <b>JSD ≥ 0</b> + R-Type guard.",
        sx + 26.0,
        884.0,
        "DejaVu Sans 13.5",
        C_EMERALD,
        a * p_g6,
        max_width=sw - 52.0,
        line_spacing=1.35,
    )


# ---------------------------------------------------------------------------
# Scene 6 (75.0 - 84.0s): 4-Language Scorecard & Reconciliation End Slate
# ---------------------------------------------------------------------------

def render_scene_6(ctx: cairo.Context, t: float) -> None:
    a = scene_alpha(t, 74.8, 84.0, fade_in=0.6, fade_out=0.7)
    if a <= 0.0:
        return

    draw_pill(ctx, "FOUR-LANGUAGE MACHINE-CHECKED VERIFICATION", WIDTH * 0.5, 48.0, C_EMERALD, a, "center")
    draw_text(ctx, "<b>Zero Cached Data Reads. Zero Arbitrary Shortcuts.</b>", WIDTH * 0.5, 124.0, "DejaVu Sans 38", C_WHITE, a, "center", "center")

    cards = [
        (
            75.5,
            "LEAN 4.36.0  ·  FORMAL PROOFS",
            C_CYAN,
            "• <b>24 / 24</b> Lake jobs PASS (0 errors, 0 warnings)\n"
            "• <b>0 sorryAx</b> · <b>0 ofReduceBool</b> · Zero Mathlib\n"
            "• Universal ∀<i>N</i> proofs: Thms A, B, Cor B.1, NEG-M11 &amp; Thm C",
        ),
        (
            76.4,
            "LANE 1  ·  PURE C++20 (g++ &amp; clang++)",
            C_GOLD,
            "• Dual-compiler strict <tt>-O2 -Wall -Wextra -Werror</tt>\n"
            "• <b>30 / 30</b> standalone SWE-sweep assertions PASS\n"
            "• Bareiss + modular SNF, Dhar gonality, Edgeworth &amp; 2D axes",
        ),
        (
            77.3,
            "SWIFT++  ·  SWIFT 6.4 ↔ C++20 INTEROP",
            C_MAGENTA,
            "• Pure Swift 6.4 vs Live C++20 Interop at every turn\n"
            "• <b>15 / 15</b> XCTests  ·  <b>19 / 19</b> CLI gates PASS\n"
            "• Max cross-lane delta: <b>0.000e+00</b>",
        ),
        (
            78.2,
            "4TH LANGUAGE  ·  RUST 1.100.0",
            C_EMERALD,
            "• Zero external crates  ·  <b>7 / 7</b> integration tests PASS\n"
            "• Exhaustive sweep: <b>10,576</b> chords (<i>N</i> ≤ 72, <i>S</i><sub>max</sub>)\n"
            "• Extends baseline Thm 4.3 to <b>11,452</b> systems (<i>N</i> ≤ 96)",
        ),
    ]

    cw, ch = 858.0, 248.0
    for idx, (t_in, title, col, body) in enumerate(cards):
        r, c = idx // 2, idx % 2
        px = 80.0 + c * (cw + 44.0)
        py = 196.0 + r * (ch + 30.0)
        p = ease_out_cubic(seg_prog(t, t_in, t_in + 0.65))
        ca = a * p
        if ca <= 0.0:
            continue
        yo = 16.0 * (1 - p)
        draw_panel(ctx, px, py + yo, cw, ch, ca, col, 22.0, border_width=2.4)
        draw_pill(ctx, "PASS", px + cw - 26.0, py + 24.0 + yo, C_EMERALD, ca, "right", "DejaVu Sans Bold 13")
        draw_text(ctx, f"<b>{title}</b>", px + 30.0, py + 32.0 + yo, "DejaVu Sans 19", col, ca)
        draw_text(ctx, body, px + 30.0, py + 86.0 + yo, "DejaVu Sans 16.5", C_WHITE, ca, max_width=cw - 60.0, line_spacing=1.45)

    p_end = ease_out_cubic(seg_prog(t, 79.1, 80.2))
    draw_panel(ctx, 80.0, 768.0, 1760.0, 214.0, a * p_end, C_GOLD, 24.0, border_width=2.6)
    draw_text(ctx, "<b>ERGENTICS  ·  MORPHEUS  ·  PRIME CADENCES</b>", WIDTH * 0.5, 822.0, "DejaVu Sans 29", C_WHITE, a * p_end, "center", "center")
    draw_text(
        ctx,
        "Audit-Forward Contribution by <span foreground='#00F0FF'><b>Gemini 4 Neon</b></span>   ·   Ready for <span foreground='#FFB800'><b>Grok Bot Reconciliation</b></span>",
        WIDTH * 0.5,
        880.0,
        "DejaVu Sans 21",
        C_SLATE,
        a * p_end,
        "center",
        "center",
    )
    draw_text(
        ctx,
        "Code Commit 60c786d (MIT)  ·  Data Manifest e911bec (CC BY 4.0)  ·  github.com/Ergentics1/Morpheus",
        WIDTH * 0.5,
        936.0,
        "DejaVu Sans Mono 16",
        C_EMERALD,
        a * p_end,
        "center",
        "center",
    )


# ---------------------------------------------------------------------------
# Master Frame Renderer + Poster Generator
# ---------------------------------------------------------------------------

def render_frame_surface(t: float, data: MathData) -> cairo.ImageSurface:
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    draw_background(ctx, t, show_timeline=True)

    if t < 6.4:
        render_scene_0(ctx, t)
    if 5.6 <= t <= 19.4:
        render_scene_1(ctx, t, data)
    if 18.6 <= t <= 37.4:
        render_scene_2(ctx, t, data)
    if 36.6 <= t <= 47.4:
        render_scene_3(ctx, t)
    if 46.6 <= t <= 61.4:
        render_scene_4(ctx, t, data)
    if 60.6 <= t <= 75.4:
        render_scene_5(ctx, t, data)
    if t >= 74.6:
        render_scene_6(ctx, t)

    return surf


def render_poster(data: MathData, poster_path: str) -> None:
    """Render a crisp 1920x1080 hero thumbnail PNG (zero PNG text metadata chunks)."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    draw_background(ctx, 0.0, show_timeline=False)

    draw_pill(ctx, "ERGENTICS  ·  MORPHEUS  ·  ADPIE CYCLE 4", 90.0, 88.0, C_CYAN, 1.0, "left", "DejaVu Sans Bold 15")
    draw_text(ctx, "<b>PRIME\nCADENCES</b>", 90.0, 168.0, "DejaVu Sans 86", C_WHITE, 1.0, line_spacing=0.98)
    draw_text(
        ctx,
        "Two Original Proofs, One 8-EDO Counterexample,\nand Exact 6th-Order Honeycomb Cumulants",
        90.0,
        438.0,
        "DejaVu Serif 25",
        C_GOLD,
        1.0,
        line_spacing=1.32,
    )

    badges = [
        ("THEOREMS A, B &amp; COR B.1", "Open Problem (3) resolved ∀N ≥ 5  ·  NEG-M11 (N=8, S={2})", C_MAGENTA),
        ("THEOREM C  (C-2' / C-2'')", "4th-order isotropy (−17/2m)  ·  C₆ splitting  ·  75.3× TV leap", C_CYAN),
        ("4-LANGUAGE MACHINE-CHECKED", "Lean 4.36 · C++20 · Swift++ (0.000e+00) · Rust (10,576 chords)", C_EMERALD),
    ]
    for i, (b_head, b_sub, col) in enumerate(badges):
        by = 590.0 + i * 124.0
        draw_panel(ctx, 90.0, by, 930.0, 102.0, 1.0, col, 16.0, border_width=2.2)
        draw_text(ctx, f"<b>{b_head}</b>", 118.0, by + 18.0, "DejaVu Sans Bold 16", col, 1.0)
        draw_text(ctx, b_sub, 118.0, by + 54.0, "DejaVu Sans Mono 15", C_WHITE, 1.0)

    # Right hero graphic: glowing C_6 lotus + 8-EDO tritone duality motif
    rcx, rcy = 1465.0, 495.0
    R_base, R_amp = 248.0, 62.0
    for rr in (188.0, 248.0, 310.0):
        ctx.new_path()
        ctx.arc(rcx, rcy, rr, 0, 2 * math.pi)
        set_rgba(ctx, C_GRID, 1.45)
        ctx.set_line_width(1.5)
        ctx.stroke()
    ctx.new_path()
    ctx.arc(rcx, rcy, R_base, 0, 2 * math.pi)
    set_rgba(ctx, C_EMERALD, 0.85)
    ctx.set_line_width(3.0)
    ctx.stroke()

    for mult, alp in [(3.6, 0.14), (1.0, 0.98)]:
        ctx.new_path()
        for k in range(241):
            ang = 2.0 * math.pi * (k / 240.0)
            rr = R_base + R_amp * math.cos(6.0 * ang)
            px, py = rcx + rr * math.cos(ang), rcy - rr * math.sin(ang)
            if k == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        set_rgba(ctx, C_GOLD, alp)
        ctx.set_line_width(4.5 * mult)
        ctx.stroke()

    draw_glow_line(ctx, rcx - 125, rcy, rcx + 125, rcy, C_CYAN, 5.0, 0.95)
    draw_glow_line(ctx, rcx, rcy - 125, rcx, rcy + 125, C_MAGENTA, 5.0, 0.95)
    for dx, dy, col in [(-125, 0, C_CYAN), (125, 0, C_CYAN), (0, -125, C_MAGENTA), (0, 125, C_MAGENTA)]:
        draw_glow_circle(ctx, rcx + dx, rcy + dy, 12.0, col, 1.0)
    draw_glow_circle(ctx, rcx, rcy, 16.0, C_GOLD, 1.0)

    draw_text(
        ctx,
        "<b>Gemini 4 Neon</b>  ·  For Grok Bot Reconciliation",
        rcx,
        896.0,
        "DejaVu Sans Mono 16.5",
        C_WHITE,
        0.95,
        "center",
        "center",
    )
    draw_text(
        ctx,
        "github.com/Ergentics1/Morpheus  ·  MIT / CC BY 4.0",
        rcx,
        938.0,
        "DejaVu Sans Mono 13.5",
        C_SLATE,
        0.90,
        "center",
        "center",
    )

    os.makedirs(os.path.dirname(os.path.abspath(poster_path)), exist_ok=True)
    surf.write_to_png(poster_path)


# ---------------------------------------------------------------------------
# Multiprocess Video Encoder Pipeline
# ---------------------------------------------------------------------------

_G_DATA: MathData | None = None


def _init_worker(data: MathData) -> None:
    global _G_DATA, _BG_CACHE
    _G_DATA = data
    _BG_CACHE = build_static_bg_surface()


def _render_frame_bytes(frame_idx: int) -> bytes:
    assert _G_DATA is not None
    surf = render_frame_surface(frame_idx / float(FPS), _G_DATA)
    return bytes(surf.get_data())


def encode_video(data: MathData, out_mp4: str, workers: int) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(out_mp4)), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = os.path.join(tmpdir, "soundtrack.wav")
        print("Synthesizing frame-synchronized 12-EDO & 8-EDO stereo musical score...", flush=True)
        synthesize_soundtrack(data, wav_path)

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-loglevel", "warning",
            "-f", "rawvideo",
            "-pix_fmt", "bgra",
            "-s", f"{WIDTH}x{HEIGHT}",
            "-r", str(FPS),
            "-i", "pipe:0",
            "-i", wav_path,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            "-map_metadata", "-1",
            "-shortest",
            out_mp4,
        ]
        print(f"Rendering {TOTAL_FRAMES} frames ({WIDTH}x{HEIGHT} @ {FPS}fps) with {workers} workers...", flush=True)
        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
        assert proc.stdin is not None
        try:
            with mp.Pool(processes=workers, initializer=_init_worker, initargs=(data,)) as pool:
                for idx, raw in enumerate(pool.imap(_render_frame_bytes, range(TOTAL_FRAMES), chunksize=8)):
                    proc.stdin.write(raw)
                    if (idx + 1) % 300 == 0 or idx + 1 == TOTAL_FRAMES:
                        print(f"  rendered {idx + 1}/{TOTAL_FRAMES} frames ({100.0 * (idx + 1) / TOTAL_FRAMES:.1f}%)", flush=True)
        finally:
            proc.stdin.close()
            rc = proc.wait()
        if rc != 0:
            raise RuntimeError(f"ffmpeg exited with code {rc}")
    sz_mb = os.path.getsize(out_mp4) / (1024.0 * 1024.0)
    print(f"Encoded {out_mp4} ({sz_mb:.2f} MB)", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Render Morpheus ADPIE Cycle 4 Gemini 4 Neon video.")
    ap.add_argument("--keyframes-dir", type=str, default=None, help="Export QA keyframe PNGs to this directory")
    ap.add_argument("--poster", type=str, default=None, help="Export 1920x1080 hero poster PNG")
    ap.add_argument("--output", type=str, default=None, help="Encode final 1080p stereo MP4")
    ap.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 2), help="Worker process count")
    args = ap.parse_args()

    print("Computing exact first-principles Tonnetz, NEG-M11, and m=40 transfer-matrix data...", flush=True)
    data = compute_all_math()
    print(
        f"  pi(40)={data.total_primes_40}, m*k4(u,v,zz)=({data.m_ex_kurt_u:.4f}, {data.m_ex_kurt_v:.4f}, {data.m_ex_kurt_zigzag:.4f}), "
        f"TV=({data.tv_gauss:.3e}, {data.tv_edge4:.3e}, {data.tv_edge6:.3e})",
        flush=True,
    )

    if args.keyframes_dir:
        os.makedirs(args.keyframes_dir, exist_ok=True)
        kfs = [
            ("00_title.png", 3.6),
            ("01a_tonnetz_hex.png", 10.6),
            ("01b_tonnetz_wind.png", 16.8),
            ("02a_theorem_a.png", 23.0),
            ("02b_neg_m11_8edo.png", 30.2),
            ("03a_theorem_b.png", 40.5),
            ("03b_cor_b1.png", 44.8),
            ("04_theorem_c_polar.png", 58.5),
            ("05_edgeworth_m40.png", 72.5),
            ("06_scorecard.png", 81.2),
        ]
        for fname, ts in kfs:
            outp = os.path.join(args.keyframes_dir, fname)
            render_frame_surface(ts, data).write_to_png(outp)
            print(f"  wrote keyframe {outp}", flush=True)

    if args.poster:
        render_poster(data, args.poster)
        print(f"  wrote poster {args.poster}", flush=True)

    if args.output:
        encode_video(data, args.output, args.workers)


if __name__ == "__main__":
    main()
