#pragma once
#include <cstdint>
#include <cstddef>

namespace ergentics {

// Status codes for R-Type global runtime invariant guards.
enum InvariantCode : int32_t {
    INV_OK = 0,
    INV_EMPTY_INPUT = 1,
    INV_NON_FINITE = 2,
    INV_NOT_SYMMETRIC = 3,
    INV_NOT_POSITIVE_DEFINITE = 4,
    INV_CHOLESKY_FAILED = 5,
    INV_NOT_PSD = 6,
    INV_WRONG_NULLITY = 7,
    INV_CONSERVATION_VIOLATION = 8,
    INV_NEGATIVE_PROBABILITY = 9,
    INV_OUT_OF_DOMAIN = 10
};

struct MatrixInvariantReport {
    int32_t code;
    bool all_finite;
    bool diagonal_positive;
    bool symmetric;
    bool cholesky_ok;
    double max_asymmetry;
    double lambda_min;
    double lambda_max;
    int32_t zero_eigenvalue_count;
};

struct ConservationReport {
    int32_t code;
    bool all_finite;
    bool all_non_negative;
    double sum_value;
    double abs_error;
};

struct ExactConservationReport {
    int32_t code;
    bool all_non_negative;
    int64_t sum_value;
    int64_t expected_sum;
};

// R-Type global checks: reject NaN/Inf, check symmetry, run Cholesky and Jacobi eigensolve.
bool all_finite_f64(const double* xs, std::size_t n);
MatrixInvariantReport check_symmetric_pd(const double* a_row_major, std::size_t n, double sym_tol, double pd_tol);
MatrixInvariantReport check_symmetric_psd_nullity(
    const double* a_row_major, std::size_t n, int32_t expected_nullity, double sym_tol, double zero_tol
);
// Hermitian complex matrix check on interleaved (re, im) row-major entries (2*n*n doubles).
bool check_hermitian_complex(const double* interleaved, std::size_t n, double tol, double* out_max_err);
ConservationReport check_probability_simplex(const double* probs, std::size_t n, double sum_tol);
ExactConservationReport check_exact_integer_conservation(const int64_t* counts, std::size_t n, int64_t expected_total);

} // namespace ergentics
