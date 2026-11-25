#include "novelty.hpp"
#include "tonnetz.hpp"
#include "deterministic.hpp"
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <set>
#include <utility>
#include <vector>

namespace ergentics {

namespace {

inline int32_t circ_dist(int32_t a, int32_t b, int32_t n) {
    int32_t d = (a >= b) ? (a - b) : (b - a);
    return (2 * d <= n) ? d : (n - d);
}

inline std::array<int32_t, 3> sorted_triple(int32_t a, int32_t b, int32_t c) {
    std::array<int32_t, 3> v = {a, b, c};
    std::sort(v.begin(), v.end());
    return v;
}

inline std::pair<int32_t, int32_t> sorted_pair(int32_t a, int32_t b) {
    return (a < b) ? std::make_pair(a, b) : std::make_pair(b, a);
}

bool graph_has_cycle(int32_t n_nodes, const std::vector<std::pair<int32_t, int32_t>>& edges) {
    std::vector<int32_t> par(static_cast<std::size_t>(n_nodes));
    for (int32_t i = 0; i < n_nodes; ++i) par[static_cast<std::size_t>(i)] = i;
    auto find = [&](int32_t x) {
        while (par[static_cast<std::size_t>(x)] != x) {
            par[static_cast<std::size_t>(x)] = par[static_cast<std::size_t>(par[static_cast<std::size_t>(x)])];
            x = par[static_cast<std::size_t>(x)];
        }
        return x;
    };
    for (const auto& e : edges) {
        int32_t ru = find(e.first);
        int32_t rv = find(e.second);
        if (ru == rv) return true;
        par[static_cast<std::size_t>(ru)] = rv;
    }
    return false;
}

bool is_octatonic_diameter_triple(int32_t n, const std::array<int32_t, 3>& cls) {
    if (n % 8 != 0) return false;
    int32_t m = n / 8;
    std::array<int32_t, 3> ivs = {
        circ_dist(cls[0], cls[1], n),
        circ_dist(cls[1], cls[2], n),
        circ_dist(cls[0], cls[2], n)
    };
    std::sort(ivs.begin(), ivs.end());
    return ivs[0] == m && ivs[1] == 3 * m && ivs[2] == 4 * m;
}

// Explicit check of NEG-M11: N = 8, S = {2}, c0 = {0, 1, 4}, T/I-orbit.
// Two vertex-disjoint prime 4-cycles produce identical cyclic tune (3, 5, 7, 1).
bool verify_neg_m11_explicit() {
    const int32_t N = 8;
    std::set<std::array<int32_t, 3>> ti_orbit;
    for (int32_t t = 0; t < N; ++t) {
        ti_orbit.insert(sorted_triple(t % N, (t + 1) % N, (t + 4) % N));
        ti_orbit.insert(sorted_triple(t % N, (t + N - 1) % N, (t + N - 4) % N));
    }
    const std::array<std::array<int32_t, 3>, 4> cyc1 = {{
        {0, 1, 4}, {0, 3, 4}, {0, 4, 5}, {0, 4, 7}
    }};
    const std::array<std::array<int32_t, 3>, 4> cyc2 = {{
        {1, 2, 6}, {2, 3, 6}, {2, 5, 6}, {2, 6, 7}
    }};
    const std::array<int32_t, 4> expected_tune = {3, 5, 7, 1};

    auto check_cycle = [&](const std::array<std::array<int32_t, 3>, 4>& cyc,
                           std::array<int32_t, 4>& out_tune) -> bool {
        for (int i = 0; i < 4; ++i) {
            auto c = cyc[static_cast<std::size_t>(i)];
            if (ti_orbit.find(c) == ti_orbit.end()) return false;
            // Step-free for S = {2}: no circular distance in chord equals 2.
            if (circ_dist(c[0], c[1], N) == 2 ||
                circ_dist(c[1], c[2], N) == 2 ||
                circ_dist(c[0], c[2], N) == 2) {
                return false;
            }
            auto nxt = cyc[static_cast<std::size_t>((i + 1) % 4)];
            auto prv = cyc[static_cast<std::size_t>((i + 3) % 4)];
            if (nxt == prv) return false; // non-backtracking
            // Exactly 2 shared pitches, 1 moving voice with circular distance 2.
            int shared = 0;
            int32_t depart = -1, arrive = -1;
            for (int a = 0; a < 3; ++a) {
                bool found = false;
                for (int b = 0; b < 3; ++b) {
                    if (c[static_cast<std::size_t>(a)] == nxt[static_cast<std::size_t>(b)]) found = true;
                }
                if (found) shared++; else depart = c[static_cast<std::size_t>(a)];
            }
            for (int b = 0; b < 3; ++b) {
                bool found = false;
                for (int a = 0; a < 3; ++a) {
                    if (nxt[static_cast<std::size_t>(b)] == c[static_cast<std::size_t>(a)]) found = true;
                }
                if (!found) arrive = nxt[static_cast<std::size_t>(b)];
            }
            if (shared != 2 || depart < 0 || arrive < 0) return false;
            if (circ_dist(depart, arrive, N) != 2) return false;
            out_tune[static_cast<std::size_t>(i)] = arrive;
        }
        // Primitive check (period != 1, != 2).
        if (cyc[0] == cyc[2] && cyc[1] == cyc[3]) return false;
        return true;
    };

    std::array<int32_t, 4> t1{}, t2{};
    if (!check_cycle(cyc1, t1) || !check_cycle(cyc2, t2)) return false;
    if (t1 != expected_tune || t2 != expected_tune) return false;
    // Disjoint chord sets.
    for (const auto& a : cyc1) {
        for (const auto& b : cyc2) {
            if (a == b) return false;
        }
    }
    return true;
}

int32_t mobius_mu_local(int32_t n) {
    if (n <= 0) return 0;
    int32_t mu = 1;
    for (int32_t p = 2; p * p <= n; ++p) {
        if (n % p == 0) {
            n /= p;
            if (n % p == 0) return 0;
            mu = -mu;
        }
    }
    if (n > 1) mu = -mu;
    return mu;
}

struct AxisStats {
    int64_t total_primes;
    int64_t bad_div;
    double k2_over_m;
    double m_std4;
    double m2_std6;
};

AxisStats compute_tonnetz_axis_exact(int32_t s0, int32_t s1, int32_t s2, int32_t div_k, int32_t m) {
    int32_t succ[72][2];
    int32_t step_s[72];
    const int32_t ms[3] = {s0, s1, s2};
    for (int32_t v = 0; v < 24; ++v) {
        int32_t r = v % 12;
        for (int32_t mv = 0; mv < 3; ++mv) {
            int32_t e = 3 * v + mv;
            int32_t tv = 0;
            if (v < 12) {
                tv = (mv == 0) ? (12 + r) : (mv == 1 ? (12 + (r + 4) % 12) : (12 + (r + 9) % 12));
                step_s[e] = ms[mv];
            } else {
                tv = (mv == 0) ? r : (mv == 1 ? ((r + 8) % 12) : ((r + 3) % 12));
                step_s[e] = -ms[mv];
            }
            int idx = 0;
            for (int32_t mv2 = 0; mv2 < 3; ++mv2) {
                if (mv2 != mv) succ[e][idx++] = 3 * tv + mv2;
            }
        }
    }
    int32_t max_step = std::max(std::abs(s0), std::max(std::abs(s1), std::abs(s2)));
    int32_t max_s = max_step * m;
    int32_t stride = 2 * max_s + 1;
    int32_t off = max_s;
    int32_t max_w = max_s / div_k;
    int32_t w_stride = 2 * max_w + 1;

    std::vector<std::vector<int64_t>> n_dw(
        static_cast<std::size_t>(m + 1),
        std::vector<int64_t>(static_cast<std::size_t>(w_stride), 0)
    );
    int64_t bad_div = 0;
    std::vector<int64_t> cur(static_cast<std::size_t>(72 * stride), 0);
    std::vector<int64_t> nxt(static_cast<std::size_t>(72 * stride), 0);

    for (int32_t e0 = 0; e0 < 72; ++e0) {
        std::fill(cur.begin(), cur.end(), 0);
        cur[static_cast<std::size_t>(e0 * stride + off + step_s[e0])] = 1;
        for (int32_t d = 2; d <= m; ++d) {
            std::fill(nxt.begin(), nxt.end(), 0);
            int32_t slim = max_step * (d - 1);
            for (int32_t e = 0; e < 72; ++e) {
                int32_t base = e * stride;
                int32_t e1 = succ[e][0], e2 = succ[e][1];
                int32_t ds1 = step_s[e1], ds2 = step_s[e2];
                int32_t b1 = e1 * stride, b2 = e2 * stride;
                for (int32_t s = -slim; s <= slim; ++s) {
                    int64_t c = cur[static_cast<std::size_t>(base + off + s)];
                    if (c == 0) continue;
                    nxt[static_cast<std::size_t>(b1 + off + s + ds1)] += c;
                    nxt[static_cast<std::size_t>(b2 + off + s + ds2)] += c;
                }
            }
            cur.swap(nxt);
            if (d % 2 == 0 && (m % d == 0)) {
                int32_t slim_d = max_step * d;
                for (int32_t e = 0; e < 72; ++e) {
                    if (succ[e][0] != e0 && succ[e][1] != e0) continue;
                    int32_t base = e * stride;
                    for (int32_t s = -slim_d; s <= slim_d; ++s) {
                        int64_t c = cur[static_cast<std::size_t>(base + off + s)];
                        if (c == 0) continue;
                        if (s % div_k != 0) bad_div += c;
                        else n_dw[static_cast<std::size_t>(d)][static_cast<std::size_t>(s / div_k + max_w)] += c;
                    }
                }
            }
        }
    }

    std::vector<int64_t> pi_w(static_cast<std::size_t>(w_stride), 0);
    int64_t total_pi = 0;
    for (int32_t w = -max_w; w <= max_w; ++w) {
        int64_t acc = 0;
        for (int32_t d = 2; d <= m; d += 2) {
            if (m % d != 0) continue;
            int32_t k = m / d;
            if (w % k != 0) continue;
            int32_t mu = mobius_mu_local(k);
            if (mu == 0) continue;
            acc += static_cast<int64_t>(mu) * n_dw[static_cast<std::size_t>(d)][static_cast<std::size_t>(w / k + max_w)];
        }
        int64_t cnt = acc / m;
        pi_w[static_cast<std::size_t>(w + max_w)] = cnt;
        total_pi += cnt;
    }

    std::vector<double> t2(static_cast<std::size_t>(w_stride), 0.0);
    std::vector<double> t4(static_cast<std::size_t>(w_stride), 0.0);
    std::vector<double> t6(static_cast<std::size_t>(w_stride), 0.0);
    double inv_tot = 1.0 / static_cast<double>(total_pi);
    for (int32_t w = -max_w; w <= max_w; ++w) {
        std::size_t idx = static_cast<std::size_t>(w + max_w);
        double p = static_cast<double>(pi_w[idx]) * inv_tot;
        double wd = static_cast<double>(w);
        double w2 = wd * wd;
        t2[idx] = p * w2;
        t4[idx] = p * w2 * w2;
        t6[idx] = p * w2 * w2 * w2;
    }
    double m2 = sum_neumaier(t2.data(), t2.size());
    double m4 = sum_neumaier(t4.data(), t4.size());
    double m6 = sum_neumaier(t6.data(), t6.size());
    double k2 = m2;
    double k4 = m4 - 3.0 * m2 * m2;
    double k6 = m6 - 15.0 * m4 * m2 + 30.0 * m2 * m2 * m2;
    double dm = static_cast<double>(m);
    return AxisStats{
        total_pi,
        bad_div,
        k2 / dm,
        dm * (k4 / (k2 * k2)),
        dm * dm * (k6 / (k2 * k2 * k2))
    };
}

} // namespace

NoveltyTuneClassificationReport verify_novelty_tune_classification(int32_t n_max) {
    NoveltyTuneClassificationReport rep{};
    rep.n_max = n_max;
    rep.neg_m11_verified = verify_neg_m11_explicit();

    for (int32_t n = 5; n <= n_max; ++n) {
        // Deduplicate 3-note chord classes up to T/I equivalence (canonical minimal triple).
        std::set<std::array<int32_t, 3>> classes;
        for (int32_t a = 1; a < n; ++a) {
            for (int32_t b = a + 1; b < n; ++b) {
                std::array<int32_t, 3> best = {n, n, n};
                for (int32_t t = 0; t < n; ++t) {
                    auto c1 = sorted_triple((n - t) % n, (a + n - t) % n, (b + n - t) % n);
                    if (c1 < best) best = c1;
                    auto c2 = sorted_triple(t % n, (t + n - a) % n, (t + n - b) % n);
                    if (c2 < best) best = c2;
                }
                classes.insert(best);
            }
        }

        for (const auto& cls : classes) {
            rep.chords_tested++;
            int32_t d01 = circ_dist(cls[0], cls[1], n);
            int32_t d12 = circ_dist(cls[1], cls[2], n);
            int32_t d02 = circ_dist(cls[0], cls[2], n);

            // Maximal legal step set S_max(c0) = {1..floor(N/2)} \ I(c0).
            std::vector<int32_t> legal_steps;
            for (int32_t s = 1; s <= n / 2; ++s) {
                if (s != d01 && s != d12 && s != d02) legal_steps.push_back(s);
            }

            // Build full T/I orbit for Theorem A check (L_0 ∩ L_t).
            std::set<std::array<int32_t, 3>> ti_set;
            std::set<std::array<int32_t, 3>> t_set;
            for (int32_t t = 0; t < n; ++t) {
                auto ct = sorted_triple((cls[0] + t) % n, (cls[1] + t) % n, (cls[2] + t) % n);
                t_set.insert(ct);
                ti_set.insert(ct);
                auto ci = sorted_triple((n + t - cls[0]) % n, (n + t - cls[1]) % n, (n + t - cls[2]) % n);
                ti_set.insert(ci);
            }

            // Theorem A: check |L_0 ∩ L_t| <= 2 for all 1 <= t < N in full T/I orbit.
            std::vector<std::set<std::pair<int32_t, int32_t>>> links(static_cast<std::size_t>(n));
            for (const auto& c : ti_set) {
                links[static_cast<std::size_t>(c[0])].insert(sorted_pair(c[1], c[2]));
                links[static_cast<std::size_t>(c[1])].insert(sorted_pair(c[0], c[2]));
                links[static_cast<std::size_t>(c[2])].insert(sorted_pair(c[0], c[1]));
            }
            for (int32_t t = 1; t < n; ++t) {
                int32_t common = 0;
                for (const auto& p : links[0]) {
                    if (links[static_cast<std::size_t>(t)].count(p)) common++;
                }
                if (common > rep.max_link_intersection) rep.max_link_intersection = common;
            }

            // Theorem B: check one-moving-voice held-note cycles under S_max(c0) for T and T/I.
            auto has_one_voice_cycle = [&](const std::set<std::array<int32_t, 3>>& orb) -> bool {
                std::vector<std::vector<int32_t>> comp_list;
                // Map held pair (u, v) with u < v to sorted list of completions.
                std::vector<std::vector<int32_t>> comp_map(static_cast<std::size_t>(n * n));
                for (const auto& c : orb) {
                    comp_map[static_cast<std::size_t>(c[0] * n + c[1])].push_back(c[2]);
                    comp_map[static_cast<std::size_t>(c[0] * n + c[2])].push_back(c[1]);
                    comp_map[static_cast<std::size_t>(c[1] * n + c[2])].push_back(c[0]);
                }
                for (auto& v : comp_map) {
                    if (v.size() >= 3) {
                        std::sort(v.begin(), v.end());
                        v.erase(std::unique(v.begin(), v.end()), v.end());
                        if (v.size() >= 3) comp_list.push_back(std::move(v));
                    }
                }
                for (std::size_t i = 0; i < comp_list.size(); ++i) {
                    for (std::size_t j = i + 1; j < comp_list.size(); ++j) {
                        std::vector<int32_t> common;
                        std::set_intersection(
                            comp_list[i].begin(), comp_list[i].end(),
                            comp_list[j].begin(), comp_list[j].end(),
                            std::back_inserter(common)
                        );
                        if (common.size() < 3) continue;
                        std::vector<std::pair<int32_t, int32_t>> edges;
                        for (std::size_t a = 0; a < common.size(); ++a) {
                            for (std::size_t b = a + 1; b < common.size(); ++b) {
                                int32_t dist = circ_dist(common[a], common[b], n);
                                if (std::find(legal_steps.begin(), legal_steps.end(), dist) != legal_steps.end()) {
                                    edges.emplace_back(static_cast<int32_t>(a), static_cast<int32_t>(b));
                                }
                            }
                        }
                        if (graph_has_cycle(static_cast<int32_t>(common.size()), edges)) return true;
                    }
                }
                return false;
            };

            if (has_one_voice_cycle(t_set)) rep.t_orbit_failures++;
            if (has_one_voice_cycle(ti_set)) {
                if (is_octatonic_diameter_triple(n, cls)) rep.ti_octatonic_failures++;
                else rep.ti_unexpected_failures++;
            }
        }
    }

    int64_t expected_oct = static_cast<int64_t>(n_max / 8);
    rep.passed = (rep.max_link_intersection <= 2) &&
                 (rep.t_orbit_failures == 0) &&
                 (rep.ti_octatonic_failures == expected_oct) &&
                 (rep.ti_unexpected_failures == 0) &&
                 rep.neg_m11_verified;
    return rep;
}

EdgeworthWindingReport evaluate_edgeworth_winding_calibration(int32_t m) {
    EdgeworthWindingReport rep{};
    rep.length_m = m;
    WindingDistribution wd = compute_exact_winding_distribution(m);
    rep.total_primes = wd.total_primes;

    double p[17];
    double inv_tot = 1.0 / static_cast<double>(wd.total_primes);
    double t2[17], t4[17];
    for (int i = 0; i < 17; ++i) {
        p[i] = static_cast<double>(wd.prime_counts[i]) * inv_tot;
        double w = static_cast<double>(wd.w_min + i);
        double w2 = w * w;
        t2[i] = p[i] * w2;
        t4[i] = p[i] * w2 * w2;
    }
    double m2 = sum_neumaier(t2, 17);
    double m4 = sum_neumaier(t4, 17);
    double dm = static_cast<double>(m);
    double sig2 = dm / 24.0;
    double sig = std::sqrt(sig2);

    rep.variance = m2;
    rep.var_abs_error = std::fabs(m2 - sig2);
    rep.excess_kurtosis = m4 / (m2 * m2) - 3.0;
    rep.m_times_excess_kurtosis = dm * rep.excess_kurtosis;

    const double c4 = -17.0 / (48.0 * dm);
    const double c6 = 1469.0 / (2880.0 * dm * dm);
    const double c8 = 289.0 / (4608.0 * dm * dm);

    auto eval_order = [&](int order, double& out_tv, double& out_jsd, double* out_kl) {
        auto weight = [&](int wi) {
            double z = static_cast<double>(wi) / sig;
            double z2 = z * z;
            double base = std::exp(-0.5 * z2);
            if (order == 0) return base;
            double h4 = z2 * z2 - 6.0 * z2 + 3.0;
            double poly = 1.0 + c4 * h4;
            if (order >= 6) {
                double h6 = z2 * z2 * z2 - 15.0 * z2 * z2 + 45.0 * z2 - 15.0;
                double h8 = z2 * z2 * z2 * z2 - 28.0 * z2 * z2 * z2 + 210.0 * z2 * z2 - 420.0 * z2 + 105.0;
                poly += c6 * h6 + c8 * h8;
            }
            return std::max(0.0, base * poly);
        };
        double znorm = 0.0;
        for (int w = -24; w <= 24; ++w) znorm += weight(w);
        double q[17];
        for (int i = 0; i < 17; ++i) q[i] = weight(wd.w_min + i) / znorm;
        double q_in = sum_neumaier(q, 17);
        double q_out = std::max(0.0, 1.0 - q_in);
        double tv_sum = q_out;
        double kl = 0.0;
        double jsd = 0.5 * std::log(2.0) * q_out;
        for (int i = 0; i < 17; ++i) {
            tv_sum += std::fabs(p[i] - q[i]);
            double mid = 0.5 * (p[i] + q[i]);
            if (p[i] > 0.0) {
                jsd += 0.5 * p[i] * std::log(p[i] / mid);
                if (out_kl != nullptr && q[i] > 0.0) {
                    kl += p[i] * std::log(p[i] / q[i]);
                }
            }
            if (q[i] > 0.0) {
                jsd += 0.5 * q[i] * std::log(q[i] / mid);
            }
        }
        out_tv = 0.5 * tv_sum;
        out_jsd = jsd;
        if (out_kl != nullptr) *out_kl = kl;
    };

    eval_order(0, rep.tv_gaussian, rep.jsd_gaussian, &rep.kl_gaussian);
    eval_order(4, rep.tv_edgeworth4, rep.jsd_edgeworth4, nullptr);
    eval_order(6, rep.tv_edgeworth6, rep.jsd_edgeworth6, nullptr);
    rep.tv_gain_4 = (rep.tv_edgeworth4 > 0.0) ? (rep.tv_gaussian / rep.tv_edgeworth4) : 0.0;
    rep.tv_gain_6 = (rep.tv_edgeworth6 > 0.0) ? (rep.tv_gaussian / rep.tv_edgeworth6) : 0.0;

    bool ok = (wd.non_multiple_12_closed == 0) &&
              (rep.kl_gaussian >= 0.0) &&
              (rep.jsd_gaussian >= 0.0) &&
              (rep.jsd_edgeworth4 >= 0.0) &&
              (rep.jsd_edgeworth6 >= 0.0) &&
              (rep.tv_edgeworth4 < rep.tv_gaussian) &&
              (rep.jsd_edgeworth4 < rep.jsd_gaussian);
    if (m >= 24) {
        ok = ok && (rep.tv_edgeworth6 < rep.tv_edgeworth4) &&
                   (rep.jsd_edgeworth6 < rep.jsd_edgeworth4);
    }
    if (m == 40) {
        ok = ok && (std::fabs(rep.m_times_excess_kurtosis - (-8.5)) < 0.01) &&
                   (rep.tv_gain_4 > 10.0) &&
                   (rep.tv_gain_6 > 70.0) &&
                   (rep.var_abs_error < 1e-4);
    }
    rep.passed = ok;
    return rep;
}

TonnetzAxisCumulantReport verify_tonnetz_axis_cumulants(int32_t m) {
    TonnetzAxisCumulantReport rep{};
    rep.length_m = m;
    AxisStats su = compute_tonnetz_axis_exact(-1, -1, 2, 12, m);
    AxisStats sv = compute_tonnetz_axis_exact(-1, 2, -1, 9, m);
    AxisStats sa = compute_tonnetz_axis_exact(0, 1, -1, 1, m);

    rep.total_primes = su.total_primes;
    rep.bad_divisibility_count = su.bad_div + sv.bad_div + sa.bad_div;
    rep.k2_over_m_u = su.k2_over_m;
    rep.k2_over_m_v = sv.k2_over_m;
    rep.k2_over_m_zigzag = sa.k2_over_m;
    rep.m_ex_kurt_u = su.m_std4;
    rep.m_ex_kurt_v = sv.m_std4;
    rep.m_ex_kurt_zigzag = sa.m_std4;
    rep.max_isotropy_spread_4th = std::max(
        std::fabs(su.m_std4 - (-8.5)),
        std::max(std::fabs(sv.m_std4 - (-8.5)), std::fabs(sa.m_std4 - (-8.5)))
    );
    rep.m2_std6_u = su.m2_std6;
    rep.m2_std6_v = sv.m2_std6;
    rep.m2_std6_zigzag = sa.m2_std6;

    bool counts_match = (su.total_primes == sv.total_primes) && (su.total_primes == sa.total_primes);
    bool k2_ok = std::fabs(su.k2_over_m - 1.0 / 24.0) < 1e-3 &&
                 std::fabs(sv.k2_over_m - 2.0 / 27.0) < 1e-3 &&
                 std::fabs(sa.k2_over_m - 2.0) < 1e-2;
    bool iso4_ok = (m >= 36) ? (rep.max_isotropy_spread_4th < 0.05) : (rep.max_isotropy_spread_4th < 0.5);
    rep.passed = counts_match && (rep.bad_divisibility_count == 0) && k2_ok && iso4_ok;
    return rep;
}

} // namespace ergentics
