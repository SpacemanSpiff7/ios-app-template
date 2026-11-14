import Core
import Foundation
@testable import Home
import Persistence
import Testing

@Suite(.serialized)
struct ItemWorkflowTests {
    @Test func saveReopenEditAndCancel() throws {
        let (container, cleanup) = try makeFileBackedContainer()
        defer { cleanup() }
        let repository = ItemRepository(container: container)
        let store = HomeStore(repository: repository)
        var draft = ItemDraft()
        draft.name = "Notebook"
        draft.amountText = "2"
        #expect(store.save(draft))
        #expect(store.save(draft))
        #expect(try repository.items().count == 1)
        let saved = try #require(store.items.first)
        var canceled = ItemDraft(item: saved)
        canceled.name = "Discarded"
        #expect(canceled.hasChanges)
        #expect(try repository.items().first?.name == "Notebook")
        var edit = ItemDraft(item: saved)
        edit.amountText = "3"
        #expect(store.save(edit))
        let reopened = HomeStore(repository: repository)
        #expect(reopened.items.first?.amount == 3)
        _ = container
    }

    @Test func staleEditCannotOverwriteNewerValue() throws {
        let (container, cleanup) = try makeFileBackedContainer()
        defer { cleanup() }
        let repository = ItemRepository(container: container)
        let original = Item(name: "Notebook", amount: 1)
        try repository.save(original)
        let store = HomeStore(repository: repository)
        var draft = ItemDraft(item: original)
        draft.amountText = "3"
        try repository.save(Item(id: original.id, name: "Updated elsewhere", amount: 2))
        #expect(!store.save(draft))
        #expect(try repository.items().first?.amount == 2)
        #expect(draft.amountText == "3")
        _ = container
    }

    @Test func failedSaveRetainsDraftAndOriginal() {
        enum Failure: Error { case disk }
        let original = Item(name: "Notebook", amount: 1)
        let store = HomeStore(load: { [original] }, save: { _ in throw Failure.disk })
        var draft = ItemDraft(item: original)
        draft.amountText = "2"
        #expect(!store.save(draft))
        #expect(draft.amountText == "2")
        #expect(store.items == [original])
        #expect(store.saveError != nil)
    }

    @Test func acceptedSaveDoesNotBecomeARefreshFailure() {
        enum Failure: Error { case read }
        var reads = 0
        var persisted: Item?
        let store = HomeStore(load: {
            reads += 1
            guard reads <= 2 else { throw Failure.read }
            return []
        }, save: { persisted = $0 })
        var draft = store.beginEditing()
        draft.name = "Notebook"
        #expect(store.save(draft))
        #expect(store.items == [persisted].compactMap { $0 })
        #expect(store.saveError == nil)
        store.reload()
        #expect(store.loadError != nil)
        #expect(store.items.first == persisted)
    }

    @Test func validationErrorsStayWithTheirEditor() {
        let store = HomeStore(load: { [] }, save: { _ in })
        let draft = store.beginEditing()
        #expect(!store.save(draft))
        #expect(store.saveError != nil)
        #expect(store.loadError == nil)
        _ = store.beginEditing()
        #expect(store.saveError == nil)
    }
}
