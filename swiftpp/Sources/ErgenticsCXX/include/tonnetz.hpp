#pragma once
#include <cstdint>
#include <cstddef>
#include "calibration.hpp"

namespace ergentics {

// First-principles Tonnetz / Prime Cadences engine (Sections 2-6).
// Vertex indexing: 0..11 = Major(r), 12..23 = Minor(r), r in Z_12.
// Move indexing: 0 = P, 1 = L, 2 = R.

struct TriadMoveResult {
    int32_t target_vertex;
    int32_t voice_step;      // semitone shift in {-2, -1, +1, +2}
    int32_t arriving_pitch;  // pitch class in 0..11 that arrives
    int32_t departing_pitch; // pitch class in 0..11 that departs
};

struct WindingDistribution {
    int32_t length_m;
    int32_t w_min;
    int32_t w_max;
    int64_t total_closed_walks; // N_m
    int64_t total_primes;       // pi(m)
    int64_t non_multiple_12_closed; // must be 0 (Thm 5.1 integrality check)
    int64_t closed_counts[17];  // N_m(w) indexed by w - w_min for |w| <= 8
    int64_t prime_counts[17];   // pi(m, w) indexed by w - w_min for |w| <= 8
};

struct FluxWindowReport {
    double edge_low;            // 4 * arccos(3/4)
    double edge_high;           // 2*pi - 4 * arccos(3/4)
    double max_eig_at_edge_low;
    double max_eig_at_pi;       // sqrt(5 + 2*sqrt(2))
    double min_eig_at_2pi_3;    // Dirac point = 0
    bool cyclic_ramanujan[13];  // for n = 1..12
};

struct TuneCheckReport {
    int64_t rooted_primes_checked;
    int64_t decode_failures;
    int64_t periodic_tune_failures;
    bool lemma_l1;
    bool lemma_l2;
    bool lemma_l3;
    bool backtrack_counterexample_confirmed;
};

struct EDOComparisonReport {
    double lambda_max_12;
    double lambda_max_31;
    double lambda_max_53;
    bool ramanujan_12;
    bool ramanujan_31;
    bool ramanujan_53;
};

TriadMoveResult apply_plr_move(int32_t vertex, int32_t move_id);
// Fill 24x24 adjacency matrix A (row-major, 576 doubles).
void build_adjacency_matrix(double* out_24x24);
// Fill 24x24 Laplacian L = 3I - A (row-major, 576 doubles).
void build_laplacian_matrix(double* out_24x24);
// Fill 2x2 Tonnetz Gram matrix G and exact covariance (1/2) G^{-1}.
void build_tonnetz_gram(double* out_2x2);
void build_tonnetz_covariance_per_step(double* out_2x2);
// Fill 24x24 twisted Hermitian adjacency A_phi (interleaved re, im: 2*576 doubles).
void build_twisted_adjacency_complex(double phi, double* out_interleaved_24x24);
// Exact max |lambda_k(phi)| from Theorem 5.2 closed form.
double twisted_max_eigenvalue(double phi);
// Evaluate Theorem 5.3 Riemann window and cyclic covers n = 1..12.
FluxWindowReport evaluate_flux_window();
// Exact Ihara-Bass check at parameter u: returns |det(I-uB) - (1-u^2)^12 det(I-uA+2u^2I)|.
double ihara_bass_residual(double u);
// Exact prime cadence count pi(m) and winding distribution pi(m, w) from scratch via 72-edge transfer matrix.
// Valid for even m in [2, 40].
WindingDistribution compute_exact_winding_distribution(int32_t m);
// Exact verification of Lemma 4.1 & Theorem 4.2 tune decoder on all rooted primes up to max_len (e.g. 12 or 16).
TuneCheckReport verify_tune_theorem(int32_t max_len);
// Compare major-triad graph spectral radius in 12-EDO, 31-EDO, and 53-EDO (NEG-M3).
EDOComparisonReport evaluate_edo_ramanujan_comparison();
// Exact exhaustive census of all 2^13 = 8192 signing classes of X (Remark 5.4 / RCT-1).
SigningCensusReport run_signing_census_exact();
// Keyed-PRNG RCT-3: non-backtracking walk null vs exact closed-walk & prime-cadence winding laws.
WindingNullRCTReport run_winding_null_rct(int32_t m, PRNGKey key, int64_t n_walks);

// Swift C++ interop helpers for fixed-size struct array access.
inline int64_t winding_prime_count(const WindingDistribution& wd, int32_t idx) {
    return (idx >= 0 && idx < 17) ? wd.prime_counts[idx] : 0;
}
inline int64_t winding_closed_count(const WindingDistribution& wd, int32_t idx) {
    return (idx >= 0 && idx < 17) ? wd.closed_counts[idx] : 0;
}
inline bool flux_cyclic_is_ramanujan(const FluxWindowReport& fw, int32_t n) {
    return (n >= 0 && n <= 12) ? fw.cyclic_ramanujan[n] : false;
}

} // namespace ergentics
