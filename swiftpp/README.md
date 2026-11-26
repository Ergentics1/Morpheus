# Morpheus Swift++ Triple-Check Toolkit (`swiftpp/`)

First-principles **Code Model** (MIT License) implementation of the **Ergentics** verification core and *Prime Cadences* theorem checkers using the **Swift++ Triple-Check Method**:

| Lane | Target / Build | Description |
| :--- | :--- | :--- |
| **Lane 1 — Pure C++20** | `ErgenticsCXX` + `test_cxx_standalone` (`CMakeLists.txt`) | Standalone C++20 compiled with system `g++` and `clang++` (`-O2 -Wall -Wextra -Werror`) |
| **Lane 2 — Pure Swift 6.4** | `ErgenticsSwift` (`Package.swift`) | Independent idiomatic Swift 6.4 with **zero C++ imports** and zero C++ interop flags |
| **Lane 3 — Swift ↔ C++20 Interop** | `ErgenticsInterop` + `ErgenticsCLI` + 4 SWE-Sweep test suites | Live bidirectional Swift 6.4 ↔ C++20 interop (`.interoperabilityMode(.Cxx)`) cross-checking every turn against Lane 2 |

> **Non-conflation rule:** This directory contains **executable code only** — zero cached JSON tables or data blobs. Optional calibration JSON exports write strictly to an explicit external path (e.g. `data/calibrations/`).

## Build & Run Commands

### 1. Lane 1 — Standalone Pure C++20 (`g++` and `clang++`)

```bash
cmake -S swiftpp -B build/cxx-gcc -DCMAKE_CXX_COMPILER=g++
cmake --build build/cxx-gcc -j
ctest --test-dir build/cxx-gcc --output-on-failure -V

cmake -S swiftpp -B build/cxx-clang -DCMAKE_CXX_COMPILER=clang++
cmake --build build/cxx-clang -j
ctest --test-dir build/cxx-clang --output-on-failure -V
```

### 2. Lanes 2 & 3 — Pure Swift 6.4 + Live Swift ↔ C++20 Interop

On Linux with Swift 6.4, pass `--build-system native` (see `NEG-E4` in [`NEGATIVES.md`](../NEGATIVES.md)):

```bash
swift test --package-path swiftpp --build-system native
swift run --package-path swiftpp --build-system native ErgenticsCLI
```

To emit a schema-compliant calibration JSON record (matching [`CALIBRATIONS.md`](../CALIBRATIONS.md)) to the Data Model plane:

```bash
swift run --package-path swiftpp --build-system native -c release ErgenticsCLI \
  --commit "$(git rev-parse --short HEAD)" \
  --export-calibration data/calibrations/c2_winding_m40_swiftpp.json \
  --export-edgeworth data/calibrations/c2_edgeworth_m40_swiftpp.json \
  --export-theorem-d data/calibrations/theorem_d_pincer_swiftpp.json
```

## SWE-Sweep Coverage

- **`DeterministicTests` (`D-Type`):** Catastrophic floating-point cancellation sweep (naive forward/reverse vs. Kahan vs. Neumaier), exact Möbius $\mu(n)$ and GCD, 72-edge bidirectional Swift ↔ C++20 PLR involution round-trip, Ihara–Bass determinant identity, first-principles 72-edge transfer matrix up to $m=40$ ($\pi(40) = 54{,}975{,}717{,}792$, Correspondence `C-1`), Lemma 4.1 / Theorem 4.2 tune decoder + `NEG-M4` backtracking counterexample (`C-4`), Section 7 exact arithmetic (`section7.*` / `Section7.swift`: Thm 7.7 Bareiss + modular SNF `K(X)` & `NEG-E7`, Prop 7.2/Thm 7.8 `|Aut(X)| = 24` & Dhar gonality `gon(X) = 6`, Thm 3.5/Props 7.9–7.10 $P_{44}$ & direct $\mathbb{F}_{2^k}$ genus-5 curve point counts, Prop 3.7 Eisenstein conductor `12`, Thms 7.1/7.13 Schreier basis & Bruhat–Tits ball $r \le 7$), and **ADPIE Cycle 5 (`section7_cycle5.*` / `Section7Cycle5.swift`):** Novelty 3 **Theorem D** (from-scratch 64-pt Gauss–Legendre Poitou–Odlyzko Three-Pincer Hilbert class field obstruction unconditionally killing all $n \ge 9$, forcing $h_F = 1, u \le 4$ for $n = 7, 8$, and killing sextic $u \in \{16, 32\}$ to collapse `Open (2)`'s ceiling $6.67 \times 10^7 \to 2.65 \times 10^7$), exhaustive genus-13 Shimura curve census catching omitted **`NEG-E10` `X_0^690(1)`** (`19` pairs, `11` torsion-free, `4` $\Gamma_H$), exact Siegel + Gauss reduced-form $h^+(D)$ quadratic scan ($D \le 1200$, `Prop 7.18(a)`), exhaustive 504-element $PGL_2(\mathbb{F}_8)$ census (`56/56` order-3 free, `Prop 7.17(b)`), and `Prop 7.3` $\gamma_0^k$ obstruction (`0.000e+00` cross-lane delta across all 22 CLI checks).
- **`RuntimeTests` (`R-Type`):** Global symmetric PD via Cholesky + cyclic Jacobi eigensolver on Tonnetz Gram $G$ and $\operatorname{Cov} = \frac{1}{2}G^{-1}$, off-diagonal spike rejection despite positive diagonals, `NaN`/`±Inf` poisoning guards, Laplacian $3I-A$ PSD nullity $= 1$, twisted $A_\varphi$ Hermiticity, exact integer conservation $\sum_w \pi(m,w) = \pi(m)$, and simplex conservation.
- **`CalibrationTests` (`P-Type`, RCTs & Cycle 4 Novelties):** Full Rung-1 discrete Gaussian calibration (`C-2`), Edgeworth Ladder `C-2'` (**10.92×**) / `C-2''` (**75.30×**) and 2D Tonnetz isotropy/anisotropy across $W=-u, v, 4u+3v$ at $m=40$ (Theorem C, `novelty.*` / `Novelty.swift`), exhaustive Theorems A & B + `NEG-M11` sweep across all 948 chords $5 \le N \le 32$, flux window & cyclic cover Ramanujan boundary (`C-3`, `NEG-M2`), 12/31/53-EDO graph RH threshold (`NEG-M3`), exhaustive 8,192 signing census (`RCT-1`, `NEG-M9`), keyed 2-adic slope doubling vs. non-fixed control discs (`RCT-2`, `NEG-M10`), and keyed Monte Carlo non-backtracking walk null isolating the Möbius primitivity correction (`RCT-3`).
- **`SeamTests` (`D ↔ R ↔ P`):** Word-for-word bit-exact `KeyedPRNG` (FNV-1a + SplitMix64 + Xoshiro256**) lockstep between Pure Swift 6.4 and C++20, order-invariance across trials, and fail-closed `P → R → D` guarded handoffs rejecting indefinite covariance, `NaN`, out-of-domain flux, uncalibrated TV, and small-$m$ kurtosis violations.
