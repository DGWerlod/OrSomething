import pygame
pygame.font.init()

# FONTS

muli = pygame.font.Font("fonts/muli.ttf",60)
mulismall = pygame.font.Font("fonts/muli.ttf",15)

def buildText(rawText,size,color):
	font = pygame.font.Font("fonts/muli.ttf",size)
	text = font.render(rawText,True,color)
	return text

def centeredText(rawText,size,color,widthOfParent):
	text = buildText(rawText,size,color)
	textRect = text.get_rect()
	textRect.left = widthOfParent/2 - textRect.width/2
	return text, textRect

# IMAGES

background = pygame.image.load("img/backgroundLight.png")
playerBody = [pygame.image.load("img/basic.png"),
			pygame.image.load("img/lessBasic.png"),
			pygame.image.load("img/leastBasic.png"),]

# COLORS

black = (0,0,0)
white = (255,255,255)

blueOG = (30,144,255)
mediumBlue = (0,105,207)
darkBlue = (0,65,128)
lightGrey = (236,236,236)
levelGrey = (221,221,221)
darkGrey =(206,206,206)

red = (255,30,32) # split compliment #2 of blueOG

# NOTES
# font.render: text, antialias, color, bg
# this creates a surface (img?) you can blit