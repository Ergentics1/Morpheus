import Foundation

/// Domain-separated keyed PRNG (SplitMix64 seeding + Xoshiro256**).
/// Zero global RNG state: every trial/check receives an explicit key for bit-exact replay.
public struct PRNGKey: Sendable, Equatable, Hashable {
    public let suiteHash: UInt64
    public let experimentHash: UInt64
    public let trialIndex: UInt64
    public let seed: UInt64

    public init(suiteHash: UInt64, experimentHash: UInt64, trialIndex: UInt64, seed: UInt64) {
        self.suiteHash = suiteHash
        self.experimentHash = experimentHash
        self.trialIndex = trialIndex
        self.seed = seed
    }

    public init(suite: String, experiment: String, trialIndex: UInt64, seed: UInt64) {
        self.suiteHash = fnv1a64(suite)
        self.experimentHash = fnv1a64(experiment)
        self.trialIndex = trialIndex
        self.seed = seed
    }
}

@inline(__always)
public func fnv1a64(_ text: String) -> UInt64 {
    var h: UInt64 = 14695981039346656037
    for b in text.utf8 {
        h ^= UInt64(b)
        h = h &* 1099511628211
    }
    return h
}

@inline(__always)
public func splitmix64Next(_ state: inout UInt64) -> UInt64 {
    state = state &+ 0x9E3779B97F4A7C15
    var z = state
    z = (z ^ (z >> 30)) &* 0xBF58476D1CE4E5B9
    z = (z ^ (z >> 27)) &* 0x94D049BB133111EB
    return z ^ (z >> 31)
}

@inline(__always)
public func rotl64(_ x: UInt64, _ k: Int) -> UInt64 {
    (x << k) | (x >> (64 - k))
}

public struct KeyedPRNG: Sendable, Equatable {
    public var s0: UInt64
    public var s1: UInt64
    public var s2: UInt64
    public var s3: UInt64

    public init(key: PRNGKey) {
        var acc = key.seed ^ 0x243F6A8885A308D3
        acc = splitmix64Next(&acc) ^ key.suiteHash
        acc = splitmix64Next(&acc) ^ key.experimentHash
        acc = splitmix64Next(&acc) ^ key.trialIndex

        var a = splitmix64Next(&acc)
        let b = splitmix64Next(&acc)
        let c = splitmix64Next(&acc)
        let d = splitmix64Next(&acc)
        if (a | b | c | d) == 0 {
            a = 1
        }
        self.s0 = a
        self.s1 = b
        self.s2 = c
        self.s3 = d
    }

    public init(suite: String, experiment: String, trialIndex: UInt64, seed: UInt64) {
        self.init(key: PRNGKey(suite: suite, experiment: experiment, trialIndex: trialIndex, seed: seed))
    }

    @inline(__always)
    public mutating func nextUInt64() -> UInt64 {
        let result = rotl64(s1 &* 5, 7) &* 9
        let t = s1 << 17
        s2 ^= s0
        s3 ^= s1
        s1 ^= s2
        s0 ^= s3
        s2 ^= t
        s3 = rotl64(s3, 45)
        return result
    }

    /// Uniform in [0, 1) with exact 53-bit IEEE-754 mantissa resolution.
    @inline(__always)
    public mutating func nextUnitDouble() -> Double {
        let inv2Pow53 = 1.0 / 9007199254740992.0
        return Double(nextUInt64() >> 11) * inv2Pow53
    }

    /// Unbiased bounded integer in [0, bound) via Lemire rejection sampling.
    @inline(__always)
    public mutating func nextBounded(_ bound: UInt64) -> UInt64 {
        if bound <= 1 { return 0 }
        let threshold = (~bound &+ 1) % bound
        while true {
            let r = nextUInt64()
            if r >= threshold { return r % bound }
        }
    }

    /// Standard normal N(0, 1) via Box-Muller using open interval (0, 1].
    public mutating func nextNormalDouble() -> Double {
        let twoPi = 6.283185307179586476925286766559
        var u1 = nextUnitDouble()
        if u1 <= 0.0 {
            u1 = 0.5 / 9007199254740992.0
        }
        let u2 = nextUnitDouble()
        return sqrt(-2.0 * log(u1)) * cos(twoPi * u2)
    }
}
