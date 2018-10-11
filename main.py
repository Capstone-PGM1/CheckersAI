import pygame

# the empty shell is copied from https://nerdparadise.com/programming/pygame/part1
pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()