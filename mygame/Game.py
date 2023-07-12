from Objects import *
import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.
import pygame.font
import random
import time

class Game:
    #Constructor
    def __init__(self,level):
        #level
        self.level = level
        #screen init 
        self.screen_width = 750
        self.screen_height = 450
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        #state_of_game ( True or False )
        self.game_state = False
        #Frame per secnod
        self.clock = pygame.time.Clock()
        #랜덤한 alien이 뽑히고, shooting을 하는 간격 ( = level)
        self.interval = 4 - self.level
        #gaps
        self.init_x = [150,250,350,450,550]
        self.init_y = [100,150,200]
        #objects stats
        self.shuttle_speed = 2
        self.alien_speed = 1 * self.level
        self.bullet_speed = 5 + self.level
        self.boss_hp = 2 + self.level
        self.boss_speed = 2 * self.level
        #bullet list
        self.bullet_list = []
        #object rendering 
        self.asset = Assets()
        self.boss = Alien(315,10,self.asset.get_image("boss_image"),100,100,self.boss_hp)
        self.aliens = [[Alien (self.init_x[i],self.init_y[j],self.asset.get_image("alien_image"),40,40,1) for i in range(5)] for j in range(3)]
        self.shuttle = Object(350,385,self.asset.get_image("shuttle_image"),40,40,3)
        #shooting time interval 변수
        self.interval = 2
        self.start_time = time.time()
        self.end_time = 0
        #alien들의 shooting 플래그
        self.shootIsReady = False
        #boss flag 
        self.boss_flag = False
        #기타 flags
        self.game_over = False
        self.nextLevel = False

    #start menu rendering
    def draw_start_menu(self):
        ##main메뉴버튼 렌더링 
        self.screen.blit(self.asset.get_image("start_image"),[0,0])
        rect = pygame.Rect(300,250,150,50) # x,y,width,height
        font = pygame.font.SysFont('Arial',18)
        pygame.draw.rect(self.screen,(220,220,220),rect) 
        levle_text = font.render(f'LEVEL {self.level}',True,(0,0,0))
        level_text_rect = levle_text.get_rect(center=(self.screen_width // 2 , self.screen_height // 2 + 200))
        self.screen.blit(levle_text,level_text_rect)
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
        #좌측화면하단에 shuttle hp 및 우측화면하단에 level렌더링 좌측상단에 boss_hp렌더링
        font = pygame.font.SysFont('Arial', 18)
        hp_text = font.render(f'HP:{self.shuttle.get_hp()}', True, (255, 255, 255))
        hp_text_rect = hp_text.get_rect(x=10,y=self.screen_height-30)
        level_text = font.render(f'LEVEL:{self.level}', True, (255, 255, 255))
        level_text_rect = level_text.get_rect(x=self.screen_width-80,y=self.screen_height-30)
        boss_hp_text = font.render(f'BOSS :{self.boss.get_hp()}', True, (255, 255, 255))
        boss_hp_text_rect = level_text.get_rect(x=10,y=10)
        #종료조건과 레벨업 flag 설정 
        if self.shuttle.get_hp()==0:
            self.game_over = True
        
        if self.boss.get_hp()==0:
            self.nextLevel = True

        #alien의 shooting 인터벌 지정 
        current_time = time.time()
        time_gap = current_time - self.start_time
        #float타입 시간간격을 int로 형변환후 interval과 일치할경우 Flag를 True로 세팅
        if int(time_gap) == self.interval:
            self.shootIsReady = True
            self.start_time = time.time()
            
        #alien이 벽에 부딪혔을경우 chang=True로 설정. 모든 Alien 인스턴스의 vector를 바꿔준다 
        change = False
        #인스턴스 렌더링 및 인스턴스 움직임 
        self.screen.blit(self.asset.get_image("space"),[0,0])
        self.screen.blit(self.shuttle.get_image(),self.shuttle.get_pos())
        self.screen.blit(self.boss.get_image(),self.boss.get_pos())
        self.screen.blit(hp_text, hp_text_rect)
        self.screen.blit(level_text, level_text_rect)
        self.screen.blit(boss_hp_text,boss_hp_text_rect)
        #외계인 움직임 및 방향전환 
        for alien_row in self.aliens:
            for alien in alien_row:
                self.screen.blit(alien.get_image(),alien.get_pos())
                if alien.get_vector() == True:
                    hit = alien.move_left(self.alien_speed)
                    if hit: 
                        change = True
                else:
                    hit = alien.move_right(self.alien_speed)
                    if hit:
                        change = True
        #Boss 움직임 제어 및 방향전환
        if self.boss.get_vector()==True:
            hit = self.boss.move_left(self.boss_speed)
            if hit:
                change = True
        else:
            hit = self.boss.move_right(self.boss_speed)
            if hit:
                change = True
        #총알 렌더링과 인스턴스 피격 검사 
        for bullet in self.bullet_list:
            self.screen.blit(bullet.get_image(),bullet.get_pos())
            #bullet move
            if isinstance(bullet.get_owner(),Alien):
                bullet.move_down(self.bullet_speed)
            else:
                bullet.move_up(self.bullet_speed)
            [bullet_x,bullet_y] = bullet.get_pos()
            #총알이 화면밖으로 사라지면 레퍼런스 지워주기
            if bullet_y <0 or bullet_y>750:
                owner = bullet.get_owner()
                owner.decrease_bulletcount()
                self.bullet_list.remove(bullet)
            #bullet이 오브젝트에 피격되었는지 검사
            shuttle_x,shuttle_y = self.shuttle.get_pos()
            shuttle_width = self.shuttle.get_width()
            shuttle_height = self.shuttle.get_height()
            #셔틀에 대한 총알 피격검사
            if shuttle_y<bullet_y and bullet_y<shuttle_y+shuttle_height and shuttle_x<bullet_x and bullet_x<shuttle_x+shuttle_width and type(self.shuttle)!=type(bullet.get_owner()):
                #shuttle의 hp를 내려주고 bullet을 없애준다 
                self.shuttle.decrease_hp()
                bullet.get_owner().decrease_bulletcount() #shuttle 
                self.bullet_list.remove(bullet)
            #모든 alien에 대한 총알 피격검사
            for row in self.aliens:
                for alien in row:
                    alien_x,alien_y = alien.get_pos()
                    if bullet_y<alien.y + alien.get_height() and alien_y<bullet_y and alien_x<bullet_x and bullet_x < alien_x + alien.get_width() and type(alien)!=type(bullet.get_owner()):
                        #alien의 hp를 낮춰주고 bullet 및 alien을 화면에서 지워줌 
                        alien.decrease_hp()
                        row.remove(alien)
                        bullet.get_owner().decrease_bulletcount() #shuttle 
                        self.bullet_list.remove(bullet)
            #boss에 대한 총알 피격검사
            boss_x,boss_y = self.boss.get_pos()
            boss_width = self.boss.get_width()
            boss_height = self.boss.get_height()
            if boss_y<bullet_y and bullet_y<boss_y+boss_height and boss_x<bullet_x and bullet_x<boss_x+boss_width and type(self.boss)!=type(bullet.get_owner()):
                self.boss.decrease_hp()
                bullet.get_owner().decrease_bulletcount() #shuttle 
                self.bullet_list.remove(bullet)
        #alien 하나가 벽에 부딪혔을 경우, vector를 반대로 바꿔준다 
        if change:
            for row in self.aliens:
                for alien in row:
                    alien.set_vector()
            self.boss.set_vector()
        #alien random shooting 로직 
        if self.shootIsReady:
            try:
                for row in self.aliens:
                    shoot_alien = random.choice(row)
                    bullet=shoot_alien.shooting(self.asset)
                    self.bullet_list.append(bullet)
                self.shootIsReady = False
            except:
                self.shootIsReady = False
            bullet = self.boss.shooting(self.asset)
            self.bullet_list.append(bullet)
        #display update
        pygame.display.update()
    #start pygame
    def menuLoop(self):
        #메인 화면 루프
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

    def gameLoop(self):
        #key가 계속 눌리는지 확인하는 변수
        moving_left = False
        moving_right = False
        #게임 화면 루프 
        while self.game_state:
            #Game over
            if self.game_over:
                break
            if self.nextLevel:
                break
            #Events
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
    
    def run(self):
        pygame.init()
        self.menuLoop()
        self.gameLoop()
        #게임오버시
        if self.game_over:
            # 다시 시작할지 여부를 묻는 메시지 출력
            font = pygame.font.SysFont('Arial', 18)
            text = font.render('Restart? (Y/N)', True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
            self.screen.blit(text, text_rect)
            pygame.display.update()

            choice = True
            # 키 입력 대기
            while choice:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:  # 'Y' 키를 누르면 게임 재시작
                            self.__init__(1)
                            choice = False
                        elif event.key == pygame.K_n:  # 'N' 키를 누르면 게임 종료
                            pygame.quit()
                            sys.exit()
        #level 클리어시
        if self.nextLevel:
            self.__init__(self.level+1)
            



                


