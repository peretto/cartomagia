import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GRAY = (200, 200, 200)
SHADOW = (180, 180, 180)

# Tela
WIDTH, HEIGHT = 1024, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adivinhação das 21 Cartas")

# Fontes
font = pygame.font.SysFont(None, 32)
font_btn = pygame.font.SysFont(None, 28)

# Gerar baralho
suits = ['♥', '♦', '♣', '♠']
values = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
baralho = [v + s for s in suits for v in values]

# Funções auxiliares
def cor_carta(carta):
    return RED if '♥' in carta or '♦' in carta else BLACK

def embaralhar_cartas():
    return random.sample(baralho, 21)

def distribuir_em_montes(cartas):
    montes = [[], [], []]
    for i, carta in enumerate(cartas):
        montes[i % 3].append(carta)
    return montes

def recompor_cartas(montes, escolha):
    if escolha == 0:
        nova_ordem = montes[1] + montes[0] + montes[2]
    elif escolha == 1:
        nova_ordem = montes[0] + montes[1] + montes[2]
    else:
        nova_ordem = montes[0] + montes[2] + montes[1]
    return nova_ordem

def desenhar_carta(carta, x, y):
    largura, altura = 80, 120
    sombra_offset = 5
    pygame.draw.rect(screen, SHADOW, (x + sombra_offset, y + sombra_offset, largura, altura))
    pygame.draw.rect(screen, WHITE, (x, y, largura, altura))
    pygame.draw.rect(screen, BLACK, (x, y, largura, altura), 2)
    texto = font.render(carta, True, cor_carta(carta))
    text_rect = texto.get_rect(center=(x + largura // 2, y + altura // 2))
    screen.blit(texto, text_rect)

def desenhar_montes(montes):
    screen.fill(WHITE)
    for i, monte in enumerate(montes):
        y_base = 50 + i * 180
        for j, carta in enumerate(monte):
            desenhar_carta(carta, 70 + j * 105, y_base)
        pygame.draw.rect(screen, GRAY, botoes[i])
        txt_btn = font_btn.render("Está aqui", True, BLACK)
        text_rect = txt_btn.get_rect(center=botoes[i].center)
        screen.blit(txt_btn, text_rect)
    pygame.display.flip()

def mostrar_carta_escolhida(carta):
    screen.fill(WHITE)
    mensagem = font.render("A carta escolhida foi:", True, BLACK)
    screen.blit(mensagem, (WIDTH // 2 - mensagem.get_width() // 2, HEIGHT // 2 - 100))
    largura, altura = 80, 120
    x = WIDTH // 2 - largura // 2
    y = HEIGHT // 2 - altura // 2
    sombra_offset = 5
    pygame.draw.rect(screen, SHADOW, (x + sombra_offset, y + sombra_offset, largura, altura))
    pygame.draw.rect(screen, WHITE, (x, y, largura, altura))
    pygame.draw.rect(screen, BLACK, (x, y, largura, altura), 2)
    texto = font.render(carta, True, cor_carta(carta))
    text_rect = texto.get_rect(center=(x + largura // 2, y + altura // 2))
    screen.blit(texto, text_rect)
    pygame.display.flip()
    pygame.time.wait(5000)

# Inicializa o jogo
cartas = embaralhar_cartas()
rodada = 0
botoes = [pygame.Rect(810, 50 + i * 180 + 40, 130, 50) for i in range(3)]

running = True
mostrar_revelacao = False

while running:
    montes = distribuir_em_montes(cartas)
    desenhar_montes(montes)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not mostrar_revelacao:
            for i, botao in enumerate(botoes):
                if botao.collidepoint(event.pos):
                    cartas = recompor_cartas(montes, i)
                    rodada += 1
                    if rodada == 3:
                        mostrar_revelacao = True
                        carta_escolhida = cartas[10]  # 11ª carta
                        mostrar_carta_escolhida(carta_escolhida)
                        cartas = embaralhar_cartas()
                        rodada = 0
                        mostrar_revelacao = False

pygame.quit()
sys.exit()
