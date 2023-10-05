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
from acessar import AcessarObra

SQL: Path = Path()


class Centro(QScrollArea):
    def __init__(self, window: QMainWindow, sqlCaminho: Path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current: Itens
        self.parents = window

        global SQL
        SQL = sqlCaminho

    def mudarJanela(self, janela: str, qtdColunas: int = 3,
                    cadastrar: bool = False) -> None:
        if cadastrar:
            janelaAtiva = Itens(
                self, janela, qtdColunas=qtdColunas, cadastrar=True)
            self.setJanela(janelaAtiva)
            return
        janelaAtiva = Itens(self, janela, qtdColunas=qtdColunas)
        self.setJanela(janelaAtiva)

    def setJanela(self, classe: QWidget) -> None:
        try:
            self.current.delete()
        except AttributeError:
            ...
        self.setWidget(classe)
        self.current = classe  # type: ignore
        self.setWidgetResizable(True)

    def acessarObras(self):
        acesso = AcessarObra(self)
        self.setJanela(acesso)

    def acessarMateriais(self):
        attr = getattr(self, "acessarMateriais")
        print(attr.__name__)

    def acessarClientes(self):
        print("Acessado")

    def acessarPessoal(self):
        print("Acessado")


class Itens(QWidget):
    def __init__(self, parent: Centro, table: str, qtdColunas: int,
                 cadastrar=False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.threadbool = True
        self.cabecalho: list[tuple[str]]
        self.cabecalho_nomes: list[str]

        # Inicializa as variáveis recebidas
        self.boolCadastrar = cadastrar
        self.parents = parent
        self.table = table
        self.qtdColunas = qtdColunas

        # Busca o cabeçalho
        with SqlReader(SQL, CODE) as arquivo:
            self.cabecalho = arquivo.getCabec(self.table)

        # Filtra para que só apareça o nome de cada coluna da tabela APENAS
        self.cabecalho_nomes = [a[1] for a in self.cabecalho]  # type: ignore

        # filtra para mostrar apenas as colunas "Id" e "Nome"
        self.cabecalho_nomes_limitado = self.cabecalho_nomes[:self.qtdColunas]
        if self.boolCadastrar:
            self.cadastro = Cadastro(
                self.table, self.cabecalho_nomes, SQL,
                qtdColunas=self.qtdColunas, parent=self)
            self.setLayout(self.cadastro)
            return
        self.adicionaLayoutPadrao()
        # self.atualizaThread = Thread(target=self.atualizaAuto)
        # self.atualizaThread.start()

    # def atualizaAuto(self) -> None:
    #     while (self.threadbool):
    #         tempo = time()
    #         self.atualizaInfo()
    #         while (time()-tempo < 10 and self.threadbool):
    #             ...

    def adicionaLayoutPadrao(self):
        # Inicializa o layout da classe
        self._layout = QVBoxLayout()

        # Inicializa a barra de busca da janela
        self.busca = Buscador(self, self.cabecalho_nomes_limitado)

        # Inicializa o buscador
        self._layout.addWidget(self.busca)

        # Inicializa o cabeçalho com uma lista com todos os nomes das colunas
        self.cabecalho_widget = Cabeçalho(self.cabecalho_nomes, self.table,
                                           self.qtdColunas, parent=self)

        self._layout.addWidget(self.cabecalho_widget)

        # Inicializa e alinha o layout
        self.setLayout(self._layout)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.botao.setFixedWidth(self.width())

        # Atualiza os itens na tela, excluindo os antigos e adicionando novos
        self.atualizaInfo()

    def delete(self):
        self.threadbool = False
        for i in self.linhas:
            i.delete()
        if self.boolCadastrar:
            self.cadastro
        self.cabecalho_widget.deleteLater()
        self.busca.delete()
        self.busca.deleteLater()
        self.deleteLater()

    def atualizaInfo(self, filter: str | None = None, table: str | None = None
                     ):
        """
        Atualiza as linhas da janela Itens
        """
        self.info2: list = []
        self.info: list[tuple[str]]

        try:
            for a in self.linhas:
                a.delete()
        except AttributeError:
            pass

        # Define o tipo das linhas
        self.linhas: list[Linha] = []

        # busca as informações da tabela sql fornecida
        with SqlReader(SQL, CODE) as arquivo:
            self.info = arquivo.getInfo(self.table)

        # Se o filtro existir, ele só exibe as linhas com as especificações
        # escolhidas
        if filter is not None and table is not None:
            filter = filter.lower()

            for i in self.info:
                if (str(filter) in str(
                    i[self.cabecalho_nomes_limitado.index(table)]).lower()
                        and i not in self.info2):
                    self.info2.append(i)
        else:
            self.info2 = self.info.copy()

        # Adiciona as linhas com todas as informações coletadas
        for i in self.info2:
            # Filtra para mostrar apenas id e nome
            i = i[:self.qtdColunas]  # type: ignore

            # Adiciona as linhas em uma lista para melhor manuseio delas
            self.linhas.append(Linha(self, list(i), self.table))
            self._layout.addWidget(self.linhas[-1])
            self.adjustSize()


class Cabeçalho(QWidget):
    def __init__(self, cabecalho_nomes: list[str], table: str, qtdColunas,
                 parent: Itens) \
            -> None:
        self.qtdColunas = qtdColunas
        """
        Inicia o cabeçalho dentro da janela Itens
        """
        super().__init__()
        self.parents = parent
        self._layout = QHBoxLayout()
        self.espaco = QLabel()
        self.adicionar = QPushButton("Cadastrar")
        self.cabecalho_nomes = cabecalho_nomes  # Indica os itens do cabeçalho
        self.table = table
        self.adicionar.clicked.connect(self.cadastro)

        self.espaco.setFixedWidth(WIDTH_BOTAO)
        self.adicionar.setFixedWidth(WIDTH_BOTAO)
        self.setLayout(self._layout)

        lista_labels: list[QLabel] = []

        for i in self.cabecalho_nomes[:qtdColunas]:
            lista_labels.append(QLabel(i))
            self._layout.addWidget(lista_labels[-1])
            lista_labels[-1].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self.espaco)
        self._layout.addWidget(self.adicionar)
        lista_labels[0].setFixedWidth(WIDTH_ID)

    def cadastro(self):
        # cadastrar = Cadastro(self.table, self.cabecalho_nomes, self)
        self.parents.parents.mudarJanela(self.table,
                                         qtdColunas=self.qtdColunas,
                                         cadastrar=True)


class Linha(QWidget):
    """
    Define a linha da janela Itens
    """

    def __init__(self, parent: Itens, lista: list[str], table: str, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.parents = parent
        self.table = table
        self.labels: list[QLabel] = []
        self._layout = QHBoxLayout()
        self.setFixedHeight(HEIGHT_ITENS)

        for i in lista:
            self.labels.append(QLabel(str(i)))
            # self.labels[-1].setFixedWidth(int(parent.width()/(len(lista))-1))
            self._layout.addWidget(self.labels[-1])
            self.labels[-1].setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.labels[0].setFixedWidth(WIDTH_ID)

        self.X = QPushButton("X")
        self.entrar_usuario = QPushButton("Acessar")

        # self.text.setFixedWidth(parent.width())
        self.X.setFixedWidth(WIDTH_BOTAO)

        self.entrar_usuario.setFixedWidth(WIDTH_BOTAO)
        self.X.clicked.connect(self.deleteItemInfo)
        self.entrar_usuario.clicked.connect(self.acessar)

        self._layout.addWidget(self.entrar_usuario)
        self._layout.addWidget(self.X)
        self.setLayout(self._layout)
        self.parents.adjustSize()

    def deleteItemInfo(self):
        """Apaga as informações tanto do programa quanto na tabela em sql"""
        with SqlReader(SQL, CODE) as arquivo:
            arquivo.delInfo(self.table, int(self.labels[0].text()))
        for i in self.labels:
            i.deleteLater()
        self.X.deleteLater()
        self._layout.deleteLater()
        self.deleteLater()
        self.parents.linhas.remove(self)

    def acessar(self):
        attr = getattr(self.parents.parents,
                       f"acessar{self.table.capitalize()}")
        attr()

    def delete(self):
        """Deleta apenas o Widget, sem afetar informações salvas"""
        for i in self.labels:
            i.deleteLater()
        self.X.deleteLater()
        self._layout.deleteLater()
        self.deleteLater()


class Buscador(QWidget):
    def __init__(self, parent: Itens, cabecalho: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inicializa os componentes do buscador
        self.buscador_text = LinhaBuscador(self)
        self.combo_box = QComboBox()
        self._layout = QHBoxLayout()
        self.parents = parent

        self.combo_box.addItems(cabecalho)
        self.combo_box.currentIndexChanged.connect(
            self.buscador_text.ativaAtualizaInfo)
        # self.buscador_botao = QPushButton("Buscar")
        # self.buscador_botao.clicked.connect(self.decoratorBuscador(
        #     self.parents.atualizaInfo, self.buscador_text.text))

        self._layout.addWidget(self.buscador_text)
        self._layout.addWidget(self.combo_box)
        # self._layout.addWidget(self.buscador_botao)
        self.buscador_text.setPlaceholderText("Pesquisar")
        self.setLayout(self._layout)

    def delete(self):
        self.buscador_text.deleteLater()
        self.combo_box.deleteLater()
        self._layout.deleteLater()
        self.deleteLater()

    # def decoratorBuscador(self, func, func2, *args, **kwargs):
    #     def decorado():
    #         print(func2())
    #         func(func2())
    #     return decorado


class LinhaBuscador(QLineEdit):
    def __init__(self, parent: Buscador, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parents = parent

    def ativaAtualizaInfo(self):
        self.parents.parents.atualizaInfo(
            self.parents.buscador_text.text(),
            self.parents.combo_box.currentText())

    def keyPressEvent(self, arg__1: QKeyEvent) -> None:
        KEYS = Qt.Key

        # Atualiza os itens de acordo com o que esta escrito no buscador_text
        # cada vez que um número ou letra é digitado
        if (arg__1.text().isalpha() or arg__1.key() in [KEYS.Key_Backspace] or
           arg__1.text().isalnum()):
            super().keyPressEvent(arg__1)
            self.ativaAtualizaInfo()
            return
        return super().keyPressEvent(arg__1)
