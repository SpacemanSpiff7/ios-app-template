import Foundation

/// Text buffers remain intact until Save. Cancel never changes the accepted item.
public struct ItemDraft: Equatable, Identifiable, Sendable {
    public let id: UUID
    public let original: Item?
    public var name: String
    public var amountText: String
    private let initialAmountText: String

    public init(item: Item? = nil, locale: Locale = .current) {
        self.id = item?.id ?? UUID()
        self.original = item
        self.name = item?.name ?? ""
        let text = item.map { NumberInput.text(for: $0.amount, locale: locale) } ?? "1"
        self.amountText = text
        self.initialAmountText = text
    }

    public var hasChanges: Bool {
        name != (original?.name ?? "") || amountText != initialAmountText
    }

    public func item(locale: Locale = .current) throws -> Item {
        let title = name.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !title.isEmpty else { throw DraftError.missingName }
        let amount: Double
        if amountText == initialAmountText, let original {
            amount = original.amount
        } else {
            guard let value = NumberInput.number(from: amountText, locale: locale), value >= 0 else {
                throw DraftError.invalidAmount
            }
            amount = value
        }
        return Item(id: id, name: title, amount: amount)
    }
}

public enum DraftError: Error, Sendable {
    case missingName
    case invalidAmount
}
