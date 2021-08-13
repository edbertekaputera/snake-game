import pygame
import time
from random import randrange


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

#Fonts
font_base = pygame.font.Font(None, 50)

#TEXTBOX FUNCTION
def textbox(font, txt, colour,pos):
	text = font.render(txt, True, colour)
	screen.blit(text, pos)

#SNAKE CLASS
class Snake:
	def __init__(self):
		#SNAKE PROPERTIES
		self.x = 190
		self.y = 160
		self.x_change = 0
		self.y_change = 0
		self.speed = 6
		self.length = 1
		self.direction = ""
		self.head = []
		self.segments = []

	def draw(self):
		for segment in self.segments:
			pygame.draw.rect(screen, BLUE, [segment[0], segment[1], 20, 20])
		if self.direction == "up":
			pygame.draw.circle(screen, BLACK, (self.segments[-1][0]+5,self.segments[-1][1]+5), 2)
			pygame.draw.circle(screen, BLACK, (self.segments[-1][0]+15,self.segments[-1][1]+5), 2)
		elif self.direction == "down":
			pygame.draw.circle(screen, BLACK, (self.segments[-1][0]+5,self.segments[-1][1]+15), 2)
			pygame.draw.circle(screen, BLACK, (self.segments[-1][0]+15,self.segments[-1][1]+15), 2)
		elif self.direction == "left":
			pygame.draw.circle(screen, BLACK, (self.segments[-1][0]+5,self.segments[-1][1]+5), 2)
			pygame.draw.circle(screen, BLACK, (self.segments[-1][0]+5,self.segments[-1][1]+15), 2)
		elif self.direction == "right":
			pygame.draw.circle(screen, BLACK, (self.segments[-1][0]+15,self.segments[-1][1]+15), 2)
			pygame.draw.circle(screen, BLACK, (self.segments[-1][0]+15,self.segments[-1][1]+5), 2)
	
	def eat_check(self, food):
		if self.x == food.x - 10 and self.y == food.y - 10:
			food.reposition()
			self.length += 1

	def move(self):
		self.x += self.x_change
		self.y += self.y_change
		self.head = [self.x, self.y]
		self.segments.append(self.head)
		if len(self.segments) > self.length:
			self.segments.pop(0)

	def motion_direction(self, event):
		if event.key == pygame.K_LEFT and self.direction != "right":
			self.x_change = -30
			self.y_change = 0
			self.direction = "left"
		elif event.key == pygame.K_RIGHT and self.direction !="left":
			self.x_change = 30
			self.y_change = 0
			self.direction = "right"
		elif event.key == pygame.K_UP and self.direction != "down":
			self.x_change = 0
			self.y_change = -30
			self.direction = "up"			
		elif event.key == pygame.K_DOWN and self.direction != "up":
			self.x_change = 0
			self.y_change = 30
			self.direction = "down"

#FOOD CLASS
class Food:
	def __init__(self):
		#Properties of food
		self.x = randrange(20,380, 30)
		self.y = randrange(20, 350, 30)
		self.radius = 10

	def draw(self):
		pygame.draw.circle(screen, RED, (self.x,self.y), self.radius)

	def reposition(self):
		self.x = randrange(20,380, 30)
		self.y = randrange(20, 350, 30)


#Class initiation
snake = Snake()
food = Food()

#TICKRATE for snake speed
clock = pygame.time.Clock()

#Conditions for game to run
game_running = True

while game_running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_running = False
		elif event.type == pygame.KEYDOWN:
			snake.motion_direction(event)

	snake.move()

	screen.blit(background, (0,0))
	textbox(font_base,f"Score = {snake.length-1}", BLACK, (120,355))
	food.draw()	

	#DEATH CONDITION
	if snake.x < 10 or snake.x > 390 or snake.y < 10 or snake.y > 310:
		game_running = False
		break
	else:
		snake.draw()

	for segment in snake.segments[:-1]:
		if segment == snake.head:
			game_running = False
			break
	
	#EAT FOOD CONDITION
	snake.eat_check(food)

	pygame.display.update()
	clock.tick(snake.speed)


#Death Message Box
textbox(font_base, "You have lost!", RED, (50,150))
textbox(font_base, f"Your Score is {snake.length-1}", RED, (50,200))
pygame.display.update()
time.sleep(2)

pygame.quit()
quit()