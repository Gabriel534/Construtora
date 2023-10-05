from typing import Optional
from PySide6.QtGui import QPixmap, QIcon, QAction, QPalette, QColor
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QScrollArea, QMessageBox, QToolBar)
from PySide6.QtCore import Qt, QEvent, QSize
from sys import argv
from typing import cast
from variables import (WIDTH_MENU, WIDTH_APP_CENTRAL,
                       WINDOW_WIDTH, WINDOW_HEIGHT, HEIGHT_PUSH_BUTTON,
                       ICON, DADOS)
from pprint import pprint
from sql import SqlReader
from funcionalidades import Centro
SQL = DADOS


class Construtora(QMainWindow):
    def __init__(self, icon: QPixmap | QIcon, username: str, password: str,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Construtora")
        self.username = username
        self.password = password

        global SQL
        SQL = DADOS / f"{self.username}.sqlite3"

        self.setWindowIcon(icon)

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.central_widget = QWidget()
        layout = QHBoxLayout()
        self.menu_esquerdo = Menu(window=self)
        self.app_central = AppCentral(self)

        # self.menu = self.menuBar()
        # self.item1 = self.menu.addMenu("menu")
        # self.action = self.item1.addAction("Menu1")

        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)
        layout.addWidget(self.menu_esquerdo)
        layout.addWidget(self.app_central)
        self.adjustSize()

    # def keyPressEvent(self, event) -> None:
    #     if event.key() == Qt.Key.Key_Enter:
    #         print("Foi")
    #     return super().keyPressEvent(event)

    def ativaJanela(self, janela: QMainWindow):
        janela.show()


class AppCentral(QWidget):
    def __init__(self, parent: Construtora, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parents = parent
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.menubar = MenuBar(self)
        self.centro = Centro(self.parents, SQL)
        self._layout.addWidget(self.menubar)
        self._layout.addWidget(self.centro)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)


class MenuBar(QWidget):
    def __init__(self, parent: AppCentral, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parents = parent
        self._layout = QHBoxLayout()
        user = QLabel(f"Usuário: {self.parents.parents.username}")

        self.setLayout(self._layout)
        self._layout.addWidget(user)


class Menu(QWidget):
    def __init__(self, window: Construtora, *args, **kwargs)\
            -> None:
        super().__init__(*args, **kwargs)
        self.janela = window
        self.botoes: dict[str, QPushButton]

        self.botoes = {"obras": QPushButton("Obras"),
                       "clientes": QPushButton("Clientes"),
                       "pessoal": QPushButton("Pessoal"),
                       "materiais": QPushButton("Materiais"),
                       "submenu_compartilhe": QPushButton("Compartilhe"),
                       "submenu_contato": QPushButton("Contato"),
                       "submenu_ajuda": QPushButton("Ajuda")}

        self.itens = QVBoxLayout()

        self.cont_submenu = 0

        for key, value in self.botoes.items():
            if key[:8] != "submenu_":
                value.clicked.connect(getattr(self, key))
                value.setCheckable(True)
                self.itens.addWidget(value)
            else:
                self.cont_submenu += 1

        self.itens.addSpacing(
            self.height()-(self.cont_submenu*HEIGHT_PUSH_BUTTON))

        for key, value in self.botoes.items():
            if key[:8] == "submenu_":
                value.clicked.connect(getattr(self, key[8:]))
                self.itens.addWidget(value)

        self.setLayout(self.itens)

        self.ajusteTamanho()

    def tirarChecagem(self):
        for value in self.botoes.values():
            value.setChecked(False)

    def ajusteTamanho(self) -> None:
        self.setFixedSize(int(WIDTH_MENU*self.janela.width()),
                          self.janela.height())
        # for key, value in self.botoes.items():
        #     value.setFixedWidth(int(WIDTH_MENU*self.janela.width()))
        self.itens.setAlignment(Qt.AlignmentFlag.AlignTop)

    def obras(self):
        self.janela.app_central.centro.mudarJanela("Obras")
        self.tirarChecagem()
        self.botoes['obras'].setChecked(True)

    def pessoal(self):
        self.janela.app_central.centro.mudarJanela("Pessoa")
        self.tirarChecagem()
        self.botoes['pessoal'].setChecked(True)

    def clientes(self):
        self.janela.app_central.centro.mudarJanela("Clientes")
        self.tirarChecagem()
        self.botoes['clientes'].setChecked(True)

    def materiais(self):
        self.janela.app_central.centro.mudarJanela("Materiais", qtdColunas=5)
        self.tirarChecagem()
        self.botoes['materiais'].setChecked(True)

    def compartilhe(self):
        ...

    def contato(self):
        msg = QMessageBox()
        msg.setWindowTitle("Contato")
        msg.setText(
            "Email: gsampaiosantos537@gmail.com\nTelefone: (35) 98273-2938")
        msg.setIcon(msg.Icon.NoIcon)
        msg.exec()

    def ajuda(self):
        import webbrowser

        # Define a URL do Google
        url = "https://www.google.com"

        # Define o caminho do executável do Chrome
        chrome_path = "C:\Program Files\Google\Chrome\Application/chrome.exe"

        # Registra o caminho do executável do Chrome
        webbrowser.register(
            'chrome', None, webbrowser.BackgroundBrowser(chrome_path))

        # Abre a URL no Chrome
        webbrowser.get('chrome').open_new_tab(url)


def style(qApp: QApplication):
    qApp.setStyle("Fusion")
    dark_palette = QPalette()

    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(
        QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

    qApp.setPalette(dark_palette)

    qApp.setStyleSheet(
        "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px \
        solid white; }")


if __name__ == "__main__":
    from qt_material import apply_stylesheet
    app = QApplication(argv)
    icon = QIcon(str(ICON))
    app.setWindowIcon(icon)
    # from styles import setupTheme
    # setupTheme()
    app.setStyle("Fusion")
    # apply_stylesheet(app, theme='dark_amber.xml')

    window = Construtora(icon, "servidor", "a")
    window.show()
    # style(app)  # dark fusion

    app.exec()
