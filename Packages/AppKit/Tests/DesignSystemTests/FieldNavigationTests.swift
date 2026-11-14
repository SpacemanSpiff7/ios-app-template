@testable import DesignSystem
import Testing

struct FieldNavigationTests {
    @Test func navigationRespectsEdgesAndUnknownFocus() {
        let fields = ["name", "amount", "limit"]
        let first = FieldNavigation.neighbors(fields: fields, current: "name")
        #expect(first.previous == nil)
        #expect(first.next == "amount")
        let middle = FieldNavigation.neighbors(fields: fields, current: "amount")
        #expect(middle.previous == "name")
        #expect(middle.next == "limit")
        let last = FieldNavigation.neighbors(fields: fields, current: "limit")
        #expect(last.previous == "amount")
        #expect(last.next == nil)
        let unknown = FieldNavigation.neighbors(fields: fields, current: "missing")
        #expect(unknown.previous == nil && unknown.next == nil)
        let none = FieldNavigation.neighbors(fields: fields, current: nil)
        #expect(none.previous == nil && none.next == nil)
    }
}
