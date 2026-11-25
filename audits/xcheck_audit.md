# Audit: cross-check of the [X] results (Ergentics' program)

**32/32 PASS**

Script: `code/xcheck/audit_xcheck.py`. Everything is recomputed from scratch; no stored JSON is read. It re-checks the held-note claims (Theorem A/B, Corollary B.1, NEG-M11 in the [X] packet; Thm 4.4 and Cor 4.5 here), the higher cumulants (Thm 6.2, Prop 6.3), the exact m = 40 benchmarks, the decoder count (NEG-E8) and the Edgeworth calibration (Remark 6.4).

| # | check | result | detail |
|---|---|---|---|
| 1 | Thm A: common link edges of two notes <= 2 (all chord classes, N<=30) | PASS |  |
| 2 | Thm B: every one-voice collision lies in the family 8\|N, {0,N/8,N/2}, N/4 in S (all S, N<=24) | PASS | 273 |
| 3 | Thm B: with maximal step sets, collisions at exactly N=8,16,...,72 (N<=72) | PASS | 9 |
| 4 | Cor B.1: no collision for halving-closed S | PASS |  |
| 5 | NEG-M11: N=8, S={2}, {0,1,4}: both 4-cycles valid and non-backtracking | PASS |  |
| 6 | NEG-M11: same cyclic tune (3,5,7,1) | PASS |  |
| 7 | Thm C: kappa4/kappa2^2 = -17/2 per step along W=-u | PASS |  |
| 8 | Thm C: kappa4/kappa2^2 = -17/2 per step along v | PASS |  |
| 9 | Thm C: kappa4/kappa2^2 = -17/2 per step along 4u+3v | PASS |  |
| 10 | Thm C: kappa4/kappa2^2 = -17/2 per step along u+v | PASS |  |
| 11 | Thm C: kappa4/kappa2^2 = -17/2 per step along 2u+v | PASS |  |
| 12 | Thm C: kappa4/kappa2^2 = -17/2 per step along u+2v | PASS |  |
| 13 | Thm C: kappa6/kappa2^3 = (1470+cos 6a)/4 along W=-u | PASS |  |
| 14 | Thm C: kappa6/kappa2^3 = (1470+cos 6a)/4 along v | PASS |  |
| 15 | Thm C: kappa6/kappa2^3 = (1470+cos 6a)/4 along 4u+3v | PASS |  |
| 16 | Thm C: kappa6/kappa2^3 = (1470+cos 6a)/4 along u+v | PASS |  |
| 17 | Thm C: kappa6/kappa2^3 = (1470+cos 6a)/4 along 2u+v | PASS |  |
| 18 | Thm C: kappa6/kappa2^3 = (1470+cos 6a)/4 along u+2v | PASS |  |
| 19 | Thm C: W rates 1/24, -17/1152, 1469/55296 | PASS |  |
| 20 | odd cumulants vanish on all six axes | PASS |  |
| 21 | Prop (all cumulants of W): closed form reproduces the series; kappa8/m = -887099/7962624 | PASS | [1/24, -17/1152, 1469/55296, -887099/7962624] |
| 22 | m=40 W=-u: total primes = 54,975,717,792 = pi(40) from tr B^m | PASS |  |
| 23 | m=40 W=-u: m*kappa_ex matches the [X] record | PASS | -8.495174375280602 |
| 24 | m=40 v: total primes = 54,975,717,792 = pi(40) from tr B^m | PASS |  |
| 25 | m=40 v: m*kappa_ex matches the [X] record | PASS | -8.48978326883313 |
| 26 | m=40 4u+3v: total primes = 54,975,717,792 = pi(40) from tr B^m | PASS |  |
| 27 | m=40 4u+3v: m*kappa_ex matches the [X] record | PASS | -8.490888952147145 |
| 28 | NEG-E8: rooted primes of length <= 16 total 174,864 (131,136 of length 16) | PASS | 174864 |
| 29 | C-2: TV and JSD reproduce the [X] record | PASS |  |
| 30 | C-2': TV and JSD reproduce the [X] record | PASS |  |
| 31 | C-2'': TV and JSD reproduce the [X] record | PASS |  |
| 32 | Edgeworth ladder decreases: TV(C-2) > TV(C-2') > TV(C-2'') | PASS |  |
