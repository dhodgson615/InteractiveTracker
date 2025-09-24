// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "InteractiveTracker",
    platforms: [
        .macOS(.v10_15)
    ],
    products: [
        .executable(name: "InteractiveTracker", targets: ["InteractiveTracker"])
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "InteractiveTracker",
            dependencies: []
        )
    ]
)