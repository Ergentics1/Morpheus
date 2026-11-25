#include "section7.hpp"
#include "tonnetz.hpp"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <set>
#include <tuple>
#include <vector>

namespace ergentics {

namespace {

using i128 = __int128_t;

inline i128 i128_abs(i128 x) { return x < 0 ? -x : x; }

inline int32_t v2_u64(uint64_t u) {
    if (u == 0ULL) return 1000000;
    int32_t c = 0;
    while ((u & 1ULL) == 0ULL) {
        u >>= 1ULL;
        ++c;
    }
    return c;
}

inline int32_t v2_i64(int64_t x) {
    if (x == 0) return 1000000;
    return v2_u64(x < 0 ? static_cast<uint64_t>(-x) : static_cast<uint64_t>(x));
}

// Determinant via Gaussian elimination with partial pivoting (for float Weil residual cross-check).
double det_lu_24(std::vector<double> m) {
    constexpr std::size_t n = 24;
    double sign = 1.0;
    for (std::size_t k = 0; k < n; ++k) {
        std::size_t piv = k;
        double best = std::abs(m[k * n + k]);
        for (std::size_t i = k + 1; i < n; ++i) {
            double v = std::abs(m[i * n + k]);
            if (v > best) { best = v; piv = i; }
        }
        if (best == 0.0) return 0.0;
        if (piv != k) {
            for (std::size_t j = k; j < n; ++j) std::swap(m[k * n + j], m[piv * n + j]);
            sign = -sign;
        }
        double diag = m[k * n + k];
        for (std::size_t i = k + 1; i < n; ++i) {
            double f = m[i * n + k] / diag;
            for (std::size_t j = k + 1; j < n; ++j) m[i * n + j] -= f * m[k * n + j];
        }
    }
    double det = sign;
    for (std::size_t i = 0; i < n; ++i) det *= m[i * n + i];
    return det;
}

// Exact multiplication of integer polynomials.
std::vector<int64_t> poly_mul(const std::vector<int64_t>& a, const std::vector<int64_t>& b) {
    std::vector<int64_t> out(a.size() + b.size() - 1, 0);
    for (std::size_t i = 0; i < a.size(); ++i) {
        for (std::size_t j = 0; j < b.size(); ++j) {
            out[i + j] += a[i] * b[j];
        }
    }
    return out;
}

// Exact Newton identities for P(u) = prod (1 - alpha_i u) = 1 + c_1 u + ... -> N_k = 2^k + 1 - sum alpha_i^k.
std::vector<int64_t> implied_f2_point_counts(const std::vector<int64_t>& c, int max_k) {
    std::vector<int64_t> s(static_cast<std::size_t>(max_k + 1), 0);
    std::vector<int64_t> N(static_cast<std::size_t>(max_k), 0);
    for (int k = 1; k <= max_k; ++k) {
        int64_t ck = (static_cast<std::size_t>(k) < c.size()) ? c[static_cast<std::size_t>(k)] : 0;
        int64_t acc = -static_cast<int64_t>(k) * ck;
        for (int j = 1; j < k; ++j) {
            int64_t cj = (static_cast<std::size_t>(j) < c.size()) ? c[static_cast<std::size_t>(j)] : 0;
            acc -= cj * s[static_cast<std::size_t>(k - j)];
        }
        s[static_cast<std::size_t>(k)] = acc;
        N[static_cast<std::size_t>(k - 1)] = (1LL << k) + 1LL - acc;
    }
    return N;
}

// Precomputed exact GF(2^k) multiplication table for k in 1..5.
struct GF2Table {
    int q;
    uint8_t mul[32][32];
    uint8_t sq[32];

    explicit GF2Table(int k) : q(1 << k) {
        static constexpr int kPolys[6] = {0, 0x2, 0x7, 0xB, 0x13, 0x25};
        int poly = kPolys[k];
        for (int a = 0; a < q; ++a) {
            for (int b = 0; b < q; ++b) {
                int res = 0;
                int aa = a;
                int bb = b;
                for (int bit = 0; bit < k; ++bit) {
                    if (bb & 1) res ^= aa;
                    bb >>= 1;
                    aa <<= 1;
                    if (aa & q) aa ^= poly;
                }
                mul[a][b] = static_cast<uint8_t>(res);
            }
            sq[a] = mul[a][a];
        }
    }
};

// Direct F_{2^k} projective point count on genus-5 complete intersections A and B in P^4 (Prop 7.10).
void count_prop7_10_curves(int k, int64_t& count_a, int64_t& count_b) {
    GF2Table gf(k);
    const int q = gf.q;
    int64_t ca = 0;
    int64_t cb = 0;

    auto eval_point = [&](uint8_t T, uint8_t U, uint8_t X, uint8_t Y, uint8_t Z) {
        uint8_t TT = gf.sq[T], UU = gf.sq[U], XX = gf.sq[X], YY = gf.sq[Y], ZZ = gf.sq[Z];
        uint8_t TU = gf.mul[T][U], TX = gf.mul[T][X], TY = gf.mul[T][Y], TZ = gf.mul[T][Z];
        uint8_t UX = gf.mul[U][X], UY = gf.mul[U][Y], UZ = gf.mul[U][Z];
        uint8_t XY = gf.mul[X][Y], XZ = gf.mul[X][Z], YZ = gf.mul[Y][Z];

        // Shared first quadric: TX + TZ + Y^2 + YZ + Z^2 = 0.
        uint8_t q1 = TX ^ TZ ^ YY ^ YZ ^ ZZ;
        if (q1 != 0) return;

        // Curve A:
        uint8_t a2 = TT ^ TU ^ TY ^ TZ ^ UU ^ UX ^ UZ ^ XZ ^ YY;
        if (a2 == 0) {
            uint8_t a3 = TY ^ UU ^ UX ^ UZ ^ XX ^ XY ^ XZ ^ YY ^ YZ ^ ZZ;
            if (a3 == 0) ++ca;
        }

        // Curve B:
        uint8_t b2 = TX ^ UX ^ UY ^ UZ;
        if (b2 == 0) {
            uint8_t b3 = TU ^ UU ^ UX ^ UY ^ UZ ^ XX ^ XY ^ XZ ^ YY ^ ZZ;
            if (b3 == 0) ++cb;
        }
    };

    // Normalized projective coordinates in P^4(F_q).
    for (int u = 0; u < q; ++u)
        for (int x = 0; x < q; ++x)
            for (int y = 0; y < q; ++y)
                for (int z = 0; z < q; ++z)
                    eval_point(1, static_cast<uint8_t>(u), static_cast<uint8_t>(x), static_cast<uint8_t>(y), static_cast<uint8_t>(z));
    for (int x = 0; x < q; ++x)
        for (int y = 0; y < q; ++y)
            for (int z = 0; z < q; ++z)
                eval_point(0, 1, static_cast<uint8_t>(x), static_cast<uint8_t>(y), static_cast<uint8_t>(z));
    for (int y = 0; y < q; ++y)
        for (int z = 0; z < q; ++z)
            eval_point(0, 0, 1, static_cast<uint8_t>(y), static_cast<uint8_t>(z));
    for (int z = 0; z < q; ++z)
        eval_point(0, 0, 0, 1, static_cast<uint8_t>(z));
    eval_point(0, 0, 0, 0, 1);

    count_a = ca;
    count_b = cb;
}

// Dhar's burning algorithm: returns true iff the q-reduced divisor equivalent to D has coeff(q) >= 1.
bool dhar_q_reduced_positive(const std::array<int32_t, 24>& adj3_0,
                             const std::array<int32_t, 24>& adj3_1,
                             const std::array<int32_t, 24>& adj3_2,
                             std::array<int32_t, 24> d,
                             int32_t q) {
    if (d[static_cast<std::size_t>(q)] >= 1) return true;
    int32_t burned_deg[24];
    bool burned[24];
    int32_t queue[24];

    for (;;) {
        for (int i = 0; i < 24; ++i) {
            burned_deg[i] = 0;
            burned[i] = false;
        }
        int head = 0, tail = 0;
        burned[q] = true;
        queue[tail++] = q;

        while (head < tail) {
            int32_t u = queue[head++];
            int32_t nbs[3] = {adj3_0[u], adj3_1[u], adj3_2[u]};
            for (int k = 0; k < 3; ++k) {
                int32_t v = nbs[k];
                if (burned[v]) continue;
                ++burned_deg[v];
                if (burned_deg[v] > d[static_cast<std::size_t>(v)]) {
                    burned[v] = true;
                    queue[tail++] = v;
                }
            }
        }
        if (tail == 24) {
            return d[static_cast<std::size_t>(q)] >= 1;
        }
        // Fire the unburned set U simultaneously.
        for (int v = 0; v < 24; ++v) {
            if (!burned[v]) {
                int32_t nbs[3] = {adj3_0[v], adj3_1[v], adj3_2[v]};
                for (int k = 0; k < 3; ++k) {
                    int32_t nb = nbs[k];
                    if (burned[nb]) {
                        d[static_cast<std::size_t>(v)] -= 1;
                        d[static_cast<std::size_t>(nb)] += 1;
                    }
                }
            }
        }
        if (d[static_cast<std::size_t>(q)] >= 1) return true;
    }
}

struct Mat2 {
    int64_t a, b, c, d;
};

Mat2 mat2_mul(Mat2 x, Mat2 y) {
    return {
        x.a * y.a + x.b * y.c,
        x.a * y.b + x.b * y.d,
        x.c * y.a + x.d * y.c,
        x.c * y.b + x.d * y.d
    };
}

// Odd modular inverse modulo 2^r (Newton-Hensel doubling).
uint64_t inv_mod_pow2(uint64_t x, int r) {
    uint64_t inv = 1ULL;
    for (int i = 0; i < 6; ++i) {
        inv = inv * (2ULL - x * inv);
    }
    if (r >= 64) return inv;
    return inv & ((1ULL << r) - 1ULL);
}

// Canonical Bruhat-Tits tree vertex invariant (kind, dist_r, residue mod 2^r) for lattice M * Z_2^2.
std::tuple<int32_t, int32_t, uint64_t> bruhat_tits_vertex_key(Mat2 m) {
    int32_t content = std::min(std::min(v2_i64(m.a), v2_i64(m.b)),
                               std::min(v2_i64(m.c), v2_i64(m.d)));
    int64_t a = m.a >> content;
    int64_t b = m.b >> content;
    int64_t c = m.c >> content;
    int64_t d = m.d >> content;
    int64_t det = a * d - b * c;
    int32_t r = v2_i64(det);
    if (r == 0) return {0, 0, 0ULL};
    uint64_t mask = (1ULL << r) - 1ULL;

    // Case 0: top row has an odd entry -> unique basis [(1, alpha), (0, 2^r)].
    if ((a & 1LL) != 0 || (b & 1LL) != 0) {
        int64_t u = ((a & 1LL) != 0) ? a : b;
        int64_t w = ((a & 1LL) != 0) ? c : d;
        uint64_t u_mod = static_cast<uint64_t>(u) & mask;
        uint64_t w_mod = static_cast<uint64_t>(w) & mask;
        uint64_t alpha = (w_mod * inv_mod_pow2(u_mod, r)) & mask;
        return {0, r, alpha};
    }
    // Case 1: top row both even -> bottom row has an odd entry -> unique basis [(beta, 1), (2^r, 0)] with beta even.
    int64_t u = ((c & 1LL) != 0) ? a : b;
    int64_t w = ((c & 1LL) != 0) ? c : d;
    uint64_t u_mod = static_cast<uint64_t>(u) & mask;
    uint64_t w_mod = static_cast<uint64_t>(w) & mask;
    uint64_t beta = (u_mod * inv_mod_pow2(w_mod, r)) & mask;
    return {1, r, beta};
}

} // namespace

SandpileSNFReport compute_sandpile_group_snf() {
    SandpileSNFReport rep{};
    constexpr std::size_t n = 23;
    std::vector<i128> lap(n * n, 0);

    // Exact 23x23 reduced Laplacian (drop vertex 23).
    for (int32_t v = 0; v < 23; ++v) {
        lap[static_cast<std::size_t>(v) * n + static_cast<std::size_t>(v)] = 3;
        for (int32_t mv = 0; mv < 3; ++mv) {
            int32_t u = apply_plr_move(v, mv).target_vertex;
            if (u < 23) {
                lap[static_cast<std::size_t>(v) * n + static_cast<std::size_t>(u)] = -1;
            }
        }
    }

    // 1. Exact Bareiss fraction-free determinant (intermediates bounded by Hadamard's bound, 55 bits << 127).
    std::vector<i128> B = lap;
    i128 prev_piv = 1;
    for (std::size_t k = 0; k < n; ++k) {
        std::size_t piv_row = k;
        while (piv_row < n && B[piv_row * n + k] == 0) ++piv_row;
        if (piv_row == n) return rep;
        if (piv_row != k) {
            for (std::size_t j = 0; j < n; ++j) std::swap(B[k * n + j], B[piv_row * n + j]);
        }
        i128 piv = B[k * n + k];
        for (std::size_t i = k + 1; i < n; ++i) {
            for (std::size_t j = k + 1; j < n; ++j) {
                i128 num = B[i * n + j] * piv - B[i * n + k] * B[k * n + j];
                if (num % prev_piv != 0) return rep;
                B[i * n + j] = num / prev_piv;
            }
        }
        prev_piv = piv;
    }
    const int64_t Delta = static_cast<int64_t>(i128_abs(B[(n - 1) * n + (n - 1)]));
    if (Delta <= 0) return rep;

    auto mod_d = [&](i128 x) -> int64_t {
        i128 r = x % static_cast<i128>(Delta);
        if (r < 0) r += static_cast<i128>(Delta);
        return static_cast<int64_t>(r);
    };
    auto gcd64 = [](int64_t a, int64_t b) -> int64_t {
        a = a < 0 ? -a : a;
        b = b < 0 ? -b : b;
        while (b != 0) { int64_t t = a % b; a = b; b = t; }
        return a;
    };
    auto ext_gcd = [](int64_t a, int64_t b, int64_t& s_out, int64_t& t_out) -> int64_t {
        int64_t old_r = a, r = b;
        int64_t old_s = 1, s = 0;
        int64_t old_t = 0, t = 1;
        while (r != 0) {
            int64_t q = old_r / r;
            int64_t nr = old_r - q * r; old_r = r; r = nr;
            int64_t ns = old_s - q * s; old_s = s; s = ns;
            int64_t nt = old_t - q * t; old_t = t; t = nt;
        }
        s_out = old_s;
        t_out = old_t;
        return old_r;
    };

    // 2. Exact Iliopoulos-Bezout modular SNF modulo Delta (eliminates 283-bit intermediate expression swell).
    std::vector<int64_t> M(n * n, 0);
    for (std::size_t idx = 0; idx < n * n; ++idx) M[idx] = mod_d(lap[idx]);

    auto swap_rows = [&](std::size_t r1, std::size_t r2) {
        if (r1 == r2) return;
        for (std::size_t j = 0; j < n; ++j) std::swap(M[r1 * n + j], M[r2 * n + j]);
    };
    auto swap_cols = [&](std::size_t c1, std::size_t c2) {
        if (c1 == c2) return;
        for (std::size_t i = 0; i < n; ++i) std::swap(M[i * n + c1], M[i * n + c2]);
    };
    auto unit_normalize_row = [&](std::size_t k) {
        int64_t a = M[k * n + k];
        int64_t s = 0, t = 0;
        int64_t g = ext_gcd(a, Delta, s, t);
        if (a == g) return;
        int64_t m = Delta / g;
        int64_t rem = g;
        int64_t extra_prod = 1;
        for (int64_t p = 2; p * p <= rem; ++p) {
            if (rem % p == 0) {
                while (rem % p == 0) rem /= p;
                if (m % p != 0) extra_prod *= p;
            }
        }
        if (rem > 1 && m % rem != 0) extra_prod *= rem;
        int64_t c1 = 0, c2 = 0;
        ext_gcd(m, extra_prod, c1, c2);
        int64_t u = mod_d(static_cast<i128>(s) * static_cast<i128>(extra_prod) * static_cast<i128>(c2) +
                          static_cast<i128>(m) * static_cast<i128>(c1));
        for (std::size_t j = k; j < n; ++j) {
            M[k * n + j] = mod_d(static_cast<i128>(u) * static_cast<i128>(M[k * n + j]));
        }
    };

    for (std::size_t k = 0; k < n; ++k) {
        for (;;) {
            bool found = false;
            std::size_t pi = k, pj = k;
            int64_t best_g = Delta + 1;
            for (std::size_t i = k; i < n; ++i) {
                for (std::size_t j = k; j < n; ++j) {
                    int64_t v = M[i * n + j];
                    if (v != 0) {
                        int64_t g = gcd64(v, Delta);
                        if (!found || g < best_g) {
                            found = true;
                            best_g = g;
                            pi = i;
                            pj = j;
                        }
                    }
                }
            }
            if (!found) break;
            swap_rows(k, pi);
            swap_cols(k, pj);
            unit_normalize_row(k);

            bool changed = false;
            for (std::size_t i = k + 1; i < n; ++i) {
                if (M[i * n + k] == 0) continue;
                int64_t a = M[k * n + k];
                int64_t b = M[i * n + k];
                if (b % a == 0) {
                    int64_t q = b / a;
                    for (std::size_t j = k; j < n; ++j) {
                        M[i * n + j] = mod_d(static_cast<i128>(M[i * n + j]) - static_cast<i128>(q) * static_cast<i128>(M[k * n + j]));
                    }
                } else {
                    int64_t s = 0, t = 0;
                    int64_t g = ext_gcd(a, b, s, t);
                    int64_t u1 = -b / g, u2 = a / g;
                    for (std::size_t j = k; j < n; ++j) {
                        i128 mk = static_cast<i128>(M[k * n + j]);
                        i128 mi = static_cast<i128>(M[i * n + j]);
                        M[k * n + j] = mod_d(static_cast<i128>(s) * mk + static_cast<i128>(t) * mi);
                        M[i * n + j] = mod_d(static_cast<i128>(u1) * mk + static_cast<i128>(u2) * mi);
                    }
                    unit_normalize_row(k);
                    changed = true;
                }
            }
            if (changed) continue;

            for (std::size_t j = k + 1; j < n; ++j) {
                if (M[k * n + j] == 0) continue;
                int64_t a = M[k * n + k];
                int64_t b = M[k * n + j];
                if (b % a == 0) {
                    int64_t q = b / a;
                    for (std::size_t i = k; i < n; ++i) {
                        M[i * n + j] = mod_d(static_cast<i128>(M[i * n + j]) - static_cast<i128>(q) * static_cast<i128>(M[i * n + k]));
                    }
                } else {
                    int64_t s = 0, t = 0;
                    int64_t g = ext_gcd(a, b, s, t);
                    int64_t u1 = -b / g, u2 = a / g;
                    for (std::size_t i = k; i < n; ++i) {
                        i128 mk = static_cast<i128>(M[i * n + k]);
                        i128 mj = static_cast<i128>(M[i * n + j]);
                        M[i * n + k] = mod_d(static_cast<i128>(s) * mk + static_cast<i128>(t) * mj);
                        M[i * n + j] = mod_d(static_cast<i128>(u1) * mk + static_cast<i128>(u2) * mj);
                    }
                    changed = true;
                }
            }
            if (changed) continue;

            int64_t piv = M[k * n + k];
            std::size_t bad_i = n;
            for (std::size_t i = k + 1; i < n && bad_i == n; ++i) {
                for (std::size_t j = k + 1; j < n; ++j) {
                    if (M[i * n + j] % piv != 0) { bad_i = i; break; }
                }
            }
            if (bad_i < n) {
                for (std::size_t j = k; j < n; ++j) M[k * n + j] = mod_d(static_cast<i128>(M[k * n + j]) + static_cast<i128>(M[bad_i * n + j]));
                continue;
            }
            break;
        }
    }

    // 3. Independent R-Type F_p nullity cross-check for every prime p | Delta (p = 2, 3, 23).
    auto nullity_mod_p = [&](int64_t p) -> int32_t {
        std::vector<int64_t> fp(n * n, 0);
        for (std::size_t idx = 0; idx < n * n; ++idx) {
            int64_t v = static_cast<int64_t>(lap[idx]) % p;
            fp[idx] = v < 0 ? v + p : v;
        }
        std::size_t rank = 0;
        for (std::size_t c = 0; c < n; ++c) {
            std::size_t piv = n;
            for (std::size_t i = rank; i < n; ++i) {
                if (fp[i * n + c] != 0) { piv = i; break; }
            }
            if (piv == n) continue;
            if (piv != rank) {
                for (std::size_t j = c; j < n; ++j) std::swap(fp[rank * n + j], fp[piv * n + j]);
            }
            int64_t s = 0, t = 0;
            ext_gcd(fp[rank * n + c], p, s, t);
            int64_t inv = ((s % p) + p) % p;
            for (std::size_t j = c; j < n; ++j) fp[rank * n + j] = (fp[rank * n + j] * inv) % p;
            for (std::size_t i = 0; i < n; ++i) {
                if (i == rank || fp[i * n + c] == 0) continue;
                int64_t f = fp[i * n + c];
                for (std::size_t j = c; j < n; ++j) {
                    fp[i * n + j] = (fp[i * n + j] - f * fp[rank * n + j]) % p;
                    if (fp[i * n + j] < 0) fp[i * n + j] += p;
                }
            }
            ++rank;
        }
        return static_cast<int32_t>(n - rank);
    };

    bool div_ok = true;
    int64_t order = 1;
    int32_t nt = 0;
    int64_t prev_d = 1;
    int32_t cnt2 = 0, cnt3 = 0, cnt23 = 0;
    for (std::size_t k = 0; k < n; ++k) {
        int64_t dk = (M[k * n + k] == 0) ? Delta : gcd64(M[k * n + k], Delta);
        if (dk <= 0 || (k > 0 && (dk % prev_d) != 0)) div_ok = false;
        prev_d = dk;
        order *= dk;
        if (dk % 2 == 0) ++cnt2;
        if (dk % 3 == 0) ++cnt3;
        if (dk % 23 == 0) ++cnt23;
        if (dk > 1 && nt < 8) rep.invariant_factors[nt++] = dk;
    }
    bool fp_ranks_ok = (cnt2 == nullity_mod_p(2)) && (cnt3 == nullity_mod_p(3)) && (cnt23 == nullity_mod_p(23));
    rep.nontrivial_count = nt;
    rep.group_order = order;
    rep.divisibility_chain_ok = div_ok && fp_ranks_ok && (order == Delta);
    rep.passed = rep.divisibility_chain_ok && nt == 5 &&
                 rep.invariant_factors[0] == 2 &&
                 rep.invariant_factors[1] == 2 &&
                 rep.invariant_factors[2] == 8 &&
                 rep.invariant_factors[3] == 736 &&
                 rep.invariant_factors[4] == 6624 &&
                 order == 156008448LL;
    return rep;
}

GonalityAutReport verify_gonality_and_automorphisms() {
    GonalityAutReport rep{};

    std::array<int32_t, 24> adj0{}, adj1{}, adj2{};
    bool adj[24][24] = {{false}};
    struct UEdge { int32_t u, v; };
    std::vector<UEdge> edges;
    for (int32_t v = 0; v < 24; ++v) {
        adj0[v] = apply_plr_move(v, 0).target_vertex;
        adj1[v] = apply_plr_move(v, 1).target_vertex;
        adj2[v] = apply_plr_move(v, 2).target_vertex;
        adj[v][adj0[v]] = adj[v][adj1[v]] = adj[v][adj2[v]] = true;
        if (v < 12) {
            edges.push_back({v, adj0[v]});
            edges.push_back({v, adj1[v]});
            edges.push_back({v, adj2[v]});
        }
    }

    // 1. Exhaustive backtracking enumeration of Aut(X) (BFS vertex ordering for instant pruning).
    std::vector<int32_t> order;
    bool seen[24] = {false};
    order.push_back(0);
    seen[0] = true;
    for (std::size_t qi = 0; qi < order.size(); ++qi) {
        int32_t u = order[qi];
        int32_t nbs[3] = {adj0[u], adj1[u], adj2[u]};
        for (int k = 0; k < 3; ++k) {
            if (!seen[nbs[k]]) { seen[nbs[k]] = true; order.push_back(nbs[k]); }
        }
    }

    std::vector<std::array<int32_t, 24>> auts;
    std::array<int32_t, 24> perm;
    perm.fill(-1);
    bool used[24] = {false};

    auto search_aut = [&](auto&& self, int32_t depth) -> void {
        if (depth == 24) {
            auts.push_back(perm);
            return;
        }
        int32_t v = order[static_cast<std::size_t>(depth)];
        // Collect already-mapped neighbors of v to restrict candidate images.
        int32_t mapped_nbs[3];
        int32_t mapped_cnt = 0;
        int32_t nbs[3] = {adj0[v], adj1[v], adj2[v]};
        for (int k = 0; k < 3; ++k) {
            if (perm[static_cast<std::size_t>(nbs[k])] >= 0) {
                mapped_nbs[mapped_cnt++] = perm[static_cast<std::size_t>(nbs[k])];
            }
        }
        auto try_img = [&](int32_t img) {
            if (used[img]) return;
            for (int k = 0; k < mapped_cnt; ++k) {
                if (!adj[img][mapped_nbs[k]]) return;
            }
            perm[static_cast<std::size_t>(v)] = img;
            used[img] = true;
            self(self, depth + 1);
            used[img] = false;
            perm[static_cast<std::size_t>(v)] = -1;
        };
        if (mapped_cnt == 0) {
            for (int32_t img = 0; img < 24; ++img) try_img(img);
        } else {
            int32_t anchor = mapped_nbs[0];
            try_img(adj0[anchor]);
            try_img(adj1[anchor]);
            try_img(adj2[anchor]);
        }
    };
    search_aut(search_aut, 0);
    rep.aut_order = static_cast<int32_t>(auts.size());

    // 2. Enumerate involutions in Aut(X) and test Chan's tree-quotient criterion.
    int32_t inv_cnt = 0;
    int32_t tree_q = 0;
    int32_t min_betti = 1000;
    for (const auto& p : auts) {
        bool is_id = true;
        bool is_inv = true;
        for (int i = 0; i < 24; ++i) {
            if (p[static_cast<std::size_t>(i)] != i) is_id = false;
            if (p[static_cast<std::size_t>(p[static_cast<std::size_t>(i)])] != i) is_inv = false;
        }
        if (is_id || !is_inv) continue;
        ++inv_cnt;

        // Vertex orbits count V_q; unfolded edge orbits count E_q (folded edges where p[u]==v add a leaf, +0 to Betti).
        int32_t v_orb = 0;
        for (int i = 0; i < 24; ++i) {
            if (i <= p[static_cast<std::size_t>(i)]) ++v_orb;
        }
        std::set<std::pair<int32_t, int32_t>> edge_orbits;
        int32_t unfolded_orbits = 0;
        for (const auto& e : edges) {
            int32_t pu = p[static_cast<std::size_t>(e.u)];
            int32_t pv = p[static_cast<std::size_t>(e.v)];
            if (pu == e.v && pv == e.u) continue; // folded to a degree-1 leaf
            int32_t a1 = std::min(e.u, e.v), b1 = std::max(e.u, e.v);
            int32_t a2 = std::min(pu, pv), b2 = std::max(pu, pv);
            auto rep_e = std::min(std::make_pair(a1, b1), std::make_pair(a2, b2));
            if (edge_orbits.insert(rep_e).second) ++unfolded_orbits;
        }
        int32_t betti = unfolded_orbits - v_orb + 1;
        if (betti < min_betti) min_betti = betti;
        if (betti == 0) ++tree_q;
    }
    rep.involution_count = inv_cnt;
    rep.tree_quotient_count = tree_q;
    rep.min_quotient_betti = min_betti;

    // 3. Exhaustive Dhar-burning rank check over all effective divisors D >= (C) of degree <= 5.
    auto has_rank_ge_1 = [&](const std::array<int32_t, 24>& d) -> bool {
        // Test farthest vertices first to prune non-rank-1 divisors on step 1.
        static constexpr int32_t q_order[24] = {
            6, 18, 17, 7, 5, 19, 11, 13, 1, 23, 2, 22, 3, 21, 4, 20, 8, 16, 9, 15, 10, 14, 12, 0
        };
        for (int idx = 0; idx < 24; ++idx) {
            if (!dhar_q_reduced_positive(adj0, adj1, adj2, d, q_order[idx])) return false;
        }
        return true;
    };

    int64_t tested = 0;
    int64_t found_le5 = 0;
    std::array<int32_t, 24> div{};
    div[0] = 1;

    auto enum_div = [&](auto&& self, int32_t rem, int32_t min_v) -> void {
        if (rem == 0) {
            ++tested;
            if (has_rank_ge_1(div)) ++found_le5;
            return;
        }
        for (int32_t v = min_v; v < 24; ++v) {
            ++div[static_cast<std::size_t>(v)];
            self(self, rem - 1, v);
            --div[static_cast<std::size_t>(v)];
        }
    };
    for (int32_t deg = 1; deg <= 5; ++deg) {
        enum_div(enum_div, deg - 1, 0);
    }
    rep.divisors_deg_le5_tested = tested;
    rep.rank1_deg_le5_found = found_le5;

    // 4. Verify degree-6 witness 2*C + 2*Am + Db + Abm (vertices 0, 21, 1, 20).
    std::array<int32_t, 24> witness{};
    witness[0] = 2;  // 2 C
    witness[21] = 2; // 2 Am (minor root 9 -> 12 + 9 = 21)
    witness[1] = 1;  // Db (major root 1)
    witness[20] = 1; // Abm (minor root 8 -> 12 + 8 = 20)
    rep.witness_deg6_rank1_ok = has_rank_ge_1(witness);
    rep.computed_gonality = (found_le5 == 0 && rep.witness_deg6_rank1_ok) ? 6 : -1;

    rep.passed = (rep.aut_order == 24) &&
                 (rep.involution_count == 13) &&
                 (rep.tree_quotient_count == 0) &&
                 (rep.min_quotient_betti >= 1) &&
                 (rep.divisors_deg_le5_tested == 20475) &&
                 (rep.rank1_deg_le5_found == 0) &&
                 rep.witness_deg6_rank1_ok &&
                 (rep.computed_gonality == 6);
    return rep;
}

F2CurvesReport verify_f2_curves_and_weil() {
    F2CurvesReport rep{};

    // Exact Weil factors (Theorem 3.5 / Prop 7.9):
    std::vector<int64_t> L1  = {1, -1, 2};
    std::vector<int64_t> L1p = {1,  1, 2};
    std::vector<int64_t> L2  = {1, 0, -1, 0, 4};
    std::vector<int64_t> L2p = {1, 0,  1, 0, 4};
    std::vector<int64_t> L4  = {1, 0, 4, 0, 9, 0, 16, 0, 16};

    std::vector<int64_t> p44 = {1};
    for (int i = 0; i < 3; ++i) p44 = poly_mul(p44, L1);
    for (int i = 0; i < 3; ++i) p44 = poly_mul(p44, L1p);
    for (int i = 0; i < 2; ++i) p44 = poly_mul(p44, L2);
    for (int i = 0; i < 2; ++i) p44 = poly_mul(p44, L2p);
    for (int i = 0; i < 2; ++i) p44 = poly_mul(p44, L4);

    auto n_p44 = implied_f2_point_counts(p44, 6);
    for (int i = 0; i < 6; ++i) rep.p44_point_counts[i] = n_p44[static_cast<std::size_t>(i)];

    // Verify Theorem 3.5 factorization against det(I - uA + 2u^2I) at multiple u values.
    double adj[576];
    build_adjacency_matrix(adj);
    double max_res = 0.0;
    const double us[3] = {0.11, 0.23, 0.37};
    for (double u : us) {
        std::vector<double> m(576, 0.0);
        for (int i = 0; i < 24; ++i) {
            for (int j = 0; j < 24; ++j) m[static_cast<std::size_t>(i * 24 + j)] = -u * adj[i * 24 + j];
            m[static_cast<std::size_t>(i * 24 + i)] += 1.0 + 2.0 * u * u;
        }
        double lhs = det_lu_24(m);
        double pval = 0.0;
        double up = 1.0;
        for (int64_t c : p44) { pval += static_cast<double>(c) * up; up *= u; }
        double rhs = (1.0 - u) * (1.0 - 2.0 * u) * (1.0 + u) * (1.0 + 2.0 * u) * pval;
        double err = std::abs(lhs - rhs);
        if (err > max_res) max_res = err;
    }
    rep.weil_factor_max_residual = max_res;

    // NEG-M6: cofactor a = 0 -> (1 + 2u^2) * L_4 forces (N_4 - N_2)/4 = -1 degree-4 places.
    auto p_a0 = poly_mul({1, 0, 2}, L4);
    auto n_a0 = implied_f2_point_counts(p_a0, 4);
    rep.cofactor_a0_deg4_places = (n_a0[3] - n_a0[1]) / 4;

    // Expected counts from L_A = (1 - u + 2u^2)*L_4 and L_B = (1 + u + 2u^2)*L_4.
    auto exp_a = implied_f2_point_counts(poly_mul(L1, L4), 5);
    auto exp_b = implied_f2_point_counts(poly_mul(L1p, L4), 5);
    bool curves_match = true;
    for (int k = 1; k <= 5; ++k) {
        int64_t ca = 0, cb = 0;
        count_prop7_10_curves(k, ca, cb);
        rep.curve_a_counts[k - 1] = ca;
        rep.curve_b_counts[k - 1] = cb;
        rep.expected_a_counts[k - 1] = exp_a[static_cast<std::size_t>(k - 1)];
        rep.expected_b_counts[k - 1] = exp_b[static_cast<std::size_t>(k - 1)];
        if (ca != rep.expected_a_counts[k - 1] || cb != rep.expected_b_counts[k - 1]) {
            curves_match = false;
        }
    }

    rep.passed = (rep.p44_point_counts[0] == 3) &&
                 (rep.p44_point_counts[1] == 39) &&
                 (rep.p44_point_counts[2] == 9) &&
                 (rep.p44_point_counts[3] == 75) &&
                 (rep.p44_point_counts[4] == 33) &&
                 (rep.p44_point_counts[5] == 27) &&
                 (rep.p44_point_counts[5] < rep.p44_point_counts[1]) &&
                 (rep.cofactor_a0_deg4_places == -1) &&
                 curves_match &&
                 (rep.weil_factor_max_residual < 1e-11);
    return rep;
}

Eisenstein12MapsReport verify_eisenstein_12_maps() {
    Eisenstein12MapsReport rep{};
    // Build set of 24 consonant triad 12-bit masks.
    uint32_t cons_masks[24];
    for (int r = 0; r < 12; ++r) {
        cons_masks[r] = (1U << r) | (1U << ((r + 4) % 12)) | (1U << ((r + 7) % 12));
        cons_masks[12 + r] = (1U << r) | (1U << ((r + 3) % 12)) | (1U << ((r + 7) % 12));
    }
    auto is_cons = [&](int x, int y, int z) -> bool {
        if (x == y || y == z || x == z) return false;
        uint32_t m = (1U << x) | (1U << y) | (1U << z);
        for (int i = 0; i < 24; ++i) if (cons_masks[i] == m) return true;
        return false;
    };
    auto gcd_i = [](int a, int b) {
        while (b != 0) { int t = a % b; a = b; b = t; }
        return a;
    };

    int32_t map_cnt = 0;
    int32_t min_c = 1000;
    int32_t max_c = 0;
    bool any_ideal = false;

    for (int a = 0; a < 12; ++a) {
        for (int b = 0; b < 12; ++b) {
            if (gcd_i(gcd_i(a, b), 12) != 1) continue;
            int ab = (a + b) % 12;
            if (!is_cons(0, a, ab) || !is_cons(0, ab, b)) continue;
            ++map_cnt;

            // Find smallest conductor d in 1..12 such that multiplication by d*omega preserves ker(psi).
            // omega * (m + n*omega) = -n + (m - n)*omega.
            int32_t cond = 12;
            for (int d = 1; d <= 12; ++d) {
                bool ok = true;
                for (int m = 0; m < 12 && ok; ++m) {
                    for (int n = 0; n < 12; ++n) {
                        if ((a * m + b * n) % 12 != 0) continue;
                        int val = (a * (-d * n) + b * (d * m - d * n)) % 12;
                        if (val != 0) { ok = false; break; }
                    }
                }
                if (ok) { cond = d; break; }
            }
            if (cond < min_c) min_c = cond;
            if (cond > max_c) max_c = cond;
            if (cond == 1) any_ideal = true;
        }
    }

    rep.tonnetz_map_count = map_cnt;
    rep.min_conductor = min_c;
    rep.max_conductor = max_c;
    rep.any_kernel_is_ideal = any_ideal;
    rep.passed = (map_cnt == 12) && (min_c == 12) && (max_c == 12) && !any_ideal;
    return rep;
}

SchottkyGroupReport verify_schottky_group() {
    SchottkyGroupReport rep{};
    const Mat2 sig[3] = {
        {0, 1, 2, 0},   // sigma_P
        {0, 2, 1, 0},   // sigma_L
        {-1, 1, 1, 1}   // sigma_R
    };

    // 1. BFS spanning tree of X -> 13 Schreier generators of K = ker(W -> D_12).
    std::vector<int32_t> parent(24, -1);
    std::vector<int32_t> parent_mv(24, -1);
    std::vector<std::vector<int32_t>> word_to(24);
    bool visited[24] = {false};
    bool in_tree[24][3] = {{false}};
    std::vector<int32_t> q;
    visited[0] = true;
    q.push_back(0);
    for (std::size_t qi = 0; qi < q.size(); ++qi) {
        int32_t u = q[qi];
        for (int32_t mv = 0; mv < 3; ++mv) {
            int32_t v = apply_plr_move(u, mv).target_vertex;
            if (!visited[v]) {
                visited[v] = true;
                parent[v] = u;
                parent_mv[v] = mv;
                word_to[v] = word_to[u];
                word_to[v].push_back(mv);
                in_tree[u][mv] = true;
                in_tree[v][mv] = true;
                q.push_back(v);
            }
        }
    }

    int32_t sch_cnt = 0;
    int32_t sch_hyp = 0;
    int32_t sch_ker = 0;
    for (int32_t u = 0; u < 12; ++u) {
        for (int32_t mv = 0; mv < 3; ++mv) {
            if (in_tree[u][mv]) continue;
            int32_t v = apply_plr_move(u, mv).target_vertex;
            // Schreier word: word_to[u] + [mv] + reverse(word_to[v]), reduced by cancelling adjacent equal moves.
            std::vector<int32_t> w = word_to[u];
            w.push_back(mv);
            for (int i = static_cast<int>(word_to[v].size()) - 1; i >= 0; --i) {
                w.push_back(word_to[v][static_cast<std::size_t>(i)]);
            }
            std::vector<int32_t> red;
            for (int32_t x : w) {
                if (!red.empty() && red.back() == x) red.pop_back();
                else red.push_back(x);
            }
            ++sch_cnt;

            // Check kernel membership on all 24 triads.
            bool fixes_all = true;
            for (int32_t t = 0; t < 24; ++t) {
                int32_t cur = t;
                for (int32_t m : red) cur = apply_plr_move(cur, m).target_vertex;
                if (cur != t) { fixes_all = false; break; }
            }
            if (fixes_all) ++sch_ker;

            // Compute exact 2x2 matrix & check hyperbolicity: 2 * v2(tr) < v2(det).
            Mat2 mat = {1, 0, 0, 1};
            for (int32_t m : red) mat = mat2_mul(mat, sig[m]);
            int64_t tr = mat.a + mat.d;
            int64_t det = mat.a * mat.d - mat.b * mat.c;
            if (2 * v2_i64(tr) < v2_i64(det)) ++sch_hyp;
        }
    }
    rep.schreier_count = sch_cnt;
    rep.schreier_hyperbolic = sch_hyp;
    rep.schreier_in_kernel = sch_ker;

    // 2. Simple transitivity on the Bruhat-Tits ball of radius 7 (382 reduced words).
    std::set<std::tuple<int32_t, int32_t, uint64_t>> bt_vertices;
    int32_t word_cnt = 0;
    auto dfs_ball = [&](auto&& self, int32_t depth, int32_t last_mv, Mat2 cur) -> void {
        ++word_cnt;
        bt_vertices.insert(bruhat_tits_vertex_key(cur));
        if (depth == 7) return;
        for (int32_t mv = 0; mv < 3; ++mv) {
            if (mv == last_mv) continue;
            self(self, depth + 1, mv, mat2_mul(cur, sig[mv]));
        }
    };
    dfs_ball(dfs_ball, 0, -1, {1, 0, 0, 1});
    rep.bt_ball_r7_words = word_cnt;
    rep.bt_ball_r7_distinct = static_cast<int32_t>(bt_vertices.size());

    // 3. Explicit trace obstruction generator gamma_0 = P L R L P R P L.
    const int32_t g0_word[8] = {0, 1, 2, 1, 0, 2, 0, 1};
    Mat2 g0 = {1, 0, 0, 1};
    for (int i = 0; i < 8; ++i) g0 = mat2_mul(g0, sig[g0_word[i]]);
    rep.gamma0_tr = g0.a + g0.d;
    rep.gamma0_det = g0.a * g0.d - g0.b * g0.c;
    rep.gamma0_tau_gt_4 = (rep.gamma0_tr * rep.gamma0_tr > 4 * rep.gamma0_det);

    rep.passed = (sch_cnt == 13) && (sch_hyp == 13) && (sch_ker == 13) &&
                 (word_cnt == 382) && (rep.bt_ball_r7_distinct == 382) &&
                 (rep.gamma0_tr == 85) && (rep.gamma0_det == 256) && rep.gamma0_tau_gt_4;
    return rep;
}

} // namespace ergentics
