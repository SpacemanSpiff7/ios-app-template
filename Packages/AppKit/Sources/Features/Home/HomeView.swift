import Core
import DesignSystem
import SwiftUI

public struct HomeView: View {
    @Bindable private var store: HomeStore
    @State private var draft: ItemDraft?

    public init(store: HomeStore) {
        self.store = store
    }

    public var body: some View {
        NavigationStack {
            List {
                if store.items.isEmpty {
                    emptyState
                }
                ForEach(store.items) { item in
                    Button { draft = store.beginEditing(item) } label: {
                        LabeledContent {
                            Text(item.amount, format: .number)
                        } label: {
                            Text(item.name)
                        }
                        .fullRowHitTarget()
                    }
                    .tint(.primary)
                }
                if let message = store.loadError {
                    Section {
                        Text(message)
                        Button("Try Again", action: store.reload)
                    }
                }
            }
            .navigationTitle("__APP_NAME__")
            .primaryActionBar("Add Item") { draft = store.beginEditing() }
            .sheet(item: $draft) { draft in
                NavigationStack { ItemEditor(store: store, draft: draft) }
            }
        }
    }

    private var emptyState: some View {
        ContentUnavailableView(
            "No Items",
            systemImage: "tray",
            description: Text("Add an item to get started.")
        )
        .listRowSeparator(.hidden)
    }
}
