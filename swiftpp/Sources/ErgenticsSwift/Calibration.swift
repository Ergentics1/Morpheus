import Foundation

/// Correspondence Principle evaluation inside a dimensionless regime.
public struct CorrespondenceCheck: Sendable, Equatable {
    public let deeperValue: Double
    public let olderValue: Double
    public let regimeParam: Double
    public let absError: Double
    public let relError: Double
    public let boundValue: Double
    public let finite: Bool
    public let withinBound: Bool
}

/// Full Rung-1 distributional calibration vector (beyond point estimates).
public struct Rung1CalibrationReport: Sendable, Equatable {
    public let code: InvariantCode
    public let totalVariation: Double
    public let klDivergence: Double
    public let ksDistance: Double
    public let wasserstein1: Double
    public let mean: Double
    public let variance: Double
    public let skewness: Double
    public let excessKurtosis: Double
    public let cov1Sigma: Double
    public let cov2Sigma: Double
    public let cov3Sigma: Double
    public let simplexError: Double

    public init(
        code: InvariantCode,
        totalVariation: Double,
        klDivergence: Double,
        ksDistance: Double,
        wasserstein1: Double,
        mean: Double,
        variance: Double,
        skewness: Double,
        excessKurtosis: Double,
        cov1Sigma: Double,
        cov2Sigma: Double,
        cov3Sigma: Double,
        simplexError: Double
    ) {
        self.code = code
        self.totalVariation = totalVariation
        self.klDivergence = klDivergence
        self.ksDistance = ksDistance
        self.wasserstein1 = wasserstein1
        self.mean = mean
        self.variance = variance
        self.skewness = skewness
        self.excessKurtosis = excessKurtosis
        self.cov1Sigma = cov1Sigma
        self.cov2Sigma = cov2Sigma
        self.cov3Sigma = cov3Sigma
        self.simplexError = simplexError
    }
}

/// RCT-2 paired treatment-vs-control summary for Lemma 7.14 (2-adic edge-length doubling).
public struct TwoAdicRCTReport: Sendable, Equatable {
    public let treatmentSamples: Int64
    public let treatmentSlope2Hits: Int64
    public let controlSamples: Int64
    public let controlSlope1Hits: Int64
    public let passed: Bool
}

/// RCT-1 signing census summary (Remark 5.4: voice-parity vs all 8191 nontrivial signings).
public struct SigningCensusReport: Sendable, Equatable {
    public let totalClasses: Int64
    public let nontrivialClasses: Int64
    public let ramanujanNontrivial: Int64
    public let voiceParityRank: Int64
    public let bestMaxEig: Double
    public let voiceParityMaxEig: Double
    public let passed: Bool
}

/// RCT-3 keyed Monte Carlo non-backtracking walk null vs exact closed-walk & prime-cadence laws.
public struct WindingNullRCTReport: Sendable, Equatable {
    public let lengthM: Int32
    public let totalWalksSampled: Int64
    public let closedWalksObserved: Int64
    public let nonMultiple12Observed: Int64
    public let mcVsExactClosedTV: Double
    public let exactClosedVsPrimeTV: Double
    public let mcMean: Double
    public let mcVariance: Double
    public let passed: Bool
}

public func evaluateCorrespondence(
    deeperValue: Double, olderValue: Double, regimeParam: Double, boundValue: Double
) -> CorrespondenceCheck {
    let finite = deeperValue.isFinite && olderValue.isFinite && regimeParam.isFinite && boundValue.isFinite && boundValue >= 0.0
    if !finite {
        return CorrespondenceCheck(
            deeperValue: deeperValue, olderValue: olderValue, regimeParam: regimeParam,
            absError: .nan, relError: .nan, boundValue: boundValue, finite: false, withinBound: false
        )
    }
    let absErr = abs(deeperValue - olderValue)
    let denom = abs(olderValue)
    let relErr = denom > 0.0 ? absErr / denom : absErr
    return CorrespondenceCheck(
        deeperValue: deeperValue, olderValue: olderValue, regimeParam: regimeParam,
        absError: absErr, relError: relErr, boundValue: boundValue, finite: true, withinBound: absErr <= boundValue
    )
}

public func evaluateDiscreteGaussianCalibration(
    probs: [Double], wMin: Int32, sigma2: Double
) -> Rung1CalibrationReport {
    if !sigma2.isFinite || sigma2 <= 0.0 {
        return Rung1CalibrationReport(code: .outOfDomain, totalVariation: 0, klDivergence: 0, ksDistance: 0, wasserstein1: 0, mean: 0, variance: 0, skewness: 0, excessKurtosis: 0, cov1Sigma: 0, cov2Sigma: 0, cov3Sigma: 0, simplexError: 0)
    }
    let sim = checkProbabilitySimplex(probs, sumTol: 1e-12)
    if sim.code != .ok {
        return Rung1CalibrationReport(code: sim.code, totalVariation: 0, klDivergence: 0, ksDistance: 0, wasserstein1: 0, mean: 0, variance: 0, skewness: 0, excessKurtosis: 0, cov1Sigma: 0, cov2Sigma: 0, cov3Sigma: 0, simplexError: sim.absError)
    }

    let n = probs.count
    let wMax = wMin + Int32(n) - 1
    let extLo = min(wMin, -12) - 12
    let extHi = max(wMax, 12) + 12
    var zNorm = 0.0
    for w in extLo...extHi {
        let wd = Double(w)
        zNorm += exp(-0.5 * wd * wd / sigma2)
    }

    var q = [Double](repeating: 0.0, count: n)
    for i in 0..<n {
        let w = Double(wMin + Int32(i))
        q[i] = exp(-0.5 * w * w / sigma2) / zNorm
    }
    let qMassInside = sumNeumaier(q)
    let qTailOutside = max(0.0, 1.0 - qMassInside)

    var tvSum = qTailOutside
    var kl = 0.0
    var cdfP = 0.0
    var cdfQ = 0.5 * qTailOutside
    var ks = cdfQ
    var w1 = 0.0
    for i in 0..<n {
        let pi = probs[i]
        let qi = q[i]
        tvSum += abs(pi - qi)
        if pi > 0.0 {
            kl += pi * log(pi / qi)
        }
        cdfP += pi
        cdfQ += qi
        let diff = abs(cdfP - cdfQ)
        if diff > ks { ks = diff }
        if i + 1 < n { w1 += diff }
    }

    var mean = 0.0
    for i in 0..<n {
        mean += probs[i] * Double(wMin + Int32(i))
    }
    var m2 = 0.0
    var m3 = 0.0
    var m4 = 0.0
    for i in 0..<n {
        let d = Double(wMin + Int32(i)) - mean
        let d2 = d * d
        m2 += probs[i] * d2
        m3 += probs[i] * d2 * d
        m4 += probs[i] * d2 * d2
    }
    let sigma = sqrt(max(0.0, m2))
    var skew = 0.0
    var exKurt = 0.0
    var c1 = 0.0
    var c2 = 0.0
    var c3 = 0.0
    if sigma > 0.0 {
        skew = m3 / (sigma * sigma * sigma)
        exKurt = m4 / (m2 * m2) - 3.0
        for i in 0..<n {
            let ad = abs(Double(wMin + Int32(i)) - mean)
            if ad <= sigma { c1 += probs[i] }
            if ad <= 2.0 * sigma { c2 += probs[i] }
            if ad <= 3.0 * sigma { c3 += probs[i] }
        }
    }

    return Rung1CalibrationReport(
        code: .ok,
        totalVariation: 0.5 * tvSum,
        klDivergence: kl,
        ksDistance: ks,
        wasserstein1: w1,
        mean: mean,
        variance: m2,
        skewness: skew,
        excessKurtosis: exKurt,
        cov1Sigma: c1,
        cov2Sigma: c2,
        cov3Sigma: c3,
        simplexError: sim.absError
    )
}

internal func v2Int64(_ x: Int64) -> Int32 {
    if x == 0 { return 1_000_000 }
    var u: UInt64 = x < 0 ? UInt64(-x) : UInt64(x)
    var c: Int32 = 0
    while (u & 1) == 0 {
        u >>= 1
        c += 1
    }
    return c
}

/// Keyed-PRNG RCT-2 for Lemma 7.14: 2-adic slope doubling on fixed discs vs slope 1 controls.
public func runTwoAdicSlopeRCT(treatmentKey: PRNGKey, controlKey: PRNGKey, nSamples: Int64) -> TwoAdicRCTReport {
    if nSamples <= 0 {
        return TwoAdicRCTReport(treatmentSamples: 0, treatmentSlope2Hits: 0, controlSamples: 0, controlSlope1Hits: 0, passed: false)
    }

    var rngT = KeyedPRNG(key: treatmentKey)
    var treatSamples: Int64 = 0
    var treatHits: Int64 = 0
    for _ in 0..<nSamples {
        var num = Int64(rngT.nextBounded(999) + 1)
        let denExp = Int32(rngT.nextBounded(7))
        if rngT.nextBounded(2) == 1 { num = -num }
        let v2_2c = 1 + v2Int64(num) - denExp
        let k = v2_2c - 1 - Int32(rngT.nextBounded(4))
        let oddU = Int64(2 * rngT.nextBounded(6) + 1)
        let exp2c = 1 - denExp
        let minE = min(exp2c, k)
        let t2c = num << Int(exp2c - minE)
        let tU = oddU << Int(k - minE)
        let v2Sum = minE + v2Int64(t2c + tU)
        let v2Prod = k + v2Sum
        treatSamples += 1
        if v2Prod == 2 * k { treatHits += 1 }
    }

    var rngC = KeyedPRNG(key: controlKey)
    var ctrlSamples: Int64 = 0
    var ctrlHits: Int64 = 0
    for _ in 0..<nSamples {
        let num = Int64(rngC.nextBounded(999) + 1)
        let denExp = Int32(rngC.nextBounded(7))
        let v2_2c = 1 + v2Int64(num) - denExp
        let k = v2_2c + 1 + Int32(rngC.nextBounded(4))
        let oddU = Int64(2 * rngC.nextBounded(4) + 1)
        let exp2c = 1 - denExp
        let minE = min(exp2c, k)
        let t2c = num << Int(exp2c - minE)
        let tU = oddU << Int(k - minE)
        let v2Sum = minE + v2Int64(t2c + tU)
        let v2Prod = k + v2Sum
        ctrlSamples += 1
        if v2Prod == v2_2c + k { ctrlHits += 1 }
    }

    return TwoAdicRCTReport(
        treatmentSamples: treatSamples,
        treatmentSlope2Hits: treatHits,
        controlSamples: ctrlSamples,
        controlSlope1Hits: ctrlHits,
        passed: treatHits == treatSamples && ctrlHits == ctrlSamples
    )
}
