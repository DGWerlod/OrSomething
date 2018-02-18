import pygame, math, random
pygame.init()

ctx = pygame.display.set_mode((900,600))
pygame.display.set_caption("Albert")
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

anEntity = Entity(13,10,10,10)

def main():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				close()
		ctx.fill((236,236,236))
		anEntity.go()
		pygame.display.update()
		clock.tick(60)
main()