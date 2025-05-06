import random
import math
from pygame import Rect

# tamanho
LARGURA = 800
ALTURA = 600

# status
ESTADO_MENU = "menu"
ESTADO_JOGO = "jogo"
ESTADO_DERROTA = "derrota"
ESTADO_VITORIA = "vitoria"
estado_atual = ESTADO_MENU

# som controle
som_ativo = True
musica_tocando = False

# botões menu
botoes = {
    "iniciar": Rect(300, 200, 200, 50),
    "som": Rect(300, 280, 200, 50),
    "sair": Rect(300, 360, 200, 50)
}

# sprites do herói
heroi_parado = ["heroi_parado1", "heroi_parado2"]
heroi_andando = ["heroi_andando1", "heroi_andando2"]
indice_animacao_heroi = 0
temporizador_animacao_heroi = 0

# herói
class Heroi:
    def __init__(self):
        self.x = LARGURA // 2
        self.y = ALTURA // 2
        self.velocidade = 2
        self.lista_imagens = heroi_parado
        self.imagem = self.lista_imagens[0]
        self.retangulo = Rect(self.x, self.y, 32, 32)
        self.vida = 4 

    def mover(self):
        dx = dy = 0
        if keyboard.left:
            dx = -self.velocidade
        if keyboard.right:
            dx = self.velocidade
        if keyboard.up:
            dy = -self.velocidade
        if keyboard.down:
            dy = self.velocidade

        self.x += dx
        self.y += dy
        self.retangulo.topleft = (self.x, self.y)

        if dx != 0 or dy != 0:
            self.lista_imagens = heroi_andando
        else:
            self.lista_imagens = heroi_parado

    def animar(self):
        global temporizador_animacao_heroi, indice_animacao_heroi
        temporizador_animacao_heroi += 1
        if temporizador_animacao_heroi > 10:
            temporizador_animacao_heroi = 0
            indice_animacao_heroi = (indice_animacao_heroi + 1) % len(self.lista_imagens)
        self.imagem = self.lista_imagens[indice_animacao_heroi]

    def desenhar(self):
        screen.blit(self.imagem, (self.x, self.y))

heroi = Heroi()

# inimigo
class Inimigo:
    def __init__(self, x, y, largura_patrulha):
        self.x = x
        self.y = y
        self.velocidade = 1
        self.direcao = 1
        self.x_inicial = x
        self.largura_patrulha = largura_patrulha
        self.imagens_andando = ["inimigo_andando1", "inimigo_andando2"]
        self.imagens_parado = ["inimigo_parado1", "inimigo_parado2"]
        self.lista_imagens = self.imagens_parado
        self.imagem = self.lista_imagens[0]
        self.indice_animacao = 0
        self.temporizador_animacao = 0
        self.retangulo = Rect(self.x, self.y, 32, 32)
        self.movendo = True

    def mover(self):
        self.x += self.velocidade * self.direcao
        self.movendo = True
        if self.x > self.x_inicial + self.largura_patrulha or self.x < self.x_inicial:
            self.direcao *= -1
            self.movendo = False
        self.retangulo.topleft = (self.x, self.y)

    def animar(self):
        if self.movendo:
            self.lista_imagens = self.imagens_andando
        else:
            self.lista_imagens = self.imagens_parado

        self.temporizador_animacao += 1
        if self.temporizador_animacao > 15:
            self.temporizador_animacao = 0
            self.indice_animacao = (self.indice_animacao + 1) % len(self.lista_imagens)
        self.imagem = self.lista_imagens[self.indice_animacao]

    def desenhar(self):
        screen.blit(self.imagem, (self.x, self.y))

# lista com os inimigos
inimigos = [
    Inimigo(100, 400, 200),
    Inimigo(500, 300, 150),
    Inimigo(200, 500, 100)
]

# desenho
def draw():
    screen.clear()
    if estado_atual == ESTADO_MENU:
        desenhar_menu()
    elif estado_atual == ESTADO_JOGO:
        desenhar_jogo()
    elif estado_atual == ESTADO_DERROTA:
        screen.fill((100, 0, 0))
        screen.draw.text("Voce perdeu!", center=(LARGURA//2, ALTURA//2), fontsize=60, color="white")
    elif estado_atual == ESTADO_VITORIA:
        screen.fill((0, 100, 0))
        screen.draw.text("Voce venceu!", center=(LARGURA//2, ALTURA//2), fontsize=60, color="white")

# menu
def desenhar_menu():
    screen.fill((30, 30, 60))
    screen.draw.text("Jogo de Aventura", center=(LARGURA//2, 100), fontsize=60, color="white")
    for nome, botao in botoes.items():
        screen.draw.filled_rect(botao, (70, 70, 150))
        screen.draw.textbox(nome.capitalize(), botao, color="white")

# tela
def desenhar_jogo():
    heroi.desenhar()
    for inimigo in inimigos:
        inimigo.desenhar()
    screen.draw.text(f"Vida: {heroi.vida}", (10, 10), fontsize=30, color="white")

# atualiza
def update():
    global estado_atual
    if estado_atual == ESTADO_JOGO:
        heroi.mover()
        heroi.animar()

        for inimigo in inimigos[:]:
            inimigo.mover()
            inimigo.animar()

            if heroi.retangulo.colliderect(inimigo.retangulo):
                if som_ativo:
                    sounds.colisao.play() 
                heroi.vida -= 1
                heroi.x = LARGURA // 2
                heroi.y = ALTURA // 2
                heroi.retangulo.topleft = (heroi.x, heroi.y)
                inimigos.remove(inimigo)

        if heroi.vida <= 0:
            estado_atual = ESTADO_DERROTA
        elif not inimigos:
            estado_atual = ESTADO_VITORIA

# menu config
def on_mouse_down(pos):
    global estado_atual, som_ativo, musica_tocando, heroi, inimigos
    if estado_atual == ESTADO_MENU:
        if botoes["iniciar"].collidepoint(pos):
            estado_atual = ESTADO_JOGO
            heroi = Heroi()
            inimigos = [
                Inimigo(100, 400, 200),
                Inimigo(500, 300, 150),
                Inimigo(200, 500, 100)
            ]
            if som_ativo and not musica_tocando:
                try:
                    music.stop() 
                    music.play("musica_fundo") 
                    music.set_volume(0.5)
                    musica_tocando = True
                except Exception as e:
                    print("Erro ao tentar reproduzir a música:", e)
        elif botoes["som"].collidepoint(pos):
            som_ativo = not som_ativo
            if som_ativo:
                try:
                    music.play("musica_fundo")
                    music.set_volume(0.5)
                    musica_tocando = True
                except Exception as e:
                    print("Erro ao tentar reproduzir a música:", e)
            else:
                music.stop()
                musica_tocando = False
        elif botoes["sair"].collidepoint(pos):
            exit()
