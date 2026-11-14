import Core
import Foundation
@testable import Home
import Persistence
import SwiftUI
import Testing
import UIKit

/// Render artifacts for inspection; these do not establish focus, gestures or VoiceOver.
@Suite(.serialized, .timeLimit(.minutes(1)))
struct NativeRenderTests {
    @Test(arguments: [false, true])
    func emptyAndPopulatedHomeRender(accessibility: Bool) async throws {
        let (container, cleanup) = try makeFileBackedContainer()
        defer { cleanup() }
        let repository = ItemRepository(container: container)
        let store = HomeStore(repository: repository)
        try await render(HomeView(store: store), name: "home-empty", accessibility: accessibility)
        try repository.save(Item(name: "Notebook", amount: 2))
        store.reload()
        try await render(HomeView(store: store), name: "home-populated", accessibility: accessibility)
        _ = container
    }

    @Test(arguments: [false, true])
    func editorAndSaveFailureRender(accessibility: Bool) async throws {
        enum Failure: Error { case disk }
        let store = HomeStore(load: { [] }, save: { _ in throw Failure.disk })
        var draft = ItemDraft()
        draft.name = "Notebook"
        let screen = NavigationStack { ItemEditor(store: store, draft: draft) }
        try await render(screen, name: "editor", accessibility: accessibility)
        #expect(!store.save(draft))
        try await render(screen, name: "editor-failure", accessibility: accessibility)
        #expect(draft.name == "Notebook")
    }

    private func render<Content: View>(
        _ content: Content,
        name: String,
        accessibility: Bool
    ) async throws {
        let scene = try #require(UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }.first)
        let previous = scene.windows.first(where: \.isKeyWindow)
        let window = UIWindow(windowScene: scene)
        if let previous { window.frame = previous.frame }
        window.overrideUserInterfaceStyle = accessibility ? .dark : .light
        let root = content.dynamicTypeSize(accessibility ? .accessibility3 : .large)
            .environment(\.colorScheme, accessibility ? .dark : .light)
        let host = UIHostingController(rootView: root)
        window.rootViewController = host
        window.makeKeyAndVisible()
        defer {
            window.isHidden = true
            window.rootViewController = nil
            previous?.makeKeyAndVisible()
        }
        host.view.layoutIfNeeded()
        try await Task.sleep(for: .seconds(1))
        host.view.layoutIfNeeded()
        var didDraw = false
        let image = UIGraphicsImageRenderer(size: window.bounds.size).pngData { _ in
            didDraw = window.drawHierarchy(in: window.bounds, afterScreenUpdates: true)
        }
        #expect(didDraw && image.count > 1_000)
        let project = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
        let folder = project.appendingPathComponent(".scratch/ui-audit", isDirectory: true)
        try FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
        let suffix = accessibility ? "dark-ax3" : "light-standard"
        try image.write(to: folder.appendingPathComponent("\(name)-\(suffix).png"), options: .atomic)
    }
}
