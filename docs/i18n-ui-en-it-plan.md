# UI i18n plan: English + Italian

## Scope (IMPORTANT)
This plan is **only** about the application **UI language** (English/Italian). It must not affect the mod/game translation pipeline.

### In scope
- UI language selection via `program_language_comboBox`.
- UI translation loading/unloading via `QTranslator` and `retranslateUi()`.
- Automatic UI language selection at startup:
  - If OS language is Italian (`it`) ⇒ UI = Italian.
  - Otherwise ⇒ UI = English.
- Translating UI-facing strings (UI widgets, menu, dialogs, accessibility descriptions) **only if they belong to the UI**.

### Out of scope (DO NOT TOUCH)
To avoid breaking the mod translation system, **do not change**:
- Any “mod translation languages” selectors / defaults:
  - `selector_original_language_comboBox`, `selector_target_language_comboBox`
  - `selector_game_supported_source_language_comboBox`, `selector_game_supported_target_language_comboBox`
- Any logic around `TranslatorManager(source_language=..., target_language=...)`.
- Any mapping between languages and Paradox localization folders.

---

## Preconditions / current state
- UI translation is currently handled via `QTranslator` + `retranslateUi()` and additional retranslate calls (e.g. `LanguageConstants.retranslate()`).
- There is legacy RU text in UI sources and constants; the goal is to make **English** the UI source language and **Italian** the translated language.

---

# Incremental commit plan

## Commit 1 — Normalize UI language to EN/IT (stable codes)
### Goal
Make UI language a stable concept with only **English** and **Italiano** available, removing any hard-coded RU “base language” logic.

### Tasks
- Update UI language handling so the selector exposes only:
  - `English` (code: `en`)
  - `Italiano` (code: `it`)
- Ensure the stored UI language preference uses stable codes (`en`/`it`) rather than UI labels.
- Remove special-case logic like `if currentText != 'Русский'` from UI language switching.

### Checks
- UI language combo shows only “English” and “Italiano”.
- Old stored values (e.g. RU strings) do not crash; they fallback to EN.

### Commit message
`i18n(ui): normalize UI language selector to EN/IT`

---

## Commit 2 — Auto-select UI language on startup (OS it → IT else EN)
### Goal
At first launch (or when no valid preference exists), select UI language based on system locale:
- OS language is Italian ⇒ UI Italian
- else ⇒ UI English

### Tasks
- Define priority:
  1) saved user preference (if valid)
  2) otherwise, autodetect from system locale
- Apply selected UI language before showing the main window.

### Checks
- Fresh start on Italian OS ⇒ UI in Italian.
- Fresh start on non-Italian OS ⇒ UI in English.
- If user changes language manually, the selection persists and overrides autodetect on next launch.

### Commit message
`i18n(ui): auto-select UI language from system locale`

---

## Commit 3 — Deterministic translator loading (UI only)
### Goal
Make translator loading predictable and minimal.

### Tasks
- Define an explicit set of `.qm` files needed for UI translations (at minimum Italian).
- Stop loading “all files found in the directory” without filtering.
- Enforce rule:
  - `it` ⇒ install Italian translator(s)
  - `en` ⇒ remove translators (English is base; translator optional but not required)

### Checks
- Switching EN ⇄ IT works reliably.
- Missing `.qm` file results in a safe fallback to EN + warning/log, no crash.

### Commit message
`i18n(ui): make translator loading deterministic (it only, en base)`

---

## Commit 4 — Make English the UI source language (regen UI)
### Goal
Ensure the UI “source strings” are **English**, so English works without a translator.

### Tasks
- Identify the `.ui` source file for MainWindow.
- Change its labels/buttons text to English.
- Regenerate `gui/window_ui/MainWindow.py` using `pyuic5`.
- Ensure `retranslateUi()` source text is English.

### Checks
- With UI language `en` and no translator, UI shows English.
- With UI language `it`, UI shows Italian.

### Commit message
`i18n(ui): switch UI source language to English (regen MainWindow UI)`

---

## Commit 5 — Align Python-side UI strings (LanguageConstants etc.)
### Goal
Ensure non-Designer UI strings (menu labels, dialogs, warnings, accessibility UI strings) follow the same EN-base/IT-translation approach.

### Tasks
- Convert `LanguageConstants` (and any other UI constants class) to have **English source** strings.
- Keep them translatable through Qt (`QCoreApplication.translate`) so they end up in the Italian `.ts/.qm`.
- Ensure language change calls retranslate methods as already done.

### Checks
- Menu labels and window titles match the selected UI language.
- No changes to mod translation language selection.

### Commit message
`i18n(ui): make UI constants EN base and translatable`

---

# Mandatory regression checks (every commit)
- Keyboard navigation/tab order/shortcuts must continue to work.
- No changes to mod translation selectors and defaults.
- No changes to `TranslatorManager` logic for mod translation.

---

## Notes for the coding agent
- If settings storage is ambiguous, create a dedicated setting key for UI language (e.g. `ui_language`) rather than reusing fields tied to mod translation.
- Keep commits small and focused; after each commit, run the app and validate the relevant checklist.
