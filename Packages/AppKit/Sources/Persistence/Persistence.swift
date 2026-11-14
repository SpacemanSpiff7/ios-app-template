import Core
import SwiftData

/// Register EVERY @Model here. Containers in app and tests must use `AppSchema.current`.
public enum AppSchemaV1: VersionedSchema {
    public static let versionIdentifier = Schema.Version(1, 0, 0)
    public static var models: [any PersistentModel.Type] { [ItemRecord.self] }
}

public enum AppSchema {
    public static let current = AppSchemaV1.self
}

public enum AppMigrationPlan: SchemaMigrationPlan {
    public static var schemas: [any VersionedSchema.Type] { [AppSchemaV1.self] }
    public static var stages: [MigrationStage] { [] }
}
