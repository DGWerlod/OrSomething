# IMPORTS
import pygame, math, random, copy
import media, collisions, text
pygame.init()

# GLOBAL VAR SETUP
global gameW, gameH, gameIW, presets, controls, mouse, screenid, inConstruction
gameW, gameH, gameIW = 900, 600, 700
presets = {'keyW':pygame.K_w,'keyA':pygame.K_a,'keyS':pygame.K_s,'keyD':pygame.K_d,'keySpace':pygame.K_SPACE}
controls = {'keyW':False,'keyA':False,'keyS':False,'keyD':False,'keySpace':False}
mouse = {'pos':pygame.mouse.get_pos(),'click':False,'held':False}
screenid = 0
gravity = 0.75
inConstruction = True

# PYGAME WINDOW SETUP
ctx = pygame.display.set_mode((gameW,gameH))
pygame.display.set_caption("Albert")
clock = pygame.time.Clock()

# CLASSES

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

class Goal(Entity):
	def  __init__(self,x,y,w,h,color):
		super().__init__(x,y,w,h,color)
	def draw(self):
		pygame.draw.rect(ctx,self.color,(self.x,self.y,self.w,self.h),2)

class Selection(Entity):
	def  __init__(self,x,y,w,h,color,selectionID,strokeWidth=0):
		super().__init__(x,y,w,h,color)
		self.selectionID = selectionID
		self.strokeWidth = strokeWidth
	def draw(self):
		if self.strokeWidth > 0:
			pygame.draw.rect(ctx,self.color,(self.x,self.y,self.w,self.h),self.strokeWidth)
		else:
			super().draw()

class Material(Entity):
	def __init__(self,type):
		if type == 0:
			w, h = 100, 50
		elif type == 1:
			w, h = 50, 50
		elif type == 2:
			w, h = 25, 50
		else:
			print("Material type " + str(type) + " does not exist")
		super().__init__(0,0,w,h,media.mediumBlue)
		self.exists = False
		self.moving = False
		self.type = type
	def canPlace(self):
		for mb in materialButtons:
			if collisions.rectangles(self,mb):
				return False
		return True
	def go(self):
		if self.exists:
			if not mouse['held']:
				if self.canPlace():
					self.moving = False
				else:
					resetMaterial(self)
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
		global inConstruction
		if inConstruction:
			return False
		if self.y > gameH:
			inConstruction = True
		for o in obstructions:
			if collisions.rectangles(self,o):
				return False
		for u in usedMaterials:
			for uu in u:
				if collisions.rectangles(self,uu):
					return False
		if self.y < 0 or self.x < 0 or self.x + self.w > gameIW:
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

# STATIC OBJECT SETUP

levelRects = [Selection(25,25,250,175,media.blueOG,3,2),
				Selection(325,25,250,175,media.blueOG,4,2),
				Selection(625,25,250,175,media.blueOG,5,2),
				Selection(25,225,250,175,media.blueOG,6,2),
				Selection(325,225,250,175,media.blueOG,7,2),
				Selection(625,225,250,175,media.blueOG,8,2)]
instructionButton = Selection(200,425,500,150,media.blueOG,9,2)
returnButton = Selection(725,25,150,80,media.darkBlue,2)
materialButtons = [Selection(725,200,100,50,media.mediumBlue,0),
					Selection(725,275,50,50,media.mediumBlue,1),
					Selection(725,350,25,50,media.mediumBlue,2)]
goButton = Selection(725,475,150,80,media.mediumBlue,-1)

# DYNAMIC OBJECT SETUP

goalLocation = Goal(0,0,30,60,media.blueOG)
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
		obstructions = copy.deepcopy(self.obstructions)
		materials = copy.deepcopy(self.materials)
		usedMaterials = [[],[],[]]

# LEVELS ARE BUILT AND ADDED HERE
levels = [0,0,0, # first 3 empty indeces to comply with opening screens
		Level((10,520),(660,10),
			[Entity(0,580,900,20,media.darkBlue)],
			[[Material(0),Material(0),Material(0),Material(0)],
			[],[]]),
		Level((10,520),(660,10),
			[Entity(0,580,900,20,media.darkBlue),Entity(345,80,10,520,media.darkBlue)],
			[[Material(0)],
			[Material(1),Material(1)],[Material(2)]]),
		Level((10,520),(660,10),
			[Entity(0,580,900,20,media.darkBlue),Entity(195,150,10,450,media.darkBlue),Entity(395,0,10,450,media.darkBlue)],
			[[],[Material(1)],[Material(2),Material(2),Material(2),Material(2)]]),
		Level((10,520),(660,10),
			[Entity(0,580,100,20,media.darkBlue),Entity(700,580,200,20,media.darkBlue)],
			[[],[],[Material(2),Material(2),Material(2),Material(2)]]),
		Level((10,520),(660,10),
			[Entity(0,580,100,20,media.darkBlue),Entity(700,580,200,20,media.darkBlue),Entity(295,300,10,300,media.darkBlue),Entity(395,0,10,450,media.darkBlue)],
			[[Material(0)],[],[Material(2),Material(2),Material(2)]]),
		Level((10,520),(660,10),
			[Entity(0,580,100,20,media.darkBlue),Entity(700,580,200,20,media.darkBlue),Entity(0,470,300,10,media.darkBlue),],
			[[],[Material(1)],[Material(2),Material(2),Material(2),Material(2)]]),
]

# HELPER FUNCTIONS

def pickupMaterial(selectionID):
	materials[selectionID][0].exists = True
	materials[selectionID][0].moving = True
	usedMaterials[selectionID].append(materials[selectionID][0])
	materials[selectionID].remove(materials[selectionID][0])
	text.refreshCounter(selectionID, len(materials[selectionID]))

def resetMaterial(material):
	material.exists = False
	materials[material.type].append(material)
	usedMaterials[material.type].remove(material)
	text.refreshCounter(material.type, len(materials[material.type]))

# SCREEN TYPE FUNCTIONS

def titleScreen():
	ctx.fill(media.lightGrey)
	ctx.blit(text.title,text.titleRECT)
	ctx.blit(text.footer,text.footerRECT)

def instructions():
	ctx.fill(media.lightGrey)
	ctx.blit(text.instructionsHeader,text.instructionsHeaderRECT)
	for l in text.instructions:
		ctx.blit(l[0],l[1])
	ctx.blit(text.footer,text.footerRECT)

def levelSelect():
	ctx.fill(media.lightGrey)
	levelNum = 1

	# LEVEL BUTTONS AND TEXT
	for l in levelRects:
		l.go()
		text, textRect = media.centeredText("Level " + str(levelNum), 50,  media.blueOG,250)
		textRect.left += l.x
		textRect.top = l.y + l.h/2 - textRect.h/2 - 3 #-3 aesthetic
		ctx.blit(text,textRect)
		levelNum += 1

	# RETURN BUTTON AND TEXT
	instructionButton.go()
	text, textRect = media.centeredText("Return to Instructions", 30,  media.blueOG, 500)
	textRect.left += 200
	textRect.top = 425 + 75 - textRect.h/2 - 3 #-3 aesthetic
	ctx.blit(text,textRect)   
    
def level():
	# BACKGROUNDS
	# ctx.fill(media.lightGrey)
	ctx.blit(media.background, (0,0))
	pygame.draw.rect(ctx, media.darkGrey,(700,0,200,600))

	# BUTTONS
	
	returnButton.go()
	ctx.blit(text.returnToLevels,text.returnToLevelsRECT)

	goButton.go()
	if(inConstruction):
		ctx.blit(text.goButton,text.goButtonRECT)
	else:
		ctx.blit(text.stopButton,text.stopButtonRECT)

	for mb in materialButtons:
		mb.go()
	for c in text.counters:
		ctx.blit(c[0],c[1])

	# PLATFORMING ELEMENTS
	for o in obstructions:
		o.go()
	for u in usedMaterials:
		for uu in u:
			uu.go()

	# PLAYER ELEMENTS
	goalLocation.go()
	daniel.go()
    
    # LEVEL COMPLETION
	if collisions.rectangles(goalLocation,daniel):
		global screenid
		screenid = 2

def close():
	pygame.display.quit() # prevents a rare crashing bug
	pygame.quit()
	quit()

def main():
	global screenid, inConstruction
	while True:

		# EVENT HANDLING - MOUSE
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

		# EVENT HANDLING - KEYS
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

		# CLICK ACTIONS
		if mouse['click']:
			
			# INTRO SCREENS
			if screenid < 2:
				screenid += 1

			# LEVEL SELECT
			elif screenid == 2:
				for l in levelRects:
					if collisions.pointRect(mouse['pos'],l):
						inConstruction = True
						screenid = l.selectionID
						levels[screenid].load()
						for c in range(0,3):
							text.refreshCounter(c,len(materials[c]))
				if collisions.pointRect(mouse['pos'],instructionButton):
					screenid -= 1

			# IN-LEVEL ACTIONS
			else:
				if collisions.pointRect(mouse['pos'],returnButton):
					screenid = 2
				if inConstruction:
					for mb in materialButtons:
						if collisions.pointRect(mouse['pos'],mb):
							if len(materials[mb.selectionID]) != 0:
								pickupMaterial(mb.selectionID)
							else:
								pass #print("NO MORE OF ID " + str(mb.selectionID))
					for u in usedMaterials:
						for uu in u:
							if collisions.pointRect(mouse['pos'],uu):
								resetMaterial(uu)

				# SWITCH IN/OUT OF CONSTRUCTION
				if collisions.pointRect(mouse['pos'], goButton):
					inConstruction = not inConstruction
					daniel.x = levels[screenid].start[0]
					daniel.y = levels[screenid].start[1]

		# SCREEN STATUS
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