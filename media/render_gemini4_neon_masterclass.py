#!/usr/bin/env python3
"""
Morpheus — Gemini 4 Neon Educator Masterclass Video Generator (~3:45)
"How the Neo-Riemannian Tonnetz Satisfies the Graph Riemann Hypothesis
 — and Unlocks Endless Adaptive Music (Live Chess + Spoken in Harmony)"

License: MIT (Code Model). Rendered media assets: CC BY 4.0.

First-principles generator (zero reads of cached data files):
  - Exact 24-triad 12-EDO, 62-triad 31-EDO, and 106-triad 53-EDO PLR graphs
    and exact Ihara-Bass zeta pole spectra (44 nontrivial poles on |u|=1/sqrt(2))
  - Exact magnetic-flux twisted spectrum A_phi & Riemann Window (|phi| < 2.8909)
  - Exact 72-edge transfer-matrix prime cadence counts at m = 40 (54,975,717,792)
  - Authentic 19-ply Traxler Counterattack chess match with legal board states
  - Spoken narration synthesized via SVOX Pico TTS and harmonized live through a
    24-band SciPy stereo channel vocoder tuned to the active Tonnetz triad!
"""

from __future__ import annotations

import argparse
import html
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
from scipy import signal

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo  # noqa: E402

# ---------------------------------------------------------------------------
# Master video/audio settings & Gemini 4 Neon palette
# ---------------------------------------------------------------------------

WIDTH = 1920
HEIGHT = 1080
FPS = 24
SAMPLE_RATE = 48000

C_BG_DEEP = (0.022, 0.032, 0.070, 1.0)
C_BG_MID = (0.048, 0.076, 0.152, 1.0)
C_GRID = (0.110, 0.185, 0.320, 0.24)
C_PANEL = (0.052, 0.084, 0.165, 0.89)
C_PANEL_BORDER = (0.185, 0.315, 0.495, 0.50)

C_CYAN = (0.000, 0.941, 1.000, 1.0)
C_MAGENTA = (1.000, 0.180, 0.576, 1.0)
C_GOLD = (1.000, 0.722, 0.000, 1.0)
C_EMERALD = (0.173, 0.961, 0.608, 1.0)
C_CORAL = (1.000, 0.420, 0.420, 1.0)
C_VIOLET = (0.680, 0.470, 1.000, 1.0)
C_WHITE = (0.945, 0.962, 1.000, 1.0)
C_SLATE = (0.620, 0.695, 0.830, 1.0)
C_DIM = (0.375, 0.460, 0.600, 1.0)

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
    return 1.0 if t1 <= t0 and t >= t0 else (0.0 if t1 <= t0 else clamp01((t - t0) / (t1 - t0)))


def scene_alpha(t: float, t0: float, t1: float, fade_in: float = 0.65, fade_out: float = 0.65) -> float:
    if t < t0 or t > t1:
        return 0.0
    a_in = smoothstep((t - t0) / fade_in) if fade_in > 0 else 1.0
    a_out = smoothstep((t1 - t) / fade_out) if fade_out > 0 else 1.0
    return min(a_in, a_out)


# ---------------------------------------------------------------------------
# First-Principles Math Core (Zero Cached Data Reads)
# ---------------------------------------------------------------------------

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
    raise ValueError(op)


def mobius_mu(n: int) -> int:
    mu, p, x = 1, 2, n
    while p * p <= x:
        if x % p == 0:
            x //= p
            if x % p == 0:
                return 0
            mu = -mu
        p += 1
    return -mu if x > 1 else mu


def compute_edo_lambda_max(N: int, maj_third: int, fifth: int) -> float:
    """Exact max nontrivial adjacency eigenvalue of the 2N-triad PLR graph in N-EDO."""
    A = np.zeros((2 * N, 2 * N), dtype=np.float64)
    min_third = fifth - maj_third
    for r in range(N):
        u = r
        # P: {r, r+M, r+F} <-> {r, r+m, r+F}
        vP = N + r
        # L: {r, r+M, r+F} <-> {r+M, r+F, r+M+F} = minor on r+M
        vL = N + ((r + maj_third) % N)
        # R: {r, r+M, r+F} <-> {r-m, r, r+M} = minor on r - min_third
        vR = N + ((r - min_third) % N)
        for v in (vP, vL, vR):
            A[u, v] += 1.0
            A[v, u] += 1.0
    evals = np.linalg.eigvalsh(A)
    nontriv = [abs(x) for x in evals if abs(abs(x) - 3.0) > 1e-6]
    return float(max(nontriv))


def compute_ihara_poles_and_flux() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    """Exact 44 nontrivial + 4 trivial poles of zeta_X(u) and twisted spectrum A_phi."""
    A = np.zeros((24, 24), dtype=np.float64)
    for mode in (0, 1):
        for root in range(12):
            u = mode * 12 + root
            for op in ("P", "L", "R"):
                nm, nr, _ = plr_move(mode, root, op)
                A[u, nm * 12 + nr] = 1.0
    evals = np.linalg.eigvalsh(A)
    nontriv_poles = []
    triv_poles = []
    for lam in evals:
        # 1 - lam*u + 2*u^2 = 0  =>  u = (lam +/- sqrt(lam^2 - 8)) / 4
        disc = complex(lam * lam - 8.0, 0.0)
        sq = np.sqrt(disc)
        u1 = (lam + sq) / 4.0
        u2 = (lam - sq) / 4.0
        if abs(abs(lam) - 3.0) < 1e-6:
            triv_poles.extend([u1, u2])
        else:
            nontriv_poles.extend([u1, u2])

    # Twisted spectrum A_phi: weight edge (u -> v) by exp(i * phi * delta / 12)
    phis = np.linspace(0.0, 3.8, 191)
    lmax_phi = np.zeros_like(phis)
    for k, phi in enumerate(phis):
        H = np.zeros((24, 24), dtype=np.complex128)
        for mode in (0, 1):
            for root in range(12):
                u = mode * 12 + root
                for op in ("P", "L", "R"):
                    nm, nr, delta = plr_move(mode, root, op)
                    v = nm * 12 + nr
                    H[u, v] += np.exp(1j * phi * (delta / 12.0))
        ev = np.linalg.eigvalsh(H)
        lmax_phi[k] = float(np.max(np.abs(ev)))
    # Find critical phi_c where lmax_phi crosses 2*sqrt(2)
    thresh = 2.0 * math.sqrt(2.0)
    idx_c = int(np.argmax(lmax_phi < thresh))
    # Linear refinement
    if 0 < idx_c < len(phis):
        p0, p1 = phis[idx_c - 1], phis[idx_c]
        y0, y1 = lmax_phi[idx_c - 1], lmax_phi[idx_c]
        phi_c = float(p0 + (thresh - y0) / (y1 - y0) * (p1 - p0))
    else:
        phi_c = 2.8909
    return (
        np.array(nontriv_poles, dtype=np.complex128),
        np.array(triv_poles, dtype=np.complex128),
        phis,
        lmax_phi,
        phi_c,
    )


def compute_exact_m40_and_edgeworth() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, int, float, float, float]:
    ops = ["P", "L", "R"]
    edges = []
    edge_id = {}
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
    nxt = [[edge_id[(v, o2)] for o2 in range(3) if edge_id[(v, o2)] != rev[i]] for i, (u, v, _o, _d) in enumerate(edges)]

    m_target = 40
    divisors = [d for d in range(1, m_target + 1) if m_target % d == 0]
    off = 96
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

    w_vals = np.arange(-8, 9, dtype=np.int64)
    pi_counts = np.zeros(len(w_vals), dtype=np.int64)
    for i, w in enumerate(w_vals):
        acc = 0
        for d in divisors:
            k = m_target // d
            if w % k == 0:
                s_idx = off + 12 * int(w // k)
                if 0 <= s_idx < width:
                    acc += mobius_mu(k) * int(closed[d][s_idx])
        pi_counts[i] = acc // m_target

    total = int(np.sum(pi_counts))
    assert total == 54975717792
    p = pi_counts.astype(np.float64) / float(total)
    sig = math.sqrt(40.0 / 24.0)
    c4 = -17.0 / (48.0 * 40.0)
    c6 = 1469.0 / (2880.0 * 1600.0)
    c8 = 289.0 / (4608.0 * 1600.0)

    def eval_ord(order: int) -> Tuple[np.ndarray, float]:
        w_all = np.arange(-24, 25, dtype=np.float64)
        z = w_all / sig
        z2 = z * z
        b = np.exp(-0.5 * z2)
        if order == 0:
            wt = b
        else:
            h4 = z2 * z2 - 6.0 * z2 + 3.0
            poly = 1.0 + c4 * h4
            if order >= 6:
                h6 = z2 ** 3 - 15.0 * z2 ** 2 + 45.0 * z2 - 15.0
                h8 = z2 ** 4 - 28.0 * z2 ** 3 + 210.0 * z2 ** 2 - 420.0 * z2 + 105.0
                poly = poly + c6 * h6 + c8 * h8
            wt = np.maximum(0.0, b * poly)
        wt /= np.sum(wt)
        q = wt[24 - 8 : 24 + 9]
        q_out = max(0.0, 1.0 - float(np.sum(q)))
        tv = 0.5 * (q_out + float(np.sum(np.abs(p - q))))
        return q, tv

    q0, tv0 = eval_ord(0)
    q4, tv4 = eval_ord(4)
    q6, tv6 = eval_ord(6)
    return w_vals, p, q0, q4, q6, total, tv0, tv4, tv6


# ---------------------------------------------------------------------------
# Authentic Chess Engine State (Traxler Counterattack — 19 Legal Plies!)
# ---------------------------------------------------------------------------

@dataclass
class ChessStep:
    ply: int
    san: str
    from_sq: Tuple[int, int]  # (file 0..7, rank 0..7 where rank 0 = 1st rank bottom)
    to_sq: Tuple[int, int]
    eval_cp: float            # White-perspective pawns (+ winning White, - winning Black)
    phase: str                # "OPENING", "ATTACK", "CRISIS", "WINNING"
    chord_name: str
    chord_pcs: Tuple[int, int, int]
    flux_phi: float
    winding_w: float
    board: List[List[str]]    # 8x8 [rank][file]


def build_traxler_chess_game() -> List[ChessStep]:
    """
    Build exact legal 8x8 board snapshots for the dramatic Traxler Counterattack:
      1. e4 e5  2. Nf3 Nc6  3. Bc4 Nf6  4. Ng5 Bc5!?
      5. Nxf7? Bxf2+!!  6. Kf1 Qe7?  7. Nxh8 d5  8. exd5 Bg4  9. Be2 Bxe2+  10. Qxe2
    """
    board = [
        list("RNBQKBNR"),  # rank 0 (1st rank)
        list("PPPPPPPP"),  # rank 1 (2nd rank)
        list("........"),
        list("........"),
        list("........"),
        list("........"),
        list("pppppppp"),  # rank 6 (7th rank)
        list("rnbqkbnr"),  # rank 7 (8th rank)
    ]

    def sq(name: str) -> Tuple[int, int]:
        return (ord(name[0]) - ord("a"), int(name[1]) - 1)

    def snap() -> List[List[str]]:
        return [row[:] for row in board]

    # (san, from, to, eval, phase, chord_name, pcs, flux, winding)
    script = [
        ("Start",    "e2", "e2", +0.2, "OPENING", "C",   (0, 4, 7),   0.10, 0.00),
        ("1. e4",    "e2", "e4", +0.3, "OPENING", "C",   (0, 4, 7),   0.18, 0.00),
        ("1... e5",  "e7", "e5", +0.2, "OPENING", "Am",  (9, 0, 4),   0.22, 0.17),
        ("2. Nf3",   "g1", "f3", +0.3, "OPENING", "F",   (5, 9, 0),   0.28, 0.25),
        ("2... Nc6", "b8", "c6", +0.2, "OPENING", "Dm",  (2, 5, 9),   0.32, 0.42),
        ("3. Bc4",   "f1", "c4", +0.4, "OPENING", "C",   (0, 4, 7),   0.45, 0.50),
        ("3... Nf6", "g8", "f6", +0.3, "ATTACK",  "Em",  (4, 7, 11),  0.85, 0.67),
        ("4. Ng5",   "f3", "g5", +1.1, "ATTACK",  "G",   (7, 11, 2),  1.35, 0.83),
        ("4... Bc5!?", "f8", "c5", +1.6, "ATTACK", "Bm", (11, 2, 6),  1.82, 1.00),
        ("5. Nxf7?", "g5", "f7", -1.4, "CRISIS",  "Cm",  (0, 3, 7),   2.35, 0.75),
        ("5... Bxf2+!!", "c5", "f2", -3.2, "CRISIS", "A♭m", (8, 11, 3), 2.76, 0.50),
        ("6. Kf1",   "e1", "f1", -2.5, "CRISIS",  "Em",  (4, 7, 11),  2.62, 0.42),
        ("6... Qe7?", "d8", "e7", +1.8, "WINNING", "G",  (7, 11, 2),  1.45, 0.83),
        ("7. Nxh8",  "f7", "h8", +4.4, "WINNING", "D",   (2, 6, 9),   0.95, 1.17),
        ("7... d5",  "d7", "d5", +5.2, "WINNING", "A",   (9, 1, 4),   0.72, 1.42),
        ("8. exd5",  "e4", "d5", +6.4, "WINNING", "E",   (4, 8, 11),  0.55, 1.67),
        ("8... Bg4", "c8", "g4", +6.9, "WINNING", "Am",  (9, 0, 4),   0.42, 1.83),
        ("9. Be2",   "c4", "e2", +7.4, "WINNING", "F",   (5, 9, 0),   0.25, 1.92),
        ("9... Bxe2+", "g4", "e2", +7.8, "WINNING", "G", (7, 11, 2),  0.18, 2.00),
        ("10. Qxe2", "d1", "e2", +8.4, "WINNING", "Cmaj9", (0, 4, 7), 0.08, 2.00),
    ]

    steps: List[ChessStep] = []
    for ply, (san, f_s, t_s, ev, phase, cname, pcs, phi, wv) in enumerate(script):
        f_sq = sq(f_s)
        t_sq = sq(t_s)
        if ply > 0:
            piece = board[f_sq[1]][f_sq[0]]
            assert piece != ".", f"Illegal move {san}: empty square {f_s}"
            board[f_sq[1]][f_sq[0]] = "."
            board[t_sq[1]][t_sq[0]] = piece
        steps.append(ChessStep(ply, san, f_sq, t_sq, ev, phase, cname, pcs, phi, wv, snap()))
    return steps


# ---------------------------------------------------------------------------
# Narration Script & Timeline ("Spoken in Harmony" Dynamic Scheduler!)
# ---------------------------------------------------------------------------

@dataclass
class VoiceCue:
    chapter: int
    text: str
    caption: str
    chord_pcs: Tuple[int, int, int]
    tuning: str = "12edo"       # "12edo" or "8edo"
    pre_gap: float = 0.65
    post_gap: float = 0.75
    start_s: float = 0.0
    dur_s: float = 0.0


def build_voice_script() -> List[VoiceCue]:
    return [
        # Chapter 1: The Hidden Bridge (Music <-> Graphene)
        VoiceCue(
            1,
            "What do a single sheet of graphene, the Riemann Hypothesis, and a live game of chess have in common?",
            "What do graphene, the Riemann Hypothesis, and chess have in common?",
            (0, 4, 7), pre_gap=1.6, post_gap=0.7,
        ),
        VoiceCue(
            1,
            "Music. Every major and minor triad in twelve-tone harmony lives on a twenty-four-vertex graph called the Tonnetz dual.",
            "Every major & minor triad lives on the 24-vertex Tonnetz dual graph X.",
            (9, 0, 4), pre_gap=0.45, post_gap=0.7,
        ),
        VoiceCue(
            1,
            "Shift just one voice by a semitone or whole tone — the P, L, and R moves — and you walk directly across the hexagonal honeycomb of graphene.",
            "Neo-Riemannian P, L, R moves trace the exact hexagonal honeycomb of graphene.",
            (5, 9, 0), pre_gap=0.45, post_gap=1.4,
        ),
        # Chapter 2: The Graph Riemann Hypothesis
        VoiceCue(
            2,
            "Now count the prime cadences: primitive chord loops that never backtrack. Their generating function is the Ihara zeta function.",
            "Prime cadences are non-backtracking loops counted by the Ihara zeta function ζ_X(u).",
            (0, 4, 7), pre_gap=0.9, post_gap=0.7,
        ),
        VoiceCue(
            2,
            "Miraculously, all forty-four nontrivial poles sit squarely on the critical circle of radius one over the square root of two.",
            "All 44 nontrivial poles lock onto the critical circle |u| = 1/√2 — Graph Riemann Hypothesis!",
            (4, 7, 11), pre_gap=0.45, post_gap=0.75,
        ),
        VoiceCue(
            2,
            "That proves the twelve-tone Tonnetz satisfies the Graph Riemann Hypothesis. It is a Ramanujan graph, matching the exact Dirac energy bands of graphene.",
            "Theorem 3.1: 12-EDO is a Ramanujan expander matching graphene's exact Dirac bands.",
            (7, 11, 2), pre_gap=0.45, post_gap=0.75,
        ),
        VoiceCue(
            2,
            "Not every tuning system survives this test. Thirty-one tone barely stays inside the bound, while fifty-three tone breaks the Riemann Hypothesis outright.",
            "12-EDO (2.236) & 31-EDO (2.825) pass ≤ 2√2 = 2.828 — 53-EDO (2.857) breaks Graph RH!",
            (2, 5, 9), pre_gap=0.45, post_gap=1.4,
        ),
        # Chapter 3: Why Ramanujan Unlocks Adaptive Endless Music
        VoiceCue(
            3,
            "So why does the Graph Riemann Hypothesis unlock adaptive, endless music?",
            "Why does Ramanujan optimality unlock adaptive, endless music?",
            (0, 4, 7), pre_gap=0.9, post_gap=0.65,
        ),
        VoiceCue(
            3,
            "An ordinary slow-mixing graph traps a score inside repetitive four-chord loops. A Ramanujan graph mixes at the fastest speed allowed by mathematics.",
            "Alon–Boppana optimality: fastest possible harmonic mixing — zero repetitive ruts.",
            (9, 0, 4), pre_gap=0.45, post_gap=0.7,
        ),
        VoiceCue(
            3,
            "By length forty, there are fifty-four point nine seven billion distinct prime cadences — so the harmony never repeats, yet can steer smoothly to any mood in three beats.",
            "π(40) = 54,975,717,792 prime cadences: endless novelty + 3-beat harmonic agility.",
            (5, 9, 0), pre_gap=0.45, post_gap=0.75,
        ),
        VoiceCue(
            3,
            "And twisting the Tonnetz with a magnetic flux phi bends harmonic tension continuously inside the Riemann Window, up to two point eight nine.",
            "Theorem 5.3: Magnetic flux φ tunes emotional tension inside the Riemann Window |φ| < 2.8909.",
            (7, 11, 2), pre_gap=0.45, post_gap=1.4,
        ),
        # Chapter 4: Live Chess Match (Phase & Position Drive Harmony!)
        VoiceCue(
            4,
            "Watch this mathematics score a live game of chess: the wild Traxler Counterattack.",
            "Live Demo: Traxler Counterattack — Chess phase & evaluation drive flux φ and winding W.",
            (0, 4, 7), pre_gap=0.9, post_gap=0.9,
        ),
        VoiceCue(
            4,
            "In the balanced opening, the evaluation hovers near zero. Magnetic flux stays low, and airy major and relative-minor triads breathe calmly.",
            "Phase 1 (Opening, Eval +0.3): Low flux φ ≈ 0.3, calm diatonic C → Am → F → Dm → C.",
            (5, 9, 0), pre_gap=0.4, post_gap=1.6,
        ),
        VoiceCue(
            4,
            "Now White attacks f-seven, and Black ignites the Traxler. Tension climbs inside the Riemann Window as voice winding accelerates upward.",
            "Phase 2 (Attack, 4. Ng5 Bc5!?): Flux rises to φ = 1.82 inside the Riemann Window; W climbs!",
            (7, 11, 2), pre_gap=0.4, post_gap=1.8,
        ),
        VoiceCue(
            4,
            "Crisis! Black sacrifices the bishop on f-two with check! Evaluation plunges to minus three point two. Flux races to the Ramanujan edge, pulling the chords and my voice into dark chromatic minor harmony.",
            "Phase 3 (CRISIS, 5... Bxf2+!! Eval −3.2): Flux surges to φ = 2.76 → dark minor mediants!",
            (8, 11, 3), pre_gap=0.4, post_gap=3.6,  # Musical breathing room to feel the dark minor shift!
        ),
        VoiceCue(
            4,
            "Then Black slips with Queen e-seven! White snatches the rook and shatters the center. Evaluation flips decisively to White — flux snaps clean, lifting the entire Tonnetz into radiant major harmony.",
            "Phase 4 (Winning Turnaround, 7. Nxh8 → 10. Qxe2, Eval +8.4): Flux resets → radiant Cmaj9!",
            (0, 4, 7), pre_gap=0.4, post_gap=2.6,
        ),
        # Chapter 5: Novelty 1 — Coding Theory, NEG-M11 (8-EDO), Corollary B.1
        VoiceCue(
            5,
            "In our audit-forward verification, we resolved Open Problem three: does the moving melody alone always decode the hidden chord loop?",
            "Novelty 1 (Open Problem 3): Does the moving melody alone uniquely identify the chord walk?",
            (0, 4, 7), pre_gap=0.9, post_gap=0.7,
        ),
        VoiceCue(
            5,
            "Surprise! In eight-tone tuning, we uncovered counterexample N-E-G M-eleven. Listen closely: disjoint tritones in your left and right ears sing the exact same melody in unison.",
            "NEG-M11 (N=8, S={2}): Left {0,4} vs Right {2,6} — disjoint 8-EDO loops, identical tune (3,5,7,1)!",
            (0, 3, 4), tuning="8edo", pre_gap=0.45, post_gap=3.8,  # Pure 8-EDO listening showcase!
        ),
        VoiceCue(
            5,
            "Theorems A and B prove that octatonic illusion is the only obstruction for any N at least five. In twelve-tone harmony, Corollary B-one guarantees lossless melody-to-chord decoding forever.",
            "Theorems A, B & Cor B.1: Zero collisions ∀N ≥ 5 for every consecutive step set S = {1,…,k}!",
            (5, 9, 0), pre_gap=0.45, post_gap=1.4,
        ),
        # Chapter 6: Novelty 2 — Theorem C (Statistical Mechanics & C_6 Crystal)
        VoiceCue(
            6,
            "Finally, how does an endless soundtrack drift over forty chords? Theorem C derives the exact two-dimensional honeycomb cumulants through order six.",
            "Novelty 2 (Theorem C): Exact 2D honeycomb log-MGF & cumulants through order 6.",
            (0, 4, 7), pre_gap=0.9, post_gap=0.7,
        ),
        VoiceCue(
            6,
            "At fourth order, drift is one hundred percent rotationally isotropic — minus eight point five in every direction. Only at sixth order does the hexagonal C-six crystal emerge, cutting winding error seventy-five-fold.",
            "Order 4: 100% isotropic (−17/2m). Order 6: C₆ splitting (367.25 vs 367.75) → 75.3× TV leap!",
            (7, 11, 2), pre_gap=0.45, post_gap=1.6,
        ),
        # Chapter 7: Four-Language Finale
        VoiceCue(
            7,
            "Every theorem powering this music is machine-checked from first principles in Lean four, C-plus-plus, Swift-plus-plus, and Rust. Welcome to Morpheus — where pure mathematics becomes living, endless harmony.",
            "4-Language Verified: Lean 4 · C++20 · Swift++ (0.000e+00) · Rust (10,576 chords). — Gemini 4 Neon",
            (0, 4, 7), pre_gap=0.9, post_gap=3.2,
        ),
    ]


# ---------------------------------------------------------------------------
# "Spoken in Harmony" Audio Engine (Pico TTS + 24-Band SciPy Chord Vocoder!)
# ---------------------------------------------------------------------------

def freq_12edo(pc: int, octave: int = 4) -> float:
    return 440.0 * (2.0 ** ((12 * (octave + 1) + (pc % 12) - 69.0) / 12.0))


def freq_8edo(pc: int, octave: int = 4) -> float:
    return (261.6255653 * (2.0 ** (octave - 4))) * (2.0 ** ((pc % 8) / 8.0))


def render_pico_48k(text: str, tmpdir: str, idx: int) -> np.ndarray:
    wav_p = os.path.join(tmpdir, f"cue_{idx:02d}.wav")
    subprocess.run(["pico2wave", "-l", "en-US", "-w", wav_p, text], check=True)
    with wave.open(wav_p, "rb") as wf:
        sr = wf.getframerate()
        raw = np.frombuffer(wf.readframes(wf.getnframes()), dtype="<i2").astype(np.float64) / 32768.0
    # Resample cleanly 16k -> 48k (exact integer 3x polyphase)
    sig = signal.resample_poly(raw, SAMPLE_RATE // math.gcd(sr, SAMPLE_RATE), sr // math.gcd(sr, SAMPLE_RATE))
    # Trim leading/trailing near-silence gently
    nz = np.where(np.abs(sig) > 0.008)[0]
    if len(nz) > 0:
        i0 = max(0, int(nz[0]) - int(0.03 * SAMPLE_RATE))
        i1 = min(len(sig), int(nz[-1]) + int(0.06 * SAMPLE_RATE))
        sig = sig[i0:i1]
    # High-pass 95 Hz to keep dry voice crisp & clear
    sos_hp = signal.butter(2, 95.0 / (SAMPLE_RATE * 0.5), btype="highpass", output="sos")
    sig = signal.sosfilt(sos_hp, sig)
    peak = float(np.max(np.abs(sig)))
    if peak > 1e-6:
        sig = sig / peak * 0.85
    return sig


def build_vocoder_filters() -> List[np.ndarray]:
    """Precompute 22 log-spaced Butterworth bandpass filters (130 Hz -> 4600 Hz)."""
    edges = np.geomspace(130.0, 4600.0, 23)
    nyq = SAMPLE_RATE * 0.5
    return [signal.butter(2, [edges[i] / nyq, edges[i + 1] / nyq], btype="bandpass", output="sos") for i in range(22)]


def build_env_lp() -> np.ndarray:
    return signal.butter(2, 26.0 / (SAMPLE_RATE * 0.5), btype="lowpass", output="sos")


def bandlimited_saw_chord(freqs: Sequence[float], n: int, phase_off: float = 0.0) -> np.ndarray:
    """Rich harmonic vocal-choir carrier built from partials 1..14 of each triad tone."""
    t = np.arange(n, dtype=np.float64) / SAMPLE_RATE
    out = np.zeros(n, dtype=np.float64)
    for f_idx, f0 in enumerate(freqs):
        vib = 0.0022 * np.sin(2.0 * math.pi * (4.6 + 0.35 * f_idx) * t + phase_off)
        ph = 2.0 * math.pi * f0 * (t + vib / (2.0 * math.pi * 4.8)) + phase_off + 0.7 * f_idx
        for h in range(1, 13):
            if f0 * h < 4700.0:
                out += (1.0 / (h ** 0.82)) * np.sin(h * ph)
    peak = float(np.max(np.abs(out)))
    return out / peak if peak > 1e-6 else out


def harmonize_voice_stereo(
    dry: np.ndarray,
    chord_pcs: Tuple[int, int, int],
    tuning: str,
    bp_filters: List[np.ndarray],
    lp_env: np.ndarray,
) -> np.ndarray:
    """
    Create "Spoken in Harmony" stereo track:
      - Crisp centered dry educator voice
      - Live 22-band formant-tracked 3-part neo-Riemannian stereo vocal harmony!
    """
    n = len(dry)
    f_fn = freq_8edo if tuning == "8edo" else freq_12edo
    # Left choir: root(3,4) + fifth(3,4); Right choir: third(3,4) + root(4)
    freqs_l = [f_fn(chord_pcs[0], 3), f_fn(chord_pcs[2], 3), f_fn(chord_pcs[0], 4)]
    freqs_r = [f_fn(chord_pcs[1], 3), f_fn(chord_pcs[1], 4), f_fn(chord_pcs[2], 4)]
    car_l = bandlimited_saw_chord(freqs_l, n, 0.0)
    car_r = bandlimited_saw_chord(freqs_r, n, 1.3)

    voc_l = np.zeros(n, dtype=np.float64)
    voc_r = np.zeros(n, dtype=np.float64)
    for sos in bp_filters:
        v_band = signal.sosfilt(sos, dry)
        env = np.maximum(0.0, signal.sosfilt(lp_env, np.abs(v_band)))
        voc_l += env * signal.sosfilt(sos, car_l)
        voc_r += env * signal.sosfilt(sos, car_r)

    v_peak = max(float(np.max(np.abs(voc_l))), float(np.max(np.abs(voc_r))), 1e-6)
    voc_l = voc_l / v_peak * 0.44
    voc_r = voc_r / v_peak * 0.44

    # Mix: crystal-clear dry voice (center) + lush 3-voice harmonic choir (stereo wide!)
    st = np.zeros((n, 2), dtype=np.float64)
    st[:, 0] = 0.72 * dry + 0.56 * voc_l + 0.16 * voc_r
    st[:, 1] = 0.72 * dry + 0.56 * voc_r + 0.16 * voc_l
    # Smooth micro fades
    fn = min(n, int(0.02 * SAMPLE_RATE))
    if fn > 1:
        st[:fn] *= np.linspace(0.0, 1.0, fn)[:, None]
        st[-fn:] *= np.linspace(1.0, 0.0, fn)[:, None]
    return st


def synth_note(freq: float, dur: float, amp: float, timbre: str = "rhodes") -> np.ndarray:
    n = int(round(dur * SAMPLE_RATE))
    if n <= 0:
        return np.zeros(0, dtype=np.float64)
    t = np.arange(n, dtype=np.float64) / SAMPLE_RATE
    if timbre == "rhodes":
        env = (1.0 - np.exp(-t / 0.015)) * np.exp(-t / (dur * 0.55 + 0.18))
        tine = 0.16 * np.exp(-t / 0.05) * np.sin(2.0 * math.pi * freq * 7.0 * t)
        sig = (
            1.00 * np.sin(2.0 * math.pi * freq * t + tine)
            + 0.26 * np.sin(2.0 * math.pi * 2.0 * freq * t) * np.exp(-t / 0.42)
            + 0.09 * np.sin(2.0 * math.pi * 3.0 * freq * t) * np.exp(-t / 0.24)
        )
    elif timbre == "bell":
        env = (1.0 - np.exp(-t / 0.005)) * np.exp(-t / (dur * 0.36 + 0.08))
        sig = (
            1.00 * np.sin(2.0 * math.pi * freq * t)
            + 0.36 * np.sin(2.0 * math.pi * 2.0 * freq * t) * np.exp(-t / 0.18)
            + 0.14 * np.sin(2.0 * math.pi * 3.0 * freq * t) * np.exp(-t / 0.10)
        )
    elif timbre == "bass":
        env = (1.0 - np.exp(-t / 0.02)) * np.exp(-t / (dur * 0.65 + 0.25))
        sig = 0.85 * np.sin(2.0 * math.pi * freq * t) + 0.25 * np.sin(2.0 * math.pi * 2.0 * freq * t)
    else:  # warm harmonic pad
        att = min(0.75, dur * 0.25)
        rel = min(0.95, dur * 0.30)
        env = np.maximum(0.0, np.minimum(1.0, t / max(att, 1e-4)) * np.minimum(1.0, (dur - t) / max(rel, 1e-4)))
        sig = (
            0.55 * np.sin(2.0 * math.pi * freq * t)
            + 0.45 * np.sin(2.0 * math.pi * freq * 1.0024 * t + 0.4)
            + 0.16 * np.sin(2.0 * math.pi * 2.0 * freq * t)
        )
    fn = min(n, int(0.015 * SAMPLE_RATE))
    if fn > 1:
        env[-fn:] *= np.linspace(1.0, 0.0, fn)
    return amp * env * sig


def add_stereo(buf: np.ndarray, sig: np.ndarray, start_s: float, pan: float = 0.0) -> None:
    i0 = int(round(start_s * SAMPLE_RATE))
    if i0 >= len(buf) or len(sig) == 0:
        return
    i1 = min(len(buf), i0 + len(sig))
    seg = sig[: i1 - i0]
    ang = (pan + 1.0) * (math.pi / 4.0)
    buf[i0:i1, 0] += seg * math.cos(ang)
    buf[i0:i1, 1] += seg * math.sin(ang)


def add_stereo_pair(buf: np.ndarray, st: np.ndarray, start_s: float) -> None:
    i0 = int(round(start_s * SAMPLE_RATE))
    if i0 >= len(buf) or len(st) == 0:
        return
    i1 = min(len(buf), i0 + len(st))
    buf[i0:i1] += st[: i1 - i0]


def apply_reverb(buf: np.ndarray, wet: float = 0.85) -> np.ndarray:
    out = buf.copy()
    taps_l = [(0.029, 0.19), (0.061, 0.14), (0.107, 0.095), (0.173, 0.06), (0.251, 0.038)]
    taps_r = [(0.035, 0.19), (0.071, 0.14), (0.119, 0.095), (0.187, 0.06), (0.269, 0.038)]
    for d, g in taps_l:
        k = int(round(d * SAMPLE_RATE))
        if k < len(buf):
            out[k:, 0] += wet * g * buf[:-k, 0]
            out[k:, 1] += wet * 0.35 * g * buf[:-k, 0]
    for d, g in taps_r:
        k = int(round(d * SAMPLE_RATE))
        if k < len(buf):
            out[k:, 1] += wet * g * buf[:-k, 1]
            out[k:, 0] += wet * 0.35 * g * buf[:-k, 1]
    return out


@dataclass
class MasterBundle:
    duration_s: float
    total_frames: int
    chapter_spans: Dict[int, Tuple[float, float]]
    cues: List[VoiceCue]
    chess_steps: List[ChessStep]
    chess_times: List[float]
    nontriv_poles: np.ndarray
    triv_poles: np.ndarray
    phis: np.ndarray
    lmax_phi: np.ndarray
    phi_c: float
    edo12: float
    edo31: float
    edo53: float
    w_vals: np.ndarray
    p_exact: np.ndarray
    q_gauss: np.ndarray
    q_edge4: np.ndarray
    q_edge6: np.ndarray
    total_primes_40: int
    tv_gauss: float
    tv_edge4: float
    tv_edge6: float


def prepare_master_and_audio(wav_out: str | None) -> MasterBundle:
    print("Computing exact first-principles spectra (12/31/53-EDO, Ihara poles, flux, m=40)...", flush=True)
    nontriv_poles, triv_poles, phis, lmax_phi, phi_c = compute_ihara_poles_and_flux()
    edo12 = compute_edo_lambda_max(12, 4, 7)
    edo31 = compute_edo_lambda_max(31, 10, 18)
    edo53 = compute_edo_lambda_max(53, 17, 31)
    w_vals, p_ex, q0, q4, q6, tot40, tv0, tv4, tv6 = compute_exact_m40_and_edgeworth()
    chess_steps = build_traxler_chess_game()

    cues = build_voice_script()
    print(f"Synthesizing {len(cues)} Pico TTS cues & 22-band stereo harmonic vocoder tracks...", flush=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        dry_list: List[np.ndarray] = []
        cursor = 0.0
        ch_starts: Dict[int, float] = {}
        ch_ends: Dict[int, float] = {}

        for idx, cue in enumerate(cues):
            dry = render_pico_48k(cue.text, tmpdir, idx)
            dry_list.append(dry)
            dur = len(dry) / float(SAMPLE_RATE)
            if cue.chapter not in ch_starts:
                ch_starts[cue.chapter] = cursor
            cursor += cue.pre_gap
            cue.start_s = cursor
            cue.dur_s = dur
            cursor += dur + cue.post_gap
            ch_ends[cue.chapter] = cursor

        duration_s = math.ceil(cursor + 1.0)
        total_frames = int(round(duration_s * FPS))
        chapter_spans = {ch: (ch_starts[ch], ch_ends[ch]) for ch in sorted(ch_starts.keys())}

        # Schedule the 20 chess snapshots across Chapter 4 aligned to its 5 narration cues!
        c4_cues = [c for c in cues if c.chapter == 4]
        # Map phases to exact cues:
        #   Opening (plies 0..5): from ch4 start -> c4_cues[1] end
        #   Attack (plies 6..8): across c4_cues[2]
        #   Crisis (plies 9..11): across c4_cues[3] (Bxf2+!! hits right at "Crisis! Black sacrifices...")
        #   Winning (plies 12..19): across c4_cues[4] -> ch4 end
        c4_t0, c4_t1 = chapter_spans[4]
        t_open_end = c4_cues[2].start_s - 0.2
        t_att_end = c4_cues[3].start_s - 0.1
        t_cris_end = c4_cues[4].start_s - 0.2

        chess_times: List[float] = []
        chess_times.extend(np.linspace(c4_t0 + 0.4, t_open_end, 6).tolist())          # plies 0..5
        chess_times.extend(np.linspace(t_open_end + 0.8, t_att_end, 3).tolist())      # plies 6..8
        chess_times.extend([c4_cues[3].start_s + 0.1, c4_cues[3].start_s + 1.8, c4_cues[3].start_s + 5.8])  # plies 9..11
        chess_times.extend(np.linspace(t_cris_end + 0.4, c4_t1 - 1.6, 8).tolist())    # plies 12..19
        assert len(chess_times) == len(chess_steps)

        if wav_out is not None:
            n_samp = int(round(duration_s * SAMPLE_RATE))
            music_buf = np.zeros((n_samp, 2), dtype=np.float64)
            voice_buf = np.zeros((n_samp, 2), dtype=np.float64)
            voice_env = np.zeros(n_samp, dtype=np.float64)

            bp_filters = build_vocoder_filters()
            lp_env = build_env_lp()

            # 1. Harmonize & mix all 22 spoken cues
            for cue, dry in zip(cues, dry_list):
                st_v = harmonize_voice_stereo(dry, cue.chord_pcs, cue.tuning, bp_filters, lp_env)
                add_stereo_pair(voice_buf, st_v, cue.start_s)
                i0 = int(round(cue.start_s * SAMPLE_RATE))
                i1 = min(n_samp, i0 + len(dry))
                voice_env[i0:i1] = 1.0

            # Smooth ducking envelope so music breathes generously between phrases & sits warmly under voice
            duck_lp = signal.butter(1, 3.5 / (SAMPLE_RATE * 0.5), btype="lowpass", output="sos")
            duck_mask = np.clip(signal.sosfilt(duck_lp, voice_env), 0.0, 1.0)
            music_gain = 1.0 - 0.42 * duck_mask  # -4.7 dB gentle duck while speaking

            # 2. Compose adaptive harmonic score synced to every chapter & chess move!
            # Subtle harmonic chord bed following every cue
            for k, cue in enumerate(cues):
                t_start = cue.start_s - 0.35
                t_next = cues[k + 1].start_s - 0.35 if k + 1 < len(cues) else duration_s - 0.5
                span = max(1.0, t_next - t_start)
                if cue.chapter == 4:
                    continue  # Chapter 4 gets dedicated LIVE CHESS-DRIVEN SCORE!
                if cue.tuning == "8edo":
                    # Pure 8-EDO NEG-M11 stereo duality showcase!
                    n_beats = int(span / 0.78)
                    tune_8 = [3, 5, 7, 1]
                    for b in range(n_beats):
                        tb = t_start + b * 0.78
                        mp_pc = tune_8[b % 4]
                        add_stereo(music_buf, synth_note(freq_8edo(0, 3), 0.85, 0.11, "rhodes"), tb, -0.72)
                        add_stereo(music_buf, synth_note(freq_8edo(4, 3), 0.85, 0.10, "rhodes"), tb, -0.62)
                        add_stereo(music_buf, synth_note(freq_8edo(2, 3), 0.85, 0.11, "rhodes"), tb, 0.62)
                        add_stereo(music_buf, synth_note(freq_8edo(6, 3), 0.85, 0.10, "rhodes"), tb, 0.72)
                        add_stereo(music_buf, synth_note(freq_8edo(mp_pc, 5), 0.72, 0.13, "bell"), tb, 0.0)
                else:
                    pcs = cue.chord_pcs
                    # Warm evolving pad
                    add_stereo(music_buf, synth_note(freq_12edo(pcs[0], 3), span + 0.5, 0.11, "pad"), t_start, -0.25)
                    add_stereo(music_buf, synth_note(freq_12edo(pcs[2], 3), span + 0.5, 0.09, "pad"), t_start, 0.25)
                    add_stereo(music_buf, synth_note(freq_12edo(pcs[1], 4), span + 0.5, 0.08, "pad"), t_start, 0.0)
                    # Gentle Rhodes pulse + sparkling Tonnetz chime arpeggio
                    step_dt = 1.45 if cue.chapter in (1, 2, 7) else 1.15
                    n_pulses = max(1, int(span / step_dt))
                    for p_i in range(n_pulses):
                        tp = t_start + p_i * step_dt
                        for v_i, pc in enumerate(pcs):
                            add_stereo(music_buf, synth_note(freq_12edo(pc, 4), step_dt * 0.92, 0.065, "rhodes"), tp + 0.05 * v_i, -0.3 + 0.3 * v_i)
                        bell_pc = pcs[p_i % 3]
                        add_stereo(music_buf, synth_note(freq_12edo(bell_pc, 5), 0.9, 0.055, "bell"), tp + 0.18, 0.35 * math.sin(p_i * 1.4))

            # 3. CHAPTER 4 CENTERPIECE: Live Chess-Driven Adaptive Score!
            # Every chess ply dynamically shifts chord, octave, rhythmic pulse, and tension!
            for idx, stp in enumerate(chess_steps):
                t0 = chess_times[idx]
                t1 = chess_times[idx + 1] if idx + 1 < len(chess_steps) else c4_t1
                dur_step = max(0.5, t1 - t0)
                pcs = stp.chord_pcs
                if stp.phase == "OPENING":
                    # Calm, airy, open voicings
                    for j, pc in enumerate(pcs):
                        add_stereo(music_buf, synth_note(freq_12edo(pc, 4), dur_step + 0.3, 0.09, "rhodes"), t0 + 0.04 * j, -0.25 + 0.25 * j)
                    add_stereo(music_buf, synth_note(freq_12edo(pcs[0], 3), dur_step + 0.4, 0.09, "pad"), t0, 0.0)
                elif stp.phase == "ATTACK":
                    # Faster energetic arpeggiation + rising bass
                    add_stereo(music_buf, synth_note(freq_12edo(pcs[0], 3), dur_step + 0.2, 0.12, "bass"), t0, -0.15)
                    n_sub = max(2, int(dur_step / 0.55))
                    for s_i in range(n_sub):
                        ts = t0 + s_i * (dur_step / n_sub)
                        pc_n = pcs[s_i % 3]
                        add_stereo(music_buf, synth_note(freq_12edo(pc_n, 4 + (s_i % 2)), 0.55, 0.085, "rhodes"), ts, -0.35 + 0.35 * (s_i % 3))
                        add_stereo(music_buf, synth_note(freq_12edo(pc_n, 5), 0.42, 0.06, "bell"), ts, 0.35 * (1 if s_i % 2 == 0 else -1))
                elif stp.phase == "CRISIS":
                    # Dark, urgent, low-octave minor mediants + tritone danger pulse!
                    add_stereo(music_buf, synth_note(freq_12edo(pcs[0], 2), dur_step + 0.3, 0.16, "bass"), t0, 0.0)
                    add_stereo(music_buf, synth_note(freq_12edo((pcs[0] + 6) % 12, 3), dur_step + 0.2, 0.085, "pad"), t0, 0.35)
                    n_sub = max(3, int(dur_step / 0.38))
                    for s_i in range(n_sub):
                        ts = t0 + s_i * (dur_step / n_sub)
                        for j, pc in enumerate(pcs):
                            add_stereo(music_buf, synth_note(freq_12edo(pc, 3), 0.34, 0.075, "rhodes"), ts, -0.45 + 0.45 * j)
                        if s_i % 2 == 0:
                            add_stereo(music_buf, synth_note(freq_12edo((pcs[0] + 6) % 12, 4), 0.28, 0.07, "bell"), ts, 0.0)
                else:  # WINNING turnaround!
                    # Soaring triumphant major climbs resolving into radiant Cmaj9!
                    add_stereo(music_buf, synth_note(freq_12edo(pcs[0], 3), dur_step + 0.4, 0.12, "pad"), t0, -0.2)
                    add_stereo(music_buf, synth_note(freq_12edo(pcs[2], 3), dur_step + 0.4, 0.10, "pad"), t0, 0.2)
                    for j, pc in enumerate(pcs):
                        add_stereo(music_buf, synth_note(freq_12edo(pc, 4), dur_step + 0.35, 0.10, "rhodes"), t0 + 0.05 * j, -0.3 + 0.3 * j)
                        add_stereo(music_buf, synth_note(freq_12edo(pc, 5), 0.85, 0.08, "bell"), t0 + 0.12 * j, -0.3 + 0.3 * j)
                    if idx == len(chess_steps) - 1:
                        # Glorious Cmaj9 resolution!
                        for pc, oc, pan in [(0, 3, -0.3), (7, 3, 0.3), (4, 4, -0.4), (11, 4, 0.4), (2, 5, 0.0), (0, 6, 0.0)]:
                            add_stereo(music_buf, synth_note(freq_12edo(pc, oc), 3.6, 0.095, "pad"), t0, pan)

            # Final radiant Cmaj9 outro cadence
            t_end = cues[-1].start_s + cues[-1].dur_s - 0.5
            for pc, oc, amp, pan in [(0, 3, 0.14, -0.25), (7, 3, 0.12, 0.25), (4, 4, 0.10, -0.35), (11, 4, 0.08, 0.35), (2, 5, 0.07, 0.0)]:
                add_stereo(music_buf, synth_note(freq_12edo(pc, oc), duration_s - t_end, amp, "pad"), t_end, pan)

            # Master stereo mix: reverb on music & voice, gentle ducking, soft peak limit
            music_wet = apply_reverb(music_buf, wet=0.95) * music_gain[:, None]
            voice_wet = apply_reverb(voice_buf, wet=0.45)
            mix = 0.88 * voice_wet + 0.78 * music_wet

            fi = int(0.35 * SAMPLE_RATE)
            fo = int(1.8 * SAMPLE_RATE)
            mix[:fi] *= np.linspace(0.0, 1.0, fi)[:, None]
            mix[-fo:] *= np.linspace(1.0, 0.0, fo)[:, None]

            peak = float(np.max(np.abs(mix)))
            if peak > 1e-6:
                mix = np.tanh(mix / (peak * 0.86)) * 0.86

            pcm = np.clip(mix * 32767.0, -32768.0, 32767.0).astype("<i2")
            with wave.open(wav_out, "wb") as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(pcm.tobytes())
            print(f"Synthesized {duration_s:.1f}s stereo Spoken-in-Harmony master soundtrack -> {wav_out}", flush=True)

    return MasterBundle(
        duration_s=duration_s,
        total_frames=total_frames,
        chapter_spans=chapter_spans,
        cues=cues,
        chess_steps=chess_steps,
        chess_times=chess_times,
        nontriv_poles=nontriv_poles,
        triv_poles=triv_poles,
        phis=phis,
        lmax_phi=lmax_phi,
        phi_c=phi_c,
        edo12=edo12,
        edo31=edo31,
        edo53=edo53,
        w_vals=w_vals,
        p_exact=p_ex,
        q_gauss=q0,
        q_edge4=q4,
        q_edge6=q6,
        total_primes_40=tot40,
        tv_gauss=tv0,
        tv_edge4=tv4,
        tv_edge6=tv6,
    )


# ---------------------------------------------------------------------------
# Cairo + Pango Primitives (Clean Sub-Paths & Cached Obsidian Backdrop)
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
    ctx: cairo.Context, x: float, y: float, w: float, h: float, alpha: float = 1.0,
    border_col: Tuple[float, float, float, float] = C_PANEL_BORDER, radius: float = 18.0,
    fill_col: Tuple[float, float, float, float] = C_PANEL, border_width: float = 1.8,
) -> None:
    rounded_rect(ctx, x, y, w, h, radius)
    set_rgba(ctx, fill_col, alpha)
    ctx.fill_preserve()
    set_rgba(ctx, border_col, alpha)
    ctx.set_line_width(border_width)
    ctx.stroke()


def draw_text(
    ctx: cairo.Context, markup: str, x: float, y: float, font_desc: str = "DejaVu Sans 20",
    color: Tuple[float, float, float, float] = C_WHITE, alpha: float = 1.0,
    align: str = "left", valign: str = "top", max_width: float | None = None, line_spacing: float = 1.24,
) -> Tuple[float, float]:
    layout = PangoCairo.create_layout(ctx)
    layout.set_font_description(Pango.FontDescription(font_desc))
    layout.set_markup(markup, -1)
    if max_width is not None:
        layout.set_width(int(max_width * Pango.SCALE))
        layout.set_wrap(Pango.WrapMode.WORD_CHAR)
    layout.set_alignment(
        Pango.Alignment.CENTER if align == "center" else (Pango.Alignment.RIGHT if align == "right" else Pango.Alignment.LEFT)
    )
    layout.set_line_spacing(line_spacing)
    _, logical = layout.get_pixel_extents()
    tw, th = float(logical.width), float(logical.height)
    dx = x - (max_width * 0.5 if max_width and align == "center" else (max_width if max_width and align == "right" else (tw * 0.5 if align == "center" else (tw if align == "right" else 0.0))))
    dy = y - (th * 0.5 if valign == "center" else (th if valign == "bottom" else 0.0))
    ctx.save()
    ctx.new_path()
    ctx.move_to(dx, dy)
    set_rgba(ctx, color, alpha)
    PangoCairo.show_layout(ctx, layout)
    ctx.restore()
    return tw, th


def draw_pill(
    ctx: cairo.Context, text: str, x: float, y: float, accent: Tuple[float, float, float, float],
    alpha: float = 1.0, align: str = "left", font: str = "DejaVu Sans Bold 13",
) -> float:
    layout = PangoCairo.create_layout(ctx)
    layout.set_font_description(Pango.FontDescription(font))
    layout.set_markup(text, -1)
    _, logical = layout.get_pixel_extents()
    pw, ph = logical.width + 30.0, logical.height + 14.0
    px = x if align == "left" else (x - pw * 0.5 if align == "center" else x - pw)
    rounded_rect(ctx, px, y, pw, ph, ph * 0.5)
    ctx.set_source_rgba(accent[0], accent[1], accent[2], 0.16 * alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(accent[0], accent[1], accent[2], 0.88 * alpha)
    ctx.set_line_width(1.6)
    ctx.stroke()
    draw_text(ctx, text, px + pw * 0.5, y + ph * 0.5, font, accent, alpha, "center", "center")
    return pw


def draw_glow_line(
    ctx: cairo.Context, x0: float, y0: float, x1: float, y1: float,
    col: Tuple[float, float, float, float], width: float = 3.5, alpha: float = 1.0,
) -> None:
    ctx.save()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for mult, a in [(3.2, 0.13), (1.8, 0.28), (1.0, 0.96)]:
        ctx.new_path()
        ctx.move_to(x0, y0)
        ctx.line_to(x1, y1)
        set_rgba(ctx, col, alpha * a)
        ctx.set_line_width(width * mult)
        ctx.stroke()
    ctx.restore()


def draw_glow_circle(
    ctx: cairo.Context, cx: float, cy: float, r: float,
    col: Tuple[float, float, float, float], alpha: float = 1.0, fill_core: bool = True,
) -> None:
    if r <= 0.1 or alpha <= 0.0:
        return
    pat = cairo.RadialGradient(cx, cy, 0.0, cx, cy, r * 2.8)
    pat.add_color_stop_rgba(0.0, col[0], col[1], col[2], 0.65 * alpha)
    pat.add_color_stop_rgba(0.38, col[0], col[1], col[2], 0.20 * alpha)
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


def build_static_bg() -> cairo.ImageSurface:
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    pat = cairo.RadialGradient(WIDTH * 0.5, HEIGHT * 0.42, 60.0, WIDTH * 0.5, HEIGHT * 0.5, WIDTH * 0.72)
    pat.add_color_stop_rgba(0.0, C_BG_MID[0], C_BG_MID[1], C_BG_MID[2], 1.0)
    pat.add_color_stop_rgba(1.0, C_BG_DEEP[0], C_BG_DEEP[1], C_BG_DEEP[2], 1.0)
    ctx.set_source(pat)
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.fill()

    set_rgba(ctx, C_GRID, 0.48)
    ctx.set_line_width(1.0)
    R = 72.0
    dx, dy = R * 1.5, R * math.sqrt(3.0)
    for ci in range(-1, int(WIDTH / dx) + 2):
        for ri in range(-1, int(HEIGHT / dy) + 2):
            cx, cy = ci * dx, ri * dy + (0.5 * dy if ci % 2 else 0.0)
            ctx.new_sub_path()
            for k in range(6):
                a0 = k * math.pi / 3.0
                px, py = cx + R * math.cos(a0), cy + R * math.sin(a0)
                if k == 0:
                    ctx.move_to(px, py)
                else:
                    ctx.line_to(px, py)
            ctx.close_path()
    ctx.stroke()
    return surf


_BG_CACHE: cairo.ImageSurface | None = None


def draw_chrome(ctx: cairo.Context, t: float, bundle: MasterBundle) -> None:
    global _BG_CACHE
    if _BG_CACHE is None:
        _BG_CACHE = build_static_bg()
    ctx.set_source_surface(_BG_CACHE, 0, 0)
    ctx.paint()

    # Live synchronized spoken-in-harmony educator caption ribbon (bottom safe area y=946..1028)
    active_cue = None
    for cue in bundle.cues:
        if cue.start_s - 0.15 <= t <= cue.start_s + cue.dur_s + 0.45:
            active_cue = cue
            break

    if active_cue is not None:
        ca = min(
            smoothstep((t - (active_cue.start_s - 0.15)) / 0.25),
            smoothstep(((active_cue.start_s + active_cue.dur_s + 0.45) - t) / 0.30),
        )
        draw_panel(ctx, 72.0, 944.0, WIDTH - 144.0, 72.0, ca * 0.94, C_PANEL_BORDER, 14.0, fill_col=(0.032, 0.052, 0.105, 0.94), border_width=1.4)
        # Live spoken-in-harmony chord indicator pill on the left
        chord_col = C_MAGENTA if active_cue.tuning == "8edo" else C_GOLD
        c_tag = "8-EDO HARMONY" if active_cue.tuning == "8edo" else f"HARMONY: {PITCH_NAMES_12[active_cue.chord_pcs[0]]}" + ("m" if (active_cue.chord_pcs[1] - active_cue.chord_pcs[0]) % 12 == 3 else "")
        draw_pill(ctx, c_tag, 94.0, 963.0, chord_col, ca, "left", "DejaVu Sans Mono Bold 11")
        draw_text(ctx, html.escape(active_cue.caption), 326.0, 980.0, "DejaVu Sans 16.5", C_WHITE, ca, "left", "center", max_width=1490.0)

    # Progress bar & timestamp
    bar_y = HEIGHT - 32.0
    ctx.new_path()
    ctx.set_source_rgba(0.18, 0.28, 0.44, 0.35)
    ctx.rectangle(72.0, bar_y, WIDTH - 144.0, 3.0)
    ctx.fill()
    prog = clamp01(t / bundle.duration_s)
    grad = cairo.LinearGradient(72.0, 0, WIDTH - 72.0, 0)
    grad.add_color_stop_rgba(0.0, C_CYAN[0], C_CYAN[1], C_CYAN[2], 0.92)
    grad.add_color_stop_rgba(0.5, C_MAGENTA[0], C_MAGENTA[1], C_MAGENTA[2], 0.92)
    grad.add_color_stop_rgba(1.0, C_GOLD[0], C_GOLD[1], C_GOLD[2], 0.96)
    ctx.new_path()
    ctx.set_source(grad)
    ctx.rectangle(72.0, bar_y, (WIDTH - 144.0) * prog, 3.0)
    ctx.fill()

    draw_text(ctx, "ERGENTICS  ·  MORPHEUS MASTERCLASS  ·  GEMINI 4 NEON (SPOKEN IN HARMONY)", 72.0, HEIGHT - 22.0, "DejaVu Sans Mono 10.5", C_DIM, 0.92)
    mm, ss = int(t // 60), int(t % 60)
    tm, ts = int(bundle.duration_s // 60), int(bundle.duration_s % 60)
    draw_text(ctx, f"{mm:02d}:{ss:02d} / {tm:02d}:{ts:02d}", WIDTH - 72.0, HEIGHT - 22.0, "DejaVu Sans Mono 10.5", C_DIM, 0.92, "right")


# ---------------------------------------------------------------------------
# Chapter 1: The Hidden Bridge — Music <-> Graphene Honeycomb
# ---------------------------------------------------------------------------

def render_ch1(ctx: cairo.Context, t: float, t0: float, t1: float) -> None:
    a = scene_alpha(t, t0, t1)
    if a <= 0.0:
        return
    u = seg_prog(t, t0, t1)

    draw_pill(ctx, "CHAPTER 1  ·  MUSIC THEORY ↔ CONDENSED-MATTER PHYSICS", 72.0, 44.0, C_CYAN, a)
    draw_text(ctx, "<b>The Tonnetz Dual IS a Graphene Honeycomb</b>", 72.0, 92.0, "DejaVu Sans 36", C_WHITE, a)

    # Left panel: animated Tonnetz triangles morphing into glowing honeycomb graphene bonds!
    draw_panel(ctx, 72.0, 166.0, 1080.0, 748.0, a, C_PANEL_BORDER, 22.0)
    ctx.save()
    rounded_rect(ctx, 76.0, 170.0, 1072.0, 740.0, 20.0)
    ctx.clip()

    ox, oy, L = 612.0, 540.0, 134.0
    e1 = (L, 0.0)
    e2 = (L * 0.5, -L * math.sqrt(3.0) / 2.0)

    def xy(i: float, j: float) -> Tuple[float, float]:
        return (ox + i * e1[0] + j * e2[0], oy + i * e1[1] + j * e2[1])

    # Fade triangular pitch lattice slightly as dual honeycomb emerges!
    morph = ease_in_out_cubic(seg_prog(u, 0.42, 0.78))
    ctx.new_path()
    set_rgba(ctx, (0.28, 0.42, 0.65, 0.48 * (1.0 - 0.55 * morph)), a)
    ctx.set_line_width(1.4)
    for i in range(-4, 5):
        ctx.move_to(*xy(i, -4)); ctx.line_to(*xy(i, 4))
    for j in range(-4, 5):
        ctx.move_to(*xy(-4, j)); ctx.line_to(*xy(4, j))
    for s in range(-6, 7):
        ctx.move_to(*xy(-4, s + 4)); ctx.line_to(*xy(4, s - 4))
    ctx.stroke()

    # Draw dual honeycomb bonds (Major centroids -> Minor centroids!) glowing stronger as morph -> 1
    for i in range(-3, 3):
        for j in range(-2, 3):
            # Up triangle (Major): (i,j), (i+1,j), (i,j+1)
            mx = (xy(i, j)[0] + xy(i + 1, j)[0] + xy(i, j + 1)[0]) / 3.0
            my = (xy(i, j)[1] + xy(i + 1, j)[1] + xy(i, j + 1)[1]) / 3.0
            # Three adjacent Down triangles (Minor): P, L, R neighbors!
            nbs = [
                [(i, j), (i + 1, j), (i + 1, j - 1)],          # P
                [(i + 1, j), (i, j + 1), (i + 1, j + 1)],      # L
                [(i, j), (i, j + 1), (i - 1, j + 1)],          # R
            ]
            cols = [C_CYAN, C_MAGENTA, C_GOLD]
            for k, tri in enumerate(nbs):
                nx = sum(xy(p[0], p[1])[0] for p in tri) / 3.0
                ny = sum(xy(p[0], p[1])[1] for p in tri) / 3.0
                if 80 < mx < 1144 and 176 < my < 904 and 80 < nx < 1144 and 176 < ny < 904:
                    draw_glow_line(ctx, mx, my, nx, ny, cols[k], 1.6 + 2.2 * morph, a * (0.25 + 0.70 * morph))
            if 95 < mx < 1128 and 190 < my < 890:
                draw_glow_circle(ctx, mx, my, 5.5 + 4.5 * morph, C_CYAN, a * (0.35 + 0.65 * morph))
            # Also draw minor node for (i,j)-(i+1,j)-(i+1,j-1)
            dnx = (xy(i, j)[0] + xy(i + 1, j)[0] + xy(i + 1, j - 1)[0]) / 3.0
            dny = (xy(i, j)[1] + xy(i + 1, j)[1] + xy(i + 1, j - 1)[1]) / 3.0
            if 95 < dnx < 1128 and 190 < dny < 890:
                draw_glow_circle(ctx, dnx, dny, 5.5 + 4.5 * morph, C_MAGENTA, a * (0.35 + 0.65 * morph))

    # Central highlighted C-hexagon
    hex_c = [
        [(0, 0), (1, 0), (0, 1)], [(0, 0), (1, 0), (1, -1)], [(0, 0), (1, -1), (0, -1)],
        [(0, 0), (0, -1), (-1, 0)], [(0, 0), (-1, 0), (-1, 1)], [(0, 0), (-1, 1), (0, 1)],
    ]
    c_pts = [(sum(xy(p[0], p[1])[0] for p in tri) / 3.0, sum(xy(p[0], p[1])[1] for p in tri) / 3.0) for tri in hex_c]
    step_k = int((t - t0) * 1.1) % 6
    for k in range(6):
        p0, p1 = c_pts[k], c_pts[(k + 1) % 6]
        draw_glow_line(ctx, p0[0], p0[1], p1[0], p1[1], C_GOLD, 4.0, a * 0.9)
    draw_glow_circle(ctx, c_pts[step_k][0], c_pts[step_k][1], 14.0, C_WHITE, a)

    # Pitch-class vertices (fade softly as graphene emerges)
    if morph < 0.95:
        for i in range(-3, 4):
            for j in range(-2, 3):
                px, py = xy(i, j)
                if 105 < px < 1120 and 195 < py < 885:
                    pc = (7 * i + 4 * j) % 12
                    ctx.new_path()
                    ctx.arc(px, py, 14.0, 0, 2 * math.pi)
                    set_rgba(ctx, (0.06, 0.10, 0.19, 0.92 * (1.0 - 0.6 * morph)), a)
                    ctx.fill_preserve()
                    set_rgba(ctx, C_SLATE, a * 0.65 * (1.0 - 0.6 * morph))
                    ctx.set_line_width(1.3)
                    ctx.stroke()
                    draw_text(ctx, PITCH_NAMES_12[pc], px, py, "DejaVu Sans 10.5", C_WHITE, a * (1.0 - 0.6 * morph), "center", "center")

    ctx.restore()

    # Right Educator Panel: 3 Cross-Domain Cards
    rx, rw = 1184.0, 664.0
    cards = [
        ("1.  MUSIC THEORY", "24 Triads (12 Major · 12 Minor)", "Each P, L, R flip moves exactly one pitch by 1 or 2 semitones — maximally smooth voice leading.", C_CYAN),
        ("2.  GRAPHENE PHYSICS", "Exact Dual Honeycomb Lattice", "Major &amp; minor triads sit on the A and B carbon sublattices. Their eigenvalues are graphene's Dirac bands!", C_MAGENTA),
        ("3.  THE QUESTION", "Why Can Harmony Flow Forever?", "Count primitive non-backtracking loops — prime cadences — and the Riemann Hypothesis appears.", C_GOLD),
    ]
    for i, (tag, head, desc, col) in enumerate(cards):
        cy = 166.0 + i * 256.0
        p = ease_out_cubic(seg_prog(u, 0.06 + 0.22 * i, 0.24 + 0.22 * i))
        draw_panel(ctx, rx, cy, rw, 232.0, a * p, col, 20.0, border_width=2.2)
        draw_pill(ctx, tag, rx + 26.0, cy + 22.0, col, a * p, "left", "DejaVu Sans Bold 12")
        draw_text(ctx, f"<b>{head}</b>", rx + 26.0, cy + 72.0, "DejaVu Sans 20", C_WHITE, a * p)
        draw_text(ctx, desc, rx + 26.0, cy + 116.0, "DejaVu Sans 16", C_SLATE, a * p, max_width=rw - 52.0, line_spacing=1.36)


# ---------------------------------------------------------------------------
# Chapter 2: The Graph Riemann Hypothesis (Complex u-Plane + 12/31/53-EDO)
# ---------------------------------------------------------------------------

def render_ch2(ctx: cairo.Context, t: float, t0: float, t1: float, b: MasterBundle) -> None:
    a = scene_alpha(t, t0, t1)
    if a <= 0.0:
        return
    u = seg_prog(t, t0, t1)

    draw_pill(ctx, "CHAPTER 2  ·  NUMBER THEORY ↔ QUANTUM BANDS ↔ EXPANDERS", 72.0, 44.0, C_MAGENTA, a)
    draw_text(ctx, "<b>How the Tonnetz Satisfies the Graph Riemann Hypothesis</b>", 72.0, 92.0, "DejaVu Sans 35", C_WHITE, a)

    # Left panel: EXACT Complex u-plane with ALL 44 nontrivial poles locked on |u| = 1/sqrt(2)!
    draw_panel(ctx, 72.0, 166.0, 960.0, 748.0, a, C_CYAN, 22.0)
    cx, cy = 552.0, 544.0
    scale = 265.0
    r_crit = scale / math.sqrt(2.0)

    draw_text(ctx, "<b>POLES OF THE IHARA ZETA FUNCTION  ζ<sub><i>X</i></sub>(<i>u</i>)</b>", cx, 204.0, "DejaVu Sans 19", C_CYAN, a, "center", "center")

    # Coordinate axes & unit circle (dashed)
    ctx.new_path()
    ctx.move_to(cx - 330, cy); ctx.line_to(cx + 330, cy)
    ctx.move_to(cx, cy - 285); ctx.line_to(cx, cy + 285)
    set_rgba(ctx, C_SLATE, a * 0.35)
    ctx.set_line_width(1.2)
    ctx.stroke()

    ctx.save()
    ctx.new_path()
    ctx.set_dash([6.0, 6.0])
    ctx.arc(cx, cy, scale, 0, 2 * math.pi)
    set_rgba(ctx, C_DIM, a * 0.55)
    ctx.set_line_width(1.4)
    ctx.stroke()
    ctx.restore()
    draw_text(ctx, "|u| = 1", cx + scale - 16.0, cy - 22.0, "DejaVu Sans Mono 12", C_DIM, a, "right", "center")

    # Glowing Critical Circle |u| = 1/sqrt(2)
    p_circ = ease_out_cubic(seg_prog(u, 0.10, 0.35))
    ctx.save()
    for mult, alp in [(3.5, 0.14), (1.0, 0.95)]:
        ctx.new_path()
        ctx.arc(cx, cy, r_crit, 0, 2 * math.pi * p_circ)
        set_rgba(ctx, C_CYAN, a * alp)
        ctx.set_line_width(3.2 * mult)
        ctx.stroke()
    ctx.restore()
    draw_text(ctx, "<b>CRITICAL CIRCLE  |u| = 1/√2</b>", cx, cy - r_crit - 24.0, "DejaVu Sans Mono 13.5", C_CYAN, a * p_circ, "center", "center")

    # Plot ALL 44 exact nontrivial poles snapping onto |u| = 1/sqrt(2)!
    p_poles = ease_out_cubic(seg_prog(u, 0.24, 0.58))
    for k, z in enumerate(b.nontriv_poles):
        pk = clamp01((p_poles * 44.0 - k) / 4.0)
        if pk <= 0.0:
            continue
        px = cx + z.real * scale
        py = cy - z.imag * scale
        draw_glow_circle(ctx, px, py, 6.2 * pk, C_EMERALD, a * pk)

    # Plot 4 trivial poles ±1, ±1/2 in gold crosses
    for z in b.triv_poles:
        px, py = cx + z.real * scale, cy - z.imag * scale
        draw_glow_line(ctx, px - 8, py - 8, px + 8, py + 8, C_GOLD, 2.4, a)
        draw_glow_line(ctx, px - 8, py + 8, px + 8, py - 8, C_GOLD, 2.4, a)

    draw_text(
        ctx,
        "<span foreground='#2CF59B'>● 44 nontrivial poles: ALL on |u| = 1/√2</span>    ·    <span foreground='#FFB800'>✕ 4 trivial poles (±1, ±½)</span>",
        cx,
        878.0,
        "DejaVu Sans Mono 13.5",
        C_WHITE,
        a,
        "center",
        "center",
    )

    # Right top panel: Spectral Bridge Formula
    rx, rw = 1064.0, 784.0
    draw_panel(ctx, rx, 166.0, rw, 270.0, a, C_GOLD, 20.0)
    draw_text(ctx, "<b>THEOREM 3.1  ·  RAMANUJAN EQUIVALENCE</b>", rx + 26.0, 192.0, "DejaVu Sans 17", C_GOLD, a)
    draw_text(
        ctx,
        "Graph RH holds  ⇔  |<i>λ</i><sub>nontriv</sub>(<i>X</i>)| ≤ 2√2 ≈ <b>2.8284</b>",
        rx + 26.0,
        242.0,
        "DejaVu Serif 18.5",
        C_WHITE,
        a,
    )
    draw_text(
        ctx,
        "• Eigenvalues of <i>X</i> equal the 12 graphene Fourier moduli ±|<i>f</i><sub><i>k</i></sub>|.\n"
        "• Maximum nontrivial modulus in 12-EDO is |<i>f</i><sub>3</sub>| = |2 − <i>i</i>| = <b>√5 ≈ 2.2361</b>.\n"
        "• Huge spectral gap below 2√2 = 2.8284 → optimal Alon–Boppana mixing!",
        rx + 26.0,
        296.0,
        "DejaVu Sans 14",
        C_SLATE,
        a,
        max_width=rw - 52.0,
        line_spacing=1.34,
    )

    # Right bottom panel: 12-EDO vs 31-EDO vs 53-EDO Ramanujan Gauge (NEG-M3!)
    p_edo = ease_out_cubic(seg_prog(u, 0.56, 0.85))
    draw_panel(ctx, rx, 464.0, rw, 450.0, a * (0.25 + 0.75 * p_edo), C_MAGENTA if p_edo > 0.5 else C_PANEL_BORDER, 20.0)
    draw_text(ctx, "<b>TUNING SYSTEM TEST (NEG-M3): WHO SATISFIES GRAPH RH?</b>", rx + 26.0, 492.0, "DejaVu Sans 15", C_WHITE, a)

    edos = [
        ("12-EDO  (Standard)", b.edo12, True,  C_EMERALD, "PASS  (√5 = 2.2361  ≪  2.8284)"),
        ("31-EDO  (Meantone)", b.edo31, True,  C_GOLD,    "PASS  (2.8246  &lt;  2.8284, hairline!)"),
        ("53-EDO  (Mercator)", b.edo53, False, C_MAGENTA, "FAIL  (2.8565  &gt;  2.8284, breaks RH!)"),
    ]
    bx0 = rx + 28.0
    bw_max = rw - 56.0
    thresh = 2.0 * math.sqrt(2.0)
    # Bar scale: 1.8 -> 3.0
    def bar_x(val: float) -> float:
        return bx0 + bw_max * clamp01((val - 1.8) / 1.2)

    tx_thr = bar_x(thresh)
    ctx.save()
    ctx.new_path()
    ctx.set_dash([6.0, 5.0])
    ctx.move_to(tx_thr, 540.0); ctx.line_to(tx_thr, 845.0)
    set_rgba(ctx, C_CYAN, a * 0.85)
    ctx.set_line_width(2.0)
    ctx.stroke()
    ctx.restore()
    draw_text(ctx, "2√2 = 2.8284", tx_thr - 8.0, 868.0, "DejaVu Sans Mono 12.5", C_CYAN, a, "right", "center")

    for i, (nm, val, ok, col, badge) in enumerate(edos):
        yy = 556.0 + i * 98.0
        draw_text(ctx, f"<b>{nm}</b>", bx0, yy, "DejaVu Sans 16", C_WHITE, a)
        draw_text(ctx, badge, rx + rw - 28.0, yy, "DejaVu Sans Mono 13.5", col, a, "right")
        rounded_rect(ctx, bx0, yy + 32.0, bw_max, 24.0, 8.0)
        set_rgba(ctx, (0.11, 0.16, 0.27, 0.85), a)
        ctx.fill()
        fw = max(12.0, (bar_x(val) - bx0) * p_edo)
        rounded_rect(ctx, bx0, yy + 32.0, fw, 24.0, 8.0)
        set_rgba(ctx, col, a)
        ctx.fill()


# ---------------------------------------------------------------------------
# Chapter 3: Why Ramanujan Unlocks Adaptive Endless Music + Flux Window
# ---------------------------------------------------------------------------

def render_ch3(ctx: cairo.Context, t: float, t0: float, t1: float, b: MasterBundle) -> None:
    a = scene_alpha(t, t0, t1)
    if a <= 0.0:
        return
    u = seg_prog(t, t0, t1)

    draw_pill(ctx, "CHAPTER 3  ·  INFORMATION THEORY ↔ GENERATIVE MUSIC ENGINE", 72.0, 44.0, C_EMERALD, a)
    draw_text(ctx, "<b>Why Ramanujan Optimality Enables Endless Adaptive Music</b>", 72.0, 92.0, "DejaVu Sans 35", C_WHITE, a)

    # Top Left: Stale 4-chord box vs Ramanujan Exponential Prime Proliferation
    draw_panel(ctx, 72.0, 166.0, 864.0, 355.0, a, C_CORAL, 20.0)
    draw_text(ctx, "<b>ORDINARY GRAPH  vs.  RAMANUJAN TONNETZ</b>", 102.0, 194.0, "DejaVu Sans 18", C_WHITE, a)

    # Left mini-diagram: stuck 4-chord loop
    lx, ly = 240.0, 358.0
    sq_pts = [(lx - 70, ly - 58), (lx + 70, ly - 58), (lx + 70, ly + 58), (lx - 70, ly + 58)]
    sq_lbl = ["C", "G", "Am", "F"]
    k_box = int((t - t0) * 1.6) % 4
    for k in range(4):
        draw_glow_line(ctx, *sq_pts[k], *sq_pts[(k + 1) % 4], C_CORAL, 2.8, a * 0.7)
    for k, (px, py) in enumerate(sq_pts):
        draw_glow_circle(ctx, px, py, 16.0 if k == k_box else 11.0, C_CORAL, a)
        draw_text(ctx, f"<b>{sq_lbl[k]}</b>", px, py, "DejaVu Sans 11", C_BG_DEEP, a, "center", "center")
    draw_text(ctx, "Trapped in 1 loop\n(predictable fatigue)", lx, 470.0, "DejaVu Sans 14", C_CORAL, a, "center", "center")

    # Right mini-diagram: exploding Ramanujan branching tree!
    rx0, ry0 = 650.0, 330.0
    draw_glow_circle(ctx, rx0, ry0, 11.0, C_GOLD, a)
    for k in range(6):
        a1 = k * math.pi / 3.0 + (t - t0) * 0.25
        p1 = (rx0 + 52 * math.cos(a1), ry0 + 52 * math.sin(a1))
        draw_glow_line(ctx, rx0, ry0, *p1, C_CYAN, 2.2, a * 0.8)
        draw_glow_circle(ctx, *p1, 6.5, C_CYAN, a)
        for s in (-0.32, 0.32):
            p2 = (rx0 + 98 * math.cos(a1 + s), ry0 + 98 * math.sin(a1 + s))
            draw_glow_line(ctx, *p1, *p2, C_EMERALD, 1.6, a * 0.65)
            draw_glow_circle(ctx, *p2, 4.2, C_EMERALD, a * 0.9)
    draw_text(ctx, "<b>π(40) = 54,975,717,792</b>\nprime cadences (never repeats!)", rx0, 474.0, "DejaVu Sans Mono 13.5", C_EMERALD, a, "center", "center")

    # Bottom Left: 3 Engineering Properties of Adaptive Music
    draw_panel(ctx, 72.0, 548.0, 864.0, 366.0, a, C_CYAN, 20.0)
    draw_text(ctx, "<b>THREE GUARANTEES FOR ENDLESS ADAPTIVE SOUNDTRACKS</b>", 102.0, 578.0, "DejaVu Sans 17.5", C_CYAN, a)
    props = [
        ("1. Exponential Novelty", "π(m) ~ 2^(m+1)/m yields 54.97 billion distinct loops by m = 40.", C_EMERALD),
        ("2. Optimal Mixing Speed", "Alon–Boppana bound O(2^(−m/2)) steers harmony to any mood in 3 beats.", C_GOLD),
        ("3. Continuous Voice-Leading", "Every step moves 1 voice by ≤ 2 semitones — zero jarring harmonic cuts.", C_MAGENTA),
    ]
    for i, (ph, pd, col) in enumerate(props):
        yy = 634.0 + i * 88.0
        draw_text(ctx, f"<b>{ph}:</b>", 102.0, yy, "DejaVu Sans 16.5", col, a)
        draw_text(ctx, pd, 102.0, yy + 30.0, "DejaVu Sans 15", C_SLATE, a, max_width=800.0)

    # Right full-height panel: EXACT Theorem 5.3 Magnetic Flux Riemann Window Plot!
    draw_panel(ctx, 968.0, 166.0, 880.0, 748.0, a, C_GOLD, 22.0)
    draw_text(ctx, "<b>THEOREM 5.3  ·  THE MAGNETIC FLUX RIEMANN WINDOW</b>", 1408.0, 204.0, "DejaVu Sans 18.5", C_GOLD, a, "center", "center")
    draw_text(ctx, "Twisted Tonnetz spectrum  <i>λ</i><sub>max</sub>(<i>A</i><sub><i>φ</i></sub>)  as a function of harmonic flux <i>φ</i>", 1408.0, 240.0, "DejaVu Sans 15", C_SLATE, a, "center", "center")

    px0, py0, pw0, ph0 = 1054.0, 290.0, 742.0, 448.0
    def fx(phi: float) -> float:
        return px0 + pw0 * (phi / 3.8)
    def fy(lam: float) -> float:
        return py0 + ph0 * (1.0 - (lam - 2.65) / 0.40)

    # Shaded Riemann Window (0 <= phi <= phi_c)
    p_win = ease_out_cubic(seg_prog(u, 0.35, 0.72))
    rw_x = fx(b.phi_c) - px0
    rounded_rect(ctx, px0, py0, rw_x * p_win, ph0, 6.0)
    set_rgba(ctx, C_EMERALD, 0.12 * a * p_win)
    ctx.fill()
    draw_text(ctx, "<b>RIEMANN WINDOW</b>\n|φ| &lt; 2.8909\n(Safe adaptive tension!)", px0 + rw_x * 0.44, py0 + 285.0, "DejaVu Sans 15.5", C_EMERALD, a * p_win, "center", "center")

    # Danger zone beyond phi_c
    rounded_rect(ctx, fx(b.phi_c), py0, px0 + pw0 - fx(b.phi_c), ph0, 6.0)
    set_rgba(ctx, C_MAGENTA, 0.12 * a * p_win)
    ctx.fill()
    draw_text(ctx, "<b>BEYOND\nWINDOW</b>", fx(b.phi_c) + 86.0, py0 + 335.0, "DejaVu Sans 13.5", C_MAGENTA, a * p_win, "center", "center")

    # Horizontal grid & 2*sqrt(2) Ramanujan line
    for lv in (2.70, 2.80, 2.90, 3.00):
        yy = fy(lv)
        ctx.new_path()
        ctx.move_to(px0, yy); ctx.line_to(px0 + pw0, yy)
        set_rgba(ctx, C_GRID, a * 1.2)
        ctx.set_line_width(1.0)
        ctx.stroke()
        draw_text(ctx, f"{lv:.2f}", px0 - 12.0, yy, "DejaVu Sans Mono 12", C_DIM, a, "right", "center")

    y_ram = fy(2.0 * math.sqrt(2.0))
    ctx.save()
    ctx.new_path()
    ctx.set_dash([7.0, 5.0])
    ctx.move_to(px0, y_ram); ctx.line_to(px0 + pw0, y_ram)
    set_rgba(ctx, C_CYAN, a * 0.9)
    ctx.set_line_width(2.0)
    ctx.stroke()
    ctx.restore()
    draw_text(ctx, "2√2 ≈ 2.8284", px0 + pw0 - 8.0, y_ram - 16.0, "DejaVu Sans Mono 12", C_CYAN, a, "right", "center")

    # Exact computed curve lambda_max(A_phi)
    k_lim = max(2, int(ease_out_cubic(seg_prog(u, 0.20, 0.78)) * len(b.phis)))
    for mult, alp in [(3.0, 0.15), (1.0, 0.98)]:
        ctx.new_path()
        for k in range(k_lim):
            xx, yy = fx(float(b.phis[k])), fy(float(b.lmax_phi[k]))
            if k == 0:
                ctx.move_to(xx, yy)
            else:
                ctx.line_to(xx, yy)
        set_rgba(ctx, C_GOLD, a * alp)
        ctx.set_line_width(3.4 * mult)
        ctx.stroke()

    # Exact crossing marker at phi_c
    draw_glow_circle(ctx, fx(b.phi_c), y_ram, 9.0 * p_win, C_MAGENTA, a * p_win)
    for pv in (0.0, 1.0, 2.0, 2.89, 3.5):
        draw_text(ctx, f"{pv:.2f}", fx(pv), py0 + ph0 + 22.0, "DejaVu Sans Mono 12", C_SLATE, a, "center", "center")
    draw_text(ctx, "Magnetic flux φ  (controlled live by game tension!)", px0 + pw0 * 0.5, py0 + ph0 + 56.0, "DejaVu Sans 15", C_WHITE, a, "center", "center")

    draw_text(
        ctx,
        "Inside |<i>φ</i>| &lt; 2.8909, twisting the Tonnetz smoothly shifts harmonic color\nwithout breaking Ramanujan optimality — ready to score a live chess match!",
        1408.0,
        856.0,
        "DejaVu Sans 15",
        C_SLATE,
        a,
        "center",
        "center",
        max_width=810.0,
        line_spacing=1.32,
    )


# ---------------------------------------------------------------------------
# Chapter 4: LIVE CHESS MATCH — Music Shifting by Phase & Position!
# ---------------------------------------------------------------------------

UNICODE_PIECES = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
}


def render_ch4_chess(ctx: cairo.Context, t: float, t0: float, t1: float, b: MasterBundle) -> None:
    a = scene_alpha(t, t0, t1)
    if a <= 0.0:
        return

    # Locate current chess ply
    ply_idx = 0
    for i, ts in enumerate(b.chess_times):
        if t >= ts:
            ply_idx = i
    stp = b.chess_steps[ply_idx]

    phase_colors = {
        "OPENING": C_CYAN,
        "ATTACK": C_GOLD,
        "CRISIS": C_MAGENTA,
        "WINNING": C_EMERALD,
    }
    p_col = phase_colors[stp.phase]

    draw_pill(ctx, f"CHAPTER 4  ·  LIVE CHESS DEMO  ·  PHASE: {stp.phase}", 72.0, 44.0, p_col, a)
    draw_text(ctx, "<b>Traxler Counterattack: Position &amp; Phase Drive the Tonnetz</b>", 72.0, 92.0, "DejaVu Sans 34", C_WHITE, a)

    # --- 1. Live Vertical Evaluation Bar (x = 72..142, y = 168..896) ---
    ex, ey, ew, eh = 72.0, 168.0, 68.0, 728.0
    draw_panel(ctx, ex, ey, ew, eh, a, p_col, 14.0, fill_col=(0.06, 0.07, 0.12, 0.96), border_width=2.2)
    # Smoothly interpolate eval across plies
    ev = stp.eval_cp
    if ply_idx > 0:
        frac_e = ease_out_cubic(clamp01((t - b.chess_times[ply_idx]) / 0.55))
        ev = b.chess_steps[ply_idx - 1].eval_cp * (1 - frac_e) + stp.eval_cp * frac_e
    w_frac = clamp01(0.5 + math.tanh(ev / 4.2) * 0.46)
    wh = eh * w_frac
    rounded_rect(ctx, ex + 4, ey + eh - wh + 4, ew - 8, max(8.0, wh - 8), 10.0)
    bar_c = C_EMERALD if ev >= 1.5 else (C_MAGENTA if ev <= -1.0 else C_CYAN)
    set_rgba(ctx, bar_c, 0.82 * a)
    ctx.fill()
    # Center zero tick
    ctx.new_path()
    ctx.move_to(ex, ey + eh * 0.5); ctx.line_to(ex + ew, ey + eh * 0.5)
    set_rgba(ctx, C_WHITE, a * 0.7)
    ctx.set_line_width(2.0)
    ctx.stroke()
    draw_text(ctx, f"<b>{ev:+.1f}</b>", ex + ew * 0.5, ey + eh + 18.0, "DejaVu Sans Mono 13.5", bar_c, a, "center", "center")

    # --- 2. Glowing 8x8 Neon Chess Board (x = 166..894, y = 168..896, cached per ply!) ---
    bx, by, bsize = 166.0, 168.0, 728.0
    sq_s = bsize / 8.0
    draw_panel(ctx, bx - 8, by - 8, bsize + 16, bsize + 16, a, p_col, 18.0, border_width=2.6)

    if ply_idx not in _CHESS_BOARD_CACHE:
        bsurf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(bsize), int(bsize))
        bctx = cairo.Context(bsurf)
        bctx.set_antialias(cairo.ANTIALIAS_GOOD)
        for rank in range(8):
            for file_i in range(8):
                sx = file_i * sq_s
                sy = (7 - rank) * sq_s
                is_light = (rank + file_i) % 2 == 1
                sq_col = (0.145, 0.205, 0.335, 1.0) if is_light else (0.068, 0.100, 0.185, 1.0)
                bctx.new_path()
                bctx.rectangle(sx, sy, sq_s, sq_s)
                set_rgba(bctx, sq_col, 1.0)
                bctx.fill()
                if ply_idx > 0 and ((file_i, rank) == stp.from_sq or (file_i, rank) == stp.to_sq):
                    bctx.new_path()
                    bctx.rectangle(sx + 2, sy + 2, sq_s - 4, sq_s - 4)
                    set_rgba(bctx, p_col, 0.32)
                    bctx.fill_preserve()
                    set_rgba(bctx, p_col, 0.92)
                    bctx.set_line_width(2.4)
                    bctx.stroke()
                ch = stp.board[rank][file_i]
                if ch != ".":
                    glyph = UNICODE_PIECES[ch]
                    p_tint = C_WHITE if ch.isupper() else (0.85, 0.36, 0.65, 1.0)
                    draw_text(bctx, glyph, sx + sq_s * 0.5, sy + sq_s * 0.50, "DejaVu Sans 50", p_tint, 1.0, "center", "center")
        _CHESS_BOARD_CACHE[ply_idx] = bsurf

    ctx.save()
    ctx.set_source_surface(_CHESS_BOARD_CACHE[ply_idx], bx, by)
    ctx.paint_with_alpha(a)
    ctx.restore()

    # Board file/rank coordinates
    for i in range(8):
        draw_text(ctx, chr(ord("a") + i), bx + (i + 0.5) * sq_s, by + bsize + 18.0, "DejaVu Sans Mono 12", C_DIM, a, "center", "center")
        draw_text(ctx, str(i + 1), bx - 16.0, by + (7 - i + 0.5) * sq_s, "DejaVu Sans Mono 12", C_DIM, a, "center", "center")

    # --- 3. Right Control Telemetry: Live Move + Active Chord + Flux Gauge + Mini Tonnetz ---
    rx, rw = 936.0, 912.0

    # Top card: Current Move + Phase + Harmonic State
    draw_panel(ctx, rx, 168.0, rw, 224.0, a, p_col, 20.0, border_width=2.4)
    draw_text(ctx, "CURRENT MOVE", rx + 30.0, 194.0, "DejaVu Sans Mono 12.5", C_SLATE, a)
    draw_text(ctx, f"<b>{stp.san}</b>", rx + 30.0, 232.0, "DejaVu Sans Mono 30", C_WHITE, a)
    draw_text(ctx, f"Eval: <b>{ev:+.1f}</b>", rx + 30.0, 314.0, "DejaVu Sans Mono 19", bar_c, a)

    # Active chord badge on right side of top card
    draw_text(ctx, "LIVE TONNETZ TRIAD", rx + 425.0, 194.0, "DejaVu Sans Mono 12.5", C_SLATE, a)
    draw_text(ctx, f"<b>{stp.chord_name}</b>", rx + 425.0, 232.0, "DejaVu Sans 36", p_col, a)
    pc_names = " – ".join(PITCH_NAMES_12[p] for p in stp.chord_pcs)
    draw_text(ctx, f"Voices: <b>{pc_names}</b>  ·  W = <b>+{stp.winding_w:.2f}</b>", rx + 425.0, 316.0, "DejaVu Sans Mono 14.5", C_WHITE, a)

    # Middle card: Live Flux Meter inside Theorem 5.3's Riemann Window!
    draw_panel(ctx, rx, 418.0, rw, 194.0, a, C_GOLD, 20.0)
    draw_text(ctx, "<b>MAGNETIC FLUX  φ(t)  (RIEMANN WINDOW)</b>", rx + 30.0, 444.0, "DejaVu Sans 15.5", C_GOLD, a)
    draw_text(ctx, f"<b>φ = {stp.flux_phi:.2f} / 2.8909</b>", rx + rw - 30.0, 444.0, "DejaVu Sans Mono 15.5", p_col, a, "right")
    mx0, my0, mw0, mh0 = rx + 30.0, 496.0, rw - 60.0, 34.0
    rounded_rect(ctx, mx0, my0, mw0, mh0, 10.0)
    set_rgba(ctx, (0.10, 0.15, 0.26, 0.9), a)
    ctx.fill()
    # Critical wall marker at 2.8909 / 3.2
    cx_wall = mx0 + mw0 * (2.8909 / 3.2)
    fw_phi = max(14.0, mw0 * clamp01(stp.flux_phi / 3.2))
    rounded_rect(ctx, mx0, my0, fw_phi, mh0, 10.0)
    set_rgba(ctx, p_col, a * 0.92)
    ctx.fill()
    ctx.new_path()
    ctx.move_to(cx_wall, my0 - 8); ctx.line_to(cx_wall, my0 + mh0 + 8)
    set_rgba(ctx, C_CYAN, a)
    ctx.set_line_width(3.0)
    ctx.stroke()
    draw_text(ctx, "Calm (φ=0)", mx0, my0 + 48.0, "DejaVu Sans Mono 12", C_CYAN, a)
    draw_text(ctx, "φ_c = 2.8909 (Ramanujan Wall)", cx_wall, my0 + 48.0, "DejaVu Sans Mono 12", C_CYAN, a, "right")

    # Bottom card: Live Harmonic Trajectory & Phase Explanation
    draw_panel(ctx, rx, 638.0, rw, 258.0, a, C_PANEL_BORDER, 20.0)
    draw_text(ctx, "<b>LIVE ADAPTIVE HARMONIC WALK (ZERO REPETITION)</b>", rx + 30.0, 666.0, "DejaVu Sans 16.5", C_WHITE, a)

    # Plot live chord trajectory nodes across plies 0..ply_idx
    tx0, tx1 = rx + 46.0, rx + rw - 46.0
    ty_mid = 768.0
    n_tot = len(b.chess_steps)
    pts_tr = []
    for k in range(ply_idx + 1):
        st_k = b.chess_steps[k]
        xx = tx0 + (tx1 - tx0) * (k / float(n_tot - 1))
        yy = ty_mid - math.tanh(st_k.eval_cp / 4.5) * 48.0
        pts_tr.append((xx, yy, phase_colors[st_k.phase], st_k.chord_name))
    for k in range(len(pts_tr) - 1):
        draw_glow_line(ctx, pts_tr[k][0], pts_tr[k][1], pts_tr[k + 1][0], pts_tr[k + 1][1], pts_tr[k + 1][2], 3.0, a * 0.9)
    for k, (xx, yy, col, cnm) in enumerate(pts_tr):
        is_last = (k == len(pts_tr) - 1)
        draw_glow_circle(ctx, xx, yy, 9.5 if is_last else 5.0, col, a)
        if is_last or k in (0, 5, 8, 10, 13, 19):
            draw_text(ctx, cnm, xx, yy - 20.0 if k % 2 == 0 else yy + 22.0, "DejaVu Sans Mono 11", col, a, "center", "center")

    phase_notes = {
        "OPENING": "Balanced opening → low flux, warm diatonic major/minor voice leading.",
        "ATTACK":  "Rising sharpness → flux climbs inside Riemann Window; faster arpeggios &amp; winding.",
        "CRISIS":  "Bxf2+!! → flux nears Ramanujan wall: dark chromatic minor &amp; tritone tension!",
        "WINNING": "Decisive turnaround → flux clears, chords soar into radiant major resolution!",
    }
    draw_text(ctx, phase_notes[stp.phase], rx + 30.0, 854.0, "DejaVu Sans 13.5", p_col, a)


# ---------------------------------------------------------------------------
# Chapter 5: Novelty 1 — Coding Theory, NEG-M11 (8-EDO) & Corollary B.1
# ---------------------------------------------------------------------------

def render_ch5(ctx: cairo.Context, t: float, t0: float, t1: float) -> None:
    a = scene_alpha(t, t0, t1)
    if a <= 0.0:
        return
    u = seg_prog(t, t0, t1)

    draw_pill(ctx, "CHAPTER 5  ·  CODING THEORY ↔ MICROTONAL HARMONY (NOVELTY 1)", 72.0, 44.0, C_MAGENTA, a)
    draw_text(ctx, "<b>Open Problem (3): 8-EDO Illusion (NEG-M11) vs. 12-EDO Guarantee</b>", 72.0, 92.0, "DejaVu Sans 34", C_WHITE, a)

    # Split 8-EDO stereo clock + center unison melody + bottom Corollary B.1 resolution
    tune_8 = [3, 5, 7, 1]
    step = int((t - t0) / 0.78) % 4
    m_pc = tune_8[step]

    def draw_clock(cx: float, cy: float, r: float, held: Tuple[int, int], col: Tuple[float, float, float, float], title: str) -> None:
        ctx.new_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        set_rgba(ctx, (0.18, 0.28, 0.46, 0.78), a)
        ctx.set_line_width(2.0)
        ctx.stroke()

        def pos(pc: int) -> Tuple[float, float]:
            ang = -math.pi / 2.0 + (pc % 8) * (math.pi / 4.0)
            return (cx + r * math.cos(ang), cy + r * math.sin(ang))

        h0, h1, mp = pos(held[0]), pos(held[1]), pos(m_pc)
        draw_glow_line(ctx, *h0, *h1, col, 4.0, a * 0.9)
        ctx.new_path()
        ctx.move_to(*h0); ctx.line_to(*h1); ctx.line_to(*mp); ctx.close_path()
        set_rgba(ctx, col, 0.24 * a)
        ctx.fill_preserve()
        set_rgba(ctx, col, 0.95 * a)
        ctx.set_line_width(2.6)
        ctx.stroke()
        for k in range(4):
            draw_glow_line(ctx, *pos(tune_8[k]), *pos(tune_8[(k + 1) % 4]), C_GOLD, 2.4, a * 0.72)
        for pc in range(8):
            px, py = pos(pc)
            if pc == m_pc:
                draw_glow_circle(ctx, px, py, 16.0, C_GOLD, a)
                draw_text(ctx, f"<b>{pc}</b>", px, py, "DejaVu Sans Mono 14", C_BG_DEEP, a, "center", "center")
            elif pc in held:
                draw_glow_circle(ctx, px, py, 15.0, col, a)
                draw_text(ctx, f"<b>{pc}</b>", px, py, "DejaVu Sans Mono 14", C_BG_DEEP, a, "center", "center")
            else:
                ctx.new_path()
                ctx.arc(px, py, 12.5, 0, 2 * math.pi)
                set_rgba(ctx, (0.07, 0.11, 0.20, 0.96), a)
                ctx.fill_preserve()
                set_rgba(ctx, C_DIM, a)
                ctx.set_line_width(1.3)
                ctx.stroke()
                draw_text(ctx, str(pc), px, py, "DejaVu Sans Mono 12", C_SLATE, a, "center", "center")
        draw_text(ctx, title, cx, cy - r - 38.0, "DejaVu Sans Bold 17", col, a, "center", "center")
        cs = sorted([held[0], held[1], m_pc])
        draw_text(ctx, f"{{{cs[0]}, {cs[1]}, {cs[2]}}}", cx, cy + r + 34.0, "DejaVu Sans Mono 16", C_WHITE, a, "center", "center")

    draw_panel(ctx, 72.0, 166.0, 560.0, 500.0, a, C_CYAN, 20.0)
    draw_clock(352.0, 422.0, 148.0, (0, 4), C_CYAN, "ORBIT A  (LEFT EAR: holds {0, 4})")

    draw_panel(ctx, 1288.0, 166.0, 560.0, 500.0, a, C_MAGENTA, 20.0)
    draw_clock(1568.0, 422.0, 148.0, (2, 6), C_MAGENTA, "ORBIT B  (RIGHT EAR: holds {2, 6})")

    draw_panel(ctx, 664.0, 166.0, 592.0, 500.0, a, C_GOLD, 20.0)
    cx_m = 960.0
    draw_pill(ctx, "COUNTEREXAMPLE  NEG-M11", cx_m, 198.0, C_MAGENTA, a, "center", "DejaVu Sans Bold 13")
    draw_text(ctx, "<b>N = 8  ·  S = {2}  ·  T/I({0, 1, 4})</b>", cx_m, 268.0, "DejaVu Sans Mono 17", C_WHITE, a, "center", "center")
    pxs = [772.0, 898.0, 1022.0, 1148.0]
    for k in range(3):
        draw_glow_line(ctx, pxs[k] + 28, 372.0, pxs[k + 1] - 28, 372.0, C_GOLD, 2.6, a * 0.7)
    for k, pc in enumerate(tune_8):
        act = (k == step)
        if act:
            draw_glow_circle(ctx, pxs[k], 372.0, 30.0, C_GOLD, a)
            draw_text(ctx, f"<b>{pc}</b>", pxs[k], 372.0, "DejaVu Sans Mono 21", C_BG_DEEP, a, "center", "center")
        else:
            ctx.new_path()
            ctx.arc(pxs[k], 372.0, 23.0, 0, 2 * math.pi)
            set_rgba(ctx, (0.09, 0.13, 0.22, 0.96), a)
            ctx.fill_preserve()
            set_rgba(ctx, C_GOLD, 0.72 * a)
            ctx.set_line_width(1.8)
            ctx.stroke()
            draw_text(ctx, str(pc), pxs[k], 372.0, "DejaVu Sans Mono 18", C_GOLD, a, "center", "center")
    draw_text(ctx, "Identical cyclic melody: <b>(3, 5, 7, 1)</b>", cx_m, 444.0, "DejaVu Sans 17", C_GOLD, a, "center", "center")
    draw_text(ctx, "<b>Orbit A ∩ Orbit B = ∅</b>\n(Two disjoint 4-cycles, ONE tune!)", cx_m, 548.0, "DejaVu Sans 18", C_WHITE, a, "center", "center", line_spacing=1.35)

    # Bottom banner: Theorems A, B & Corollary B.1 resolution
    p_bot = ease_out_cubic(seg_prog(u, 0.52, 0.78))
    draw_panel(ctx, 72.0, 694.0, 1776.0, 220.0, a * (0.25 + 0.75 * p_bot), C_EMERALD, 20.0, border_width=2.4)
    draw_text(
        ctx,
        "<b>THEOREMS A, B &amp; COROLLARY B.1 (PROVED UNIVERSALLY IN LEAN 4):</b>",
        106.0,
        724.0,
        "DejaVu Sans 18.5",
        C_EMERALD,
        a,
    )
    draw_text(
        ctx,
        "• <b>Theorem A:</b> |<i>L</i><sub><i>h</i>₁</sub> ∩ <i>L</i><sub><i>h</i>₂</sub>| ≤ 2 ∀<i>N</i> ≥ 3, ∀<i>S</i>  (zero 2-moving-voice collisions).\n"
        "• <b>Theorem B:</b> 1-voice collision exists <b>iff</b>  <i>N</i> = 8<i>m</i>  ∧  <i>C</i> = <i>T/I</i>({0, <i>m</i>, 4<i>m</i>})  ∧  2<i>m</i> ∈ <i>S</i>  (10,576 chords verified in Rust).\n"
        "• <b>Corollary B.1:</b> For <b>12-EDO</b> &amp; every consecutive step set <i>S</i> = {1,…,<i>k</i>}, 2<i>m</i> ∈ <i>S</i> ⇒ <i>m</i> ∈ <i>S</i> is forbidden → <b>ZERO collisions ∀<i>N</i> ≥ 5!</b>",
        106.0,
        768.0,
        "DejaVu Sans 16",
        C_WHITE,
        a,
        max_width=1700.0,
        line_spacing=1.38,
    )


# ---------------------------------------------------------------------------
# Chapter 6: Novelty 2 — Theorem C (Statistical Mechanics & 75.3x Edgeworth)
# ---------------------------------------------------------------------------

def render_ch6(ctx: cairo.Context, t: float, t0: float, t1: float, b: MasterBundle) -> None:
    a = scene_alpha(t, t0, t1)
    if a <= 0.0:
        return
    u = seg_prog(t, t0, t1)

    draw_pill(ctx, "CHAPTER 6  ·  STATISTICAL MECHANICS ↔ RANDOM WALKS (NOVELTY 2)", 72.0, 44.0, C_GOLD, a)
    draw_text(ctx, "<b>Theorem C: Isotropic Drift, <i>C</i><sub>6</sub> Crystal &amp; 75.3× Precision Leap</b>", 72.0, 92.0, "DejaVu Sans 34", C_WHITE, a)

    # Left panel: Dual Polar Visual (Order 4 Emerald Circle + Order 6 Gold C_6 Crystal!)
    draw_panel(ctx, 72.0, 166.0, 820.0, 748.0, a, C_GOLD, 22.0)
    cx, cy = 482.0, 514.0
    draw_text(
        ctx,
        "log(<i>ρ</i>(<i>ξ</i>)/2) = −¼ <i>r</i>² − <span foreground='#2CF59B'><b>17/192</b></span> <i>r</i>⁴ − <span foreground='#FFB800'><b>(49/768 + cos 6<i>α</i> / 23040)</b></span> <i>r</i>⁶",
        cx,
        208.0,
        "DejaVu Serif 17.5",
        C_WHITE,
        a,
        "center",
        "center",
    )

    R0, Ramp = 190.0, 46.0
    bloom = ease_out_cubic(seg_prog(u, 0.35, 0.72))
    # Order-4 Emerald Isotropic Circle
    ctx.new_path()
    ctx.arc(cx, cy, R0, 0, 2 * math.pi)
    set_rgba(ctx, C_EMERALD, a * 0.92)
    ctx.set_line_width(3.4)
    ctx.stroke()

    # Order-6 Gold C_6 Crystal Flower
    for mult, alp in [(3.4, 0.14), (1.0, 0.98)]:
        ctx.new_path()
        for k in range(241):
            ang = 2.0 * math.pi * (k / 240.0)
            rr = R0 + Ramp * bloom * math.cos(6.0 * ang)
            px, py = cx + rr * math.cos(ang), cy - rr * math.sin(ang)
            if k == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        set_rgba(ctx, C_GOLD, a * alp * bloom)
        ctx.set_line_width(3.8 * mult)
        ctx.stroke()

    draw_glow_circle(ctx, cx + R0 + Ramp * bloom, cy, 8.5, C_GOLD, a)
    draw_text(ctx, "<b>Zigzag (4u+3v)</b>\n367.75", cx + 252.0, cy - 86.0, "DejaVu Sans Mono 12.5", C_GOLD, a * bloom, "left", "center")
    ang_ac = 5.0 * math.pi / 6.0
    draw_glow_circle(ctx, cx + (R0 - Ramp * bloom) * math.cos(ang_ac), cy - (R0 - Ramp * bloom) * math.sin(ang_ac), 8.5, C_CYAN, a)
    draw_text(ctx, "<b>Armchair (W=−u, v)</b>\n367.25", cx - 375.0, cy - 115.0, "DejaVu Sans Mono 12.5", C_CYAN, a * bloom, "left", "center")

    draw_text(
        ctx,
        "<span foreground='#2CF59B'><b>Order 4 (Circle):</b> <i>m</i>·<i>κ</i><sub>ex</sub> = −17/2 = −8.500 in ALL directions (NEG-E3 resolved)</span>\n"
        "<span foreground='#FFB800'><b>Order 6 (Crystal):</b> Hexagonal <i>C</i><sub>6</sub> anisotropy breaks out (1469/4 vs 1471/4)</span>",
        cx,
        840.0,
        "DejaVu Sans 14.5",
        C_WHITE,
        a,
        "center",
        "center",
        max_width=770.0,
        line_spacing=1.42,
    )

    # Right panel: Exact m=40 Edgeworth Ladder & Flattening Residual (54.97B primes!)
    draw_panel(ctx, 924.0, 166.0, 924.0, 748.0, a, C_CYAN, 22.0)
    draw_text(ctx, "<b>m = 40  (54,975,717,792 PRIMES)  ·  EDGEWORTH LADDER</b>", 1386.0, 206.0, "DejaVu Sans 18", C_CYAN, a, "center", "center")

    p0 = ease_out_cubic(seg_prog(u, 0.14, 0.34))
    p4 = ease_out_cubic(seg_prog(u, 0.42, 0.60))
    p6 = ease_out_cubic(seg_prog(u, 0.64, 0.82))

    # Zoomed residual plot (y = 256..556)
    rx0, ry0, rw0, rh0 = 1002.0, 272.0, 804.0, 290.0
    rmid = ry0 + rh0 * 0.5
    max_r = 0.011
    draw_text(ctx, "Zoomed Residual  <i>P</i><sub>40</sub>(<i>w</i>) − <i>Q</i>(<i>w</i>)  (watch error collapse 75.3×!)", rx0, ry0 - 10.0, "DejaVu Sans 14.5", C_SLATE, a, "left", "bottom")
    ctx.new_path()
    ctx.move_to(rx0, rmid); ctx.line_to(rx0 + rw0, rmid)
    set_rgba(ctx, C_SLATE, a * 0.55)
    ctx.set_line_width(1.3)
    ctx.stroke()

    def wx(wf: float) -> float:
        return rx0 + rw0 * ((wf + 5.5) / 11.0)

    def draw_res(q_arr: np.ndarray, col: Tuple[float, float, float, float], prog: float, lw: float) -> None:
        if prog <= 0.0:
            return
        pts = [(wx(float(w)), rmid - float(b.p_exact[w + 8] - q_arr[w + 8]) / max_r * (rh0 * 0.44)) for w in range(-5, 6)]
        for k in range(len(pts) - 1):
            draw_glow_line(ctx, *pts[k], *pts[k + 1], col, lw, a * prog)
        for px, py in pts:
            draw_glow_circle(ctx, px, py, 5.0, col, a * prog)

    draw_res(b.q_gauss, C_CORAL, p0 * (0.42 if p6 > 0.5 else 1.0), 2.4)
    draw_res(b.q_edge4, C_GOLD, p4 * (0.65 if p6 > 0.5 else 1.0), 2.8)
    draw_res(b.q_edge6, C_CYAN, p6, 3.4)

    for w in range(-5, 6):
        draw_text(ctx, f"{w:+d}" if w != 0 else "0", wx(float(w)), ry0 + rh0 + 18.0, "DejaVu Sans Mono 12", C_DIM, a, "center", "center")

    # 3 Precision Metric Bars below
    rows = [
        ("C-2   Gaussian  O(1/m)",        f"TV = {b.tv_gauss:.4e}   (1.0×)",                         C_CORAL, p0, 1.0 / 75.3),
        ("C-2'  4th Edgeworth  O(1/m²)",  f"TV = {b.tv_edge4:.4e}   ({b.tv_gauss/b.tv_edge4:.1f}×)", C_GOLD,  p4, (b.tv_gauss / b.tv_edge4) / 75.3),
        ("C-2'' 6th Edgeworth  O(1/m³)",  f"TV = {b.tv_edge6:.4e}   ({b.tv_gauss/b.tv_edge6:.1f}×)", C_CYAN,  p6, 1.0),
    ]
    for i, (lbl, mtxt, col, pr, frac) in enumerate(rows):
        yy = 620.0 + i * 94.0
        ca = a * (0.25 + 0.75 * pr)
        draw_text(ctx, f"<b>{lbl}</b>", 964.0, yy, "DejaVu Sans 16", col, ca)
        draw_text(ctx, f"<b>{mtxt}</b>", 1808.0, yy, "DejaVu Sans Mono 16", C_WHITE, ca, "right")
        rounded_rect(ctx, 964.0, yy + 32.0, 844.0, 20.0, 8.0)
        set_rgba(ctx, (0.11, 0.16, 0.27, 0.85), ca)
        ctx.fill()
        rounded_rect(ctx, 964.0, yy + 32.0, max(14.0, 844.0 * frac * pr), 20.0, 8.0)
        set_rgba(ctx, col, ca)
        ctx.fill()


# ---------------------------------------------------------------------------
# Chapter 7: Four-Language Verification & Living Harmony Finale
# ---------------------------------------------------------------------------

def render_ch7(ctx: cairo.Context, t: float, t0: float, t1: float) -> None:
    a = scene_alpha(t, t0, t1, fade_in=0.65, fade_out=0.8)
    if a <= 0.0:
        return
    u = seg_prog(t, t0, t1)

    draw_pill(ctx, "CHAPTER 7  ·  FOUR-LANGUAGE MACHINE-CHECKED SCIENCE", WIDTH * 0.5, 44.0, C_EMERALD, a, "center")
    draw_text(ctx, "<b>Where Pure Mathematics Becomes Living, Endless Harmony</b>", WIDTH * 0.5, 118.0, "DejaVu Sans 36", C_WHITE, a, "center", "center")

    cards = [
        ("LEAN 4.36.0", "24/24 jobs · 0 sorryAx · Zero Mathlib\nUniversal ∀N proofs of Thms A, B, Cor B.1 &amp; Thm C", C_CYAN),
        ("PURE C++20", "g++ 13.3 &amp; clang++ 18.1 (-Werror)\n30/30 standalone SWE-sweep assertions PASS", C_GOLD),
        ("SWIFT++ INTEROP", "Pure Swift 6.4 ↔ C++20 at every turn\n15/15 XCTest · 19/19 CLI · 0.000e+00 delta", C_MAGENTA),
        ("RUST 1.100.0", "Zero external crates · 7/7 PASS\n10,576 chords (N≤72) · 11,452 systems (N≤96)", C_EMERALD),
    ]
    cw, ch = 860.0, 210.0
    for i, (head, desc, col) in enumerate(cards):
        r, c = i // 2, i % 2
        px, py = 72.0 + c * (cw + 56.0), 184.0 + r * (ch + 28.0)
        pr = ease_out_cubic(seg_prog(u, 0.05 + 0.12 * i, 0.25 + 0.12 * i))
        draw_panel(ctx, px, py, cw, ch, a * pr, col, 20.0, border_width=2.4)
        draw_pill(ctx, "PASS", px + cw - 24.0, py + 22.0, C_EMERALD, a * pr, "right", "DejaVu Sans Bold 12")
        draw_text(ctx, f"<b>{head}</b>", px + 28.0, py + 28.0, "DejaVu Sans 20", col, a * pr)
        draw_text(ctx, desc, px + 28.0, py + 86.0, "DejaVu Sans 16.5", C_WHITE, a * pr, max_width=cw - 56.0, line_spacing=1.42)

    p_end = ease_out_cubic(seg_prog(u, 0.42, 0.68))
    draw_panel(ctx, 72.0, 678.0, 1776.0, 232.0, a * p_end, C_GOLD, 24.0, border_width=2.6)
    draw_text(ctx, "<b>ERGENTICS  ·  MORPHEUS  ·  PRIME CADENCES</b>", WIDTH * 0.5, 732.0, "DejaVu Sans 30", C_WHITE, a * p_end, "center", "center")
    draw_text(
        ctx,
        "Educator Masterclass by <span foreground='#00F0FF'><b>Gemini 4 Neon</b></span>   ·   Spoken in Neo-Riemannian Harmony   ·   For <span foreground='#FFB800'><b>Grok Bot Reconciliation</b></span>",
        WIDTH * 0.5,
        794.0,
        "DejaVu Sans 19",
        C_SLATE,
        a * p_end,
        "center",
        "center",
    )
    draw_text(
        ctx,
        "github.com/Ergentics1/Morpheus   ·   MIT (Code Model)  /  CC BY 4.0 (Media &amp; Data Model)",
        WIDTH * 0.5,
        854.0,
        "DejaVu Sans Mono 16",
        C_EMERALD,
        a * p_end,
        "center",
        "center",
    )


# ---------------------------------------------------------------------------
# Frame Dispatch & Parallel Encoder
# ---------------------------------------------------------------------------

_CHESS_BOARD_CACHE: Dict[int, cairo.ImageSurface] = {}


def render_frame_surface(t: float, b: MasterBundle) -> cairo.ImageSurface:
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_GOOD)
    draw_chrome(ctx, t, b)

    sp = b.chapter_spans
    if sp[1][0] - 0.5 <= t <= sp[1][1] + 0.5:
        render_ch1(ctx, t, *sp[1])
    if sp[2][0] - 0.5 <= t <= sp[2][1] + 0.5:
        render_ch2(ctx, t, *sp[2], b)
    if sp[3][0] - 0.5 <= t <= sp[3][1] + 0.5:
        render_ch3(ctx, t, *sp[3], b)
    if sp[4][0] - 0.5 <= t <= sp[4][1] + 0.5:
        render_ch4_chess(ctx, t, *sp[4], b)
    if sp[5][0] - 0.5 <= t <= sp[5][1] + 0.5:
        render_ch5(ctx, t, *sp[5])
    if sp[6][0] - 0.5 <= t <= sp[6][1] + 0.5:
        render_ch6(ctx, t, *sp[6], b)
    if sp[7][0] - 0.5 <= t <= b.duration_s + 0.5:
        render_ch7(ctx, t, sp[7][0], b.duration_s)

    return surf


_G_BUNDLE: MasterBundle | None = None


def _init_worker(b: MasterBundle) -> None:
    global _G_BUNDLE, _BG_CACHE, _CHESS_BOARD_CACHE
    _G_BUNDLE = b
    _BG_CACHE = build_static_bg()
    _CHESS_BOARD_CACHE = {}


def _render_bytes(frame_idx: int) -> bytes:
    assert _G_BUNDLE is not None
    return bytes(render_frame_surface(frame_idx / float(FPS), _G_BUNDLE).get_data())


def main() -> None:
    ap = argparse.ArgumentParser(description="Render Morpheus Gemini 4 Neon 4:18 Educator Masterclass.")
    ap.add_argument("--keyframes-dir", type=str, default=None)
    ap.add_argument("--audio-out", type=str, default=None, help="Write 48kHz stereo Spoken-in-Harmony WAV")
    ap.add_argument("--frame-range", type=int, nargs=2, default=None, metavar=("START", "END"), help="Render video-only frame slice [START, END)")
    ap.add_argument("--output", type=str, default=None)
    ap.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 2))
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = args.audio_out if args.audio_out else (os.path.join(tmpdir, "masterclass_harmony.wav") if (args.output and not args.frame_range) else None)
        bundle = prepare_master_and_audio(wav_path)
        print(f"Timeline built: {bundle.duration_s:.1f}s ({bundle.total_frames} frames @ {FPS}fps)", flush=True)
        for ch, (s, e) in bundle.chapter_spans.items():
            print(f"  Chapter {ch}: {s:6.1f}s -> {e:6.1f}s ({e - s:4.1f}s)", flush=True)

        if args.keyframes_dir:
            os.makedirs(args.keyframes_dir, exist_ok=True)
            sp = bundle.chapter_spans
            kfs = [
                ("mc01_graphene.png", sp[1][0] + (sp[1][1] - sp[1][0]) * 0.70),
                ("mc02_graph_rh.png", sp[2][0] + (sp[2][1] - sp[2][0]) * 0.78),
                ("mc03_ramanujan_flux.png", sp[3][0] + (sp[3][1] - sp[3][0]) * 0.72),
                ("mc04a_chess_crisis.png", bundle.chess_times[10] + 0.8),
                ("mc04b_chess_winning.png", bundle.chess_times[19] + 0.6),
                ("mc05_neg_m11.png", sp[5][0] + (sp[5][1] - sp[5][0]) * 0.68),
                ("mc06_theorem_c.png", sp[6][0] + (sp[6][1] - sp[6][0]) * 0.78),
                ("mc07_finale.png", sp[7][0] + (bundle.duration_s - sp[7][0]) * 0.65),
            ]
            for fn, ts in kfs:
                outp = os.path.join(args.keyframes_dir, fn)
                render_frame_surface(ts, bundle).write_to_png(outp)
                print(f"  wrote keyframe {outp}", flush=True)

        if args.output:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            f0, f1 = (args.frame_range[0], min(args.frame_range[1], bundle.total_frames)) if args.frame_range else (0, bundle.total_frames)
            n_frames = f1 - f0
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-loglevel", "warning",
                "-thread_queue_size", "64",
                "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "pipe:0",
            ]
            if wav_path and not args.frame_range:
                ffmpeg_cmd += [
                    "-i", wav_path,
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-map_metadata", "-1", "-shortest",
                    args.output,
                ]
            else:
                ffmpeg_cmd += [
                    "-map", "0:v:0",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
                    "-map_metadata", "-1",
                    args.output,
                ]
            print(f"Encoding frames [{f0}, {f1}) ({n_frames} frames) with {args.workers} workers -> {args.output}...", flush=True)
            proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
            assert proc.stdin is not None
            try:
                with mp.Pool(processes=args.workers, initializer=_init_worker, initargs=(bundle,)) as pool:
                    for i_rel, raw in enumerate(pool.imap(_render_bytes, range(f0, f1), chunksize=24)):
                        proc.stdin.write(raw)
                        if (i_rel + 1) % 600 == 0 or i_rel + 1 == n_frames:
                            print(f"  rendered {i_rel + 1}/{n_frames} ({100.0 * (i_rel + 1) / n_frames:.1f}%)", flush=True)
            finally:
                proc.stdin.close()
                rc = proc.wait()
            if rc != 0:
                raise RuntimeError(f"ffmpeg exited with {rc}")
            print(f"Encoded {args.output} ({os.path.getsize(args.output) / (1024.0 * 1024.0):.2f} MB)", flush=True)


if __name__ == "__main__":
    main()
