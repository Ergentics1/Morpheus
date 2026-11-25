/// Theorem 7.4 & Corollary 7.5: Exact Z/12Z voltage cover X -> Theta and
/// exact Z[zeta_12][u] Artin-Ihara character factorization of zeta_X(u)^{-1}.
use crate::cyclotomic::Z12;

fn apply_plr(v: usize, mv: usize) -> usize {
    let r = v % 12;
    if v < 12 {
        match mv {
            0 => 12 + r,
            1 => 12 + (r + 4) % 12,
            _ => 12 + (r + 9) % 12,
        }
    } else {
        match mv {
            0 => r,
            1 => (r + 8) % 12,
            _ => (r + 3) % 12,
        }
    }
}

fn poly_mul_z12(a: &[Z12], b: &[Z12]) -> Vec<Z12> {
    let mut out = vec![Z12::ZERO; a.len() + b.len() - 1];
    for (i, &ai) in a.iter().enumerate() {
        for (j, &bj) in b.iter().enumerate() {
            out[i + j] = out[i + j].add(ai.mul(bj));
        }
    }
    out
}

fn poly_mul_i128(a: &[i128], b: &[i128]) -> Vec<i128> {
    let mut out = vec![0i128; a.len() + b.len() - 1];
    for (i, &ai) in a.iter().enumerate() {
        for (j, &bj) in b.iter().enumerate() {
            out[i + j] += ai * bj;
        }
    }
    out
}

#[derive(Debug, Clone)]
pub struct TowerArtinReport {
    pub edges_voltage_verified: usize,
    pub pl_cycle_len: usize,
    pub pr_cycle_len: usize,
    pub lr_cycle_len: usize,
    pub artin_order_blocks_exact: bool,
    pub full_weil_product_exact: bool,
    pub passed: bool,
}

pub fn verify_tower_and_artin_ihara() -> TowerArtinReport {
    // Theorem 7.4(b): level(Maj(r)) = 5r mod 12, level(Min(r)) = 5(r - 4) mod 12.
    // Voltages from Major -> Minor: P: +4, L: +0, R: +1 (mod 12).
    let level = |v: usize| -> i32 {
        let r = (v % 12) as i32;
        if v < 12 {
            (5 * r).rem_euclid(12)
        } else {
            (5 * (r - 4)).rem_euclid(12)
        }
    };
    let expected_volt = [4i32, 0, 1]; // P, L, R
    let mut verified_edges = 0usize;
    for u in 0..12 {
        for mv in 0..3 {
            let v = apply_plr(u, mv);
            let dv = (level(v) - level(u)).rem_euclid(12);
            if dv == expected_volt[mv] {
                verified_edges += 1;
            }
        }
    }

    // Theorem 7.4(c): loop lifts on X.
    let loop_len = |m1: usize, m2: usize| -> usize {
        let mut cur = 0usize;
        let mut steps = 0usize;
        loop {
            cur = apply_plr(cur, m1);
            cur = apply_plr(cur, m2);
            steps += 2;
            if cur == 0 || steps > 48 {
                break;
            }
        }
        steps
    };
    let pl_len = loop_len(0, 1); // 6
    let pr_len = loop_len(0, 2); // 8
    let lr_len = loop_len(1, 2); // 24

    // Corollary 7.5: exact character factor L_Theta(u, chi_k)^{-1} / (1-u^2) = (1 + 2u^2)^2 - |phi_k|^2 u^2
    // with phi_k = 1 + zeta^k + zeta^{4k} in exact Z[zeta_12][u].
    let char_poly = |k: i32| -> Vec<Z12> {
        let phi_k = Z12::ONE.add(Z12::zeta_pow(k)).add(Z12::zeta_pow(4 * k));
        let nsq = phi_k.norm_sq();
        // (1 + 2u^2)^2 - |phi_k|^2 u^2 = 1 + (4 - |phi_k|^2) u^2 + 4 u^4.
        vec![
            Z12::ONE,
            Z12::ZERO,
            Z12::from_int(4).sub(nsq),
            Z12::ZERO,
            Z12::from_int(4),
        ]
    };

    let to_z12_poly = |coeffs: &[i128]| -> Vec<Z12> {
        coeffs.iter().map(|&c| Z12::from_int(c)).collect()
    };

    let prod_ks = |ks: &[i32]| -> Vec<Z12> {
        let mut acc = vec![Z12::ONE];
        for &k in ks {
            acc = poly_mul_z12(&acc, &char_poly(k));
        }
        acc
    };

    // Exact integer polynomials for each order d in {1, 2, 3, 4, 6, 12}:
    let l1 = [1i128, -1, 2];
    let l1p = [1i128, 1, 2];
    let l2 = [1i128, 0, -1, 0, 4];
    let l2p = [1i128, 0, 1, 0, 4];
    let l4 = [1i128, 0, 4, 0, 9, 0, 16, 0, 16];

    let exp_d1 = poly_mul_i128(&[1, 0, -1], &[1, 0, -4]); // (1-u^2)(1-4u^2)
    let exp_d2 = poly_mul_i128(&l1, &l1p);
    let exp_d3 = poly_mul_i128(&l2p, &l2p);
    let exp_d4 = poly_mul_i128(&l2, &l2);
    let exp_d6 = poly_mul_i128(&exp_d2, &exp_d2);
    let exp_d12 = poly_mul_i128(&l4, &l4);

    let ok_d1 = prod_ks(&[0]) == to_z12_poly(&exp_d1);
    let ok_d2 = prod_ks(&[6]) == to_z12_poly(&exp_d2);
    let ok_d3 = prod_ks(&[4, 8]) == to_z12_poly(&exp_d3);
    let ok_d4 = prod_ks(&[3, 9]) == to_z12_poly(&exp_d4);
    let ok_d6 = prod_ks(&[2, 10]) == to_z12_poly(&exp_d6);
    let ok_d12 = prod_ks(&[1, 5, 7, 11]) == to_z12_poly(&exp_d12);
    let blocks_ok = ok_d1 && ok_d2 && ok_d3 && ok_d4 && ok_d6 && ok_d12;

    // Multiply all 12 character factors and confirm exact equality with (1-u^2)(1-4u^2) * P_44(u).
    let full_artin = prod_ks(&[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]);
    let mut expected_full = exp_d1.clone();
    expected_full = poly_mul_i128(&expected_full, &exp_d2);
    expected_full = poly_mul_i128(&expected_full, &exp_d3);
    expected_full = poly_mul_i128(&expected_full, &exp_d4);
    expected_full = poly_mul_i128(&expected_full, &exp_d6);
    expected_full = poly_mul_i128(&expected_full, &exp_d12);
    let full_ok = full_artin == to_z12_poly(&expected_full);

    let passed = verified_edges == 36
        && pl_len == 6
        && pr_len == 8
        && lr_len == 24
        && blocks_ok
        && full_ok;

    TowerArtinReport {
        edges_voltage_verified: verified_edges,
        pl_cycle_len: pl_len,
        pr_cycle_len: pr_len,
        lr_cycle_len: lr_len,
        artin_order_blocks_exact: blocks_ok,
        full_weil_product_exact: full_ok,
        passed,
    }
}
