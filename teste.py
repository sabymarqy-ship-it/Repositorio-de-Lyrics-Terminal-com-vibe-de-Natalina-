import time      # Para controlar o tempo e pausas
import sys       # Para comandos de sistema e escrita direta no terminal (stdout)
import os        # Para detectar o tamanho da janela do terminal
import random    # Para gerar a posição aleatória da neve

# --- CONSTANTES ANSI (Códigos que controlam cores e estilo no terminal) ---
RESET = "\033[0m"      # Reseta todas as cores para o padrão
BOLD = "\033[1m"       # Deixa o texto em negrito

# --- CORES NATALINAS PADRONIZADAS (Usando códigos de cores 256-bit) ---
TITLE_COLOR = "\033[38;5;157m"      # Verde Pastel
HIGHLIGHT_COLOR = "\033[38;5;217m"  # Vermelho Bem Clarinho (letra atual)
MAIN_COLOR = "\033[37m"             # Branco (artista)
SNOW_COLOR = "\033[97m"             # Branco Brilhante (neve)
INACTIVE_LYRIC_COLOR = "\033[38;5;244m" # Cinza (letras que já passaram ou virão)

# --- COMANDOS DE CONTROLE DO TERMINAL ---
# Lambda que retorna a sequência para mover o cursor para uma linha e coluna específica
CURSOR_POS = lambda row, col: f"\033[{row};{col}H"
CLEAR_SCREEN = "\033[H\033[J"       # Limpa a tela inteira
HIDE_CURSOR = "\033[?25l"           # Esconde o cursor piscante
SHOW_CURSOR = "\033[?25h"           # Mostra o cursor novamente

# --- CONFIGURAÇÃO DA NEVE ---
snowflakes = [] # Lista que guardará a posição [linha, coluna, caractere] de cada floco

def create_snow(width, height):
    """Cria novos flocos de neve no topo da tela"""
    max_snow_width = min(width, 70) # Limita a neve à esquerda (até a coluna 70)
    if random.random() < 0.25:      # 25% de chance de criar um floco por frame
        # Adiciona [linha inicial 1, coluna aleatória, caractere asterisco]
        snowflakes.append([1, random.randint(1, max_snow_width), "*"])

def update_snow(height):
    """Faz a neve cair e remove flocos que saíram da tela"""
    global snowflakes
    for flake in snowflakes:
        flake[0] += 1 # Aumenta a linha (faz o floco descer)
    # Mantém na lista apenas flocos que ainda não ultrapassaram a altura do terminal
    snowflakes = [f for f in snowflakes if f[0] <= height]

def draw_snow():
    """Desenha cada floco de neve na sua posição atual"""
    for row, col, char in snowflakes:
        sys.stdout.write(CURSOR_POS(row, col))         # Move o cursor
        sys.stdout.write(f"{SNOW_COLOR}{char}{RESET}") # Desenha o floco colorido

# --- DADOS DA MÚSICA ---
CONTENT_INFO = {"title": "Nome da Musica/Poema", "artist": "Nome do Artista"}

# Lista de dicionários com o tempo de início e a letra
LYRICS_DATA = [
    {"time": 0.0, "original": "Exemplo de como a letra da música ou poema\npode ser exibida aqui."},
    {"time": 1.0, "original": "..."}, # o \n é um quebra texto.
    {"time": 2.0, "original": "..."},
    # ... (outras linhas)
    {"time": 61.0, "original": "..."}
]

def display_frame(current_line_index, term_w, term_h):
    """Renderiza um 'quadro' completo: neve + título + letras"""
    sys.stdout.write(CLEAR_SCREEN) # Limpa o frame anterior
    draw_snow()                    # Desenha a neve primeiro (fica ao fundo)
    
    start_col = 6 # Margem esquerda
    curr_row = 3  # Linha inicial

    # Desenha Título
    sys.stdout.write(CURSOR_POS(curr_row, start_col))
    sys.stdout.write(f"{BOLD}{TITLE_COLOR}{CONTENT_INFO['title']}{RESET}")
    curr_row += 1
    # Desenha Artista
    sys.stdout.write(CURSOR_POS(curr_row, start_col))
    sys.stdout.write(f"{MAIN_COLOR}{CONTENT_INFO['artist']}{RESET}")
    
    curr_row += 2 # Espaço antes das letras

    # Lógica de Janela: Mostra a linha atual e algumas vizinhas (estilo Spotify)
    start_view = max(0, current_line_index - 3) # Começa 3 linhas antes da atual
    end_view = start_view + 10                  # Mostra até 10 linhas no total

    for i in range(start_view, end_view):
        if i < len(LYRICS_DATA):
            line_content = LYRICS_DATA[i]["original"]
            # Se for a linha que deve tocar agora, usa a cor de destaque, senão cinza
            color = BOLD + HIGHLIGHT_COLOR if i == current_line_index else INACTIVE_LYRIC_COLOR
            
            # Divide a frase caso ela tenha "\n" (quebras de linha manuais)
            sub_lines = line_content.split('\n')
            for sub in sub_lines:
                if curr_row < term_h - 1: # Evita escrever fora da altura do terminal
                    sys.stdout.write(CURSOR_POS(curr_row, start_col))
                    sys.stdout.write(f"{color}{sub}{RESET}")
                    curr_row += 1
        
    sys.stdout.flush() # Força a exibição imediata de tudo que foi escrito no buffer

def main():
    """Função principal que gerencia o loop de animação"""
    try:
        sys.stdout.write(HIDE_CURSOR) # Esconde o cursor para não atrapalhar o visual
        start_time = time.monotonic()  # Marca o tempo real de início
        while True:
            w, h = os.get_terminal_size()     # Pega o tamanho atual da janela
            elapsed = time.monotonic() - start_time # Calcula quantos segundos passaram
            
            # Encontra qual linha da música corresponde ao tempo atual
            idx = 0
            while idx < len(LYRICS_DATA) and elapsed >= LYRICS_DATA[idx]["time"]:
                idx += 1
            idx -= 1 # Ajusta o índice para a linha correta
            
            # Se a música acabou (passou 3 segundos da última linha), encerra
            if idx >= len(LYRICS_DATA) - 1 and elapsed > LYRICS_DATA[-1]["time"] + 3:
                break

            create_snow(w, h)             # Lógica de neve
            update_snow(h)                # Move a neve
            display_frame(max(0, idx), w, h) # Desenha tudo
            
            time.sleep(0.08) # Controla a taxa de atualização (FPS)
    except KeyboardInterrupt:
        pass # Permite sair do programa com Ctrl+C
    finally:
        # Garante que o cursor volte e a tela limpe ao fechar
        sys.stdout.write(SHOW_CURSOR + CLEAR_SCREEN)
        print("MERRY CHRISTMAS! ⛄❄️")

if __name__ == "__main__":
    main()