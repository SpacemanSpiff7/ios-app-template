import Core
import Foundation
import Observation
import Persistence

@Observable
public final class HomeStore {
    public private(set) var items: [Item] = []
    public private(set) var loadError: String?
    public private(set) var saveError: String?
    private let loadItems: () throws -> [Item]
    private let writeItem: (Item) throws -> Void

    public convenience init(repository: ItemRepository) {
        self.init(load: repository.items, save: repository.save)
    }

    init(load: @escaping () throws -> [Item], save: @escaping (Item) throws -> Void) {
        self.loadItems = load
        self.writeItem = save
        reload()
    }

    public func reload() {
        do {
            items = try loadItems()
            loadError = nil
        } catch {
            loadError = String(localized: "Items couldn’t be loaded. Try again.")
        }
    }

    public func beginEditing(_ item: Item? = nil) -> ItemDraft {
        saveError = nil
        return ItemDraft(item: item)
    }

    public func save(_ draft: ItemDraft, locale: Locale = .current) -> Bool {
        do {
            let item = try draft.item(locale: locale)
            let latest = try loadItems()
            let current = latest.first { $0.id == draft.id }
            guard current == draft.original || (draft.original == nil && current == item) else {
                saveError = String(localized: "This item changed. Reopen it before saving.")
                return false
            }
            try writeItem(item)
            // The committed value is accepted even if a later independent refresh fails.
            items = (latest.filter { $0.id != item.id } + [item]).sorted { $0.name < $1.name }
            saveError = nil
            return true
        } catch DraftError.missingName {
            saveError = String(localized: "Enter a name.")
        } catch DraftError.invalidAmount {
            saveError = String(localized: "Enter an amount of zero or more.")
        } catch {
            saveError = String(localized: "Your changes couldn’t be saved. Try again.")
        }
        return false
    }
}
