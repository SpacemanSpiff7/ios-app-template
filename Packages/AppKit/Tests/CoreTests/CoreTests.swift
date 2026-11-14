import Core
import Testing

struct CoreTests {
    @Test func schemaVersionIsPositive() {
        #expect(CoreVersion.schema > 0)
    }
}
