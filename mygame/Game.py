from Objects import *
import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.
import pygame.font

class Game:
    def __init__(self):
        #screen init 
        self.screen_width = 750
        self.screen_height = 450
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        #state_of_game ( True or False )
        self.game_state = False
        #Frame per secnod
        self.clock = pygame.time.Clock()
        #level 
        self.level = 1 
        #gaps
        self.init_x = [150,250,350,450,550]
        self.init_y = [100,150,2200]
        #objects speed
        self.shuttle_speed = 10
        self.alien_speed = 1
        self.bullet_speed = 5
        #bullet list
        self.bullet_list = []
        #objects
        #object rendering 
        self.asset = Assets()
        self.boss = Object(315,10,self.asset.get_image("boss_image"),100,100)
        self.aliens = [[Alien (self.init_x[i],self.init_y[j],self.asset.get_image("alien_image"),40,40) for i in range(5)] for j in range(3)]
        self.shuttle = Object(350,385,self.asset.get_image("shuttle_image"),40,40)

        #start menu rendering
    def draw_start_menu(self):
        ##main메뉴버튼 렌더링 
        self.screen.blit(self.asset.get_image("start_image"),[0,0])
        rect = pygame.Rect(300,250,150,50) # x,y,width,height
        font = pygame.font.SysFont('Arial',18)
        pygame.draw.rect(self.screen,(220,220,220),rect) 
        #space_invaders blit
        self.screen.blit(self.asset.get_image("space_invaders"),[220,50])
        # '시작하기' 텍스트 렌더링
        text = font.render('START', True, (0, 0, 0))  # 텍스트를 렌더링하여 이미지(surface) 생성
        text_rect = text.get_rect(center=rect.center)  # 텍스트 이미지의 위치 설정
        self.screen.blit(text, text_rect)  # 텍스트 이미지를 화면에 표시
        #display update
        pygame.display.update()
    #game rendering
    def draw_game(self):
        #벽에 부딪혔는가 
        change = False
        #렌더링 및 피격검사 
        self.screen.blit(self.asset.get_image("space"),[0,0])
        self.screen.blit(self.shuttle.get_image(),self.shuttle.get_pos())
        self.screen.blit(self.boss.get_image(),self.boss.get_pos())
        for alien_row in self.aliens:
            for alien in alien_row:
                self.screen.blit(alien.get_image(),alien.get_pos())
                if alien.get_vector() == True:
                    hit = alien.move_left(1)
                    if hit: 
                        change = True
                else:
                    hit = alien.move_right(1)
                    if hit:
                        change = True
        for bullet in self.bullet_list:
            self.screen.blit(bullet.get_image(),bullet.get_pos())
            #bullet move
            if type(bullet.get_owner())==type(Alien):
                bullet.move_down(self.bullet_speed)
            else:
                bullet.move_up(self.bullet_speed)
            [bullet_x,bullet_y] = bullet.get_pos()
            #총알이 화면밖으로 사라지면 참조포인터를 지워준다 
            if bullet_y <0 or bullet_y>750:
                owner = bullet.get_owner()
                owner.decrease_bulletcount()
                self.bullet_list.remove(bullet)
            #bullet이 오브젝트에 피격되었는지 검사
            shuttle_x,shuttle_y = self.shuttle.get_pos()
            #셔틀이 외계인 총알에 피격
            if shuttle_y<bullet_y and bullet_y<shuttle_y+self.shuttle.get_height() and shuttle_x<bullet_x and bullet_x<shuttle_x+self.shuttle.get_width() and type(self.shuttle)!=type(bullet.get_owner()):
                #shuttle의 hp를 내려주고 bullet을 없애준다 
                print('d')
                self.shuttle.decrease_hp()
                self.bullet_list.remove(bullet)
            #alien을 for문을 돌면서 피격됬는지 검사 
            for row in self.aliens:
                for alien in row:
                    alien_x,alien_y = alien.get_pos()
                    if bullet_y<alien.y + alien.get_height() and alien_y<bullet_y and alien_x<bullet_x and bullet_x < alien_x + alien.get_width() and type(alien)!=type(bullet.get_owner()):
                        #alien의 hp를 낮춰주고 bullet 및 alien을 화면에서 지워줌 
                        alien.decrease_hp()
                        row.remove(alien)
                        bullet.get_owner().decrease_bulletcount() #shuttle 
                        self.bullet_list.remove(bullet)

            
      
        #벽에 부딪혔을 경우, vector를 반대로 바꿔준다 
        if change:
            for row in self.aliens:
                for alien in row:
                    alien.set_vector()
        #alien random shooting 

        #display update
        pygame.display.update()

    def run(self):
        #pygame init
        pygame.init()
        while not self.game_state:
            for event in pygame.event.get(): # 발생한 입력 event 목록의 event마다 검사
                if event.type == QUIT: # event의 type이 QUIT에 해당할 경우
                    pygame.quit() # pygame을 종료한다
                    sys.exit() # 창을 닫는다
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x,mouse_y = pygame.mouse.get_pos()
                        if (mouse_x>=300 and mouse_x<=450) and (mouse_y>=250 and mouse_y<=300):
                            self.game_state = True
                self.draw_start_menu()
        #isKeyPressed?
        moving_left = False
        moving_right = False
        #Loop of Game
        while self.game_state:
            for event in pygame.event.get():
                if event.type == QUIT: # event의 type이 QUIT에 해당할 경우
                    pygame.quit() # pygame을 종료한다
                    sys.exit() # 창을 닫는다
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        moving_left = True
                        
                    elif event.key == pygame.K_RIGHT:
                        moving_right = True
                        
                    elif event.key == pygame.K_SPACE:
                        bulletcount = self.shuttle.get_bulletcount()
                        if(bulletcount!=1):
                            bullet = self.shuttle.shooting(self.asset)
                            self.bullet_list.append(bullet)
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        moving_right = False
            if moving_left:
                self.shuttle.move_left(self.shuttle_speed)
            if moving_right:
                self.shuttle.move_right(self.shuttle_speed)
            self.draw_game()
            self.clock.tick(60) #60fps
        