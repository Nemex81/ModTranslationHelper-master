from collections.abc import Callable

from PyQt5 import QtCore, QtGui, QtWidgets
from loguru import logger


def apply_tab_order(widgets: list[QtWidgets.QWidget]) -> None:
    """Apply an explicit tab chain, skipping None and non-focusable widgets."""
    previous_widget: QtWidgets.QWidget | None = None
    for widget in widgets:
        if widget is None:
            continue
        if not widget.focusPolicy() & QtCore.Qt.TabFocus:
            logger.warning(f'Skip non-focusable widget in tab order: {widget.objectName() or type(widget).__name__}')
            continue
        if previous_widget is not None:
            QtWidgets.QWidget.setTabOrder(previous_widget, widget)
        previous_widget = widget


def set_focus_policies(focus: list[QtWidgets.QWidget], no_focus: list[QtWidgets.QWidget]) -> None:
    """Set focus policies for interactive and decorative widgets."""
    for widget in focus:
        if widget is None:
            continue
        widget.setFocusPolicy(QtCore.Qt.StrongFocus)
    for widget in no_focus:
        if widget is None:
            continue
        widget.setFocusPolicy(QtCore.Qt.NoFocus)


def add_shortcut(parent: QtWidgets.QWidget, key: QtGui.QKeySequence | str, callback: Callable,
                context: QtCore.Qt.ShortcutContext = QtCore.Qt.ApplicationShortcut) -> QtWidgets.QShortcut:
    """Create a shortcut with a consistent context and return it."""
    sequence = key if isinstance(key, QtGui.QKeySequence) else QtGui.QKeySequence(key)
    shortcut = QtWidgets.QShortcut(sequence, parent)
    shortcut.setContext(context)
    shortcut.activated.connect(callback)
    return shortcut
