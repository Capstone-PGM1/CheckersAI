import pygame

pygame.init()

class Tiles:
	# tile size
	Size = 80
	# function for scaling tiles
	def Load_Texture(file, Size):
		bitmap = pygame.image.load(file)
		bitmap = pygame.transform.scale(bitmap, (Size, Size))
		surface = pygame.Surface((Size, Size), pygame.HWSURFACE|pygame.SRCALPHA)
		surface.blit(bitmap, (0, 0))
		return surface

	# https://opengameart.org/content/fabric-grey
	greyTile = Load_Texture("grey.png", Size)
	# https://opengameart.org/content/4k-seamless-white-marble-stone-textures-public-domain
	whiteTile = Load_Texture("white.jpg", Size)
	# https://opengameart.org/content/seamless-pattern-fabric-textile
	tanTile = Load_Texture("tan.png", Size)
	# https://opengameart.org/content/leather-black
	blackTile = Load_Texture("black.png", 20)
