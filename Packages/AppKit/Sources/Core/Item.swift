import Foundation

/// Replace with the product's first value model; persistence records stay private.
public struct Item: Equatable, Identifiable, Sendable {
    public let id: UUID
    public var name: String
    public var amount: Double

    public init(id: UUID = UUID(), name: String, amount: Double) {
        self.id = id
        self.name = name
        self.amount = amount
    }
}
