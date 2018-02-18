import pygame, math, random
pygame.init()

class Block(Entity):
    
    def __init__(self, x, y, w, h):
        super().__init__(x,y,w,h) 
        self.exists = True
        self.color = (0,65,128)
    def pos(self):
        pass
    def place(x, y):
        self.x = x
        self.y = y
    def remove():
        exists = False
    def go():
        if exists:
            self.draw()
        
       
        
        