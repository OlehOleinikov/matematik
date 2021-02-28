from PyQt5.QtCore import Qt, QMetaObject, pyqtSignal, pyqtSlot, QEvent
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton,
                            QLabel, QSizePolicy)
from gui.gui_import_folder import Ui_modal_win_choose_import_folder


class HardWinClass(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._w = Ui_modal_win_choose_import_folder()
        self.setupUi()

        contentLayout = QHBoxLayout()
        # # contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.addWidget()

        self.windowContent.setLayout(contentLayout)

        # self.setWindowTitle(self._w.windowTitle())
        # self.setGeometry(self._w.geometry())

    def setupUi(self):
        self.windowContent = QWidget(self.windowFrame)
        self.vboxFrame.addWidget(self.windowContent)
'''
        # Adding attribute to clean up the parent window when the child is closed
        self._w.setAttribute(Qt.WA_DeleteOnClose, True)
        self._w.destroyed.connect(self.__child_was_closed)
'''

