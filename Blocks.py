

class Block():
    def __init__(self):
        self.position = {
            'x':5,
            'y':2
        }
        self.bricks = []
    
    def init_position(self):
        self.position = {
            'x':5,
            'y':2
        }
    
    def move_left(self):
        self.position['x'] -= 1
    
    def move_right(self):
        self.position['x'] += 1
    
    def move_down(self):
        self.position['y'] += 1

    def change(self):
        self.bricks[0] , self.bricks[1] = self.bricks[1] , self.bricks[0]
        self.bricks[1] , self.bricks[2] = self.bricks[2] , self.bricks[1]
    
        

