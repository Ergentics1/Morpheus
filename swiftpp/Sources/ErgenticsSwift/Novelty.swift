import Foundation

/// Novelty 1 (Theorem A, Theorem B, Corollary B.1, NEG-M11):
/// Exhaustive check of ALL 3-note chord classes under maximal legal step sets S_max(c_0)
/// across all 5 <= N <= nMax.
public struct NoveltyTuneClassificationReport: Sendable, Equatable {
    public let nMax: Int32
    public let chordsTested: Int64
    public let maxLinkIntersection: Int32
    public let tOrbitFailures: Int64
    public let tiOctatonicFailures: Int64
    public let tiUnexpectedFailures: Int64
    public let negM11Verified: Bool
    public let passed: Bool
}

/// Novelty 2 (Theorem C, Correspondence C-2' and C-2''):
/// Exact prime-cadence winding law vs Gaussian (C-2), 4th-order Edgeworth (C-2'), and 6th-order Edgeworth (C-2'').
public struct EdgeworthWindingReport: Sendable, Equatable {
    public let lengthM: Int32
    public let totalPrimes: Int64
    public let variance: Double
    public let varAbsError: Double
    public let excessKurtosis: Double
    public let mTimesExcessKurtosis: Double
    public let tvGaussian: Double
    public let klGaussian: Double
    public let jsdGaussian: Double
    public let tvEdgeworth4: Double
    public let jsdEdgeworth4: Double
    public let tvEdgeworth6: Double
    public let jsdEdgeworth6: Double
    public let tvGain4: Double
    public let tvGain6: Double
    public let passed: Bool
}

/// Novelty 2 (Theorem C, 2D Tonnetz Isotropy & C_6 Hexagonal Symmetry Breaking):
/// Exact prime-cadence cumulants across all 3 canonical Tonnetz axes (W = -u, v, 4u + 3v).
public struct TonnetzAxisCumulantReport: Sendable, Equatable {
    public let lengthM: Int32
    public let totalPrimes: Int64
    public let badDivisibilityCount: Int64
    public let k2OverMU: Double
    public let k2OverMV: Double
    public let k2OverMZigzag: Double
    public let mExKurtU: Double
    public let mExKurtV: Double
    public let mExKurtZigzag: Double
    public let maxIsotropySpread4th: Double
    public let m2Std6U: Double
    public let m2Std6V: Double
    public let m2Std6Zigzag: Double
    public let passed: Bool
}

private struct PitchTriple: Hashable, Comparable {
    let a: Int32
    let b: Int32
    let c: Int32

    init(_ x: Int32, _ y: Int32, _ z: Int32) {
        var arr = [x, y, z]
        if arr[0] > arr[1] { arr.swapAt(0, 1) }
        if arr[1] > arr[2] { arr.swapAt(1, 2) }
        if arr[0] > arr[1] { arr.swapAt(0, 1) }
        self.a = arr[0]
        self.b = arr[1]
        self.c = arr[2]
    }

    static func < (lhs: PitchTriple, rhs: PitchTriple) -> Bool {
        if lhs.a != rhs.a { return lhs.a < rhs.a }
        if lhs.b != rhs.b { return lhs.b < rhs.b }
        return lhs.c < rhs.c
    }
}

private struct PitchPair: Hashable {
    let a: Int32
    let b: Int32

    init(_ x: Int32, _ y: Int32) {
        if x < y {
            self.a = x
            self.b = y
        } else {
            self.a = y
            self.b = x
        }
    }
}

@inline(__always)
private func circDist(_ a: Int32, _ b: Int32, _ n: Int32) -> Int32 {
    let d = a >= b ? (a - b) : (b - a)
    return 2 * d <= n ? d : (n - d)
}

private func graphHasCycle(nNodes: Int, edges: [(Int, Int)]) -> Bool {
    var par = Array(0..<nNodes)
    func find(_ x0: Int) -> Int {
        var x = x0
        while par[x] != x {
            par[x] = par[par[x]]
            x = par[x]
        }
        return x
    }
    for (u, v) in edges {
        let ru = find(u)
        let rv = find(v)
        if ru == rv { return true }
        par[ru] = rv
    }
    return false
}

private func isOctatonicDiameterTriple(_ n: Int32, _ cls: PitchTriple) -> Bool {
    if n % 8 != 0 { return false }
    let m = n / 8
    var ivs = [circDist(cls.a, cls.b, n), circDist(cls.b, cls.c, n), circDist(cls.a, cls.c, n)]
    ivs.sort()
    return ivs[0] == m && ivs[1] == 3 * m && ivs[2] == 4 * m
}

private func verifyNegM11Explicit() -> Bool {
    let n: Int32 = 8
    var tiOrbit = Set<PitchTriple>()
    for t: Int32 in 0..<n {
        tiOrbit.insert(PitchTriple(t % n, (t + 1) % n, (t + 4) % n))
        tiOrbit.insert(PitchTriple(t % n, (t + n - 1) % n, (t + n - 4) % n))
    }
    let cyc1 = [PitchTriple(0, 1, 4), PitchTriple(0, 3, 4), PitchTriple(0, 4, 5), PitchTriple(0, 4, 7)]
    let cyc2 = [PitchTriple(1, 2, 6), PitchTriple(2, 3, 6), PitchTriple(2, 5, 6), PitchTriple(2, 6, 7)]
    let expectedTune: [Int32] = [3, 5, 7, 1]

    func checkCycle(_ cyc: [PitchTriple]) -> [Int32]? {
        var tune = [Int32]()
        for i in 0..<4 {
            let c = cyc[i]
            if !tiOrbit.contains(c) { return nil }
            if circDist(c.a, c.b, n) == 2 || circDist(c.b, c.c, n) == 2 || circDist(c.a, c.c, n) == 2 {
                return nil
            }
            let nxt = cyc[(i + 1) % 4]
            let prv = cyc[(i + 3) % 4]
            if nxt == prv { return nil }
            let ca = [c.a, c.b, c.c]
            let na = [nxt.a, nxt.b, nxt.c]
            var shared = 0
            var depart: Int32 = -1
            var arrive: Int32 = -1
            for x in ca {
                if na.contains(x) { shared += 1 } else { depart = x }
            }
            for y in na {
                if !ca.contains(y) { arrive = y }
            }
            if shared != 2 || depart < 0 || arrive < 0 { return nil }
            if circDist(depart, arrive, n) != 2 { return nil }
            tune.append(arrive)
        }
        if cyc[0] == cyc[2] && cyc[1] == cyc[3] { return nil }
        return tune
    }

    guard let t1 = checkCycle(cyc1), let t2 = checkCycle(cyc2) else { return false }
    if t1 != expectedTune || t2 != expectedTune { return false }
    for a in cyc1 {
        if cyc2.contains(a) { return false }
    }
    return true
}

public func verifyNoveltyTuneClassification(nMax: Int32) -> NoveltyTuneClassificationReport {
    var chordsTested: Int64 = 0
    var maxLinkIntersection: Int32 = 0
    var tOrbitFailures: Int64 = 0
    var tiOctatonicFailures: Int64 = 0
    var tiUnexpectedFailures: Int64 = 0
    let negM11OK = verifyNegM11Explicit()

    for n: Int32 in 5...nMax {
        var classes = Set<PitchTriple>()
        for a: Int32 in 1..<n {
            for b: Int32 in (a + 1)..<n {
                var best = PitchTriple(n, n, n)
                for t: Int32 in 0..<n {
                    let c1 = PitchTriple((n - t) % n, (a + n - t) % n, (b + n - t) % n)
                    if c1 < best { best = c1 }
                    let c2 = PitchTriple(t % n, (t + n - a) % n, (t + n - b) % n)
                    if c2 < best { best = c2 }
                }
                classes.insert(best)
            }
        }

        for cls in classes {
            chordsTested += 1
            let d01 = circDist(cls.a, cls.b, n)
            let d12 = circDist(cls.b, cls.c, n)
            let d02 = circDist(cls.a, cls.c, n)
            var legalSteps = Set<Int32>()
            for s: Int32 in 1...(n / 2) {
                if s != d01 && s != d12 && s != d02 { legalSteps.insert(s) }
            }

            var tSet = Set<PitchTriple>()
            var tiSet = Set<PitchTriple>()
            for t: Int32 in 0..<n {
                let ct = PitchTriple((cls.a + t) % n, (cls.b + t) % n, (cls.c + t) % n)
                tSet.insert(ct)
                tiSet.insert(ct)
                let ci = PitchTriple((n + t - cls.a) % n, (n + t - cls.b) % n, (n + t - cls.c) % n)
                tiSet.insert(ci)
            }

            // Theorem A: |L_0 ∩ L_t| <= 2 universally.
            var links = Array(repeating: Set<PitchPair>(), count: Int(n))
            for c in tiSet {
                links[Int(c.a)].insert(PitchPair(c.b, c.c))
                links[Int(c.b)].insert(PitchPair(c.a, c.c))
                links[Int(c.c)].insert(PitchPair(c.a, c.b))
            }
            for t in 1..<Int(n) {
                var common: Int32 = 0
                for p in links[0] {
                    if links[t].contains(p) { common += 1 }
                }
                if common > maxLinkIntersection { maxLinkIntersection = common }
            }

            // Theorem B: one-moving-voice held-note cycles under S_max(c_0).
            func hasOneVoiceCycle(_ orb: Set<PitchTriple>) -> Bool {
                let ni = Int(n)
                var compMap = Array(repeating: [Int32](), count: ni * ni)
                for c in orb {
                    compMap[Int(c.a) * ni + Int(c.b)].append(c.c)
                    compMap[Int(c.a) * ni + Int(c.c)].append(c.b)
                    compMap[Int(c.b) * ni + Int(c.c)].append(c.a)
                }
                var compList = [[Int32]]()
                for var v in compMap where v.count >= 3 {
                    v.sort()
                    var uniq = [Int32]()
                    for x in v {
                        if uniq.last != x { uniq.append(x) }
                    }
                    if uniq.count >= 3 { compList.append(uniq) }
                }
                for i in 0..<compList.count {
                    for j in (i + 1)..<compList.count {
                        var common = [Int32]()
                        let a = compList[i]
                        let b = compList[j]
                        var ia = 0, ib = 0
                        while ia < a.count && ib < b.count {
                            if a[ia] == b[ib] {
                                common.append(a[ia])
                                ia += 1
                                ib += 1
                            } else if a[ia] < b[ib] {
                                ia += 1
                            } else {
                                ib += 1
                            }
                        }
                        if common.count < 3 { continue }
                        var edges = [(Int, Int)]()
                        for u in 0..<common.count {
                            for v in (u + 1)..<common.count {
                                if legalSteps.contains(circDist(common[u], common[v], n)) {
                                    edges.append((u, v))
                                }
                            }
                        }
                        if graphHasCycle(nNodes: common.count, edges: edges) { return true }
                    }
                }
                return false
            }

            if hasOneVoiceCycle(tSet) { tOrbitFailures += 1 }
            if hasOneVoiceCycle(tiSet) {
                if isOctatonicDiameterTriple(n, cls) { tiOctatonicFailures += 1 }
                else { tiUnexpectedFailures += 1 }
            }
        }
    }

    let expectedOct = Int64(nMax / 8)
    let passed = maxLinkIntersection <= 2 &&
                 tOrbitFailures == 0 &&
                 tiOctatonicFailures == expectedOct &&
                 tiUnexpectedFailures == 0 &&
                 negM11OK
    return NoveltyTuneClassificationReport(
        nMax: nMax,
        chordsTested: chordsTested,
        maxLinkIntersection: maxLinkIntersection,
        tOrbitFailures: tOrbitFailures,
        tiOctatonicFailures: tiOctatonicFailures,
        tiUnexpectedFailures: tiUnexpectedFailures,
        negM11Verified: negM11OK,
        passed: passed
    )
}

public func evaluateEdgeworthWindingCalibration(m: Int32) -> EdgeworthWindingReport {
    let wd = computeExactWindingDistribution(m: m)
    let invTot = 1.0 / Double(wd.totalPrimes)
    var p = [Double](repeating: 0.0, count: 17)
    var t2 = [Double](repeating: 0.0, count: 17)
    var t4 = [Double](repeating: 0.0, count: 17)
    for i in 0..<17 {
        p[i] = Double(wd.primeCounts[i]) * invTot
        let w = Double(wd.wMin + Int32(i))
        let w2 = w * w
        t2[i] = p[i] * w2
        t4[i] = p[i] * w2 * w2
    }
    let m2 = sumNeumaier(t2)
    let m4 = sumNeumaier(t4)
    let dm = Double(m)
    let sig2 = dm / 24.0
    let sig = sqrt(sig2)
    let varAbsErr = abs(m2 - sig2)
    let exKurt = m4 / (m2 * m2) - 3.0
    let mExKurt = dm * exKurt

    let c4 = -17.0 / (48.0 * dm)
    let c6 = 1469.0 / (2880.0 * dm * dm)
    let c8 = 289.0 / (4608.0 * dm * dm)

    func evalOrder(_ order: Int) -> (tv: Double, jsd: Double, kl: Double) {
        func weight(_ wi: Int32) -> Double {
            let z = Double(wi) / sig
            let z2 = z * z
            let base = exp(-0.5 * z2)
            if order == 0 { return base }
            let h4 = z2 * z2 - 6.0 * z2 + 3.0
            var poly = 1.0 + c4 * h4
            if order >= 6 {
                let h6 = z2 * z2 * z2 - 15.0 * z2 * z2 + 45.0 * z2 - 15.0
                let h8 = z2 * z2 * z2 * z2 - 28.0 * z2 * z2 * z2 + 210.0 * z2 * z2 - 420.0 * z2 + 105.0
                poly += c6 * h6 + c8 * h8
            }
            return max(0.0, base * poly)
        }
        var znorm = 0.0
        for w: Int32 in -24...24 { znorm += weight(w) }
        var q = [Double](repeating: 0.0, count: 17)
        for i in 0..<17 { q[i] = weight(wd.wMin + Int32(i)) / znorm }
        let qIn = sumNeumaier(q)
        let qOut = max(0.0, 1.0 - qIn)
        var tvSum = qOut
        var kl = 0.0
        var jsd = 0.5 * log(2.0) * qOut
        for i in 0..<17 {
            tvSum += abs(p[i] - q[i])
            let mid = 0.5 * (p[i] + q[i])
            if p[i] > 0.0 {
                jsd += 0.5 * p[i] * log(p[i] / mid)
                if order == 0 && q[i] > 0.0 {
                    kl += p[i] * log(p[i] / q[i])
                }
            }
            if q[i] > 0.0 {
                jsd += 0.5 * q[i] * log(q[i] / mid)
            }
        }
        return (0.5 * tvSum, jsd, kl)
    }

    let g0 = evalOrder(0)
    let g4 = evalOrder(4)
    let g6 = evalOrder(6)
    let gain4 = g4.tv > 0.0 ? (g0.tv / g4.tv) : 0.0
    let gain6 = g6.tv > 0.0 ? (g0.tv / g6.tv) : 0.0

    var ok = wd.nonMultiple12Closed == 0 &&
             g0.kl >= 0.0 && g0.jsd >= 0.0 && g4.jsd >= 0.0 && g6.jsd >= 0.0 &&
             g4.tv < g0.tv && g4.jsd < g0.jsd
    if m >= 24 { ok = ok && (g6.tv < g4.tv) && (g6.jsd < g4.jsd) }
    if m == 40 {
        ok = ok && abs(mExKurt - (-8.5)) < 0.01 && gain4 > 10.0 && gain6 > 70.0 && varAbsErr < 1e-4
    }
    return EdgeworthWindingReport(
        lengthM: m,
        totalPrimes: wd.totalPrimes,
        variance: m2,
        varAbsError: varAbsErr,
        excessKurtosis: exKurt,
        mTimesExcessKurtosis: mExKurt,
        tvGaussian: g0.tv,
        klGaussian: g0.kl,
        jsdGaussian: g0.jsd,
        tvEdgeworth4: g4.tv,
        jsdEdgeworth4: g4.jsd,
        tvEdgeworth6: g6.tv,
        jsdEdgeworth6: g6.jsd,
        tvGain4: gain4,
        tvGain6: gain6,
        passed: ok
    )
}

private func mobiusMuLocal(_ n0: Int32) -> Int32 {
    if n0 <= 0 { return 0 }
    var n = n0
    var mu: Int32 = 1
    var p: Int32 = 2
    while p * p <= n {
        if n % p == 0 {
            n /= p
            if n % p == 0 { return 0 }
            mu = -mu
        }
        p += 1
    }
    if n > 1 { mu = -mu }
    return mu
}

private struct AxisStatsSwift {
    let totalPrimes: Int64
    let badDiv: Int64
    let k2OverM: Double
    let mStd4: Double
    let m2Std6: Double
}

private func computeTonnetzAxisExact(_ s0: Int32, _ s1: Int32, _ s2: Int32, _ divK: Int32, _ m: Int32) -> AxisStatsSwift {
    var succ0 = [Int](repeating: 0, count: 72)
    var succ1 = [Int](repeating: 0, count: 72)
    var stepS = [Int](repeating: 0, count: 72)
    let ms = [Int(s0), Int(s1), Int(s2)]
    for v in 0..<24 {
        let r = v % 12
        for mv in 0..<3 {
            let e = 3 * v + mv
            let tv: Int
            if v < 12 {
                tv = mv == 0 ? (12 + r) : (mv == 1 ? (12 + (r + 4) % 12) : (12 + (r + 9) % 12))
                stepS[e] = ms[mv]
            } else {
                tv = mv == 0 ? r : (mv == 1 ? ((r + 8) % 12) : ((r + 3) % 12))
                stepS[e] = -ms[mv]
            }
            var idx = 0
            for mv2 in 0..<3 where mv2 != mv {
                if idx == 0 { succ0[e] = 3 * tv + mv2 } else { succ1[e] = 3 * tv + mv2 }
                idx += 1
            }
        }
    }
    let mi = Int(m)
    let dk = Int(divK)
    let maxStep = max(abs(ms[0]), max(abs(ms[1]), abs(ms[2])))
    let maxS = maxStep * mi
    let stride = 2 * maxS + 1
    let off = maxS
    let maxW = maxS / dk
    let wStride = 2 * maxW + 1

    var nDW = Array(repeating: [Int64](repeating: 0, count: wStride), count: mi + 1)
    var badDiv: Int64 = 0
    var cur = [Int64](repeating: 0, count: 72 * stride)
    var nxt = [Int64](repeating: 0, count: 72 * stride)

    for e0 in 0..<72 {
        cur.withUnsafeMutableBufferPointer { $0.initialize(repeating: 0) }
        cur[e0 * stride + off + stepS[e0]] = 1
        for d in 2...mi {
            nxt.withUnsafeMutableBufferPointer { $0.initialize(repeating: 0) }
            let slim = maxStep * (d - 1)
            for e in 0..<72 {
                let base = e * stride
                let e1 = succ0[e]
                let e2 = succ1[e]
                let ds1 = stepS[e1]
                let ds2 = stepS[e2]
                let b1 = e1 * stride
                let b2 = e2 * stride
                for s in (-slim)...slim {
                    let c = cur[base + off + s]
                    if c == 0 { continue }
                    nxt[b1 + off + s + ds1] &+= c
                    nxt[b2 + off + s + ds2] &+= c
                }
            }
            swap(&cur, &nxt)
            if d % 2 == 0 && (mi % d == 0) {
                let slimD = maxStep * d
                for e in 0..<72 where succ0[e] == e0 || succ1[e] == e0 {
                    let base = e * stride
                    for s in (-slimD)...slimD {
                        let c = cur[base + off + s]
                        if c == 0 { continue }
                        if s % dk != 0 {
                            badDiv += c
                        } else {
                            nDW[d][s / dk + maxW] += c
                        }
                    }
                }
            }
        }
    }

    var piW = [Int64](repeating: 0, count: wStride)
    var totalPi: Int64 = 0
    for w in (-maxW)...maxW {
        var acc: Int64 = 0
        var d = 2
        while d <= mi {
            if mi % d == 0 {
                let k = mi / d
                if w % k == 0 {
                    let mu = mobiusMuLocal(Int32(k))
                    if mu != 0 {
                        acc += Int64(mu) * nDW[d][w / k + maxW]
                    }
                }
            }
            d += 2
        }
        let cnt = acc / Int64(mi)
        piW[w + maxW] = cnt
        totalPi += cnt
    }

    var t2 = [Double](repeating: 0.0, count: wStride)
    var t4 = [Double](repeating: 0.0, count: wStride)
    var t6 = [Double](repeating: 0.0, count: wStride)
    let invTot = 1.0 / Double(totalPi)
    for w in (-maxW)...maxW {
        let idx = w + maxW
        let p = Double(piW[idx]) * invTot
        let wd = Double(w)
        let w2 = wd * wd
        t2[idx] = p * w2
        t4[idx] = p * w2 * w2
        t6[idx] = p * w2 * w2 * w2
    }
    let m2 = sumNeumaier(t2)
    let m4 = sumNeumaier(t4)
    let m6 = sumNeumaier(t6)
    let k2 = m2
    let k4 = m4 - 3.0 * m2 * m2
    let k6 = m6 - 15.0 * m4 * m2 + 30.0 * m2 * m2 * m2
    let dm = Double(m)
    return AxisStatsSwift(
        totalPrimes: totalPi,
        badDiv: badDiv,
        k2OverM: k2 / dm,
        mStd4: dm * (k4 / (k2 * k2)),
        m2Std6: dm * dm * (k6 / (k2 * k2 * k2))
    )
}

public func verifyTonnetzAxisCumulants(m: Int32) -> TonnetzAxisCumulantReport {
    let su = computeTonnetzAxisExact(-1, -1, 2, 12, m)
    let sv = computeTonnetzAxisExact(-1, 2, -1, 9, m)
    let sa = computeTonnetzAxisExact(0, 1, -1, 1, m)

    let badDiv = su.badDiv + sv.badDiv + sa.badDiv
    let spread = max(
        abs(su.mStd4 - (-8.5)),
        max(abs(sv.mStd4 - (-8.5)), abs(sa.mStd4 - (-8.5)))
    )
    let countsMatch = su.totalPrimes == sv.totalPrimes && su.totalPrimes == sa.totalPrimes
    let k2OK = abs(su.k2OverM - 1.0 / 24.0) < 1e-3 &&
               abs(sv.k2OverM - 2.0 / 27.0) < 1e-3 &&
               abs(sa.k2OverM - 2.0) < 1e-2
    let iso4OK = m >= 36 ? (spread < 0.05) : (spread < 0.5)
    let passed = countsMatch && badDiv == 0 && k2OK && iso4OK

    return TonnetzAxisCumulantReport(
        lengthM: m,
        totalPrimes: su.totalPrimes,
        badDivisibilityCount: badDiv,
        k2OverMU: su.k2OverM,
        k2OverMV: sv.k2OverM,
        k2OverMZigzag: sa.k2OverM,
        mExKurtU: su.mStd4,
        mExKurtV: sv.mStd4,
        mExKurtZigzag: sa.mStd4,
        maxIsotropySpread4th: spread,
        m2Std6U: su.m2Std6,
        m2Std6V: sv.m2Std6,
        m2Std6Zigzag: sa.m2Std6,
        passed: passed
    )
}
