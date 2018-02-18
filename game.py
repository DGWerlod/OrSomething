import pygame, math, random
import media, collisions
pygame.init()

global gameW, gameH, presets, controls, mouse, screenid
gameW, gameH = 900, 600
presets = {'keyW':pygame.K_w,'keyA':pygame.K_a,'keyS':pygame.K_s,'keyD':pygame.K_d,'keySpace':pygame.K_SPACE}
controls = {'keyW':False,'keyA':False,'keyS':False,'keyD':False,'keySpace':False}
mouse = {'pos':pygame.mouse.get_pos(),'click':False,'held':False}
screenid = 0
gravity = 0.75

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
        self.moving = False
	def place(x, y):
		self.exists = True
		self.x = x
		self.y = y
	def remove():
		self.exists = False
	def go():
		if self.exists:
			if self.moving:
				self.place(mouse['pos'][0],mouse['pos'][1])
			self.draw()

class Actor(Entity):
	def __init__(self,x,y,w,h,color,spd):
		super().__init__(x,y,w,h,color)
		self.spd = spd
	def lockToGround(self,verticalSpeed):
		for i in range(abs(int(verticalSpeed)), -1, -1):
			self.y += i
			check = self.canMove()
			self.y -= i
			if check:
				return i
		return 0
	def isOnGround(self):
		self.y += 1
		check = self.canMove()
		self.y -= 1
		if check:
			return False
		else:
			return True

class Enemy(Actor):
	def __init__(self):
		pass

class Player(Actor):
	def __init__(self,x,y,w,h,spdX,img,level):
		super().__init__(x,y,w,h,media.blueOG,[spdX,0])
		self.img = img
		self.level = level
	def canMove(self):
		"""for o in obstructions:
			if collisions.rectangles(self,o,ballR):
				return False
		for e in enemies:
			if collisions.rectangles(self,e,ballR):
				return False
		if self.y - ballR < 0 or self.x < 0 or self.y + self.h > gameH - gameIH or self.x + self.w > gameW:
			return False"""
		return True
	def pos(self):
		if controls['keyA'] == True:
			self.x -= self.spd[0]
			if not self.canMove():
				self.x += self.spd[0]
		if controls['keyD'] == True:
			self.x += self.spd[0]
			if not self.canMove():
				self.x -= self.spd[0]

		self.y -= self.spd[1]
		if not self.canMove():
			self.y += self.spd[1]
			self.y += self.lockToGround(self.spd[1])
			self.y = math.ceil(self.y)
			self.spd[1] = 0
		elif not self.isOnGround():
			self.spd[1] -= gravity
		if self.isOnGround() and (controls['keyW'] == True or controls['keySpace'] == True):
			self.spd[1] = 10

	def draw(self):
		ctx.blit(self.img[self.level],(self.x,self.y))

levelRects = [Selection(100,100,300,150,media.blueOG,3),
				Selection(100,350,300,150,media.blueOG,4),
				Selection(500,100,300,150,media.blueOG,5),
				Selection(500,350,300,150,media.blueOG,6)]
daniel= Player(10, 520, 30, 60, 5, media.playerBody, 0)

class Level(object):
	def __init__(self,start,goal,materials):
		self.start = start
		self.goal = goal
		self.materials = materials
	def load(self):
		pass

levels = [0,0,0,"""the levels"""]

def titleScreen():
	ctx.fill(media.blueOG)    
	title, titleRECT = media.centeredText("ALBERT THE INTIMIDATING", 60, (31,31,31), gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2
	ctx.blit(title,titleRECT)

	title, titleRECT = media.centeredText("click anywhere to continue", 30, (31,31,31),gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 -200
	ctx.blit(title,titleRECT)

	fps = media.mulismall.render(str(round(clock.get_fps(),1)),True,media.black)
	fpsRECT = fps.get_rect()
	ctx.blit(fps,(5,0))

def instructions():
	ctx.fill(media.blueOG)
	title, titleRECT = media.centeredText("Instructions", 60,(31,31,31), gameW)
	titleRECT.top = titleRECT.height/2 +10
	ctx.blit(title,titleRECT)
	title, titleRECT = media.centeredText("wasd to move", 30,(31,31,31), gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 -100
	ctx.blit(title,titleRECT)
	title, titleRECT = media.centeredText("space to jump", 30,(31,31,31), gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 -50
	ctx.blit(title,titleRECT)
	title, titleRECT = media.centeredText("Drag and drop objects to build your environment", 30, (31,31,31),gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 -0
	ctx.blit(title,titleRECT)
	title, titleRECT = media.centeredText("Reach the goal zone to improve your sad life", 30,(31,31,31), gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 +50
	ctx.blit(title,titleRECT)
	title, titleRECT = media.centeredText("click anywhere to continue on living your sad life", 30,(31,31,31), gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 +200
	ctx.blit(title,titleRECT)
    
def levelSelect():
	ctx.fill(media.greyBG)
	levelNum = 1
	for l in levelRects:
		l.draw()
		text, textRect = media.centeredText("Level " + str(levelNum), 50, (31,31,31),300)
		textRect.left += l.x
		textRect.top = l.y + l.h/2 - textRect.h/2 - 5 #-5 aesthetic
		ctx.blit(text,textRect)
		levelNum += 1

obstructions = [Entity(0,580,900,20,media.blueBlocks)]
returnButton = Selection(725,25,150,80,media.blueBlocks,2)
materialButton = Selection(750,300,100,50,(0,105,207),-1)
def level():
	ctx.fill(media.greyBG)
<<<<<<< HEAD
	pygame.draw.rect(ctx,(206,206,206),(700,0,200,600)) # right panel
	
	for o in obstructions:
		o.go()
	returnButton.go();

=======

	pygame.draw.rect(ctx,(206,206,206),(700,0,200,600))
	pygame.draw.rect(ctx,(0,65,128),(0,580,900,20))
	returnButton.go()
	pygame.draw.rect(ctx,(0,65,128),(0,580,900,20))
>>>>>>> 72639d9d68d2971b9e57f11da1d67c2ef99ceb5b
	text, textRect = media.centeredText("Select Level", 20, (206,206,206), 150)
	textRect.left += 725
	textRect.top = 25 + 40 - textRect.h/2
	ctx.blit(text,textRect)
<<<<<<< HEAD

	pygame.draw.rect(ctx,(30,144,255),(725,475,150,80))
=======
	materialButton.go()
>>>>>>> 72639d9d68d2971b9e57f11da1d67c2ef99ceb5b
	text, textRect = media.centeredText("GO", 50, (206,206,206), 150)
	textRect.left += 730-2 
	textRect.top = 475 + 35 - textRect.h/2
	ctx.blit(text,textRect)

	daniel.go()
    
    #level 1 specifics
	pygame.draw.rect(ctx,(0,105,207),(750,300,100,50))
	text, textRect = media.centeredText("x4", 30, (30,144,255), 50)
	textRect.left += 805 
	textRect.top = 300 + 35-2 - textRect.h/2
	ctx.blit(text,textRect)
    
	if(mouse['held'] && collisions.pointRect(mouse['pos'],materialButton):
#material is set to exist and be moving
       
       
        

def close():
	pygame.quit()
	quit()

def main():
	global screenid
	while True:

		# EVENT HANDLING
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

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				close()
			elif event.type == pygame.KEYDOWN:
				for p in presets:
					if event.key == presets[p]:
						controls[p] = True
			elif event.type == pygame.KEYUP:
				for p in presets:
					if event.key == presets[p]:
						controls[p] = False


		# SCREEN CHANGING
		if mouse['click']:
			if screenid < 2:
				screenid += 1
			elif screenid == 2:
				for l in levelRects:
					if collisions.pointRect(mouse['pos'],l):
						#levels[l.levelID].load()
						screenid += 1
			elif collisions.pointRect(mouse['pos'],returnButton):
				screenid = 2

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