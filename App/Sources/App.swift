import Home
import Persistence
import SwiftUI

@main
struct __APP_NAME__App: App {
    @State private var store: HomeStore?
    @State private var isStorageUnavailable = false

    var body: some Scene {
        WindowGroup {
            Group {
                if let store {
                    HomeView(store: store)
                } else if isStorageUnavailable {
                    ContentUnavailableView {
                        Label("Items Unavailable", systemImage: "exclamationmark.triangle")
                    } description: {
                        Text("Your items couldn’t be opened.")
                    } actions: {
                        Button("Try Again", action: openStore)
                    }
                } else {
                    ProgressView()
                }
            }
            .task { openStore() }
        }
    }

    private func openStore() {
        do {
            store = HomeStore(repository: try ItemRepository())
            isStorageUnavailable = false
        } catch {
            isStorageUnavailable = true
        }
    }
}
