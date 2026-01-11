from PyQt5 import QtWidgets, QtGui, QtCore
from deep_translator.exceptions import ServerException
from deepl import AuthorizationException
from loguru import logger

from gui.a11y_keyboard import add_shortcut, apply_tab_order, set_focus_policies
from gui.dialog_window import CustomDialog
from gui.window_ui.AddAccountData import Ui_Dialog
from main import TranslatorAccount

import qtawesome as qta

from translators.translator_manager import TranslatorManager


class AddAccountDataWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, title=None, icon=None, api_name=None, account_data: TranslatorAccount = None):
        super(AddAccountDataWindow, self).__init__(parent=parent)
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.__shortcuts: list[QtWidgets.QShortcut] = []
        if title:
            self.setWindowTitle(title)
        if icon:
            self.setWindowIcon(icon)
        self.__ui.save_pushButton.setEnabled(False)
        self.__ui.save_pushButton.setAutoDefault(False)

        self.__api_name = api_name
        self.__account = account_data
        self.__ui.api_key_lineEdit.setText(account_data.get_translator_account(api_name).get('api_key', ''))
        self.__validate_key()

        self.__change_icon()
        self.__init_keyboard_nav()
        self.__init_shortcuts()

        self.__ui.api_key_lineEdit.editingFinished.connect(self.__validate_key)
        self.__ui.save_pushButton.clicked.connect(self.__save_key)

    def __init_keyboard_nav(self):
        focus_widgets = [
            self.__ui.api_key_lineEdit,
            self.__ui.save_pushButton,
        ]
        no_focus_widgets = [self.__ui.api_key_label]
        set_focus_policies(focus_widgets, no_focus_widgets)
        apply_tab_order(focus_widgets)
        self.__ui.api_key_lineEdit.setFocus()

    def __init_shortcuts(self):
        self.__shortcuts = [
            add_shortcut(self, 'Esc', self.close, context=QtCore.Qt.WidgetWithChildrenShortcut),
            add_shortcut(self, 'Return', self.__ui.save_pushButton.click,
                         context=QtCore.Qt.WidgetWithChildrenShortcut),
        ]

    def __change_icon(self):
        if self.__key_validation:
            icon_name = 'fa5.check-circle'
        else:
            icon_name = 'fa5.times-circle'
        if self.__ui.horizontalLayout.itemAt(1):
            icon = self.__ui.horizontalLayout.itemAt(1).widget()
            icon.setPixmap(qta.icon(icon_name).pixmap(QtCore.QSize(16, 16)))
        else:
            icon = QtWidgets.QLabel()
            icon.setPixmap(qta.icon(icon_name).pixmap(QtCore.QSize(16, 16)))
            self.__ui.horizontalLayout.addWidget(icon)

    def __validate_key(self):
        try:
            if self.__ui.api_key_lineEdit.text():
                exception = TranslatorManager(api_key=self.__ui.api_key_lineEdit.text(),
                                              api_service=self.__api_name).raise_authorization_exception()
                if isinstance(exception, AuthorizationException):
                    raise exception
                self.__key_validation = True
                self.__ui.save_pushButton.setEnabled(True)
            else:
                self.__key_validation = False
                error = CustomDialog(text='Введите ключ!')
                error.exec_()
                self.__key_validation = False
        except (ServerException, AuthorizationException) as error:
            logger.warning(f'{error}')
            self.__key_validation = False
            error = CustomDialog(text=f'Ключ {self.__ui.api_key_lineEdit.text()} недействителен!')
            error.exec_()

        self.__change_icon()

    def __save_key(self):
        self.__account.add_new_account(translator_name=self.__api_name, api_key=self.__ui.api_key_lineEdit.text())
        self.__account.save_accounts()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if not self.__key_validation:
            self.parent().set_default()
        super(AddAccountDataWindow, self).closeEvent(a0)
