/// Domain-separated keyed PRNG (FNV-1a + SplitMix64 + Xoshiro256**).
/// Bit-for-bit identical to Lane 1 (C++20) and Lane 2 (Pure Swift 6.4).

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct PrngKey {
    pub suite_hash: u64,
    pub experiment_hash: u64,
    pub trial_index: u64,
    pub seed: u64,
}

impl PrngKey {
    pub fn new(suite: &str, experiment: &str, trial_index: u64, seed: u64) -> Self {
        Self {
            suite_hash: fnv1a_64(suite.as_bytes()),
            experiment_hash: fnv1a_64(experiment.as_bytes()),
            trial_index,
            seed,
        }
    }
}

pub fn fnv1a_64(bytes: &[u8]) -> u64 {
    let mut h: u64 = 14_695_981_039_346_656_037;
    for &b in bytes {
        h ^= b as u64;
        h = h.wrapping_mul(1_099_511_628_211);
    }
    h
}

pub fn splitmix64_next(state: &mut u64) -> u64 {
    *state = state.wrapping_add(0x9E37_79B9_7F4A_7C15);
    let mut z = *state;
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^ (z >> 31)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct KeyedPrng {
    s0: u64,
    s1: u64,
    s2: u64,
    s3: u64,
}

impl KeyedPrng {
    pub fn from_key(key: PrngKey) -> Self {
        let mut acc = key.seed ^ 0x243F_6A88_85A3_08D3;
        acc = splitmix64_next(&mut acc) ^ key.suite_hash;
        acc = splitmix64_next(&mut acc) ^ key.experiment_hash;
        acc = splitmix64_next(&mut acc) ^ key.trial_index;

        let mut s0 = splitmix64_next(&mut acc);
        let s1 = splitmix64_next(&mut acc);
        let s2 = splitmix64_next(&mut acc);
        let s3 = splitmix64_next(&mut acc);
        if (s0 | s1 | s2 | s3) == 0 {
            s0 = 1;
        }
        Self { s0, s1, s2, s3 }
    }

    #[inline]
    pub fn next_u64(&mut self) -> u64 {
        let result = self.s1.wrapping_mul(5).rotate_left(7).wrapping_mul(9);
        let t = self.s1 << 17;
        self.s2 ^= self.s0;
        self.s3 ^= self.s1;
        self.s1 ^= self.s2;
        self.s0 ^= self.s3;
        self.s2 ^= t;
        self.s3 = self.s3.rotate_left(45);
        result
    }

    #[inline]
    pub fn next_unit_f64(&mut self) -> f64 {
        const INV_2_53: f64 = 1.0 / 9_007_199_254_740_992.0;
        ((self.next_u64() >> 11) as f64) * INV_2_53
    }

    #[inline]
    pub fn next_bounded(&mut self, bound: u64) -> u64 {
        if bound <= 1 {
            return 0;
        }
        let threshold = bound.wrapping_neg() % bound;
        loop {
            let r = self.next_u64();
            if r >= threshold {
                return r % bound;
            }
        }
    }
}
