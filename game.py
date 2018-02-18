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
	title, titleRECT = media.centeredText("ALBERT THE INTIMIDATING", 60, gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2
	ctx.blit(title,titleRECT)

	title, titleRECT = media.centeredText("click anywhere to continue", 30, gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 -200
	ctx.blit(title,titleRECT)

	fps = media.mulismall.render(str(round(clock.get_fps(),1)),True,media.black)
	fpsRECT = fps.get_rect()
	ctx.blit(fps,(5,0))

def instructions():
	ctx.fill((30,144,255))
	ctx.blit(title,titleRECT)
<<<<<<< HEAD
	title, titleRECT = media.centeredText("wasd to move", 30, gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 -100
	ctx.blit(title,titleRECT)
	title, titleRECT = media.centeredText("space to jump", 30, gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 -50
	ctx.blit(title,titleRECT)
	title, titleRECT = media.centeredText("Drag and drop objects to build your environment", 30, gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 -0
	ctx.blit(title,titleRECT)
	title, titleRECT = media.centeredText("Reach the goal zone to improve your sad life", 30, gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 +50
	ctx.blit(title,titleRECT)
	title, titleRECT = media.centeredText("click anywhere to continue on living your sad life", 30, gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 +200
	ctx.blit(title,titleRECT)
def levelselection():
    pass
def level(screenid):
	ctx.fill((236,236,236))
	anEntity = Entity(13,10,10,10,(0,0,0)) 
	anEntity.go()
=======
>>>>>>> c3b76c3ff7413e210b9f25580e994c5570e051f4

def close():
	pygame.quit()
	quit()

def main():
	screenid = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				close()
		if screenid == 0:
			titleScreen()
			if pygame.mouse.get_pressed()[0]:
				screenid = 1
		elif screenid == 1:
			instructions()
			if pygame.mouse.get_pressed()[0]:
				screenid = 3
		elif screenid == 2:
			screenid = levelselection()
		elif screenid == 3:            
			level(1)
		pygame.display.update()
		clock.tick(60)
main()