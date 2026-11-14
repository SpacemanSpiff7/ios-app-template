import SwiftUI
import UIKit

/// Ends text entry without submitting a search, saving a draft or dismissing its screen.
public enum KeyboardDismissal {
    public static func dismiss() {
        _ = UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
    }
}

public extension View {
    /// Attach once to each screen's content inside its NavigationStack, never to individual fields or rows.
    func withKeyboardToolbar() -> some View {
        modifier(KeyboardDismissToolbar())
    }
}

/// One keyboard bar per screen: previous/next for the focused editor's numeric fields, and Done.
private struct KeyboardDismissToolbar: ViewModifier {
    @State private var isVisible = false
    @FocusedValue(\.fieldNavigation) private var navigation

    func body(content: Content) -> some View {
        content
            .toolbar {
                if isVisible {
                    ToolbarItemGroup(placement: .keyboard) {
                        if let navigation, navigation.previous != nil || navigation.next != nil {
                            Button { navigation.previous?() } label: { Image(systemName: "chevron.up") }
                                .disabled(navigation.previous == nil)
                                .accessibilityLabel("Previous field")
                            Button { navigation.next?() } label: { Image(systemName: "chevron.down") }
                                .disabled(navigation.next == nil)
                                .accessibilityLabel("Next field")
                        }
                        Spacer()
                        Button("Done", action: KeyboardDismissal.dismiss).fontWeight(.semibold)
                    }
                }
            }
            .scrollDismissesKeyboard(.interactively)
            .onAppear { isVisible = true }
            .onDisappear { isVisible = false }
    }
}
