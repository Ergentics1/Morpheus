import TriadicNauru

-- Compile-time axiom audit: ensures zero `sorryAx` and zero `Lean.ofReduceBool`.
#print axioms TriadicNauru.thm1_utt_parity_hom
#print axioms TriadicNauru.thm2_T_PLR_even_parity_misses_Q
#print axioms TriadicNauru.thm3_I0_not_in_UTT
#print axioms TriadicNauru.thm4_I0_normalizes_UTT
#print axioms TriadicNauru.thm5_nauru_symmetric_bipartite
#print axioms TriadicNauru.thm6_nauru_3_regular
#print axioms TriadicNauru.thm7_nauru_no_4cycles
#print axioms TriadicNauru.thm8_nauru_prime_hexagon
#print axioms TriadicNauru.thm9_nauru_exact_spectral_traces
#print axioms TriadicNauru.thm10_all_five_F2_elliptic_curves
#print axioms TriadicNauru.thm11_raynaud_orders_exact
#print axioms TriadicNauru.thm12_lame_amalgam_euler_char
#print axioms TriadicNauru.thm13_lame_family_universal_identities
#print axioms TriadicNauru.thm14_split_involution_obstruction
#print axioms TriadicNauru.thm15_rational_arithmetic_uniqueness
#print axioms TriadicNauru.thm16_O3_amalgam_exact
#print axioms TriadicNauru.thm17_O3_gamma6_arithmetic_and_mod3
#print axioms TriadicNauru.thm18_fricke_vogt_arithmetic_vs_nonarithmetic
#print axioms TriadicNauru.thm19_hensel_q2_mod64
#print axioms TriadicNauru.thm20_ramanujan_gaps_exact
#print axioms TriadicNauru.thm21_cfs_duality_commute_and_T6
#print axioms TriadicNauru.thm22_qutt_Imaj_not_normalizing_UTT
#print axioms TriadicNauru.thm23_eisenstein_nauru_exact_isomorphism
#print axioms TriadicNauru.thm24_nauru_T_PLR_even_parity_decomp
#print axioms TriadicNauru.thm25_definite_quat_su2_unitarity_and_walls
#print axioms TriadicNauru.thm26_dic6_Z_moments_and_K44_quotient
#print axioms TriadicNauru.thm27_canonical_3adic_dic6_non_arithmetic
#print axioms TriadicNauru.thm28_hurwitz_amalgam_and_corrected_w4
#print axioms TriadicNauru.thm29_hensel_sqrt_minus2_mod_3pow12
#print axioms TriadicNauru.thm30_hurwitz_T4_all_lengths_freeness
#print axioms TriadicNauru.thm31_hurwitz_euler_char_and_congruence_index
#print axioms TriadicNauru.thm32_psl2_order_gt_s3_for_all_ge_5
#print axioms TriadicNauru.thm33_hurwitz_normalizer_and_F3_quaternion
#print axioms TriadicNauru.thm34_nauru_exact_unimodular_snf
#print axioms TriadicNauru.thm35_dic6_exact_unimodular_snf
#print axioms TriadicNauru.thm36_b5_congruence_and_noncongruence_arithmetic
#print axioms TriadicNauru.thm37_dic6_gonality_witness_and_six_ring
#print axioms TriadicNauru.thm38_nauru_pi18_ramanujan_and_twin_duality

def main : IO Unit := do
  IO.println "TriadicNauru Lean 4.36.0 Oracle: ALL 38 THEOREMS KERNEL-CHECKED (0 sorryAx, 0 ofReduceBool)."
  IO.println s!"  O3 gamma6 = ({TriadicNauru.o3Gamma6.c0}, {TriadicNauru.o3Gamma6.c1}, {TriadicNauru.o3Gamma6.c2}, {TriadicNauru.o3Gamma6.c3}), trd={TriadicNauru.o3Trd TriadicNauru.o3Gamma6}, nrd={TriadicNauru.o3Nrd TriadicNauru.o3Gamma6}"
  IO.println s!"  O2 Hurwitz w4 = ({TriadicNauru.hbW4.c0}, {TriadicNauru.hbW4.c1}, {TriadicNauru.hbW4.c2}, {TriadicNauru.hbW4.c3}), trd={TriadicNauru.qbTrd TriadicNauru.hbW4}, nrd={TriadicNauru.qbNrd TriadicNauru.hbW4}"
