import pygame

class Assets:
    def __init__(self):
        #image_assets and resizing
        start_image = pygame.image.load(r"C:\Users\limju\OneDrive\바탕 화면\codes\mygame\assets\first_asset.png")
        start_image = pygame.transform.scale(start_image,(750,450))
        space_invaders = pygame.image.load(r"C:\Users\limju\OneDrive\바탕 화면\codes\mygame\assets\space_invaders.png")
        space_invaders = pygame.transform.scale(space_invaders,(300,200))
        alien_image = pygame.image.load(r"C:\Users\limju\OneDrive\바탕 화면\codes\mygame\assets\alien.png")
        alien_image = pygame.transform.scale(alien_image,(40,40))
        boss_image = pygame.image.load(r"C:\Users\limju\OneDrive\바탕 화면\codes\mygame\assets\boss.png")
        boss_image = pygame.transform.scale(boss_image,(100,100))
        shuttle_image = pygame.image.load(r"C:\Users\limju\OneDrive\바탕 화면\codes\mygame\assets\shuttle.png")
        shuttle_image = pygame.transform.scale(shuttle_image,(40,40))
        space = pygame.image.load(r"C:\Users\limju\OneDrive\바탕 화면\codes\mygame\assets\space.png")
        space = pygame.transform.scale(space,(750,450))
        bullet_image = pygame.image.load(r"C:\Users\limju\OneDrive\바탕 화면\codes\mygame\assets\bullet.png")
        bullet_image = pygame.transform.scale(bullet_image,(10,20))
        self.images = {
            "start_image" : start_image,
            "space_invaders" : space_invaders,
            "boss_image" : boss_image,
            "shuttle_image" : shuttle_image,
            "space" : space,
            "bullet_image" : bullet_image,
            "alien_image" : alien_image
        }

    def get_image(self,assetName):
        return self.images[assetName]

class Bullet:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def move_up(self,speed):
        pass
    def move_down(self,speed):
        pass

#Objects define 
class Object:
    def __init__(self,x,y,image,width,height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image = image
        self.hp = 1
        self.bulletCount = 0
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def decrease_hp(self):
        self.hp -= 1
        if(self.hp == 0):
            del(self)
    def get_pos(self):
        return [self.x , self.y]
    def move_left(self,speed):
        if(self.x > 0):
            self.x -= speed
    def move_right(self,speed):
        if(self.x + self.width < 750):
            self.x += speed
    def get_image(self):
        return self.image
    def shooting(self,asset):
        bullet = Bullet(self.x,self.y,asset.get_image("bullet_image"),10,20,self)
        self.bulletCount += 1
        return bullet
    def get_bulletcount(self):
        return self.bulletCount
    def decrease_bulletcount(self):
        self.bulletCount -= 1
    
class Bullet(Object):
    def __init__(self,x,y,image,width,height,owner):
        super().__init__(x,y,image,width,height)
        self.owner = owner
    def move_down(self,speed):
        self.y += speed
    def move_up(self,speed):
        self.y -= speed
    def get_owner(self):
        return self.owner

class Alien(Object):
    def __init__(self,x,y,image,width,height):
        super().__init__(x,y,image,width,height)
        self.vector = True
    def get_vector(self):
        return self.vector
    def set_vector(self):
        self.vector = not self.vector
    def move_left(self,speed):
        if(self.x > 0):
            self.x -= speed
            return False
        else:
            return True
    def move_right(self,speed):
        if(self.x + self.width < 750):
            self.x += speed
            return False
        else:
            return True
    def move_down(self,speed):
        self.y += speed
