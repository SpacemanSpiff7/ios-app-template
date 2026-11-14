import Core
import Foundation
import SwiftData

@Model
final class ItemRecord {
    var id = UUID()
    var name: String = ""
    var amount: Double = 0

    init(item: Item) {
        id = item.id
        name = item.name
        amount = item.amount
    }

    var value: Item { Item(id: id, name: name, amount: amount) }
}
