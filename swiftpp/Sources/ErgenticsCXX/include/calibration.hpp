#pragma once
#include <cstdint>
#include <cstddef>
#include "keyed_prng.hpp"

namespace ergentics {

// Correspondence Principle evaluation inside a dimensionless regime.
struct CorrespondenceCheck {
    double deeper_value;
    double older_value;
    double regime_param;
    double abs_error;
    double rel_error;
    double bound_value;
    bool finite;
    bool within_bound;
};

// Full Rung-1 distributional calibration vector (beyond point estimates).
struct Rung1CalibrationReport {
    int32_t code;              // 0 = OK, nonzero = R-Type invariant rejection
    double total_variation;    // 0.5 * sum |P - Q|
    double kl_divergence;      // sum_{P>0} P log(P / Q)
    double ks_distance;        // sup |F_P - F_Q|
    double wasserstein_1;      // sum |F_P - F_Q| * dw (unit integer support step)
    double mean;
    double variance;
    double skewness;
    double excess_kurtosis;    // mu_4 / sigma^4 - 3
    double cov_1sigma;         // P(|W - mu| <= 1*sigma)
    double cov_2sigma;         // P(|W - mu| <= 2*sigma)
    double cov_3sigma;         // P(|W - mu| <= 3*sigma)
    double simplex_error;      // |sum(P) - 1|
};

// RCT paired treatment-vs-control summary for Lemma 7.14 (2-adic edge-length doubling).
struct TwoAdicRCTReport {
    int64_t treatment_samples;
    int64_t treatment_slope2_hits;
    int64_t control_samples;
    int64_t control_slope1_hits;
    bool passed;
};

// RCT-1 signing census summary (Remark 5.4: voice-parity vs all 8191 nontrivial signings).
struct SigningCensusReport {
    int64_t total_classes;       // 8192
    int64_t nontrivial_classes;  // 8191
    int64_t ramanujan_nontrivial;// 7675
    int64_t voice_parity_rank;   // 7372 (count of signing classes with strictly smaller max|lambda|, of 8192)
    double best_max_eig;         // 1 + sqrt(2)
    double voice_parity_max_eig; // sqrt(5 + 2*sqrt(2))
    bool passed;
};

// RCT-3 keyed Monte Carlo non-backtracking walk null vs exact closed-walk & prime-cadence laws.
struct WindingNullRCTReport {
    int32_t length_m;
    int64_t total_walks_sampled;
    int64_t closed_walks_observed;
    int64_t non_multiple_12_observed;
    double mc_vs_exact_closed_tv;    // TV(MC closed walks, exact N_m(w)/N_m)
    double exact_closed_vs_prime_tv; // exact Mobius primitivity correction TV(N_m/N_m, pi_m/pi_m)
    double mc_mean;
    double mc_variance;
    bool passed;
};

CorrespondenceCheck evaluate_correspondence(
    double deeper_value, double older_value, double regime_param, double bound_value
);

// Evaluate full Rung-1 calibration of discrete probabilities P on integer support [w_min..w_max]
// against Gaussian N(0, sigma2) discretized via normalized density Q(w) proportional to exp(-w^2/(2*sigma2)).
Rung1CalibrationReport evaluate_discrete_gaussian_calibration(
    const double* probs, std::size_t n, int32_t w_min, double sigma2
);

// Keyed-PRNG RCT for 2-adic slope doubling on fixed discs (|2c|<r) vs non-fixed control discs (|2c|>r).
TwoAdicRCTReport run_two_adic_slope_rct(PRNGKey treatment_key, PRNGKey control_key, int64_t n_samples);

} // namespace ergentics
