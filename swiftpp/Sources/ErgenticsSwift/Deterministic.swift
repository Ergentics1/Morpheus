import Foundation

/// D-Type summation report comparing naive, reverse, Kahan, and Neumaier orders.
public struct SummationSweepResult: Sendable, Equatable {
    public let naiveForward: Double
    public let naiveReverse: Double
    public let kahan: Double
    public let neumaier: Double
    public let maxOrderSpread: Double
    public let allFinite: Bool
}

/// Exact Mobius function mu(n).
public func mobiusMu(_ n: Int32) -> Int32 {
    if n <= 0 { return 0 }
    var mu: Int32 = 1
    var x = n
    var p: Int32 = 2
    while p * p <= x {
        if x % p == 0 {
            x /= p
            if x % p == 0 { return 0 }
            mu = -mu
        }
        p += 1
    }
    if x > 1 { mu = -mu }
    return mu
}

/// Exact non-negative greatest common divisor.
public func gcdInt64(_ a: Int64, _ b: Int64) -> Int64 {
    var x = a < 0 ? -a : a
    var y = b < 0 ? -b : b
    while y != 0 {
        let t = x % y
        x = y
        y = t
    }
    return x
}

public func sumNaiveForward(_ xs: [Double]) -> Double {
    var s = 0.0
    for x in xs { s += x }
    return s
}

public func sumNaiveReverse(_ xs: [Double]) -> Double {
    var s = 0.0
    for i in stride(from: xs.count - 1, through: 0, by: -1) {
        s += xs[i]
    }
    return s
}

public func sumKahan(_ xs: [Double]) -> Double {
    var sum = 0.0
    var c = 0.0
    for x in xs {
        let y = x - c
        let t = sum + y
        c = (t - sum) - y
        sum = t
    }
    return sum
}

public func sumNeumaier(_ xs: [Double]) -> Double {
    var sum = 0.0
    var c = 0.0
    for x in xs {
        let t = sum + x
        if abs(sum) >= abs(x) {
            c += (sum - t) + x
        } else {
            c += (x - t) + sum
        }
        sum = t
    }
    return sum + c
}

public func runSummationSweep(_ xs: [Double]) -> SummationSweepResult {
    let finite = allFinite(xs)
    let nf = sumNaiveForward(xs)
    let nr = sumNaiveReverse(xs)
    let kh = sumKahan(xs)
    let nm = sumNeumaier(xs)
    let vals = [nf, nr, kh, nm]
    var lo = vals[0]
    var hi = vals[0]
    for v in vals.dropFirst() {
        if v < lo { lo = v }
        if v > hi { hi = v }
    }
    return SummationSweepResult(
        naiveForward: nf,
        naiveReverse: nr,
        kahan: kh,
        neumaier: nm,
        maxOrderSpread: hi - lo,
        allFinite: finite
    )
}
