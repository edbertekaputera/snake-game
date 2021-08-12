import pygame
import time
import random


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
BLUE = (29, 140, 204)
RED = (255,0,0)

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

#Scoreboard
score = 0

#Fonts
font_base = pygame.font.Font(None, 50)

#TEXTBOX FUNCTION
def textbox(font, txt, colour,pos):
	text = font.render(txt, True, colour)
	screen.blit(text, pos)

#SNAKE FUNCTION
def snake(snake_segments):
	for segment in snake_segments:
		pygame.draw.rect(screen, BLUE, [segment[0], segment[1], 20, 20])
	if direction == "up":
		pygame.draw.circle(screen, BLACK, (snake_segments[-1][0]+5,snake_segments[-1][1]+5), 2)
		pygame.draw.circle(screen, BLACK, (snake_segments[-1][0]+15,snake_segments[-1][1]+5), 2)
	elif direction == "down":
		pygame.draw.circle(screen, BLACK, (snake_segments[-1][0]+5,snake_segments[-1][1]+15), 2)
		pygame.draw.circle(screen, BLACK, (snake_segments[-1][0]+15,snake_segments[-1][1]+15), 2)
	elif direction == "left":
		pygame.draw.circle(screen, BLACK, (snake_segments[-1][0]+5,snake_segments[-1][1]+5), 2)
		pygame.draw.circle(screen, BLACK, (snake_segments[-1][0]+5,snake_segments[-1][1]+15), 2)
	elif direction == "right":
		pygame.draw.circle(screen, BLACK, (snake_segments[-1][0]+15,snake_segments[-1][1]+15), 2)
		pygame.draw.circle(screen, BLACK, (snake_segments[-1][0]+15,snake_segments[-1][1]+5), 2)
	
		
#SNAKE PROPERTIES
x = 190
y = 160
x_change = 0
y_change = 0
speed = 6
snake_segments = []
length_snake = 1
direction = ""

#TICKRATE for snake speed
clock = pygame.time.Clock()

#Position of food
food_x = random.randrange(20,380, 30)
food_y = random.randrange(20, 350, 30)

#Conditions for game to run
game_running = True

while game_running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT and direction != "right":
				x_change = -30
				y_change = 0
				direction = "left"
			elif event.key == pygame.K_RIGHT and direction !="left":
				x_change = 30
				y_change = 0
				direction = "right"
			elif event.key == pygame.K_UP and direction != "down":
				x_change = 0
				y_change = -30
				direction = "up"			
			elif event.key == pygame.K_DOWN and direction != "up":
				x_change = 0
				y_change = 30
				direction = "down"

	x += x_change
	y += y_change

	head = [x,y]
	snake_segments.append(head)
	if len(snake_segments) > length_snake:
		snake_segments.pop(0)

	screen.blit(background, (0,0))
	textbox(font_base,f"Score = {score}", BLACK, (120,355))
	pygame.draw.circle(screen, RED, (food_x,food_y), 10)
	if x < 10 or x > 390 or y < 10 or y > 310:
		game_running = False
		break
	else:
		snake(snake_segments)

	for segment in snake_segments[:-1]:
		if segment == head:
			game_running = False
			break

	if x == food_x - 10 and y == food_y - 10:
		score += 1
		food_x = random.randrange(20,380, 30)
		food_y = random.randrange(20, 350, 30)
		length_snake += 1
	pygame.display.update()
	clock.tick(speed)


#Death Message Box
textbox(font_base, "You have lost!", RED, (50,150))
textbox(font_base, f"Your Score is {score}", RED, (50,200))
pygame.display.update()
time.sleep(2)

pygame.quit()
quit()