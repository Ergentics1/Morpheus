# Ergentics Independent Verification Scripts (`ergentics/`)

Standalone **Code Model** (MIT License) verification scripts built from first principles with **zero reads of cached upstream `code/` JSON outputs or `code/` modules**.

## Scripts

- [`shimura_brandt_xcheck.py`](shimura_brandt_xcheck.py) — Independent from-scratch PARI/GP (`cypari2`) verifier for the Section 7 Shimura curve and Brandt-graph computations:
  1. **Theorem 7.11 & `NEG-E10`:** Exhaustive genus-13 enumeration of all **19** $X_0^D(N)$ pairs ($2 \mid D$, catching the omitted 4-prime curve $X_0^{690}(1)$ with $\phi(690) = 176 > 168$, $e_2 = 0$, $e_3 = 8$, $\dim S_2^{345\text{-new}} = 15$, $\operatorname{charpoly}(T_2) \bmod (t^4 - 4t^2 + 1) = 3t^3 + t^2 + 21t + 7 \neq 0$) plus all **4** 24-component $\Gamma_H$ variants.
  2. **Proposition 7.19(a)–(c):** Independent `nflist` enumeration of totally real fields of degree $n = 2$ ($D \le 1200$, `lfun` $\zeta_F(-1)$ cross-checked against exact Siegel's formula on all 118 split-2 fields), $n = 3$ ($d_F \le 5200$), and $n = 4$ ($d_F \le 60000$), followed by direct from-scratch quaternion-algebra (`alginit`), cyclic-ideal Eichler-order, and $v$-neighbour Brandt-graph construction across all $h_F^+ = 1$ mass-12 solutions (verifying weighted symmetry $w_j B_{ij} = w_i B_{ji}$, exact mass $= 12$, class counts, unit indices, and $(t^4 - 4t^2 + 1) \nmid \operatorname{charpoly}(B(v))$).
  3. **Theorem 7.20(c):** Independent from-scratch verification of the degree-5 near-miss field $d_F = 106069$ ($x^5 - 2x^4 - 4x^3 + 7x^2 + 3x - 4$, $D'' = \mathfrak{p}_{13}$, $|\zeta_F(-1)| = 16$, $h_F^+ = 1$) and its exact 12×12 Brandt characteristic polynomial $t(t - 3)(t + 1)(t^4 + 3t^3 - 4t - 1)(t^5 - t^4 - 8t^3 + 8t^2 + 15t - 16)$.

- [`open1_torsion_xcheck.py`](open1_torsion_xcheck.py) — Independent from-scratch Python + SymPy verifier for the Open Problem (1) & Lemma 7.14 results reconciled from Ergentics' clean-room Research Monograph I into `v0.3.0`:
  1. Wild involution $\sigma(z) = 3/z$ on $A_e = \{1/2 < |x|_2 < 1\}$ (fixes $(L_0, L_1)$, fixed points $\pm\sqrt{3}$ strictly inside $A_e$, cancellation-free identity $u(1+x)-4 = x(x-2)/(1+x)$).
  2. Ramified $e_v = 2, f_v = 1$ obstruction (`Prop 7.17(c)` sharpened): verifies the 36 midpoints in Class A ($M(\mathcal{O}) \ge 36$) and the explicit balanced $M = 36$ graph-of-groups witness with 36 $C_3$-leaves.
  3. Unramified cyclotomic obstruction ($e_v = 1, f_v \ge 2$) and exact $\mathbb{Z}_2[\omega]$ Klein Ping-Pong verification of the non-arithmetic sharpness counterexample $\Gamma_5 = \ker((\mathbb{Z}/2)^{*5} \to D_{12}) \subset PGL_2(\mathbb{Q}_4)$ ($s_i^2 = 2I$, $v_2(\det s_i) = 1$, 24 vertices / 36 core edges / 48 inverted edges).

## Run

```bash
/usr/bin/python3 ergentics/shimura_brandt_xcheck.py
/usr/bin/python3 ergentics/open1_torsion_xcheck.py
```
