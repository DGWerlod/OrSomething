import pygame, math, random
pygame.init()

ctx = pygame.display.set_mode((200,100))
pygame.display.set_caption("CircleGame")
clock = pygame.time.Clock()

class Room(object):
	def __init__(self):
		pass

def close():
	pygame.quit()
	quit()


def main():
	pygame.display.update()
	clock.tick(2)
main()