#pragma once
#include <cstdint>
#include <cstddef>
#include "invariants.hpp"
#include "calibration.hpp"

namespace ergentics {

// Guarded P -> R -> D seam contract: probabilistic/numerical estimator must pass
// finiteness, calibration bounds, and global PD covariance before driving deterministic kernels.
enum SeamCode : int32_t {
    SEAM_OK = 0,
    SEAM_REJECT_NON_FINITE = 1,
    SEAM_REJECT_UNCALIBRATED_TV = 2,
    SEAM_REJECT_UNCALIBRATED_KURTOSIS = 3,
    SEAM_REJECT_INDEFINITE_COV = 4,
    SEAM_REJECT_OOD_FLUX = 5,
    SEAM_REJECT_INVARIANT = 6
};

struct SeamPolicy {
    double max_tv;
    double max_abs_excess_kurtosis;
    double min_cov_eigenvalue;
    double flux_min;
    double flux_max;
};

struct SeamDecision {
    int32_t code;
    bool allowed;
    double deterministic_output; // populated only when allowed == true (else 0.0)
    double cov_lambda_min;
};

// Gate a probabilistic calibration + 2x2 covariance estimate + flux parameter before invoking
// the deterministic twisted spectral radius kernel.
SeamDecision guarded_flux_kernel_handoff(
    Rung1CalibrationReport cal,
    const double* cov_2x2_row_major,
    double flux_phi,
    SeamPolicy policy
);

} // namespace ergentics
