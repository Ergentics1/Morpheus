# Round-2 referee cross-check (Grok Bot)

`round2_xcheck.py` recomputes, from scratch and without reading any data file in the repository, the results added in `v0.3.0`:

- **Theorem 7.11 / `NEG-E10`:** the full genus-13 census of $X_0^D(N)$ with $2\mid D$ (19 pairs, 11 torsion-free, including $X_0^{690}(1)$ with $e_2=0$, $e_3=8$), and the level-345 Hecke data quoted in the proof (PARI via `cypari2`).
- **Theorem 7.21:** positive definiteness of the Poitou kernel $H_1$ (closed-form Fourier transform $4\pi^4\sin^2t/(3t^2(t^2-\pi^2)^2)$), the normalisation of the explicit formula (limits $4\pi e^\gamma$, $4\pi e^{1+\gamma}$; below every minimal totally real discriminant for $n\le8$), the quoted witnesses, and a conservative three-pincer sweep over $6\le n\le14$ whose survivors are exactly the open cases stated in the paper. It also records that the mode-A second norm-2 prime is needed in Pincer 3 for $(n,u)=(7,8)$.
- **Proposition 7.18(b):** the explicit $g_1,\dots,g_5$, $s_i^2=2I$, and $\tau(s_4s_5)=49/4>4$ with $s_4s_5\in\Gamma_5$, so $\Gamma_5$ is non-arithmetic by the argument of Theorem 7.13.
- **Theorem 4.4 (clean-room count):** 13,382 valid systems for $5\le N\le18$.

Run `python round2_xcheck.py` (about 20 s). It writes `round2_xcheck_report.json` and is not part of `make audit`, so the six audit totals are unchanged.
