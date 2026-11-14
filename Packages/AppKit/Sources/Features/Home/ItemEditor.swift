import Core
import DesignSystem
import SwiftUI

struct ItemEditor: View {
    @Bindable var store: HomeStore
    @State var draft: ItemDraft
    @State private var isConfirmingDiscard = false
    @FocusState private var focus: Field?
    @Environment(\.dismiss) private var dismiss
    @Environment(\.locale) private var locale

    enum Field: Hashable { case name, amount }

    var body: some View {
        Form {
            Section {
                TextField("Name", text: $draft.name)
                    .focused($focus, equals: .name)
                NumericFieldRow(
                    "Amount",
                    text: $draft.amountText,
                    unit: "",
                    id: Field.amount,
                    focus: $focus
                )
            }
            if let message = store.saveError {
                Section { Text(message).foregroundStyle(.secondary) }
            }
        }
        .navigationTitle(draft.original == nil ? "Add Item" : "Edit Item")
        .navigationBarTitleDisplayMode(.inline)
        .withKeyboardToolbar()
        .focusedValue(\.fieldNavigation, FieldNavigation(fields: [Field.name, .amount], focus: $focus))
        .primaryActionBar("Save") {
            if store.save(draft, locale: locale) { dismiss() }
        }
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    if draft.hasChanges { isConfirmingDiscard = true } else { dismiss() }
                }
            }
        }
        .interactiveDismissDisabled(draft.hasChanges)
        .confirmationDialog("Discard your changes?", isPresented: $isConfirmingDiscard, titleVisibility: .visible) {
            Button("Discard Changes", role: .destructive) { dismiss() }
            Button("Keep Editing", role: .cancel) {}
        }
    }
}
