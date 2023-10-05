from typing import Optional
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QScrollArea, QMessageBox, QLineEdit)
from PySide6.QtCore import Qt
from sys import argv
from main_ import Construtora
from variables import (ICON, LOGIN_HEIGHT, LOGIN_WIDTH, SQL)


class Login(QMainWindow):
    def __init__(self, icon: QIcon, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.icon = icon
        self._login: str = "sdffdsfds"
        self.senha: str = ""
        self.setWindowIcon(self.icon)
        self.setFixedSize(LOGIN_WIDTH, LOGIN_HEIGHT)
        centralWidget = QWidget()
        _layout = QVBoxLayout()
        self.bemVindoText = QLabel("Seja bem vindo de volta!")
        self.loginText = QLabel("Login:")
        self.loginLine = QLineEdit()
        self.senhaText = QLabel("Senha:")
        self.senhaLine = QLineEdit()
        self.loginLayout = QHBoxLayout()
        self.loginButton = QPushButton("Login")
        self.cadastrarButton = QPushButton("Cadastre-se")
        self.loginLayout.addWidget(self.cadastrarButton)
        self.loginLayout.addWidget(self.loginButton)
        self.loginButton.clicked.connect(self.login)
        self.loginLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        _layout.addWidget(self.bemVindoText)
        _layout.addWidget(self.loginText)
        _layout.addWidget(self.loginLine)
        _layout.addWidget(self.senhaText)
        _layout.addWidget(self.senhaLine)
        _layout.addLayout(self.loginLayout)
        centralWidget.setLayout(_layout)
        self.setCentralWidget(centralWidget)

    def login(self):
        self._login = self.loginLine.text()
        self.senha = self.senhaLine.text()
        if self._login != "" and self.senha != "":
            self.construtora = Construtora(self.icon, self._login, self.senha)
            self.construtora.show()
            self.close()
            return
        self.bemVindoText.setText("Login ou senha incorretos")


if __name__ == "__main__":
    app = QApplication(argv)
    icon = QIcon(str(ICON))
    app.setWindowIcon(icon)
    # from styles import setupTheme
    # setupTheme()
    window = Login(icon)
    window.show()
    app.setStyle("Fusion")
    app.exec()
