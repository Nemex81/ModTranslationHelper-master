# Accessibility: keyboard (TAB order + shortcuts) plan

Repository: https://github.com/Nemex81/ModTranslationHelper-master

## Scope
This document plans **only**:
- Keyboard navigation order (Tab / Shift+Tab).
- Keyboard shortcuts (accelerators / global shortcuts).

Out of scope:
- Screen reader announcements/labels/ARIA equivalents.
- Visual redesign.
- Translation engine logic.

## Files in scope (GUI)
Primary:
- `gui/main_window.py`
- `gui/window_ui/MainWindow.py`

Secondary windows:
- `gui/settings_window.py`
- `gui/window_ui/SettingsWindow.py`
- `gui/add_account_data_window.py`
- `gui/window_ui/AddAccountData.py`
- `gui/stat_table_window.py`
- `gui/window_ui/StatTableWindow.py`
- `gui/window_ui/BaseTable.py`

Optional (only if needed for consistent keyboard close/confirm):
- `gui/dialog_window.py`
- `gui/window_ui/CustomDialog.py`

## Implementation principles
1. **Deterministic Tab order**: each window defines and applies an explicit tab chain.
2. **No hidden shortcuts**: avoid overriding `keyPressEvent` for app shortcuts unless strictly necessary.
3. **Shortcut consistency**: same key combos do the same kind of action across windows.
4. **Incremental commits**: each commit completes a coherent slice and is testable.

---

## Commit plan (incremental)

### Commit 1 — Add shared keyboard utility
**Goal**: introduce a reusable helper for Tab order and shortcuts without changing window behavior yet.

**Add**: `gui/a11y_keyboard.py`

**Requirements**
- Provide a function to apply a tab chain:
  - `apply_tab_order(widgets: list[QtWidgets.QWidget]) -> None`
  - Must skip `None` values safely and warn/log if a widget is not focusable.
- Provide focus-policy helpers:
  - `set_focus_policies(focus: list[QWidget], no_focus: list[QWidget]) -> None`
  - Use `Qt.StrongFocus` for interactive controls, `Qt.NoFocus` for decorative widgets.
- Provide shortcut helper:
  - `add_shortcut(parent: QWidget, key: QKeySequence | str, callback: Callable, context=Qt.ApplicationShortcut) -> QShortcut`

**Checklist**
- [ ] `gui/a11y_keyboard.py` exists.
- [ ] No behavior changes in the app yet.
- [ ] Type hints and short docstrings included.

### Commit 2 — Main window: explicit Tab order (v1)
**Goal**: fix main window Tab order end-to-end.

**Modify**: `gui/main_window.py`

**Implementation steps**
1. Add `__init_keyboard_nav()` called at the end of `__init__` (after UI is fully set up).
2. Build a `tab_order` list in the intended workflow order:
   - Game selection / app language (if focusable)
   - Game path: line edit -> select button -> open button
   - Mod original path: line edit -> select button -> open button
   - Previous translation path: line edit -> select button -> open button
   - Target/output path: line edit -> select button -> open button
   - Translator source/target language combo boxes
   - Need-translate checkbox and related buttons
   - (Temporarily) scroll area widget itself
   - Disable-original-line checkbox
   - Run
   - Discord/Donate links
3. Apply tab order with `apply_tab_order(tab_order)`.
4. Set initial focus to `game_directory_lineEdit`.

**Checklist**
- [ ] `__init_keyboard_nav()` exists and is called.
- [ ] Tab order is stable and predictable.
- [ ] Initial focus is on the first meaningful control.

### Commit 3 — Main window: standard shortcuts (replace keyPressEvent)
**Goal**: implement discoverable shortcuts; remove the current single-key `R` handler.

**Modify**: `gui/main_window.py`

**Implementation steps**
1. Replace `keyPressEvent` shortcut logic with `QShortcut`/`QAction`.
2. Add shortcuts (minimum set):
   - `Ctrl+R` => Run (`run_pushButton.click()`)
   - `Alt+G` => focus `game_directory_lineEdit`
   - `Alt+M` => focus `original_directory_lineEdit`
   - `Alt+P` => focus `previous_directory_lineEdit`
   - `Alt+T` => focus `target_directory_lineEdit`
   - `Alt+U` => click `update_need_translation_area_pushButton`
3. Menu shortcut for Settings action:
   - Prefer `Ctrl+,` (common) OR `Alt+S` (if not conflicting). Choose one and document it.
4. Ensure shortcuts remain valid after `__change_language()` rebuilds the menubar.

**Checklist**
- [ ] `keyPressEvent` no longer triggers Run on plain `R`.
- [ ] Shortcuts work regardless of current focus (use ApplicationShortcut).
- [ ] Settings shortcut still works after switching program language.

### Commit 4 — Main window: ScrollArea checkbox navigation policy
**Goal**: prevent focus chaos when checkbox list is rebuilt.

**Modify**: `gui/main_window.py`

**Decision required (pick ONE approach)**
- **Approach A (recommended)**: Tab enters the area once; arrow keys move between checkboxes.
- **Approach B**: Tab iterates through every checkbox.

**Implementation steps (Approach A)**
1. In `__form_checkbox_cascade()`, store created checkboxes in `self.__need_translate_checkboxes` in creation order.
2. Install an eventFilter or per-checkbox key handler for Up/Down:
   - Up => focus previous checkbox
   - Down => focus next checkbox
3. Ensure that rebuilding the scroll area re-installs the handlers and updates `self.__need_translate_checkboxes`.
4. Ensure Tab order jumps from the “controls above” to the first checkbox (or the scroll area container) and then out to “disable_original_line_checkBox”.

**Checklist**
- [ ] After clicking “Update”, focus navigation still works.
- [ ] Arrow keys move within checkbox list without leaving it.
- [ ] Tab exits the section predictably.

### Commit 5 — Settings window: Tab order + close/save shortcuts
**Goal**: consistent keyboard navigation in Settings.

**Modify**: `gui/settings_window.py`, `gui/window_ui/SettingsWindow.py`

**Implementation steps**
1. Define a deterministic `tab_order` and apply it.
2. Add shortcuts:
   - `Esc` => close dialog
   - `Ctrl+S` => save/apply (only if there is a save/apply action)

**Checklist**
- [ ] Tab order is logical.
- [ ] Esc closes.
- [ ] Ctrl+S saves/applies (if supported).

### Commit 6 — AddAccountData window: Tab order + close/confirm shortcuts
**Goal**: consistent keyboard navigation in AddAccountData.

**Modify**: `gui/add_account_data_window.py`, `gui/window_ui/AddAccountData.py`

**Implementation steps**
1. Apply `tab_order` (service selector -> API key -> OK -> Cancel).
2. Add shortcuts:
   - `Esc` => cancel/close
   - `Enter` => confirm (only if safe and already expected)

**Checklist**
- [ ] Focus starts at the first editable field.
- [ ] Esc closes.
- [ ] Enter confirms (if implemented).

### Commit 7 — Stat/Table windows: define focus policy (minimal)
**Goal**: avoid trapping the user in a table with Tab.

**Modify**: `gui/stat_table_window.py`, `gui/window_ui/StatTableWindow.py`, `gui/window_ui/BaseTable.py`

**Choose one**
- Minimal: table not focusable by Tab; only action buttons are in tab order.
- Full: implement keyboard navigation in the table.

**Checklist**
- [ ] Tab does not get trapped.
- [ ] Esc closes (if window is modal).

---

## Global checklist (update per commit)
- [ ] Commit 1 merged.
- [ ] Commit 2 merged.
- [ ] Commit 3 merged.
- [ ] Commit 4 merged.
- [ ] Commit 5 merged.
- [ ] Commit 6 merged.
- [ ] Commit 7 merged.
