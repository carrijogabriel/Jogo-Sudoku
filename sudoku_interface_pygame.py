#Parte gráfica do jogo - com Claude 

import pygame
import sys
import numpy as np
from jogo_main import gerar_jogo_inicial_aleatorio, sudoku_legivel, verificar_sudoku, resolvendo_sudoku

"""
Sudoku Interface com Pygame

Este arquivo cria uma interface gráfica completa para jogar Sudoku usando Pygame.

Funcionalidades:
- Gera jogo inicial aleatório chamando sudoku.py
- Grid 9x9 com blocos 3x3 visualmente separados por linhas mais grossas
- Números iniciais (fixos) em cinza, números inseridos pelo usuário em preto
- Células com conflitos destacadas em vermelho
- Seleção de célula com borda amarela ao clicar
- Digitação de 1-9 nas células selecionadas (apenas editáveis)
- Delete/Backspace para apagar
- Botões: Novo Jogo, Resolver, Limpar, Verificar
- Mensagens de status em português brasileiro
- Detecção automática de conflitos ao desenhar
- Verificação de Sudoku completo e válido

Requisitos:
- Arquivo sudoku.py com as funções: gerar_jogo_inicial_aleatorio(), verificar_sudoku(grid), resolvendo_sudoku(grid)
- sudoku_legivel() importado mas não usado na interface
- grid é lista de listas Python (converte numpy se necessário)
- resolvendo_sudoku modifica grid in-place e retorna True se resolvido

Execução: python sudoku_interface_pygame.py
"""

# Inicializa o Pygame
pygame.init()

# Dimensões da janela e grid
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
CELL_SIZE = 50
GRID_SIZE = 9 * CELL_SIZE
GRID_X = 75
GRID_Y = 60
BUTTON_Y = 530
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 45

# Cores
COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'red': (255, 50, 50),
    'yellow': (255, 255, 0),
    'blue': (50, 100, 200),
    'dark_blue': (30, 60, 120),
    'hover_blue': (80, 130, 220)
}

# Fontes
font_num = pygame.font.Font(None, 48)
font_btn = pygame.font.Font(None, 32)
font_status = pygame.font.Font(None, 28)

# Botões 
buttons = [
{'text': 'Novo Jogo', 'action': 'new', 'rect': pygame.Rect(75, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)},
{'text': 'Resolver', 'action': 'solve', 'rect': pygame.Rect(205, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)},
{'text': 'Limpar', 'action': 'clear', 'rect': pygame.Rect(335, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)},
{'text': 'Verificar', 'action': 'verify', 'rect': pygame.Rect(465, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)}
]

class SudokuGame:
    """Classe principal que gerencia o estado e lógica do jogo Sudoku."""

    def __init__(self):
        """Inicializa o jogo gerando um novo puzzle."""
        self.grid = []  # Grade atual 9x9 (lista de listas)
        self.fixed = []  # Máscara de células fixas (True se fixo)
        self.selected = None  # Célula selecionada (row, col) ou None
        self.status = "Bem-vindo ao Sudoku! Clique em uma célula para começar."
        self.new_game()

    def new_game(self):
        """Gera um novo jogo inicial aleatório, convertendo numpy para lista se necessário."""
        initial = gerar_jogo_inicial_aleatorio()
        # Converte numpy array para lista Python se aplicável
        if isinstance(initial, np.ndarray):
            self.grid = initial.tolist()
        else:
            self.grid = [row[:] for row in initial]  # Cópia profunda
        # Determina células fixas (onde há número inicial)
        self.fixed = [[self.grid[r][c] != 0 for c in range(9)] for r in range(9)]
        self.selected = None
        self.status = "Novo jogo gerado! Clique em uma célula editável e digite 1-9."

    def solve(self):
        """Resolve o Sudoku chamando resolvendo_sudoku (não altera fixos, mas preenche tudo)."""
        temp_grid = [row[:] for row in self.grid]  # Cópia para segurança
        if resolvendo_sudoku(temp_grid):
            self.grid = temp_grid
            self.status = "Sudoku resolvido automaticamente!"
        else:
            self.status = "Não foi possível resolver este Sudoku."

    def clear(self):
        """Limpa apenas as células editáveis (não fixas)."""
        for r in range(9):
            for c in range(9):
                if not self.fixed[r][c]:
                    self.grid[r][c] = 0
        self.status = "Células editáveis limpas."

    def verify(self):
        """Verifica se há conflitos e se está completo."""
        is_valid = verificar_sudoku(self.grid)
        is_filled = all(self.grid[r][c] != 0 for r in range(9) for c in range(9))
        if is_valid:
            if is_filled:
                self.status = "Parabéns! Sudoku completado corretamente! 🎉"
            else:
                self.status = "Sem conflitos. Continue preenchendo! ✅"
        else:
            self.status = "Há conflitos! Verifique as células em vermelho. ❌"

    def set_cell(self, row, col, num):
        """Define um número em uma célula editável."""
        if not self.fixed[row][col] and 1 <= num <= 9:
            self.grid[row][col] = num

    def clear_cell(self, row, col):
        """Apaga uma célula editável."""
        if not self.fixed[row][col]:
            self.grid[row][col] = 0

    def has_conflict(self, row, col):
        """Verifica se a célula (row, col) tem conflito com outras no row/col/box."""
        num = self.grid[row][col]
        if num == 0:
            return False
        # Verifica linha
        for c in range(9):
            if c != col and self.grid[row][c] == num:
                return True
        # Verifica coluna
        for r in range(9):
            if r != row and self.grid[r][col] == num:
                return True
        # Verifica bloco 3x3
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for dr in range(3):
            for dc in range(3):
                r = box_row_start + dr
                c = box_col_start + dc
                if r != row and c != col and self.grid[r][c] == num:
                    return True
        return False

# Cria a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Pygame - Interface Completa")
clock = pygame.time.Clock()

# Instância do jogo
game = SudokuGame()

# Funções de desenho
def draw_grid(screen):
    """Desenha o grid 9x9 com linhas mais grossas nos blocos 3x3."""
    for i in range(10):
        thickness = 5 if i % 3 == 0 else 2
        # Linhas verticais
        pygame.draw.line(screen, COLORS['black'],
                         (GRID_X + i * CELL_SIZE, GRID_Y),
                         (GRID_X + i * CELL_SIZE, GRID_Y + GRID_SIZE), thickness)
        # Linhas horizontais
        pygame.draw.line(screen, COLORS['black'],
                         (GRID_X, GRID_Y + i * CELL_SIZE),
                         (GRID_X + GRID_SIZE, GRID_Y + i * CELL_SIZE), thickness)

def draw_numbers(screen, game):
    """Desenha os números no grid com cores apropriadas e detecção de conflito."""
    for r in range(9):
        for c in range(9):
            num = game.grid[r][c]
            if num != 0:
                # Cor base: cinza para fixos, preto para editáveis
                color = COLORS['gray'] if game.fixed[r][c] else COLORS['black']
                # Vermelho se conflito
                if game.has_conflict(r, c):
                    color = COLORS['red']
                text = font_num.render(str(num), True, color)
                # Centraliza o texto na célula
                text_rect = text.get_rect(center=(
                    GRID_X + c * CELL_SIZE + CELL_SIZE // 2,
                    GRID_Y + r * CELL_SIZE + CELL_SIZE // 2
                ))
                screen.blit(text, text_rect)

def draw_selected(screen, row, col):
    """Desenha borda amarela na célula selecionada."""
    rect = pygame.Rect(
        GRID_X + col * CELL_SIZE + 4,
        GRID_Y + row * CELL_SIZE + 4,
        CELL_SIZE - 8,
        CELL_SIZE - 8
    )
    pygame.draw.rect(screen, COLORS['yellow'], rect, 4)

def draw_buttons(screen, mouse_pos):
    """Desenha os botões com efeito hover."""
    for btn in buttons:
        # Cor com hover
        color = COLORS['hover_blue'] if btn['rect'].collidepoint(mouse_pos) else COLORS['blue']
        pygame.draw.rect(screen, color, btn['rect'])
        pygame.draw.rect(screen, COLORS['black'], btn['rect'], 3)
        # Texto centralizado
        text = font_btn.render(btn['text'], True, COLORS['white'])
        text_rect = text.get_rect(center=btn['rect'].center)
        screen.blit(text, text_rect)

def draw_status(screen, status):
    """Desenha a mensagem de status no topo."""
    # Quebra de linha se texto longo
    words = status.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font_status.size(test_line)[0] < SCREEN_WIDTH - 20:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    y = 10
    for line in lines:
        text = font_status.render(line, True, COLORS['black'])
        screen.blit(text, (10, y))
        y += 30

# Loop principal do jogo
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # Verifica clique em botão
            clicked = False
            for btn in buttons:
                if btn['rect'].collidepoint(pos):
                    if btn['action'] == 'new':
                        game.new_game()
                    elif btn['action'] == 'solve':
                        game.solve()
                    elif btn['action'] == 'clear':
                        game.clear()
                    elif btn['action'] == 'verify':
                        game.verify()
                    clicked = True
                    break
            if not clicked:
                # Clique no grid para selecionar célula
                mx, my = pos
                if (GRID_X <= mx < GRID_X + GRID_SIZE and
                    GRID_Y <= my < GRID_Y + GRID_SIZE):
                    col = (mx - GRID_X) // CELL_SIZE
                    row = (my - GRID_Y) // CELL_SIZE
                    game.selected = (row, col)
        elif event.type == pygame.KEYDOWN:
            if game.selected is not None:
                row, col = game.selected
                # Digita número 1-9
                if event.unicode.isdigit():
                    num = int(event.unicode)
                    game.set_cell(row, col, num)
                # Apaga com Backspace ou Delete
                elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    game.clear_cell(row, col)

    # Desenha tudo
    screen.fill(COLORS['white'])
    draw_status(screen, game.status)
    draw_grid(screen)
    draw_numbers(screen, game)
    if game.selected is not None:
        draw_selected(screen, *game.selected)
    draw_buttons(screen, mouse_pos)
    pygame.display.flip()
    clock.tick(60)

# Finaliza
pygame.quit()
sys.exit()
