import pygame 
import sys
from pygame.locals import QUIT,KEYDOWN
import random
import Blocks

pygame.init()

def get_initialized_board():
    board = []
    for i in range(0,20):
        board.append([0 for _ in range(10)])
    return board

def canmove_left(now_block):
    x = now_block.position['x']
    y = now_block.position['y']
    if x<= 0 :
        return False
    elif board[y][x-1]!=0:
         return False
    return True

def canmove_right(now_block):
    x = now_block.position['x']
    y = now_block.position['y']
    if x>=9:
        return False
    elif board[y][x+1] != 0:
        return False
    return True

def canmove_down(now_block):
     x = now_block.position['x']
     y = now_block.position['y']
     if y>=19:
          return False
     elif board[y+1][x] != 0:
          return False
     return True
     
def save_value_board(x,y,value):
     global board
     board[y][x] = value
     
def update_game():
    blockSize = {
            'width' : screen.get_width() / 13 -2,
            'height' : screen.get_height() / 20 -2
    }
    margin = {
            'x' : 10 , 'y' : 10
    }

    for y in range(0,len(board)):
            line = board[y]
            for x in range(0,len(line)):
                brick = line[x]
                pygame.draw.rect(screen, block_colors[brick], 
                                [
                                    x*(blockSize['width']+1) + margin['x'],
                                    y*(blockSize['height']+1) + margin['y'],
                                    blockSize['width'] , blockSize['height']
                                ] )
    position = now_block.position
    x = now_block.position['x']
    for i in range(0,len(now_block.bricks)):
            brick = now_block.bricks[i]
            y = now_block.position['y'] - i
            pygame.draw.rect(screen,block_colors[brick],
                            [
                                x*(blockSize['width']+1) + margin['x'],
                                    y*(blockSize['height']+1) + margin['y'],
                                    blockSize['width'] , blockSize['height']
                            ])
    
    for i in range(0,len(next_block.bricks)):
            brick = next_block.bricks[i]
            y = next_block.position['y'] - i
            pygame.draw.rect(screen, block_colors[brick],
                            [
                                11*(blockSize['width']+1) + margin['x'],
                                y*(blockSize['height']+1) + margin['y'],
                                blockSize['width'] , blockSize['height']
                            ]
                            )
             
    pygame.display.update()    
    
block_colors = [
    (64,64,64),
    (255,255,255),
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (128,0,0),
    (0,128,0),
    (0,0,128),
    (255,0,255),
    (0,255,255)
]

screen_size = {
    'width' : 240 , 
    'height' : 480
}

def check_horizontal(x,y,color,candidates):
     if x>=10:
          return candidates
     if color == 0:
          return candidates
     if board[y][x] != color:
          return candidates
     if board[y][x] == color:
          candidates.append({'x':x, 'y':y})
          check_horizontal(x+1,y,color,candidates)

def check_vertical(x,y,color,candidates):
     if y>=20:
          return candidates
     if color ==0:
          return candidates
     if board[y][x] != color:
          return candidates
     if board[y][x] == color:
          candidates.append({'x':x,'y':y})
          check_vertical(x,y+1,color,candidates)

def insert_bricks(candidates,queue):
     for candidate in candidates:
          if(queue.count(candidate)<=0):
               queue.append(candidate)
     return queue

def check_board():
     queue = [
     ]
     score = []
     for y in range(0,len(board)):
            line = board[y]
            for x in range(0,len(line)):
                color = line[x]

                candidates = check_horizontal(x,y,color,[])
                if len(candidates) >= 3:
                    queue = insert_bricks(candidates,queue)
                    candidates = check_vertical(x,y,color,[])
            if len(candidates) >= 3:
                queue = insert_bricks(candidates,queue)


screen = pygame.display.set_mode((screen_size['width'],screen_size['height']))

pygame.display.set_caption('HEXA')

now_block = Blocks.Block()
next_block = Blocks.Block()
board = get_initialized_board()

now_block.bricks = [
    random.randint(1,len(block_colors)-1),
    random.randint(1,len(block_colors)-1),
    random.randint(1,len(block_colors)-1),
]

next_block.init_position()

next_block.bricks = [
    random.randint(1,len(block_colors)-1),
    random.randint(1,len(block_colors)-1),
    random.randint(1,len(block_colors)-1),
]

delay = 1000
level = 0
score = 0
while True:
    update_game()
    
    for event in pygame.event.get(): 
          if event.type == KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_UP:
                    now_block.change()
                    break
                elif event.key == pygame.K_LEFT:
                    if canmove_left(now_block):
                        now_block.move_left()
                    break
                elif event.key == pygame.K_RIGHT:
                    if canmove_right(now_block):
                          now_block.move_right()
                    break
                elif event.key == pygame.K_DOWN:
                    if canmove_down(now_block):
                        now_block.move_down()
                    break
    if canmove_down(now_block):
         level += 1
         if level > delay : 
              level = 0
              now_block.move_down()
         continue
    else:
        for i in range(0,len(0,len(now_block.bricks))):
             x= now_block.position['x']
             y = now_block.position['y']
             save_value_board(x,y,now_block.bricks[i])
    
        while(True):
             point = check_board()
             if point <= 0: break
             score += point
        
        now_block.init_position()
        now_block.bricks = next_block.bricks

        next_block.bricks = [
             random.randint(1,len(block_colors)-1),
             random.randint(1,len(block_colors)-1),
             random.randint(1,len(block_colors)-1)
        ]

        delay -= 1
              
