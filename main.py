import pygame
import time
import pandas as pd
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
WHITE = (255,255,255)
GREY = (192,192,192)
GOLD = (255,215,0)
BRONZE = (181, 101, 29)

#2D Gameboard Screen Initiation
pygame.init()
clock = pygame.time.Clock()
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
font_big = pygame.font.Font(None, 50)
font_medium = pygame.font.Font(None,35)
font_verybig = pygame.font.Font(None, 100)

#TEXTBOX FUNCTION
def textbox(font, txt, colour,pos):
	text = font.render(txt, True, colour)
	screen.blit(text, pos)

#HIGHSCORE FUNCTION
database = pd.read_csv("highscore.csv", sep=";")
highscore = database["score"].max()

def highscore_update(data, score):
		timestamp = time.strftime("%B %d,%Y, %H:%M:%S", time.localtime())
		new = {"name" : name,"timestamp" : timestamp,"score" : score}
		if len(data) <= 5:
			data = data.append(new, ignore_index=True, )
			data = data.sort_values(by=["score"], ascending=False)
			data[:11].to_csv("highscore.csv", sep=";", index=False)

		elif score >= database["score"][4]:
			data = data.append(new, ignore_index=True, )
			data = data.sort_values(by=["score"], ascending=False)
			data[:11].to_csv("highscore.csv", sep=";", index=False)

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
			food.reposition(snake=self)
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

	def reposition(self, snake):
		while [self.x - 10,self.y - 10] in snake.segments: 
		#Makes sure food doesn't spawn in body
			self.x = randrange(20,380, 30)
			self.y = randrange(20, 350, 30)

#Game loop condition
game_begin = True

while game_begin:
	#Intro
	name = ""
	intro_running = True
	input_rect = pygame.Rect(130,100,250,50)
	start_rect = pygame.Rect(50, 200, 300, 150)
	button_color = GREY
	while intro_running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if start_rect.collidepoint(pygame.mouse.get_pos()):
				button_color = LIGHT_GREEN
			else:
				button_color = GREY

			if event.type == pygame.MOUSEBUTTONDOWN:
				if start_rect.collidepoint(event.pos) and len(name) > 0:
					intro_running = False
					time.sleep(0.5)
					break

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					name = name[:-1]
				elif event.key == pygame.K_RETURN:
					if len(name) > 0:
						intro_running = False
						time.sleep(0.5)
						break
				else:
					if len(name) <= 11:
						name += event.unicode

		screen.fill(BLACK)
		pygame.draw.rect(screen, WHITE, input_rect)
		pygame.draw.rect(screen, button_color, start_rect)
		textbox(font_big, "What is your name?", WHITE, [35,50])
		textbox(font_big, "Name:", WHITE, [20,110])
		textbox(font_verybig, "START", BLACK, [90,250])
		textbox(font_big, name, BLACK, [135,110])
		pygame.display.update()

	#Class initiation
	snake = Snake()
	food = Food()

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
		textbox(font_medium,f"Score = {snake.length-1}", BLACK, (30,360))
		textbox(font_medium,f"Highscore = {highscore}", BLACK, (200,360))
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
	highscore_update(database, snake.length-1)
	end_running = True
	quit_color = GREY 
	again_color = GREY
	quit_rect = pygame.Rect(40,320,150,45)
	again_rect = pygame.Rect(210,320,150,45)
	while end_running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if quit_rect.collidepoint(pygame.mouse.get_pos()):
				quit_color = LIGHT_GREEN
				again_color = GREY
			elif again_rect.collidepoint(pygame.mouse.get_pos()):
				quit_color = GREY
				again_color = LIGHT_GREEN
			else:
				quit_color = GREY
				again_color = GREY

			if event.type == pygame.MOUSEBUTTONDOWN:
				if quit_rect.collidepoint(event.pos):
					end_running = False
					game_begin = False
					time.sleep(0.5)

				elif again_rect.collidepoint(event.pos):
					end_running = False
					game_begin = True
					time.sleep(0.5)

		database = pd.read_csv("highscore.csv", sep=";")
		screen.fill(BLACK)
		pygame.draw.rect(screen, quit_color, quit_rect)
		pygame.draw.rect(screen, again_color, again_rect)
		textbox(font_medium, "TRY AGAIN", BLACK,[216,330])
		textbox(font_medium, "QUIT GAME", BLACK,[44,330])

		textbox(font_big, "Leaderboards", LIGHT_GREEN, [80,100])
		if len(database) >= 1:
			textbox(font_medium, "01:", GOLD, [60,140])
			textbox(font_medium, database['name'][0], GOLD, [110,140])
			textbox(font_medium, str(database['score'][0]), GOLD, [310,140])
		if len(database) >=2:
			textbox(font_medium, "02:", GREY, [58,170])
			textbox(font_medium, database['name'][1], GREY, [110,170])
			textbox(font_medium, str(database['score'][1]), GREY, [310,170])
		if len(database) >= 3:
			textbox(font_medium, "03:", BRONZE, [58,200])
			textbox(font_medium, database['name'][2], BRONZE, [110,200])
			textbox(font_medium, str(database['score'][2]), BRONZE, [310,200])
		if len(database) >= 4:
			textbox(font_medium, "04:", WHITE, [59,230])
			textbox(font_medium, database['name'][3], WHITE, [110,230])
			textbox(font_medium, str(database['score'][3]), WHITE, [310,230])
		if len(database) >= 5:
			textbox(font_medium, "05:", WHITE, [57,260])
			textbox(font_medium, database['name'][4], WHITE, [110,260])
			textbox(font_medium, str(database['score'][4]), WHITE, [310,260])

		if snake.length-1 > highscore:
			textbox(font_big, "NEW HIGHSCORE!", RED, (50,25))
		else:
			textbox(font_big, "You have lost!", RED, (80,25))

		textbox(font_medium, f"Your Score is {snake.length-1}", RED, (110,60))
		pygame.display.update()


pygame.quit()
quit()