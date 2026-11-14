import SwiftUI

public extension View {
    /// Apply to a button's label so whitespace participates in the native row's tap target.
    func fullRowHitTarget() -> some View {
        frame(maxWidth: .infinity, minHeight: 44, alignment: .leading)
            .contentShape(.rect)
    }
}
