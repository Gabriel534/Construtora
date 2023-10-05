from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import (QApplication, QWidget, QMainWindow, QWidget,
                               QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QLineEdit,
                               QMessageBox)
from PySide6.QtGui import Qt, QIcon, QKeyEvent
from variables import (CADASTRAR_LINE_WIDTH, ICON,
                       CADASTRAR_SALVAR_BUTTON, CADASTRAR_VOLTAR_BUTTON)
from sql import SqlReader
from pathlib import Path
import re
SQL: Path = Path()


class Cadastro(QVBoxLayout):
    def __init__(self, table: str, cabecalho: list[str], sqlCaminho: Path,
                 qtdColunas: int, parent: QWidget, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.qtdColunas = qtdColunas
        self.parents = parent
        global SQL
        SQL = sqlCaminho
        # self.setWindowTitle("Cadastro")
        # icon = QIcon(str(ICON))
        # self.setWindowIcon(icon)
        # self.setMinimumWidth(CADASTRAR_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.linhas: list[Linha] = []
        self.table = table
        self.cabeçalho = cabecalho

        # central_width = QWidget()

        self.voltarButton = QPushButton("<-")
        self.voltarButton.setFixedWidth(CADASTRAR_VOLTAR_BUTTON)
        self.voltarButton.clicked.connect(self.retornar)

        self.addWidget(self.voltarButton)

        self.text = QLabel(f"Cadastro {self.table}")
        self.layoutText = QHBoxLayout()
        self.layoutText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutText.addWidget(self.text)
        self.addLayout(self.layoutText)

        self.cadastrarButton = QPushButton("Salvar")
        self.cadastrarButton.setFixedWidth(int(CADASTRAR_SALVAR_BUTTON))
        self.cadastrarButton.clicked.connect(self.cadastrar)

        self.layoutSalvarButton = QHBoxLayout()
        self.layoutSalvarButton.addWidget(self.cadastrarButton)
        self.layoutSalvarButton.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.adicionaLabels()
        self.addLayout(self.layoutSalvarButton)
        # self.parents.adjustSize()

    def adicionaLabels(self):
        for i in self.cabeçalho[1:]:
            self.linhas.append(Linha(i))
            self.linhas[-1].setFixedWidth(int(CADASTRAR_LINE_WIDTH))
            self.addWidget(self.linhas[-1])

    def cadastrar(self) -> None:
        self.itens: dict[str, str] = {}

        for a in self.linhas:
            self.itens[a.text.text()] = a.line.text()

        self.confirmacao = self.formataCampos(self.itens)
        msg = QMessageBox()

        if self.confirmacao is False:
            msg.setIcon(msg.Icon.Critical)
            msg.setText("Data inválida")
            msg.exec()
            return

        with SqlReader(SQL) as arquivo:
            try:
                arquivo.addInfo(self.table, **self.itens)
            except Exception as error:
                msg.setIcon(msg.Icon.Critical)
                msg.setText(str(error))
                msg.exec()
                return
            else:
                msg.setIcon(msg.Icon.Information)
                msg.setText("Dados salvos com sucesso!!!")
                msg.setStandardButtons(msg.StandardButton.Ok)
                msg.button(msg.StandardButton.Ok).clicked.connect(
                    self.retornar)
                msg.exec()

    def formataCampos(self, dict: dict[str, str]) -> bool:
        formatoData = re.compile(r'^(\d{2})/(\d{2})/(\d{4})$')

        for key, value in dict.items():
            if value == "":
                del dict[key]
                continue
            if "Data" in key.capitalize():
                try:
                    data = re.findall(formatoData, value)[0]
                except IndexError:
                    return False

                dict[key] = f"{data[0]}-{data[1]}-{data[2]}"
        self.itens = dict
        return True

    def delete(self):
        for a in self.linhas:
            a.delete()
        self.cadastrarButton.deleteLater()
        self.layoutSalvarButton.deleteLater()
        self.deleteLater()

    def retornar(self):
        self.parents.parents.mudarJanela(  # type: ignore
            self.table, qtdColunas=self.qtdColunas)  # type: ignore


class Linha(QWidget):
    def __init__(self, text: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._layout = QVBoxLayout()
        self.text = QLabel(text)
        # self.text.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.line = LineItem(text=text)

        self.setLayout(self._layout)
        self._layout.addWidget(self.text)
        self._layout.addWidget(self.line)

    def delete(self):
        self.text.deleteLater()
        self.line.deleteLater()
        self._layout.deleteLater()
        self.deleteLater()


class LineItem(QLineEdit):
    def __init__(self, text, *args, **kwags):
        super().__init__(*args, **kwags)
        self.teste = False
        self.texto = text
        self.setMaxLength(40)
        self.setInputMask("00/00/0000;_") if self.texto[:4] == "Data" else ...
        self.setInputMask(
            "000.000.000.00;_") if self.texto[:3] == "Cpf" else ...
        self.setInputMask(
            "(00)0000-0000;_") if self.texto[:8] == "Telefone" else ...

    def keyPressEvent(self, arg__1: QKeyEvent) -> None:
        KEYS = Qt.Key
        if arg__1.key() in [KEYS.Key_0, KEYS.Key_1, KEYS.Key_2, KEYS.Key_3,
                            KEYS.Key_4, KEYS.Key_5, KEYS.Key_6, KEYS.Key_7,
                            KEYS.Key_8, KEYS.Key_9]:
            if self.texto[:8] == "Telefone":
                texto = self.text()
                if len(self.text()) == 13 and self.text()[4:5] == "9":
                    self.setInputMask(
                        "(00)00000-0000;_")
                    text2 = f"{texto[:8]}{texto[9:10]}-\
                                 {texto[10:]}{arg__1.text()}"
                    self.setText(text2)
                    self.teste = True

        if arg__1.key() == KEYS.Key_Backspace and self.teste is True:
            super().keyPressEvent(arg__1)
            texto = self.text()
            self.teste = False
            self.setInputMask(
                "(00)0000-0000;_")
            self.setText(texto)
            return
        return super().keyPressEvent(arg__1)
