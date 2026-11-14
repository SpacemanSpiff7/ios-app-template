import Foundation
import Persistence
import SwiftData

/// File-backed SwiftData container for the app-host test target (in-memory traps here).
/// Usage: `let (container, cleanup) = try makeFileBackedContainer(); defer { cleanup() }`
func makeFileBackedContainer(name: String = #function) throws -> (ModelContainer, () -> Void) {
    let url = FileManager.default.temporaryDirectory
        .appendingPathComponent("\(name)-\(UUID().uuidString).store")
    let config = ModelConfiguration(url: url)
    let container = try ModelContainer(
        for: Schema(AppSchema.current.models),
        migrationPlan: AppMigrationPlan.self,
        configurations: config
    )
    let cleanup = {
        for suffix in ["", "-shm", "-wal"] {
            try? FileManager.default.removeItem(at: URL(fileURLWithPath: url.path + suffix))
        }
    }
    return (container, cleanup)
}
