import pygame

pygame.init()
dis = pygame.display.set_mode((400,300))
pygame.display.update()
pygame.display.set_caption("Edbert Ekaputera's Snake Game")
game_over = False
while game_over == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_over = True

pygame.quit()
quit()