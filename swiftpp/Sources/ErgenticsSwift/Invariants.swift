import Foundation

/// Status codes for R-Type global runtime invariant guards.
public enum InvariantCode: Int32, Sendable, Equatable {
    case ok = 0
    case emptyInput = 1
    case nonFinite = 2
    case notSymmetric = 3
    case notPositiveDefinite = 4
    case choleskyFailed = 5
    case notPSD = 6
    case wrongNullity = 7
    case conservationViolation = 8
    case negativeProbability = 9
    case outOfDomain = 10
}

public struct MatrixInvariantReport: Sendable, Equatable {
    public let code: InvariantCode
    public let allFinite: Bool
    public let diagonalPositive: Bool
    public let symmetric: Bool
    public let choleskyOK: Bool
    public let maxAsymmetry: Double
    public let lambdaMin: Double
    public let lambdaMax: Double
    public let zeroEigenvalueCount: Int32
}

public struct ConservationReport: Sendable, Equatable {
    public let code: InvariantCode
    public let allFinite: Bool
    public let allNonNegative: Bool
    public let sumValue: Double
    public let absError: Double
}

public struct ExactConservationReport: Sendable, Equatable {
    public let code: InvariantCode
    public let allNonNegative: Bool
    public let sumValue: Int64
    public let expectedSum: Int64
}

public func allFinite(_ xs: [Double]) -> Bool {
    for x in xs where !x.isFinite { return false }
    return true
}

/// Cyclic Jacobi eigensolver for real symmetric n x n matrices (row-major).
internal func jacobiEigenvalues(_ input: [Double], n: Int) -> [Double]? {
    if n == 0 || input.count != n * n { return nil }
    if !allFinite(input) { return nil }
    var a = input
    let maxSweeps = 120
    for _ in 0..<maxSweeps {
        var offNorm = 0.0
        for p in 0..<n {
            for q in (p + 1)..<n {
                let apq = a[p * n + q]
                offNorm += apq * apq
            }
        }
        if sqrt(2.0 * offNorm) <= 1e-13 { break }

        for p in 0..<n {
            for q in (p + 1)..<n {
                let apq = a[p * n + q]
                if abs(apq) <= 1e-16 { continue }
                let app = a[p * n + p]
                let aqq = a[q * n + q]
                let tau = (aqq - app) / (2.0 * apq)
                let t = tau >= 0.0
                    ? (1.0 / (tau + sqrt(1.0 + tau * tau)))
                    : (-1.0 / (-tau + sqrt(1.0 + tau * tau)))
                let c = 1.0 / sqrt(1.0 + t * t)
                let s = t * c

                a[p * n + p] = app - t * apq
                a[q * n + q] = aqq + t * apq
                a[p * n + q] = 0.0
                a[q * n + p] = 0.0

                for r in 0..<n {
                    if r == p || r == q { continue }
                    let arp = a[r * n + p]
                    let arq = a[r * n + q]
                    let nrp = c * arp - s * arq
                    let nrq = s * arp + c * arq
                    a[r * n + p] = nrp
                    a[p * n + r] = nrp
                    a[r * n + q] = nrq
                    a[q * n + r] = nrq
                }
            }
        }
    }
    var eigs = [Double](repeating: 0.0, count: n)
    for i in 0..<n {
        let v = a[i * n + i]
        if !v.isFinite { return nil }
        eigs[i] = v
    }
    eigs.sort()
    return eigs
}

internal func choleskyPDCheck(_ a: [Double], n: Int, pdTol: Double) -> Bool {
    var l = [Double](repeating: 0.0, count: n * n)
    for i in 0..<n {
        for j in 0...i {
            var sum = 0.0
            for k in 0..<j {
                sum += l[i * n + k] * l[j * n + k]
            }
            if i == j {
                let d = a[i * n + i] - sum
                if !d.isFinite || d <= pdTol { return false }
                l[i * n + j] = sqrt(d)
            } else {
                let val = (a[i * n + j] - sum) / l[j * n + j]
                if !val.isFinite { return false }
                l[i * n + j] = val
            }
        }
    }
    return true
}

/// R-Type global PD verification: rejects NaN/Inf, asymmetry, negative eigenvalues, and Cholesky failures.
public func checkSymmetricPD(_ a: [Double], n: Int, symTol: Double = 1e-12, pdTol: Double = 1e-12) -> MatrixInvariantReport {
    if n == 0 || a.count != n * n {
        return MatrixInvariantReport(code: .emptyInput, allFinite: false, diagonalPositive: false, symmetric: false, choleskyOK: false, maxAsymmetry: 0, lambdaMin: 0, lambdaMax: 0, zeroEigenvalueCount: 0)
    }
    if !allFinite(a) {
        return MatrixInvariantReport(code: .nonFinite, allFinite: false, diagonalPositive: false, symmetric: false, choleskyOK: false, maxAsymmetry: 0, lambdaMin: 0, lambdaMax: 0, zeroEigenvalueCount: 0)
    }
    var diagPos = true
    for i in 0..<n where a[i * n + i] <= pdTol {
        diagPos = false
    }
    var maxAsym = 0.0
    for i in 0..<n {
        for j in (i + 1)..<n {
            let d = abs(a[i * n + j] - a[j * n + i])
            if d > maxAsym { maxAsym = d }
        }
    }
    let symOK = maxAsym <= symTol
    if !symOK {
        return MatrixInvariantReport(code: .notSymmetric, allFinite: true, diagonalPositive: diagPos, symmetric: false, choleskyOK: false, maxAsymmetry: maxAsym, lambdaMin: 0, lambdaMax: 0, zeroEigenvalueCount: 0)
    }
    var sym = [Double](repeating: 0.0, count: n * n)
    for i in 0..<n {
        for j in 0..<n {
            sym[i * n + j] = 0.5 * (a[i * n + j] + a[j * n + i])
        }
    }
    guard let eigs = jacobiEigenvalues(sym, n: n) else {
        return MatrixInvariantReport(code: .nonFinite, allFinite: false, diagonalPositive: diagPos, symmetric: true, choleskyOK: false, maxAsymmetry: maxAsym, lambdaMin: 0, lambdaMax: 0, zeroEigenvalueCount: 0)
    }
    let lMin = eigs[0]
    let lMax = eigs[n - 1]
    var zCnt: Int32 = 0
    for ev in eigs where abs(ev) <= pdTol { zCnt += 1 }
    let cholOK = choleskyPDCheck(sym, n: n, pdTol: pdTol)
    let code: InvariantCode
    if lMin <= pdTol {
        code = .notPositiveDefinite
    } else if !cholOK {
        code = .choleskyFailed
    } else {
        code = .ok
    }
    return MatrixInvariantReport(code: code, allFinite: true, diagonalPositive: diagPos, symmetric: true, choleskyOK: cholOK, maxAsymmetry: maxAsym, lambdaMin: lMin, lambdaMax: lMax, zeroEigenvalueCount: zCnt)
}

public func checkSymmetricPSDNullity(
    _ a: [Double], n: Int, expectedNullity: Int32, symTol: Double = 1e-12, zeroTol: Double = 1e-9
) -> MatrixInvariantReport {
    if n == 0 || a.count != n * n {
        return MatrixInvariantReport(code: .emptyInput, allFinite: false, diagonalPositive: false, symmetric: false, choleskyOK: false, maxAsymmetry: 0, lambdaMin: 0, lambdaMax: 0, zeroEigenvalueCount: 0)
    }
    if !allFinite(a) {
        return MatrixInvariantReport(code: .nonFinite, allFinite: false, diagonalPositive: false, symmetric: false, choleskyOK: false, maxAsymmetry: 0, lambdaMin: 0, lambdaMax: 0, zeroEigenvalueCount: 0)
    }
    var diagNonNeg = true
    for i in 0..<n where a[i * n + i] < -zeroTol { diagNonNeg = false }
    var maxAsym = 0.0
    for i in 0..<n {
        for j in (i + 1)..<n {
            let d = abs(a[i * n + j] - a[j * n + i])
            if d > maxAsym { maxAsym = d }
        }
    }
    if maxAsym > symTol {
        return MatrixInvariantReport(code: .notSymmetric, allFinite: true, diagonalPositive: diagNonNeg, symmetric: false, choleskyOK: false, maxAsymmetry: maxAsym, lambdaMin: 0, lambdaMax: 0, zeroEigenvalueCount: 0)
    }
    var sym = [Double](repeating: 0.0, count: n * n)
    for i in 0..<n {
        for j in 0..<n {
            sym[i * n + j] = 0.5 * (a[i * n + j] + a[j * n + i])
        }
    }
    guard let eigs = jacobiEigenvalues(sym, n: n) else {
        return MatrixInvariantReport(code: .nonFinite, allFinite: false, diagonalPositive: diagNonNeg, symmetric: true, choleskyOK: false, maxAsymmetry: maxAsym, lambdaMin: 0, lambdaMax: 0, zeroEigenvalueCount: 0)
    }
    let lMin = eigs[0]
    let lMax = eigs[n - 1]
    var zCnt: Int32 = 0
    for ev in eigs where abs(ev) <= zeroTol { zCnt += 1 }
    let code: InvariantCode
    if lMin < -zeroTol {
        code = .notPSD
    } else if zCnt != expectedNullity {
        code = .wrongNullity
    } else {
        code = .ok
    }
    return MatrixInvariantReport(code: code, allFinite: true, diagonalPositive: diagNonNeg, symmetric: true, choleskyOK: lMin > zeroTol, maxAsymmetry: maxAsym, lambdaMin: lMin, lambdaMax: lMax, zeroEigenvalueCount: zCnt)
}

/// Check Hermiticity of an interleaved (re, im) row-major complex n x n matrix.
public func checkHermitianComplex(_ interleaved: [Double], n: Int, tol: Double = 1e-12) -> (ok: Bool, maxErr: Double) {
    if n == 0 || interleaved.count != 2 * n * n || !allFinite(interleaved) {
        return (false, Double.nan)
    }
    var maxErr = 0.0
    for i in 0..<n {
        let diagIm = abs(interleaved[2 * (i * n + i) + 1])
        if diagIm > maxErr { maxErr = diagIm }
        for j in (i + 1)..<n {
            let reIJ = interleaved[2 * (i * n + j)]
            let imIJ = interleaved[2 * (i * n + j) + 1]
            let reJI = interleaved[2 * (j * n + i)]
            let imJI = interleaved[2 * (j * n + i) + 1]
            let er = abs(reIJ - reJI)
            let ei = abs(imIJ + imJI)
            if er > maxErr { maxErr = er }
            if ei > maxErr { maxErr = ei }
        }
    }
    return (maxErr <= tol, maxErr)
}

public func checkProbabilitySimplex(_ probs: [Double], sumTol: Double = 1e-12) -> ConservationReport {
    if probs.isEmpty {
        return ConservationReport(code: .emptyInput, allFinite: false, allNonNegative: false, sumValue: 0, absError: 0)
    }
    if !allFinite(probs) {
        return ConservationReport(code: .nonFinite, allFinite: false, allNonNegative: false, sumValue: 0, absError: 0)
    }
    var nonNeg = true
    for p in probs where p < 0.0 { nonNeg = false }
    let sum = sumNeumaier(probs)
    let err = abs(sum - 1.0)
    let code: InvariantCode
    if !nonNeg {
        code = .negativeProbability
    } else if err > sumTol {
        code = .conservationViolation
    } else {
        code = .ok
    }
    return ConservationReport(code: code, allFinite: true, allNonNegative: nonNeg, sumValue: sum, absError: err)
}

public func checkExactIntegerConservation(_ counts: [Int64], expectedTotal: Int64) -> ExactConservationReport {
    if counts.isEmpty {
        return ExactConservationReport(code: .emptyInput, allNonNegative: false, sumValue: 0, expectedSum: expectedTotal)
    }
    var nonNeg = true
    var acc: Int64 = 0
    for c in counts {
        if c < 0 { nonNeg = false }
        acc += c
    }
    let code: InvariantCode
    if !nonNeg {
        code = .negativeProbability
    } else if acc != expectedTotal {
        code = .conservationViolation
    } else {
        code = .ok
    }
    return ExactConservationReport(code: code, allNonNegative: nonNeg, sumValue: acc, expectedSum: expectedTotal)
}
