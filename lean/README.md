# Morpheus Lean 4 Formal Oracles (`lean/`)

Machine-checked **Code Model** (MIT License) formal proofs in pure **Lean 4.36.0** (zero external dependencies, zero `sorry`, zero custom axioms).

## Verified Theorems

| Module | Theorems Formally Proved |
| :--- | :--- |
| `Morpheus/TriadGraph.lean` | **Prop 2.1 & Cor 2.2:** $P, L, R$ involutions, bipartiteness, 3-regularity, $P = L(LR)^4$, $R = L(LR)$, exact order 12 of $LR$, simple transitivity of $D_{12}$ on `Fin 24`, Betti rank $13$ |
| `Morpheus/TuneTheorem.lean` | **Lemma 4.1, Thm 4.2 local uniqueness, `NEG-M4`:** pairwise distinct departing pitches (`L1`), unique backtracking departure (`L2`), triad interval gap & step sizes (`L3`), unique single-step move decoding, explicit backtracking counterexample `C→Cm→C` vs `E→Abm→E` |
| `Morpheus/ConductorTwo.lean` | **Prop 3.7 (`NEG-M1`) & Thm 3.8:** mod-3/mod-4 root obstructions for $\mathbb{Z}[\omega]$, $\mathbb{Z}[i]$, $\Phi_{12}$; non-ideal counterexample in $\mathbb{Z}[\omega]$; universal ring homomorphism $\psi: \mathbb{Z}[\sqrt{-3}] \to \mathbb{Z}_{12}$ (`psi_add`, `psi_mul`), exact principal ideal kernel `(3 - √-3)` (`psi_kernel_iff_ideal`), unimodular basis, non-reduced $\mathcal{O}/(2)$, and even-conductor iff criterion |
| `Morpheus/WindingAndSchottky.lean` | **Thm 5.1, Thm 6.1 Gram, Thm 7.1(a), Thm 7.13 (`NEG-M8`):** coboundary proof that $12 \mid \text{walkVoiceSum}$ for *every* closed cadence of *any* length $m \in \mathbb{N}$; exact $\det G = 108$; $\sigma_s^2 = 2I$; $\gamma_0 = PLRLPRPL \in K$; universal Chebyshev/Cayley–Hamilton proof that $\operatorname{tr}(\gamma_0^k)^2 > 4\det(\gamma_0^k)$ for *every* integer power $k \ge 1$ |

## Build & Verify

```bash
lake --dir lean build
lake --dir lean exe morpheus-lean
```
