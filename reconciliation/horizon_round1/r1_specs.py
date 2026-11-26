# -*- coding: utf-8 -*-
"""Run specs the author needs to supply before simulation figures can be re-run."""
SPECS = {
"wp030_shape_propulsion": """
**SPEC-030 — coupled 4-body triad and Landis tether runs (§3, Fig. 2, Fig. 4)**

| Field | Needed |
| :--- | :--- |
| Units / constants | μ (or G, M_p), triad mass M and per-body m, L_max, L_min (Landis arm) |
| Initial state | a0, e0 = 0.2, true anomaly at t = 0, initial shape (α or (Θ, Φ, θ0)), initial spin |
| Control law | the switching function α(t) or q(t): trigger (true anomaly / radius / energy), gain k, q_max, slew-rate limit |
| Integrator | method, fixed step or tolerance, steps per orbit, number of orbits (5 stated) |
| Diagnostics | definition of a 'tumble' (angle threshold, frame), ΔE definition (osculating vs total), the Eq. 5 residual normalisation |
| Arm A (Landis) | retraction profile, whether arm inertia is included, spin-up metric |
| Seeds | RNG seed and stream for the N = 1,600 trials (G4N uses SplitMix64; state the [E] generator) |
""",
"wp031_3d_j2_hil": """
**SPEC-031 — 5-orbit J2 diagnostic (§2, Fig. 2) and HIL slack test (§4)**

| Field | Needed |
| :--- | :--- |
| Units | μ, R_E (6,378.137 km assumed), J2, tether L (nondimensional) |
| Initial state | r0, v0 vector, inclination i0, RAAN, argument of perigee, initial triad attitude and spin |
| Baseline | whether a point-mass (L = 0) run under the same J2 field was subtracted |
| Integrator | method, step/tolerance, orbit count |
| HIL | controller gains, sensor noise, slack threshold, tick length, 2,000-tick seed |
""",
"wp032_bennu_3body": """
**SPEC-032 — Bennu ladder, 48-DOF FEM, FDIR and figure-8 / Lagrange kick runs**

| Field | Needed |
| :--- | :--- |
| Bennu model | μ_B, R_eq, C20/J2, C22 values and reference radius |
| FEM | node masses, EA, damping, reel slew rate, jam onset time, time step |
| FDIR | detection threshold, slack definition, count window |
| Kick test | kick size, direction (position/velocity, which body), integrator, step, horizon, growth metric (5,570× vs 11,618× depends on these) |
| Figure-8 | initial conditions source (Chenciner–Montgomery / Simó digits), Yoshida-4 step |
""",
"wp033_halo_tag_guidance": """
**SPEC-033 — W^u branch, station-keeping and TAG Monte Carlo**

| Field | Needed |
| :--- | :--- |
| W^u | kick size (1e-4 assumed) and sign convention for the unstable eigenvector (the +v_u branch impacts the Moon at about 17.4 d; the −v_u branch does not) |
| Station-keeping | noise model and seed, burn cadence, deadband, control law, horizon (3,051× vs 3,442× depends on these) |
| TAG | contact area A_h (needed to check C_D = 1.60), regolith density used, Monte Carlo seed and N |
| Didymos L2 | μ, separation, triad L used for L_y* = 40.44 m |
""",
"wp034_null_cone_gravity": "",
"wp035_tuft_hagedorn_repair": "",
}
