'''Sans Fight'''
__version__="April 17 2025"
__author__ = "Ryan Xue"


import pygame, random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (169, 0, 0)
YELLOW = (255, 255, 0)

# Dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
state = 'dialogue'

class Soul(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.soulmode = 'RED'
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.rect = pygame.Rect(SCREEN_WIDTH/2-8, SCREEN_HEIGHT/3*2, 16, 16)
        self.redimg = pygame.image.load('Red.png').convert_alpha()
        self.image = self.redimg
        self.transparent_img = pygame.Surface([16,16], pygame.SRCALPHA)
        self.transparent_img.fill((0, 0, 0, 0))
    def update(self):
        if state == 'histurn':
            if self.soulmode == 'RED':
                self.image = self.redimg
                if not self.down == self.up:
                    if self.down:
                        self.rect.y += 5
                    else:
                        self.rect.y -= 5
                if not self.right == self.left:
                    if self.right:
                        self.rect.x += 5
                    else:
                        self.rect.x -= 5

            elif self.soulmode == 'BLUEDOWN':
                self.soulmode = 'RED'
        else:
            self.image = self.transparent_img


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("UNDERTALE")
    soul = Soul()
    clock = pygame.time.Clock()
    done = False
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(soul)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if state == 'yourturn':
                screen.fill(BLACK)
            elif state == 'histurn':
                if soul.soulmode == 'RED':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            soul.up = True
                        elif event.key == pygame.K_DOWN:
                            soul.down = True
                        elif event.key == pygame.K_LEFT:
                            soul.left = True
                        elif event.key == pygame.K_RIGHT:
                            soul.right = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            soul.up = False
                        elif event.key == pygame.K_DOWN:
                            soul.down = False
                        elif event.key == pygame.K_LEFT:
                            soul.left = False
                        elif event.key == pygame.K_RIGHT:
                            soul.right = False
            elif state == 'dialogue':
                screen.fill(BLACK)
        screen.fill(BLACK)
        active_sprite_list.draw(screen)
        active_sprite_list.update()
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()