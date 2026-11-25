#pragma once
#include <cstdint>
#include <cstddef>

namespace ergentics {

// D-Type summation report comparing naive, reverse, Kahan, and Neumaier orders.
struct SummationSweepResult {
    double naive_forward;
    double naive_reverse;
    double kahan;
    double neumaier;
    double max_order_spread;
    bool all_finite;
};

// Exact integer arithmetic & anti-cancellation summation primitives.
int32_t mobius_mu(int32_t n);
int64_t gcd_i64(int64_t a, int64_t b);
double sum_naive_forward(const double* xs, std::size_t n);
double sum_naive_reverse(const double* xs, std::size_t n);
double sum_kahan(const double* xs, std::size_t n);
double sum_neumaier(const double* xs, std::size_t n);
SummationSweepResult run_summation_sweep(const double* xs, std::size_t n);

} // namespace ergentics
