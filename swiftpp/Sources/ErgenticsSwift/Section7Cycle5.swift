import Foundation

/// Pure Swift 6.4 independent verifier for ADPIE Cycle 5 (zero C++ imports):
/// 1. Novelty 3 (Theorem D — Three-Pincer Hilbert Class Field Obstruction) & Theorem 7.19(b);
/// 2. Exhaustive genus-13 Shimura curve census (Theorem 7.11 & NEG-E10: X_0^690(1));
/// 3. Exact Siegel real-quadratic scan (Prop 7.18(a)), PGL_2(F_8) 504-element census (Prop 7.17(b)),
///    and Hamilton trace obstruction (Prop 7.3).

public struct TheoremDPincerReport: Sendable, Equatable {
    public let passed: Bool
    public let quadratureSelfCheckOK: Bool
    public let qExplicitFormulaLB: Double
    public let tail15LBb42: Double
    public let tail15UB: Double
    public let tail15EMinusF2: Double
    public let deg9To14Survivors: Int32
    public let worstDeg9Margin: Double
    public let worstDeg10Margin: Double
    public let deg7MaxSurvivingU: Int32
    public let deg7Hge2Survivors: Int32
    public let deg7MaxRootDisc: Double
    public let deg8MaxSurvivingU: Int32
    public let deg8Hge2Survivors: Int32
    public let deg8MaxRootDisc: Double
    public let deg6MaxSurvivingU: Int32
    public let deg6U16H1Dead: Int32
    public let deg6U16Hge2Dead: Int32
    public let deg6U16H1Margin: Double
    public let deg6U16Hge2Margin: Double
    public let deg6OldDiscCeiling: Double
    public let deg6NewDiscCeiling: Double
}

public struct ShimuraGenus13Report: Sendable, Equatable {
    public let passed: Bool
    public let totalPairs: Int32
    public let torsionFreePairs: Int32
    public let negE10Detected: Int32
    public let negE10Phi: Int32
    public let negE10E2: Int32
    public let negE10E3: Int32
    public let gammaHCount: Int32
}

public struct Section7ArithmeticCycle5Report: Sendable, Equatable {
    public let passed: Bool
    public let quadSplit2Scanned: Int32
    public let quadHplus1Solutions: Int32
    public let quadD41Solutions: Int32
    public let quadD137Solutions: Int32
    public let pgl2F8Order: Int32
    public let pgl2F8Order3Count: Int32
    public let pgl2F8Order3FreeCount: Int32
    public let gamma0PowersObstructed: Int32
}

private let kCycle5Pi = 3.141592653589793238462643383279502884
private let kCycle5EulerGamma = 0.577215664901532860606512090082402431

private struct PureGL64 {
    let t: [Double]
    let w: [Double]
    let selfCheckOK: Bool

    init() {
        let n = 64
        var nodes = [Double](repeating: 0.0, count: n)
        var weights = [Double](repeating: 0.0, count: n)
        for i in 0..<(n / 2) {
            var x = cos(kCycle5Pi * (Double(i) + 0.75) / (Double(n) + 0.5))
            var dp = 0.0
            for _ in 0..<12 {
                var p0 = 1.0
                var p1 = x
                for k in 2...n {
                    let dk = Double(k)
                    let p2 = ((2.0 * dk - 1.0) * x * p1 - (dk - 1.0) * p0) / dk
                    p0 = p1
                    p1 = p2
                }
                dp = Double(n) * (x * p1 - p0) / (x * x - 1.0)
                let dx = p1 / dp
                x -= dx
                if abs(dx) < 1e-16 { break }
            }
            let wi = 2.0 / ((1.0 - x * x) * dp * dp)
            nodes[i] = -x
            nodes[n - 1 - i] = x
            weights[i] = wi
            weights[n - 1 - i] = wi
        }
        var sumW = 0.0
        var sumX2 = 0.0
        for i in 0..<n {
            sumW += weights[i]
            sumX2 += weights[i] * nodes[i] * nodes[i]
        }
        self.t = nodes
        self.w = weights
        self.selfCheckOK = abs(sumW - 2.0) < 1e-14 && abs(sumX2 - 2.0 / 3.0) < 1e-14
    }
}

@inline(__always)
private func poitouH1(_ u: Double) -> Double {
    if u <= 0.0 { return 1.0 }
    if u >= 2.0 { return 0.0 }
    return ((2.0 - u) * (1.0 + 0.5 * cos(kCycle5Pi * u)) / 3.0) + sin(kCycle5Pi * u) / (2.0 * kCycle5Pi)
}

private struct PoitouPoint {
    let b: Double
    let logA: Double
    let logB: Double
    let E: Double
    let f2: Double
    let f4: Double
}

private func primeBoost(_ q: Int64, b: Double) -> Double {
    let lq = log(Double(q))
    var s = 0.0
    var qm = Double(q)
    var m = 1
    while Double(m) * lq < 2.0 * b {
        s += (4.0 * lq / (1.0 + qm)) * poitouH1(Double(m) * lq / b)
        qm *= Double(q)
        m += 1
    }
    return s
}

private func evalPoitou(_ gl: PureGL64, b: Double) -> PoitouPoint {
    var iSinh = 0.0
    var iCosh = 0.0
    for i in 0..<64 {
        let u = 1.0 + gl.t[i]
        let x = b * u
        let g = poitouH1(u)
        let wi = gl.w[i]
        iSinh += wi * b * (1.0 - g) / sinh(x)
        let ch = cosh(0.5 * x)
        iCosh += wi * b * g / (2.0 * ch * ch)
    }
    let iTail = (b < 18.0) ? log((exp(2.0 * b) + 1.0) / (exp(2.0 * b) - 1.0)) : 2.0 * exp(-2.0 * b)
    let logB = kCycle5EulerGamma + log(4.0 * kCycle5Pi) - iSinh - iTail
    let logA = logB + iCosh
    return PoitouPoint(b: b, logA: logA, logB: logB, E: (8.0 * b) / 3.0, f2: primeBoost(2, b: b), f4: primeBoost(4, b: b))
}

private func bestLBGrid(_ grid: [PoitouPoint], deg: Double, rho1: Double, coeffF2: Double, coeffF4: Double) -> Double {
    var best = -1e9
    for p in grid {
        let val = rho1 * p.logA + (1.0 - rho1) * p.logB - p.E / deg + coeffF2 * p.f2 + coeffF4 * p.f4
        if val > best { best = val }
    }
    return best
}

private func isPrime64(_ n: Int64) -> Bool {
    if n < 2 { return false }
    if n % 2 == 0 { return n == 2 }
    var d: Int64 = 3
    while d * d <= n {
        if n % d == 0 { return false }
        d += 2
    }
    return true
}

private func gcdLocal64(_ a0: Int64, _ b0: Int64) -> Int64 {
    var a = a0 < 0 ? -a0 : a0
    var b = b0 < 0 ? -b0 : b0
    while b != 0 {
        let r = a % b
        a = b
        b = r
    }
    return a
}

private func sigma1Local(_ n: Int64) -> Int64 {
    var s: Int64 = 0
    var d: Int64 = 1
    while d * d <= n {
        if n % d == 0 {
            s += d
            if d * d != n { s += n / d }
        }
        d += 1
    }
    return s
}

private func isqrtLocal(_ n: Int64) -> Int64 {
    var r = Int64(Double(n).squareRoot())
    while (r + 1) * (r + 1) <= n { r += 1 }
    while r * r > n { r -= 1 }
    return r
}

private func legendreLocal(_ a: Int64, _ p: Int64) -> Int {
    let x = ((a % p) + p) % p
    if x == 0 { return 0 }
    var res: Int64 = 1
    var e = (p - 1) / 2
    var base = x
    while e > 0 {
        if (e & 1) == 1 { res = (res * base) % p }
        base = (base * base) % p
        e >>= 1
    }
    return (res == p - 1) ? -1 : Int(res)
}

private func isFundamentalDisc(_ D: Int64) -> Bool {
    if D <= 1 { return false }
    if D % 4 == 1 {
        var p: Int64 = 2
        while p * p <= D {
            if D % (p * p) == 0 { return false }
            p += 1
        }
        return true
    }
    if D % 4 == 0 {
        let m = D / 4
        if m % 4 != 2 && m % 4 != 3 { return false }
        var p: Int64 = 2
        while p * p <= m {
            if m % (p * p) == 0 { return false }
            p += 1
        }
        return true
    }
    return false
}

private struct QuadForm: Hashable {
    let a: Int64
    let b: Int64
    let c: Int64
}

private func narrowClassNumberQuad(_ D: Int64) -> Int32 {
    let sD = isqrtLocal(D)
    var forms = Set<QuadForm>()
    var b: Int64 = 1
    while b <= sD {
        if (D - b * b) % 4 == 0 {
            let prod = (D - b * b) / 4
            var d: Int64 = 1
            while d <= prod {
                if prod % d == 0 && sD - b < 2 * d && 2 * d < sD + b {
                    let c = prod / d
                    if gcdLocal64(gcdLocal64(d, b), c) == 1 {
                        forms.insert(QuadForm(a: d, b: b, c: -c))
                        forms.insert(QuadForm(a: -d, b: b, c: c))
                    }
                }
                d += 1
            }
        }
        b += 1
    }
    func step(_ f: QuadForm) -> QuadForm {
        let ac = f.c < 0 ? -f.c : f.c
        let bNew = 2 * ac * ((sD + f.b) / (2 * ac)) - f.b
        let cNew = (bNew * bNew - D) / (4 * f.c)
        return QuadForm(a: f.c, b: bNew, c: cNew)
    }
    var visited = Set<QuadForm>()
    var cycles: Int32 = 0
    for f in forms {
        if visited.contains(f) { continue }
        cycles += 1
        var cur = f
        while !visited.contains(cur) {
            visited.insert(cur)
            cur = step(cur)
        }
    }
    return cycles
}

private func countQuadDNSolutions(_ D: Int64, target PTarget: Int64) -> Int32 {
    var norms: [Int64] = [2]
    if PTarget + 1 >= 3 {
        for p in Int64(3)...(PTarget + 1) {
            if !isPrime64(p) { continue }
            let leg = legendreLocal(D, p)
            if leg == 1 {
                norms.append(p)
                norms.append(p)
            } else if leg == 0 {
                norms.append(p)
            } else if p * p <= PTarget + 1 {
                norms.append(p * p)
            }
        }
    }
    var count: Int32 = 0
    func dfs(_ idx: Int, _ rem: Int64, _ dCnt: Int) {
        if rem == 1 {
            if dCnt % 2 == 0 { count += 1 }
            return
        }
        if idx == norms.count { return }
        let q = norms[idx]
        dfs(idx + 1, rem, dCnt)
        if q == 2 {
            dfs(idx + 1, rem, dCnt + 1)
        } else if rem % (q - 1) == 0 {
            dfs(idx + 1, rem / (q - 1), dCnt + 1)
        }
        var f = q + 1
        while f <= rem {
            if rem % f == 0 {
                dfs(idx + 1, rem / f, dCnt)
            }
            if f > rem / q { break }
            f *= q
        }
    }
    dfs(0, PTarget, 0)
    return count
}

@inline(__always)
private func kroneckerNeg4(_ p: Int64) -> Int64 {
    if p == 2 { return 0 }
    return (p % 4 == 1) ? 1 : -1
}

@inline(__always)
private func kroneckerNeg3(_ p: Int64) -> Int64 {
    if p == 3 { return 0 }
    return (p % 3 == 1) ? 1 : -1
}

@inline(__always)
private func f8Mul(_ a: UInt8, _ b: UInt8) -> UInt8 {
    var p: UInt8 = 0
    for i: UInt8 in 0..<3 {
        if (b & (1 << i)) != 0 { p ^= (a << i) }
    }
    if (p & 16) != 0 { p ^= (0b1011 << 1) }
    if (p & 8) != 0 { p ^= 0b1011 }
    return p & 7
}

@inline(__always)
private func f8Inv(_ a: UInt8) -> UInt8 {
    let a2 = f8Mul(a, a)
    let a4 = f8Mul(a2, a2)
    return f8Mul(a2, a4)
}

private struct F8Mat2 {
    let a, b, c, d: UInt8
}

@inline(__always)
private func f8MatMul(_ x: F8Mat2, _ y: F8Mat2) -> F8Mat2 {
    F8Mat2(
        a: f8Mul(x.a, y.a) ^ f8Mul(x.b, y.c),
        b: f8Mul(x.a, y.b) ^ f8Mul(x.b, y.d),
        c: f8Mul(x.c, y.a) ^ f8Mul(x.d, y.c),
        d: f8Mul(x.c, y.b) ^ f8Mul(x.d, y.d)
    )
}

@inline(__always)
private func f8IsScalar(_ m: F8Mat2) -> Bool {
    m.b == 0 && m.c == 0 && m.a == m.d && m.a != 0
}

@inline(__always)
private func f8P1Act(_ m: F8Mat2, _ pt: Int) -> Int {
    let num: UInt8
    let den: UInt8
    if pt == 8 {
        num = m.a
        den = m.c
    } else {
        let x = UInt8(pt)
        num = f8Mul(m.a, x) ^ m.b
        den = f8Mul(m.c, x) ^ m.d
    }
    if den == 0 { return 8 }
    return Int(f8Mul(num, f8Inv(den)))
}

public func verifyTheoremDPincer() -> TheoremDPincerReport {
    let gl = PureGL64()
    let p2 = evalPoitou(gl, b: 2.0)
    var qPSum = 0.0
    for p in Int64(2)...60 {
        if isPrime64(p) && log(Double(p)) < 4.0 {
            qPSum += primeBoost(p, b: 2.0)
        }
    }
    let qExplicitLB = p2.logA - p2.E + qPSum

    let p42 = evalPoitou(gl, b: 4.2)
    let tail15EMinusF2 = p42.E - p42.f2
    let tail15LB = exp(p42.logA - tail15EMinusF2 / 15.0)
    let tail15UB = exp((2.0 / 3.0) * log(8.0 * kCycle5Pi * kCycle5Pi) + (2.0 / 45.0) * log(9.0 / 4.0))

    var grid = [PoitouPoint]()
    grid.reserveCapacity(231)
    for i in 0...230 {
        grid.append(evalPoitou(gl, b: 0.5 + 0.05 * Double(i)))
    }

    func ubLog(n: Int, u: Int, mode: Int) -> Double {
        let C: Double = (mode == 0) ? (4.5 * Double(u))
            : ((mode == 1) ? ((27.0 / 8.0) * Double(u)) : (2.0 * Double(u)))
        return (2.0 / 3.0) * log(4.0 * kCycle5Pi * kCycle5Pi) + (2.0 / (3.0 * Double(n))) * log(C)
    }

    var deg9To14Survivors: Int32 = 0
    var worstDeg9Margin = 1e9
    var worstDeg10Margin = 1e9
    var deg7MaxU: Int32 = 0
    var deg7Hge2: Int32 = 0
    var deg7MaxRD = 0.0
    var deg8MaxU: Int32 = 0
    var deg8Hge2: Int32 = 0
    var deg8MaxRD = 0.0
    var deg6MaxU: Int32 = 0
    var deg6U16H1Dead: Int32 = 0
    var deg6U16Hge2Dead: Int32 = 0
    var deg6U16H1Margin = -1e9
    var deg6U16Hge2Margin = -1e9
    let deg6OldDisc = exp(6.0 * ubLog(n: 6, u: 32, mode: 0))
    let deg6NewDisc = exp(6.0 * ubLog(n: 6, u: 8, mode: 0))

    for n in 6...14 {
        let modeStart = (n % 2 == 0) ? 0 : 1
        let modeEnd = (n % 2 == 0) ? 0 : 2
        let dn = Double(n)
        for mode in modeStart...modeEnd {
            for k in 0..<n {
                let u = 1 << k
                let ub = ubLog(n: n, u: u, mode: mode)
                let cf2F = (mode == 1 ? 2.0 : 1.0) / dn
                let lbF = bestLBGrid(grid, deg: dn, rho1: 1.0, coeffF2: cf2F, coeffF4: 0.0)

                var subH1 = -1e9
                if k >= 1 {
                    for j in 1...k {
                        var rho1 = 0.0
                        if j < k {
                            let num = Int64(n) * ((Int64(1) << (k - j)) - 1)
                            let den = (Int64(1) << k) - 1
                            let r1Min = (num + den - 1) / den
                            rho1 = Double(r1Min) / dn
                        }
                        let cf4 = (mode == 1 ? 2.0 : 1.0) / (2.0 * dn)
                        let val = bestLBGrid(grid, deg: dn * Double(1 << j), rho1: rho1, coeffF2: 0.0, coeffF4: cf4)
                        if val > subH1 { subH1 = val }
                    }
                }

                var lbH1 = lbF
                if k >= 1 {
                    let cf4Extra = (mode == 1) ? (1.0 / (2.0 * dn)) : 0.0
                    let b1 = bestLBGrid(grid, deg: dn * Double(u), rho1: 0.0, coeffF2: 1.0 / dn, coeffF4: cf4Extra)
                    let lbFv1 = max(lbF, max(b1, subH1))
                    let b2Lv = bestLBGrid(grid, deg: dn * Double(u / 2), rho1: 0.0, coeffF2: 1.0 / dn, coeffF4: cf4Extra)
                    let b2H = bestLBGrid(grid, deg: dn * Double(u), rho1: 0.0, coeffF2: 0.0, coeffF4: (mode == 1 ? 2.0 : 1.0) / (2.0 * dn))
                    let lbFv2 = max(lbF, max(b2Lv, max(b2H, subH1)))
                    lbH1 = min(lbFv1, lbFv2)
                }

                var lbH2 = lbF
                for j in 0...k {
                    var rho1 = 0.0
                    if j == 0 {
                        rho1 = 1.0
                    } else if j < k {
                        let num = Int64(n) * ((Int64(1) << (k - j)) - 1)
                        let den = (Int64(1) << k) - 1
                        let r1Min = (num + den - 1) / den
                        rho1 = Double(r1Min) / dn
                    }
                    let val = bestLBGrid(grid, deg: 2.0 * dn * Double(1 << j), rho1: rho1, coeffF2: 0.0, coeffF4: 0.0)
                    if val > lbH2 { lbH2 = val }
                }

                let m1 = exp(lbH1) - exp(ub)
                let m2 = exp(lbH2) - exp(ub)
                let dead1 = lbH1 > ub
                let dead2 = lbH2 > ub

                if n >= 9 {
                    if !dead1 || !dead2 { deg9To14Survivors += 1 }
                    if n == 9 { worstDeg9Margin = min(worstDeg9Margin, min(m1, m2)) }
                    if n == 10 { worstDeg10Margin = min(worstDeg10Margin, min(m1, m2)) }
                } else if n == 8 {
                    if !dead2 { deg8Hge2 += 1 }
                    if !dead1 || !dead2 {
                        deg8MaxU = max(deg8MaxU, Int32(u))
                        deg8MaxRD = max(deg8MaxRD, exp(ub))
                    }
                } else if n == 7 {
                    if !dead2 { deg7Hge2 += 1 }
                    if !dead1 || !dead2 {
                        deg7MaxU = max(deg7MaxU, Int32(u))
                        deg7MaxRD = max(deg7MaxRD, exp(ub))
                    }
                } else if n == 6 {
                    if u == 16 {
                        deg6U16H1Dead = dead1 ? 1 : 0
                        deg6U16Hge2Dead = dead2 ? 1 : 0
                        deg6U16H1Margin = m1
                        deg6U16Hge2Margin = m2
                    }
                    if !dead1 || !dead2 {
                        deg6MaxU = max(deg6MaxU, Int32(u))
                    }
                }
            }
        }
    }

    let passed = gl.selfCheckOK &&
        qExplicitLB <= 0.0 && qExplicitLB > -1e-4 &&
        tail15EMinusF2 > 0.0 && tail15LB > tail15UB &&
        deg9To14Survivors == 0 &&
        worstDeg9Margin > 0.30 &&
        worstDeg10Margin > 0.90 &&
        deg7MaxU == 4 && deg7Hge2 == 0 &&
        deg8MaxU == 4 && deg8Hge2 == 0 &&
        deg6MaxU == 8 &&
        deg6U16H1Dead == 1 && deg6U16Hge2Dead == 1 &&
        deg6U16H1Margin > 0.01 && deg6U16Hge2Margin > 0.30

    return TheoremDPincerReport(
        passed: passed,
        quadratureSelfCheckOK: gl.selfCheckOK,
        qExplicitFormulaLB: qExplicitLB,
        tail15LBb42: tail15LB,
        tail15UB: tail15UB,
        tail15EMinusF2: tail15EMinusF2,
        deg9To14Survivors: deg9To14Survivors,
        worstDeg9Margin: worstDeg9Margin,
        worstDeg10Margin: worstDeg10Margin,
        deg7MaxSurvivingU: deg7MaxU,
        deg7Hge2Survivors: deg7Hge2,
        deg7MaxRootDisc: deg7MaxRD,
        deg8MaxSurvivingU: deg8MaxU,
        deg8Hge2Survivors: deg8Hge2,
        deg8MaxRootDisc: deg8MaxRD,
        deg6MaxSurvivingU: deg6MaxU,
        deg6U16H1Dead: deg6U16H1Dead,
        deg6U16Hge2Dead: deg6U16Hge2Dead,
        deg6U16H1Margin: deg6U16H1Margin,
        deg6U16Hge2Margin: deg6U16Hge2Margin,
        deg6OldDiscCeiling: deg6OldDisc,
        deg6NewDiscCeiling: deg6NewDisc
    )
}

public func verifyShimuraGenus13Census() -> ShimuraGenus13Report {
    var oddPrimes = [Int64]()
    var p: Int64 = 3
    while p <= 1001 {
        if isPrime64(p) { oddPrimes.append(p) }
        p += 2
    }

    struct DCand {
        let D: Int64
        let phiD: Int64
        let e2D: Int64
        let e3D: Int64
    }
    var dCands = [DCand]()
    func genD(_ idx: Int, _ cnt: Int, _ D: Int64, _ phiD: Int64, _ e2D: Int64, _ e3D: Int64) {
        if cnt >= 2 && cnt % 2 == 0 {
            dCands.append(DCand(D: D, phiD: phiD, e2D: e2D, e3D: e3D))
        }
        for i in idx..<oddPrimes.count {
            let q = oddPrimes[i]
            if phiD * (q - 1) > 1000 { break }
            genD(i + 1, cnt + 1, D * q, phiD * (q - 1),
                 e2D * (1 - kroneckerNeg4(q)), e3D * (1 - kroneckerNeg3(q)))
        }
    }
    genD(0, 1, 2, 1, 1, 2)

    var totalPairs: Int32 = 0
    var torsionFreePairs: Int32 = 0
    var negE10Detected: Int32 = 0
    var negE10Phi: Int32 = 0
    var negE10E2: Int32 = 0
    var negE10E3: Int32 = 0

    for dc in dCands {
        let maxN = 1000 / dc.phiD
        var N: Int64 = 1
        while N <= maxN {
            if gcdLocal64(dc.D, N) == 1 {
                var tmp = N
                var psiN: Int64 = 1
                var e2N: Int64 = 1
                var e3N: Int64 = 1
                var q: Int64 = 3
                while q * q <= tmp {
                    if tmp % q == 0 {
                        var k = 0
                        var qkMinus1: Int64 = 1
                        while tmp % q == 0 {
                            if k >= 1 { qkMinus1 *= q }
                            tmp /= q
                            k += 1
                        }
                        psiN *= qkMinus1 * (q + 1)
                        e2N *= (1 + kroneckerNeg4(q))
                        e3N *= (q == 3) ? (k == 1 ? 1 : 0) : (1 + kroneckerNeg3(q))
                    }
                    q += 2
                }
                if tmp > 1 {
                    psiN *= (tmp + 1)
                    e2N *= (1 + kroneckerNeg4(tmp))
                    e3N *= (tmp == 3) ? 1 : (1 + kroneckerNeg3(tmp))
                }
                if dc.phiD * psiN <= 1000 {
                    let e2 = dc.e2D * e2N
                    let e3 = dc.e3D * e3N
                    if 12 + dc.phiD * psiN - 3 * e2 - 4 * e3 == 12 * 13 {
                        totalPairs += 1
                        if e2 == 0 && e3 == 0 { torsionFreePairs += 1 }
                        if dc.D == 690 && N == 1 {
                            negE10Detected = 1
                            negE10Phi = Int32(dc.phiD)
                            negE10E2 = Int32(e2)
                            negE10E3 = Int32(e3)
                        }
                    }
                }
            }
            N += 2
        }
    }

    var gammaHCount: Int32 = 0
    for dc in dCands {
        if 144 % dc.phiD != 0 { continue }
        var N: Int64 = 3
        while N <= 144 {
            if gcdLocal64(dc.D, N) == 1 {
                var tmp = N
                var psiN: Int64 = 1
                var phiN: Int64 = 1
                var q: Int64 = 3
                while q * q <= tmp {
                    if tmp % q == 0 {
                        var k = 0
                        var qkMinus1: Int64 = 1
                        while tmp % q == 0 {
                            if k >= 1 { qkMinus1 *= q }
                            tmp /= q
                            k += 1
                        }
                        psiN *= qkMinus1 * (q + 1)
                        phiN *= qkMinus1 * (q - 1)
                    }
                    q += 2
                }
                if tmp > 1 {
                    psiN *= (tmp + 1)
                    phiN *= (tmp - 1)
                }
                if 144 % (dc.phiD * psiN) == 0 {
                    let d = 144 / (dc.phiD * psiN)
                    if d >= 2 && (phiN / 2) % d == 0 {
                        gammaHCount += 1
                    }
                }
            }
            N += 2
        }
    }

    let passed = (totalPairs == 19 &&
                  torsionFreePairs == 11 &&
                  negE10Detected == 1 &&
                  negE10Phi == 176 &&
                  negE10E2 == 0 &&
                  negE10E3 == 8 &&
                  gammaHCount == 4)
    return ShimuraGenus13Report(
        passed: passed,
        totalPairs: totalPairs,
        torsionFreePairs: torsionFreePairs,
        negE10Detected: negE10Detected,
        negE10Phi: negE10Phi,
        negE10E2: negE10E2,
        negE10E3: negE10E3,
        gammaHCount: gammaHCount
    )
}

public func verifySection7ArithmeticCycle5() -> Section7ArithmeticCycle5Report {
    var quadSplit2Scanned: Int32 = 0
    var quadHplus1Solutions: Int32 = 0
    var quadD41Solutions: Int32 = 0
    var quadD137Solutions: Int32 = 0

    for D in Int64(5)...1200 {
        if !isFundamentalDisc(D) || D % 8 != 1 { continue }
        quadSplit2Scanned += 1
        var z60: Int64 = 0
        var b: Int64 = 1
        while b * b < D {
            z60 += 2 * sigma1Local((D - b * b) / 4)
            b += 2
        }
        if 1440 % z60 != 0 { continue }
        if narrowClassNumberQuad(D) != 1 { continue }
        let sols = countQuadDNSolutions(D, target: 1440 / z60)
        quadHplus1Solutions += sols
        if D == 41 { quadD41Solutions = sols }
        if D == 137 { quadD137Solutions = sols }
    }

    var pgl2Order: Int32 = 0
    var pgl2Ord3: Int32 = 0
    var pgl2Ord3Free: Int32 = 0
    for a: UInt8 in 0..<8 {
        for b: UInt8 in 0..<8 {
            for c: UInt8 in 0..<8 {
                for d: UInt8 in 0..<8 {
                    let det = f8Mul(a, d) ^ f8Mul(b, c)
                    if det == 0 { continue }
                    let lead: UInt8 = (a != 0) ? a : ((b != 0) ? b : ((c != 0) ? c : d))
                    if lead != 1 { continue }
                    pgl2Order += 1
                    let m = F8Mat2(a: a, b: b, c: c, d: d)
                    if f8IsScalar(m) { continue }
                    let m2 = f8MatMul(m, m)
                    let m3 = f8MatMul(m2, m)
                    if f8IsScalar(m3) {
                        pgl2Ord3 += 1
                        var fixed = false
                        for pt in 0..<9 {
                            if f8P1Act(m, pt) == pt {
                                fixed = true
                                break
                            }
                        }
                        if !fixed { pgl2Ord3Free += 1 }
                    }
                }
            }
        }
    }

    // Prop 7.3: Exact Int128 recurrence verifying tr(gamma_0^k)^2 > 4 * det(gamma_0^k) for k = 1..12.
    // Since det(gamma_0^k) = 256^k = (16^k)^2 and tk > 0, tk^2 > 4 * detK <=> tk > 2 * 16^k;
    // also verify tk^2 > 4 * detK directly for k <= 9 (max ~5.3e34 < Int128.max).
    var tPrev2: Int128 = 2
    var tPrev1: Int128 = 85
    var detK: Int128 = 256
    var sdetK: Int128 = 16
    var gamma0Obstructed: Int32 = 0
    for k in 1...12 {
        let tk: Int128 = (k == 1) ? tPrev1 : (85 * tPrev1 - 256 * tPrev2)
        if k >= 2 {
            tPrev2 = tPrev1
            tPrev1 = tk
            detK *= 256
            sdetK *= 16
        }
        var okK = (tk > 2 * sdetK)
        if k <= 9 {
            okK = okK && (tk * tk > 4 * detK)
        }
        if okK { gamma0Obstructed += 1 }
    }

    let passed = (quadHplus1Solutions == 3 &&
                  quadD41Solutions == 2 &&
                  quadD137Solutions == 1 &&
                  pgl2Order == 504 &&
                  pgl2Ord3 == 56 &&
                  pgl2Ord3Free == 56 &&
                  gamma0Obstructed == 12)

    return Section7ArithmeticCycle5Report(
        passed: passed,
        quadSplit2Scanned: quadSplit2Scanned,
        quadHplus1Solutions: quadHplus1Solutions,
        quadD41Solutions: quadD41Solutions,
        quadD137Solutions: quadD137Solutions,
        pgl2F8Order: pgl2Order,
        pgl2F8Order3Count: pgl2Ord3,
        pgl2F8Order3FreeCount: pgl2Ord3Free,
        gamma0PowersObstructed: gamma0Obstructed
    )
}
