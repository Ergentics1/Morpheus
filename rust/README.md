# Morpheus Rust Exact Arithmetic & General $N$-EDO Verifier (`rust/`)

Zero-dependency **Code Model** (MIT License) fourth-language verifier in Rust (`rustc 1.100.0`). Recomputes every claim from first principles with zero reads of cached data files.

## Verified Theorems

- **Theorem 3.4 (`src/cyclotomic.rs`):** Exact $\mathbb{Z}[\zeta_{12}] = \mathbb{Z}[x]/(x^4 - x^2 + 1)$ arithmetic for all 12 Fourier coefficients $f_k$: $f_3 = 2 - i$, $f_9 = 2 + i$, $f_4 = 1 + 2\omega$ ($f_4^2 = -3$), $f_1$ minimal polynomial $x^4 - 2x^3 + 2x^2 + 2x + 1 = 0$, unit norm $N(f_1) = 1$, $|f_5|^2 = 2 + \sqrt{3}$, Galois action $\sigma_a(f_k) = f_{ak}$, $M_{11}$ graph automorphism, and $M_7$ bijection onto the 24 `[0, 1, 4]` chords & 36 flip edges.
- **Theorem 7.4 & Corollary 7.5 (`src/tower.rs`):** Exact $\mathbb{Z}/12\mathbb{Z}$ voltage cover $X \to \Theta$ across all 36 edges ($P:+4, L:0, R:+1$), loop lifts $(6, 8, 24)$, and exact $\mathbb{Z}[\zeta_{12}][u]$ Artin–Ihara character factorization by order $d \in \{1, 2, 3, 4, 6, 12\}$.
- **Theorem 4.2 (`src/tune_general.rs`):** Local tune decoder verified across all **174,864** rooted primes of length $m \le 16$ (of which **131,136** have length $m = 16$; `0` failures).
- **Theorem 4.3 / Correspondence `C-4` (`src/tune_general.rs`):** Exact held-note link-graph cycle criterion verified across all **6,028** $(N, S, \mathcal{C})$ tuning systems for $5 \le N \le 72$ (`0` counterexamples) and extended to **11,452** systems for $5 \le N \le 96$ via `--n-max 96` (`0` counterexamples).
- **Fourth-Language Cross-Oracle (`src/swe_sweep.rs`, `src/keyed_prng.rs`):** Independent cross-check of $\pi(40) = 54{,}975{,}717{,}792$, Rung-1 TV/excess-kurtosis, anti-cancellation summation, global PD/Cholesky spike & `NaN` guards, and bit-exact `KeyedPRNG` parity with C++20 and Pure Swift 6.4.
- **ADPIE Cycle 4 Original Novelties (`src/novelty.rs`):**
  - **Theorems A, B, Cor B.1 & `NEG-M11`:** Exhaustive maximal-$S_{\max}(c_0)$ sweep across all **10,576** 3-note chord classes for $5 \le N \le 72$ (covering all $2^{\lfloor N/2\rfloor}$ step sets by monotonicity): `max|L0∩Lt| = 2`, `T_fail = 0`, exact 9 octatonic $T/I$ diameter witnesses at $N = 8, 16, \dots, 72$, `TI_unexp = 0`, and explicit `NEG-M11` counterexample ($N=8, S=\{2\}, c_0=\{0,1,4\}$).
  - **Theorem C (`C-2'` / `C-2''`):** Exact 72-edge transfer-matrix verification at $m = 40$ across bond-parallel armchair axes ($W = -u$, $v$) and bond-perpendicular zigzag axis ($4u + 3v$), confirming universal 4th-cumulant rotational isotropy ($m\kappa_{\mathrm{ex}} \to -8.5$) and **10.92×** (`C-2'`) / **75.30×** (`C-2''`) TV reduction.

## Build & Run

```bash
cargo test --manifest-path rust/Cargo.toml --release
cargo run --manifest-path rust/Cargo.toml --release
```
