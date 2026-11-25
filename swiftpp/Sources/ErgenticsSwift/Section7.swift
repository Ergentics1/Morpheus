import Foundation

public struct SandpileSNFReport: Sendable, Equatable {
    public let nontrivialCount: Int32
    public let invariantFactors: [Int64]
    public let groupOrder: Int64
    public let divisibilityChainOK: Bool
    public let passed: Bool
}

public struct GonalityAutReport: Sendable, Equatable {
    public let autOrder: Int32
    public let involutionCount: Int32
    public let treeQuotientCount: Int32
    public let minQuotientBetti: Int32
    public let divisorsDegLe5Tested: Int64
    public let rank1DegLe5Found: Int64
    public let witnessDeg6Rank1OK: Bool
    public let computedGonality: Int32
    public let passed: Bool
}

public struct F2CurvesReport: Sendable, Equatable {
    public let p44PointCounts: [Int64]    // N_1..N_6
    public let cofactorA0Deg4Places: Int64
    public let curveACounts: [Int64]      // #A(F_{2^k}), k = 1..5
    public let curveBCounts: [Int64]      // #B(F_{2^k}), k = 1..5
    public let expectedACounts: [Int64]
    public let expectedBCounts: [Int64]
    public let weilFactorMaxResidual: Double
    public let passed: Bool
}

public struct Eisenstein12MapsReport: Sendable, Equatable {
    public let tonnetzMapCount: Int32
    public let minConductor: Int32
    public let maxConductor: Int32
    public let anyKernelIsIdeal: Bool
    public let passed: Bool
}

public struct SchottkyGroupReport: Sendable, Equatable {
    public let schreierCount: Int32
    public let schreierHyperbolic: Int32
    public let schreierInKernel: Int32
    public let btBallR7Words: Int32
    public let btBallR7Distinct: Int32
    public let gamma0Tr: Int64
    public let gamma0Det: Int64
    public let gamma0TauGt4: Bool
    public let passed: Bool
}

// MARK: - Theorem 7.7: Exact Bareiss + Iliopoulos-Bezout Modular SNF + F_p Nullity Guard

private func extGcd64(_ a: Int64, _ b: Int64) -> (g: Int64, s: Int64, t: Int64) {
    var oldR = a, r = b
    var oldS: Int64 = 1, s: Int64 = 0
    var oldT: Int64 = 0, t: Int64 = 1
    while r != 0 {
        let q = oldR / r
        (oldR, r) = (r, oldR - q * r)
        (oldS, s) = (s, oldS - q * s)
        (oldT, t) = (t, oldT - q * t)
    }
    return (oldR, oldS, oldT)
}

public func computeSandpileGroupSNF() -> SandpileSNFReport {
    let n = 23
    var lap = [Int128](repeating: 0, count: n * n)
    for v: Int32 in 0..<23 {
        lap[Int(v) * n + Int(v)] = 3
        for mv: Int32 in 0..<3 {
            let u = applyPLRMove(vertex: v, moveId: mv).targetVertex
            if u < 23 {
                lap[Int(v) * n + Int(u)] = -1
            }
        }
    }

    // 1. Exact Bareiss fraction-free determinant (intermediates bounded at 55 bits << 127).
    var B = lap
    var prevPiv: Int128 = 1
    for k in 0..<n {
        var pivRow = k
        while pivRow < n && B[pivRow * n + k] == 0 { pivRow += 1 }
        if pivRow == n {
            return SandpileSNFReport(nontrivialCount: 0, invariantFactors: [], groupOrder: 0, divisibilityChainOK: false, passed: false)
        }
        if pivRow != k {
            for j in 0..<n { B.swapAt(k * n + j, pivRow * n + j) }
        }
        let piv = B[k * n + k]
        if k + 1 < n {
            for i in (k + 1)..<n {
                for j in (k + 1)..<n {
                    let num = B[i * n + j] * piv - B[i * n + k] * B[k * n + j]
                    if num % prevPiv != 0 {
                        return SandpileSNFReport(nontrivialCount: 0, invariantFactors: [], groupOrder: 0, divisibilityChainOK: false, passed: false)
                    }
                    B[i * n + j] = num / prevPiv
                }
            }
        }
        prevPiv = piv
    }
    let rawDet = B[(n - 1) * n + (n - 1)]
    let delta128 = rawDet < 0 ? -rawDet : rawDet
    let delta = Int64(delta128)

    func modD(_ x: Int128) -> Int64 {
        var r = x % delta128
        if r < 0 { r += delta128 }
        return Int64(r)
    }

    // 2. Exact Iliopoulos-Bezout modular SNF mod Delta (avoids 283-bit intermediate expression swell).
    var M = lap.map { modD($0) }

    func swapRows(_ r1: Int, _ r2: Int) {
        if r1 == r2 { return }
        for j in 0..<n { M.swapAt(r1 * n + j, r2 * n + j) }
    }
    func swapCols(_ c1: Int, _ c2: Int) {
        if c1 == c2 { return }
        for i in 0..<n { M.swapAt(i * n + c1, i * n + c2) }
    }
    func unitNormalizeRow(_ k: Int) {
        let a = M[k * n + k]
        let (g, s, _) = extGcd64(a, delta)
        if a == g { return }
        let m = delta / g
        var rem = g
        var extraProd: Int64 = 1
        var p: Int64 = 2
        while p * p <= rem {
            if rem % p == 0 {
                while rem % p == 0 { rem /= p }
                if m % p != 0 { extraProd *= p }
            }
            p += 1
        }
        if rem > 1 && m % rem != 0 { extraProd *= rem }
        let (_, c1, c2) = extGcd64(m, extraProd)
        let u = modD(Int128(s) * Int128(extraProd) * Int128(c2) + Int128(m) * Int128(c1))
        for j in k..<n {
            M[k * n + j] = modD(Int128(u) * Int128(M[k * n + j]))
        }
    }

    for k in 0..<n {
        while true {
            var found = false
            var pi = k, pj = k
            var bestG = delta + 1
            for i in k..<n {
                for j in k..<n {
                    let v = M[i * n + j]
                    if v != 0 {
                        let g = gcdInt64(v, delta)
                        if !found || g < bestG {
                            found = true
                            bestG = g
                            pi = i
                            pj = j
                        }
                    }
                }
            }
            if !found { break }
            swapRows(k, pi)
            swapCols(k, pj)
            unitNormalizeRow(k)

            var changed = false
            if k + 1 < n {
                for i in (k + 1)..<n {
                    if M[i * n + k] == 0 { continue }
                    let a = M[k * n + k], b = M[i * n + k]
                    if b % a == 0 {
                        let q = b / a
                        for j in k..<n {
                            M[i * n + j] = modD(Int128(M[i * n + j]) - Int128(q) * Int128(M[k * n + j]))
                        }
                    } else {
                        let (g, s, t) = extGcd64(a, b)
                        let u1 = -b / g, u2 = a / g
                        for j in k..<n {
                            let mk = Int128(M[k * n + j])
                            let mi = Int128(M[i * n + j])
                            M[k * n + j] = modD(Int128(s) * mk + Int128(t) * mi)
                            M[i * n + j] = modD(Int128(u1) * mk + Int128(u2) * mi)
                        }
                        unitNormalizeRow(k)
                        changed = true
                    }
                }
            }
            if changed { continue }

            if k + 1 < n {
                for j in (k + 1)..<n {
                    if M[k * n + j] == 0 { continue }
                    let a = M[k * n + k], b = M[k * n + j]
                    if b % a == 0 {
                        let q = b / a
                        for i in k..<n {
                            M[i * n + j] = modD(Int128(M[i * n + j]) - Int128(q) * Int128(M[i * n + k]))
                        }
                    } else {
                        let (g, s, t) = extGcd64(a, b)
                        let u1 = -b / g, u2 = a / g
                        for i in k..<n {
                            let mk = Int128(M[i * n + k])
                            let mj = Int128(M[i * n + j])
                            M[i * n + k] = modD(Int128(s) * mk + Int128(t) * mj)
                            M[i * n + j] = modD(Int128(u1) * mk + Int128(u2) * mj)
                        }
                        changed = true
                    }
                }
            }
            if changed { continue }

            let piv = M[k * n + k]
            var badI = n
            if k + 1 < n {
                outer: for i in (k + 1)..<n {
                    for j in (k + 1)..<n {
                        if M[i * n + j] % piv != 0 {
                            badI = i
                            break outer
                        }
                    }
                }
            }
            if badI < n {
                for j in k..<n {
                    M[k * n + j] = modD(Int128(M[k * n + j]) + Int128(M[badI * n + j]))
                }
                continue
            }
            break
        }
    }

    // 3. Independent R-Type F_p nullity cross-check for p in {2, 3, 23}.
    func nullityModP(_ p: Int64) -> Int32 {
        var fp = lap.map { val -> Int64 in
            let v = Int64(val) % p
            return v < 0 ? v + p : v
        }
        var rank = 0
        for c in 0..<n {
            var piv = n
            for i in rank..<n where fp[i * n + c] != 0 {
                piv = i; break
            }
            if piv == n { continue }
            if piv != rank {
                for j in c..<n { fp.swapAt(rank * n + j, piv * n + j) }
            }
            let (_, s, _) = extGcd64(fp[rank * n + c], p)
            let inv = ((s % p) + p) % p
            for j in c..<n { fp[rank * n + j] = (fp[rank * n + j] * inv) % p }
            for i in 0..<n {
                if i == rank || fp[i * n + c] == 0 { continue }
                let f = fp[i * n + c]
                for j in c..<n {
                    var v = (fp[i * n + j] - f * fp[rank * n + j]) % p
                    if v < 0 { v += p }
                    fp[i * n + j] = v
                }
            }
            rank += 1
        }
        return Int32(n - rank)
    }

    var divOK = true
    var order: Int64 = 1
    var factors = [Int64]()
    var prevD: Int64 = 1
    var cnt2: Int32 = 0, cnt3: Int32 = 0, cnt23: Int32 = 0
    for k in 0..<n {
        let dk = M[k * n + k] == 0 ? delta : gcdInt64(M[k * n + k], delta)
        if dk <= 0 || (k > 0 && (dk % prevD) != 0) { divOK = false }
        prevD = dk
        order *= dk
        if dk % 2 == 0 { cnt2 += 1 }
        if dk % 3 == 0 { cnt3 += 1 }
        if dk % 23 == 0 { cnt23 += 1 }
        if dk > 1 { factors.append(dk) }
    }
    let fpOK = cnt2 == nullityModP(2) && cnt3 == nullityModP(3) && cnt23 == nullityModP(23)
    let chainOK = divOK && fpOK && order == delta
    let passed = chainOK && factors == [2, 2, 8, 736, 6624] && order == 156_008_448

    return SandpileSNFReport(
        nontrivialCount: Int32(factors.count),
        invariantFactors: factors,
        groupOrder: order,
        divisibilityChainOK: chainOK,
        passed: passed
    )
}

// MARK: - Prop 7.2 & Thm 7.8 (NEG-M7): Aut(X), 13 Involutions, & Exact Dhar-Burning Gonality

private func dharQReducedPositive(
    adj0: [Int], adj1: [Int], adj2: [Int], initial: [Int32], q: Int
) -> Bool {
    if initial[q] >= 1 { return true }
    var d = initial
    var burnedDeg = [Int32](repeating: 0, count: 24)
    var burned = [Bool](repeating: false, count: 24)
    var queue = [Int](repeating: 0, count: 24)

    while true {
        for i in 0..<24 {
            burnedDeg[i] = 0
            burned[i] = false
        }
        var head = 0
        var tail = 0
        burned[q] = true
        queue[tail] = q
        tail += 1

        while head < tail {
            let u = queue[head]
            head += 1
            let n0 = adj0[u], n1 = adj1[u], n2 = adj2[u]
            for v in [n0, n1, n2] {
                if burned[v] { continue }
                burnedDeg[v] += 1
                if burnedDeg[v] > d[v] {
                    burned[v] = true
                    queue[tail] = v
                    tail += 1
                }
            }
        }
        if tail == 24 {
            return d[q] >= 1
        }
        for v in 0..<24 where !burned[v] {
            for nb in [adj0[v], adj1[v], adj2[v]] where burned[nb] {
                d[v] -= 1
                d[nb] += 1
            }
        }
        if d[q] >= 1 { return true }
    }
}

public func verifyGonalityAndAutomorphisms() -> GonalityAutReport {
    var adj0 = [Int](repeating: 0, count: 24)
    var adj1 = [Int](repeating: 0, count: 24)
    var adj2 = [Int](repeating: 0, count: 24)
    var adjMat = [Bool](repeating: false, count: 24 * 24)
    var edges = [(Int, Int)]()
    for v: Int32 in 0..<24 {
        let u0 = Int(applyPLRMove(vertex: v, moveId: 0).targetVertex)
        let u1 = Int(applyPLRMove(vertex: v, moveId: 1).targetVertex)
        let u2 = Int(applyPLRMove(vertex: v, moveId: 2).targetVertex)
        let vi = Int(v)
        adj0[vi] = u0; adj1[vi] = u1; adj2[vi] = u2
        adjMat[vi * 24 + u0] = true
        adjMat[vi * 24 + u1] = true
        adjMat[vi * 24 + u2] = true
        if vi < 12 {
            edges.append((vi, u0))
            edges.append((vi, u1))
            edges.append((vi, u2))
        }
    }

    // 1. Exhaustive Aut(X) via BFS-ordered backtracking.
    var order = [0]
    var seen = [Bool](repeating: false, count: 24)
    seen[0] = true
    var qi = 0
    while qi < order.count {
        let u = order[qi]; qi += 1
        for nb in [adj0[u], adj1[u], adj2[u]] where !seen[nb] {
            seen[nb] = true
            order.append(nb)
        }
    }

    var auts = [[Int]]()
    var perm = [Int](repeating: -1, count: 24)
    var used = [Bool](repeating: false, count: 24)

    func searchAut(_ depth: Int) {
        if depth == 24 {
            auts.append(perm)
            return
        }
        let v = order[depth]
        var mapped = [Int]()
        for nb in [adj0[v], adj1[v], adj2[v]] where perm[nb] >= 0 {
            mapped.append(perm[nb])
        }
        func tryImg(_ img: Int) {
            if used[img] { return }
            for mnb in mapped where !adjMat[img * 24 + mnb] { return }
            perm[v] = img
            used[img] = true
            searchAut(depth + 1)
            used[img] = false
            perm[v] = -1
        }
        if mapped.isEmpty {
            for img in 0..<24 { tryImg(img) }
        } else {
            let anchor = mapped[0]
            tryImg(adj0[anchor]); tryImg(adj1[anchor]); tryImg(adj2[anchor])
        }
    }
    searchAut(0)

    // 2. Involutions & Chan's tree-quotient criterion.
    var invCnt: Int32 = 0
    var treeQ: Int32 = 0
    var minBetti: Int32 = 1000
    struct EdgeKey: Hashable { let a: Int; let b: Int }
    for p in auts {
        var isId = true
        var isInv = true
        for i in 0..<24 {
            if p[i] != i { isId = false }
            if p[p[i]] != i { isInv = false }
        }
        if isId || !isInv { continue }
        invCnt += 1

        var vOrb: Int32 = 0
        for i in 0..<24 where i <= p[i] { vOrb += 1 }
        var edgeOrbits = Set<EdgeKey>()
        for (u, v) in edges {
            let pu = p[u], pv = p[v]
            if pu == v && pv == u { continue }
            let a1 = min(u, v), b1 = max(u, v)
            let a2 = min(pu, pv), b2 = max(pu, pv)
            let key = (a1 < a2 || (a1 == a2 && b1 <= b2)) ? EdgeKey(a: a1, b: b1) : EdgeKey(a: a2, b: b2)
            edgeOrbits.insert(key)
        }
        let betti = Int32(edgeOrbits.count) - vOrb + 1
        if betti < minBetti { minBetti = betti }
        if betti == 0 { treeQ += 1 }
    }

    // 3. Exhaustive Dhar-burning rank check over all degree <= 5 effective divisors D >= (C).
    let qOrder = [6, 18, 17, 7, 5, 19, 11, 13, 1, 23, 2, 22, 3, 21, 4, 20, 8, 16, 9, 15, 10, 14, 12, 0]
    func hasRankGe1(_ d: [Int32]) -> Bool {
        for q in qOrder {
            if !dharQReducedPositive(adj0: adj0, adj1: adj1, adj2: adj2, initial: d, q: q) {
                return false
            }
        }
        return true
    }

    var tested: Int64 = 0
    var foundLe5: Int64 = 0
    var div = [Int32](repeating: 0, count: 24)
    div[0] = 1
    func enumDiv(_ rem: Int, _ minV: Int) {
        if rem == 0 {
            tested += 1
            if hasRankGe1(div) { foundLe5 += 1 }
            return
        }
        for v in minV..<24 {
            div[v] += 1
            enumDiv(rem - 1, v)
            div[v] -= 1
        }
    }
    for deg in 1...5 {
        enumDiv(deg - 1, 0)
    }

    // 4. Degree-6 witness 2C + 2Am + Db + Abm.
    var witness = [Int32](repeating: 0, count: 24)
    witness[0] = 2; witness[21] = 2; witness[1] = 1; witness[20] = 1
    let witOK = hasRankGe1(witness)
    let gon: Int32 = (foundLe5 == 0 && witOK) ? 6 : -1

    let passed = auts.count == 24 && invCnt == 13 && treeQ == 0 && minBetti >= 1 &&
                 tested == 20475 && foundLe5 == 0 && witOK && gon == 6
    return GonalityAutReport(
        autOrder: Int32(auts.count),
        involutionCount: invCnt,
        treeQuotientCount: treeQ,
        minQuotientBetti: minBetti,
        divisorsDegLe5Tested: tested,
        rank1DegLe5Found: foundLe5,
        witnessDeg6Rank1OK: witOK,
        computedGonality: gon,
        passed: passed
    )
}

// MARK: - Thm 3.5 & Props 7.9-7.10 (NEG-M5/M6): Weil Polynomial & F_{2^k} Genus-5 Curves

private func polyMul(_ a: [Int64], _ b: [Int64]) -> [Int64] {
    var out = [Int64](repeating: 0, count: a.count + b.count - 1)
    for i in 0..<a.count {
        for j in 0..<b.count {
            out[i + j] += a[i] * b[j]
        }
    }
    return out
}

private func impliedF2Counts(_ c: [Int64], maxK: Int) -> [Int64] {
    var s = [Int64](repeating: 0, count: maxK + 1)
    var N = [Int64](repeating: 0, count: maxK)
    for k in 1...maxK {
        let ck: Int64 = k < c.count ? c[k] : 0
        var acc = -Int64(k) * ck
        if k > 1 {
            for j in 1..<k {
                let cj: Int64 = j < c.count ? c[j] : 0
                acc -= cj * s[k - j]
            }
        }
        s[k] = acc
        N[k - 1] = (Int64(1) << k) + 1 - acc
    }
    return N
}

private func detLU24(_ input: [Double]) -> Double {
    var m = input
    let n = 24
    var sign = 1.0
    for k in 0..<n {
        var piv = k
        var best = abs(m[k * n + k])
        if k + 1 < n {
            for i in (k + 1)..<n {
                let v = abs(m[i * n + k])
                if v > best { best = v; piv = i }
            }
        }
        if best == 0.0 { return 0.0 }
        if piv != k {
            for j in k..<n { m.swapAt(k * n + j, piv * n + j) }
            sign = -sign
        }
        let diag = m[k * n + k]
        if k + 1 < n {
            for i in (k + 1)..<n {
                let f = m[i * n + k] / diag
                for j in (k + 1)..<n { m[i * n + j] -= f * m[k * n + j] }
            }
        }
    }
    var det = sign
    for i in 0..<n { det *= m[i * n + i] }
    return det
}

private func countProp710Curves(k: Int) -> (Int64, Int64) {
    let q = 1 << k
    let polys = [0, 0x2, 0x7, 0xB, 0x13, 0x25]
    let poly = polys[k]
    var mul = [UInt8](repeating: 0, count: 32 * 32)
    var sq = [UInt8](repeating: 0, count: 32)
    for a in 0..<q {
        for b in 0..<q {
            var res = 0, aa = a, bb = b
            for _ in 0..<k {
                if (bb & 1) != 0 { res ^= aa }
                bb >>= 1
                aa <<= 1
                if (aa & q) != 0 { aa ^= poly }
            }
            mul[a * 32 + b] = UInt8(res)
        }
        sq[a] = mul[a * 32 + a]
    }

    var ca: Int64 = 0
    var cb: Int64 = 0
    @inline(__always)
    func evalPoint(_ T: Int, _ U: Int, _ X: Int, _ Y: Int, _ Z: Int) {
        let TT = sq[T], UU = sq[U], XX = sq[X], YY = sq[Y], ZZ = sq[Z]
        let TU = mul[T * 32 + U], TX = mul[T * 32 + X], TY = mul[T * 32 + Y], TZ = mul[T * 32 + Z]
        let UX = mul[U * 32 + X], UY = mul[U * 32 + Y], UZ = mul[U * 32 + Z]
        let XY = mul[X * 32 + Y], XZ = mul[X * 32 + Z], YZ = mul[Y * 32 + Z]

        if (TX ^ TZ ^ YY ^ YZ ^ ZZ) != 0 { return }
        if (TT ^ TU ^ TY ^ TZ ^ UU ^ UX ^ UZ ^ XZ ^ YY) == 0 {
            if (TY ^ UU ^ UX ^ UZ ^ XX ^ XY ^ XZ ^ YY ^ YZ ^ ZZ) == 0 { ca += 1 }
        }
        if (TX ^ UX ^ UY ^ UZ) == 0 {
            if (TU ^ UU ^ UX ^ UY ^ UZ ^ XX ^ XY ^ XZ ^ YY ^ ZZ) == 0 { cb += 1 }
        }
    }

    for u in 0..<q {
        for x in 0..<q {
            for y in 0..<q {
                for z in 0..<q { evalPoint(1, u, x, y, z) }
            }
        }
    }
    for x in 0..<q {
        for y in 0..<q {
            for z in 0..<q { evalPoint(0, 1, x, y, z) }
        }
    }
    for y in 0..<q {
        for z in 0..<q { evalPoint(0, 0, 1, y, z) }
    }
    for z in 0..<q { evalPoint(0, 0, 0, 1, z) }
    evalPoint(0, 0, 0, 0, 1)
    return (ca, cb)
}

public func verifyF2CurvesAndWeil() -> F2CurvesReport {
    let L1: [Int64]  = [1, -1, 2]
    let L1p: [Int64] = [1,  1, 2]
    let L2: [Int64]  = [1, 0, -1, 0, 4]
    let L2p: [Int64] = [1, 0,  1, 0, 4]
    let L4: [Int64]  = [1, 0, 4, 0, 9, 0, 16, 0, 16]

    var p44: [Int64] = [1]
    for _ in 0..<3 { p44 = polyMul(p44, L1) }
    for _ in 0..<3 { p44 = polyMul(p44, L1p) }
    for _ in 0..<2 { p44 = polyMul(p44, L2) }
    for _ in 0..<2 { p44 = polyMul(p44, L2p) }
    for _ in 0..<2 { p44 = polyMul(p44, L4) }

    let nP44 = impliedF2Counts(p44, maxK: 6)

    let adj = buildAdjacencyMatrix()
    var maxRes = 0.0
    for u in [0.11, 0.23, 0.37] {
        var m = [Double](repeating: 0.0, count: 576)
        for i in 0..<24 {
            for j in 0..<24 { m[i * 24 + j] = -u * adj[i * 24 + j] }
            m[i * 24 + i] += 1.0 + 2.0 * u * u
        }
        let lhs = detLU24(m)
        var pval = 0.0
        var up = 1.0
        for c in p44 { pval += Double(c) * up; up *= u }
        let rhs = (1.0 - u) * (1.0 - 2.0 * u) * (1.0 + u) * (1.0 + 2.0 * u) * pval
        let err = abs(lhs - rhs)
        if err > maxRes { maxRes = err }
    }

    let nA0 = impliedF2Counts(polyMul([1, 0, 2], L4), maxK: 4)
    let a0Places = (nA0[3] - nA0[1]) / 4

    let expA = impliedF2Counts(polyMul(L1, L4), maxK: 5)
    let expB = impliedF2Counts(polyMul(L1p, L4), maxK: 5)
    var obsA = [Int64](repeating: 0, count: 5)
    var obsB = [Int64](repeating: 0, count: 5)
    var curvesMatch = true
    for k in 1...5 {
        let (ca, cb) = countProp710Curves(k: k)
        obsA[k - 1] = ca
        obsB[k - 1] = cb
        if ca != expA[k - 1] || cb != expB[k - 1] { curvesMatch = false }
    }

    let passed = nP44 == [3, 39, 9, 75, 33, 27] && nP44[5] < nP44[1] &&
                 a0Places == -1 && curvesMatch && maxRes < 1e-11
    return F2CurvesReport(
        p44PointCounts: nP44,
        cofactorA0Deg4Places: a0Places,
        curveACounts: obsA,
        curveBCounts: obsB,
        expectedACounts: expA,
        expectedBCounts: expB,
        weilFactorMaxResidual: maxRes,
        passed: passed
    )
}

// MARK: - Prop 3.7 (NEG-M1): Exhaustive 12 Tonnetz-Axis Eisenstein Multiplier Conductors

public func verifyEisenstein12Maps() -> Eisenstein12MapsReport {
    var consMasks = [UInt32]()
    consMasks.reserveCapacity(24)
    for r in 0..<12 {
        consMasks.append((1 << r) | (1 << ((r + 4) % 12)) | (1 << ((r + 7) % 12)))
        consMasks.append((1 << r) | (1 << ((r + 3) % 12)) | (1 << ((r + 7) % 12)))
    }
    func isCons(_ x: Int, _ y: Int, _ z: Int) -> Bool {
        if x == y || y == z || x == z { return false }
        let mask: UInt32 = (1 << x) | (1 << y) | (1 << z)
        return consMasks.contains(mask)
    }

    var mapCnt: Int32 = 0
    var minC: Int32 = 1000
    var maxC: Int32 = 0
    var anyIdeal = false

    for a in 0..<12 {
        for b in 0..<12 {
            if gcdInt64(gcdInt64(Int64(a), Int64(b)), 12) != 1 { continue }
            let ab = (a + b) % 12
            if !isCons(0, a, ab) || !isCons(0, ab, b) { continue }
            mapCnt += 1
            var cond: Int32 = 12
            for d in 1...12 {
                var ok = true
                outer: for m in 0..<12 {
                    for n in 0..<12 {
                        if (a * m + b * n) % 12 != 0 { continue }
                        let val = (a * (-d * n) + b * (d * m - d * n)) % 12
                        if val != 0 { ok = false; break outer }
                    }
                }
                if ok { cond = Int32(d); break }
            }
            if cond < minC { minC = cond }
            if cond > maxC { maxC = cond }
            if cond == 1 { anyIdeal = true }
        }
    }
    return Eisenstein12MapsReport(
        tonnetzMapCount: mapCnt,
        minConductor: minC,
        maxConductor: maxC,
        anyKernelIsIdeal: anyIdeal,
        passed: mapCnt == 12 && minC == 12 && maxC == 12 && !anyIdeal
    )
}

// MARK: - Thms 7.1 & 7.13 (NEG-M8): Schottky Schreier Generators & Bruhat-Tits Ball

private struct Mat2 {
    let a: Int64, b: Int64, c: Int64, d: Int64
}

private func mat2Mul(_ x: Mat2, _ y: Mat2) -> Mat2 {
    Mat2(
        a: x.a * y.a + x.b * y.c,
        b: x.a * y.b + x.b * y.d,
        c: x.c * y.a + x.d * y.c,
        d: x.c * y.b + x.d * y.d
    )
}

private func invModPow2(_ x: UInt64, _ r: Int) -> UInt64 {
    var inv: UInt64 = 1
    for _ in 0..<6 {
        inv = inv &* (2 &- x &* inv)
    }
    if r >= 64 { return inv }
    return inv & ((UInt64(1) << r) &- 1)
}

private struct BTKey: Hashable {
    let kind: Int32
    let r: Int32
    let residue: UInt64
}

private func bruhatTitsVertexKey(_ m: Mat2) -> BTKey {
    let content = min(min(v2Int64(m.a), v2Int64(m.b)), min(v2Int64(m.c), v2Int64(m.d)))
    let a = m.a >> content
    let b = m.b >> content
    let c = m.c >> content
    let d = m.d >> content
    let r = v2Int64(a * d - b * c)
    if r == 0 { return BTKey(kind: 0, r: 0, residue: 0) }
    let mask = (UInt64(1) << Int(r)) &- 1
    if (a & 1) != 0 || (b & 1) != 0 {
        let u = (a & 1) != 0 ? a : b
        let w = (a & 1) != 0 ? c : d
        let uMod = UInt64(bitPattern: u) & mask
        let wMod = UInt64(bitPattern: w) & mask
        let alpha = (wMod &* invModPow2(uMod, Int(r))) & mask
        return BTKey(kind: 0, r: r, residue: alpha)
    }
    let u = (c & 1) != 0 ? a : b
    let w = (c & 1) != 0 ? c : d
    let uMod = UInt64(bitPattern: u) & mask
    let wMod = UInt64(bitPattern: w) & mask
    let beta = (uMod &* invModPow2(wMod, Int(r))) & mask
    return BTKey(kind: 1, r: r, residue: beta)
}

public func verifySchottkyGroup() -> SchottkyGroupReport {
    let sig = [
        Mat2(a: 0, b: 1, c: 2, d: 0),
        Mat2(a: 0, b: 2, c: 1, d: 0),
        Mat2(a: -1, b: 1, c: 1, d: 1),
    ]

    var wordTo = [[Int32]](repeating: [], count: 24)
    var visited = [Bool](repeating: false, count: 24)
    var inTree = [[Bool]](repeating: [Bool](repeating: false, count: 3), count: 24)
    var q: [Int32] = [0]
    visited[0] = true
    var qi = 0
    while qi < q.count {
        let u = q[qi]; qi += 1
        for mv: Int32 in 0..<3 {
            let v = applyPLRMove(vertex: u, moveId: mv).targetVertex
            if !visited[Int(v)] {
                visited[Int(v)] = true
                wordTo[Int(v)] = wordTo[Int(u)] + [mv]
                inTree[Int(u)][Int(mv)] = true
                inTree[Int(v)][Int(mv)] = true
                q.append(v)
            }
        }
    }

    var schCnt: Int32 = 0
    var schHyp: Int32 = 0
    var schKer: Int32 = 0
    for u: Int32 in 0..<12 {
        for mv: Int32 in 0..<3 {
            if inTree[Int(u)][Int(mv)] { continue }
            let v = applyPLRMove(vertex: u, moveId: mv).targetVertex
            let raw = wordTo[Int(u)] + [mv] + wordTo[Int(v)].reversed()
            var red = [Int32]()
            for x in raw {
                if red.last == x { red.removeLast() } else { red.append(x) }
            }
            schCnt += 1

            var fixesAll = true
            for t: Int32 in 0..<24 {
                var cur = t
                for m in red { cur = applyPLRMove(vertex: cur, moveId: m).targetVertex }
                if cur != t { fixesAll = false; break }
            }
            if fixesAll { schKer += 1 }

            var mat = Mat2(a: 1, b: 0, c: 0, d: 1)
            for m in red { mat = mat2Mul(mat, sig[Int(m)]) }
            let tr = mat.a + mat.d
            let det = mat.a * mat.d - mat.b * mat.c
            if 2 * v2Int64(tr) < v2Int64(det) { schHyp += 1 }
        }
    }

    var btVertices = Set<BTKey>()
    var wordCnt: Int32 = 0
    func dfsBall(_ depth: Int, _ lastMv: Int, _ cur: Mat2) {
        wordCnt += 1
        btVertices.insert(bruhatTitsVertexKey(cur))
        if depth == 7 { return }
        for mv in 0..<3 where mv != lastMv {
            dfsBall(depth + 1, mv, mat2Mul(cur, sig[mv]))
        }
    }
    dfsBall(0, -1, Mat2(a: 1, b: 0, c: 0, d: 1))

    let g0Word = [0, 1, 2, 1, 0, 2, 0, 1]
    var g0 = Mat2(a: 1, b: 0, c: 0, d: 1)
    for m in g0Word { g0 = mat2Mul(g0, sig[m]) }
    let g0Tr = g0.a + g0.d
    let g0Det = g0.a * g0.d - g0.b * g0.c
    let tauGt4 = g0Tr * g0Tr > 4 * g0Det

    let passed = schCnt == 13 && schHyp == 13 && schKer == 13 &&
                 wordCnt == 382 && btVertices.count == 382 &&
                 g0Tr == 85 && g0Det == 256 && tauGt4
    return SchottkyGroupReport(
        schreierCount: schCnt,
        schreierHyperbolic: schHyp,
        schreierInKernel: schKer,
        btBallR7Words: wordCnt,
        btBallR7Distinct: Int32(btVertices.count),
        gamma0Tr: g0Tr,
        gamma0Det: g0Det,
        gamma0TauGt4: tauGt4,
        passed: passed
    )
}
