import pygame, math, random
import media, collisions
pygame.init()

global gameW, gameH, presets, controls, mouse, screenid

gameW, gameH = 900, 600
presets = {'keyW':pygame.K_w,'keyA':pygame.K_a,'keyS':pygame.K_s,'keyD':pygame.K_d,'keySpace':pygame.K_SPACE}
controls = {'keyW':False,'keyA':False,'keyS':False,'keyD':False,'keySpace':False}
mouse = {'pos':pygame.mouse.get_pos(),'click':False,'held':False}
screenid = 0

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

class Selection(Entity):
	def  __init__(self,x,y,w,h,color,levelID):
		super().__init__(x,y,w,h,color)
		self.levelID = levelID

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
		super().__init__(x,y,w,h,media.blueOG)
		self.img = img
		self.level = level
	def draw(self):
		ctx.blit(self.img[self.level],(self.x,self.y))

levelRects = [Selection(100,100,300,150,media.blueOG,3),
				Selection(100,350,300,150,media.blueOG,4),
				Selection(500,100,300,150,media.blueOG,5),
				Selection(500,350,300,150,media.blueOG,6)]
daniel= Player(10, 520, 30, 60, media.playerBody, 0)

class Level(object):
	def __init__(self,start,goal,materials):
		self.start = start
		self.goal = goal
		self.materials = materials
	def load(self):
		pass

levels = [0,0,0,"""the levels"""]

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
	title, titleRECT = media.centeredText("Instructions", 60, gameW)
	titleRECT.top = titleRECT.height/2 +10
	ctx.blit(title,titleRECT)
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
    
def levelSelect():
	ctx.fill((236, 236, 236))
	levelNum = 1
	for l in levelRects:
		l.draw()
		text, textRect = media.centeredText("Level " + str(levelNum), 50, 300)
		textRect.left += l.x
		textRect.top = l.y + l.h/2 - textRect.h/2 - 5 #-5 aesthetic
		ctx.blit(text,textRect)
		levelNum += 1
    
def level():
	ctx.fill((236,236,236))
	daniel.draw()
	pygame.draw.rect(ctx,(206,206,206),(700,0,200,600))
	pygame.draw.rect(ctx,(0,65,128),(0,580,900,20))

def close():
	pygame.quit()
	quit()

def main():
	global screenid
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				close()
		info = pygame.mouse.get_pressed()
		if info[0] == True:
			if mouse['held'] == False:
				mouse['click'] = True
				mouse['held'] = True
			else:
				mouse['click'] = False
		else:
			mouse['click'] = False
			mouse['held'] = False
		mouse['pos'] = pygame.mouse.get_pos()

		if mouse['click']:
			if screenid < 2:
				screenid += 1
			elif screenid == 2:
				for l in levelRects:
					if collisions.pointRect(mouse['pos'],l):
						#levels[l.levelID].load()
						screenid += 1


		if screenid == 0:
			titleScreen()
		elif screenid == 1:
			instructions()
		elif screenid == 2:
			levelSelect()
		else:
			level()

		pygame.display.update()
		clock.tick(10)
main()