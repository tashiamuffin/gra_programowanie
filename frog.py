import pygame
import random as Random
from pygame.locals import *
from sys import exit
import random

#### TRZEBA TERAZ DODAĆ WPADANIE DO WODY + LICZNIK CZASU + LICZNIK ŻYĆ  
SCREEN_WIDTH = 1102
SCREEN_HEIGHT = 804
WHITE = (255,255,255)
pygame.init()

screen = pygame.display.set_mode((1102,804), 0, 0) ###background ma 1102x804, width, depth 
pygame.display.set_caption('Frogger')
##ładowanie obrazków

background = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\bg.jpg').convert()
frog_up = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
frog_done = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
frog_left = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_left.png').convert_alpha()
frog_right = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_right.png').convert_alpha()
frpg_down = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()
car1 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\auto1.png').convert_alpha()
car2 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\auto2.png').convert_alpha()
car3 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\auto3.png').convert_alpha()
car4 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\auto4.png').convert_alpha()
car5 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\police.png').convert_alpha()
log = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\lg.png').convert_alpha()
logl = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\logl.png').convert_alpha()


class Frog(pygame.sprite.Sprite):
    def __init__(self):
        # Inicjalizuj klasę bazową Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
        self.rect = self.image.get_rect() #rozmiar rysunku
        self.position = [SCREEN_WIDTH/2, SCREEN_HEIGHT - 25]
        self.rect.center = (self.position[0], self.position[1]) #pozycja początkowa
        self.ability = 1 ###umiejętność poruszania się, gdy jest -1 to nie może się ruszać ( jest już na górze szczęsliwa i czeka na inne żabki)

    def update(self):
        if self.ability == 1: ##jeśli może się poruszać to
            self.rect.center = (self.position[0],self.position[1])#move in-place

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

        elif self.ability == 0: ## jej ostatni skok na bezpieczne miejsce
            self.rect.center = (self.position[0],self.position[1])#move in-place

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

            self.ability -=1

### ----------------auta---------------
class cars(pygame.sprite.Sprite):
  
    def __init__(self):
        #730, 660, 600, 540, 470
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice([car1, car2, car3, car4, car5])
        self.rect = self.image.get_rect()
        self.position = random.choice([[0,730], [0,660], [0,600], [0,540],[0,470]])
        self.rect.center = (self.position[0],self.position[1])
        self.x_velocity = 0.5

    def update(self):
        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0],self.position[1])
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH: ##gdy wyjdzie poza ekran to znika
            self.kill()

### ------------- kłody -----------

class logsl(pygame.sprite.Sprite): ###kłody płynące w lewo
  
    def __init__(self):
        #360, 300, 240, 180, - pasy
        pygame.sprite.Sprite.__init__(self)
        self.image = log
        self.rect = self.image.get_rect()
        self.position = [SCREEN_WIDTH,random.choice([300,180])]
        self.rect.center = (self.position[0],self.position[1])
        self.x_velocity = -0.4

    def update(self):
        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0],self.position[1])#move in-place
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class logsr(pygame.sprite.Sprite): ###kłody płynące w prawo
  
    def __init__(self):
        #360, 300, 240, 180 - pasy
        pygame.sprite.Sprite.__init__(self)
        self.image = logl
        self.rect = self.image.get_rect()
        self.position = [0,random.choice([360,240,120])]
        self.rect.center = (self.position[0],self.position[1])
        self.x_velocity = 0.4

    def update(self):
        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0],self.position[1])#move in-place
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


class LiveBoard(pygame.sprite.Sprite):
    def __init__(self):
        #inicjalizuj klasę bazową
        pygame.sprite.Sprite.__init__(self)
        self.lives = 3
        self.text = "lives: %4d" % self.lives
        self.font = pygame.font.SysFont(None,50)
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = (50,5)

    def update(self):
        self.lives -= 1
        self.text = "Lives: %4d" % self.lives
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = (50,5)


class WinBoard(pygame.sprite.Sprite):
    def __init__(self,time, text):
        #inicjalizuj klasę bazową
        pygame.sprite.Sprite.__init__(self)
        self.time = time
        self.text = ("YOU {} with time: %4d s" % int(self.time)).format(text)
        self.font = pygame.font.SysFont(None,50)
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = (300,410)

class LossBoard(pygame.sprite.Sprite):
    def __init__(self):
        #inicjalizuj klasę bazową
        pygame.sprite.Sprite.__init__(self)
        self.text = "YOU LOST :c TRY AGAIN"
        self.font = pygame.font.SysFont(None, 50)
        self.image = self.font.render(self.text,1,WHITE)
        self.rect = (300,410)

## ----------------main -------------
def main():
    frog_sprite = pygame.sprite.RenderClear() #kontener na żabe
    frog = Frog()                       #stwórz żabe
    frog_sprite.add(frog) 

    # Inicjalizuj statki wroga
    cars_sprites = pygame.sprite.RenderClear() #kontener dla aut
    cars_sprites.add(cars())
    logs_sprites = pygame.sprite.RenderClear() # kontener dla logs

    scoreboardSprite = pygame.sprite.RenderClear()
    scoreboardSprite.add(LiveBoard())
    scoreboardSprite.draw(screen)
    pygame.display.flip()

    clock = pygame.time.Clock()
    ##generowanie tła 
    sit = True
    addenemyfighterCounter = 0
    addlogsl = 0
    addlogsr = 0
    lives = 3
    frogs_arrived = -1
    time = 0
    #start_time = pygame.time.get_ticks()
    end_time = 0
    win_am = 1
    
    while sit:

        if frogs_arrived == -1:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sit = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sit = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position
                    if button.collidepoint(mouse_pos):
                        frogs_arrived += 1

            screen.blit(background, (0, 0))
            button = pygame.Rect(300, 480, 450, 50) ##left top wifth height
            pygame.draw.rect(screen, [0, 0, 0], button)  # draw button
            font = pygame.font.SysFont(None, 24)
            img = font.render('PRESS ENTER OR THIS BUTTON TO START THE GAME', True, (255,244,244))
            screen.blit(img, (310, 500))
            
            font2 = pygame.font.SysFont("comicsansms", 50)
            title = font2.render('WELCOME TO THE GAME FROGGER', True, (255,244,244))
            screen.blit(title, (100, 300))
            pygame.display.flip()

        elif 0 <= frogs_arrived <= 5:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sit = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sit = False
                    elif event.key == K_LEFT:
                        frog.position[0] = frog.position[0] - 60
                        frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_left.png').convert_alpha()
                    elif event.key == K_RIGHT:
                        frog.position[0] = frog.position[0] + 60
                        frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_right.png').convert_alpha()
                    elif event.key == K_UP:
                        ####gdy żaba jest u samej góry i chce wejść na bezpieczną lilię
                        if frog.position[1] < 130 and 520<frog.position[0]<570:
                            frog.position[1] = 60
                            frog.position[0] = 545
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()
                            frog = Frog()
                            frog_sprite.add(frog) 
                        elif frog.position[1] < 130 and 150<frog.position[0]<220:
                            frog.position[1] = 60
                            frog.position[0] = 185
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()
                            frog = Frog()
                            frog_sprite.add(frog) 
                        elif frog.position[1] < 130 and 335<frog.position[0]<400:
                            frog.position[1] = 60
                            frog.position[0] = 365
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()
                            frog = Frog()
                            frog_sprite.add(frog) 
                        elif frog.position[1] < 130 and 690<frog.position[0]<760:
                            frog.position[1] = 60
                            frog.position[0] = 725
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()
                            frog = Frog()
                            frog_sprite.add(frog) 
                        elif frog.position[1] < 130 and 880<frog.position[0]<930:
                            frog.position[1] = 60
                            frog.position[0] = 905
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()
                            frog = Frog()
                            frog_sprite.add(frog) 
                        ### zwyczajny ruch w górę
                        elif frog.position[1] > 130:
                            frog.position[1] = frog.position[1] - 60
                            frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
                    elif event.key == K_DOWN:
                        frog.position[1] = frog.position[1] + 60
                        frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_LEFT:
                        frog.position[0] = frog.position[0] - 60
                        frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_left.png').convert_alpha()
                    elif event.key == K_RIGHT:
                        frog.position[0] = frog.position[0] + 60
                        frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_right.png').convert_alpha()
                    elif event.key == K_UP:
                        frog.position[1] = frog.position[1] - 60
                        frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
                    elif event.key == K_DOWN:
                        frog.position[1] = frog.position[1] + 60
                        frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()

                screen.blit(background, (0, 0))
                scoreboardSprite.draw(screen)
                frog_sprite.draw(screen)
                pygame.display.update()
            
            addenemyfighterCounter += 1
            addlogsl += 1
            addlogsr += 1
            time +=1
            ###render aut i logów

            if addenemyfighterCounter >= 200:
                cars_sprites.add(cars())
                cars_sprites.add(cars())
                addenemyfighterCounter = 0
            if addlogsl >= 350:
                logs_sprites.add(logsl())
                addlogsl = 0
            if addlogsr >= 260:
                logs_sprites.add(logsr())
                addlogsr = 0

            
            #Aktualizuj wszystkie sprite'y
            
            cars_sprites.update()
            logs_sprites.update()
            frog_sprite.update()
            
            ###uderzenie autem
            if frog.position[1] < 400 and len(pygame.sprite.groupcollide(logs_sprites, frog_sprite, 0, 0)) == 0:
                frog.kill()
                frog = Frog()
                lives -= 1
                frog_sprite.add(frog)
                scoreboardSprite.update()
                scoreboardSprite.clear(screen, background)
                scoreboardSprite.draw(screen)
            

            for hit in pygame.sprite.groupcollide(cars_sprites,frog_sprite,False, True):
                frog = Frog()
                lives -= 1
                frog_sprite.add(frog)
                scoreboardSprite.update()
                scoreboardSprite.clear(screen, background)
                scoreboardSprite.draw(screen)

            ###wejście na kłodę
            for log_travel in pygame.sprite.groupcollide(logs_sprites, frog_sprite, 0, 0):
                frog.position[0] += log_travel.x_velocity
                frog_sprite.update()
                frog_sprite.draw(screen)

            ####wygrana
            if frogs_arrived == 5:
                frogs_arrived +=1
                end_time = pygame.time.get_ticks()


            #Wyczyść ekran
            
            cars_sprites.clear(screen, background)
            logs_sprites.clear(screen, background)
            frog_sprite.clear(screen, background)

            #Rysuj sprite'y na ekranie
            cars_sprites.draw(screen)
            logs_sprites.draw(screen)
            frog_sprite.draw(screen)
            
            if lives <= 0:
                    print("Koniec gry")
                    frogs_arrived = 6
                    end_time = pygame.time.get_ticks()
                    win_am = 0

            pygame.display.flip()

        # ------------- poza główną akcją-------------
        else:
            cars_sprites.clear(screen, background)
            logs_sprites.clear(screen, background)
            frog_sprite.clear(screen, background)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sit = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sit = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    if button.collidepoint(mouse_pos):
                        main()
                
                if win_am:
                    win_table = WinBoard(end_time/1000,"WON")
                else:  
                    win_table = LossBoard()

                button = pygame.Rect(300, 480, 420, 50) ##left top wifth height
                pygame.draw.rect(screen, [0, 0, 0], button)  # draw button

                scoreboardSprite.add(win_table)
                scoreboardSprite.draw(screen)
                font = pygame.font.SysFont(None, 24)
                img = font.render('PRESS ENTER OR THIS BUTTON TO START AGAIN', True, (255,244,244))
                screen.blit(img, (310, 500))
                                    
                pygame.display.flip()
    

    pygame.quit()

main()

