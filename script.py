import random
import pygame as pg
from pathlib import Path

pg.init()
SIZE = (460, 700)
janela = pg.display.set_mode(SIZE, (pg.SCALED | pg.RESIZABLE), 0, 0, 0)
pg.display.set_caption('FlappyBugs')
pg.display.set_icon(pg.image.load('pc.png'))
font = pg.font.SysFont('Bauhaus', 60)
font2 = pg.font.SysFont('Bauhaus', 40)

#Cor
WHITE = (255, 255, 255)
RED = (235, 64, 52)
DARKBLUE = (33, 41, 54)

#variaveis
jogando = False
fim = False
chao_vel = 0
ram_gap = 80
ram_frequencia = 1500
ultima_ram = pg.time.get_ticks()
game_speed = 5
pontos = 0
pontosDisplay = 0
passando = False
musics = ["music/Captain Scurvy.mp3", "music/Mighty Like Us.mp3", "music/The Builder.mp3"]
music = pg.mixer.music.load(musics[random.randint(0,2)])
SFX = {
    0 : pg.mixer.Sound("music/jump.wav"),
    1 : pg.mixer.Sound("music/hitHurt.wav"),
    2 : pg.mixer.Sound("music/pass.wav"),
    3 : pg.mixer.Sound("music/pickup.wav")
}
for i in SFX:
    SFX[i].set_volume(0.3)
pg.mixer.music.set_volume(0.3)

#imagens
chao = pg.image.load('chao.png')

#Mostrar pontos
def text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    janela.blit(img, (x, y))

def restart():
    ram_group.empty()
    gpu_group.empty()
    pc.rect.x = 80
    pc.rect.y = int(SIZE[1] / 2)
    pc.vel = 0
    pc.image = pg.transform.rotate(pc.imagem, 0)
    score = 0
    global music
    music = pg.mixer.music.load(musics[random.randint(0,2)])
    pg.mixer.music.play(-1)
    return score

#Definir objeto pc
class Pc(pg.sprite.Sprite):
    #func ready
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.imagem = pg.image.load('pc.png')
        self.image = self.imagem
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.jumped = False
        
    # func process
    def update(self):
        
        if fim == False:
            if jogando == True:
                #cair
                self.vel += 0.8
                if self.vel > 15:
                    self.vel = 15
                if self.rect.bottom < 720 - chao.get_rect()[3]:
                    self.rect.y += int(self.vel)
                    
            #pular    
            if pg.key.get_pressed()[pg.K_SPACE] and not self.jumped:
                self.jumped = True
                self.vel = -10
                SFX[0].play()
            if not pg.key.get_pressed()[pg.K_SPACE]:
                self.jumped = False
            
            #girar
            self.image = pg.transform.rotate(self.imagem, self.vel * -2)
        
#Definir objeto ram
class Ram(pg.sprite.Sprite):
    def __init__(self, x ,y, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('ram.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pg.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - ram_gap]
        elif position == -1:
            self.rect.topleft = [x, y + ram_gap]

    def update(self):
        if jogando == True and fim == False:
            self.rect.x -= game_speed
        if self.rect.right < 0:
            self.kill()

class Gpu(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('gpu.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        if jogando == True and fim == False:
            self.rect.x -= game_speed
        if self.rect.right < 0:
            self.kill()

pc = Pc(80, int(SIZE[1] / 2))
pc_group = pg.sprite.Group()
pc_group.add(pc)
ram_group = pg.sprite.Group()
gpu_group = pg.sprite.Group()

# /////////////////////////////////// GAME ///////////////////////////////////
def nivel():
    global jogando
    global fim
    global chao_vel
    global ram_gap
    global ram_frequencia
    global ultima_ram
    global game_speed
    global pontos
    global pontosDisplay
    global passando
    #preparar instancia do pc

    rodando = True
    while rodando:
        pg.time.Clock().tick(60)
        janela.fill(DARKBLUE)

        if pc.rect.bottom > 720 - chao.get_rect()[3]:
            if jogando:
                SFX[1].play()
            jogando = False
            fim = True

        pc_group.draw(janela)
        pc_group.update()
        ram_group.draw(janela)
        ram_group.update()
        gpu_group.draw(janela)
        gpu_group.update()

        #Definir pontos
        if len(ram_group) > 0:
            if pc_group.sprites()[0].rect.left > ram_group.sprites()[0].rect.left and pc_group.sprites()[0].rect.right < ram_group.sprites()[0].rect.right + 6 and passando == False:
                passando = True
            if passando == True:
                if pc_group.sprites()[0].rect.left > ram_group.sprites()[0].rect.right:
                    SFX[2].play()
                    pontos += 1
                    passando = False

        if pontos > pontosDisplay:
            pontosDisplay += 1

        # text(str(pontosDisplay), font, WHITE, SIZE[0] / 2, 20)
        textPoints = str(pontosDisplay)
        texto = font.render(textPoints, True, WHITE)
        text_rect = texto.get_rect(center=(SIZE[0]/2, 40))
        janela.blit(texto, text_rect)

        #Colisoes por grupos {  if pc_group collider with ram_group or pc collider with cellin :
        #                           fim de jogo  }
        if pg.sprite.groupcollide(pc_group, ram_group, False, False) or pc.rect.top < 0:
            if jogando:
                SFX[1].play()
            jogando = False
            fim = True     

        #Colisoes por grupos {  if pc_group collider with gpu_group or pc collider with cellin :
        #                           fim de jogo  }
        if pg.sprite.groupcollide(pc_group, gpu_group, False, True):
            SFX[3].play()
            pontos += 5

        for event in pg.event.get():
            if event.type == pg.QUIT:
                rodando = False
                pg.quit()
                quit()
        if pg.key.get_pressed()[pg.K_SPACE] and jogando == False and fim == False:
            jogando = True
        if pg.key.get_pressed()[pg.K_SPACE] and jogando == True and fim == True:
            jogando = True

        janela.blit(chao, (chao_vel, 720 - chao.get_rect()[3]))
        if fim == False:

            #gerador de obstaculos
            if jogando:
                time = pg.time.get_ticks()
                if time - ultima_ram > ram_frequencia:
                    ram_altura = random.randint(-100, 100)
                    btnRam = Ram(480, int(SIZE[0]/1.3 + ram_altura), 1)
                    topRam = Ram(480, int(SIZE[0]/1.3 + ram_altura), -1)
                    a = random.randint(0, 100)
                    if a > 80:
                        gpu = Gpu(490, int(SIZE[0]/1.3 + ram_altura))
                        gpu_group.add(gpu)
                    ram_group.add(btnRam) 
                    ram_group.add(topRam)
                    ultima_ram = time

            chao_vel -= game_speed
            if chao_vel < -chao.get_rect()[2] / 2:
                chao_vel = 0 

        if fim == True:
            if pg.key.get_pressed()[pg.K_r]:
                fim = False
                pontosDisplay = 0
                pontos = restart()

        pg.display.flip()

def menu():
    rodando = True
    time = 0
    global music
    music = pg.mixer.music.load(musics[random.randint(0,2)])
    pg.mixer.music.play(-1)
    while rodando:
        pg.time.Clock().tick(60)
        janela.fill(DARKBLUE)
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                rodando = False
                pg.quit()
                quit()
            if mouse[0] > 170 and mouse[0] < 310 and mouse[1] > 340 and mouse[1] < 382:
                if event.type == pg.MOUSEBUTTONUP:
                    nivel()
        button = pg.draw.rect(janela,(255, 255, 255), ((SIZE[0]/2-70, SIZE[1]/2-20), (140, 40)))
        texto = font2.render('Jogar', True, (0, 0, 0))
        text_rect = texto.get_rect(center=(SIZE[0]/2, SIZE[1]/2))
        janela.blit(texto, text_rect)

        titulo = font.render('FlappyBugs', True, WHITE)
        text_rect1 = titulo.get_rect(center=(SIZE[0]/2, 40))
        janela.blit(titulo, text_rect1)

        pg.display.flip()
menu()
pg.quit()
