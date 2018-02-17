import pygame, math, random
pygame.init()

ctx = pygame.display.set_mode((200,100))
pygame.display.set_caption("CircleGame")
clock = pygame.time.Clock()

class Entity(object):
	def  __init__(self,x,y,w,h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	def pos(self):
		pass
	def draw(self):
		pygame.draw.rect(ctx,(0,0,0),(self.x,self.y,self.w,self.h))
	def go(self):
		self.pos()
		self.draw()

def close():
	pygame.quit()
	quit()


def main():
	pygame.display.update()
	clock.tick(2)
main()