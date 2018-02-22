# IMPORTS
import pygame, math, random, copy
import media, collisions, text
pygame.init()

# GLOBAL VAR SETUP
global gameW, gameH, gameIW, presets, controls, mouse, screenid, inConstruction
gameW, gameH, gameIW = 900, 600, 700
presets = {'keyW':pygame.K_w,'keyA':pygame.K_a,'keyS':pygame.K_s,'keyD':pygame.K_d,'keySpace':pygame.K_SPACE}
controls = {'keyW':False,'keyA':False,'keyS':False,'keyD':False,'keySpace':False}
mouse = {'pos':pygame.mouse.get_pos(),'left_click':False,'left_held':False,'right_click':False,'right_held':False}
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
		# pygame.draw.rect(ctx,self.color,(self.x,self.y,self.w,self.h),2)
		dashedRect(self.x, self.y, self.w, self.h, 2, 3, 10, self.color)

class RedZone(Entity):
	def  __init__(self,x,y,w,h,alpha=128):
		super().__init__(x,y,w,h,media.red)
		self.surface = pygame.Surface((w,h))
		self.surface.set_alpha(alpha)
		self.surface.fill(self.color)
	def draw(self):
		ctx.blit(self.surface, (self.x,self.y))

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
	def pos(self):
		self.x = mouse['pos'][0]-self.w/2
		self.y = mouse['pos'][1]-self.h/2
	def go(self):
		if self.exists:
			if not mouse['left_held']:
				if self.canPlace():
					self.moving = False
				else:
					resetMaterial(self)
			if self.moving:
				self.pos()
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
text.buildLevelText(levelRects)

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
	def __init__(self,start,goal,materials,obstructions,redzones=[],enemies=[]): 
		self.start = start
		self.goal = goal
		self.obstructions = obstructions
		self.redzones = redzones
		self.enemies = enemies
		self.materials = []
		typeIndex = 0
		for m in materials:
			self.materials.append([])
			for i in range(0,m):
				self.materials[typeIndex].append(Material(typeIndex))
			typeIndex += 1
	def load(self):
		daniel.x = self.start[0]
		daniel.y = self.start[1]
		goalLocation.x = self.goal[0]
		goalLocation.y = self.goal[1]

		global obstructions, materials, usedMaterials
		obstructions = copy.deepcopy(self.obstructions)
		materials = copy.deepcopy(self.materials)
		usedMaterials = [[],[],[]]

# COMMON LEVEL ELEMENTS ARE PREBUILT HERE
ground = Entity(0,580,gameIW,20,media.darkBlue)
startPlatform = Entity(0,580,100,20,media.darkBlue)

# LEVELS ARE BUILT AND ADDED HERE
levels = [0,0,0, # first 3 empty indeces to comply with opening screens
		Level((10,520),(660,10),[4,0,0],
			[ground]),

		Level((10,520),(660,10),[1,2,1],
			[ground,Entity(345,80,10,520,media.darkBlue)]),

		Level((10,520),(660,10),[0,1,4],
			[ground,Entity(195,150,10,450,media.darkBlue),Entity(395,0,10,450,media.darkBlue)]),

		Level((10,520),(660,10),[0,0,4],
			[startPlatform]),

		Level((10,520),(660,10),[1,0,3],
			[startPlatform,Entity(295,300,10,300,media.darkBlue),Entity(395,0,10,450,media.darkBlue)]),

		Level((10,520),(660,10),[0,1,4],
			[startPlatform,Entity(0,470,300,10,media.darkBlue)]),
]

# HELPER FUNCTIONS

def pickupMaterial(selectionID):
	materials[selectionID][0].pos()
	materials[selectionID][0].exists, materials[selectionID][0].moving = True, True
	usedMaterials[selectionID].append(materials[selectionID][0])
	materials[selectionID].remove(materials[selectionID][0])
	text.refreshCounter(selectionID, len(materials[selectionID]))

def resetMaterial(material):
	material.pos()
	material.exists, material.moving = False, False
	materials[material.type].append(material)
	usedMaterials[material.type].remove(material)
	text.refreshCounter(material.type, len(materials[material.type]))

def switchMode():
	global inConstruction
	inConstruction = not inConstruction
	daniel.x = levels[screenid].start[0]
	daniel.y = levels[screenid].start[1]

def dashedRect(x, y, w, h, sW, sG, sA, color):
	# sW = stroke width (thickness), sG = stroke gap (blank space to left and right of dash in each sA),
	# sA = stroke area (the amount of pixels equal to the sum of one stroke length and two stroke gaps)
	for dx in range(0,w,sA):
		pygame.draw.line(ctx,color,(x + dx + sG, y),(x + dx + sA-sG, y),sW)
		pygame.draw.line(ctx,color,(x + dx + sG, y + h-sW/2),(x + dx + sA-sG, y + h-sW/2),sW)
	for dy in range(0,h,sA):
		pygame.draw.line(ctx,color,(x, y + dy + sG),(x, y + dy + sA-sG),2)
		pygame.draw.line(ctx,color,(x + w-sW/2, y + dy + sG),(x + w-sW/2, y + dy + sA-sG),sW)


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

	# LEVEL BUTTONS AND TEXT
	for l in levelRects:
		l.go()
	for t in text.levelText:
		ctx.blit(t[0],t[1])

	# RETURN BUTTON AND TEXT
	instructionButton.go()
	
	ctx.blit(text.returnToInstructions,text.returnToInstructionsRect)   
    
def level():
	# BACKGROUNDS
	# ctx.fill(media.lightGrey)
	ctx.blit(media.background, (0,0))
	pygame.draw.rect(ctx, media.levelGrey,(gameIW,0,200,gameH))
	pygame.draw.line(ctx, media.black,(gameIW-1,0),(gameIW-1,gameH),2)
	pygame.draw.rect(ctx, media.darkBlue,(gameIW-1,580,200+1,20)) # ground below right panel for symmetry
	
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
			if mouse['left_held'] == False:
				mouse['left_click'] = True
				mouse['left_held'] = True
			else:
				mouse['left_click'] = False
		else:
			mouse['left_click'] = False
			mouse['left_held'] = False
		if info[2] == True:
			if mouse['right_held'] == False:
				mouse['right_click'] = True
				mouse['right_held'] = True
			else:
				mouse['right_click'] = False
		else:
			mouse['right_click'] = False
			mouse['right_held'] = False

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
		if mouse['left_click']:
			
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
					for u in usedMaterials:
						for uu in u:
							if collisions.pointRect(mouse['pos'],uu):
								resetMaterial(uu)
					for mb in materialButtons:
						if collisions.pointRect(mouse['pos'],mb):
							if len(materials[mb.selectionID]) != 0:
								pickupMaterial(mb.selectionID)
							else:
								pass #print("NO MORE OF ID " + str(mb.selectionID))

				# SWITCH IN/OUT OF CONSTRUCTION
				if collisions.pointRect(mouse['pos'], goButton):
					switchMode()

		if mouse['right_click']:
			if screenid > 2:
				switchMode()

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