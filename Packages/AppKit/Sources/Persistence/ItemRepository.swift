import Core
import Foundation
import SwiftData

/// Owns the container so its context cannot outlive it. Values, not @Model instances, leave this target.
@MainActor
public struct ItemRepository {
    private let container: ModelContainer

    public init(container: ModelContainer) {
        self.container = container
        container.mainContext.autosaveEnabled = false
    }

    public init() throws {
        let schema = Schema(AppSchema.current.models)
        self.init(container: try ModelContainer(for: schema, migrationPlan: AppMigrationPlan.self))
    }

    public func items() throws -> [Item] {
        try container.mainContext.fetch(FetchDescriptor<ItemRecord>(sortBy: [SortDescriptor(\.name)]))
            .map(\.value)
    }

    public func save(_ item: Item) throws {
        let context = container.mainContext
        let itemID = item.id
        let descriptor = FetchDescriptor<ItemRecord>(predicate: #Predicate { $0.id == itemID })
        if let record = try context.fetch(descriptor).first {
            record.name = item.name
            record.amount = item.amount
        } else {
            context.insert(ItemRecord(item: item))
        }
        do {
            try context.save()
        } catch {
            context.rollback()
            throw error
        }
    }
}
