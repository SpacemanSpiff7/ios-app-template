// swift-tools-version: __SWIFT_TOOLS_VERSION__
import PackageDescription

let core: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("ExistentialAny"),
]
let ui: [SwiftSetting] = [.defaultIsolation(MainActor.self)] + core

let package = Package(
    name: "AppKit",
    platforms: [.iOS("__MIN_IOS__")],
    products: [
        .library(name: "Core", targets: ["Core"]),
        .library(name: "Domain", targets: ["Domain"]),
        .library(name: "Persistence", targets: ["Persistence"]),
        .library(name: "DesignSystem", targets: ["DesignSystem"]),
        .library(name: "Features", targets: ["Home"]),
    ],
    targets: [
        // ---- nonisolated layer -------------------------------------------
        .target(name: "Core", swiftSettings: core),
        .target(name: "Domain", dependencies: ["Core"], swiftSettings: core),
        .target(name: "Persistence", dependencies: ["Core"], swiftSettings: core),
        // ---- MainActor layer ---------------------------------------------
        .target(name: "DesignSystem", swiftSettings: ui),
        .target(name: "Home", dependencies: ["Core", "Domain", "Persistence", "DesignSystem"],
                path: "Sources/Features/Home", swiftSettings: ui),
        // ---- tests --------------------------------------------------------
        .testTarget(name: "CoreTests", dependencies: ["Core"], swiftSettings: core),
        .testTarget(name: "DesignSystemTests", dependencies: ["DesignSystem"], swiftSettings: ui),
    ]
)
