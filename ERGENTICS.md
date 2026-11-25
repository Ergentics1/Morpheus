# Ergentics Library & Swift++ Triple-Check Spec

Design and organization blueprint for the **Ergentics** core library (`ergentics/`) and **Swift++** Triple-Check workspace (`swiftpp/`).

> **Scope:** Both `ergentics/` and `swiftpp/` belong strictly to the **Code Model** (MIT License). Lay out code deeply and clearly, keep comments tight and to the point, and store all generated datasets/calibration outputs outside source trees under `data/` (CC BY 4.0).

## 1. What Is Swift++? (The Triple-Check Method)

**Swift++** is a **three-way cross-check coding method** using live Swift ↔ C++ interoperability at every turn, continuously compared against both standalone languages:

| Lane | Execution Path | What It Catches |
| :--- | :--- | :--- |
| **Lane 1 — Pure C++20** | Standalone C++20 compiled with `g++` / `clang++` | Reference low-level numerical/memory behavior without Swift runtime overhead |
| **Lane 2 — Pure Swift 6.4** | Independent idiomatic Swift 6.4 with zero C++ calls | Logic bugs, signedness/overflow errors, independent algorithmic verification |
| **Lane 3 — Swift ↔ C++ Interop** | Live bidirectional Swift 6.4 ↔ C++20 interop (`.interoperabilityMode(.Cxx)`) at every turn | ABI/struct-layout mismatches, bridging/ownership bugs, FMA/rounding divergence, and boundary seam leaks |

**Triple-Check Invariant:** For every step/turn of an algorithm or verifier, all three lanes (`Pure C++`, `Pure Swift`, and `Swift ↔ C++ Interop`) must agree within exact algebraic equality (`D-Type`) or identical quantified bounds (`R-Type`, `P-Type`, keyed-PRNG `Seam` bit-exact replay).

## 2. Ergentics Core Library (`ergentics/`)

Shared mathematical and verification contracts implemented cleanly across the Code Model (`swiftpp/`, `rust/`, `lean/`):

| Module | Verification Role | Core Responsibilities |
| :--- | :--- | :--- |
| `correspondence` | Core Thesis | Dimensionless regime structs, exact-vs-limiting mismatch evaluators, monotone error-bound assertions (`C-1`–`C-4`) |
| `invariants` | `R-Type` Runtime | Symmetric PD verification ($\lambda_{\min} > 0$ & Cholesky), PSD nullity check, Hermiticity check, `NaN`/`±Inf` poisoning guards, aggregate conservation validators |
| `calibration` | `P-Type` Rung-1 & RCT | Full distributional metrics (TV, KL, KS, $W_1$, skewness, excess kurtosis, tail coverage) and pre-registered RCT control runners |
| `seam` | `D ↔ R ↔ P` Seams | Domain-separated keyed PRNG streams (bit-exact replay invariant to test order) and validated `P → R → D` boundary wrappers |

### Library Rules

- **Zero hidden global state:** No global RNGs, no mutable process-wide tolerances, no implicit reads from cached `.json` artifacts.
- **Explicit failure semantics:** Runtime guards (`invariants`, `seam`) return typed errors on `NaN`, `±Inf`, indefinite matrices, conservation violations, or uncalibrated/OOD inputs — never silently clamp component-wise.
- **Deep code, tight comments:** Lay out algorithms transparently with concise docstrings stating exact preconditions, postconditions, and invariants.

## 3. Swift++ Workspace Layout (`swiftpp/`)

```text
swiftpp/
├── README.md                    # Swift++ Triple-Check build & test commands
├── Package.swift                # Swift 6.4 SwiftPM manifest (.interoperabilityMode(.Cxx))
├── CMakeLists.txt               # Standalone Pure C++20 build & test target (g++ / clang++)
├── Sources/
│   ├── ErgenticsCoreCXX/        # Lane 1: Pure C++20 headers & kernels (+ module.modulemap)
│   │   ├── include/
│   │   │   ├── module.modulemap
│   │   │   └── ergentics_cxx.hpp
│   │   └── src/
│   ├── ErgenticsCoreSwift/      # Lane 2: Independent Pure Swift 6.4 implementation
│   ├── ErgenticsInterop/        # Lane 3: Live Swift 6.4 ↔ C++20 interop bridge at every turn
│   └── PrimeCadencesTriple/     # 3-way runner comparing C++ vs Swift vs Swift↔C++ interop
└── Tests/
    ├── DeterministicTests/      # D-Type: 3-way exact & adversarial float-cancellation sweeps
    ├── RuntimeTests/            # R-Type: 3-way global PD/PSD/conservation & fault injection
    ├── CalibrationTests/        # P-Type: 3-way Rung-1 distributional calibration & keyed RCTs
    └── SeamTests/               # D ↔ R ↔ P: 3-way bit-exact keyed PRNG & ABI seam checks
```

### Toolchain & Data Hygiene

- **Compiler split:** Swift 6.4.3 (`swiftly`) is appended to `PATH` so system `g++ 13.3` / `clang++ 18.1` stay default for standalone **Lane 1 (Pure C++20)** builds, while `swift build --build-system native` / `swift test --build-system native` execute **Lane 2 (Pure Swift)** and **Lane 3 (Swift ↔ C++20 Interop)** cleanly on Linux (avoiding Swift 6.4's `SWBBuildService` container clock trap).
- **Data separation:** `swiftpp/` never stores or reads mutable cached data inside `Sources/` or `Tests/`. Any emitted calibration or benchmark outputs write through explicit CLI flags to `data/calibrations/` (CC BY 4.0) with SHA-256 manifest updates.
