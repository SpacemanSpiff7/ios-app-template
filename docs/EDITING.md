# Editing contract

Use this contract for new, existing and nested editors. The Items sample is a concrete reference.

- The store owns the accepted value and persistence; the editor owns a separate draft.
- A new draft never writes a placeholder. Add/Save validates and commits once.
- Dirty state compares the entire draft with its starting value, including invalid text and nested options.
- Cancel asks before discarding a dirty draft; disable interactive dismissal until that explicit choice.
  A clean editor exits directly.
- A pushed editor keeps the standard back action while clean and guards every dirty exit.
- Nested Apply stages changes in the parent draft. It does not bypass the parent's Save.
- Preserve a draft after validation or persistence failure and show an actionable error.
- Disable duplicate commits. An asynchronous update applies only if its originating draft/revision is still current.
- Keep entered text separate from parsed numbers: support the locale's decimal separator and valid zero.
  Blank is unknown, not zero; avoid rounding the stored value through a formatted display string.
- NumericFieldRow and .withKeyboardToolbar() provide consistent fields, Done and previous/next movement.
  Done ends text entry; it does not save or dismiss the editor.

Verify add → save → reopen → edit → cancel → reopen, plus repeated Save, invalid input, failed saves and
interrupted work. Include secondary/advanced editors in the same check. Confirm interaction at AX3/dark and
with VoiceOver; a rendered image alone does not establish focus or dismissal behavior.
