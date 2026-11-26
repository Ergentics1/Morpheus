#include "section7_cycle5.hpp"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <set>
#include <tuple>
#include <vector>

namespace ergentics {

namespace {

constexpr double kPi = 3.141592653589793238462643383279502884;
constexpr double kEulerGamma = 0.577215664901532860606512090082402431;

/// Compute exact 64-point Gauss-Legendre nodes and weights on [-1, 1] from scratch
/// via Newton-Raphson on P_64(x) (zero external lookup tables).
struct GL64 {
    std::array<double, 64> t{};
    std::array<double, 64> w{};
    bool self_check_ok{false};

    GL64() {
        constexpr int N = 64;
        for (int i = 0; i < N / 2; ++i) {
            double x = std::cos(kPi * (static_cast<double>(i) + 0.75) / (static_cast<double>(N) + 0.5));
            double dp = 0.0;
            for (int iter = 0; iter < 12; ++iter) {
                double p0 = 1.0;
                double p1 = x;
                for (int k = 2; k <= N; ++k) {
                    double dk = static_cast<double>(k);
                    double p2 = ((2.0 * dk - 1.0) * x * p1 - (dk - 1.0) * p0) / dk;
                    p0 = p1;
                    p1 = p2;
                }
                dp = static_cast<double>(N) * (x * p1 - p0) / (x * x - 1.0);
                double dx = p1 / dp;
                x -= dx;
                if (std::fabs(dx) < 1e-16) break;
            }
            double wi = 2.0 / ((1.0 - x * x) * dp * dp);
            t[static_cast<std::size_t>(i)] = -x;
            t[static_cast<std::size_t>(N - 1 - i)] = x;
            w[static_cast<std::size_t>(i)] = wi;
            w[static_cast<std::size_t>(N - 1 - i)] = wi;
        }
        double sum_w = 0.0;
        double sum_x2 = 0.0;
        for (int i = 0; i < N; ++i) {
            sum_w += w[static_cast<std::size_t>(i)];
            sum_x2 += w[static_cast<std::size_t>(i)] * t[static_cast<std::size_t>(i)] * t[static_cast<std::size_t>(i)];
        }
        self_check_ok = (std::fabs(sum_w - 2.0) < 1e-14 && std::fabs(sum_x2 - 2.0 / 3.0) < 1e-14);
    }
};

/// Odlyzko-Poitou positive-definite kernel H_1(u) = (h * h)(u) / 3 on [0, 2],
/// where h(t) = 1 + cos(pi * t) on [-1, 1].
inline double poitou_h1(double u) {
    if (u <= 0.0) return 1.0;
    if (u >= 2.0) return 0.0;
    return ((2.0 - u) * (1.0 + 0.5 * std::cos(kPi * u)) / 3.0) + std::sin(kPi * u) / (2.0 * kPi);
}

struct PoitouParams {
    double b;
    double logA;
    double logB;
    double E;
    double f2;
    double f4;
};

double prime_boost(int64_t q, double b) {
    const double lq = std::log(static_cast<double>(q));
    double s = 0.0;
    double qm = static_cast<double>(q);
    for (int m = 1; static_cast<double>(m) * lq < 2.0 * b; ++m) {
        const double u = static_cast<double>(m) * lq / b;
        s += (4.0 * lq / (1.0 + qm)) * poitou_h1(u);
        qm *= static_cast<double>(q);
    }
    return s;
}

PoitouParams eval_poitou(const GL64& gl, double b) {
    double i_sinh = 0.0;
    double i_cosh = 0.0;
    for (int i = 0; i < 64; ++i) {
        const double u = 1.0 + gl.t[static_cast<std::size_t>(i)]; // [0, 2]
        const double x = b * u;
        const double g = poitou_h1(u);
        const double wi = gl.w[static_cast<std::size_t>(i)];
        i_sinh += wi * b * (1.0 - g) / std::sinh(x);
        const double ch = std::cosh(0.5 * x);
        i_cosh += wi * b * g / (2.0 * ch * ch);
    }
    const double i_tail = (b < 18.0) ? std::log((std::exp(2.0 * b) + 1.0) / (std::exp(2.0 * b) - 1.0))
                                     : 2.0 * std::exp(-2.0 * b);
    const double logB = kEulerGamma + std::log(4.0 * kPi) - i_sinh - i_tail;
    const double logA = logB + i_cosh;
    return PoitouParams{b, logA, logB, (8.0 * b) / 3.0, prime_boost(2, b), prime_boost(4, b)};
}

double best_lb_grid(const std::vector<PoitouParams>& grid, double deg, double rho1, double coeff_f2, double coeff_f4) {
    double best = -1e9;
    for (const auto& p : grid) {
        const double val = rho1 * p.logA + (1.0 - rho1) * p.logB - p.E / deg + coeff_f2 * p.f2 + coeff_f4 * p.f4;
        if (val > best) best = val;
    }
    return best;
}

bool is_prime_i64(int64_t n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    for (int64_t d = 3; d * d <= n; d += 2) {
        if (n % d == 0) return false;
    }
    return true;
}

int64_t gcd_local(int64_t a, int64_t b) {
    a = a < 0 ? -a : a;
    b = b < 0 ? -b : b;
    while (b != 0) {
        int64_t r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int64_t sigma1_i64(int64_t n) {
    int64_t s = 0;
    for (int64_t d = 1; d * d <= n; ++d) {
        if (n % d == 0) {
            s += d;
            if (d * d != n) s += n / d;
        }
    }
    return s;
}

int64_t isqrt_i64(int64_t n) {
    int64_t r = static_cast<int64_t>(std::sqrt(static_cast<double>(n)));
    while ((r + 1) * (r + 1) <= n) ++r;
    while (r * r > n) --r;
    return r;
}

int legendre_p(int64_t a, int64_t p) {
    int64_t x = ((a % p) + p) % p;
    if (x == 0) return 0;
    int64_t res = 1;
    int64_t e = (p - 1) / 2;
    int64_t base = x;
    while (e > 0) {
        if (e & 1) res = (res * base) % p;
        base = (base * base) % p;
        e >>= 1;
    }
    return (res == p - 1) ? -1 : static_cast<int>(res);
}

bool is_fundamental_discriminant(int64_t D) {
    if (D <= 1) return false;
    if (D % 4 == 1) {
        for (int64_t p = 2; p * p <= D; ++p) {
            if (D % (p * p) == 0) return false;
        }
        return true;
    }
    if (D % 4 == 0) {
        int64_t m = D / 4;
        if (m % 4 != 2 && m % 4 != 3) return false;
        for (int64_t p = 2; p * p <= m; ++p) {
            if (m % (p * p) == 0) return false;
        }
        return true;
    }
    return false;
}

/// Exact narrow class number h^+(D) for real quadratic fundamental discriminant D
/// via proper SL_2(Z) equivalence cycles of Gauss reduced indefinite binary quadratic forms.
int32_t narrow_class_number_quad(int64_t D) {
    const int64_t sD = isqrt_i64(D);
    using Form = std::tuple<int64_t, int64_t, int64_t>;
    std::set<Form> forms;
    for (int64_t b = 1; b <= sD; ++b) {
        if ((D - b * b) % 4 != 0) continue;
        const int64_t prod = (D - b * b) / 4;
        for (int64_t d = 1; d <= prod; ++d) {
            if (prod % d != 0) continue;
            if (sD - b < 2 * d && 2 * d < sD + b) {
                const int64_t c = prod / d;
                if (gcd_local(gcd_local(d, b), c) == 1) {
                    forms.insert({d, b, -c});
                    forms.insert({-d, b, c});
                }
            }
        }
    }
    auto step = [D, sD](const Form& f) -> Form {
        const auto [a, b, c] = f;
        (void)a;
        const int64_t ac = c < 0 ? -c : c;
        const int64_t b_new = 2 * ac * ((sD + b) / (2 * ac)) - b;
        const int64_t c_new = (b_new * b_new - D) / (4 * c);
        return {c, b_new, c_new};
    };
    std::set<Form> visited;
    int32_t cycles = 0;
    for (const auto& f : forms) {
        if (visited.count(f)) continue;
        ++cycles;
        Form cur = f;
        while (!visited.count(cur)) {
            visited.insert(cur);
            cur = step(cur);
        }
    }
    return cycles;
}

/// Count exact (D'', N) solutions for real quadratic field Q(sqrt(D)) with 2 split,
/// fixing one prime v|2, |D''| even, coprime D'', N, v, achieving product P_target.
int32_t count_quad_dn_solutions(int64_t D, int64_t P_target) {
    std::vector<int64_t> norms;
    norms.push_back(2); // conjugate prime v' | 2
    for (int64_t p = 3; p <= P_target + 1; ++p) {
        if (!is_prime_i64(p)) continue;
        const int leg = legendre_p(D, p);
        if (leg == 1) {
            norms.push_back(p);
            norms.push_back(p);
        } else if (leg == 0) {
            norms.push_back(p);
        } else if (p * p <= P_target + 1) {
            norms.push_back(p * p);
        }
    }
    int32_t count = 0;
    auto dfs = [&](auto&& self, std::size_t idx, int64_t rem, int d_cnt) -> void {
        if (rem == 1) {
            if (d_cnt % 2 == 0) ++count;
            return;
        }
        if (idx == norms.size()) return;
        const int64_t q = norms[idx];
        // Option 0: skip
        self(self, idx + 1, rem, d_cnt);
        // Option 1: include in D'' (factor q - 1)
        if (q == 2) {
            self(self, idx + 1, rem, d_cnt + 1);
        } else if (rem % (q - 1) == 0) {
            self(self, idx + 1, rem / (q - 1), d_cnt + 1);
        }
        // Option 2: include q^e in N (factor q^{e-1}(q + 1))
        int64_t f = q + 1;
        while (f <= rem) {
            if (rem % f == 0) {
                self(self, idx + 1, rem / f, d_cnt);
            }
            if (f > rem / q) break;
            f *= q;
        }
    };
    dfs(dfs, 0, P_target, 0);
    return count;
}

inline int kronecker_neg4(int64_t p) {
    if (p == 2) return 0;
    return (p % 4 == 1) ? 1 : -1;
}

inline int kronecker_neg3(int64_t p) {
    if (p == 3) return 0;
    return (p % 3 == 1) ? 1 : -1;
}

/// F_8 = F_2[alpha]/(alpha^3 + alpha + 1) arithmetic on 0..7.
inline uint8_t f8_mul(uint8_t a, uint8_t b) {
    uint8_t p = 0;
    for (int i = 0; i < 3; ++i) {
        if (b & (1u << i)) p ^= static_cast<uint8_t>(a << i);
    }
    if (p & 16u) p ^= static_cast<uint8_t>(0b1011u << 1);
    if (p & 8u) p ^= 0b1011u;
    return static_cast<uint8_t>(p & 7u);
}

inline uint8_t f8_inv(uint8_t a) {
    uint8_t a2 = f8_mul(a, a);
    uint8_t a4 = f8_mul(a2, a2);
    return f8_mul(a2, a4); // a^6 = a^{-1} in F_8^*
}

struct F8Mat {
    uint8_t a, b, c, d;
};

inline F8Mat f8_mat_mul(F8Mat x, F8Mat y) {
    return F8Mat{
        static_cast<uint8_t>(f8_mul(x.a, y.a) ^ f8_mul(x.b, y.c)),
        static_cast<uint8_t>(f8_mul(x.a, y.b) ^ f8_mul(x.b, y.d)),
        static_cast<uint8_t>(f8_mul(x.c, y.a) ^ f8_mul(x.d, y.c)),
        static_cast<uint8_t>(f8_mul(x.c, y.b) ^ f8_mul(x.d, y.d))
    };
}

inline bool f8_is_scalar(F8Mat m) {
    return m.b == 0 && m.c == 0 && m.a == m.d && m.a != 0;
}

inline int f8_p1_act(F8Mat m, int pt) {
    // pt = 8 represents infinity (1:0); pt in 0..7 represents (pt:1).
    uint8_t num, den;
    if (pt == 8) {
        num = m.a;
        den = m.c;
    } else {
        uint8_t x = static_cast<uint8_t>(pt);
        num = static_cast<uint8_t>(f8_mul(m.a, x) ^ m.b);
        den = static_cast<uint8_t>(f8_mul(m.c, x) ^ m.d);
    }
    if (den == 0) return 8;
    return static_cast<int>(f8_mul(num, f8_inv(den)));
}

} // namespace

TheoremDPincerReport verify_theorem_d_pincer() {
    const GL64 gl;
    TheoremDPincerReport rep{};
    rep.quadrature_self_check_ok = gl.self_check_ok;

    // Self-check exact Weil-Poitou explicit formula on Q (d_Q = 1, r1 = 1, r2 = 0) at b = 2.0.
    const PoitouParams p2 = eval_poitou(gl, 2.0);
    double q_psum = 0.0;
    for (int64_t p = 2; p <= 60; ++p) {
        if (is_prime_i64(p) && std::log(static_cast<double>(p)) < 4.0) {
            q_psum += prime_boost(p, 2.0);
        }
    }
    rep.q_explicit_formula_lb = p2.logA - p2.E + q_psum;

    // Universal monotone tail for ALL n >= 15 at b = 4.2 (independently verifies Thm 7.19(b)).
    const PoitouParams p42 = eval_poitou(gl, 4.2);
    rep.tail15_e_minus_f2 = p42.E - p42.f2;
    rep.tail15_lb_b42 = std::exp(p42.logA - rep.tail15_e_minus_f2 / 15.0);
    rep.tail15_ub = std::exp((2.0 / 3.0) * std::log(8.0 * kPi * kPi) + (2.0 / 45.0) * std::log(9.0 / 4.0));

    // Dense b-grid in [0.5, 12.0] with step 0.05 (includes b = 6.00 exactly).
    std::vector<PoitouParams> grid;
    grid.reserve(231);
    for (int i = 0; i <= 230; ++i) {
        grid.push_back(eval_poitou(gl, 0.5 + 0.05 * static_cast<double>(i)));
    }

    auto ub_log = [](int n, int u, int mode) -> double {
        // mode: 0 = even (9/2 * u), 1 = odd_A (27/8 * u), 2 = odd_B (2 * u)
        double C = (mode == 0) ? (4.5 * static_cast<double>(u))
                               : ((mode == 1) ? ((27.0 / 8.0) * static_cast<double>(u))
                                              : (2.0 * static_cast<double>(u)));
        return (2.0 / 3.0) * std::log(4.0 * kPi * kPi) + (2.0 / (3.0 * static_cast<double>(n))) * std::log(C);
    };

    rep.deg9_to_14_survivors = 0;
    rep.worst_deg9_margin = 1e9;
    rep.worst_deg10_margin = 1e9;
    rep.deg7_max_surviving_u = 0;
    rep.deg7_hge2_survivors = 0;
    rep.deg7_max_root_disc = 0.0;
    rep.deg8_max_surviving_u = 0;
    rep.deg8_hge2_survivors = 0;
    rep.deg8_max_root_disc = 0.0;
    rep.deg6_max_surviving_u = 0;
    rep.deg6_u16_h1_dead = 0;
    rep.deg6_u16_hge2_dead = 0;
    rep.deg6_u16_h1_margin = -1e9;
    rep.deg6_u16_hge2_margin = -1e9;
    rep.deg6_old_disc_ceiling = std::exp(6.0 * ub_log(6, 32, 0));
    rep.deg6_new_disc_ceiling = std::exp(6.0 * ub_log(6, 8, 0));

    for (int n = 6; n <= 14; ++n) {
        const int mode_start = (n % 2 == 0) ? 0 : 1;
        const int mode_end = (n % 2 == 0) ? 0 : 2;
        for (int mode = mode_start; mode <= mode_end; ++mode) {
            for (int k = 0; k < n; ++k) {
                const int u = 1 << k;
                const double ub = ub_log(n, u, mode);
                const double dn = static_cast<double>(n);

                // Pincer 1: F itself (totally real, deg n, 1 or 2 norm-2 primes).
                const double cf2_F = (mode == 1 ? 2.0 : 1.0) / dn;
                const double lb_F = best_lb_grid(grid, dn, 1.0, cf2_F, 0.0);

                // Pincer 3 subfields inside H_F^+/F when h_F = 1 (Gal = F_2^k, exponent 2 -> >= (1/2n) f_4 per norm-2 prime).
                double sub_h1 = -1e9;
                for (int j = 1; j <= k; ++j) {
                    double rho1 = 0.0;
                    if (j < k) {
                        const int64_t num = static_cast<int64_t>(n) * ((1LL << (k - j)) - 1LL);
                        const int64_t den = (1LL << k) - 1LL;
                        const int64_t r1_min = (num + den - 1LL) / den;
                        rho1 = static_cast<double>(r1_min) / dn;
                    }
                    const double cf4 = (mode == 1 ? 2.0 : 1.0) / (2.0 * dn);
                    const double val = best_lb_grid(grid, dn * static_cast<double>(1 << j), rho1, 0.0, cf4);
                    if (val > sub_h1) sub_h1 = val;
                }

                double lb_h1 = lb_F;
                if (k >= 1) {
                    const double cf4_extra = (mode == 1) ? (1.0 / (2.0 * dn)) : 0.0;
                    // Branch f_v = 1: v splits completely in H_F^+ (deg n*u).
                    const double b1 = best_lb_grid(grid, dn * static_cast<double>(u), 0.0, 1.0 / dn, cf4_extra);
                    const double lb_fv1 = std::max({lb_F, b1, sub_h1});
                    // Branch f_v = 2: v splits completely in decomposition field L_v (deg n*u/2) & contributes f4 in H_F^+.
                    const double b2_lv = best_lb_grid(grid, dn * static_cast<double>(u / 2), 0.0, 1.0 / dn, cf4_extra);
                    const double b2_h = best_lb_grid(grid, dn * static_cast<double>(u), 0.0, 0.0, (mode == 1 ? 2.0 : 1.0) / (2.0 * dn));
                    const double lb_fv2 = std::max({lb_F, b2_lv, b2_h, sub_h1});
                    lb_h1 = std::min(lb_fv1, lb_fv2);
                }

                // Pincer 2: h_F >= 2 -> wide Hilbert class field H_F totally real deg >= 2n + codim-j subfields in H_F^+/H_F.
                double lb_h2 = lb_F;
                for (int j = 0; j <= k; ++j) {
                    double rho1 = 0.0;
                    if (j == 0) {
                        rho1 = 1.0;
                    } else if (j < k) {
                        const int64_t num = static_cast<int64_t>(n) * ((1LL << (k - j)) - 1LL);
                        const int64_t den = (1LL << k) - 1LL;
                        const int64_t r1_min = (num + den - 1LL) / den;
                        rho1 = static_cast<double>(r1_min) / dn;
                    }
                    const double val = best_lb_grid(grid, 2.0 * dn * static_cast<double>(1 << j), rho1, 0.0, 0.0);
                    if (val > lb_h2) lb_h2 = val;
                }

                const double m1 = std::exp(lb_h1) - std::exp(ub);
                const double m2 = std::exp(lb_h2) - std::exp(ub);
                const bool dead1 = (lb_h1 > ub);
                const bool dead2 = (lb_h2 > ub);

                if (n >= 9) {
                    if (!dead1 || !dead2) ++rep.deg9_to_14_survivors;
                    if (n == 9) rep.worst_deg9_margin = std::min({rep.worst_deg9_margin, m1, m2});
                    if (n == 10) rep.worst_deg10_margin = std::min({rep.worst_deg10_margin, m1, m2});
                } else if (n == 8) {
                    if (!dead2) ++rep.deg8_hge2_survivors;
                    if (!dead1 || !dead2) {
                        rep.deg8_max_surviving_u = std::max(rep.deg8_max_surviving_u, u);
                        rep.deg8_max_root_disc = std::max(rep.deg8_max_root_disc, std::exp(ub));
                    }
                } else if (n == 7) {
                    if (!dead2) ++rep.deg7_hge2_survivors;
                    if (!dead1 || !dead2) {
                        rep.deg7_max_surviving_u = std::max(rep.deg7_max_surviving_u, u);
                        rep.deg7_max_root_disc = std::max(rep.deg7_max_root_disc, std::exp(ub));
                    }
                } else if (n == 6) {
                    if (u == 16) {
                        rep.deg6_u16_h1_dead = dead1 ? 1 : 0;
                        rep.deg6_u16_hge2_dead = dead2 ? 1 : 0;
                        rep.deg6_u16_h1_margin = m1;
                        rep.deg6_u16_hge2_margin = m2;
                    }
                    if (!dead1 || !dead2) {
                        rep.deg6_max_surviving_u = std::max(rep.deg6_max_surviving_u, u);
                    }
                }
            }
        }
    }

    rep.passed = rep.quadrature_self_check_ok &&
                 rep.q_explicit_formula_lb <= 0.0 && rep.q_explicit_formula_lb > -1e-4 &&
                 rep.tail15_e_minus_f2 > 0.0 && rep.tail15_lb_b42 > rep.tail15_ub &&
                 rep.deg9_to_14_survivors == 0 &&
                 rep.worst_deg9_margin > 0.30 &&
                 rep.worst_deg10_margin > 0.90 &&
                 rep.deg7_max_surviving_u == 4 && rep.deg7_hge2_survivors == 0 &&
                 rep.deg8_max_surviving_u == 4 && rep.deg8_hge2_survivors == 0 &&
                 rep.deg6_max_surviving_u == 8 &&
                 rep.deg6_u16_h1_dead == 1 && rep.deg6_u16_hge2_dead == 1 &&
                 rep.deg6_u16_h1_margin > 0.01 && rep.deg6_u16_hge2_margin > 0.30;
    return rep;
}

ShimuraGenus13Report verify_shimura_genus13_census() {
    ShimuraGenus13Report rep{};
    std::vector<int64_t> odd_primes;
    for (int64_t p = 3; p <= 1001; p += 2) {
        if (is_prime_i64(p)) odd_primes.push_back(p);
    }

    struct DCand {
        int64_t D;
        int64_t phiD;
        int64_t e2D;
        int64_t e3D;
    };
    std::vector<DCand> d_cands;
    auto gen_D = [&](auto&& self, std::size_t idx, int cnt, int64_t D, int64_t phiD, int64_t e2D, int64_t e3D) -> void {
        if (cnt >= 2 && cnt % 2 == 0) {
            d_cands.push_back({D, phiD, e2D, e3D});
        }
        for (std::size_t i = idx; i < odd_primes.size(); ++i) {
            const int64_t p = odd_primes[i];
            if (phiD * (p - 1) > 1000) break;
            self(self, i + 1, cnt + 1, D * p, phiD * (p - 1),
                 e2D * (1 - kronecker_neg4(p)), e3D * (1 - kronecker_neg3(p)));
        }
    };
    // Start with prime 2 in D (phi=1, 1-(-4/2)=1, 1-(-3/2)=2).
    gen_D(gen_D, 0, 1, 2, 1, 1, 2);

    for (const auto& dc : d_cands) {
        const int64_t max_n = 1000 / dc.phiD;
        for (int64_t N = 1; N <= max_n; N += 2) {
            if (gcd_local(dc.D, N) != 1) continue;
            int64_t tmp = N;
            int64_t psiN = 1;
            int64_t e2N = 1;
            int64_t e3N = 1;
            for (int64_t p = 3; p * p <= tmp; p += 2) {
                if (tmp % p == 0) {
                    int k = 0;
                    int64_t pk_minus_1 = 1;
                    while (tmp % p == 0) {
                        if (k >= 1) pk_minus_1 *= p;
                        tmp /= p;
                        ++k;
                    }
                    psiN *= pk_minus_1 * (p + 1);
                    e2N *= (1 + kronecker_neg4(p));
                    e3N *= (p == 3) ? (k == 1 ? 1 : 0) : (1 + kronecker_neg3(p));
                }
            }
            if (tmp > 1) {
                const int64_t p = tmp;
                psiN *= (p + 1);
                e2N *= (1 + kronecker_neg4(p));
                e3N *= (p == 3) ? 1 : (1 + kronecker_neg3(p));
            }
            if (dc.phiD * psiN > 1000) continue;
            const int64_t e2 = dc.e2D * e2N;
            const int64_t e3 = dc.e3D * e3N;
            const int64_t num = 12 + dc.phiD * psiN - 3 * e2 - 4 * e3;
            if (num == 12 * 13) {
                ++rep.total_pairs;
                if (e2 == 0 && e3 == 0) ++rep.torsion_free_pairs;
                if (dc.D == 690 && N == 1) {
                    rep.neg_e10_detected = 1;
                    rep.neg_e10_phi = static_cast<int32_t>(dc.phiD);
                    rep.neg_e10_e2 = static_cast<int32_t>(e2);
                    rep.neg_e10_e3 = static_cast<int32_t>(e3);
                }
            }
        }
    }

    // Enumerate ALL Gamma_H variants with 24 components (mass 12: phi(D) * psi(N) * d == 144,
    // d = [(Z/NZ)^* / {+-1} : H / {+-1}] >= 2 dividing phi(N)/2), across all 2-prime and multi-prime D.
    // Note: since (Z/NZ)^* is cyclic for every odd prime power N = p^k, here every hit has N in {5, 9, 17}
    // (prime power), so each divisor d | phi(N)/2 corresponds to a unique subgroup H >= {+-1}.
    for (const auto& dc : d_cands) {
        if (144 % dc.phiD != 0) continue;
        for (int64_t N = 3; N <= 144; N += 2) {
            if (gcd_local(dc.D, N) != 1) continue;
            int64_t tmp = N;
            int64_t psiN = 1;
            int64_t phiN = 1;
            for (int64_t p = 3; p * p <= tmp; p += 2) {
                if (tmp % p == 0) {
                    int64_t pk_minus_1 = 1;
                    int k = 0;
                    while (tmp % p == 0) {
                        if (k >= 1) pk_minus_1 *= p;
                        tmp /= p;
                        ++k;
                    }
                    psiN *= pk_minus_1 * (p + 1);
                    phiN *= pk_minus_1 * (p - 1);
                }
            }
            if (tmp > 1) {
                psiN *= (tmp + 1);
                phiN *= (tmp - 1);
            }
            if (144 % (dc.phiD * psiN) != 0) continue;
            const int64_t d = 144 / (dc.phiD * psiN);
            if (d >= 2 && (phiN / 2) % d == 0) {
                ++rep.gamma_h_count;
            }
        }
    }

    rep.passed = (rep.total_pairs == 19 &&
                  rep.torsion_free_pairs == 11 &&
                  rep.neg_e10_detected == 1 &&
                  rep.neg_e10_phi == 176 &&
                  rep.neg_e10_e2 == 0 &&
                  rep.neg_e10_e3 == 8 &&
                  rep.gamma_h_count == 4);
    return rep;
}

Section7ArithmeticCycle5Report verify_section7_arithmetic_cycle5() {
    Section7ArithmeticCycle5Report rep{};

    // 1. Prop 7.18(a): Exact Siegel real-quadratic scan D <= 1200 with 2 split (D = 1 mod 8) and h^+(D) = 1.
    for (int64_t D = 5; D <= 1200; ++D) {
        if (!is_fundamental_discriminant(D) || D % 8 != 1) continue;
        ++rep.quad_split2_scanned;
        int64_t z60 = 0;
        for (int64_t b = 1; b * b < D; b += 2) {
            z60 += 2 * sigma1_i64((D - b * b) / 4);
        }
        if (1440 % z60 != 0) continue;
        if (narrow_class_number_quad(D) != 1) continue;
        const int64_t P = 1440 / z60;
        const int32_t sols = count_quad_dn_solutions(D, P);
        rep.quad_hplus1_solutions += sols;
        if (D == 41) rep.quad_d41_solutions = sols;
        if (D == 137) rep.quad_d137_solutions = sols;
    }

    // 2. Prop 7.17(b): Exhaustive PGL_2(F_8) 504-element group census (order-3 free action on P^1(F_8)).
    // Canonical projective representatives: first nonzero entry in (a, b, c, d) normalized to 1.
    for (uint8_t a = 0; a < 8; ++a) {
        for (uint8_t b = 0; b < 8; ++b) {
            for (uint8_t c = 0; c < 8; ++c) {
                for (uint8_t d = 0; d < 8; ++d) {
                    const uint8_t det = static_cast<uint8_t>(f8_mul(a, d) ^ f8_mul(b, c));
                    if (det == 0) continue;
                    // Normalize: first nonzero entry must equal 1.
                    const uint8_t lead = (a != 0) ? a : ((b != 0) ? b : ((c != 0) ? c : d));
                    if (lead != 1) continue;
                    ++rep.pgl2_f8_order;
                    const F8Mat m{a, b, c, d};
                    if (f8_is_scalar(m)) continue;
                    const F8Mat m2 = f8_mat_mul(m, m);
                    const F8Mat m3 = f8_mat_mul(m2, m);
                    if (f8_is_scalar(m3)) {
                        ++rep.pgl2_f8_order3_count;
                        bool fixed = false;
                        for (int pt = 0; pt < 9; ++pt) {
                            if (f8_p1_act(m, pt) == pt) {
                                fixed = true;
                                break;
                            }
                        }
                        if (!fixed) ++rep.pgl2_f8_order3_free_count;
                    }
                }
            }
        }
    }

    // 3. Prop 7.3: Exact integer recurrence verifying tr(gamma_0^k)^2 > 4 det(gamma_0^k) for k = 1..12
    //    (gamma_0 = [[5, -12], [-12, 80]], tr = 85, det = 256 = 16^2).
    //    For k <= 9, check tk^2 > 4 * 256^k directly in __int128 (max ~5.3e34 < 1.7e38);
    //    for all k = 1..12, since tk > 0 and det_k = (16^k)^2, tk^2 > 4 * det_k <=> tk > 2 * 16^k.
    __int128 t_prev2 = 2;   // tr(I)
    __int128 t_prev1 = 85;  // tr(gamma_0)
    __int128 det_k = 256;
    __int128 sdet_k = 16;   // sqrt(det_k) = 16^k exact
    for (int k = 1; k <= 12; ++k) {
        __int128 tk = (k == 1) ? t_prev1 : (85 * t_prev1 - 256 * t_prev2);
        if (k >= 2) {
            t_prev2 = t_prev1;
            t_prev1 = tk;
            det_k *= 256;
            sdet_k *= 16;
        }
        bool ok_k = (tk > 2 * sdet_k);
        if (k <= 9) {
            ok_k = ok_k && (tk * tk > 4 * det_k);
        }
        if (ok_k) ++rep.gamma0_powers_obstructed;
    }

    rep.passed = (rep.quad_hplus1_solutions == 3 &&
                  rep.quad_d41_solutions == 2 &&
                  rep.quad_d137_solutions == 1 &&
                  rep.pgl2_f8_order == 504 &&
                  rep.pgl2_f8_order3_count == 56 &&
                  rep.pgl2_f8_order3_free_count == 56 &&
                  rep.gamma0_powers_obstructed == 12);
    return rep;
}

} // namespace ergentics
