import pygame, math, random
import media
pygame.init()

gameW, gameH = 900, 600

ctx = pygame.display.set_mode((gameW,gameH))
pygame.display.set_caption("Albert")
clock = pygame.time.Clock()

class Entity(object):
	def  __init__(self,x,y,w,h,color):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.color = color
	def pos(self):
		pass
	def draw(self):
		pygame.draw.rect(ctx,self.color,(self.x,self.y,self.w,self.h))
	def go(self):
		self.pos()
		self.draw()

class Material(Entity):
	def __init__(self,w,h,color):
		super().__init__(0,0,w,h,color)
		self.exists = False
	def place(x, y):
		self.exists = True
		self.x = x
		self.y = y
	def remove():
		self.exists = False
	def go():
		if self.exists:
			self.draw()

class Enemy(Entity):
	def __init__(self):
		pass

class Player(Entity):
	def __init__(self,x,y,w,h,img,level):
		super().__init__(x,y,w,h,media.blue)
		self.img = img
		self.level = level
	def draw(self):
		ctx.blit(self.img[level],(self.x,self.y,self.w,self.h))


class Room(object):
	def __init__(self,start,goal,materials,enemies):
		self.start = start
		self.goal = goal
		self.materials = materials
		self.enemies = enemies
	def load(self):
		pass

def titleScreen():
	ctx.fill((30,144,255))
	title = media.muli.render("ALBERT THE INTIMIDATING",True,(31,31,31))
	titleRECT = title.get_rect()
	titleRECT.top = gameH/2 - titleRECT.height/2
	titleRECT.left = gameW/2 - titleRECT.width/2
	ctx.blit(title,titleRECT)

	subtitle = media.mulismall.render("click anywhere to continue",True,(31,31,31))
	subtitleRECT = subtitle.get_rect()
	subtitleRECT.top = gameH/2 + titleRECT.height/2
	subtitleRECT.left = gameW/2 - subtitleRECT.width/2 
	ctx.blit(subtitle,subtitleRECT)
	
	fps = media.mulismall.render(str(round(clock.get_fps(),1)),True,media.black)
	fpsRECT = fps.get_rect()
	ctx.blit(fps,(5,0))

def instructions():
	ctx.fill((30,144,255))
	ctx.blit(title,titleRECT)

def close():
	pygame.quit()
	quit()

anEntity = Entity(13,10,10,10,(0,0,0))

def main():
	screenid = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				close()
		"""ctx.fill((236,236,236))
		anEntity.go()"""
		if screenid == 0:
			titleScreen()
			if pygame.mouse.get_pressed()[0]:
				screenid = 1				
		elif screenid == 1:
			instructions()
			
		pygame.display.update()
		clock.tick(60)
main()