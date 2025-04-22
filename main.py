'''Sans Fight'''
__version__="April 17 2025"
__author__ = "Ryan Xue"


import pygame, random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (169, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0 ,255)
# Dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
state = 'histurn'

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
pygame.font.init()
#Files
SLAM = pygame.mixer.Sound('Sound/Slam.ogg')
MEGALOVANIA = pygame.mixer.Sound('Sound/MEGALOVANIA.ogg')
MEGALOVANIA.set_volume(0.6)
TEXT = pygame.mixer.Sound('Sound/BattleText.ogg')
DING = pygame.mixer.Sound('Sound/Ding.ogg')

class Health(pygame.sprite.Sprite):
    def __init__(self, health, karma):
        pygame.sprite.Sprite.__init__(self)
        for i in range(92):
            if


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
        self.redimg = pygame.image.load('Images/Red.png').convert_alpha()
        self.blueimg = pygame.image.load('Images/Blue.png').convert_alpha()
        self.image = self.redimg
        self.transparent_img = pygame.Surface([16,16], pygame.SRCALPHA)
        self.transparent_img.fill((0, 0, 0, 0))
        self.accel = 0
        self.velocity = 0
        self.height = 0
        self.olddirection = self.direction
        self.shake = 0
        self.impacting = False
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
                if (self.direction == 1 or self.direction == 3) and not self.right == self.left:
                    if self.right:
                        self.rect.x += 5
                    else:
                        self.rect.x -= 5
                if (self.direction == 2 or self.direction == 4) and not self.up == self.down:
                    if self.down:
                        self.rect.y += 5
                    else:
                        self.rect.y -= 5

                if ((self.up and self.direction == 1) or (self.left and self.direction == 2) or (self.down and self.direction == 3) or (self.right and self.direction == 4)) and self.height <= 10:
                        self.accel = 0
                        self.velocity = -6
                        self.height += 1

                else:
                    self.height = 100000
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
                if self.direction == 1:
                    self.rect.y += self.velocity
                elif self.direction == 2:
                    self.rect.x += self.velocity
                elif self.direction == 3:
                    self.rect.y -= self.velocity
                elif self.direction == 4:
                    self.rect.x -= self.velocity

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
                if self.direction == 4:
                    self.velocity = 0
            if self.rect.right > battle_box.rect.right - 5:
                self.rect.right = battle_box.rect.right - 5
                if self.direction == 2:
                    self.velocity = 0
            if self.rect.top < battle_box.rect.top + 5:
                self.rect.top = battle_box.rect.top + 5
                if self.direction == 3:
                    self.velocity = 0
            if self.rect.bottom > battle_box.rect.bottom - 5:
                self.rect.bottom = battle_box.rect.bottom - 5
                if self.direction == 1:
                    self.velocity = 0

            if not self.olddirection == self.direction:
                self.olddirection = self.direction
                self.velocity = 20
                self.height = 100000
                self.impacting = True
            if self.shake >= 1:
                self.impacting = False
                if self.shake == 1:
                    pygame.mixer.Sound.play(SLAM)
                    self.height = 0
                if self.shake == 5:
                    self.shake = -1
                self.shake += 1
            if self.velocity == 0:
                self.height = 0
                if self.impacting:
                    self.shake = 1
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
            self.rect.y = SCREEN_HEIGHT / 2 + 127 - self.rect.height

            # Check if animation is complete
            if (self.rect.x == self.target_rect.x and
                    self.rect.y == self.target_rect.y and
                    self.rect.width == self.target_rect.width and
                    self.rect.height == self.target_rect.height):
                self.animating = False


class DialogBox:
    def __init__(self, font, width, height, x, y):
        self.font = font
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.display_text = ""
        self.text_index = 0
        self.text_speed = 1
        self.active = False
        self.completed = False
        self.sound_channel = pygame.mixer.Channel(1)
    def set_text(self, text):
        self.text = text
        self.display_text = ""
        self.text_index = 0
        self.active = True
        self.completed = False

    def update(self):
        if not self.active:
            return

        if self.text_index < len(self.text):
            self.display_text += self.text[self.text_index]
            if not self.text[self.text_index].isspace():
                    self.sound_channel.stop()
                    self.sound_channel.play(TEXT)
            while self.text[self.text_index].isspace():
                self.text_index += 1
                self.display_text += self.text[self.text_index]
            self.text_index += 1
        else:
            self.completed = True

    def draw(self, screen):
        if not self.active:
            return
        words = self.display_text.split(' ')
        x, y = self.rect.x + 10, self.rect.y + 10
        line_height = self.font.get_height()
        max_width = self.rect.width - 20

        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            test_width = self.font.size(test_line)[0]

            if test_width > max_width:
                draw_text(screen, current_line, self.font, WHITE, x, y, True)
                y += line_height
                current_line = word + " "
            else:
                current_line = test_line

        draw_text(screen, current_line, self.font, WHITE, x, y, True)

def rotate_center(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image
def load_font(font_path, size):
    font = pygame.font.Font(font_path, size)
    return font
info_font = load_font('Mars.ttf', 24)
HPKR_font = load_font('8-BIT WONDER.TTF', 12)
sans_font = load_font('pixel-comic-sans-undertale-sans-font.ttf', 12)
determination_mono = load_font('DeterminationMonoWebRegular-Z5oq.ttf', 30)
def draw_text(screen, text, font, color, x, y, instant=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
def screenshake(intensity):
    if intensity == 0:
        return (0, 0)
    else:
        x = random.randint(-intensity, intensity)
        y = random.randint(-intensity, intensity)
        return (x, y)
def main():
    global state
    truescreen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("UNDERTALE")
    soul = Soul()
    clock = pygame.time.Clock()
    done = False
    turnno = 0
    health = Health(soul.health, soul.karma)
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(soul)
    battle_box = BattleBox(200, 200)
    soul.rect.center = battle_box.rect.center
    dialog_box = DialogBox(determination_mono, 545, 132, 57, 245)
    oldstate = state
    timer = 0
    lines = []
    with open('dialogue.txt') as file:
        for line in file:
            lines.append(line.rstrip())
    while not done:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if state == 'yourturn':
                """controls"""
            if state == 'histurn':
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
                    DING.play()
                elif event.key == pygame.K_6:
                    soul.soulmode = 'RED'
                    DING.play()
                elif event.key == pygame.K_7:
                    if state == 'histurn':
                        state = 'yourturn'
                        timer = 0
                    else:
                        state = 'histurn'
        if state == 'yourturn':
            battle_box.resize(545, 132)
            if timer == 20:
                if turnno == 1:
                    dialog_box.set_text(lines[0])
                elif turnno == 4:
                    dialog_box.set_text(lines[2])
                elif turnno == 9:
                    dialog_box.set_text(lines[3])
                elif turnno == 12:
                    dialog_box.set_text(lines[4])
                elif turnno == 22:
                    dialog_box.set_text(lines[9])
                elif turnno == 23:
                    dialog_box.set_text(lines[10])
                elif 30 <= soul.karma < 40:
                    dialog_box.set_text(lines[14])
                elif 20 <= soul.karma < 30:
                    dialog_box.set_text(lines[13])
                elif 10 <= soul.karma < 20:
                    dialog_box.set_text(lines[12])
                elif 0 < soul.karma < 10:
                    dialog_box.set_text(lines[11])
                elif turnno < 12:
                    dialog_box.set_text(lines[1])
                else:
                    dialog_box.set_text(lines[random.randint(5, 8)])
            elif timer > 20:  # After setting text, update and draw it
                dialog_box.update()
                dialog_box.draw(screen)
            timer += 1
        elif state == 'histurn':
            battle_box.resize(200, 200)
        battle_box.update()
        active_sprite_list.update(battle_box)
        battle_box.draw(screen)
        active_sprite_list.draw(screen)
        #healthbar.draw(screen)
        
        draw_text(screen, "CHARA", info_font, WHITE, 47.5, 375, True)
        draw_text(screen, "LV 19", info_font, WHITE, 145, 375, True)
        draw_text(screen, "HP", HPKR_font, WHITE, 230, 378, True)
        draw_text(screen, "KR", HPKR_font, WHITE, 370, 378, True)
        if soul.karma > 0:
            draw_text(screen, str(soul.health)+" / 92", info_font, MAGENTA, 410, 375, True)
        else:
            draw_text(screen, str(soul.health) + " / 92", info_font, WHITE, 410, 375, True)
        if not oldstate == state:
            oldstate = state
            if state == 'yourturn':
                turnno += 1 #only if attack add later
                if turnno == 1:
                    MEGALOVANIA.play(-1)
                elif turnno == 13:
                    MEGALOVANIA.pause()
        health.update(soul.health, soul.karma)
        health.draw(screen)
        truescreen.blit(screen, screenshake(soul.shake))
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()