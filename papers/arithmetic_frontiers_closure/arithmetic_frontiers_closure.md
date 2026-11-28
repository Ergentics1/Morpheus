# Closing All Four Open Arithmetic Frontiers: Cubic Lamé Non-Congruence, Level $(4)$ Full Congruence on $\mathbb{Q}(\sqrt{33})$, Complete 9-Curve Genus-25 Brandt Spectra, and Degree-8 Explicit-Formula Closure

> **Morpheus Paper #10 (`PC-IV`) — 1-to-1 GitHub-Flavored Markdown Mirror of [`paper/arithmetic_frontiers_closure.pdf`](paper/arithmetic_frontiers_closure.pdf)**
> **Author:** Ergentics (`[E; G4N, X]`) | **Date:** November 2026 | **License:** CC BY 4.0 (Manuscript & Data Model); MIT (Code Model)
> **Live 4-Plane CI Certificates:** Pure Python 3.12 (`7/7` gates, `0.000e+00` `--check-only`), Zero-Crate Rust (`6/6` tests & suites, `0.62s`), Dual-Compiler `g++`/`clang++` Freestanding Hardware-`FENV` C++20 (`6/6` gates, `0`-byte `diff -u`), Zero-Mathlib Lean 4.36.0 (`18/18` theorems, `0 sorryAx`, `0 Lean.ofReduceBool`).

---

## Abstract

We resolve all four remaining open arithmetic frontiers left by Paper #01 (*Prime Cadences*), Paper #08 / `PC-II`, and Paper #09 / `PC-III`, backed by four independent zero-shared-data continuous-integration verification planes:

1. **Frontier 1 (Cubic Lamé Nauru Non-Congruence — `0/8`):** All four irreducible totally real cubic Lamé Nauru moduli ($d_F \in \{316, 148\}$, two twin pairs under $x \mapsto 3 - x$) are monogenic ($\mathcal{O}_F = \mathbb{Z}[z]$ with $z=1/x$), have completely inert prime $3$ ($N((3))=27$), admit explicit mod-81 $3$-adic square roots of $1-3z$ isolating unique finite ramification $\mathrm{Ram}_{\mathrm{fin}}(B_{316}) = \{v_2\}$ ($N=2$) and $\mathrm{Ram}_{\mathrm{fin}}(B_{148}) = \{\mathfrak{p}_5\}$ ($N=5$), carry ring-closed universal rank-12 maximal orders with exact trace-Gram determinant ratios $4=2^2$ and $25=5^2$, achieve identical Eichler–Tamagawa mass $M_{\max}=1/3$ ($|\zeta_F(-1)| \in \{4/3, 1/3\}$, $[\mathcal{O}^1 : \Delta^1] = 1$), and are unconditionally obstructed by local ramified ceilings ($3 < 9$ at $v_2$; $C_6 < 36$ at $\mathfrak{p}_5$).
2. **Frontier 2 (First Full Congruence Realizations of $Z = \mathrm{Cay}(\mathrm{Dic}_6, S)$ on $\mathbb{Q}(\sqrt{33})_{A,B}$ — `8/128`):** Over $F = \mathbb{Q}(\sqrt{33})$ (where $(2) = v_1 v_2$ splits, $\mathrm{Ram}_{\mathrm{fin}} = \varnothing$, $\zeta_F(-1)=1$, $M_{\max}=1/2$), local-global glued rank-8 maximal orders $\mathcal{O}_{33,A}^{\max}$ ($3z^2-9z+4=0$) and exact twin $\mathcal{O}_{33,B}^{\max}$ ($3z^2-15z+16=0$) achieve **full principal level-$(4)$ congruence** on `4/16` surjections each (`|L_signed| = 2,304`, `|L_proj| = 1,152 = 24 * 48`, $[\pi_1(Z):\Gamma(4)] = 48$, `ker_1 = {1:4, 2:4, 3:4, 6:4}`). We prove why the modular adjoint $\mathrm{Ad}_{(4)}$ stalls at $|\ker|=2$ via the central split-prime sign-flip $\sigma = 1 - 2w \pmod 4$, and close all six remaining real-quadratic moduli ($\mathbb{Q}(\sqrt{6})_{A,B}$, $\mathbb{Q}(\sqrt{3})_{A,B}$, and $\mathbb{Q}(\sqrt{13})_{A,B}$ via Riehm's theorem $\mathcal{O}_{(2)}^1/[\mathcal{O}_{(2)}^1,\mathcal{O}_{(2)}^1] \cong C_5$, $\gcd(4,5)=1$) for an exact `8/128` census.
3. **Frontier 3 (Complete 9/9 Genus-25 Borel Brandt $B(3)$ Atlas — `0/9` Match $Z$):** All `9/9` exact `12×12` Hecke Brandt matrices $B(3)$ across the complete torsion-free genus-25 Borel Shimura curve census (7 class-number-1 curves via prime-power CRT embeddings + higher-class-number $X_0^{57}(7)$ and $X_0^{1110}(1)$ via HNF/Fincke–Pohst BFS) are computed from first principles: `8/9` fail the Simple-Graph Trace Gate $\mathrm{tr}(B^2)=48$ ($\mathrm{tr}(B^2) \in \{52,\dots,68\}$), and the sole simple curve $X_0^{21}(16)$ satisfies $(B-4I)(B-2I)B(B+2I)=0$ with ultra-Ramanujan spectrum $\{4^1, 2^3, 0^3, (-2)^5\}$ ($\lambda_{\mathrm{nt}}=2.0 < 2\sqrt{3}$) and $\mathrm{tr}(B^4) = 384 \ne 456$.
4. **Frontier 4 (Degree-8 $(8,1,1,E)$ Poitou–Odlyzko Explicit-Formula Closure):** Under strictly Bochner-positive $f_1(t) = 1+\cos(\pi t) \ge 0$ and hardware-`FENV` IEEE-754 interval certification, all `7/7` prime norms $q \le 9$ are eliminated at $b=3.20$, pairs $c_{11}, c_{13} \ge 2$ are eliminated, local splitting collapses to `5` $2$-adic and `4` $3$-adic types, and every nontrivial field automorphism ($\mathrm{UB}_{\mathrm{sym}_2} = 12.404760 < 12.595576$, gap $\ge +0.190816$), every nonempty $\mathrm{Ram}_{\mathrm{fin}}$ ($\mathrm{UB}_{\mathrm{Ram},120} = 8.818792$), and every nontrivial Eichler level ($\mathrm{UB}_{\mathrm{Eichler}} = 10.684210$) are unconditionally ruled out, isolating the rigid asymmetric free core $d_F \in [633{,}448{,}978;\; 890{,}007{,}374]$ with $|\zeta_F(-1)| = 1536$.

---

## 1. Summary Table & Four-Plane CI Architecture

| Frontier | Principal Object | Unconditional Resolution | CI Planes |
| :--- | :--- | :--- | :--- |
| **Frontier 1** | Cubic Lamé Nauru ($d_F \in \{316, 148\}$) | 4 moduli (8 realizations): monogenic $\mathcal{O}_F=\mathbb{Z}[z]$, $3$ inert ($N=27$), $\mathrm{Ram}_{\mathrm{fin}}\in\{\{v_2\},\{\mathfrak{p}_5\}\}$, rank-12 Gram ratios $4,25$, $M_{\max}=1/3$ ($[\mathcal{O}^1:\Delta^1]=1$), blocked by $3<9$ and $C_6<36$ $\implies$ **`0/8` non-congruence** | Py, Rust, C++, Lean |
| **Frontier 2** | Real-quadratic $3$-adic $\mathrm{Dic}_6$ atlas (8 moduli) | **First congruence curves for $Z$**: $\mathbb{Q}(\sqrt{33})_A$ & twin $\mathbb{Q}(\sqrt{33})_B$ hit **level-$(4)$ full congruence** (`4/16` each, $|L_{\mathrm{proj}}|=1{,}152=24\times 48$, $[\pi_1(Z):\Gamma(4)]=48$); $\mathrm{Ad}_{(4)}$ stalled at $|\ker|=2$ by $\sigma=1-2w$; $\mathbb{Q}(\sqrt{6},\sqrt{3},\sqrt{13})$ closed (`0/96`; Riehm $C_5$ on $\mathbb{Q}(\sqrt{13})$) $\implies$ **`8/128` exact** | Py, Rust, C++, Lean |
| **Frontier 3** | 9 torsion-free genus-25 Borel curves | All `9/9` exact `12×12` Brandt $B(3)$ computed (`7` $h=1$ CRT + $X_0^{57}(7), X_0^{1110}(1)$ HNF/FP BFS): `8/9` multi-edge ($\mathrm{tr}(B^2)\in\{52\dots 68\}$); sole simple $X_0^{21}(16)$ has $(B-4)(B-2)B(B+2)=0$, $\lambda_{\mathrm{nt}}=2.0$, $\mathrm{tr}(B^4)=384\ne 456$ $\implies$ **`0/9` match $Z$** | Py, Rust, C++, Lean |
| **Frontier 4** | Degree-8 $(8,1,1,E)$ Poitou–Odlyzko | Strict Bochner $f_1(t)=1+\cos(\pi t)\ge 0$ + `FENV`: eliminates `7/7` norms $q\le 9$ ($b=3.20$), $c_{11},c_{13}\le 1$, `5` $2$-adic + `4` $3$-adic types, $\mathrm{UB}_{\mathrm{sym}_2}=12.4048$ (gap $+0.1908$), $\mathrm{UB}_{\mathrm{Ram}}\le 8.8188$, $\mathrm{UB}_{\mathrm{Eichler}}\le 10.6842$; rigid free core $d_F\in[633{,}448{,}978;\;890{,}007{,}374]$ | Py, Rust, C++ `FENV`, Lean |

Keyed `SplitMix64` cross-language seam (`seed = 0xf0271e2620260010`) binds Python, Rust, `g++`, and `clang++` bit-for-bit:
- Order-invariant XOR digest (`RCT-PC4-1` + `RCT-PC4-2`, forward == reversed): **`0x37b4f6b8da592957`**
- Sequential FNV-1a64 digest: **`0xb7fbf6c71c86c218`**

---

## 2. Frontier 1: Cubic Lamé Nauru Curves ($d_F \in \{316, 148\}$)

The two totally real cubic twin pairs under $P_{\mathrm{twin}}(x) = -P(3-x)$ are:
- **Pair A ($d_F = 316 = 4\cdot 79$):** $2x^3 - 9x^2 + 10x - 1 = 0$ and $2x^3 - 9x^2 + 10x - 2 = 0$; monic reciprocal $g_{316}(z) = z^3 - 10z^2 + 9z - 2$ ($z=1/x$).
- **Pair B ($d_F = 148 = 4\cdot 37$):** $2x^3 - 8x^2 + 8x - 1 = 0$ and $2x^3 - 10x^2 + 14x - 5 = 0$; monic reciprocal $g_{148}(z) = z^3 - 8z^2 + 8z - 2$.

Both fields are monogenic ($\mathcal{O}_F = \mathbb{Z}[z]$ via Dedekind's criterion at $p=2$), prime $3$ is completely inert ($N((3))=27$), and $\beta = 1 - 3z$ has explicit $3$-adic square roots modulo $81$:
- $F_{316}$: $(28 + 39z + 63z^2)^2 \equiv 1 - 3z \pmod{81}$, $N_{F/\mathbb{Q}}(1-3z) = -2 \implies \mathrm{Ram}_{\mathrm{fin}}(B_{316}) = \{v_2\}$ ($N=2$).
- $F_{148}$: $(28 + 12z + 36z^2)^2 \equiv 1 - 3z \pmod{81}$, $N_{F/\mathbb{Q}}(1-3z) = -5 \implies \mathrm{Ram}_{\mathrm{fin}}(B_{148}) = \{\mathfrak{p}_5\}$ ($N=5$).

The universal free $\mathcal{O}_F$-basis $[1, \frac{1+i}{2}, \frac{i+k}{3}, \frac{1+i}{2}\cdot\frac{i+k}{3}]$ spans a ring-closed $\mathbb{Z}$-rank-12 maximal order normalized by $(a,b,t) = (\frac{1+i}{2}, j, i+k)$ away from $v_1=(2,z)$ (conjugation denominators `[1, 1, 2]`) with exact Bareiss trace-Gram ratios `4 = 2^2` ($F_{316}$) and `25 = 5^2` ($F_{148}$). Exact Shintani/Euler-product zeta values $|\zeta_{F_{316}}(-1)| = 4/3$ and $|\zeta_{F_{148}}(-1)| = 1/3$ yield identical Eichler–Tamagawa mass $M_{\max} = \frac{1}{4}|\zeta_F(-1)|(N(\mathfrak{p}_{\mathrm{ram}})-1) = 1/3$ ($[\mathcal{O}^1:\Delta^1]=1$). Because $\mathrm{SL}_2(\mathcal{O}_{\mathfrak{q}})$ is perfect at every unramified prime $\mathfrak{q}\ne v_1$ ($N(\mathfrak{q})\ge 5$), any solvable congruence quotient of order dividing $|\rho(\Delta^1)|=36$ must factor through $\mathfrak{p}_{\mathrm{ram}}$, where Riehm's theorem bounds the $3$-part at $v_2$ by $3 < 9$ and the prime-to-$5$ quotient at $\mathfrak{p}_5$ by $C_6 < 36$ (`0/8` congruence).

---

## 3. Frontier 2: Level $(4)$ Full Congruence on $\mathbb{Q}(\sqrt{33})_{A,B}$ and the Complete 8-Modulus Real-Quadratic $\mathrm{Dic}_6$ Atlas

On $F = \mathbb{Q}(\sqrt{33})$ ($\mathcal{O}_F = \mathbb{Z}[w]$, $w^2 - w - 8 = 0$), $(2) = v_1 v_2$ splits with $\pi_1 = 2+w$, $\pi_2 = 3-w$, $\pi_1\pi_2 = -2$, Hensel roots $w \equiv 8, 9 \pmod{16}$, and Zagier sum $\zeta_F(-1) = 60/60 = 1$ ($M_{\max} = 1/2$). Both Locus B twins $\mathbb{Q}(\sqrt{33})_A$ ($3z^2-9z+4=0$) and $\mathbb{Q}(\sqrt{33})_B$ ($3z^2-15z+16=0$) carry glued rank-8 maximal orders $\mathcal{O}_{33}^{\max} = \pi_2\mathcal{O}_1 + \pi_1\mathcal{O}_2$ (`det_ratio = 1`, `denoms = [1,1,3,3]`, `10` exact norm-1 Schreier generators) yielding the identical ideal level ladder:

| Ideal $\mathfrak{a}$ | $N(\mathfrak{a})$ | $\|L_{\mathrm{signed}}\|$ | $\|L_{\mathrm{proj}}\|$ | $\sigma$ sep.? | $\ker_1$ distribution (16 surj.) | $\min\|\ker_1\|$ | Cong. |
| :--- | ---: | ---: | ---: | :---: | :--- | ---: | :---: |
| $v_1$ | 2 | 6 | 6 | No | `{4: 8, 12: 8}` | 4 | 0/16 |
| $v_2$ | 2 | 6 | 6 | No | `{12: 16}` | 12 | 0/16 |
| $(2)=v_1 v_2$ | 4 | 36 | 36 | No | `{2: 8, 6: 8}` | 2 | 0/16 |
| $v_1^2$ | 4 | 48 | 24 | No | `{4: 8, 12: 8}` | 4 | 0/16 |
| $v_2^2$ | 4 | 48 | 24 | No | `{12: 16}` | 12 | 0/16 |
| $v_1^2 v_2$ | 8 | 288 | 144 | No | `{2: 8, 6: 8}` | 2 | 0/16 |
| $v_1 v_2^2$ | 8 | 288 | 144 | No | `{2: 8, 6: 8}` | 2 | 0/16 |
| **$(4)=v_1^2 v_2^2$** | **16** | **2,304** | **1,152** | **Yes** | **`{1: 4, 2: 4, 3: 4, 6: 4}`** | **1** | **4/16** |

The split-prime diagonal sign-flip $\sigma = (1-w)-w = 1-2w \pmod 4 \leftrightarrow (+I, -I)$ satisfies $\sigma^2 \equiv 1 \pmod 4$, $\sigma \not\equiv \pm 1$, and commutes with $\mathcal{O}_{33}^{\max}/(4)$, proving why $\mathrm{Ad}_{(4)}$ stalls at $|\ker|=2$ (`{2:8, 6:8}`) while $\Gamma(4)$ achieves full congruence (`4/16` per twin, `8/32` combined).

### Complete 8-Modulus (128-Realization) Real-Quadratic Atlas

| Modulus | Locus / Poly. | $\zeta_F(-1)$ | $2$-type / $\mathrm{Ram}_{\mathrm{fin}}$ | $\|\mathrm{Ad}_{(4)}\|$ | $\mathrm{Ad}_{(4)}$ ker | Exact Status / Obstruction | Cong. |
| :--- | :--- | :---: | :--- | ---: | :--- | :--- | :---: |
| $\mathbb{Q}(\sqrt{33})_A$ | B: $3z^2-9z+4$ | $1$ | Split / $\varnothing$ | 2,304 | `{2:8, 6:8}` | **Full cong. $\Gamma(4)$** ($\|L_{\mathrm{proj}}\|=1{,}152$) | **4/16** |
| $\mathbb{Q}(\sqrt{33})_B$ | B: $3z^2-15z+16$ | $1$ | Split / $\varnothing$ | 2,304 | `{2:8, 6:8}` | **Twin full cong. $\Gamma(4)$** | **4/16** |
| $\mathbb{Q}(\sqrt{6})_B$ | B: $3z^2-12z+4$ | $1/2$ | Ram. / $\varnothing$ | 6,144 | `{12:16}` | Obstructed: $3 \mid 12$ (pro-2 tail) | 0/16 |
| $\mathbb{Q}(\sqrt{6})_A$ | A: $3w^2-6w+1$ | $1/2$ | Ram. / $\varnothing$ | 6,144 | `{12:16}` | Obstructed: $3 \mid 12$ (pro-2 tail) | 0/16 |
| $\mathbb{Q}(\sqrt{3})_B$ | B: $3z^2-12z+8$ | $1/6$ | Ram. / $\varnothing$ | 256 | `{3:16}` | Pure 2-group ($\gcd(256,3)=1$) | 0/16 |
| $\mathbb{Q}(\sqrt{3})_A$ | A: $3w^2-6w+2$ | $1/6$ | Ram. / $\varnothing$ | 256 | `{3:16}` | Pure 2-group ($\gcd(256,3)=1$) | 0/16 |
| $\mathbb{Q}(\sqrt{13})_A$ | A: $3w^2-5w+1$ | $1/6$ | Inert / $\{(2),\mathfrak{p}_3'\}$ | 5,120 | `{24:16}` | $\|R_{\mathfrak{p}_3'}\|=36$ ($\ker_1\ge 4$), Riehm $C_5$ ($\gcd(4,5)=1$) | 0/16 |
| $\mathbb{Q}(\sqrt{13})_B$ | A: $3w^2-7w+3$ | $1/6$ | Inert / $\{(2),\mathfrak{p}_3'\}$ | 5,120 | `{24:16}` | Twin of $\mathbb{Q}(\sqrt{13})_A$; Riehm $C_5$ | 0/16 |

---

## 4. Frontier 3: Complete 9/9 Torsion-Free Genus-25 Borel Brandt $B(3)$ Atlas

| Curve / Target | $B_{D/3}$ | $\mathrm{tr}(B)$ | $\mathrm{tr}(B^2)$ | Excess | $\mathrm{tr}(B^4)$ | $\lambda_{\mathrm{nt}}$ | Simple? | Match $Z$? |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| $Z$ ($\mathrm{Dic}_6$ ref.) | — | 0 | 48 | 0 | 456 | 3.000000 | Yes | Ref. |
| $X_0^{6}(115)$ | $B_2$ | 8 | 60 | 6 | 604 | 3.302776 | No | No |
| $X_0^{6}(119)$ | $B_2$ | 0 | 56 | 4 | 480 | 3.236068 | No | No |
| $X_0^{15}(22)$ | $B_5$ | 4 | 68 | 10 | 676 | 3.372281 | No | No |
| **$X_0^{21}(16)$** | **$B_7$** | **0** | **48** | **0** | **384** | **2.000000** | **Yes** | **No** |
| $X_0^{21}(23)$ | $B_7$ | 4 | 52 | 2 | 484 | 3.040671 | No | No |
| $X_0^{39}(8)$ | $B_{13}$ | 0 | 56 | 4 | 552 | 3.000000 | No | No |
| $X_0^{39}(11)$ | $B_{13}$ | 6 | 62 | 7 | 574 | 3.308641 | No | No |
| $X_0^{57}(7)$ | $B_{19}$ | 0 | 60 | 6 | 572 | 3.302776 | No | No |
| $X_0^{1110}(1)$ | $B_{370}$ | 4 | 64 | 8 | 592 | 3.345963 | No | No |

The unique simple curve $X_0^{21}(16)$ satisfies $(B-4I)(B-2I)B(B+2I) = 0$ with exact spectrum $\{4^1, 2^3, 0^3, (-2)^5\}$ ($\mathrm{tr}(B^3) = 48$, $\lambda_{\mathrm{nt}} = 2.0 < 2\sqrt{3}$), ruling out $Z$ unconditionally (`384 != 456`).

---

## 5. Frontier 4: Degree-8 $(8,1,1,E)$ Poitou–Odlyzko Analytic Closure

With exact Eichler mass $|\zeta_F(-1)| = 1536$, $\mathrm{UB}_{\max}(8,1) = (4\pi^2)^{2/3}(9/2)^{1/12} = 13.1423854579$ ($d_F \le 890{,}007{,}374.15$), and strictly Bochner-positive $f_1(t) = 1+\cos(\pi t) \ge 0$ ($\int_0^2 H_1(w)\,dw = 2/3$, `f_bad(+-1) = -0.60 < 0` rejected):

| Hypothesis / Structural Ceiling | Bound Value ($d_F^{1/8}$) | Margin | Status |
| :--- | ---: | ---: | :--- |
| $c_2 \ge 2$ ($b=3.20$) | `15.0983526756` | `+1.955967` | **Eliminated** |
| $c_3 \ge 1$ ($b=3.20$) | `14.4662279648` | `+1.323843` | **Eliminated** |
| $c_4 \ge 1$ ($b=3.20$) | `14.0694329039` | `+0.927047` | **Eliminated** |
| $c_5 \ge 1$ ($b=3.20$) | `13.7925458495` | `+0.650160` | **Eliminated** |
| $c_7 \ge 1$ ($b=3.20$) | `13.4304522645` | `+0.288067` | **Eliminated** |
| $c_8 \ge 1$ ($b=3.20$) | `13.3064790241` | `+0.164094` | **Eliminated** |
| $c_9 \ge 1$ ($b=3.20$) | `13.2067670001` | `+0.064382` | **Eliminated** |
| $c_{11} \ge 2$ ($b=3.20$ / peak) | `13.567542` / `13.584863` | `+0.425157` | **Eliminated** |
| $c_{13} \ge 2$ ($b=3.20$ / peak) | `13.351451` / `13.362611` | `+0.209066` | **Eliminated** |
| $c_{11} = 1$ ($b=3.20$) | `13.0577523491` | `-0.084633` | Survives ($c_{11}\le 1$) |
| $\mathrm{UB}_{\mathrm{sym}_2}$ ($\|\mathrm{Aut}(F)\|\ge 2$) | `12.4047600411` | `-0.190816` | **Eliminated** (vs. `12.595576`) |
| $\mathrm{UB}_{\mathrm{Eichler}}$ ($\psi(\mathfrak{n})\ge 12$) | `10.6842103581` | `-1.911365` | **Eliminated** (vs. `12.595576`) |
| $\mathrm{UB}_{\mathrm{Ram}}$ (cons. 100 / sharp 120) | `8.953803` / `8.818792` | `-3.776784` | **Eliminated** (vs. `12.595576`) |

Only `5` $2$-adic and `4` $3$-adic splitting types survive, pinning any remaining totally real octic candidate to the rigid asymmetric free core $d_F \in [633{,}448{,}978;\; 890{,}007{,}374]$ ($\mathrm{Aut}(F)=1$, $\mathrm{Ram}_{\mathrm{fin}}=\varnothing$, $\mathfrak{n}=(1)$, $|\zeta_F(-1)|=1536$).

---

## 6. Reproducibility Commands

```bash
# Plane 1: Pure Python 3.12 stdlib (7/7 gates + --check-only parity)
python3 papers/arithmetic_frontiers_closure/code/arithmetic_frontiers_verify.py --check-only --no-figs
sha256sum -c papers/arithmetic_frontiers_closure/data/MANIFEST.sha256

# Plane 2: Zero-crate pure Rust (6/6 integration tests + 6/6 suites)
(cd papers/arithmetic_frontiers_closure/rust && RUSTFLAGS="-D warnings" cargo test --release && cargo run --release)

# Plane 3: Dual-compiler freestanding zero-heap hardware-FENV C++20 (0-byte diff)
g++ -O2 -std=c++20 -frounding-math -ffp-contract=off -Wall -Wextra -Werror papers/arithmetic_frontiers_closure/cpp/fenv_oracle.cpp -o /tmp/pc4_gcc -lm
clang++ -O2 -std=c++20 -frounding-math -ffp-contract=off -Wall -Wextra -Werror papers/arithmetic_frontiers_closure/cpp/fenv_oracle.cpp -o /tmp/pc4_clang -lm
diff -u <(/tmp/pc4_gcc) <(/tmp/pc4_clang)

# Plane 4: Zero-Mathlib Lean 4.36.0 (18/18 theorems, 0 sorryAx, 0 ofReduceBool)
(cd papers/arithmetic_frontiers_closure/lean && lake build && .lake/build/bin/arithmetic-frontiers-lean)
```
