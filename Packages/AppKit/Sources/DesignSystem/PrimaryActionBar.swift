import SwiftUI

/// The single primary action of a review or editing screen, pinned above the bottom edge.
/// Attach with `.primaryActionBar(...)` on the screen's `Form`/`List`.
public struct PrimaryActionBar: View {
    let title: String
    let status: String?
    let isDisabled: Bool
    let action: () -> Void

    public init(_ title: String, status: String? = nil, isDisabled: Bool = false, action: @escaping () -> Void) {
        self.title = title
        self.status = status
        self.isDisabled = isDisabled
        self.action = action
    }

    public var body: some View {
        VStack(spacing: 8) {
            if let status {
                Text(status)
                    .font(.footnote)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
            }
            Button(action: action) {
                Text(title).frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)
            .disabled(isDisabled)
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
    }
}

public extension View {
    /// Content scrolls beneath the bar with the system edge effect instead of a material slab.
    func primaryActionBar(
        _ title: String,
        status: String? = nil,
        isDisabled: Bool = false,
        action: @escaping () -> Void
    ) -> some View {
        safeAreaBar(edge: .bottom) {
            PrimaryActionBar(title, status: status, isDisabled: isDisabled, action: action)
        }
    }
}
