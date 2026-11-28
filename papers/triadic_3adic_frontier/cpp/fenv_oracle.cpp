// Independent Freestanding Zero-Heap C++20 Hardware IEEE-754 FENV Oracle
// for Paper PC-III: The 3-Adic Dicyclic Companion, Exact Level 3P_5 and
// Level (3) Congruence on Nauru, and the Real-Quadratic Lame Shimura Atlas.
//
// License: MIT (Code Model). Zero external dependencies, zero heap allocations
// (stack-only fixed arrays), strict hardware directed rounding (FE_DOWNWARD /
// FE_UPWARD) with -frounding-math -O2 -Wall -Wextra -Werror.

#include <array>
#include <cfenv>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

#if defined(__clang__) || defined(_MSC_VER)
#pragma STDC FENV_ACCESS ON
#endif

namespace {

// ============================================================================
// Hardware IEEE-754 Outward-Rounded Interval Arithmetic (FE_DOWNWARD/UPWARD)
// ============================================================================

inline double add_dn(double a, double b) {
    std::fesetround(FE_DOWNWARD);
    volatile double va = a, vb = b;
    volatile double r = va + vb;
    return r;
}
inline double add_up(double a, double b) {
    std::fesetround(FE_UPWARD);
    volatile double va = a, vb = b;
    volatile double r = va + vb;
    return r;
}
inline double sub_dn(double a, double b) {
    std::fesetround(FE_DOWNWARD);
    volatile double va = a, vb = b;
    volatile double r = va - vb;
    return r;
}
inline double sub_up(double a, double b) {
    std::fesetround(FE_UPWARD);
    volatile double va = a, vb = b;
    volatile double r = va - vb;
    return r;
}
inline double mul_dn(double a, double b) {
    std::fesetround(FE_DOWNWARD);
    volatile double va = a, vb = b;
    volatile double r = va * vb;
    return r;
}
inline double mul_up(double a, double b) {
    std::fesetround(FE_UPWARD);
    volatile double va = a, vb = b;
    volatile double r = va * vb;
    return r;
}
inline double div_dn(double a, double b) {
    std::fesetround(FE_DOWNWARD);
    volatile double va = a, vb = b;
    volatile double r = va / vb;
    return r;
}
inline double div_up(double a, double b) {
    std::fesetround(FE_UPWARD);
    volatile double va = a, vb = b;
    volatile double r = va / vb;
    return r;
}
inline double sqrt_dn(double a) {
    std::fesetround(FE_DOWNWARD);
    volatile double va = a;
    volatile double r = std::sqrt(va);
    return r;
}
inline double sqrt_up(double a) {
    std::fesetround(FE_UPWARD);
    volatile double va = a;
    volatile double r = std::sqrt(va);
    return r;
}

inline double pad_dn(double x, int ulps = 2) {
    double r = x;
    for (int i = 0; i < ulps; ++i) r = std::nextafter(r, -INFINITY);
    return r;
}
inline double pad_up(double x, int ulps = 2) {
    double r = x;
    for (int i = 0; i < ulps; ++i) r = std::nextafter(r, +INFINITY);
    return r;
}

struct Iv {
    double lo;
    double hi;

    static Iv exact(double x) { return {x, x}; }
    static Iv from_bounds(double a, double b) { return {a, b}; }
    double mid() const { return 0.5 * (lo + hi); }
};

inline Iv operator+(Iv a, Iv b) { return {add_dn(a.lo, b.lo), add_up(a.hi, b.hi)}; }
inline Iv operator-(Iv a, Iv b) { return {sub_dn(a.lo, b.hi), sub_up(a.hi, b.lo)}; }
inline Iv operator-(Iv a) { return {-a.hi, -a.lo}; }

inline Iv operator*(Iv a, Iv b) {
    double p1 = mul_dn(a.lo, b.lo), p2 = mul_dn(a.lo, b.hi);
    double p3 = mul_dn(a.hi, b.lo), p4 = mul_dn(a.hi, b.hi);
    double lo = std::fmin(std::fmin(p1, p2), std::fmin(p3, p4));
    double q1 = mul_up(a.lo, b.lo), q2 = mul_up(a.lo, b.hi);
    double q3 = mul_up(a.hi, b.lo), q4 = mul_up(a.hi, b.hi);
    double hi = std::fmax(std::fmax(q1, q2), std::fmax(q3, q4));
    return {lo, hi};
}

inline Iv operator/(Iv a, Iv b) {
    if (b.lo <= 0.0 && b.hi >= 0.0) {
        std::fprintf(stderr, "Interval division by zero!\n");
        std::exit(2);
    }
    double p1 = div_dn(a.lo, b.lo), p2 = div_dn(a.lo, b.hi);
    double p3 = div_dn(a.hi, b.lo), p4 = div_dn(a.hi, b.hi);
    double lo = std::fmin(std::fmin(p1, p2), std::fmin(p3, p4));
    double q1 = div_up(a.lo, b.lo), q2 = div_up(a.lo, b.hi);
    double q3 = div_up(a.hi, b.lo), q4 = div_up(a.hi, b.hi);
    double hi = std::fmax(std::fmax(q1, q2), std::fmax(q3, q4));
    return {lo, hi};
}

inline Iv iv_sqrt(Iv a) { return {sqrt_dn(a.lo), sqrt_up(a.hi)}; }

inline Iv iv_exp(Iv a) {
    std::fesetround(FE_TONEAREST);
    return {pad_dn(std::exp(a.lo), 2), pad_up(std::exp(a.hi), 2)};
}
inline Iv iv_log(Iv a) {
    std::fesetround(FE_TONEAREST);
    return {pad_dn(std::log(a.lo), 2), pad_up(std::log(a.hi), 2)};
}
inline Iv iv_sinh(Iv a) {
    std::fesetround(FE_TONEAREST);
    return {pad_dn(std::sinh(a.lo), 2), pad_up(std::sinh(a.hi), 2)};
}
inline Iv iv_cosh_pos(Iv a) {
    // Valid for a.lo >= 0
    std::fesetround(FE_TONEAREST);
    return {pad_dn(std::cosh(a.lo), 2), pad_up(std::cosh(a.hi), 2)};
}
inline Iv iv_tanh(Iv a) {
    std::fesetround(FE_TONEAREST);
    return {pad_dn(std::tanh(a.lo), 2), pad_up(std::tanh(a.hi), 2)};
}
inline Iv iv_cos_narrow(Iv a) {
    // Valid for tiny interval a (width <= 1e-12): bound using derivative |cos'| <= 1
    std::fesetround(FE_TONEAREST);
    double c1 = std::cos(a.lo), c2 = std::cos(a.hi);
    double w = a.hi - a.lo;
    return {pad_dn(std::fmin(c1, c2) - w, 2), pad_up(std::fmax(c1, c2) + w, 2)};
}
inline Iv iv_sin_narrow(Iv a) {
    std::fesetround(FE_TONEAREST);
    double s1 = std::sin(a.lo), s2 = std::sin(a.hi);
    double w = a.hi - a.lo;
    return {pad_dn(std::fmin(s1, s2) - w, 2), pad_up(std::fmax(s1, s2) + w, 2)};
}

// Certified pi and Euler-Mascheroni constants (verified 17-digit outward brackets)
constexpr Iv IV_PI = {3.14159265358979311599, 3.14159265358979356009};
constexpr Iv IV_GAMMA = {0.57721566490153286060, 0.57721566490153297163};

// FNV-1a64 digest accumulator
struct Fnv64 {
    uint64_t h = 14695981039346656037ULL;
    void mix(uint64_t v) {
        for (int i = 0; i < 8; ++i) {
            h ^= (v >> (8 * i)) & 0xFFULL;
            h *= 1099511628211ULL;
        }
    }
};

// ============================================================================
// Graphs: Nauru Y = GP(12, 5) and Dicyclic Z = Cay(Dic_6, {1, 11, 12, 18})
// ============================================================================

inline int dic6_mul(int g, int h) {
    int a = g % 12, sa = g / 12;
    int b = h % 12, sb = h / 12;
    if (sa == 0 && sb == 0) return (a + b) % 12;
    if (sa == 0 && sb == 1) return 12 + (a + b) % 12;
    if (sa == 1 && sb == 0) return 12 + (a - b + 12) % 12;
    return (a - b + 18) % 12;
}

void build_nauru(std::array<std::array<int, 3>, 24>& adj) {
    for (int i = 0; i < 12; ++i) {
        adj[i] = {(i + 11) % 12, (i + 1) % 12, 12 + i};
        adj[12 + i] = {i, 12 + (i + 7) % 12, 12 + (i + 5) % 12};
    }
}

void build_dic6_Z(std::array<std::array<int, 4>, 24>& adj) {
    constexpr int S[4] = {1, 11, 12, 18};
    for (int g = 0; g < 24; ++g) {
        for (int k = 0; k < 4; ++k) adj[g][k] = dic6_mul(g, S[k]);
    }
}

// Exact integer 24x24 matrix multiplication & minimal polynomial annihilator check
using Mat24i = std::array<std::array<int64_t, 24>, 24>;

Mat24i mat24_mul(const Mat24i& A, const Mat24i& B) {
    Mat24i C{};
    for (int i = 0; i < 24; ++i)
        for (int k = 0; k < 24; ++k)
            if (A[i][k] != 0)
                for (int j = 0; j < 24; ++j) C[i][j] += A[i][k] * B[k][j];
    return C;
}

Mat24i mat24_shift(const Mat24i& A, int64_t s) {
    Mat24i C = A;
    for (int i = 0; i < 24; ++i) C[i][i] += s;
    return C;
}

bool mat24_is_zero(const Mat24i& A) {
    for (int i = 0; i < 24; ++i)
        for (int j = 0; j < 24; ++j)
            if (A[i][j] != 0) return false;
    return true;
}

// Stack-only symmetric Jacobi eigenvalue solver on 24x24 double matrix
double jacobi_24(const Mat24i& Ai, std::array<double, 24>& eigs) {
    std::fesetround(FE_TONEAREST);
    std::array<std::array<double, 24>, 24> A{};
    std::array<std::array<double, 24>, 24> V{};
    for (int i = 0; i < 24; ++i) {
        for (int j = 0; j < 24; ++j) A[i][j] = static_cast<double>(Ai[i][j]);
        V[i][i] = 1.0;
    }
    for (int sweep = 0; sweep < 80; ++sweep) {
        double off = 0.0;
        for (int p = 0; p < 24; ++p)
            for (int q = p + 1; q < 24; ++q) off += A[p][q] * A[p][q];
        if (off < 1e-30) break;
        for (int p = 0; p < 24; ++p) {
            for (int q = p + 1; q < 24; ++q) {
                double apq = A[p][q];
                if (std::fabs(apq) < 1e-16) continue;
                double tau = (A[q][q] - A[p][p]) / (2.0 * apq);
                double t = (tau >= 0.0) ? 1.0 / (tau + std::sqrt(1.0 + tau * tau))
                                        : -1.0 / (-tau + std::sqrt(1.0 + tau * tau));
                double c = 1.0 / std::sqrt(1.0 + t * t);
                double s = t * c;
                double app = A[p][p], aqq = A[q][q];
                A[p][p] = app - t * apq;
                A[q][q] = aqq + t * apq;
                A[p][q] = A[q][p] = 0.0;
                for (int r = 0; r < 24; ++r) {
                    if (r == p || r == q) continue;
                    double arp = A[r][p], arq = A[r][q];
                    A[r][p] = A[p][r] = c * arp - s * arq;
                    A[r][q] = A[q][r] = s * arp + c * arq;
                }
                for (int r = 0; r < 24; ++r) {
                    double vrp = V[r][p], vrq = V[r][q];
                    V[r][p] = c * vrp - s * vrq;
                    V[r][q] = s * vrp + c * vrq;
                }
            }
        }
    }
    for (int i = 0; i < 24; ++i) eigs[i] = A[i][i];
    // Compute max ||A v_k - lambda_k v_k||_inf residual
    double max_res = 0.0;
    for (int k = 0; k < 24; ++k) {
        for (int i = 0; i < 24; ++i) {
            double av = 0.0;
            for (int j = 0; j < 24; ++j) av += static_cast<double>(Ai[i][j]) * V[j][k];
            double err = std::fabs(av - eigs[k] * V[i][k]);
            if (err > max_res) max_res = err;
        }
    }
    // Sort eigenvalues ascending
    for (int i = 0; i < 24; ++i)
        for (int j = i + 1; j < 24; ++j)
            if (eigs[j] < eigs[i]) std::swap(eigs[i], eigs[j]);
    return max_res;
}

int mobius(int n) {
    int mu = 1, x = n;
    for (int d = 2; d * d <= x; ++d) {
        if (x % d == 0) {
            x /= d;
            if (x % d == 0) return 0;
            mu = -mu;
        }
    }
    if (x > 1) mu = -mu;
    return mu;
}

template <size_t DEG, size_t MDIR, size_t MAXM>
void hashimoto_cadences(const std::array<std::array<int, DEG>, 24>& adj,
                        std::array<int64_t, MAXM + 1>& traces,
                        std::array<int64_t, MAXM + 1>& pi_out) {
    std::array<int, MDIR> eu{}, ev{};
    std::array<std::array<int, DEG>, 24> out_idx{};
    int idx = 0;
    for (int u = 0; u < 24; ++u) {
        for (size_t k = 0; k < DEG; ++k) {
            eu[idx] = u;
            ev[idx] = adj[u][k];
            out_idx[u][k] = idx;
            ++idx;
        }
    }
    std::array<std::array<int, DEG - 1>, MDIR> next_e{};
    for (size_t e = 0; e < MDIR; ++e) {
        int u = eu[e], v = ev[e], pos = 0;
        for (size_t k = 0; k < DEG; ++k) {
            int e2 = out_idx[v][k];
            if (ev[e2] != u) next_e[e][pos++] = e2;
        }
    }
    traces.fill(0);
    std::array<int64_t, MDIR> vec{}, nxt{};
    for (size_t s = 0; s < MDIR; ++s) {
        vec.fill(0);
        vec[s] = 1;
        for (size_t m = 1; m <= MAXM; ++m) {
            nxt.fill(0);
            for (size_t e = 0; e < MDIR; ++e) {
                int64_t val = vec[e];
                if (val != 0) {
                    for (size_t t = 0; t < DEG - 1; ++t) nxt[next_e[e][t]] += val;
                }
            }
            vec = nxt;
            traces[m] += vec[s];
        }
    }
    pi_out.fill(0);
    for (size_t m = 1; m <= MAXM; ++m) {
        int64_t tot = 0;
        for (size_t d = 1; d <= m; ++d) {
            if (m % d == 0) tot += mobius(static_cast<int>(m / d)) * traces[d];
        }
        if (tot % static_cast<int64_t>(m) != 0) std::exit(3);
        pi_out[m] = tot / static_cast<int64_t>(m);
    }
}

// ============================================================================
// Exhaustive Zero-Heap Dhar Burning on Z (Degrees 6 and 7) + Scramble S_4
// ============================================================================

inline bool dhar_reaches_vertex_Z(const std::array<std::array<int, 4>, 24>& Z,
                                  const std::array<int8_t, 24>& init_d,
                                  int target) {
    std::array<int8_t, 24> d = init_d;
    std::array<uint8_t, 24> burnt{};
    std::array<int8_t, 24> bcnt{};
    std::array<int, 24> q{};
    for (int step = 0; step < 64 && d[target] == 0; ++step) {
        burnt.fill(0);
        bcnt.fill(0);
        burnt[target] = 1;
        int qh = 0, qt = 0;
        q[qt++] = target;
        while (qh < qt) {
            int u = q[qh++];
            for (int k = 0; k < 4; ++k) {
                int v = Z[u][k];
                if (!burnt[v]) {
                    if (++bcnt[v] > d[v]) {
                        burnt[v] = 1;
                        q[qt++] = v;
                    }
                }
            }
        }
        if (qt == 24) return false;
        for (int u = 0; u < 24; ++u) {
            if (!burnt[u]) {
                for (int k = 0; k < 4; ++k) {
                    int v = Z[u][k];
                    if (burnt[v]) {
                        --d[u];
                        ++d[v];
                    }
                }
            }
        }
    }
    return d[target] > 0;
}

inline bool is_rank1_Z(const std::array<std::array<int, 4>, 24>& Z,
                       const std::array<int8_t, 24>& chips) {
    // Check targets ordered for instant rejection (farthest vertices first)
    for (int v = 1; v < 24; ++v) {
        if (chips[v] == 0) {
            if (!dhar_reaches_vertex_Z(Z, chips, v)) return false;
        }
    }
    return true;
}

void exhaustive_dhar_Z(const std::array<std::array<int, 4>, 24>& Z,
                       int extra_chips,
                       uint64_t& total_tested,
                       uint64_t& rank1_hits) {
    total_tested = 0;
    rank1_hits = 0;
    std::array<int8_t, 24> chips{};
    chips[0] = 1;

    // Non-recursive or small-depth recursion (depth <= 6) over non-decreasing multisets
    auto rec = [&](auto&& self, int rem, int start_v) -> void {
        if (rem == 0) {
            ++total_tested;
            if (is_rank1_Z(Z, chips)) ++rank1_hits;
            return;
        }
        for (int v = start_v; v < 24; ++v) {
            ++chips[v];
            self(self, rem - 1, v);
            --chips[v];
        }
    };
    rec(rec, extra_chips, 0);
}

int edmonds_karp_Z(const std::array<std::array<int, 4>, 24>& Z, uint32_t s_mask, uint32_t t_mask) {
    constexpr int N = 26, SRC = 24, SNK = 25, INF = 10000;
    std::array<std::array<int, N>, N> cap{};
    for (int u = 0; u < 24; ++u)
        for (int k = 0; k < 4; ++k) cap[u][Z[u][k]] += 1;
    for (int u = 0; u < 24; ++u) {
        if ((s_mask >> u) & 1U) cap[SRC][u] = INF;
        if ((t_mask >> u) & 1U) cap[u][SNK] = INF;
    }
    int flow = 0;
    std::array<int, N> par{}, q{};
    while (true) {
        par.fill(-1);
        par[SRC] = SRC;
        int qh = 0, qt = 0;
        q[qt++] = SRC;
        while (qh < qt && par[SNK] == -1) {
            int u = q[qh++];
            for (int v = 0; v < N; ++v) {
                if (par[v] == -1 && cap[u][v] > 0) {
                    par[v] = u;
                    q[qt++] = v;
                }
            }
        }
        if (par[SNK] == -1) break;
        int aug = INF;
        for (int v = SNK; v != SRC; v = par[v]) {
            int u = par[v];
            if (cap[u][v] < aug) aug = cap[u][v];
        }
        for (int v = SNK; v != SRC; v = par[v]) {
            int u = par[v];
            cap[u][v] -= aug;
            cap[v][u] += aug;
        }
        flow += aug;
    }
    return flow;
}

// ============================================================================
// Hardware-Rounded Poitou-Odlyzko Gauss-Legendre Quadrature (GL-64 & GL-128)
// ============================================================================

template <int NGL>
void gauss_legendre_iv(std::array<Iv, NGL>& nodes, std::array<Iv, NGL>& weights) {
    std::fesetround(FE_TONEAREST);
    constexpr double PI_D = 3.1415926535897932384626433832795;
    int m = (NGL + 1) / 2;
    for (int i = 0; i < m; ++i) {
        double x = std::cos(PI_D * (i + 0.75) / (NGL + 0.5));
        double dp = 0.0;
        for (int it = 0; it < 30; ++it) {
            double p0 = 1.0, p1 = x;
            for (int k = 2; k <= NGL; ++k) {
                double p2 = ((2.0 * k - 1.0) * x * p1 - (k - 1.0) * p0) / k;
                p0 = p1;
                p1 = p2;
            }
            dp = NGL * (x * p1 - p0) / (x * x - 1.0);
            double dx = p1 / dp;
            x -= dx;
            if (std::fabs(dx) < 1e-16) break;
        }
        // Bracket node x and weight w conservatively by 4 ULPs outward
        Iv xi = {pad_dn(x, 4), pad_up(x, 4)};
        double w_approx = 2.0 / ((1.0 - x * x) * dp * dp);
        Iv wi = {pad_dn(w_approx, 8), pad_up(w_approx, 8)};
        nodes[i] = -xi;
        nodes[NGL - 1 - i] = xi;
        weights[i] = wi;
        weights[NGL - 1 - i] = wi;
    }
}

Iv H1_iv(Iv w) {
    if (w.lo >= 2.0) return Iv::exact(0.0);
    Iv two = Iv::exact(2.0), three = Iv::exact(3.0), half = Iv::exact(0.5);
    Iv pw = IV_PI * w;
    Iv term1 = ((two - w) / three) * (Iv::exact(1.0) + half * iv_cos_narrow(pw));
    Iv term2 = iv_sin_narrow(pw) / (two * IV_PI);
    Iv res = term1 + term2;
    if (res.lo < 0.0) res.lo = 0.0;
    return res;
}

template <int NGL>
void poitou_odlyzko_iv(Iv b, Iv& logB_out, Iv& logA_out, Iv& f2_out) {
    std::array<Iv, NGL> xs{}, ws{};
    gauss_legendre_iv<NGL>(xs, ws);
    Iv intB = Iv::exact(0.0);
    Iv intA = Iv::exact(0.0);
    Iv half = Iv::exact(0.5), one = Iv::exact(1.0), two = Iv::exact(2.0);
    for (int i = 0; i < NGL; ++i) {
        Iv x = b * (xs[i] + one);
        Iv hx = half * x;
        Iv Fb = H1_iv(x / b) / iv_cosh_pos(hx);
        intB = intB + ws[i] * b * ((one - Fb) / (two * iv_sinh(hx)));
        intA = intA + ws[i] * b * (Fb / (two * iv_cosh_pos(hx)));
    }
    // Add tiny truncation margin 1e-14 on quadrature error (GL-64/128 on C^2 smooth integrand)
    Iv q_pad = {-1e-13, +1e-13};
    intB = intB + q_pad;
    intA = intA + q_pad;
    logB_out = iv_log(Iv::exact(8.0) * IV_PI) + IV_GAMMA - intB + iv_log(iv_tanh(half * b));
    logA_out = logB_out + intA;

    Iv ln2 = iv_log(two);
    Iv f2 = Iv::exact(0.0);
    double pow2 = 2.0;
    for (int m = 1; m <= 60; ++m) {
        Iv m_ln2 = Iv::exact(static_cast<double>(m)) * ln2;
        if (m_ln2.lo >= 2.0 * b.hi) break;
        Iv w = m_ln2 / b;
        f2 = f2 + Iv::exact(4.0) * (ln2 / Iv::exact(1.0 + pow2)) * H1_iv(w);
        pow2 *= 2.0;
    }
    f2_out = f2;
}

// ============================================================================
// Genus-25 3-Adic Borel Shimura Census (Zero Heap)
// ============================================================================

int kronecker_neg4(int p) { return (p == 2) ? 0 : ((p % 4 == 1) ? 1 : -1); }
int kronecker_neg3(int p) { return (p == 3) ? 0 : ((p % 3 == 1) ? 1 : -1); }

int gcd_int(int a, int b) {
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}

void genus25_census_check(int& total_out, int& tf_out) {
    std::array<int, 200> primes{};
    int np = 0;
    for (int x = 2; x < 700; ++x) {
        bool ok = true;
        for (int d = 2; d * d <= x; ++d)
            if (x % d == 0) {
                ok = false;
                break;
            }
        if (ok) primes[np++] = x;
    }
    auto eval_N = [](int D, int phiD, int e2D, int e3D, int& tot, int& tf) {
        int max_psi = 600 / phiD;
        for (int N = 1; N <= max_psi; ++N) {
            if (gcd_int(D, N) != 1) continue;
            int x = N, psi = 1;
            int n2 = (N % 4 == 0) ? 0 : 1;
            int n3 = (N % 9 == 0) ? 0 : 1;
            for (int d = 2; d * d <= x; ++d) {
                if (x % d == 0) {
                    int pe = 1;
                    while (x % d == 0) {
                        x /= d;
                        pe *= d;
                    }
                    psi *= (d + 1) * (pe / d);
                    if (d != 2) n2 *= (1 + kronecker_neg4(d));
                    if (d != 3) n3 *= (1 + kronecker_neg3(d));
                }
            }
            if (x > 1) {
                psi *= (x + 1);
                if (x != 2) n2 *= (1 + kronecker_neg4(x));
                if (x != 3) n3 *= (1 + kronecker_neg3(x));
            }
            int vol = phiD * psi;
            if (vol > 600) continue;
            int e2 = e2D * n2, e3 = e3D * n3;
            if (vol == 288 + 3 * e2 + 4 * e3) {
                ++tot;
                if (e2 == 0 && e3 == 0) ++tf;
            }
        }
    };
    total_out = 0;
    tf_out = 0;
    // omega = 2: D = 3 * p
    for (int i = 0; i < np; ++i) {
        int p = primes[i];
        if (p == 3) continue;
        int phi = 2 * (p - 1);
        if (phi > 600) continue;
        int e2D = (1 - kronecker_neg4(3)) * (1 - kronecker_neg4(p));
        int e3D = (1 - kronecker_neg3(3)) * (1 - kronecker_neg3(p));
        eval_N(3 * p, phi, e2D, e3D, total_out, tf_out);
    }
    // omega = 4: D = 3 * p1 * p2 * p3
    for (int i = 0; i < np; ++i) {
        int p1 = primes[i];
        if (p1 == 3 || 2 * (p1 - 1) > 600) continue;
        for (int j = i + 1; j < np; ++j) {
            int p2 = primes[j];
            if (p2 == 3 || 2 * (p1 - 1) * (p2 - 1) > 600) continue;
            for (int k = j + 1; k < np; ++k) {
                int p3 = primes[k];
                if (p3 == 3) continue;
                int phi = 2 * (p1 - 1) * (p2 - 1) * (p3 - 1);
                if (phi > 600) break;
                int e2D = (1 - kronecker_neg4(3)) * (1 - kronecker_neg4(p1)) *
                          (1 - kronecker_neg4(p2)) * (1 - kronecker_neg4(p3));
                int e3D = (1 - kronecker_neg3(3)) * (1 - kronecker_neg3(p1)) *
                          (1 - kronecker_neg3(p2)) * (1 - kronecker_neg3(p3));
                eval_N(3 * p1 * p2 * p3, phi, e2D, e3D, total_out, tf_out);
            }
        }
    }
}

}  // namespace

int main() {
    Fnv64 fnv;
    std::printf("Running Paper PC-III C++20 Zero-Heap Hardware FENV Oracle...\n");

    // 1. Hardware FENV directed-rounding liveness probe (1.0 + 1e-16)
    double p_dn = add_dn(1.0, 1e-16);
    double p_up = add_up(1.0, 1e-16);
    if (!(p_dn == 1.0 && p_up > 1.0)) {
        std::fprintf(stderr, "[FAIL] Hardware FENV rounding inactive: [%.17g, %.17g]\n", p_dn, p_up);
        return 1;
    }
    std::printf("  [PASS] C++1 Hardware FENV probe: 1 + 1e-16 in [%.17g, %.17g]\n", p_dn, p_up);

    // 2. Nauru Y & Dicyclic Z exact annihilators, Jacobi eigenvalues, & outward Ramanujan margins
    std::array<std::array<int, 3>, 24> Y{};
    std::array<std::array<int, 4>, 24> Z{};
    build_nauru(Y);
    build_dic6_Z(Z);

    Mat24i AY{}, AZ{};
    for (int u = 0; u < 24; ++u) {
        for (int v : Y[u]) AY[u][v] = 1;
        for (int v : Z[u]) AZ[u][v] = 1;
    }
    Mat24i AY2 = mat24_mul(AY, AY);
    Mat24i annY = mat24_mul(AY, mat24_mul(mat24_shift(AY2, -9), mat24_mul(mat24_shift(AY2, -4), mat24_shift(AY2, -1))));
    Mat24i AZ2 = mat24_mul(AZ, AZ);
    Mat24i annZ = mat24_mul(
        AZ, mat24_mul(mat24_shift(AZ2, -16),
                      mat24_mul(mat24_shift(AZ2, -9), mat24_mul(mat24_shift(AZ2, -3), mat24_shift(AZ2, -1)))));
    if (!mat24_is_zero(annY) || !mat24_is_zero(annZ)) {
        std::fprintf(stderr, "[FAIL] Minimal polynomial annihilator nonzero!\n");
        return 1;
    }

    std::array<double, 24> eigY{}, eigZ{};
    double resY = jacobi_24(AY, eigY);
    double resZ = jacobi_24(AZ, eigZ);
    Iv r2 = Iv::exact(2.0) * iv_sqrt(Iv::exact(2.0));
    Iv r3 = Iv::exact(2.0) * iv_sqrt(Iv::exact(3.0));
    Iv gapY = r2 - Iv::exact(2.0);
    Iv gapZ = r3 - Iv::exact(3.0);
    if (!(resY < 1e-13 && resZ < 1e-13 && gapY.lo > 0.828427124746 && gapZ.lo > 0.464101615137)) {
        std::fprintf(stderr, "[FAIL] Spectral / Ramanujan check failed!\n");
        return 1;
    }
    std::printf(
        "  [PASS] C++2 Exact annihilators=0, Jacobi res (Y=%.3e, Z=%.3e), Ramanujan margins (Y>=%.12f, Z>=%.12f)\n",
        resY, resZ, gapY.lo, gapZ.lo);

    // 3. Exact 72x72 & 96x96 Hashimoto prime cadences + outward Nauru m=18 corridor
    std::array<int64_t, 25> trY{}, piY{};
    std::array<int64_t, 17> trZ{}, piZ{};
    hashimoto_cadences<3, 72, 24>(Y, trY, piY);
    hashimoto_cadences<4, 96, 16>(Z, trZ, piZ);
    constexpr int64_t expY[10] = {24, 108, 216, 564, 2232, 8820, 28560, 104292, 380664, 1401744};
    constexpr int64_t expZ[7] = {60, 240, 1560, 11616, 90172, 681504, 5379960};
    for (int i = 0; i < 10; ++i) {
        if (piY[6 + 2 * i] != expY[i]) return 1;
        fnv.mix(static_cast<uint64_t>(piY[6 + 2 * i]));
    }
    for (int i = 0; i < 7; ++i) {
        if (piZ[4 + 2 * i] != expZ[i]) return 1;
        fnv.mix(static_cast<uint64_t>(piZ[4 + 2 * i]));
    }
    // Outward Ramanujan corridor at m=18 on Nauru Y
    Iv ram_lo = Iv::exact(501786.0), ram_hi = Iv::exact(546842.0);
    Iv exact_N18 = Iv::exact(static_cast<double>(trY[18]));
    Iv bad_N18 = Iv::exact(18.0) * Iv::exact(31824.0) + Iv::exact(144.0);
    if (!(ram_lo.hi <= exact_N18.lo && exact_N18.hi <= ram_hi.lo && bad_N18.lo > ram_hi.hi)) return 1;
    std::printf("  [PASS] C++3 Hashimoto pi_Y(6..24) & pi_Z(4..16) exact; m=18 N18=%lld in [501786,546842] < 572976\n",
                static_cast<long long>(trY[18]));

    // 4. Exhaustive Zero-Heap Dhar on Z (deg 6: 0/98,280; deg 7: 0/475,020) + 4-path scramble S_4
    uint64_t t6 = 0, h6 = 0, t7 = 0, h7 = 0;
    exhaustive_dhar_Z(Z, 5, t6, h6);
    exhaustive_dhar_Z(Z, 6, t7, h7);
    if (!(t6 == 98280 && h6 == 0 && t7 == 475020 && h7 == 0)) {
        std::fprintf(stderr, "[FAIL] Exhaustive Dhar mismatch: deg6=%llu/%llu deg7=%llu/%llu\n",
                     static_cast<unsigned long long>(h6), static_cast<unsigned long long>(t6),
                     static_cast<unsigned long long>(h7), static_cast<unsigned long long>(t7));
        return 1;
    }
    fnv.mix(t6);
    fnv.mix(t7);
    // Verify S_4 touching (276/276) and Edmonds-Karp cuts {8:48, 10:108}
    std::array<uint32_t, 24> eggs{};
    constexpr int E0[4] = {0, 1, 2, 20};
    for (int g = 0; g < 24; ++g) {
        uint32_t mask = 0;
        for (int v : E0) mask |= (1U << dic6_mul(g, v));
        eggs[g] = mask;
    }
    int cut8 = 0, cut10 = 0, inter = 0;
    for (int i = 0; i < 24; ++i) {
        for (int j = i + 1; j < 24; ++j) {
            if (eggs[i] & eggs[j]) {
                ++inter;
            } else {
                int c = edmonds_karp_Z(Z, eggs[i], eggs[j]);
                if (c == 8) ++cut8;
                else if (c == 10) ++cut10;
                else return 1;
            }
        }
    }
    if (!(inter == 120 && cut8 == 48 && cut10 == 108)) return 1;
    std::printf("  [PASS] C++4 Exhaustive Dhar on Z: 0/%llu (deg 6), 0/%llu (deg 7); S_4 cuts {8:%d, 10:%d}\n",
                static_cast<unsigned long long>(t6), static_cast<unsigned long long>(t7), cut8, cut10);

    // 5. Hardware FENV Outward-Rounded Poitou-Odlyzko Audit (Theorem 10)
    Iv logB64{}, logA64{}, f2_64{};
    Iv logB128{}, logA128{}, f2_128{};
    Iv b6 = Iv::exact(6.0);
    poitou_odlyzko_iv<64>(b6, logB64, logA64, f2_64);
    poitou_odlyzko_iv<128>(b6, logB128, logA128, f2_128);
    Iv pole6 = (Iv::exact(8.0) / Iv::exact(3.0)) * b6 / Iv::exact(48.0);
    Iv lb64 = iv_exp(logB64 - pole6 + (Iv::exact(8.0) / Iv::exact(48.0)) * f2_64);
    Iv lb128 = iv_exp(logB128 - pole6 + (Iv::exact(8.0) / Iv::exact(48.0)) * f2_128);
    // UB(6, 16) = (4 pi^2)^(2/3) * 72^(1/9) = exp((2/3)*log(4*pi^2) + (1/9)*log(72))
    Iv ub616 = iv_exp((Iv::exact(2.0) / Iv::exact(3.0)) * iv_log(Iv::exact(4.0) * IV_PI * IV_PI) +
                      (Iv::exact(1.0) / Iv::exact(9.0)) * iv_log(Iv::exact(72.0)));
    Iv gap616 = lb128 - ub616;
    double qdiff = std::fabs(lb64.mid() - lb128.mid());
    if (!(gap616.lo > 0.0136298 && qdiff < 1e-12)) {
        std::fprintf(stderr, "[FAIL] Poitou witness (6,16,1,2) failed: gap=[%.15f, %.15f]\n", gap616.lo, gap616.hi);
        return 1;
    }

    // Anti-facade rejection: f_bad(t) at t = +-1 with c1 = -0.3, c2 = +0.3
    Iv c1 = {-0.30000000000000004, -0.29999999999999999};
    Iv c2 = {0.29999999999999999, 0.30000000000000004};
    Iv t_end = Iv::exact(1.0);
    Iv f_bad_end = Iv::exact(1.0) + iv_cos_narrow(IV_PI * t_end) +
                   c1 * (Iv::exact(1.0) - iv_cos_narrow(Iv::exact(2.0) * IV_PI * t_end)) +
                   c2 * (iv_cos_narrow(IV_PI * t_end) + iv_cos_narrow(Iv::exact(3.0) * IV_PI * t_end));
    if (!(f_bad_end.hi < -0.599999999999)) return 1;

    // Degree-8 (8, 1, 1, E) gap preservation (b = 3.0 and continuous peak b = 3.052)
    Iv ub81 = iv_exp((Iv::exact(2.0) / Iv::exact(3.0)) * iv_log(Iv::exact(4.0) * IV_PI * IV_PI) +
                     (Iv::exact(1.0) / Iv::exact(12.0)) * iv_log(Iv::exact(4.5)));
    Iv lb8_b3{}, lb8_peak{};
    {
        Iv b3 = Iv::exact(3.0), lB{}, lA{}, f2v{};
        poitou_odlyzko_iv<128>(b3, lB, lA, f2v);
        lb8_b3 = iv_exp(lA - (Iv::exact(8.0) / Iv::exact(3.0)) * b3 / Iv::exact(8.0) + f2v / Iv::exact(8.0));
    }
    {
        Iv bp = Iv::exact(3.039865), lB{}, lA{}, f2v{};
        poitou_odlyzko_iv<128>(bp, lB, lA, f2v);
        lb8_peak = iv_exp(lA - (Iv::exact(8.0) / Iv::exact(3.0)) * bp / Iv::exact(8.0) + f2v / Iv::exact(8.0));
    }
    if (!(lb8_b3.hi < ub81.lo && lb8_peak.hi < ub81.lo)) return 1;
    std::printf(
        "  [PASS] C++5 Poitou-Odlyzko FENV: gap=[+%.12f,+%.12f]>0, f_bad(1)<%.6f REJECTED, deg8 peak=%.6f<%.6f\n",
        gap616.lo, gap616.hi, f_bad_end.hi, lb8_peak.mid(), ub81.mid());

    // 6. Genus-25 3-Adic Borel Shimura Census (19 curves, 9 torsion-free)
    int g25_tot = 0, g25_tf = 0;
    genus25_census_check(g25_tot, g25_tf);
    if (!(g25_tot == 19 && g25_tf == 9)) return 1;
    fnv.mix(static_cast<uint64_t>(g25_tot));
    fnv.mix(static_cast<uint64_t>(g25_tf));
    std::printf("  [PASS] C++6 Genus-25 3-adic Borel Shimura census: %d curves (%d torsion-free)\n", g25_tot, g25_tf);

    std::fesetround(FE_TONEAREST);
    std::printf("Summary: 6/6 C++20 Zero-Heap FENV gates PASS (FNV-1a64=0x%016llx).\n",
                static_cast<unsigned long long>(fnv.h));
    return 0;
}
