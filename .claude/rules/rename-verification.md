---
paths:
  - "**/*.swift"
---
# Renames must verify the visible target
A commit titled "rename X → Y" must change the user-visible label. Before committing:
1. `grep -rn "X"` in `Text(`, `Label(`, `navigationTitle`, `.xcstrings` — zero hits in the renamed surface.
2. `grep -rn "Y"` — at least one hit in the same surface.
3. Simulator screenshot of the screen; read it back. Old label still visible → it's a doc tweak, not a rename.
