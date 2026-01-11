# A11Y: Accessible Names & Descriptions (EN)

## Context
Repo: `Nemex81/ModTranslationHelper-master`  
Working branch: `copilot/improve-keyboard-accessibility`  
Goal: improve screen reader usability (NVDA) during Tab navigation by assigning Qt accessibility metadata (`setAccessibleName`, `setAccessibleDescription`) to the main UI controls and to dynamically created checkboxes.

## Non‑negotiable constraints
- **Do not edit Qt-generated files** (pyuic output), especially `gui/window_ui/MainWindow.py`. Any manual edits there will be lost on regeneration.
- **Do not change existing Tab order / keyboard navigation logic** already implemented in `gui/main_window.py` (`__init_keyboard_nav`, `apply_tab_order`, eventFilter behavior). This task is only about accessible names/descriptions.
- **Do not rename widgets** (objectName) coming from the UI file; only set accessibility properties at runtime in `gui/main_window.py` and `gui/dialog_window.py`.
- Keep changes small and traceable: multiple incremental commits.
- Keep strings **hardcoded in English** for now (no localization work in this task).

## Acceptance criteria (manual checklist)
After implementation:
1. Launch app and Tab through all controls in the defined tab order; NVDA should announce each control with a clear purpose (name + role + description).
2. Change UI language using `program_language_comboBox`, then Tab again: accessible descriptions must still be present (re-applied after `retranslateUi`).
3. Enter the file list area (scroll area with checkboxes). Moving with Tab/Up/Down should read each checkbox with a clear description including the file path.
4. Trigger a path error dialog; NVDA should read the error message area as “Error message” with a clear description.

---

# Commit plan

## Commit 1 — Centralized accessibility texts for main window controls

### Files
- `gui/main_window.py`

### Implementation steps
1. Add a private method, e.g. `def __init_accessibility_texts(self): ...`
2. In this method, call `setAccessibleName()` and `setAccessibleDescription()` on the widgets listed below.
3. Call `self.__init_accessibility_texts()`:
   - once in `MainWindow.__init__` after `setupUi` and after key init steps (safe place: near the end of `__init__`, after `__preset_values()` / `__check_readiness()`), and
   - at the end of `__change_language()` after `self.__ui.retranslateUi(self)` so descriptions remain set after UI retranslation.

### Controls + English strings (hardcoded)

#### Language and game
- `program_language_comboBox`
  - Name: `UI language`
  - Description: `Select the language of the application interface.`
- `select_game_comboBox`
  - Name: `Game`
  - Description: `Select the Paradox game you are translating/modding for.`

#### Paths (LineEdits + buttons)
- `game_directory_lineEdit`
  - Name: `Game localization folder`
  - Description: `Path to the game's localization folder (contains english, russian, etc.).`
- `game_directory_pushButton`
  - Name: `Browse game localization folder`
  - Description: `Open a folder picker to select the game's localization folder.`
- `game_directory_open_pushButton`
  - Name: `Open game localization folder`
  - Description: `Open the game localization folder in the file explorer.`

- `original_directory_lineEdit`
  - Name: `Mod localization folder`
  - Description: `Path to the original mod localization folder (source files).`
- `original_directory_pushButton`
  - Name: `Browse mod localization folder`
  - Description: `Open a folder picker to select the original mod localization folder.`
- `original_directory_open_pushButton`
  - Name: `Open mod localization folder`
  - Description: `Open the original mod localization folder in the file explorer.`

- `previous_directory_lineEdit`
  - Name: `Previous translation folder`
  - Description: `Optional. Path to a previous translation version to reuse already translated lines.`
- `previous_directory_pushButton`
  - Name: `Browse previous translation folder`
  - Description: `Open a folder picker to select the previous translation folder.`
- `previous_directory_open_pushButton`
  - Name: `Open previous translation folder`
  - Description: `Open the previous translation folder in the file explorer.`

- `target_directory_lineEdit`
  - Name: `Output folder`
  - Description: `Output folder where generated localization files will be saved.`
- `target_directory_pushButton`
  - Name: `Browse output folder`
  - Description: `Open a folder picker to select the output folder.`
- `target_directory_open_pushButton`
  - Name: `Open output folder`
  - Description: `Open the output folder in the file explorer.`

#### Languages
- `selector_original_language_comboBox`
  - Name: `Source language`
  - Description: `Language of the original strings to process (e.g., english).`
- `selector_target_language_comboBox`
  - Name: `Target language`
  - Description: `Language for the translated output (e.g., italian).`
- `selector_game_supported_source_language_comboBox`
  - Name: `Mod source language folder`
  - Description: `Language subfolder inside the mod localization directory used as source.`
- `selector_game_supported_target_language_comboBox`
  - Name: `Mod target language folder`
  - Description: `Language subfolder used for output and/or previous translation lookup.`

#### Machine translation area
- `need_translation_checkBox`
  - Name: `Add machine translation`
  - Description: `When enabled, adds machine translation for the selected files.`
- `check_all_pushButton`
  - Name: `Select all files`
  - Description: `Select all files in the file list below.`
- `uncheck_all_pushButton`
  - Name: `Unselect all files`
  - Description: `Unselect all files in the file list below.`
- `update_need_translation_area_pushButton`
  - Name: `Refresh file list`
  - Description: `Reload the file list from the selected mod directory.`
- `need_translate_scrollArea`
  - Name: `File list`
  - Description: `List of mod localization files. Check files to include in machine translation.`

#### Options and run
- `disable_original_line_checkBox`
  - Name: `Disable original line output`
  - Description: `Advanced option related to how original lines are written when machine translation is enabled.`
- `run_pushButton`
  - Name: `Start`
  - Description: `Start generating the output localization files.`

#### Links
- `discord_link_pushButton`
  - Name: `Discord server`
  - Description: `Open the Discord server for support and bug reports.`
- `donate_pushButton`
  - Name: `Donate`
  - Description: `Open the donation page to support the project.`

### Commit message
`a11y: add accessible descriptions to main window controls (EN)`

---

## Commit 2 — Accessibility for dynamically generated file checkboxes

### Files
- `gui/main_window.py`

### Implementation steps
In `__form_checkbox_cascade`, after creating each per-file checkbox:
- `check_box.setAccessibleName("Machine translation file")`
- `check_box.setAccessibleDescription(f"Include this file in machine translation: {file_name}")`

Optional but recommended:
- `check_box.setToolTip(f"Include this file in machine translation: {file_name}")`

### Commit message
`a11y: add accessible text for dynamic file checkboxes (EN)`

---

## Commit 3 — Error dialog accessibility metadata

### Files
- `gui/dialog_window.py`

### Implementation steps
In `CustomDialog.__init__`, after `setupUi` and after setting the text browser content:
- `self.__ui.no_path_error_textBrowser.setAccessibleName("Error message")`
- `self.__ui.no_path_error_textBrowser.setAccessibleDescription("Shows details about an error, such as an invalid or missing path.")`

### Commit message
`a11y: add accessible text to error dialog (EN)`

---

## Final verification notes (do not skip)
- Confirm no changes were made to `gui/window_ui/MainWindow.py` (or any `gui/window_ui/*` file).
- Confirm the tab order list in `__init_keyboard_nav()` remains unchanged.
- Confirm shortcuts (`Ctrl+R`, `Alt+G`, `Alt+M`, `Alt+P`, `Alt+T`, `Alt+U`) still work.
- Confirm NVDA reads meaningful descriptions for:
  - `program_language_comboBox`, `select_game_comboBox`,
  - all path fields/buttons,
  - source/target language selectors,
  - machine translation checkbox + file list + select/unselect/refresh buttons,
  - disable-original option,
  - start button,
  - discord/donate buttons,
  - and the error dialog message.
