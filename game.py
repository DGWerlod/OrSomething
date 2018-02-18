import pygame, math, random
import media, collisions
pygame.init()

global gameW, gameH, gameIW, presets, controls, mouse, screenid
gameW, gameH, gameIW = 900, 600, 700
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
	def  __init__(self,x,y,w,h,color,selectionID):
		super().__init__(x,y,w,h,color)
		self.selectionID = selectionID

class Material(Entity):
	def __init__(self,w,h):
		super().__init__(0,0,w,h,media.blueBlocks)
		self.exists = False
		self.moving = False
	def pickup(self):
		self.exists = True
		self.moving = True
	def go(self):
		if self.exists:
			if not mouse['held']:
				self.moving = False
			if self.moving:
				self.x = mouse['pos'][0]-self.w/2
				self.y = mouse['pos'][1]-self.h/2
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
		for o in obstructions:
			if collisions.rectangles(self,o):
				return False
		if self.y < 0 or self.x < 0 or self.y + self.h > gameH or self.x + self.w > gameIW:
			return False
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
			self.spd[1] = 15

	def draw(self):
		ctx.blit(self.img[self.level],(self.x,self.y))

levelRects = [Selection(100,100,300,150,media.blueOG,3),
				Selection(100,350,300,150,media.blueOG,4),
				Selection(500,100,300,150,media.blueOG,5),
				Selection(500,350,300,150,media.blueOG,6)]
returnButton = Selection(725,25,150,80,media.blueBlocks,2)
materialButtons = [Selection(750,225,100,50,(0,105,207),0),
					Selection(750,300,50,50,(0,105,207),1),
					Selection(750,375,25,50,(0,105,207),2)]

goalLocation = Entity(0,0,30,60,media.blueOG)
global obstructions, materials, usedMaterials
obstructions = []
materials = [[],[],[]]
usedMaterials = [[],[],[]]

daniel= Player(10, 520, 30, 60, 5, media.playerBody, 0)

class Level(object):
	def __init__(self,start,goal,obstructions,materials):
		self.start = start
		self.goal = goal
		self.obstructions = obstructions
		self.materials = materials
	def load(self):
		daniel.x = self.start[0]
		daniel.y = self.start[1]
		goalLocation.x = self.goal[0]
		goalLocation.y = self.goal[1]

		global obstructions, materials, usedMaterials
		obstructions = self.obstructions
		materials = self.materials
		usedMaterials = [[],[],[]]


levels = [0,0,0,
		Level((10,520),(660,10),
			[Entity(0,580,900,20,media.blueBlocks)],
			[[Material(100,50),Material(100,50),Material(100,50),Material(100,50)],
			[],[]])
]

def titleScreen():
	ctx.fill(media.greyBG)
	title, titleRECT = media.centeredText("ALBERT", 60, media.blueOG, gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2
	ctx.blit(title,titleRECT)

	title, titleRECT = media.centeredText("click anywhere to continue", 30, media.blueOG,gameW)
	titleRECT.top = gameH/2 - titleRECT.height/2 +200
	ctx.blit(title,titleRECT)

def instructions():
	ctx.fill(media.greyBG)
	title, titleRECT = media.centeredText("Instructions", 60, media.blueOG, gameW)
	titleRECT.top = titleRECT.height/2 +10
	ctx.blit(title,titleRECT)
    
	instructionsList = ["1. Drag and drop objects to build your environment",
						"2. Hit GO to start moving",
						"3. Use wasd to move and space to jump",
						"4. Reach the goal zone to improve your sad life"]

	iList = 0
	for heightChange in range(50,-150,-50):
		title, titleRECT = media.centeredText(instructionsList[iList], 30, media.blueOG, gameW)
		titleRECT.top = gameH/2 - titleRECT.height/2 - heightChange
		ctx.blit(title,titleRECT)
		iList += 1
    
	title, titleRECT = media.centeredText("click anywhere to continue", 30, media.blueOG, gameW)
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

def level():
	ctx.fill(media.greyBG)
	pygame.draw.rect(ctx,(206,206,206),(700,0,200,600)) # right panel

	for o in obstructions:
		o.go()

	returnButton.go()

	text, textRect = media.centeredText("Select Level", 20, (206,206,206), 150)
	textRect.left += 725
	textRect.top = 25 + 40 - textRect.h/2
	ctx.blit(text,textRect)

	pygame.draw.rect(ctx,(30,144,255),(725,475,150,80))
	for mb in materialButtons:
		mb.go()
    
	text, textRect = media.centeredText("GO", 50, (206,206,206), 150)
	textRect.left += 730-2 
	textRect.top = 475 + 35 - textRect.h/2
	ctx.blit(text,textRect)

	for u in usedMaterials:
		for uu in u:
			uu.go()

	daniel.go()

	#level 1 specifics
	text, textRect = media.centeredText("x4", 30, (30,144,255), 50)
	textRect.left += 825 
	textRect.top = 225 + 35-2 - textRect.h/2
	ctx.blit(text,textRect)
    
	text, textRect = media.centeredText("x4", 30, (30,144,255), 50)
	textRect.left += 825 
	textRect.top = 300 + 35-2 - textRect.h/2
	ctx.blit(text,textRect)
    
	text, textRect = media.centeredText("x4", 30, (30,144,255), 50)
	textRect.left += 825 
	textRect.top = 375 + 35-2 - textRect.h/2
	ctx.blit(text,textRect)
    
	#if(mouse['held'] && collisions.pointRect(mouse['pos'],materialButton):
	#material is set to exist and be moving

def close():
	pygame.quit()
	quit()

def main():
	global screenid
	while True:

		# EVENT HANDLING
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
						levels[l.selectionID].load()
						screenid += 1
			else:
				if collisions.pointRect(mouse['pos'],returnButton):
					screenid = 2
				for mb in materialButtons:
					if collisions.pointRect(mouse['pos'],mb):
						if len(materials[mb.selectionID]) != 0:
							materials[mb.selectionID][0].pickup()
							usedMaterials[mb.selectionID].append(materials[mb.selectionID][0])
							materials[mb.selectionID].remove(materials[mb.selectionID][0])
							
						else:
							#print("NO MORE OF ID " + str(mb.selectionID))
				for u in usedMaterials:
					for uu in u:
						if collisions.pointRect(mouse['pos'],uu):
							uu.exists = False
							materials[usedMaterials.index(u)].append(uu)
							u.remove(uu)

		if screenid == 0:
			titleScreen()
		elif screenid == 1:
			instructions()
		elif screenid == 2:
			levelSelect()
		else:
			level()

		# DEBUG
		fps = media.mulismall.render(str(round(clock.get_fps(),1)),True,media.black)
		fpsRECT = fps.get_rect()
		ctx.blit(fps,(5,0))

		pygame.display.update()
		clock.tick(60)
main()