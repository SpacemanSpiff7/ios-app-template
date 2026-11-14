@testable import __APP_NAME__
import Testing

@Suite(.serialized)
struct AppLaunchTests {
    @Test func containerBuilds() throws {
        let (container, cleanup) = try makeFileBackedContainer()
        defer { cleanup() }
        _ = container
    }
}
