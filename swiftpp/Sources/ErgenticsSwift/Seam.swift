import Foundation

/// Guarded P -> R -> D seam contract preventing uncalibrated/OOD/indefinite estimates from driving deterministic kernels.
public enum SeamCode: Int32, Sendable, Equatable {
    case ok = 0
    case rejectNonFinite = 1
    case rejectUncalibratedTV = 2
    case rejectUncalibratedKurtosis = 3
    case rejectIndefiniteCov = 4
    case rejectOODFlux = 5
    case rejectInvariant = 6
}

public struct SeamPolicy: Sendable, Equatable {
    public let maxTV: Double
    public let maxAbsExcessKurtosis: Double
    public let minCovEigenvalue: Double
    public let fluxMin: Double
    public let fluxMax: Double

    public init(maxTV: Double, maxAbsExcessKurtosis: Double, minCovEigenvalue: Double, fluxMin: Double, fluxMax: Double) {
        self.maxTV = maxTV
        self.maxAbsExcessKurtosis = maxAbsExcessKurtosis
        self.minCovEigenvalue = minCovEigenvalue
        self.fluxMin = fluxMin
        self.fluxMax = fluxMax
    }
}

public struct SeamDecision: Sendable, Equatable {
    public let code: SeamCode
    public let allowed: Bool
    public let deterministicOutput: Double
    public let covLambdaMin: Double
}

public func guardedFluxKernelHandoff(
    calibration cal: Rung1CalibrationReport,
    cov2x2RowMajor: [Double],
    fluxPhi: Double,
    policy: SeamPolicy
) -> SeamDecision {
    if !fluxPhi.isFinite || !cal.totalVariation.isFinite || !cal.excessKurtosis.isFinite {
        return SeamDecision(code: .rejectNonFinite, allowed: false, deterministicOutput: 0.0, covLambdaMin: 0.0)
    }
    if cal.code != .ok {
        return SeamDecision(code: .rejectInvariant, allowed: false, deterministicOutput: 0.0, covLambdaMin: 0.0)
    }
    if cal.totalVariation > policy.maxTV {
        return SeamDecision(code: .rejectUncalibratedTV, allowed: false, deterministicOutput: 0.0, covLambdaMin: 0.0)
    }
    if abs(cal.excessKurtosis) > policy.maxAbsExcessKurtosis {
        return SeamDecision(code: .rejectUncalibratedKurtosis, allowed: false, deterministicOutput: 0.0, covLambdaMin: 0.0)
    }
    let covRep = checkSymmetricPD(cov2x2RowMajor, n: 2, symTol: 1e-12, pdTol: policy.minCovEigenvalue)
    if covRep.code != .ok {
        let code: SeamCode = (covRep.code == .nonFinite) ? .rejectNonFinite : .rejectIndefiniteCov
        return SeamDecision(code: code, allowed: false, deterministicOutput: 0.0, covLambdaMin: covRep.lambdaMin)
    }
    if fluxPhi < policy.fluxMin || fluxPhi > policy.fluxMax {
        return SeamDecision(code: .rejectOODFlux, allowed: false, deterministicOutput: 0.0, covLambdaMin: covRep.lambdaMin)
    }
    return SeamDecision(
        code: .ok,
        allowed: true,
        deterministicOutput: twistedMaxEigenvalue(fluxPhi),
        covLambdaMin: covRep.lambdaMin
    )
}
