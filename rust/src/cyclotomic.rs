/// Exact arithmetic in the 12th cyclotomic ring Z[zeta_12] = Z[x] / (x^4 - x^2 + 1)
/// verifying Theorem 3.4 (Gaussian/Eisenstein primes, fundamental unit, minimal poly,
/// Galois action, M_11 automorphism, and M_7 isomorphism onto the [0,1,4] flip graph).
use std::collections::BTreeSet;

/// Element c0 + c1*z + c2*z^2 + c3*z^3 in Z[zeta_12], where z^4 = z^2 - 1.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Z12(pub [i128; 4]);

impl Z12 {
    pub const ZERO: Self = Self([0, 0, 0, 0]);
    pub const ONE: Self = Self([1, 0, 0, 0]);

    pub fn from_int(n: i128) -> Self {
        Self([n, 0, 0, 0])
    }

    pub fn add(self, o: Self) -> Self {
        Self([
            self.0[0] + o.0[0],
            self.0[1] + o.0[1],
            self.0[2] + o.0[2],
            self.0[3] + o.0[3],
        ])
    }

    pub fn sub(self, o: Self) -> Self {
        Self([
            self.0[0] - o.0[0],
            self.0[1] - o.0[1],
            self.0[2] - o.0[2],
            self.0[3] - o.0[3],
        ])
    }

    pub fn scale(self, k: i128) -> Self {
        Self([self.0[0] * k, self.0[1] * k, self.0[2] * k, self.0[3] * k])
    }

    pub fn mul(self, o: Self) -> Self {
        let mut p = [0i128; 7];
        for i in 0..4 {
            for j in 0..4 {
                p[i + j] += self.0[i] * o.0[j];
            }
        }
        // Reduce mod z^4 - z^2 + 1 from degree 6 down to 4.
        for deg in (4..7).rev() {
            let c = p[deg];
            p[deg] = 0;
            p[deg - 2] += c;
            p[deg - 4] -= c;
        }
        Self([p[0], p[1], p[2], p[3]])
    }

    /// Exact power zeta_12^k for any integer k (mod 12).
    pub fn zeta_pow(k: i32) -> Self {
        let r = k.rem_euclid(12);
        match r {
            0 => Self([1, 0, 0, 0]),
            1 => Self([0, 1, 0, 0]),
            2 => Self([0, 0, 1, 0]),
            3 => Self([0, 0, 0, 1]),
            4 => Self([-1, 0, 1, 0]),
            5 => Self([0, -1, 0, 1]),
            6 => Self([-1, 0, 0, 0]),
            7 => Self([0, -1, 0, 0]),
            8 => Self([0, 0, -1, 0]),
            9 => Self([0, 0, 0, -1]),
            10 => Self([1, 0, -1, 0]),
            11 => Self([0, 1, 0, -1]),
            _ => unreachable!(),
        }
    }

    /// Galois automorphism sigma_a(zeta) = zeta^a for a in {1, 5, 7, 11}.
    pub fn galois(self, a: i32) -> Self {
        let mut out = Self::ZERO;
        for i in 0..4 {
            let zp = Self::zeta_pow(a * (i as i32));
            out = out.add(zp.scale(self.0[i]));
        }
        out
    }

    /// Complex conjugation = sigma_11.
    pub fn conj(self) -> Self {
        self.galois(11)
    }

    /// Exact squared modulus |x|^2 = x * conj(x) in Z[sqrt(3)] <= Z[zeta_12].
    pub fn norm_sq(self) -> Self {
        self.mul(self.conj())
    }
}

/// Triad Fourier coefficient f_k = 1 + zeta^{4k} + zeta^{7k} in exact Z[zeta_12].
pub fn fourier_fk(k: i32) -> Z12 {
    Z12::ONE
        .add(Z12::zeta_pow(4 * k))
        .add(Z12::zeta_pow(7 * k))
}

#[derive(Debug, Clone)]
pub struct Theorem34Report {
    pub f3_is_2_minus_i: bool,
    pub f9_is_2_plus_i: bool,
    pub f4_sq_is_minus_3: bool,
    pub f1_minpoly_zero: bool,
    pub f1_unit_norm_one: bool,
    pub f5_norm_sq_is_2_plus_sqrt3: bool,
    pub f1_norm_sq_is_2_minus_sqrt3: bool,
    pub galois_action_exact: bool,
    pub m11_is_automorphism: bool,
    pub m7_isomorphism_014_edges: usize,
    pub passed: bool,
}

pub fn verify_theorem_3_4() -> Theorem34Report {
    let i_unit = Z12::zeta_pow(3);
    let omega = Z12::zeta_pow(4);
    let sqrt3 = Z12::zeta_pow(1).add(Z12::zeta_pow(11)); // zeta + zeta^-1 = sqrt(3)

    let f1 = fourier_fk(1);
    let f3 = fourier_fk(3);
    let f4 = fourier_fk(4);
    let f5 = fourier_fk(5);
    let f7 = fourier_fk(7);
    let f8 = fourier_fk(8);
    let f9 = fourier_fk(9);
    let f11 = fourier_fk(11);

    let f3_ok = f3 == Z12::from_int(2).sub(i_unit) && f3.norm_sq() == Z12::from_int(5);
    let f9_ok = f9 == Z12::from_int(2).add(i_unit) && f9.norm_sq() == Z12::from_int(5);
    let f4_ok = f4 == Z12::ONE.add(omega.scale(2))
        && f4.mul(f4) == Z12::from_int(-3)
        && f8 == f4.scale(-1)
        && f4.norm_sq() == Z12::from_int(3);

    // Minimal polynomial of f_1: x^4 - 2 x^3 + 2 x^2 + 2 x + 1 == 0.
    let f1_2 = f1.mul(f1);
    let f1_3 = f1_2.mul(f1);
    let f1_4 = f1_3.mul(f1);
    let mp = f1_4
        .sub(f1_3.scale(2))
        .add(f1_2.scale(2))
        .add(f1.scale(2))
        .add(Z12::ONE);
    let minpoly_ok = mp == Z12::ZERO;

    // Exact field norm N_{Q(z12)/Q}(f_1) = f_1 * f_5 * f_7 * f_11 == 1.
    let field_norm = f1.mul(f5).mul(f7).mul(f11);
    let unit_ok = field_norm == Z12::ONE;

    let eps = Z12::from_int(2).add(sqrt3);
    let eps_inv = Z12::from_int(2).sub(sqrt3);
    let f5_sq_ok = f5.norm_sq() == eps && f7.norm_sq() == eps && eps.mul(eps_inv) == Z12::ONE;
    let f1_sq_ok = f1.norm_sq() == eps_inv && f11.norm_sq() == eps_inv;

    // Galois action sigma_a(f_k) == f_{a*k mod 12} for all a in (Z/12Z)* and all k in Z/12Z.
    let mut galois_ok = true;
    for a in [1, 5, 7, 11] {
        for k in 0..12 {
            if fourier_fk(k).galois(a) != fourier_fk((a * k) % 12) {
                galois_ok = false;
            }
        }
    }

    // Build 24 consonant triads and 36 single-note flip edges of X.
    let mut triads: Vec<[u8; 3]> = Vec::with_capacity(24);
    for r in 0..12u8 {
        let mut m = [r, (r + 4) % 12, (r + 7) % 12];
        m.sort();
        triads.push(m);
    }
    for r in 0..12u8 {
        let mut m = [r, (r + 3) % 12, (r + 7) % 12];
        m.sort();
        triads.push(m);
    }
    let triad_set: BTreeSet<[u8; 3]> = triads.iter().copied().collect();

    let mut x_edges: BTreeSet<([u8; 3], [u8; 3])> = BTreeSet::new();
    for &c in &triads {
        for &d in &triads {
            if c < d {
                let common = c.iter().filter(|x| d.contains(x)).count();
                if common == 2 {
                    x_edges.insert((c, d));
                }
            }
        }
    }

    // M_11 (pitch -> -pitch mod 12) preserves consonant triads and all 36 edges (flipping Maj <-> Min).
    let apply_mult = |c: [u8; 3], mult: u8| -> [u8; 3] {
        let mut out = [(c[0] * mult) % 12, (c[1] * mult) % 12, (c[2] * mult) % 12];
        out.sort();
        out
    };
    let mut m11_ok = x_edges.len() == 36;
    for &(c, d) in &x_edges {
        let mc = apply_mult(c, 11);
        let md = apply_mult(d, 11);
        let pair = if mc < md { (mc, md) } else { (md, mc) };
        if !triad_set.contains(&mc) || !triad_set.contains(&md) || !x_edges.contains(&pair) {
            m11_ok = false;
        }
    }

    // M_7 maps the 24 consonant triads bijectively onto the 24 T/I-forms of [0,1,4]
    // and maps all 36 PLR edges bijectively onto single-note parsimonious moves (step in {1,2} or 2 shared notes).
    let mut orbit_014: BTreeSet<[u8; 3]> = BTreeSet::new();
    for t in 0..12u8 {
        let mut a = [t, (t + 1) % 12, (t + 4) % 12];
        a.sort();
        orbit_014.insert(a);
        let mut b = [(12 - t) % 12, (12 - (t + 1) % 12) % 12, (12 - (t + 4) % 12) % 12];
        b.sort();
        orbit_014.insert(b);
    }
    let img_m7: BTreeSet<[u8; 3]> = triads.iter().map(|&c| apply_mult(c, 7)).collect();
    let mut edges_014: BTreeSet<([u8; 3], [u8; 3])> = BTreeSet::new();
    for &c in &orbit_014 {
        for &d in &orbit_014 {
            if c < d {
                let common = c.iter().filter(|x| d.contains(x)).count();
                if common == 2 {
                    // Check moving note step in {1, 2} mod 12? Actually M_7 scales step {1,2} -> {7,2}={5,2} mod 12,
                    // while all 2-shared-note flips inside [0,1,4] form a 3-regular graph of 36 edges!
                    edges_014.insert((c, d));
                }
            }
        }
    }
    let mut m7_edges_matched = 0usize;
    if img_m7 == orbit_014 && orbit_014.len() == 24 && edges_014.len() == 36 {
        for &(c, d) in &x_edges {
            let mc = apply_mult(c, 7);
            let md = apply_mult(d, 7);
            let pair = if mc < md { (mc, md) } else { (md, mc) };
            if edges_014.contains(&pair) {
                m7_edges_matched += 1;
            }
        }
    }

    let passed = f3_ok
        && f9_ok
        && f4_ok
        && minpoly_ok
        && unit_ok
        && f5_sq_ok
        && f1_sq_ok
        && galois_ok
        && m11_ok
        && m7_edges_matched == 36;

    Theorem34Report {
        f3_is_2_minus_i: f3_ok,
        f9_is_2_plus_i: f9_ok,
        f4_sq_is_minus_3: f4_ok,
        f1_minpoly_zero: minpoly_ok,
        f1_unit_norm_one: unit_ok,
        f5_norm_sq_is_2_plus_sqrt3: f5_sq_ok,
        f1_norm_sq_is_2_minus_sqrt3: f1_sq_ok,
        galois_action_exact: galois_ok,
        m11_is_automorphism: m11_ok,
        m7_isomorphism_014_edges: m7_edges_matched,
        passed,
    }
}
