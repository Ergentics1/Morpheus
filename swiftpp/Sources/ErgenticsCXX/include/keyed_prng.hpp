#pragma once
#include <cstdint>
#include <cstddef>
#include <cmath>

namespace ergentics {

// Domain-separated keyed PRNG (SplitMix64 seeding + Xoshiro256**).
// Zero global RNG state: every trial/check receives an explicit key for bit-exact replay.
struct PRNGKey {
    uint64_t suite_hash;
    uint64_t experiment_hash;
    uint64_t trial_index;
    uint64_t seed;
};

inline uint64_t fnv1a_64_bytes(const uint8_t* data, std::size_t len) {
    uint64_t h = 14695981039346656037ULL;
    for (std::size_t i = 0; i < len; ++i) {
        h ^= static_cast<uint64_t>(data[i]);
        h *= 1099511628211ULL;
    }
    return h;
}

inline uint64_t fnv1a_64_cstr(const char* s) {
    uint64_t h = 14695981039346656037ULL;
    if (!s) return h;
    while (*s) {
        h ^= static_cast<uint8_t>(*s++);
        h *= 1099511628211ULL;
    }
    return h;
}

inline uint64_t splitmix64_next(uint64_t& state) {
    uint64_t z = (state += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

inline uint64_t rotl64(uint64_t x, int k) {
    return (x << k) | (x >> (64 - k));
}

struct KeyedPRNG {
    uint64_t s0;
    uint64_t s1;
    uint64_t s2;
    uint64_t s3;

    static KeyedPRNG from_key(PRNGKey key) {
        // Domain-separated mixing of all 4 key components via SplitMix64.
        uint64_t seed_acc = key.seed ^ 0x243F6A8885A308D3ULL;
        seed_acc = splitmix64_next(seed_acc) ^ key.suite_hash;
        seed_acc = splitmix64_next(seed_acc) ^ key.experiment_hash;
        seed_acc = splitmix64_next(seed_acc) ^ key.trial_index;

        KeyedPRNG rng{};
        rng.s0 = splitmix64_next(seed_acc);
        rng.s1 = splitmix64_next(seed_acc);
        rng.s2 = splitmix64_next(seed_acc);
        rng.s3 = splitmix64_next(seed_acc);
        if ((rng.s0 | rng.s1 | rng.s2 | rng.s3) == 0ULL) {
            rng.s0 = 1ULL;
        }
        return rng;
    }

    static KeyedPRNG make(const char* suite, const char* experiment, uint64_t trial, uint64_t seed) {
        PRNGKey k{fnv1a_64_cstr(suite), fnv1a_64_cstr(experiment), trial, seed};
        return from_key(k);
    }

    uint64_t next_u64() {
        const uint64_t result = rotl64(s1 * 5ULL, 7) * 9ULL;
        const uint64_t t = s1 << 17;
        s2 ^= s0;
        s3 ^= s1;
        s1 ^= s2;
        s0 ^= s3;
        s2 ^= t;
        s3 = rotl64(s3, 45);
        return result;
    }

    // Uniform in [0, 1) with exact 53-bit IEEE-754 mantissa resolution.
    double next_unit_f64() {
        constexpr double inv_2_53 = 1.0 / 9007199254740992.0; // 2^-53
        return static_cast<double>(next_u64() >> 11) * inv_2_53;
    }

    // Unbiased bounded integer in [0, bound) via Lemire rejection sampling.
    uint64_t next_bounded(uint64_t bound) {
        if (bound <= 1ULL) return 0ULL;
        const uint64_t threshold = (~bound + 1ULL) % bound;
        for (;;) {
            uint64_t r = next_u64();
            if (r >= threshold) return r % bound;
        }
    }

    // Standard normal N(0, 1) via Box-Muller using open interval (0, 1].
    double next_normal_f64() {
        constexpr double two_pi = 6.283185307179586476925286766559;
        double u1 = next_unit_f64();
        if (u1 <= 0.0) u1 = 0.5 / 9007199254740992.0;
        double u2 = next_unit_f64();
        return std::sqrt(-2.0 * std::log(u1)) * std::cos(two_pi * u2);
    }
};

// Free C++-interop helper functions for Swift ergonomics.
inline KeyedPRNG cxx_make_prng(uint64_t suite_h, uint64_t exp_h, uint64_t trial, uint64_t seed) {
    return KeyedPRNG::from_key(PRNGKey{suite_h, exp_h, trial, seed});
}

inline uint64_t cxx_prng_next_u64(KeyedPRNG* rng) { return rng->next_u64(); }
inline double cxx_prng_next_unit(KeyedPRNG* rng) { return rng->next_unit_f64(); }
inline uint64_t cxx_prng_next_bounded(KeyedPRNG* rng, uint64_t bound) { return rng->next_bounded(bound); }
inline double cxx_prng_next_normal(KeyedPRNG* rng) { return rng->next_normal_f64(); }

} // namespace ergentics
