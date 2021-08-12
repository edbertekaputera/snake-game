import pygame

#Constants (UPPERCASE NAMES)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
FIELD_WIDTH = 390
FIELD_HEIGHT = 330
SCOREBOARD_WIDTH = 400
SCOREBOARD_HEIGHT = 60

LIGHT_GREEN = (163,219,74)
DARK_GREEN = (133, 194, 56)
ORANGE = (191, 93, 57)
BLACK = (0,0,0)

#2D Gameboard Screen Initiation
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Edbert Ekaputera's Snake Game")

#Background => (11 rows, 13 cols) + Scoreboard
background = pygame.surface.Surface(screen.get_size())
bg_color = LIGHT_GREEN
pygame.draw.rect(background,BLACK,[0, 0, 400, 370])
for x in range(5, FIELD_WIDTH+5, 30):
   for y in range(5, FIELD_HEIGHT+5, 30):
   		pygame.draw.rect(background, bg_color, [x, y, 30, 30])
   		if bg_color == LIGHT_GREEN:
   			bg_color = DARK_GREEN
   		else:
   			bg_color = LIGHT_GREEN
pygame.draw.rect(background, ORANGE, [0,FIELD_HEIGHT+10, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT])

#Conditions for game to run
game_running = True
while game_running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_running = False
		print(event)
	screen.blit(background, (0,0))
	pygame.display.update()

pygame.quit()
quit()