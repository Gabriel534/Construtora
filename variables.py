from pathlib import Path
import pyautogui as p

sizeScreen = p.size()
WINDOW_WIDTH = sizeScreen.width - 100
WINDOW_HEIGHT = int(sizeScreen.height*2/3)
# Fixa a largura da linha do cadastro
CADASTRAR_LINE_WIDTH = sizeScreen.width/2
# Fixa a largura do botal "salvar" do cadastro
CADASTRAR_SALVAR_BUTTON = int(sizeScreen.width)/7
CADASTRAR_VOLTAR_BUTTON = int(sizeScreen.width/28)
# CADASTRAR_HEIGHT = 400
WIDTH_MENU = 0.15  # Porcentagem
WIDTH_APP_CENTRAL = 0.98-WIDTH_MENU  # Porcentagem

TAMANHO_BOTAO_TELAS = int(sizeScreen.width/14)

# Tamanho do de um botão do menu esquerdo
# Usado para dar o espaçamento entre os botôes superior e inferior do menu
HEIGHT_ITENS = int(WINDOW_HEIGHT/12)
HEIGHT_PUSH_BUTTON = int(WINDOW_HEIGHT/15)

WIDTH_BOTAO = 120

PASTA_PROJETO = Path(__file__).parent
IMAGENS = PASTA_PROJETO / "Imagens"
DADOS = PASTA_PROJETO / "Dados"
SQL = DADOS / "servidor.sqlite3"

# Fornece o ícone do programa
ICON = IMAGENS / "Icon.png"

# Fornece o tamanho do botão Cadastrar do cabeçalho
SPACING_CABECALHO_CENTRO = int(sizeScreen.width/12.72)

# Tamanho da coluna do ID
WIDTH_ID = int(sizeScreen.width/28)

PRIMARY_COLOR = '#1e81b0'
DARKER_PRIMARY_COLOR = '#16658a'
DARKEST_PRIMARY_COLOR = '#115270'

# ------------------------------------------------------------------------------------------------------------------------------------
# Variáveis de login
LOGIN_WIDTH = int(sizeScreen.width/5)
LOGIN_HEIGHT = int(sizeScreen.height/4.99)
