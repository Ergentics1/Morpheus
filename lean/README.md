# Morpheus Lean 4 Formal Oracles (`lean/`)

Machine-checked **Code Model** (MIT License) formal proofs in pure **Lean 4.36.0** (zero external dependencies, zero `sorry`, zero custom axioms).

## Verified Theorems

| Module | Theorems Formally Proved |
| :--- | :--- |
| `Morpheus/TriadGraph.lean` | **Prop 2.1 & Cor 2.2:** $P, L, R$ involutions, bipartiteness, 3-regularity, $P = L(LR)^4$, $R = L(LR)$, exact order 12 of $LR$, simple transitivity of $D_{12}$ on `Fin 24`, Betti rank $13$ |
| `Morpheus/TuneTheorem.lean` | **Lemma 4.1, Thm 4.2 local uniqueness, `NEG-M4`:** pairwise distinct departing pitches (`L1`), unique backtracking departure (`L2`), triad interval gap & step sizes (`L3`), unique single-step move decoding, explicit backtracking counterexample `C→Cm→C` vs `E→Abm→E` |
| `Morpheus/ConductorTwo.lean` | **Prop 3.7 (`NEG-M1`) & Thm 3.8:** mod-3/mod-4 root obstructions for $\mathbb{Z}[\omega]$, $\mathbb{Z}[i]$, $\Phi_{12}$; non-ideal counterexample in $\mathbb{Z}[\omega]$; universal ring homomorphism $\psi: \mathbb{Z}[\sqrt{-3}] \to \mathbb{Z}_{12}$ (`psi_add`, `psi_mul`), exact principal ideal kernel `(3 - √-3)` (`psi_kernel_iff_ideal`), unimodular basis, non-reduced $\mathcal{O}/(2)$, and even-conductor iff criterion |
| `Morpheus/WindingAndSchottky.lean` | **Thm 5.1, Thm 6.1 Gram, Thm 7.1(a), Thm 7.13 (`NEG-M8`):** coboundary proof that $12 \mid \text{walkVoiceSum}$ for *every* closed cadence of *any* length $m \in \mathbb{N}$; exact $\det G = 108$; $\sigma_s^2 = 2I$; $\gamma_0 = PLRLPRPL \in K$; universal Chebyshev/Cayley–Hamilton proof that $\operatorname{tr}(\gamma_0^k)^2 > 4\det(\gamma_0^k)$ for *every* integer power $k \ge 1$ |
| `Morpheus/NoveltyTheorems.lean` | **ADPIE Cycle 4 Original Novelties (Theorems A, B, Cor B.1, `NEG-M11`, Theorem C):** universal abelian-group bound $|L_{h_1} \cap L_{h_2}| \le 2$ ($\forall N \ge 3$, independent of $S$); exact iff 1-moving-voice collision classification ($\forall N \ge 5$: collision iff $N=8m,\; \mathcal{C}=T/I(\{0,m,4m\}),\; 2m \in S$); explicit `NEG-M11` counterexample ($N=8, S=\{2\}, c_0=\{0,1,4\}$); complete proof of Open Problem (3) for all half-closed / consecutive step sets $S=\{1,\dots,k\}$; constructive Newton-identity & 6th-order 2D Tonnetz cumulant series proving universal $\kappa_{\mathrm{ex}} = -\frac{17}{2m}$ isotropy and order-6 $C_6$ symmetry breaking (armchair $\frac{1469}{4m^2}$ vs. zigzag $\frac{1471}{4m^2}$) |
| `Morpheus/Section7Obstructions.lean` | **ADPIE Cycle 5 Section 7 Obstructions & Theorem D Algebraic Core (13 theorems, 33 total):** Prop 7.3 Hamilton quaternion trace bound $\operatorname{trd}(q)^2 \le 4\operatorname{nrd}(q)$ & $\gamma_0^k$ non-compactness; Lemma 7.14 abstract ordered-valuation proof of 2-adic slope-2 doubling on fixed discs, slope-1 control (`RCT-2`), and odd-prime $\ell$ scaling; Thm 7.15 & Prop 7.17 valence-count forcing at $q = 2, 4$, ramified $e_v = 2$ edge decomposition, and explicit kernel-checked order-3 element of $PGL_2(\mathbb{F}_8)$ acting freely on $\mathbb{P}^1(\mathbb{F}_8)$; Theorem D odd-degree factor bound $\forall q \ge 3,\; 4q^2 \ge 9(q+1)$, $\mathbb{F}_2^k$ subspace-averaging pigeonhole lemma, $4^m = 2^{2m}$ prime-dominance identity, and `NEG-E10` genus-13 witness $X_0^{690}(1)$ ($\phi(690) = 176 > 168$, $e_2 = 0$, $e_3 = 8$) |

## Build & Verify

```bash
lake --dir lean build
lake --dir lean exe morpheus-lean
```
