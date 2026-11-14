import SwiftUI

/// The one numeric text field: a filled field that selects its value on focus so typing replaces it.
public struct NumericField: View {
    @Binding private var text: String
    let placeholder: String
    let isFocused: Bool
    let alignment: TextAlignment
    @State private var selection: TextSelection?

    public init(
        text: Binding<String>,
        placeholder: String = "—",
        isFocused: Bool,
        alignment: TextAlignment = .trailing
    ) {
        self._text = text
        self.placeholder = placeholder
        self.isFocused = isFocused
        self.alignment = alignment
    }

    public var body: some View {
        TextField(placeholder, text: $text, selection: $selection)
            .keyboardType(.decimalPad)
            .multilineTextAlignment(alignment)
            .monospacedDigit()
            .padding(.horizontal, 10)
            .frame(minHeight: 44)
            .background(Color(.tertiarySystemFill), in: .rect(cornerRadius: 8))
            .onChange(of: isFocused) { _, focused in
                guard focused, !text.isEmpty else { return }
                // After the tap has placed its caret, select everything so the next key replaces the value.
                Task { selection = TextSelection(range: text.startIndex..<text.endIndex) }
            }
    }
}

/// A labelled numeric value in a `Form`/`List`: label leading, fixed-width field and unit column trailing.
/// Tapping anywhere in the row focuses the field. Stacks vertically at accessibility text sizes.
public struct NumericFieldRow<FieldID: Hashable>: View {
    let title: String
    @Binding private var text: String
    let unit: String
    let approximate: Bool
    let isInvalid: Bool
    let id: FieldID
    let focus: FocusState<FieldID?>.Binding
    @ScaledMetric(relativeTo: .body) private var fieldWidth: CGFloat = 88
    @ScaledMetric(relativeTo: .body) private var unitWidth: CGFloat = 40
    @Environment(\.dynamicTypeSize) private var typeSize

    public init(
        _ title: String,
        text: Binding<String>,
        unit: String,
        approximate: Bool = false,
        isInvalid: Bool = false,
        id: FieldID,
        focus: FocusState<FieldID?>.Binding
    ) {
        self.title = title
        self._text = text
        self.unit = unit
        self.approximate = approximate
        self.isInvalid = isInvalid
        self.id = id
        self.focus = focus
    }

    public var body: some View {
        if typeSize.isAccessibilitySize {
            VStack(alignment: .leading, spacing: 4) {
                label
                field
            }
        } else {
            HStack(spacing: 8) {
                label
                field
            }
        }
    }

    /// Extends the field's tap target to the label and the row's whitespace. The field carries the
    /// accessibility label, so this duplicate target is hidden from assistive technology.
    private var label: some View {
        Button { focus.wrappedValue = id } label: {
            Text(title)
                .frame(maxWidth: .infinity, minHeight: 44, alignment: .leading)
                .contentShape(.rect)
        }
        .buttonStyle(.plain)
        .accessibilityHidden(true)
    }

    private var field: some View {
        HStack(spacing: 6) {
            if isInvalid {
                Image(systemName: "exclamationmark.circle")
                    .foregroundStyle(.secondary)
                    .accessibilityLabel("Invalid \(title.lowercased())")
            }
            if approximate {
                Text("~").foregroundStyle(.secondary).accessibilityHidden(true)
            }
            NumericField(text: $text, isFocused: focus.wrappedValue == id)
                .frame(width: typeSize.isAccessibilitySize ? nil : fieldWidth)
                .focused(focus, equals: id)
                .accessibilityLabel(accessibilityTitle)
            if !unit.isEmpty {
                Text(unit)
                    .foregroundStyle(.secondary)
                    .accessibilityHidden(true)
                    .frame(width: typeSize.isAccessibilitySize ? nil : unitWidth, alignment: .leading)
            }
        }
    }

    private var accessibilityTitle: String {
        [title, approximate ? "approximate" : "", unit].filter { !$0.isEmpty }.joined(separator: ", ")
    }
}

/// Previous/next movement between the numeric fields of the focused editor, shown in the keyboard toolbar.
public struct FieldNavigation {
    let previous: (() -> Void)?
    let next: (() -> Void)?

    public init(previous: (() -> Void)?, next: (() -> Void)?) {
        self.previous = previous
        self.next = next
    }

    /// Movement within an ordered list of fields; nil at either end disables that direction.
    public init<FieldID: Hashable>(fields: [FieldID], focus: FocusState<FieldID?>.Binding) {
        let targets = Self.neighbors(fields: fields, current: focus.wrappedValue)
        self.previous = targets.previous.map { target in { focus.wrappedValue = target } }
        self.next = targets.next.map { target in { focus.wrappedValue = target } }
    }

    static func neighbors<FieldID: Hashable>(fields: [FieldID], current: FieldID?)
        -> (previous: FieldID?, next: FieldID?) {
        let index = current.flatMap { fields.firstIndex(of: $0) }
        let previous = index.flatMap { $0 > 0 ? fields[$0 - 1] : nil }
        let next = index.flatMap { $0 + 1 < fields.count ? fields[$0 + 1] : nil }
        return (previous, next)
    }
}

public extension FocusedValues {
    @Entry var fieldNavigation: FieldNavigation?
}
