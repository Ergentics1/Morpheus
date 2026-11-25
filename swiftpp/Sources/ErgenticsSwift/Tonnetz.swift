import Foundation

private let kPi = 3.141592653589793238462643383279502884
private let kRamanujan3 = 2.828427124746190097603377448419396157 // 2*sqrt(2)

public struct TriadMoveResult: Sendable, Equatable {
    public let targetVertex: Int32
    public let voiceStep: Int32
    public let arrivingPitch: Int32
    public let departingPitch: Int32
}

public struct WindingDistribution: Sendable, Equatable {
    public let lengthM: Int32
    public let wMin: Int32
    public let wMax: Int32
    public let totalClosedWalks: Int64
    public let totalPrimes: Int64
    public let nonMultiple12Closed: Int64
    public let closedCounts: [Int64] // 17 bins for w in -8...8
    public let primeCounts: [Int64]  // 17 bins for w in -8...8
}

public struct FluxWindowReport: Sendable, Equatable {
    public let edgeLow: Double
    public let edgeHigh: Double
    public let maxEigAtEdgeLow: Double
    public let maxEigAtPi: Double
    public let minEigAt2PiOver3: Double
    public let cyclicRamanujan: [Bool] // length 13, index n = 0...12
}

public struct TuneCheckReport: Sendable, Equatable {
    public let rootedPrimesChecked: Int64
    public let decodeFailures: Int64
    public let periodicTuneFailures: Int64
    public let lemmaL1: Bool
    public let lemmaL2: Bool
    public let lemmaL3: Bool
    public let backtrackCounterexampleConfirmed: Bool
}

public struct EDOComparisonReport: Sendable, Equatable {
    public let lambdaMax12: Double
    public let lambdaMax31: Double
    public let lambdaMax53: Double
    public let ramanujan12: Bool
    public let ramanujan31: Bool
    public let ramanujan53: Bool
}

/// First-principles 24-triad neo-Riemannian P(0), L(1), R(2) moves.
/// Vertices: 0..11 = Major(r), 12..23 = Minor(r), r in Z_12.
@inline(__always)
public func applyPLRMove(vertex: Int32, moveId: Int32) -> TriadMoveResult {
    let r = vertex % 12
    if vertex < 12 {
        if moveId == 0 {
            return TriadMoveResult(targetVertex: 12 + r, voiceStep: -1, arrivingPitch: (r + 3) % 12, departingPitch: (r + 4) % 12)
        } else if moveId == 1 {
            return TriadMoveResult(targetVertex: 12 + (r + 4) % 12, voiceStep: -1, arrivingPitch: (r + 11) % 12, departingPitch: r)
        } else {
            return TriadMoveResult(targetVertex: 12 + (r + 9) % 12, voiceStep: 2, arrivingPitch: (r + 9) % 12, departingPitch: (r + 7) % 12)
        }
    } else {
        if moveId == 0 {
            return TriadMoveResult(targetVertex: r, voiceStep: 1, arrivingPitch: (r + 4) % 12, departingPitch: (r + 3) % 12)
        } else if moveId == 1 {
            return TriadMoveResult(targetVertex: (r + 8) % 12, voiceStep: 1, arrivingPitch: (r + 8) % 12, departingPitch: (r + 7) % 12)
        } else {
            return TriadMoveResult(targetVertex: (r + 3) % 12, voiceStep: -2, arrivingPitch: (r + 10) % 12, departingPitch: r)
        }
    }
}

public func buildAdjacencyMatrix() -> [Double] {
    var a = [Double](repeating: 0.0, count: 576)
    for v: Int32 in 0..<24 {
        for m: Int32 in 0..<3 {
            let u = applyPLRMove(vertex: v, moveId: m).targetVertex
            a[Int(v) * 24 + Int(u)] = 1.0
        }
    }
    return a
}

public func buildLaplacianMatrix() -> [Double] {
    var l = buildAdjacencyMatrix().map { -$0 }
    for i in 0..<24 {
        l[i * 24 + i] += 3.0
    }
    return l
}

public func buildTonnetzGram() -> [Double] {
    func dot60(_ a1: Double, _ b1: Double, _ a2: Double, _ b2: Double) -> Double {
        a1 * a2 + b1 * b2 + 0.5 * (a1 * b2 + b1 * a2)
    }
    return [
        dot60(4.0, -4.0, 4.0, -4.0),
        dot60(4.0, -4.0, 0.0,  3.0),
        dot60(0.0,  3.0, 4.0, -4.0),
        dot60(0.0,  3.0, 0.0,  3.0),
    ]
}

public func buildTonnetzCovariancePerStep() -> [Double] {
    let g = buildTonnetzGram()
    let det = g[0] * g[3] - g[1] * g[2]
    return [
         0.5 * g[3] / det,
        -0.5 * g[1] / det,
        -0.5 * g[2] / det,
         0.5 * g[0] / det,
    ]
}

public func buildTwistedAdjacencyComplex(phi: Double) -> [Double] {
    var out = [Double](repeating: 0.0, count: 2 * 576)
    let theta = phi / 12.0
    for v: Int32 in 0..<24 {
        for m: Int32 in 0..<3 {
            let mv = applyPLRMove(vertex: v, moveId: m)
            let ang = theta * Double(mv.voiceStep)
            let idx = 2 * (Int(v) * 24 + Int(mv.targetVertex))
            out[idx] = cos(ang)
            out[idx + 1] = sin(ang)
        }
    }
    return out
}

public func twistedMaxEigenvalue(_ phi: Double) -> Double {
    var best = 0.0
    for k in 0..<12 {
        let a1 = 2.0 * kPi * (4.0 * Double(k)) / 12.0
        let a2 = 2.0 * kPi * (9.0 * Double(k)) / 12.0 + phi / 4.0
        let re = 1.0 + cos(a1) + cos(a2)
        let im = sin(a1) + sin(a2)
        let mag = hypot(re, im)
        if mag > best { best = mag }
    }
    return best
}

public func evaluateFluxWindow() -> FluxWindowReport {
    let edgeLow = 4.0 * acos(0.75)
    let edgeHigh = 2.0 * kPi - edgeLow
    let maxAtLow = twistedMaxEigenvalue(edgeLow)
    let maxAtPi = twistedMaxEigenvalue(kPi)

    var minDirac = 1e9
    let phiDirac = 2.0 * kPi / 3.0
    for k in 0..<12 {
        let a1 = 2.0 * kPi * (4.0 * Double(k)) / 12.0
        let a2 = 2.0 * kPi * (9.0 * Double(k)) / 12.0 + phiDirac / 4.0
        let mag = hypot(1.0 + cos(a1) + cos(a2), sin(a1) + sin(a2))
        if mag < minDirac { minDirac = mag }
    }

    var cyc = [Bool](repeating: false, count: 13)
    for n in 1...12 {
        var ok = true
        if n > 1 {
            for j in 1..<n {
                let phi = 2.0 * kPi * Double(j) / Double(n)
                if twistedMaxEigenvalue(phi) > kRamanujan3 + 1e-12 {
                    ok = false
                    break
                }
            }
        }
        cyc[n] = ok
    }
    return FluxWindowReport(
        edgeLow: edgeLow,
        edgeHigh: edgeHigh,
        maxEigAtEdgeLow: maxAtLow,
        maxEigAtPi: maxAtPi,
        minEigAt2PiOver3: minDirac,
        cyclicRamanujan: cyc
    )
}

private func detLU(_ input: [Double], n: Int) -> Double {
    var m = input
    var sign = 1.0
    for k in 0..<n {
        var piv = k
        var best = abs(m[k * n + k])
        if k + 1 < n {
            for i in (k + 1)..<n {
                let v = abs(m[i * n + k])
                if v > best {
                    best = v
                    piv = i
                }
            }
        }
        if best == 0.0 { return 0.0 }
        if piv != k {
            for j in k..<n {
                m.swapAt(k * n + j, piv * n + j)
            }
            sign = -sign
        }
        let diag = m[k * n + k]
        if k + 1 < n {
            for i in (k + 1)..<n {
                let f = m[i * n + k] / diag
                for j in (k + 1)..<n {
                    m[i * n + j] -= f * m[k * n + j]
                }
            }
        }
    }
    var det = sign
    for i in 0..<n { det *= m[i * n + i] }
    return det
}

public func iharaBassResidual(u: Double) -> Double {
    var ib = [Double](repeating: 0.0, count: 72 * 72)
    for e in 0..<72 {
        ib[e * 72 + e] = 1.0
        let v = Int32(e / 3)
        let m = Int32(e % 3)
        let to = Int(applyPLRMove(vertex: v, moveId: m).targetVertex)
        for m2 in 0..<3 {
            if Int32(m2) == m { continue }
            let e2 = 3 * to + m2
            ib[e * 72 + e2] -= u
        }
    }
    let lhs = detLU(ib, n: 72)

    let adj = buildAdjacencyMatrix()
    var bass = [Double](repeating: 0.0, count: 24 * 24)
    for i in 0..<24 {
        for j in 0..<24 {
            bass[i * 24 + j] = -u * adj[i * 24 + j]
        }
        bass[i * 24 + i] += 1.0 + 2.0 * u * u
    }
    let rhs = pow(1.0 - u * u, 12.0) * detLU(bass, n: 24)
    return abs(lhs - rhs)
}

public func computeExactWindingDistribution(m: Int32) -> WindingDistribution {
    let wMin: Int32 = -8
    let wMax: Int32 = 8
    let zeros = [Int64](repeating: 0, count: 17)
    if m < 2 || m > 40 || (m % 2) != 0 {
        return WindingDistribution(lengthM: m, wMin: wMin, wMax: wMax, totalClosedWalks: 0, totalPrimes: 0, nonMultiple12Closed: 0, closedCounts: zeros, primeCounts: zeros)
    }

    var succ0 = [Int](repeating: 0, count: 72)
    var succ1 = [Int](repeating: 0, count: 72)
    var stepS = [Int](repeating: 0, count: 72)
    for v: Int32 in 0..<24 {
        for mv: Int32 in 0..<3 {
            let e = Int(3 * v + mv)
            let r = applyPLRMove(vertex: v, moveId: mv)
            stepS[e] = Int(r.voiceStep)
            var idx = 0
            for mv2: Int32 in 0..<3 where mv2 != mv {
                let targetEdge = Int(3 * r.targetVertex + mv2)
                if idx == 0 { succ0[e] = targetEdge } else { succ1[e] = targetEdge }
                idx += 1
            }
        }
    }

    let mInt = Int(m)
    let maxS = 2 * mInt
    let strideLen = 2 * maxS + 1
    let offset = maxS
    var nDW = [[Int64]](repeating: [Int64](repeating: 0, count: 17), count: mInt + 1)
    var nTotal = [Int64](repeating: 0, count: mInt + 1)
    var badMod12: Int64 = 0

    var cur = [Int64](repeating: 0, count: 72 * strideLen)
    var nxt = [Int64](repeating: 0, count: 72 * strideLen)

    for e0 in 0..<72 {
        cur.withUnsafeMutableBufferPointer { buf in
            buf.initialize(repeating: 0)
        }
        cur[e0 * strideLen + (offset + stepS[e0])] = 1

        for d in 2...mInt {
            nxt.withUnsafeMutableBufferPointer { buf in
                buf.initialize(repeating: 0)
            }
            let sLim = 2 * (d - 1)
            for e in 0..<72 {
                let base = e * strideLen
                let e1 = succ0[e]
                let e2 = succ1[e]
                let ds1 = stepS[e1]
                let ds2 = stepS[e2]
                let base1 = e1 * strideLen
                let base2 = e2 * strideLen
                for s in (-sLim)...sLim {
                    let cnt = cur[base + offset + s]
                    if cnt == 0 { continue }
                    nxt[base1 + offset + s + ds1] += cnt
                    nxt[base2 + offset + s + ds2] += cnt
                }
            }
            swap(&cur, &nxt)

            if d % 2 == 0 {
                let sLimD = 2 * d
                for e in 0..<72 {
                    if succ0[e] != e0 && succ1[e] != e0 { continue }
                    let base = e * strideLen
                    for s in (-sLimD)...sLimD {
                        let cnt = cur[base + offset + s]
                        if cnt == 0 { continue }
                        if s % 12 != 0 {
                            badMod12 += cnt
                        } else {
                            let w = s / 12
                            nDW[d][w - Int(wMin)] += cnt
                            nTotal[d] += cnt
                        }
                    }
                }
            }
        }
    }

    var primeCounts = [Int64](repeating: 0, count: 17)
    var totalPi: Int64 = 0
    for w in Int(wMin)...Int(wMax) {
        var acc: Int64 = 0
        for d in stride(from: 2, through: mInt, by: 2) {
            if mInt % d != 0 { continue }
            let k = mInt / d
            if w % k != 0 { continue }
            let mu = mobiusMu(Int32(k))
            if mu == 0 { continue }
            let w0 = w / k
            acc += Int64(mu) * nDW[d][w0 - Int(wMin)]
        }
        let piMW = acc / Int64(mInt)
        primeCounts[w - Int(wMin)] = piMW
        totalPi += piMW
    }

    return WindingDistribution(
        lengthM: m,
        wMin: wMin,
        wMax: wMax,
        totalClosedWalks: nTotal[mInt],
        totalPrimes: totalPi,
        nonMultiple12Closed: badMod12,
        closedCounts: nDW[mInt],
        primeCounts: primeCounts
    )
}

private func triadNotes(_ v: Int32) -> (Int32, Int32, Int32) {
    let r = v % 12
    if v < 12 {
        return (r, (r + 4) % 12, (r + 7) % 12)
    }
    return (r, (r + 3) % 12, (r + 7) % 12)
}

private func triadFromNotes(_ a: Int32, _ b: Int32, _ c: Int32) -> Int32 {
    if a == b || b == c || a == c { return -1 }
    let mask: UInt32 = (1 << a) | (1 << b) | (1 << c)
    for v: Int32 in 0..<24 {
        let ns = triadNotes(v)
        let vm: UInt32 = (1 << ns.0) | (1 << ns.1) | (1 << ns.2)
        if vm == mask { return v }
    }
    return -1
}

public func verifyTuneTheorem(maxLen: Int32) -> TuneCheckReport {
    var l1 = true
    var l2 = true
    var l3 = true

    for v: Int32 in 0..<24 {
        let ns = triadNotes(v)
        let arr = [ns.0, ns.1, ns.2]
        for i in 0..<3 {
            for j in (i + 1)..<3 {
                var d = abs(arr[i] - arr[j])
                d = min(d, 12 - d)
                if d == 1 || d == 2 { l3 = false }
            }
        }
        var dep = [Int32](repeating: 0, count: 3)
        for mv: Int32 in 0..<3 {
            let r = applyPLRMove(vertex: v, moveId: mv)
            dep[Int(mv)] = r.departingPitch
            let st = abs(r.voiceStep)
            if st != 1 && st != 2 { l3 = false }
            for mv2: Int32 in 0..<3 {
                let r2 = applyPLRMove(vertex: r.targetVertex, moveId: mv2)
                if mv2 == mv {
                    if r2.departingPitch != r.arrivingPitch { l2 = false }
                } else {
                    if r2.departingPitch == r.arrivingPitch { l2 = false }
                }
            }
        }
        if dep[0] == dep[1] || dep[1] == dep[2] || dep[0] == dep[2] { l1 = false }
    }

    let cToCm = applyPLRMove(vertex: 0, moveId: 0)
    let cmToC = applyPLRMove(vertex: 12, moveId: 0)
    let eToAbm = applyPLRMove(vertex: 4, moveId: 1)
    let abmToE = applyPLRMove(vertex: 20, moveId: 1)
    let negM4Confirmed = (cToCm.arrivingPitch == 3 && cmToC.arrivingPitch == 4 &&
                          eToAbm.arrivingPitch == 3 && abmToE.arrivingPitch == 4)

    func decodeTune(_ tune: [Int32]) -> [Int32]? {
        let m = tune.count
        var out = [Int32](repeating: -1, count: m)
        var anyThree = false
        for i in 0..<m {
            let a = tune[(i - 2 + m) % m]
            let b = tune[(i - 1 + m) % m]
            let c = tune[i]
            let t = triadFromNotes(a, b, c)
            if t >= 0 {
                out[i] = t
                anyThree = true
            }
        }
        if !anyThree {
            var held: Int32 = -1
            var matches = 0
            for h: Int32 in 0..<12 {
                var ok = true
                for i in 0..<m {
                    if triadFromNotes(tune[(i - 1 + m) % m], tune[i], h) < 0 {
                        ok = false
                        break
                    }
                }
                if ok {
                    held = h
                    matches += 1
                }
            }
            if matches != 1 { return nil }
            for i in 0..<m {
                out[i] = triadFromNotes(tune[(i - 1 + m) % m], tune[i], held)
            }
            return out
        }
        var start = 0
        while out[start] < 0 { start += 1 }
        for step in 1..<m {
            let idx = (start + step) % m
            if out[idx] >= 0 { continue }
            let prevV = out[(idx - 1 + m) % m]
            let arr = tune[idx]
            var nextV: Int32 = -1
            for mv: Int32 in 0..<3 {
                let r = applyPLRMove(vertex: prevV, moveId: mv)
                if r.arrivingPitch == arr {
                    nextV = r.targetVertex
                    break
                }
            }
            if nextV < 0 { return nil }
            out[idx] = nextV
        }
        return out
    }

    func isPrimitive(_ seq: [Int32]) -> Bool {
        let m = seq.count
        for d in 1..<m where m % d == 0 {
            var per = true
            for i in 0..<m {
                if seq[i] != seq[i % d] {
                    per = false
                    break
                }
            }
            if per { return false }
        }
        return true
    }

    var checked: Int64 = 0
    var decodeFail: Int64 = 0
    var periodicFail: Int64 = 0

    if maxLen >= 6 {
        for targetM in stride(from: 6, through: Int(maxLen), by: 2) {
            var chords = [Int32](repeating: 0, count: targetM)
            var tune = [Int32](repeating: 0, count: targetM)
            for startV: Int32 in 0..<24 {
                func dfs(depth: Int, curV: Int32, lastMv: Int32, firstMv: Int32) {
                    if depth == targetM {
                        if curV != startV || lastMv == firstMv { return }
                        if !isPrimitive(chords) { return }
                        checked += 1
                        if !isPrimitive(tune) { periodicFail += 1 }
                        if let dec = decodeTune(tune), dec == chords {
                            // OK
                        } else {
                            decodeFail += 1
                        }
                        return
                    }
                    for mv: Int32 in 0..<3 {
                        if depth > 0 && mv == lastMv { continue }
                        let r = applyPLRMove(vertex: curV, moveId: mv)
                        chords[depth] = r.targetVertex
                        tune[depth] = r.arrivingPitch
                        dfs(depth: depth + 1, curV: r.targetVertex, lastMv: mv, firstMv: depth == 0 ? mv : firstMv)
                    }
                }
                dfs(depth: 0, curV: startV, lastMv: -1, firstMv: -1)
            }
        }
    }

    return TuneCheckReport(
        rootedPrimesChecked: checked,
        decodeFailures: decodeFail,
        periodicTuneFailures: periodicFail,
        lemmaL1: l1,
        lemmaL2: l2,
        lemmaL3: l3,
        backtrackCounterexampleConfirmed: negM4Confirmed
    )
}

public func evaluateEDORamanujanComparison() -> EDOComparisonReport {
    func maxNontrivialEDO(_ n: Int, _ a: Int, _ b: Int) -> Double {
        var best = 0.0
        for k in 1..<n {
            let t1 = 2.0 * kPi * Double(a * k) / Double(n)
            let t2 = 2.0 * kPi * Double(b * k) / Double(n)
            let mag = hypot(1.0 + cos(t1) + cos(t2), sin(t1) + sin(t2))
            if mag > best { best = mag }
        }
        return best
    }
    let l12 = maxNontrivialEDO(12, 4, 7)
    let l31 = maxNontrivialEDO(31, 10, 18)
    let l53 = maxNontrivialEDO(53, 17, 31)
    return EDOComparisonReport(
        lambdaMax12: l12,
        lambdaMax31: l31,
        lambdaMax53: l53,
        ramanujan12: l12 <= kRamanujan3,
        ramanujan31: l31 <= kRamanujan3,
        ramanujan53: l53 <= kRamanujan3
    )
}

public func runSigningCensusExact() -> SigningCensusReport {
    struct Edge { let maj: Int; let min: Int; let step: Int }
    var edges = [Edge]()
    edges.reserveCapacity(36)
    for u: Int32 in 0..<12 {
        for mv: Int32 in 0..<3 {
            let r = applyPLRMove(vertex: u, moveId: mv)
            edges.append(Edge(maj: Int(u), min: Int(r.targetVertex), step: Int(r.voiceStep)))
        }
    }

    var visited = [Bool](repeating: false, count: 24)
    var parent = [Int](repeating: -1, count: 24)
    var parentStep = [Int](repeating: 0, count: 24)
    var inTree = [Bool](repeating: false, count: 36)
    var queue = [0]
    visited[0] = true
    var qi = 0
    while qi < queue.count {
        let x = queue[qi]
        qi += 1
        for ei in 0..<36 {
            let y: Int
            let st: Int
            if edges[ei].maj == x {
                y = edges[ei].min
                st = edges[ei].step
            } else if edges[ei].min == x {
                y = edges[ei].maj
                st = -edges[ei].step
            } else {
                continue
            }
            if !visited[y] {
                visited[y] = true
                parent[y] = x
                parentStep[y] = st
                inTree[ei] = true
                queue.append(y)
            }
        }
    }

    func treeSumFromRoot(_ start: Int) -> Int {
        var node = start
        var acc = 0
        while node != 0 {
            acc += parentStep[node]
            node = parent[node]
        }
        return acc
    }

    var chordEdges = [Int]()
    var voiceParityMask: UInt32 = 0
    for ei in 0..<36 where !inTree[ei] {
        let bit = chordEdges.count
        chordEdges.append(ei)
        let cycSum = treeSumFromRoot(edges[ei].maj) + edges[ei].step - treeSumFromRoot(edges[ei].min)
        let w = cycSum / 12
        if (w & 1) != 0 {
            voiceParityMask |= (1 << bit)
        }
    }

    var maxEigs = [Double](repeating: 0.0, count: 8192)
    var ctc = [Double](repeating: 0.0, count: 144)
    var bestNontriv = 1e9
    var ramanujanCnt: Int64 = 0

    for mask: UInt32 in 0..<8192 {
        var cMat = [Double](repeating: 0.0, count: 144)
        for ei in 0..<36 {
            cMat[edges[ei].maj * 12 + (edges[ei].min - 12)] = 1.0
        }
        for b in 0..<13 {
            if (mask & (1 << b)) != 0 {
                let ei = chordEdges[b]
                cMat[edges[ei].maj * 12 + (edges[ei].min - 12)] = -1.0
            }
        }
        for i in 0..<12 {
            for j in i..<12 {
                var s = 0.0
                for k in 0..<12 {
                    s += cMat[k * 12 + i] * cMat[k * 12 + j]
                }
                ctc[i * 12 + j] = s
                ctc[j * 12 + i] = s
            }
        }
        let eigs = jacobiEigenvalues(ctc, n: 12) ?? [0.0]
        let mx = sqrt(max(0.0, eigs[eigs.count - 1]))
        maxEigs[Int(mask)] = mx
        if mask != 0 {
            if mx <= kRamanujan3 + 1e-11 { ramanujanCnt += 1 }
            if mx < bestNontriv { bestNontriv = mx }
        }
    }

    let vpEig = maxEigs[Int(voiceParityMask)]
    var strictlySmaller: Int64 = 0
    for mask in 0..<8192 where maxEigs[mask] < vpEig - 1e-9 {
        strictlySmaller += 1
    }
    let passed = (ramanujanCnt == 7675) &&
                 (strictlySmaller == 7372) &&
                 (abs(bestNontriv - (1.0 + sqrt(2.0))) < 1e-9) &&
                 (abs(vpEig - sqrt(5.0 + 2.0 * sqrt(2.0))) < 1e-9)

    return SigningCensusReport(
        totalClasses: 8192,
        nontrivialClasses: 8191,
        ramanujanNontrivial: ramanujanCnt,
        voiceParityRank: strictlySmaller,
        bestMaxEig: bestNontriv,
        voiceParityMaxEig: vpEig,
        passed: passed
    )
}

public func runWindingNullRCT(m: Int32, key: PRNGKey, nWalks: Int64) -> WindingNullRCTReport {
    if m < 6 || m > 40 || (m % 2) != 0 || nWalks <= 0 {
        return WindingNullRCTReport(lengthM: m, totalWalksSampled: nWalks, closedWalksObserved: 0, nonMultiple12Observed: 0, mcVsExactClosedTV: 0, exactClosedVsPrimeTV: 0, mcMean: 0, mcVariance: 0, passed: false)
    }

    var succ0 = [Int](repeating: 0, count: 72)
    var succ1 = [Int](repeating: 0, count: 72)
    var stepS = [Int](repeating: 0, count: 72)
    for v: Int32 in 0..<24 {
        for mv: Int32 in 0..<3 {
            let e = Int(3 * v + mv)
            let r = applyPLRMove(vertex: v, moveId: mv)
            stepS[e] = Int(r.voiceStep)
            var idx = 0
            for mv2: Int32 in 0..<3 where mv2 != mv {
                let targetEdge = Int(3 * r.targetVertex + mv2)
                if idx == 0 { succ0[e] = targetEdge } else { succ1[e] = targetEdge }
                idx += 1
            }
        }
    }

    var rng = KeyedPRNG(key: key)
    var hist = [Int64](repeating: 0, count: 17)
    var closedObs: Int64 = 0
    var badMod12: Int64 = 0
    let mInt = Int(m)

    for _ in 0..<nWalks {
        let e0 = Int(rng.nextBounded(72))
        var e = e0
        var s = stepS[e0]
        for _ in 1..<mInt {
            let branch = rng.nextBounded(2)
            e = (branch == 0) ? succ0[e] : succ1[e]
            s += stepS[e]
        }
        if succ0[e] == e0 || succ1[e] == e0 {
            closedObs += 1
            if s % 12 != 0 {
                badMod12 += 1
            } else {
                let w = s / 12
                if w >= -8 && w <= 8 { hist[w + 8] += 1 }
            }
        }
    }

    if closedObs == 0 {
        return WindingNullRCTReport(lengthM: m, totalWalksSampled: nWalks, closedWalksObserved: 0, nonMultiple12Observed: badMod12, mcVsExactClosedTV: 0, exactClosedVsPrimeTV: 0, mcMean: 0, mcVariance: 0, passed: false)
    }

    let exact = computeExactWindingDistribution(m: m)
    var tvMCClosed = 0.0
    var tvClosedPrime = 0.0
    var mean = 0.0
    var m2 = 0.0
    for i in 0..<17 {
        let pMC = Double(hist[i]) / Double(closedObs)
        let pClosed = Double(exact.closedCounts[i]) / Double(exact.totalClosedWalks)
        let pPrime = Double(exact.primeCounts[i]) / Double(exact.totalPrimes)
        tvMCClosed += abs(pMC - pClosed)
        tvClosedPrime += abs(pClosed - pPrime)
        let w = Double(i - 8)
        mean += pMC * w
        m2 += pMC * w * w
    }
    let mcTV = 0.5 * tvMCClosed
    let mobiusTV = 0.5 * tvClosedPrime
    let variance = m2 - mean * mean
    let passed = (badMod12 == 0) && (closedObs > 0) && (mcTV < 0.03)

    return WindingNullRCTReport(
        lengthM: m,
        totalWalksSampled: nWalks,
        closedWalksObserved: closedObs,
        nonMultiple12Observed: badMod12,
        mcVsExactClosedTV: mcTV,
        exactClosedVsPrimeTV: mobiusTV,
        mcMean: mean,
        mcVariance: variance,
        passed: passed
    )
}
