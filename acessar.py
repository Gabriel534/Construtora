from typing import Optional
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QScrollArea, QMessageBox, QLineEdit, QComboBox, QSizePolicy)
from PySide6.QtCore import Qt, QEvent
from variables import (WIDTH_BOTAO, SPACING_CABECALHO_CENTRO,
                       WIDTH_ID, HEIGHT_ITENS)
from sql_create import CODE
from cadastro import Cadastro
from sql import SqlReader
from pathlib import Path


class AcessarObra(QWidget):
    def __init__(self, parent: QScrollArea, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parents = parent
        self._layout = QVBoxLayout()

        self.setLayout(self._layout)

    def delete(self):
        self.deleteLater()
