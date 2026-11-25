# Prime Cadences: math audit

- PASS 24 triads, every one has exactly 3 P/L/R neighbours
- PASS graph connected and bipartite (major/minor alternate)
- PASS adjacency spectrum = ±|f_k| of {0,4,7} (60 digits)
- PASS |f1|^2=2-√3, |f2|=|f6|=1, |f3|^2=5, |f4|^2=3, |f5|^2=2+√3
- PASS largest non-trivial eigenvalue = √5 = 2.23607 ≤ 2√2 (Ramanujan / graph RH)
- PASS zero angles = 37.761°, 46.920°, 52.239°, 69.295°, 79.455°
- PASS rounded as narrated: 38, 47, 52, 69, 79 degrees
- PASS θ3 + θ4 = 90° exactly (|f3|²+|f4|² = 8)
- PASS Hashimoto matrix is 72×72 (36 edges, both directions)
- PASS no closed non-backtracking loops of odd length; none shorter than 6
- PASS π(6..16) = 32, 78, 240, 576, 2400, 8196
- PASS Ihara–Bass: det(I−uB) = (1−u²)^12·det(I−uA+2u²I) at u=0.137
- PASS explicit formula N_m = 2^(m+1)+26+2^(m/2+2)Σcos(mθ_k) matches exact traces, m=2..40 even
- PASS π(30) = 71,585,776; 2^31/30 ≈ 71,582,788
- PASS relative gap at m=30 is 0.0042 %
- PASS 12-EDO normalised error stays inside the RH band |·| ≤ 48 for m = 6..160
- PASS length 6: 24 common-tone hexagons + 8 hexatonic = 32 primes
- PASS length 8: 6 of the 78 primes are octatonic PR cycles
- PASS winding census: length 8 has no contractible (0,0) prime; length 6 has 24
- PASS addresses: hexatonic (0,±1), octatonic (±1,0), PRLRLRLR (1,1)
- PASS 124 directed Hamiltonian cycles (Albini–Antonini 2009)
- PASS 53-EDO major triad: max |λ| = 2.8565 > 2√2 (fails graph RH)
- PASS 53-EDO error exponent log2(μ) = 0.703 → narrated 0.70
- PASS 31-EDO major triad passes, barely: 2.8246 ≤ 2.8284
- PASS 53-EDO major third 17 steps = 384.9¢ vs pure 386.3¢
- PASS 53-EDO normalised error at m=160 exceeds 10^10 (grows), 12-EDO stays below 48
- PASS the constant 26 = 2 (poles ±1 of λ=±3) + 24 (Bass factor (1−u²)^12)
- PASS all six finale phrases are closed, non-backtracking, primitive loops through distinct triads
- PASS double hexagon (length 10) is contractible: 10-step (0,0) loops exist
- PASS finale addresses by lattice lift: hexagon (0,0), hexatonic (0,±1), octatonic ±(1,0), winding ±(1,1), double hexagon (0,0)
- PASS Tonnetz-bell partials = θ_k/θ_min = 1, 1.243, 1.383, 1.835, 2.104

**31/31 passed**
