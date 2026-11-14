import Core
import Foundation
import Testing

struct ItemDraftTests {
    @Test func cancelLeavesOriginalUntouched() {
        let original = Item(name: "Notebook", amount: 2)
        var draft = ItemDraft(item: original)
        draft.name = "Changed"
        draft.amountText = ""
        #expect(draft.hasChanges)
        #expect(draft.original == original)
        #expect(original.amount == 2)
    }

    @Test(arguments: ["", " ", "-1", "1x", "1.2.3", "nan", "inf"])
    func invalidAmountsStayInDraft(text: String) {
        var draft = ItemDraft()
        draft.name = "Notebook"
        draft.amountText = text
        #expect(throws: DraftError.self) { try draft.item(locale: Locale(identifier: "en_US")) }
        #expect(draft.amountText == text)
    }

    @Test(arguments: ["en_US", "de_DE"])
    func localeAndZeroAreSupported(identifier: String) throws {
        let locale = Locale(identifier: identifier)
        var draft = ItemDraft()
        draft.name = "Notebook"
        draft.amountText = "1\(locale.decimalSeparator ?? ".")25"
        #expect(try draft.item(locale: locale).amount == 1.25)
        draft.amountText = "0"
        #expect(try draft.item(locale: locale).amount == 0)
    }

    @Test func unchangedNumberDoesNotRoundTripThroughDisplay() throws {
        let original = Item(name: "Small amount", amount: 0.12345678901234567)
        var draft = ItemDraft(item: original)
        #expect(!draft.hasChanges)
        draft.name = "Renamed"
        #expect(try draft.item().amount == original.amount)
        #expect(try draft.item().id == original.id)
    }

    @Test func nameIsRequiredAndSaveKeepsStableIdentity() throws {
        var draft = ItemDraft()
        #expect(throws: DraftError.self) { try draft.item() }
        draft.name = " Notebook "
        #expect(try draft.item().name == "Notebook")
        #expect(try draft.item().id == draft.id)
    }

    @Test func tinyNonzeroAmountCanBeChangedToZero() throws {
        let locale = Locale(identifier: "en_US")
        let item = Item(name: "Tiny amount", amount: 1e-16)
        var draft = ItemDraft(item: item, locale: locale)
        #expect(NumberInput.number(from: draft.amountText, locale: locale) == item.amount)
        draft.amountText = "0"
        #expect(draft.hasChanges)
        #expect(try draft.item(locale: locale).amount == 0)
    }
}
