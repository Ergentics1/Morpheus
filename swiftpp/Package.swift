// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MorpheusSwiftPP",
    products: [
        .library(name: "ErgenticsSwift", targets: ["ErgenticsSwift"]),
        .library(name: "ErgenticsInterop", targets: ["ErgenticsInterop"]),
        .executable(name: "ErgenticsCLI", targets: ["ErgenticsCLI"]),
    ],
    targets: [
        // Lane 1 (C++20 core also built standalone via CMakeLists.txt with g++ / clang++).
        .target(
            name: "ErgenticsCXX",
            path: "Sources/ErgenticsCXX",
            sources: ["src"],
            publicHeadersPath: "include"
        ),
        // Lane 2 (Pure Swift 6.4: zero C++ imports, zero C++ interop flags).
        .target(
            name: "ErgenticsSwift",
            path: "Sources/ErgenticsSwift"
        ),
        // Lane 3 (Live Swift 6.4 <-> C++20 interop + 3-way Triple-Check comparator).
        .target(
            name: "ErgenticsInterop",
            dependencies: ["ErgenticsCXX", "ErgenticsSwift"],
            path: "Sources/ErgenticsInterop",
            swiftSettings: [.interoperabilityMode(.Cxx)]
        ),
        // CLI runner for full Triple-Check D/R/P/Seam SWE-sweep and optional Data Model export.
        .executableTarget(
            name: "ErgenticsCLI",
            dependencies: ["ErgenticsInterop", "ErgenticsSwift"],
            path: "Sources/ErgenticsCLI",
            swiftSettings: [.interoperabilityMode(.Cxx)]
        ),
        // Four SWE-Sweep test suites (D / R / P / Seam).
        .testTarget(
            name: "DeterministicTests",
            dependencies: ["ErgenticsInterop", "ErgenticsSwift", "ErgenticsCXX"],
            path: "Tests/DeterministicTests",
            swiftSettings: [.interoperabilityMode(.Cxx)]
        ),
        .testTarget(
            name: "RuntimeTests",
            dependencies: ["ErgenticsInterop", "ErgenticsSwift", "ErgenticsCXX"],
            path: "Tests/RuntimeTests",
            swiftSettings: [.interoperabilityMode(.Cxx)]
        ),
        .testTarget(
            name: "CalibrationTests",
            dependencies: ["ErgenticsInterop", "ErgenticsSwift", "ErgenticsCXX"],
            path: "Tests/CalibrationTests",
            swiftSettings: [.interoperabilityMode(.Cxx)]
        ),
        .testTarget(
            name: "SeamTests",
            dependencies: ["ErgenticsInterop", "ErgenticsSwift", "ErgenticsCXX"],
            path: "Tests/SeamTests",
            swiftSettings: [.interoperabilityMode(.Cxx)]
        ),
    ],
    cxxLanguageStandard: .cxx20
)
