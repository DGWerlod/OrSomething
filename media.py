import pygame
pygame.font.init()

muli = pygame.font.Font("fonts/muli.ttf",60)
mulismall = pygame.font.Font("fonts/muli.ttf",15)

# font.render: text, antialias, color, bg
# this creates a surface (img?) you can blit

def centeredText(rawText,size,widthOfParent):
	font = pygame.font.Font("fonts/muli.ttf",size)
	text = media.muli.render(rawText,True,(31,31,31))
	textRect = title.get_rect()
	textRect.left = widthOfParent/2 - textRect.width/2
	return text, textRect


# def centerText(surface,enclosure):
# 	rect = surface.get_rect()
#     rect.center = ((x+(w/2)), (y+(h/2)-2)) #-2 centers Muli
#     gameDisplay.blit(textSurf, textRect)

black = (0,0,0)
white = (255,255,255)

"""greylight = (166,166,166)
grey = (127,127,127)
greydark = (86,86,86)
greywall = (50,50,50)"""

redlight = (255,76,76)
red = (255,0,0)
reddark = (178,0,0)

orangelight = (255,192,76)
orange = (255,165,0)
orangedark = (204,132,0)

yellowlight = (255,255,102)
yellow = (255,255,0)
yellowdark = (178,178,0)

greenlight = (76,166,76)
green = (0,128,0)
greendark = (0,89,0)

"""bluelight = (102,102,255)
blue = (0,0,255)
bluedark = (0,0,178)"""

purplelight = (166,76,166)
purple = (128,0,128)
purpledark = (76,0,76)

# THE ACTUAL COLORS WE'RE USING THAT AREN'T FILLERS

blueOG = (30,144,255)
blueBlocks = (0,65,128)
greyText = (31,31,31)
greyBG = (236,236,236)
