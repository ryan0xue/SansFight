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
state = 'histurn'

class Soul(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.soulmode = 'BLUE'
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.direction = 1
        self.health = 92
        self.karma = 0
        self.rect = pygame.Rect(SCREEN_WIDTH/2-8, SCREEN_HEIGHT/3*2, 16, 16)
        self.redimg = pygame.image.load('Red.png').convert_alpha()
        self.blueimg = pygame.image.load('Blue.png').convert_alpha()
        self.image = self.redimg
        self.transparent_img = pygame.Surface([16,16], pygame.SRCALPHA)
        self.transparent_img.fill((0, 0, 0, 0))
        self.accel = 0
        self.velocity = 0
    def update(self, battle_box):
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

            elif self.soulmode == 'BLUE':
                self.image = self.blueimg
                if not self.right == self.left:
                    if self.right:
                        self.rect.x += 5
                    else:
                        self.rect.x -= 5
                if self.up:
                    self.accel = 0
                    self.velocity = -6
                else:
                    if self.velocity <= -1:
                        self.accel = 0.5
                        self.velocity = -1
                    elif self.velocity <= 0.5:
                        self.accel = 0.2
                    elif self.velocity <= 8:
                        self.accel = 0.6
                    else:
                        self.accel = 0
                self.velocity += self.accel
                self.rect.y += self.velocity

            if self.direction == 1:
                self.image = rotate_center(self.image, 0)
            elif self.direction == 2:
                self.image = rotate_center(self.image, 90)
            elif self.direction == 3:
                self.image = rotate_center(self.image, 180)
            elif self.direction == 4:
                self.image = rotate_center(self.image, 270)
            #detect battle box
            if self.rect.left < battle_box.rect.left + 5:
                self.rect.left = battle_box.rect.left + 5
            if self.rect.right > battle_box.rect.right - 5:
                self.rect.right = battle_box.rect.right - 5
            if self.rect.top < battle_box.rect.top + 5:
                self.rect.top = battle_box.rect.top + 5
            if self.rect.bottom > battle_box.rect.bottom - 5:
                self.rect.bottom = battle_box.rect.bottom - 5
                if self.soulmode == 'BLUE':
                    self.velocity = 0
        else:
            self.image = self.transparent_img

class BattleBox(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((SCREEN_WIDTH-width)/2, SCREEN_HEIGHT/2+150-height, width, height)
        self.target_rect = None
        self.speed = 25
        self.animating = False

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 5)
    def resize(self, new_width, new_height):
        self.target_rect = pygame.Rect((SCREEN_WIDTH-new_width)/2, SCREEN_HEIGHT/2+150-new_height, new_width, new_height)
        self.animating = True
    def update(self):
        if self.target_rect and self.animating:
            # Width
            if self.rect.width < self.target_rect.width:
                self.rect.width += min(self.speed, self.target_rect.width - self.rect.width)
            elif self.rect.width > self.target_rect.width:
                self.rect.width -= min(self.speed, self.rect.width - self.target_rect.width)

            # Height
            if self.rect.height < self.target_rect.height:
                self.rect.height += min(self.speed, self.target_rect.height - self.rect.height)
            elif self.rect.height > self.target_rect.height:
                self.rect.height -= min(self.speed, self.rect.height - self.target_rect.height)
            self.rect.x = (SCREEN_WIDTH - self.rect.width) / 2
            self.rect.y = SCREEN_HEIGHT / 2 + 150 - self.rect.height

            # Check if animation is complete
            if (self.rect.x == self.target_rect.x and
                    self.rect.y == self.target_rect.y and
                    self.rect.width == self.target_rect.width and
                    self.rect.height == self.target_rect.height):
                self.animating = False
def rotate_center(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image
def load_font(font_path, size):
    font = pygame.font.Font(font_path, size)
    return font
def draw_text(screen, text, font, color, x, y):
    """Draw text on the screen with the specified alignment."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
    return text_rect
def main():
    global state
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    info_font = load_font('Mars.ttf', 24)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("UNDERTALE")
    soul = Soul()
    clock = pygame.time.Clock()
    done = False
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(soul)
    battle_box = BattleBox(200, 200)
    soul.rect.center = battle_box.rect.center
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if state == 'yourturn':
                battle_box.resize(575, 140)
                screen.fill(BLACK)
            elif state == 'histurn':
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
                battle_box.resize(200, 200)
            if event.type == pygame.KEYDOWN: #temprary
                if event.key == pygame.K_1:
                    soul.direction = 1
                elif event.key == pygame.K_2:
                    soul.direction = 2
                elif event.key == pygame.K_3:
                    soul.direction = 3
                elif event.key == pygame.K_4:
                    soul.direction = 4
                elif event.key == pygame.K_5:
                    soul.soulmode = 'BLUE'
                elif event.key == pygame.K_6:
                    soul.soulmode = 'RED'
                elif event.key == pygame.K_7:
                    if state == 'histurn':
                        state = 'yourturn'
                    else:
                        state = 'histurn'

        screen.fill(BLACK)
        battle_box.update()
        active_sprite_list.update(battle_box)
        battle_box.draw(screen)
        active_sprite_list.draw(screen)
        
        draw_text(screen, "CHARA", info_font, WHITE, 32, 400)
        draw_text(screen, "LV 19", info_font, WHITE, 135, 400)


        clock.tick(30)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()