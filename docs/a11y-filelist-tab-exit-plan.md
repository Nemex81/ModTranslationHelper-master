# A11Y/Keyboard plan: Tab exits file list (checkboxes)

## Scope (IMPORTANT)
This plan is about **keyboard navigation** for the dynamic “files to translate” list (checkboxes inside `need_translate_scrollArea`).
It must not affect translation logic, i18n, or Qt-generated UI code.

### In scope
- `Tab` behavior when entering/exiting the dynamic checkbox list.
- Keeping **Up/Down arrows** as the primary navigation inside the list.
- Handling the edge case where the list is empty.

### Out of scope (DO NOT TOUCH)
- Mod/game translation pipeline (`TranslatorManager`, language selectors, file parsing).
- Qt-generated files (`gui/window_ui/*`).
- Global tab order structure in `__init_keyboard_nav()` except where explicitly stated.

---

## Problem statement
Currently, once focus enters the file list area, `Tab` can get “stuck” moving among many checkbox items (or otherwise failing to leave the list reliably).
This makes fast navigation impossible, especially with screen readers.

---

## Target UX behavior
1. When the user tabs to the file list area (`need_translate_scrollArea`), focus should immediately move to the **first checkbox** (if any).
2. When focus is on a checkbox:
   - `Tab` should **exit the list immediately** and go to the next widget in the GUI.
   - `Shift+Tab` should go to the previous widget in the GUI.
3. Inside the list, checkboxes should be navigated **only** via:
   - `Up` / `Down` arrows.
4. If the list is empty, `Tab` must not get stuck in the list area; focus should move to the next widget.

---

# Incremental commit plan

## Commit 1 — Remove TabFocus from dynamic checkboxes
### Goal
Make the dynamic checkboxes **not part of the Tab chain**, while still allowing focus via click and `setFocus()`.

### Files
- `gui/main_window.py`

### Implementation steps
In `MainWindow.__form_checkbox_cascade()` after creating each checkbox:
- Add `check_box.setFocusPolicy(QtCore.Qt.ClickFocus)`

Notes:
- `ClickFocus` keeps checkboxes focusable by mouse click and by programmatic `setFocus()`.
- This does **not** break the existing arrow-key navigation implementation.

### Checks
- Tab to file list area still lands on the first checkbox (because focus is set programmatically).
- Tab does not iterate through every checkbox item.

### Commit message
`a11y: remove TabFocus from dynamic file checkboxes`

---

## Commit 2 — Make Tab/Shift+Tab exit the checkbox list
### Goal
When focus is on a checkbox, Tab should move to the next GUI widget immediately.

### Files
- `gui/main_window.py`

### Implementation steps
In `MainWindow.eventFilter()` in the branch handling checkbox keypress events:
- If `event.key() == QtCore.Qt.Key_Tab`:
  - call `self.focusNextChild()`
  - `return True`
- If `event.key() == QtCore.Qt.Key_Backtab`:
  - call `self.focusPreviousChild()`
  - `return True`
- Keep existing handling for `Key_Up`/`Key_Down` unchanged.

### Checks
- While focused on any checkbox:
  - Pressing Tab moves focus to the next widget in the defined tab order.
  - Pressing Shift+Tab moves focus to the previous widget.
- Up/Down still move between checkboxes.

### Commit message
`a11y: make Tab/Shift+Tab exit the file checkbox list`

---

## Commit 3 — Empty list: skip the list area on focus
### Goal
If there are no checkboxes, entering the list area should not trap focus.

### Files
- `gui/main_window.py`

### Implementation steps
In `MainWindow.eventFilter()` where it handles:
- `watched is self.__ui.need_translate_scrollArea` and `event.type() == QtCore.QEvent.FocusIn`

Replace the unconditional focus call with:
- If `self.__need_translate_checkboxes` is non-empty:
  - focus the first checkbox (existing behavior)
- Else (empty):
  - call `self.focusNextChild()`
  - return `True`

### Checks
- With an empty file list, Tab does not stop on the scroll area.
- Focus moves directly to the next widget.

### Commit message
`a11y: skip empty file list area in Tab navigation`

---

# Progress checklist (track per commit)

## Commit 1
- [ ] `__form_checkbox_cascade()` sets `ClickFocus` on every dynamic checkbox.
- [ ] Manual test: Tab reaches file list, focus lands on first checkbox.
- [ ] Manual test: Tab does not traverse checkbox-by-checkbox.

## Commit 2
- [ ] `eventFilter()` handles `Key_Tab` on checkboxes via `focusNextChild()`.
- [ ] `eventFilter()` handles `Key_Backtab` on checkboxes via `focusPreviousChild()`.
- [ ] Manual test: Tab exits list immediately.
- [ ] Manual test: Shift+Tab exits backward.
- [ ] Manual test: Up/Down still navigate checkbox list.

## Commit 3
- [ ] `eventFilter()` checks for empty checkbox list on `need_translate_scrollArea` FocusIn.
- [ ] Manual test: with empty list, focus moves to next widget (no trap).

## Mandatory regression checks (every commit)
- [ ] No edits to `gui/window_ui/*`.
- [ ] `__init_keyboard_nav()` tab order list unchanged.
- [ ] No changes to mod translation pipeline (`TranslatorManager`, parsing, output generation).
