import Foundation

/// Strict decimal input: grouping, trailing junk and blank-as-zero are rejected.
public enum NumberInput {
    public static func number(from text: String, locale: Locale = .current) -> Double? {
        let trimmed = text.trimmingCharacters(in: .whitespacesAndNewlines)
        let separator = locale.decimalSeparator ?? "."
        guard separator == "." || !trimmed.contains(".") else { return nil }
        var normalized = ""
        for character in trimmed.replacingOccurrences(of: separator, with: ".") {
            if character == "." {
                normalized.append(character)
            } else {
                guard let digit = character.wholeNumberValue, (0...9).contains(digit) else { return nil }
                normalized.append(String(digit))
            }
        }
        guard !normalized.isEmpty, normalized.filter({ $0 == "." }).count <= 1,
              let value = Double(normalized), value.isFinite else { return nil }
        return value
    }

    public static func text(for value: Double, locale: Locale = .current) -> String {
        guard value.isFinite else { return "" }
        return value.formatted(.number.locale(locale).precision(.significantDigits(1...17)).grouping(.never))
    }
}
