#include "ergentics_cxx.hpp"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <limits>
#include <numeric>
#include <vector>

namespace ergentics {

namespace {

constexpr double kPi = 3.141592653589793238462643383279502884;
constexpr double kRamanujan3 = 2.828427124746190097603377448419396157; // 2*sqrt(2)

// Cyclic Jacobi eigensolver for real symmetric n x n matrices (row-major).
bool jacobi_eigenvalues(std::vector<double> a, std::size_t n, std::vector<double>& out_eigs) {
    if (n == 0) return false;
    for (double v : a) {
        if (!std::isfinite(v)) return false;
    }
    constexpr int max_sweeps = 120;
    for (int sweep = 0; sweep < max_sweeps; ++sweep) {
        double off_norm = 0.0;
        for (std::size_t p = 0; p < n; ++p) {
            for (std::size_t q = p + 1; q < n; ++q) {
                double apq = a[p * n + q];
                off_norm += apq * apq;
            }
        }
        if (std::sqrt(2.0 * off_norm) <= 1e-13) break;

        for (std::size_t p = 0; p < n; ++p) {
            for (std::size_t q = p + 1; q < n; ++q) {
                double apq = a[p * n + q];
                if (std::abs(apq) <= 1e-16) continue;
                double app = a[p * n + p];
                double aqq = a[q * n + q];
                double tau = (aqq - app) / (2.0 * apq);
                double t = (tau >= 0.0)
                    ? (1.0 / (tau + std::sqrt(1.0 + tau * tau)))
                    : (-1.0 / (-tau + std::sqrt(1.0 + tau * tau)));
                double c = 1.0 / std::sqrt(1.0 + t * t);
                double s = t * c;

                a[p * n + p] = app - t * apq;
                a[q * n + q] = aqq + t * apq;
                a[p * n + q] = 0.0;
                a[q * n + p] = 0.0;

                for (std::size_t r = 0; r < n; ++r) {
                    if (r == p || r == q) continue;
                    double arp = a[r * n + p];
                    double arq = a[r * n + q];
                    double nrp = c * arp - s * arq;
                    double nrq = s * arp + c * arq;
                    a[r * n + p] = nrp;
                    a[p * n + r] = nrp;
                    a[r * n + q] = nrq;
                    a[q * n + r] = nrq;
                }
            }
        }
    }
    out_eigs.resize(n);
    for (std::size_t i = 0; i < n; ++i) {
        if (!std::isfinite(a[i * n + i])) return false;
        out_eigs[i] = a[i * n + i];
    }
    std::sort(out_eigs.begin(), out_eigs.end());
    return true;
}

bool cholesky_pd_check(const double* a, std::size_t n, double pd_tol) {
    std::vector<double> L(n * n, 0.0);
    for (std::size_t i = 0; i < n; ++i) {
        for (std::size_t j = 0; j <= i; ++j) {
            double sum = 0.0;
            for (std::size_t k = 0; k < j; ++k) {
                sum += L[i * n + k] * L[j * n + k];
            }
            if (i == j) {
                double d = a[i * n + i] - sum;
                if (!std::isfinite(d) || d <= pd_tol) return false;
                L[i * n + j] = std::sqrt(d);
            } else {
                double val = (a[i * n + j] - sum) / L[j * n + j];
                if (!std::isfinite(val)) return false;
                L[i * n + j] = val;
            }
        }
    }
    return true;
}

// Determinant via Gaussian elimination with partial pivoting.
double det_lu(std::vector<double> m, std::size_t n) {
    double sign = 1.0;
    for (std::size_t k = 0; k < n; ++k) {
        std::size_t piv = k;
        double best = std::abs(m[k * n + k]);
        for (std::size_t i = k + 1; i < n; ++i) {
            double v = std::abs(m[i * n + k]);
            if (v > best) {
                best = v;
                piv = i;
            }
        }
        if (best == 0.0) return 0.0;
        if (piv != k) {
            for (std::size_t j = k; j < n; ++j) {
                std::swap(m[k * n + j], m[piv * n + j]);
            }
            sign = -sign;
        }
        double diag = m[k * n + k];
        for (std::size_t i = k + 1; i < n; ++i) {
            double f = m[i * n + k] / diag;
            for (std::size_t j = k + 1; j < n; ++j) {
                m[i * n + j] -= f * m[k * n + j];
            }
        }
    }
    double det = sign;
    for (std::size_t i = 0; i < n; ++i) det *= m[i * n + i];
    return det;
}

int32_t v2_i64(int64_t x) {
    if (x == 0) return 1000000;
    uint64_t u = (x < 0) ? static_cast<uint64_t>(-x) : static_cast<uint64_t>(x);
    int32_t c = 0;
    while ((u & 1ULL) == 0ULL) {
        u >>= 1ULL;
        ++c;
    }
    return c;
}

std::array<int32_t, 3> triad_notes(int32_t v) {
    int32_t r = v % 12;
    if (v < 12) {
        return {r, (r + 4) % 12, (r + 7) % 12};
    }
    return {r, (r + 3) % 12, (r + 7) % 12};
}

// Lookup triad index (0..23) from unordered 3-note pitch-class set, or -1 if not consonant.
int32_t triad_from_notes(int32_t a, int32_t b, int32_t c) {
    if (a == b || b == c || a == c) return -1;
    uint32_t mask = (1U << a) | (1U << b) | (1U << c);
    for (int32_t v = 0; v < 24; ++v) {
        auto ns = triad_notes(v);
        uint32_t vm = (1U << ns[0]) | (1U << ns[1]) | (1U << ns[2]);
        if (vm == mask) return v;
    }
    return -1;
}

} // namespace

// --- Deterministic (D-Type) ---

int32_t mobius_mu(int32_t n) {
    if (n <= 0) return 0;
    int32_t mu = 1;
    int32_t x = n;
    for (int32_t p = 2; p * p <= x; ++p) {
        if (x % p == 0) {
            x /= p;
            if (x % p == 0) return 0;
            mu = -mu;
        }
    }
    if (x > 1) mu = -mu;
    return mu;
}

int64_t gcd_i64(int64_t a, int64_t b) {
    a = (a < 0) ? -a : a;
    b = (b < 0) ? -b : b;
    while (b != 0) {
        int64_t t = a % b;
        a = b;
        b = t;
    }
    return a;
}

double sum_naive_forward(const double* xs, std::size_t n) {
    double s = 0.0;
    for (std::size_t i = 0; i < n; ++i) s += xs[i];
    return s;
}

double sum_naive_reverse(const double* xs, std::size_t n) {
    double s = 0.0;
    for (std::size_t i = n; i > 0; --i) s += xs[i - 1];
    return s;
}

double sum_kahan(const double* xs, std::size_t n) {
    double sum = 0.0;
    double c = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        double y = xs[i] - c;
        double t = sum + y;
        c = (t - sum) - y;
        sum = t;
    }
    return sum;
}

double sum_neumaier(const double* xs, std::size_t n) {
    double sum = 0.0;
    double c = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        double x = xs[i];
        double t = sum + x;
        if (std::abs(sum) >= std::abs(x)) {
            c += (sum - t) + x;
        } else {
            c += (x - t) + sum;
        }
        sum = t;
    }
    return sum + c;
}

SummationSweepResult run_summation_sweep(const double* xs, std::size_t n) {
    SummationSweepResult res{};
    res.all_finite = all_finite_f64(xs, n);
    res.naive_forward = sum_naive_forward(xs, n);
    res.naive_reverse = sum_naive_reverse(xs, n);
    res.kahan = sum_kahan(xs, n);
    res.neumaier = sum_neumaier(xs, n);
    double vals[4] = {res.naive_forward, res.naive_reverse, res.kahan, res.neumaier};
    double lo = vals[0], hi = vals[0];
    for (int i = 1; i < 4; ++i) {
        if (vals[i] < lo) lo = vals[i];
        if (vals[i] > hi) hi = vals[i];
    }
    res.max_order_spread = hi - lo;
    return res;
}

// --- Runtime Global Invariants (R-Type) ---

bool all_finite_f64(const double* xs, std::size_t n) {
    if (!xs && n > 0) return false;
    for (std::size_t i = 0; i < n; ++i) {
        if (!std::isfinite(xs[i])) return false;
    }
    return true;
}

MatrixInvariantReport check_symmetric_pd(const double* a, std::size_t n, double sym_tol, double pd_tol) {
    MatrixInvariantReport rep{};
    if (!a || n == 0) {
        rep.code = INV_EMPTY_INPUT;
        return rep;
    }
    rep.all_finite = all_finite_f64(a, n * n);
    if (!rep.all_finite) {
        rep.code = INV_NON_FINITE;
        return rep;
    }
    rep.diagonal_positive = true;
    for (std::size_t i = 0; i < n; ++i) {
        if (a[i * n + i] <= pd_tol) rep.diagonal_positive = false;
    }
    double max_asym = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        for (std::size_t j = i + 1; j < n; ++j) {
            double d = std::abs(a[i * n + j] - a[j * n + i]);
            if (d > max_asym) max_asym = d;
        }
    }
    rep.max_asymmetry = max_asym;
    rep.symmetric = (max_asym <= sym_tol);
    if (!rep.symmetric) {
        rep.code = INV_NOT_SYMMETRIC;
        return rep;
    }

    std::vector<double> sym(n * n);
    for (std::size_t i = 0; i < n; ++i) {
        for (std::size_t j = 0; j < n; ++j) {
            sym[i * n + j] = 0.5 * (a[i * n + j] + a[j * n + i]);
        }
    }
    std::vector<double> eigs;
    if (!jacobi_eigenvalues(sym, n, eigs)) {
        rep.code = INV_NON_FINITE;
        return rep;
    }
    rep.lambda_min = eigs.front();
    rep.lambda_max = eigs.back();
    int32_t zcnt = 0;
    for (double ev : eigs) {
        if (std::abs(ev) <= pd_tol) ++zcnt;
    }
    rep.zero_eigenvalue_count = zcnt;
    rep.cholesky_ok = cholesky_pd_check(sym.data(), n, pd_tol);

    if (rep.lambda_min <= pd_tol) {
        rep.code = INV_NOT_POSITIVE_DEFINITE;
    } else if (!rep.cholesky_ok) {
        rep.code = INV_CHOLESKY_FAILED;
    } else {
        rep.code = INV_OK;
    }
    return rep;
}

MatrixInvariantReport check_symmetric_psd_nullity(
    const double* a, std::size_t n, int32_t expected_nullity, double sym_tol, double zero_tol
) {
    MatrixInvariantReport rep{};
    if (!a || n == 0) {
        rep.code = INV_EMPTY_INPUT;
        return rep;
    }
    rep.all_finite = all_finite_f64(a, n * n);
    if (!rep.all_finite) {
        rep.code = INV_NON_FINITE;
        return rep;
    }
    rep.diagonal_positive = true;
    for (std::size_t i = 0; i < n; ++i) {
        if (a[i * n + i] < -zero_tol) rep.diagonal_positive = false;
    }
    double max_asym = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        for (std::size_t j = i + 1; j < n; ++j) {
            double d = std::abs(a[i * n + j] - a[j * n + i]);
            if (d > max_asym) max_asym = d;
        }
    }
    rep.max_asymmetry = max_asym;
    rep.symmetric = (max_asym <= sym_tol);
    if (!rep.symmetric) {
        rep.code = INV_NOT_SYMMETRIC;
        return rep;
    }

    std::vector<double> sym(n * n);
    for (std::size_t i = 0; i < n; ++i) {
        for (std::size_t j = 0; j < n; ++j) {
            sym[i * n + j] = 0.5 * (a[i * n + j] + a[j * n + i]);
        }
    }
    std::vector<double> eigs;
    if (!jacobi_eigenvalues(sym, n, eigs)) {
        rep.code = INV_NON_FINITE;
        return rep;
    }
    rep.lambda_min = eigs.front();
    rep.lambda_max = eigs.back();
    int32_t zcnt = 0;
    for (double ev : eigs) {
        if (std::abs(ev) <= zero_tol) ++zcnt;
    }
    rep.zero_eigenvalue_count = zcnt;
    rep.cholesky_ok = (rep.lambda_min > zero_tol);

    if (rep.lambda_min < -zero_tol) {
        rep.code = INV_NOT_PSD;
    } else if (zcnt != expected_nullity) {
        rep.code = INV_WRONG_NULLITY;
    } else {
        rep.code = INV_OK;
    }
    return rep;
}

bool check_hermitian_complex(const double* interleaved, std::size_t n, double tol, double* out_max_err) {
    if (!interleaved || n == 0 || !all_finite_f64(interleaved, 2 * n * n)) {
        if (out_max_err) *out_max_err = std::numeric_limits<double>::quiet_NaN();
        return false;
    }
    double max_err = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        double diag_im = std::abs(interleaved[2 * (i * n + i) + 1]);
        if (diag_im > max_err) max_err = diag_im;
        for (std::size_t j = i + 1; j < n; ++j) {
            double re_ij = interleaved[2 * (i * n + j)];
            double im_ij = interleaved[2 * (i * n + j) + 1];
            double re_ji = interleaved[2 * (j * n + i)];
            double im_ji = interleaved[2 * (j * n + i) + 1];
            double er = std::abs(re_ij - re_ji);
            double ei = std::abs(im_ij + im_ji);
            if (er > max_err) max_err = er;
            if (ei > max_err) max_err = ei;
        }
    }
    if (out_max_err) *out_max_err = max_err;
    return max_err <= tol;
}

ConservationReport check_probability_simplex(const double* probs, std::size_t n, double sum_tol) {
    ConservationReport rep{};
    if (!probs || n == 0) {
        rep.code = INV_EMPTY_INPUT;
        return rep;
    }
    rep.all_finite = all_finite_f64(probs, n);
    if (!rep.all_finite) {
        rep.code = INV_NON_FINITE;
        return rep;
    }
    rep.all_non_negative = true;
    for (std::size_t i = 0; i < n; ++i) {
        if (probs[i] < 0.0) rep.all_non_negative = false;
    }
    rep.sum_value = sum_neumaier(probs, n);
    rep.abs_error = std::abs(rep.sum_value - 1.0);
    if (!rep.all_non_negative) {
        rep.code = INV_NEGATIVE_PROBABILITY;
    } else if (rep.abs_error > sum_tol) {
        rep.code = INV_CONSERVATION_VIOLATION;
    } else {
        rep.code = INV_OK;
    }
    return rep;
}

ExactConservationReport check_exact_integer_conservation(const int64_t* counts, std::size_t n, int64_t expected_total) {
    ExactConservationReport rep{};
    rep.expected_sum = expected_total;
    if (!counts || n == 0) {
        rep.code = INV_EMPTY_INPUT;
        return rep;
    }
    rep.all_non_negative = true;
    int64_t acc = 0;
    for (std::size_t i = 0; i < n; ++i) {
        if (counts[i] < 0) rep.all_non_negative = false;
        acc += counts[i];
    }
    rep.sum_value = acc;
    if (!rep.all_non_negative) {
        rep.code = INV_NEGATIVE_PROBABILITY;
    } else if (acc != expected_total) {
        rep.code = INV_CONSERVATION_VIOLATION;
    } else {
        rep.code = INV_OK;
    }
    return rep;
}

// --- Probabilistic Calibration & Correspondence (P-Type) ---

CorrespondenceCheck evaluate_correspondence(
    double deeper_value, double older_value, double regime_param, double bound_value
) {
    CorrespondenceCheck c{};
    c.deeper_value = deeper_value;
    c.older_value = older_value;
    c.regime_param = regime_param;
    c.bound_value = bound_value;
    c.finite = std::isfinite(deeper_value) && std::isfinite(older_value) &&
               std::isfinite(regime_param) && std::isfinite(bound_value) && (bound_value >= 0.0);
    if (!c.finite) {
        c.abs_error = std::numeric_limits<double>::quiet_NaN();
        c.rel_error = std::numeric_limits<double>::quiet_NaN();
        c.within_bound = false;
        return c;
    }
    c.abs_error = std::abs(deeper_value - older_value);
    double denom = std::abs(older_value);
    c.rel_error = (denom > 0.0) ? (c.abs_error / denom) : c.abs_error;
    c.within_bound = (c.abs_error <= bound_value);
    return c;
}

Rung1CalibrationReport evaluate_discrete_gaussian_calibration(
    const double* probs, std::size_t n, int32_t w_min, double sigma2
) {
    Rung1CalibrationReport rep{};
    if (!std::isfinite(sigma2) || sigma2 <= 0.0) {
        rep.code = INV_OUT_OF_DOMAIN;
        return rep;
    }
    ConservationReport sim = check_probability_simplex(probs, n, 1e-12);
    rep.simplex_error = sim.abs_error;
    if (sim.code != INV_OK) {
        rep.code = sim.code;
        return rep;
    }

    // Discretized Gaussian reference Q(w) proportional to exp(-w^2 / (2*sigma2)) over Z.
    int32_t w_max = w_min + static_cast<int32_t>(n) - 1;
    int32_t ext_lo = std::min(w_min, -12) - 12;
    int32_t ext_hi = std::max(w_max, 12) + 12;
    double z_norm = 0.0;
    for (int32_t w = ext_lo; w <= ext_hi; ++w) {
        z_norm += std::exp(-0.5 * static_cast<double>(w * w) / sigma2);
    }

    std::vector<double> q(n, 0.0);
    for (std::size_t i = 0; i < n; ++i) {
        double w = static_cast<double>(w_min + static_cast<int32_t>(i));
        q[i] = std::exp(-0.5 * w * w / sigma2) / z_norm;
    }
    double q_mass_inside = sum_neumaier(q.data(), n);
    double q_tail_outside = std::max(0.0, 1.0 - q_mass_inside);

    // Total variation, KL, KS, and Wasserstein-1.
    double tv_sum = q_tail_outside;
    double kl = 0.0;
    double cdf_p = 0.0;
    double cdf_q = 0.5 * q_tail_outside;
    double ks = cdf_q;
    double w1 = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        double pi = probs[i];
        double qi = q[i];
        tv_sum += std::abs(pi - qi);
        if (pi > 0.0) {
            kl += pi * std::log(pi / qi);
        }
        cdf_p += pi;
        cdf_q += qi;
        double diff = std::abs(cdf_p - cdf_q);
        if (diff > ks) ks = diff;
        if (i + 1 < n) w1 += diff;
    }
    rep.total_variation = 0.5 * tv_sum;
    rep.kl_divergence = kl;
    rep.ks_distance = ks;
    rep.wasserstein_1 = w1;

    // Moments and tail coverage.
    double mean = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        mean += probs[i] * static_cast<double>(w_min + static_cast<int32_t>(i));
    }
    double m2 = 0.0, m3 = 0.0, m4 = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        double d = static_cast<double>(w_min + static_cast<int32_t>(i)) - mean;
        double d2 = d * d;
        m2 += probs[i] * d2;
        m3 += probs[i] * d2 * d;
        m4 += probs[i] * d2 * d2;
    }
    rep.mean = mean;
    rep.variance = m2;
    double sigma = std::sqrt(std::max(0.0, m2));
    if (sigma > 0.0) {
        rep.skewness = m3 / (sigma * sigma * sigma);
        rep.excess_kurtosis = m4 / (m2 * m2) - 3.0;
        double c1 = 0.0, c2 = 0.0, c3 = 0.0;
        for (std::size_t i = 0; i < n; ++i) {
            double ad = std::abs(static_cast<double>(w_min + static_cast<int32_t>(i)) - mean);
            if (ad <= sigma) c1 += probs[i];
            if (ad <= 2.0 * sigma) c2 += probs[i];
            if (ad <= 3.0 * sigma) c3 += probs[i];
        }
        rep.cov_1sigma = c1;
        rep.cov_2sigma = c2;
        rep.cov_3sigma = c3;
    }
    rep.code = INV_OK;
    return rep;
}

TwoAdicRCTReport run_two_adic_slope_rct(PRNGKey treatment_key, PRNGKey control_key, int64_t n_samples) {
    TwoAdicRCTReport rep{};
    if (n_samples <= 0) return rep;

    // Treatment arm: fixed discs (|2c|_2 < r, i.e. v2(2c) > k) -> slope 2 (v2(z^2 - c^2) == 2k).
    KeyedPRNG rng_t = KeyedPRNG::from_key(treatment_key);
    for (int64_t i = 0; i < n_samples; ++i) {
        int64_t num = static_cast<int64_t>(rng_t.next_bounded(999ULL) + 1ULL);
        int32_t den_exp = static_cast<int32_t>(rng_t.next_bounded(7ULL)); // 0..6
        if (rng_t.next_bounded(2ULL) == 1ULL) num = -num;
        int32_t v2_2c = 1 + v2_i64(num) - den_exp;
        // Pick k strictly below v2(2c) so |2c|_2 < 2^{-k} = r.
        int32_t k = v2_2c - 1 - static_cast<int32_t>(rng_t.next_bounded(4ULL));
        int64_t odd_u = static_cast<int64_t>(2ULL * rng_t.next_bounded(6ULL) + 1ULL); // 1,3,5,7,9,11
        // Compute v2(u * (2c + u)) exactly: u = odd_u * 2^k, 2c = num * 2^(1 - den_exp).
        // Shift both terms by min_exp so integer sum is exact.
        int32_t exp_2c = 1 - den_exp;
        int32_t min_e = std::min(exp_2c, k);
        int64_t t_2c = num << (exp_2c - min_e);
        int64_t t_u = odd_u << (k - min_e);
        int32_t v2_sum = min_e + v2_i64(t_2c + t_u);
        int32_t v2_prod = k + v2_sum; // v2(u) + v2(2c + u)
        ++rep.treatment_samples;
        if (v2_prod == 2 * k) ++rep.treatment_slope2_hits;
    }

    // Negative control arm: non-fixed discs (|2c|_2 > r, i.e. v2(2c) < k) -> slope 1 (v2 == v2(2c) + k).
    KeyedPRNG rng_c = KeyedPRNG::from_key(control_key);
    for (int64_t i = 0; i < n_samples; ++i) {
        int64_t num = static_cast<int64_t>(rng_c.next_bounded(999ULL) + 1ULL);
        int32_t den_exp = static_cast<int32_t>(rng_c.next_bounded(7ULL));
        int32_t v2_2c = 1 + v2_i64(num) - den_exp;
        // Pick k strictly above v2(2c) so |2c|_2 > 2^{-k} = r.
        int32_t k = v2_2c + 1 + static_cast<int32_t>(rng_c.next_bounded(4ULL));
        int64_t odd_u = static_cast<int64_t>(2ULL * rng_c.next_bounded(4ULL) + 1ULL);
        int32_t exp_2c = 1 - den_exp;
        int32_t min_e = std::min(exp_2c, k);
        int64_t t_2c = num << (exp_2c - min_e);
        int64_t t_u = odd_u << (k - min_e);
        int32_t v2_sum = min_e + v2_i64(t_2c + t_u);
        int32_t v2_prod = k + v2_sum;
        ++rep.control_samples;
        if (v2_prod == v2_2c + k) ++rep.control_slope1_hits;
    }

    rep.passed = (rep.treatment_slope2_hits == rep.treatment_samples) &&
                 (rep.control_slope1_hits == rep.control_samples);
    return rep;
}

// --- Boundary Seam (D <-> R <-> P) ---

SeamDecision guarded_flux_kernel_handoff(
    Rung1CalibrationReport cal,
    const double* cov_2x2_row_major,
    double flux_phi,
    SeamPolicy policy
) {
    SeamDecision dec{};
    dec.allowed = false;
    dec.deterministic_output = 0.0;

    if (!std::isfinite(flux_phi) || !std::isfinite(cal.total_variation) ||
        !std::isfinite(cal.excess_kurtosis)) {
        dec.code = SEAM_REJECT_NON_FINITE;
        return dec;
    }
    if (cal.code != INV_OK) {
        dec.code = SEAM_REJECT_INVARIANT;
        return dec;
    }
    if (cal.total_variation > policy.max_tv) {
        dec.code = SEAM_REJECT_UNCALIBRATED_TV;
        return dec;
    }
    if (std::abs(cal.excess_kurtosis) > policy.max_abs_excess_kurtosis) {
        dec.code = SEAM_REJECT_UNCALIBRATED_KURTOSIS;
        return dec;
    }
    MatrixInvariantReport cov_rep = check_symmetric_pd(cov_2x2_row_major, 2, 1e-12, policy.min_cov_eigenvalue);
    dec.cov_lambda_min = cov_rep.lambda_min;
    if (cov_rep.code != INV_OK) {
        dec.code = (cov_rep.code == INV_NON_FINITE) ? SEAM_REJECT_NON_FINITE : SEAM_REJECT_INDEFINITE_COV;
        return dec;
    }
    if (flux_phi < policy.flux_min || flux_phi > policy.flux_max) {
        dec.code = SEAM_REJECT_OOD_FLUX;
        return dec;
    }

    dec.code = SEAM_OK;
    dec.allowed = true;
    dec.deterministic_output = twisted_max_eigenvalue(flux_phi);
    return dec;
}

// --- Tonnetz / Prime Cadences Engine ---

TriadMoveResult apply_plr_move(int32_t vertex, int32_t move_id) {
    int32_t r = vertex % 12;
    bool is_major = (vertex < 12);
    if (is_major) {
        if (move_id == 0) { // P: {r, r+4, r+7} -> {r, r+3, r+7}
            return {12 + r, -1, (r + 3) % 12, (r + 4) % 12};
        } else if (move_id == 1) { // L: {r, r+4, r+7} -> {r+4, r+7, r+11}
            return {12 + (r + 4) % 12, -1, (r + 11) % 12, r};
        } else { // R: {r, r+4, r+7} -> {r+9, r, r+4}
            return {12 + (r + 9) % 12, +2, (r + 9) % 12, (r + 7) % 12};
        }
    } else {
        if (move_id == 0) { // P: {r, r+3, r+7} -> {r, r+4, r+7}
            return {r, +1, (r + 4) % 12, (r + 3) % 12};
        } else if (move_id == 1) { // L: {r, r+3, r+7} -> {r+8, r, r+3}
            return {(r + 8) % 12, +1, (r + 8) % 12, (r + 7) % 12};
        } else { // R: {r, r+3, r+7} -> {r+3, r+7, r+10}
            return {(r + 3) % 12, -2, (r + 10) % 12, r};
        }
    }
}

void build_adjacency_matrix(double* out_24x24) {
    std::fill(out_24x24, out_24x24 + 576, 0.0);
    for (int32_t v = 0; v < 24; ++v) {
        for (int32_t m = 0; m < 3; ++m) {
            int32_t u = apply_plr_move(v, m).target_vertex;
            out_24x24[v * 24 + u] = 1.0;
        }
    }
}

void build_laplacian_matrix(double* out_24x24) {
    build_adjacency_matrix(out_24x24);
    for (std::size_t i = 0; i < 576; ++i) out_24x24[i] = -out_24x24[i];
    for (std::size_t i = 0; i < 24; ++i) out_24x24[i * 24 + i] += 3.0;
}

void build_tonnetz_gram(double* out_2x2) {
    // Basis P_u = (4, -4), P_v = (0, 3) on 60-degree unit lattice: <x, y> = x1*y1 + x2*y2 + 0.5*(x1*y2 + x2*y1).
    auto dot60 = [](double a1, double b1, double a2, double b2) {
        return a1 * a2 + b1 * b2 + 0.5 * (a1 * b2 + b1 * a2);
    };
    out_2x2[0] = dot60(4.0, -4.0, 4.0, -4.0); // 16
    out_2x2[1] = dot60(4.0, -4.0, 0.0,  3.0); // -6
    out_2x2[2] = dot60(0.0,  3.0, 4.0, -4.0); // -6
    out_2x2[3] = dot60(0.0,  3.0, 0.0,  3.0); // 9
}

void build_tonnetz_covariance_per_step(double* out_2x2) {
    double g[4];
    build_tonnetz_gram(g);
    double det = g[0] * g[3] - g[1] * g[2]; // 108
    out_2x2[0] =  0.5 * g[3] / det; // 1/24
    out_2x2[1] = -0.5 * g[1] / det; // 1/36
    out_2x2[2] = -0.5 * g[2] / det; // 1/36
    out_2x2[3] =  0.5 * g[0] / det; // 2/27
}

void build_twisted_adjacency_complex(double phi, double* out_interleaved_24x24) {
    std::fill(out_interleaved_24x24, out_interleaved_24x24 + 2 * 576, 0.0);
    double theta = phi / 12.0;
    for (int32_t v = 0; v < 24; ++v) {
        for (int32_t m = 0; m < 3; ++m) {
            TriadMoveResult mv = apply_plr_move(v, m);
            double ang = theta * static_cast<double>(mv.voice_step);
            std::size_t idx = 2 * static_cast<std::size_t>(v * 24 + mv.target_vertex);
            out_interleaved_24x24[idx] = std::cos(ang);
            out_interleaved_24x24[idx + 1] = std::sin(ang);
        }
    }
}

double twisted_max_eigenvalue(double phi) {
    double best = 0.0;
    for (int k = 0; k < 12; ++k) {
        double a1 = 2.0 * kPi * (4.0 * k) / 12.0;
        double a2 = 2.0 * kPi * (9.0 * k) / 12.0 + phi / 4.0;
        double re = 1.0 + std::cos(a1) + std::cos(a2);
        double im = std::sin(a1) + std::sin(a2);
        double mag = std::hypot(re, im);
        if (mag > best) best = mag;
    }
    return best;
}

FluxWindowReport evaluate_flux_window() {
    FluxWindowReport rep{};
    rep.edge_low = 4.0 * std::acos(0.75);
    rep.edge_high = 2.0 * kPi - rep.edge_low;
    rep.max_eig_at_edge_low = twisted_max_eigenvalue(rep.edge_low);
    rep.max_eig_at_pi = twisted_max_eigenvalue(kPi);

    double min_dirac = 1e9;
    double phi_dirac = 2.0 * kPi / 3.0;
    for (int k = 0; k < 12; ++k) {
        double a1 = 2.0 * kPi * (4.0 * k) / 12.0;
        double a2 = 2.0 * kPi * (9.0 * k) / 12.0 + phi_dirac / 4.0;
        double mag = std::hypot(1.0 + std::cos(a1) + std::cos(a2), std::sin(a1) + std::sin(a2));
        if (mag < min_dirac) min_dirac = mag;
    }
    rep.min_eig_at_2pi_3 = min_dirac;

    rep.cyclic_ramanujan[0] = false;
    for (int n = 1; n <= 12; ++n) {
        bool ok = true;
        for (int j = 1; j < n; ++j) {
            double phi = 2.0 * kPi * static_cast<double>(j) / static_cast<double>(n);
            if (twisted_max_eigenvalue(phi) > kRamanujan3 + 1e-12) {
                ok = false;
                break;
            }
        }
        rep.cyclic_ramanujan[n] = ok;
    }
    return rep;
}

double ihara_bass_residual(double u) {
    // Directed edges indexed 0..71: e = 3*v + m.
    std::vector<double> ib(72 * 72, 0.0);
    for (int e = 0; e < 72; ++e) {
        ib[e * 72 + e] = 1.0;
        int v = e / 3;
        int m = e % 3;
        int to = apply_plr_move(v, m).target_vertex;
        for (int m2 = 0; m2 < 3; ++m2) {
            if (m2 == m) continue; // non-backtracking (each P,L,R is an involution)
            int e2 = 3 * to + m2;
            ib[e * 72 + e2] -= u;
        }
    }
    double lhs = det_lu(ib, 72);

    double adj[576];
    build_adjacency_matrix(adj);
    std::vector<double> bass(24 * 24, 0.0);
    for (std::size_t i = 0; i < 24; ++i) {
        for (std::size_t j = 0; j < 24; ++j) {
            bass[i * 24 + j] = -u * adj[i * 24 + j];
        }
        bass[i * 24 + i] += 1.0 + 2.0 * u * u;
    }
    double rhs = std::pow(1.0 - u * u, 12) * det_lu(bass, 24);
    return std::abs(lhs - rhs);
}

WindingDistribution compute_exact_winding_distribution(int32_t m) {
    WindingDistribution out{};
    out.length_m = m;
    out.w_min = -8;
    out.w_max = 8;
    if (m < 2 || m > 40 || (m % 2) != 0) return out;

    // Precompute directed edge transitions (each of 72 directed edges has 2 non-backtracking successors).
    int32_t succ[72][2];
    int32_t step_s[72];
    for (int32_t v = 0; v < 24; ++v) {
        for (int32_t mv = 0; mv < 3; ++mv) {
            int32_t e = 3 * v + mv;
            TriadMoveResult r = apply_plr_move(v, mv);
            step_s[e] = r.voice_step;
            int32_t idx = 0;
            for (int32_t mv2 = 0; mv2 < 3; ++mv2) {
                if (mv2 == mv) continue;
                succ[e][idx++] = 3 * r.target_vertex + mv2;
            }
        }
    }

    // Exact closed walk counts N_d(w) for all even d <= m.
    const int32_t max_s = 2 * m;
    const int32_t stride = 2 * max_s + 1;
    const int32_t offset = max_s;
    std::vector<std::array<int64_t, 17>> N_dw(static_cast<std::size_t>(m + 1));
    for (auto& arr : N_dw) arr.fill(0);
    std::vector<int64_t> N_total(static_cast<std::size_t>(m + 1), 0);
    int64_t bad_mod12 = 0;

    std::vector<int64_t> cur(72 * static_cast<std::size_t>(stride), 0);
    std::vector<int64_t> nxt(72 * static_cast<std::size_t>(stride), 0);

    for (int32_t e0 = 0; e0 < 72; ++e0) {
        std::fill(cur.begin(), cur.end(), 0);
        // Step 1: traverse edge e0 itself.
        cur[static_cast<std::size_t>(e0 * stride + (offset + step_s[e0]))] = 1;

        for (int32_t d = 2; d <= m; ++d) {
            std::fill(nxt.begin(), nxt.end(), 0);
            int32_t s_lim = 2 * (d - 1);
            for (int32_t e = 0; e < 72; ++e) {
                const std::size_t base = static_cast<std::size_t>(e * stride);
                int32_t e1 = succ[e][0];
                int32_t e2 = succ[e][1];
                int32_t ds1 = step_s[e1];
                int32_t ds2 = step_s[e2];
                const std::size_t base1 = static_cast<std::size_t>(e1 * stride);
                const std::size_t base2 = static_cast<std::size_t>(e2 * stride);
                for (int32_t s = -s_lim; s <= s_lim; ++s) {
                    int64_t cnt = cur[base + static_cast<std::size_t>(offset + s)];
                    if (cnt == 0) continue;
                    nxt[base1 + static_cast<std::size_t>(offset + s + ds1)] += cnt;
                    nxt[base2 + static_cast<std::size_t>(offset + s + ds2)] += cnt;
                }
            }
            cur.swap(nxt);

            if (d % 2 == 0) {
                // Closed non-backtracking walk of length d returns to edge e0 at step d
                // (meaning step d+1 would be e0 without backtracking, i.e. cur[e_prev] where e0 in succ[e_prev]).
                // Equivalently, step 1 started on e0; returning to e0 at step d+1 means at step d we are at
                // any predecessor e_p of e0; trace(B^d) counts length-d cycles on the directed line graph:
                // start at edge e0 at step 0, end at edge e0 after d transitions.
                // Re-index: we did 1 step for e0 then (d-1) transitions -> total d edges; valid closed cycle
                // iff e0 is a legal non-backtracking successor of the d-th edge!
                int32_t s_lim_d = 2 * d;
                for (int32_t e = 0; e < 72; ++e) {
                    if (succ[e][0] != e0 && succ[e][1] != e0) continue;
                    const std::size_t base = static_cast<std::size_t>(e * stride);
                    for (int32_t s = -s_lim_d; s <= s_lim_d; ++s) {
                        int64_t cnt = cur[base + static_cast<std::size_t>(offset + s)];
                        if (cnt == 0) continue;
                        if (s % 12 != 0) {
                            bad_mod12 += cnt;
                        } else {
                            int32_t w = s / 12;
                            N_dw[static_cast<std::size_t>(d)][static_cast<std::size_t>(w - out.w_min)] += cnt;
                            N_total[static_cast<std::size_t>(d)] += cnt;
                        }
                    }
                }
            }
        }
    }

    out.total_closed_walks = N_total[static_cast<std::size_t>(m)];
    out.non_multiple_12_closed = bad_mod12;
    for (int32_t i = 0; i < 17; ++i) {
        out.closed_counts[i] = N_dw[static_cast<std::size_t>(m)][static_cast<std::size_t>(i)];
    }

    // Exact Mobius inversion per winding w.
    int64_t total_pi = 0;
    for (int32_t w = out.w_min; w <= out.w_max; ++w) {
        int64_t acc = 0;
        for (int32_t d = 2; d <= m; d += 2) {
            if (m % d != 0) continue;
            int32_t k = m / d;
            if (w % k != 0) continue;
            int32_t mu = mobius_mu(k);
            if (mu == 0) continue;
            int32_t w0 = w / k;
            acc += static_cast<int64_t>(mu) * N_dw[static_cast<std::size_t>(d)][static_cast<std::size_t>(w0 - out.w_min)];
        }
        int64_t pi_mw = acc / static_cast<int64_t>(m);
        out.prime_counts[static_cast<std::size_t>(w - out.w_min)] = pi_mw;
        total_pi += pi_mw;
    }
    out.total_primes = total_pi;
    return out;
}

TuneCheckReport verify_tune_theorem(int32_t max_len) {
    TuneCheckReport rep{};
    rep.lemma_l1 = true;
    rep.lemma_l2 = true;
    rep.lemma_l3 = true;

    // Check Lemmas L1, L2, L3 exhaustively on all 24 triads and 72 directed edges.
    for (int32_t v = 0; v < 24; ++v) {
        auto ns = triad_notes(v);
        for (int i = 0; i < 3; ++i) {
            for (int j = i + 1; j < 3; ++j) {
                int d = std::abs(ns[i] - ns[j]);
                d = std::min(d, 12 - d);
                if (d == 1 || d == 2) rep.lemma_l3 = false;
            }
        }
        int32_t dep[3];
        for (int32_t mv = 0; mv < 3; ++mv) {
            TriadMoveResult r = apply_plr_move(v, mv);
            dep[mv] = r.departing_pitch;
            int step = std::abs(r.voice_step);
            if (step != 1 && step != 2) rep.lemma_l3 = false;
            // Check L2: from target_vertex, only move mv changes r.arriving_pitch.
            for (int32_t mv2 = 0; mv2 < 3; ++mv2) {
                TriadMoveResult r2 = apply_plr_move(r.target_vertex, mv2);
                if (mv2 == mv) {
                    if (r2.departing_pitch != r.arriving_pitch) rep.lemma_l2 = false;
                } else {
                    if (r2.departing_pitch == r.arriving_pitch) rep.lemma_l2 = false;
                }
            }
        }
        if (dep[0] == dep[1] || dep[1] == dep[2] || dep[0] == dep[2]) rep.lemma_l1 = false;
    }

    // Confirm negative control NEG-M4: backtracking counterexample C->Cm->C vs E->Abm->E.
    TriadMoveResult c_to_cm = apply_plr_move(0, 0);   // C -> Cm, arrives Eb (3)
    TriadMoveResult cm_to_c = apply_plr_move(12, 0);  // Cm -> C, arrives E (4)
    TriadMoveResult e_to_abm = apply_plr_move(4, 1);  // E -> Abm (G#m), arrives Eb (3)
    TriadMoveResult abm_to_e = apply_plr_move(8 + 12, 1); // Abm -> E, arrives E (4)
    rep.backtrack_counterexample_confirmed =
        (c_to_cm.arriving_pitch == 3 && cm_to_c.arriving_pitch == 4 &&
         e_to_abm.arriving_pitch == 3 && abm_to_e.arriving_pitch == 4);

    // Local Theorem 4.2 decoder from cyclic tune (n_0, ..., n_{m-1}) alone.
    auto decode_tune = [](const std::vector<int32_t>& tune, std::vector<int32_t>& out_chords) -> bool {
        const int32_t m = static_cast<int32_t>(tune.size());
        out_chords.assign(static_cast<std::size_t>(m), -1);

        // Identify voice changes: if {n_{i-2}, n_{i-1}, n_i} is a consonant triad, voices at i and i-2 differ.
        bool any_three_voices = false;
        for (int32_t i = 0; i < m; ++i) {
            int32_t a = tune[static_cast<std::size_t>((i - 2 + m) % m)];
            int32_t b = tune[static_cast<std::size_t>((i - 1 + m) % m)];
            int32_t c = tune[static_cast<std::size_t>(i)];
            int32_t t = triad_from_notes(a, b, c);
            if (t >= 0) {
                out_chords[static_cast<std::size_t>(i)] = t;
                any_three_voices = true;
            }
        }
        if (!any_three_voices) {
            // Held-note hexagon: find unique pitch class h completing every consecutive pair to a triad.
            int32_t held = -1;
            int32_t matches = 0;
            for (int32_t h = 0; h < 12; ++h) {
                bool ok = true;
                for (int32_t i = 0; i < m; ++i) {
                    int32_t prev = tune[static_cast<std::size_t>((i - 1 + m) % m)];
                    int32_t cur = tune[static_cast<std::size_t>(i)];
                    if (triad_from_notes(prev, cur, h) < 0) {
                        ok = false;
                        break;
                    }
                }
                if (ok) {
                    held = h;
                    ++matches;
                }
            }
            if (matches != 1) return false;
            for (int32_t i = 0; i < m; ++i) {
                int32_t prev = tune[static_cast<std::size_t>((i - 1 + m) % m)];
                int32_t cur = tune[static_cast<std::size_t>(i)];
                out_chords[static_cast<std::size_t>(i)] = triad_from_notes(prev, cur, held);
            }
            return true;
        }
        // Propagate forward from known 3-voice chords using exact step distance in {1, 2}.
        int32_t start = 0;
        while (out_chords[static_cast<std::size_t>(start)] < 0) ++start;
        for (int32_t step = 1; step < m; ++step) {
            int32_t idx = (start + step) % m;
            if (out_chords[static_cast<std::size_t>(idx)] >= 0) continue;
            int32_t prev_v = out_chords[static_cast<std::size_t>((idx - 1 + m) % m)];
            int32_t arr = tune[static_cast<std::size_t>(idx)];
            int32_t next_v = -1;
            for (int32_t mv = 0; mv < 3; ++mv) {
                TriadMoveResult r = apply_plr_move(prev_v, mv);
                if (r.arriving_pitch == arr) {
                    next_v = r.target_vertex;
                    break;
                }
            }
            if (next_v < 0) return false;
            out_chords[static_cast<std::size_t>(idx)] = next_v;
        }
        return true;
    };

    auto is_primitive = [](const std::vector<int32_t>& seq) -> bool {
        int32_t m = static_cast<int32_t>(seq.size());
        for (int32_t d = 1; d < m; ++d) {
            if (m % d != 0) continue;
            bool per = true;
            for (int32_t i = 0; i < m; ++i) {
                if (seq[static_cast<std::size_t>(i)] != seq[static_cast<std::size_t>(i % d)]) {
                    per = false;
                    break;
                }
            }
            if (per) return false;
        }
        return true;
    };

    // DFS over rooted non-backtracking walks starting at C major (vertex 0) — by vertex-transitivity,
    // checking all 24 starts is 24x; we test all 24 starts for max_len <= 12 (or start=0..23).
    std::vector<int32_t> chords;
    std::vector<int32_t> tune;
    std::vector<int32_t> decoded;

    for (int32_t target_m = 6; target_m <= max_len; target_m += 2) {
        chords.resize(static_cast<std::size_t>(target_m));
        tune.resize(static_cast<std::size_t>(target_m));

        for (int32_t start_v = 0; start_v < 24; ++start_v) {
            auto dfs = [&](auto&& self, int32_t depth, int32_t cur_v, int32_t last_mv, int32_t first_mv) -> void {
                if (depth == target_m) {
                    if (cur_v != start_v || last_mv == first_mv) return;
                    if (!is_primitive(chords)) return;
                    ++rep.rooted_primes_checked;
                    if (!is_primitive(tune)) ++rep.periodic_tune_failures;
                    if (!decode_tune(tune, decoded) || decoded != chords) {
                        ++rep.decode_failures;
                    }
                    return;
                }
                for (int32_t mv = 0; mv < 3; ++mv) {
                    if (depth > 0 && mv == last_mv) continue;
                    TriadMoveResult r = apply_plr_move(cur_v, mv);
                    chords[static_cast<std::size_t>(depth)] = r.target_vertex;
                    tune[static_cast<std::size_t>(depth)] = r.arriving_pitch;
                    self(self, depth + 1, r.target_vertex, mv, depth == 0 ? mv : first_mv);
                }
            };
            dfs(dfs, 0, start_v, -1, -1);
        }
    }
    return rep;
}

EDOComparisonReport evaluate_edo_ramanujan_comparison() {
    auto max_nontrivial_edo = [](int N, int a, int b) -> double {
        double best = 0.0;
        for (int k = 1; k < N; ++k) {
            double t1 = 2.0 * kPi * static_cast<double>(a * k) / static_cast<double>(N);
            double t2 = 2.0 * kPi * static_cast<double>(b * k) / static_cast<double>(N);
            double mag = std::hypot(1.0 + std::cos(t1) + std::cos(t2), std::sin(t1) + std::sin(t2));
            if (mag > best) best = mag;
        }
        return best;
    };
    EDOComparisonReport rep{};
    rep.lambda_max_12 = max_nontrivial_edo(12, 4, 7);
    rep.lambda_max_31 = max_nontrivial_edo(31, 10, 18);
    rep.lambda_max_53 = max_nontrivial_edo(53, 17, 31);
    rep.ramanujan_12 = (rep.lambda_max_12 <= kRamanujan3);
    rep.ramanujan_31 = (rep.lambda_max_31 <= kRamanujan3);
    rep.ramanujan_53 = (rep.lambda_max_53 <= kRamanujan3);
    return rep;
}

SigningCensusReport run_signing_census_exact() {
    SigningCensusReport rep{};
    rep.total_classes = 8192;
    rep.nontrivial_classes = 8191;

    // Build all 36 undirected edges (always major u in 0..11 to minor v in 12..23).
    struct Edge { int32_t maj; int32_t min; int32_t step; int32_t move_id; };
    std::vector<Edge> edges;
    edges.reserve(36);
    for (int32_t u = 0; u < 12; ++u) {
        for (int32_t mv = 0; mv < 3; ++mv) {
            TriadMoveResult r = apply_plr_move(u, mv);
            edges.push_back({u, r.target_vertex, r.voice_step, mv});
        }
    }

    // BFS spanning tree from vertex 0 -> 23 tree edges + 13 fundamental chord edges.
    std::vector<bool> visited(24, false);
    std::vector<int32_t> parent(24, -1);
    std::vector<int32_t> parent_step(24, 0); // voice step from parent -> node
    std::vector<int32_t> depth(24, 0);
    std::vector<bool> in_tree(36, false);
    std::vector<int32_t> queue;
    visited[0] = true;
    queue.push_back(0);
    for (std::size_t qi = 0; qi < queue.size(); ++qi) {
        int32_t x = queue[qi];
        for (int32_t ei = 0; ei < 36; ++ei) {
            int32_t y = -1;
            int32_t st = 0;
            if (edges[ei].maj == x) { y = edges[ei].min; st = edges[ei].step; }
            else if (edges[ei].min == x) { y = edges[ei].maj; st = -edges[ei].step; }
            if (y >= 0 && !visited[static_cast<std::size_t>(y)]) {
                visited[static_cast<std::size_t>(y)] = true;
                parent[static_cast<std::size_t>(y)] = x;
                parent_step[static_cast<std::size_t>(y)] = st;
                depth[static_cast<std::size_t>(y)] = depth[static_cast<std::size_t>(x)] + 1;
                in_tree[static_cast<std::size_t>(ei)] = true;
                queue.push_back(y);
            }
        }
    }

    // Compute exact fundamental-cycle winding for each of the 13 non-tree chords -> voice-parity mask.
    std::vector<int32_t> chord_edges;
    uint32_t voice_parity_mask = 0;
    for (int32_t ei = 0; ei < 36; ++ei) {
        if (in_tree[static_cast<std::size_t>(ei)]) continue;
        int32_t bit = static_cast<int32_t>(chord_edges.size());
        chord_edges.push_back(ei);
        // Fundamental cycle: tree path root->maj + chord (maj->min) + reverse tree path min->root.
        auto tree_sum_from_root = [&](int32_t node) -> int32_t {
            int32_t acc = 0;
            while (node != 0) {
                acc += parent_step[static_cast<std::size_t>(node)];
                node = parent[static_cast<std::size_t>(node)];
            }
            return acc;
        };
        int32_t cyc_sum = tree_sum_from_root(edges[ei].maj) + edges[ei].step - tree_sum_from_root(edges[ei].min);
        int32_t w = cyc_sum / 12;
        if ((w & 1) != 0) voice_parity_mask |= (1U << bit);
    }

    // Enumerate all 8192 signings using 12x12 bipartite Gram C^T C -> exact max eigenvalue.
    std::vector<double> max_eigs(8192, 0.0);
    std::vector<double> ctc(144, 0.0);
    std::vector<double> eigs;
    double best_nontriv = 1e9;
    int64_t ramanujan_cnt = 0;

    for (uint32_t mask = 0; mask < 8192U; ++mask) {
        double C[144] = {0.0};
        for (int32_t ei = 0; ei < 36; ++ei) {
            C[edges[ei].maj * 12 + (edges[ei].min - 12)] = 1.0;
        }
        for (int32_t b = 0; b < 13; ++b) {
            if ((mask & (1U << b)) != 0U) {
                int32_t ei = chord_edges[static_cast<std::size_t>(b)];
                C[edges[ei].maj * 12 + (edges[ei].min - 12)] = -1.0;
            }
        }
        for (int i = 0; i < 12; ++i) {
            for (int j = i; j < 12; ++j) {
                double s = 0.0;
                for (int k = 0; k < 12; ++k) s += C[k * 12 + i] * C[k * 12 + j];
                ctc[static_cast<std::size_t>(i * 12 + j)] = s;
                ctc[static_cast<std::size_t>(j * 12 + i)] = s;
            }
        }
        jacobi_eigenvalues(ctc, 12, eigs);
        double mx = std::sqrt(std::max(0.0, eigs.back()));
        max_eigs[mask] = mx;
        if (mask != 0U) {
            if (mx <= kRamanujan3 + 1e-11) ++ramanujan_cnt;
            if (mx < best_nontriv) best_nontriv = mx;
        }
    }

    double vp_eig = max_eigs[voice_parity_mask];
    int64_t strictly_smaller = 0;
    for (uint32_t mask = 0; mask < 8192U; ++mask) {
        if (max_eigs[mask] < vp_eig - 1e-9) ++strictly_smaller;
    }
    rep.ramanujan_nontrivial = ramanujan_cnt;
    rep.best_max_eig = best_nontriv;
    rep.voice_parity_max_eig = vp_eig;
    rep.voice_parity_rank = strictly_smaller;
    rep.passed = (rep.ramanujan_nontrivial == 7675) &&
                 (rep.voice_parity_rank == 7372) &&
                 (std::abs(rep.best_max_eig - (1.0 + std::sqrt(2.0))) < 1e-9) &&
                 (std::abs(rep.voice_parity_max_eig - std::sqrt(5.0 + 2.0 * std::sqrt(2.0))) < 1e-9);
    return rep;
}

WindingNullRCTReport run_winding_null_rct(int32_t m, PRNGKey key, int64_t n_walks) {
    WindingNullRCTReport rep{};
    rep.length_m = m;
    rep.total_walks_sampled = n_walks;
    if (m < 6 || m > 40 || (m % 2) != 0 || n_walks <= 0) return rep;

    int32_t succ[72][2];
    int32_t step_s[72];
    for (int32_t v = 0; v < 24; ++v) {
        for (int32_t mv = 0; mv < 3; ++mv) {
            int32_t e = 3 * v + mv;
            TriadMoveResult r = apply_plr_move(v, mv);
            step_s[e] = r.voice_step;
            int32_t idx = 0;
            for (int32_t mv2 = 0; mv2 < 3; ++mv2) {
                if (mv2 == mv) continue;
                succ[e][idx++] = 3 * r.target_vertex + mv2;
            }
        }
    }

    KeyedPRNG rng = KeyedPRNG::from_key(key);
    int64_t hist[17] = {0};
    int64_t closed_obs = 0;
    int64_t bad_mod12 = 0;

    for (int64_t t = 0; t < n_walks; ++t) {
        int32_t e0 = static_cast<int32_t>(rng.next_bounded(72ULL));
        int32_t e = e0;
        int32_t s = step_s[e0];
        for (int32_t step = 1; step < m; ++step) {
            int32_t branch = static_cast<int32_t>(rng.next_bounded(2ULL));
            e = succ[e][branch];
            s += step_s[e];
        }
        if (succ[e][0] == e0 || succ[e][1] == e0) {
            ++closed_obs;
            if (s % 12 != 0) {
                ++bad_mod12;
            } else {
                int32_t w = s / 12;
                if (w >= -8 && w <= 8) ++hist[w + 8];
            }
        }
    }

    rep.closed_walks_observed = closed_obs;
    rep.non_multiple_12_observed = bad_mod12;
    if (closed_obs == 0) return rep;

    WindingDistribution exact = compute_exact_winding_distribution(m);
    double tv_mc_closed = 0.0;
    double tv_closed_prime = 0.0;
    double mean = 0.0;
    double m2 = 0.0;
    for (int32_t i = 0; i < 17; ++i) {
        double p_mc = static_cast<double>(hist[i]) / static_cast<double>(closed_obs);
        double p_closed = static_cast<double>(exact.closed_counts[i]) / static_cast<double>(exact.total_closed_walks);
        double p_prime = static_cast<double>(exact.prime_counts[i]) / static_cast<double>(exact.total_primes);
        tv_mc_closed += std::abs(p_mc - p_closed);
        tv_closed_prime += std::abs(p_closed - p_prime);
        double w = static_cast<double>(i - 8);
        mean += p_mc * w;
        m2 += p_mc * w * w;
    }
    rep.mc_vs_exact_closed_tv = 0.5 * tv_mc_closed;
    rep.exact_closed_vs_prime_tv = 0.5 * tv_closed_prime;
    rep.mc_mean = mean;
    rep.mc_variance = m2 - mean * mean;
    rep.passed = (bad_mod12 == 0) && (closed_obs > 0) && (rep.mc_vs_exact_closed_tv < 0.03);
    return rep;
}

} // namespace ergentics
