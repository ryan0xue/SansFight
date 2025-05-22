'''Sans Fight'''
__version__ = "April 17 2025"
__author__ = "Ryan Xue"

import pygame, random, math

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FAKEWHITE = (253, 253, 253)
RED = (210, 0, 0)
YELLOW = (255, 252, 4)
MAGENTA = (255, 0, 255)
BLUE = (0, 162, 232)
GREEN = (45, 95, 45)
# Dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
state = 'talk'

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
pygame.font.init()
#Files
SLAM = pygame.mixer.Sound('Sound/Slam.ogg')
MEGALOVANIA = pygame.mixer.Sound('Sound/MEGALOVANIA.ogg')
CHOICE = pygame.mixer.Sound('Sound/The_Choice.ogg')
TEXT = pygame.mixer.Sound('Sound/BattleText.ogg')
SANSTEXT = pygame.mixer.Sound('Sound/snd_txtsans.wav')
DING = pygame.mixer.Sound('Sound/Ding.ogg')
HURT = pygame.mixer.Sound('Sound/PlayerDamaged.ogg')
CURSOR = pygame.mixer.Sound('Sound/MenuCursor.ogg')
SELECT = pygame.mixer.Sound('Sound/MenuSelect.ogg')
SLASH = pygame.mixer.Sound('Sound/snd_laz.wav')
BIRDS = pygame.mixer.Sound('Sound/mus_birdnoise.ogg')
BONESTAB = pygame.mixer.Sound('Sound/BoneStab.ogg')
ALERT = pygame.mixer.Sound('Sound/Warning.ogg')


def collide(soul_rect, target_surface, color):
    # Quick rect check first
    if not soul_rect.colliderect(pygame.Rect(0, 0, 640, 480)):
        return False

    # Create a mask for efficient collision
    surface_mask = pygame.mask.from_threshold(
        target_surface,
        color,  # Color to detect
        (1, 1, 1, 255)  # Threshold for color matching
    )

    # Create a mask for the soul
    soul_mask = pygame.mask.Mask((10, 10))
    soul_mask.fill()

    # Check for overlap
    return surface_mask.overlap(soul_mask, (soul_rect.x+3, soul_rect.y+3)) is not None
def rotate_center(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image
def load_font(font_path, size):
    font = pygame.font.Font(font_path, size)
    return font
def draw_text(screen, text, font, color, x, y):
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
def rotatecenter(img, angle):
    newimg = pygame.transform.rotate(img, angle)
    old_rect = img.get_rect()
    new_rect = newimg.get_rect()
    new_rect.center = old_rect.center
    return old_rect
def calculate_movement(angle, speed):
    radians = math.radians(angle)
    dx = speed * math.sin(radians)
    dy = speed * math.cos(radians)

    return dx, dy
info_font = load_font('Fonts/Mars.ttf', 24)
HPKR_font = load_font('Fonts/8-BIT WONDER.TTF', 12)
sans_font = load_font('Fonts/pixel-comic-sans-undertale-sans-font.ttf', 16)
determination_mono = load_font('Fonts/DeterminationMonoWebRegular-Z5oq.ttf', 32)
damage_font = load_font('Fonts/hachicro.TTF', 32)
class Options:
    def __init__(self):
        self.sequence = ['flavortext']
        self.text = None
        self.oldtext = '*'
        self.instant = False
        self.soulpos = 0
        self.skip = False
    def update(self, dialog_box, flavortext):
        self.instant = True
        if len(self.sequence) == 1:
            self.text = flavortext
            self.instant = False
        elif len(self.sequence) == 2:
            if self.sequence[1] == 'sans':
                self.text = '   * Sans'
            elif self.sequence[1] == 'spare':
                self.text = '   * Spare'
            elif self.sequence[1] == 'food':
                self.text = '* You ate the Butterscotch Pie.   * Your HP was maxed out.'
                self.instant = False
        elif len(self.sequence) == 3:
            if self.sequence[2] == 'check':
                self.text = '   * Check'
        elif len(self.sequence) == 4:
            if self.sequence[3] == 'check1':
                self.text = '* Sans 1 ATK 1 DEF                * The easiest enemy.              * Can only deal 1 damage.'
                self.instant = False
        elif len(self.sequence) == 5:
            if self.sequence[4] == 'check2':
                self.text = '* Can\'t keep dodging forever.       Keep attacking.'
                self.instant = False
        if self.skip:
            self.instant = True
        if not self.oldtext == self.text or self.instant:
            if not self.text == flavortext:
                if self.instant and not self.skip:
                    self.soulpos = 1
                else:
                    self.soulpos = 2
            else:
                self.soulpos = 0
            dialog_box.set_text(self.text, self.instant)
            self.oldtext = self.text
        self.skip = False
    def z(self, choice, completed):
        if completed:
            if len(self.sequence) == 1:
                if choice == 1 or choice == 2:
                    self.sequence.append('sans')
                elif choice == 4:
                    self.sequence.append('spare')
                else:
                    self.sequence.append('food')
            elif len(self.sequence) == 2:
                if choice == 2:
                    self.sequence.append('check')
                else:
                    self.sequence.append('done')
            elif len(self.sequence) == 3:
                if choice == 2:
                    self.sequence.append('check1')
            elif len(self.sequence) == 4:
                if choice == 2:
                    self.sequence.append('check2')
            elif len(self.sequence) == 5:
                if choice == 2:
                    self.sequence.append('done')
            SELECT.play()

    def x(self):
        if not (len(self.sequence) == 1 or (
                len(self.sequence) >= 4 and 'check1' in self.sequence) or 'food' in self.sequence or 'done' in self.sequence):
            self.sequence.pop()
            SELECT.play()
        else:
            self.skip = True
class Buttons(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.choice = 1
        self.x = 35
        self.y = 430
        self.fight = pygame.image.load('Images/fight.png').convert_alpha()
        self.act = pygame.image.load('Images/act.png').convert_alpha()
        self.item = pygame.image.load('Images/item.png').convert_alpha()
        self.mercy = pygame.image.load('Images/mercy.png').convert_alpha()
        self.sfight = pygame.image.load('Images/sfight.png').convert_alpha()
        self.sact = pygame.image.load('Images/sact.png').convert_alpha()
        self.sitem = pygame.image.load('Images/sitem.png').convert_alpha()
        self.smercy = pygame.image.load('Images/smercy.png').convert_alpha()
        self.images = [self.fight, self.act, self.item, self.mercy]
        self.image = None

    def update(self, choosing):
        if self.choice == 5:
            self.choice = 1
        elif self.choice == 0:
            self.choice = 4
        if choosing:
            if self.choice == 1:
                self.images = [self.sfight, self.act, self.item, self.mercy]
            elif self.choice == 2:
                self.images = [self.fight, self.sact, self.item, self.mercy]
            elif self.choice == 3:
                self.images = [self.fight, self.act, self.sitem, self.mercy]
            elif self.choice == 4:
                self.images = [self.fight, self.act, self.item, self.smercy]
        else:
            self.images = [self.fight, self.act, self.item, self.mercy]

    def draw(self, screen):
        self.x = 35
        self.y = 430
        for i in self.images:
            screen.blit(i, (self.x, self.y))
            self.x += 155
class Bar(pygame.sprite.Sprite):
    def __init__(self, color, length):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.Surface([math.ceil(110 * length / 92), 21])
        except:
            self.image = pygame.Surface([1, 21])
        self.image.fill(color)
        self.rect = pygame.draw.rect(self.image, color, self.image.get_rect())
class Health(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 92
        self.karma = 0
        self.empty = 0
        self.x = 255
        self.y = 400
        self.barlist = pygame.sprite.Group()

    def update(self, health, karma):
        self.health = health
        self.karma = karma
        if health + karma > 0:
            self.empty = 92 - health - karma
        else:
            self.empty = 92

    def draw(self, screen):
        # health bar is 110x21
        self.x = 255
        self.y = 400
        bar = Bar(YELLOW, self.health)
        bar.rect.x = self.x
        self.x += math.ceil(self.health * 110 / 92)
        bar.rect.y = self.y
        screen.blit(bar.image, bar.rect)

        bar = Bar(MAGENTA, self.karma)
        bar.rect.x = self.x
        self.x += math.ceil(self.karma * 110 / 92)
        bar.rect.y = self.y
        screen.blit(bar.image, bar.rect)

        bar = Bar(RED, self.empty)
        bar.rect.x = self.x
        bar.rect.y = self.y
        screen.blit(bar.image, bar.rect)

        bar = Bar(BLACK, 5)
        self.x = 365
        bar.rect.x = self.x
        bar.rect.y = self.y
        screen.blit(bar.image, bar.rect)
class Soul(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.soulmode = 'BLUE'
        self.godmode = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.gameover = False
        self.direction = 1
        self.karma = 0
        self.healthyhealth = 92
        self.health = self.healthyhealth + self.karma
        self.rect = pygame.Rect(SCREEN_WIDTH / 2 - 8, SCREEN_HEIGHT, 16, 16)
        self.redimg = pygame.image.load('Images/Red.png').convert_alpha()
        self.blueimg = pygame.image.load('Images/Blue.png').convert_alpha()
        self.image = self.redimg
        self.transparent_img = pygame.Surface([16, 16], pygame.SRCALPHA)
        self.transparent_img.fill((0, 0, 0, 0))
        self.accel = 0
        self.velocity = 0
        self.slam = False
        self.height = 0
        self.shake = 0
        self.impacting = False
        self.hurting = False
        self.karmaframes = 0
        self.moving = False
    def update(self, battle_box, screen, attacklist):
        self.moving = False
        if state == 'histurn':
            if self.soulmode == 'RED':
                self.image = self.redimg
                self.direction = 1
                self.height = 0
                self.impacting = False
                if not self.down == self.up:
                    if self.down:
                        self.rect.y += 5
                        self.moving = True
                    else:
                        self.rect.y -= 5
                        self.moving = True
                if not self.right == self.left:
                    if self.right:
                        self.rect.x += 5
                        self.moving = True
                    else:
                        self.rect.x -= 5
                        self.moving = True
            elif self.soulmode == 'BLUE':
                self.image = self.blueimg
                if (self.direction == 1 or self.direction == 3) and not self.right == self.left:
                    if self.right:
                        self.rect.x += 5
                        self.moving = True
                    else:
                        self.rect.x -= 5
                        self.moving = True
                if (self.direction == 2 or self.direction == 4) and not self.up == self.down:
                    if self.down:
                        self.rect.y += 5
                        self.moving = True
                    else:
                        self.rect.y -= 5
                        self.moving = True
                if ((self.up and self.direction == 1) or (self.left and self.direction == 2) or (
                        self.down and self.direction == 3) or (
                            self.right and self.direction == 4)) and self.height <= 10:
                    self.accel = 0
                    self.velocity = -6
                    self.height += 1
                    self.moving = True
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
                for platform in attacklist:
                    if isinstance(platform, Platform):
                        if self.rect.bottom >= platform.whiterect.top and self.rect.bottom <= platform.whiterect.top+10 and self.rect.right > platform.whiterect.left and self.rect.left < platform.whiterect.right:
                            if not self.up:
                                self.rect.bottom = platform.whiterect.top
                                self.velocity = 0
                                self.height = 0
                                self.rect.x += platform.speed
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
            if self.slam:
                self.slam = False
                self.velocity = 20
                self.height = 100000
                self.impacting = True
            if self.shake >= 1:
                self.impacting = False
                if self.shake == 1:
                    SLAM.play()
                    self.height = 0
                if self.shake == 5:
                    self.shake = -1
                self.shake += 1
            if self.velocity == 0:
                self.height = 0
                if self.impacting:
                    self.shake = 1
            if collide(self.rect, screen, WHITE) or (collide(self.rect, screen, BLUE) and self.moving):
                self.hurting = True
            else:
                self.hurting = False
        else:  #menu choosing
            self.direction = 1
        if not self.godmode:
            if self.karma > 40:
                self.karma = 40
            elif self.karma == 40:
                self.karma -= 1
                self.karmaframes = 0
            elif 30 <= self.karma < 40:
                if self.karmaframes >= 2:
                    self.karma -= 1
                    self.karmaframes = 0
            elif 20 <= self.karma < 30:
                if self.karmaframes >= 5:
                    self.karma -= 1
                    self.karmaframes = 0
            elif 10 <= self.karma < 20:
                if self.karmaframes >= 15:
                    self.karma -= 1
                    self.karmaframes = 0
            elif 1 <= self.karma < 10:
                if self.karmaframes >= 30:
                    self.karma -= 1
                    self.karmaframes = 0
            if self.karma > 0:
                self.karmaframes += 1
            if self.health >= 1:
                if self.hurting:
                    HURT.stop()
                    HURT.play()
                    if self.healthyhealth <= 1:
                        self.karma -= 1
                        self.healthyhealth = 1
                    else:
                        self.karma += 4
                        self.healthyhealth = self.health - self.karma - 1
            self.health = self.healthyhealth + self.karma
            if self.health <= 0:
                self.gameover = True
class BattleBox(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((640 - width) / 2, 390 - height, width, height)
        self.target_rect = None
        self.speed = 25
        self.animating = False

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 5)
    def resize(self, new_width, new_height):
        self.target_rect = pygame.Rect((640 - new_width) / 2, 390 - new_height, new_width, new_height)
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
            self.rect.x = (640 - self.rect.width) / 2
            self.rect.y = 390 - self.rect.height

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
        self.instant = True

    def set_text(self, text, instant):
        self.text = text
        self.display_text = ""
        self.text_index = 0
        self.active = True
        self.completed = False
        self.instant = instant

    def update(self):
        if not self.active:
            return
        if not self.instant:
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
        else:
            self.completed = True
            self.display_text = self.text

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
                draw_text(screen, current_line, self.font, WHITE, x, y)
                y += line_height
                current_line = word + " "
            else:
                current_line = test_line

        draw_text(screen, current_line, self.font, WHITE, x, y)
class SpriteSheet:
    def __init__(self, image, width, height):
        self.sheet = image
        self.width = width
        self.height = height

    def get_image(self, frame):
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), ((frame * self.width), 0, self.width, self.height))
        return image

    def draw(self, screen, frame, x, y):
        screen.blit(self.get_image(frame), (x, y))
class Slashimation:
    def __init__(self):
        self.spritesheet = SpriteSheet(pygame.image.load('Spritesheets/slash.png').convert_alpha(), 26, 110)
        self.frame = 0
        self.maxframe = 6
        self.clock = 0
        self.active = False
        self.completed = False

    def start(self):
        self.active = True
        self.completed = False
        self.frame = -2
        self.clock = 0
        SLASH.play()

    def update(self):
        if not self.active:
            return
        self.clock += 1
        if self.clock > 1:
            self.clock = 0
            self.frame += 1
            if self.frame > self.maxframe:
                self.completed = True
                self.active = False
                self.frame = -2
    def draw(self, screen, x, y):
        if not self.active:
            return
        image = self.spritesheet.get_image(self.frame)
        screen.blit(image, (x, y))
class SansBubble:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect(x, y, 170, 104)
        self.text = ""
        self.display_text = ""
        self.text_index = 0
        self.text_speed = 1
        self.active = False
        self.completed = False
        self.sound_channel = pygame.mixer.Channel(2)
        self.image = pygame.image.load('Images/bubble.png').convert_alpha()

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
                self.sound_channel.play(SANSTEXT)
            while self.text[self.text_index].isspace():
                self.text_index += 1
                self.display_text += self.text[self.text_index]
            self.text_index += 1
        else:
            self.completed = True
            self.display_text = self.text

    def draw(self, screen):
        if not self.active:
            return
        screen.blit(self.image, (self.x, self.y))
        x, y = self.rect.x + 35, self.rect.y + 15
        line_height = sans_font.get_height()
        max_width = self.rect.width
        words = self.display_text.split(' ')
        current_line = ""
        line_y = y
        for word in words:
            test_line = current_line + word + " "
            test_width = sans_font.size(test_line)[0]
            if test_width > max_width:
                draw_text(screen, current_line, sans_font, BLACK, x, line_y)
                line_y += line_height
                current_line = word + " "
            else:
                current_line = test_line
        draw_text(screen, current_line, sans_font, BLACK, x, line_y)
class Sans:
    def __init__(self, battle_box):
        self.colorkey = (195, 134, 255)
        self.legs =  pygame.image.load('Images/Legs.png').convert_alpha()
        self.legs = pygame.transform.scale(self.legs, (88, 46))
        self.legs.set_colorkey(self.colorkey)
        self.torso = pygame.image.load('Images/Torso.png').convert_alpha()
        self.torso = pygame.transform.scale(self.torso, (144, 70))
        self.torso.set_colorkey(self.colorkey)
        self.facesimage = pygame.image.load('Spritesheets/Faces.png').convert_alpha()
        self.facesimage = pygame.transform.scale(self.facesimage, (512, 64))
        self.facesimage.set_colorkey(self.colorkey)
        self.faces = SpriteSheet(self.facesimage, 64, 64)
        self.face = self.faces.get_image(0)
        self.center = SCREEN_WIDTH / 2
        self.y = battle_box.rect.y - 160
        self.xdeviation = 0
        self.ydeviation = 4
        self.ychange = 1
        self.xdirection = 1
        self.headbob = 0.5
        self.change = 0
        self.slash = 0
    def update(self, face):
        self.face = self.faces.get_image(face)
    def draw(self, screen, battle_box):
        self.y = battle_box.rect.y - 160
        if self.change == 0:
            self.change = 1
            if self.ydeviation == 4:
                self.ychange = -1
            elif self.ydeviation == 0:
                self.ychange = 1
            self.ydeviation += self.ychange
            if self.ydeviation == 4: #
                self.xdeviation = 0
            elif self.ydeviation == 2: #
                self.xdeviation = 1
            elif self.ydeviation == 0: #
                self.xdeviation = 2
            if self.xdeviation == 0 and self.ydeviation == 4:
                self.xdirection *= -1
            if self.headbob == 0.5:
                self.headbob = 1
            elif self.headbob == 1:
                self.headbob = 0
            else:
                self.headbob = 0.5
        else:
            self.change -= 1
        screen.blit(self.legs, (self.center - 44 - self.slash, self.y + 100))
        screen.blit(self.torso, (self.center - self.slash - 72 + self.xdeviation*self.xdirection-2, self.y + 53 - self.ydeviation/2))
        screen.blit(self.face, (self.center - self.slash - 32 + self.xdeviation*self.xdirection-2, self.y + 5 - self.ydeviation/2 + self.headbob))
class GasterBlaster:
    def __init__(self, timer, x, y, direction, wait, duration):
        self.x = int(x)
        self.y = int(y)
        self.direction = int(direction)
        self.wait = int(wait)
        self.duration = int(duration)
        self.starttime = timer
        self.gastersheet = pygame.image.load('Spritesheets/gasterblaster.png').convert_alpha()
        self.gastersheet = pygame.transform.scale(self.gastersheet, (516, 114))
        self.gastersheet.set_colorkey((195, 134, 255))
        self.gasterframe = SpriteSheet(self.gastersheet, 86, 114)
        self.chargesound = pygame.mixer.Sound("Sound/mus_sfx_segapower.wav")
        self.blast = pygame.mixer.Sound("Sound/mus_sfx_a_gigatalk.wav")
        self.channel = pygame.mixer.Channel(3)
        if self.direction >= 180:
            self.blastdirection = self.direction - 180
        else:
            self.blastdirection = self.direction
        self.image = self.gasterframe.get_image(0)
        self.chargesound.play()
        self.xchange, self.ychange = calculate_movement(self.direction, 15)
        self.bxchange, self.bychange = calculate_movement(self.blastdirection, 15)
        self.blasting = False
        self.remove = False
        self.framecount = 0
        self.blastimg = pygame.Surface([60, 1500])
        self.bwidth = 60
        self.bwchange = -5
        self.blastimg.fill(WHITE)
        self.blastimg = rotate_center(self.blastimg, self.blastdirection).convert_alpha()
        if 90<self.blastdirection<180:
            self.blastxy = (self.x + 47 - abs(self.bxchange * 50), self.y + 47 - abs(self.bychange * 50))
        else:
            self.blastxy = (self.x + 13 - abs(self.bxchange * 50), self.y + 13 - abs(self.bychange * 50))
        self.ix, self.iy = self.x, self.y
    def update(self, timer):
        if timer-self.starttime > self.wait:
            if self.framecount == 0:
                self.image = self.gasterframe.get_image(5)
                self.framecount = 1
            elif self.framecount == 1:
                self.image = self.gasterframe.get_image(4)
                self.framecount = 0
            self.x -= self.xchange
            self.y -= self.ychange
        elif timer-self.starttime == self.wait:
            self.channel.stop()
            self.channel.play(self.blast)
            self.image = self.gasterframe.get_image(3)
            self.blasting = True
        elif timer-self.starttime > self.wait-5:
            self.image = self.gasterframe.get_image(2)
        elif timer-self.starttime > self.wait-8:
            self.image = self.gasterframe.get_image(1)
        if timer-self.starttime >= self.wait+self.duration:
            self.blasting = False
            self.remove = True
    def draw(self, screen):
        if self.blasting:
            if self.bwidth > 60:
                self.bwchange = -5
            elif self.bwidth < 45:
                self.bwchange = 5
            self.bwidth += self.bwchange
            self.blastimg = pygame.Surface([self.bwidth, 1500])
            self.blastimg.fill(WHITE)
            self.blastimg = rotate_center(self.blastimg, self.blastdirection).convert_alpha()
            if 90 < self.blastdirection < 180:
                self.blastxy = (self.ix + (86 - self.bwidth) / 2 - abs(self.bxchange * 50)+34, self.iy + (86 - self.bwidth) / 2 - abs(self.bychange * 50)+34)
            else:
                self.blastxy = (self.ix + (86 - self.bwidth) / 2 - abs(self.bxchange * 50), self.iy + (86 - self.bwidth) / 2 - abs(self.bychange * 50))
            screen.blit(self.blastimg, self.blastxy)
        screen.blit(rotate_center(self.image, self.direction), (self.x, self.y))
class BigGasterBlaster:
    def __init__(self, timer, x, y, direction, wait, duration):
        self.x = int(x)
        self.y = int(y)
        self.direction = int(direction)
        self.wait = int(wait)
        self.duration = int(duration)
        self.starttime = timer
        self.gastersheet = pygame.image.load('Spritesheets/gasterblaster.png').convert_alpha()
        self.gastersheet = pygame.transform.scale(self.gastersheet, (774, 171))
        self.gastersheet.set_colorkey((195, 134, 255))
        self.gasterframe = SpriteSheet(self.gastersheet, 129, 171)
        self.chargesound = pygame.mixer.Sound("Sound/mus_sfx_segapower.wav")
        self.blast = pygame.mixer.Sound("Sound/mus_sfx_a_gigatalk.wav")
        self.channel = pygame.mixer.Channel(3)
        if self.direction >= 180:
            self.blastdirection = self.direction - 180
        else:
            self.blastdirection = self.direction
        self.image = self.gasterframe.get_image(0)
        self.chargesound.play()
        self.xchange, self.ychange = calculate_movement(self.direction, 15)
        self.bxchange, self.bychange = calculate_movement(self.blastdirection, 15)
        self.blasting = False
        self.remove = False
        self.framecount = 0
        self.blastimg = pygame.Surface([90, 1500])
        self.bwidth = 90
        self.bwchange = -7.5
        self.blastimg.fill(WHITE)
        self.blastimg = rotate_center(self.blastimg, self.blastdirection).convert_alpha()
        if 90<self.blastdirection<180:
            self.blastxy = (self.x + 47 - abs(self.bxchange * 50), self.y + 47 - abs(self.bychange * 50))
        else:
            self.blastxy = (self.x + 13 - abs(self.bxchange * 50), self.y + 13 - abs(self.bychange * 50))
        self.ix, self.iy = self.x, self.y
    def update(self, timer):
        if timer-self.starttime > self.wait:
            if self.framecount == 0:
                self.image = self.gasterframe.get_image(5)
                self.framecount = 1
            elif self.framecount == 1:
                self.image = self.gasterframe.get_image(4)
                self.framecount = 0
            self.x -= self.xchange
            self.y -= self.ychange
        elif timer-self.starttime == self.wait:
            self.channel.stop()
            self.channel.play(self.blast)
            self.image = self.gasterframe.get_image(3)
            self.blasting = True
        elif timer-self.starttime > self.wait-5:
            self.image = self.gasterframe.get_image(2)
        elif timer-self.starttime > self.wait-8:
            self.image = self.gasterframe.get_image(1)
        if timer-self.starttime >= self.wait+self.duration:
            self.blasting = False
            self.remove = True
    def draw(self, screen):
        if self.blasting:
            if self.bwidth > 90:
                self.bwchange = -7.5
            elif self.bwidth < 67.5:
                self.bwchange = 7.5
            self.bwidth += self.bwchange
            self.blastimg = pygame.Surface([self.bwidth, 1500])
            self.blastimg.fill(WHITE)
            self.blastimg = rotate_center(self.blastimg, self.blastdirection).convert_alpha()
            if 90 < self.blastdirection < 180:
                self.blastxy = (self.ix + (129 - self.bwidth) / 2 - abs(self.bxchange * 50)+51, self.iy + (129 - self.bwidth) / 2 - abs(self.bychange * 50)+51)
            else:
                self.blastxy = (self.ix + (129 - self.bwidth) / 2 - abs(self.bxchange * 50), self.iy + (129 - self.bwidth) / 2 - abs(self.bychange * 50))
            screen.blit(self.blastimg, self.blastxy)
        screen.blit(rotate_center(self.image, self.direction), (self.x, self.y))
class SkinnyGasterBlaster:
    def __init__(self, timer, x, y, direction, wait, duration):
        self.x = int(x)
        self.y = int(y)
        self.direction = int(direction)
        self.wait = int(wait)
        self.duration = int(duration)
        self.starttime = timer
        self.gastersheet = pygame.image.load('Spritesheets/gasterblaster.png').convert_alpha()
        self.gastersheet = pygame.transform.scale(self.gastersheet, (258, 114))
        self.gastersheet.set_colorkey((195, 134, 255))
        self.gasterframe = SpriteSheet(self.gastersheet, 43, 114)
        self.chargesound = pygame.mixer.Sound("Sound/mus_sfx_segapower.wav")
        self.blast = pygame.mixer.Sound("Sound/mus_sfx_a_gigatalk.wav")
        self.channel = pygame.mixer.Channel(3)
        if self.direction >= 180:
            self.blastdirection = self.direction - 180
        else:
            self.blastdirection = self.direction
        self.image = self.gasterframe.get_image(0)
        self.chargesound.play()
        self.xchange, self.ychange = calculate_movement(self.direction, 15)
        self.bxchange, self.bychange = calculate_movement(self.blastdirection, 15)
        self.blasting = False
        self.remove = False
        self.framecount = 0
        self.blastimg = pygame.Surface([30, 1500])
        self.bwidth = 30
        self.bwchange = -2.5
        self.blastimg.fill(WHITE)
        self.blastimg = rotate_center(self.blastimg, self.blastdirection).convert_alpha()
        if 90<self.blastdirection<180:
            self.blastxy = (self.x + 47 - abs(self.bxchange * 50), self.y + 47 - abs(self.bychange * 50))
        else:
            self.blastxy = (self.x + 13 - abs(self.bxchange * 50), self.y + 13 - abs(self.bychange * 50))
        self.ix, self.iy = self.x, self.y
    def update(self, timer):
        if timer-self.starttime > self.wait:
            if self.framecount == 0:
                self.image = self.gasterframe.get_image(5)
                self.framecount = 1
            elif self.framecount == 1:
                self.image = self.gasterframe.get_image(4)
                self.framecount = 0
            self.x -= self.xchange
            self.y -= self.ychange
        elif timer-self.starttime == self.wait:
            self.channel.stop()
            self.channel.play(self.blast)
            self.image = self.gasterframe.get_image(3)
            self.blasting = True
        elif timer-self.starttime > self.wait-5:
            self.image = self.gasterframe.get_image(2)
        elif timer-self.starttime > self.wait-8:
            self.image = self.gasterframe.get_image(1)
        if timer-self.starttime >= self.wait+self.duration:
            self.blasting = False
            self.remove = True
    def draw(self, screen):
        if self.blasting:
            if self.bwidth > 30:
                self.bwchange = -2.5
            elif self.bwidth < 22.5:
                self.bwchange = 2.5
            self.bwidth += self.bwchange
            self.blastimg = pygame.Surface([self.bwidth, 1500])
            self.blastimg.fill(WHITE)
            self.blastimg = rotate_center(self.blastimg, self.blastdirection).convert_alpha()
            if 90 < self.blastdirection < 180:
                self.blastxy = (self.ix + (43 - self.bwidth) / 2 - abs(self.bxchange * 50)+17, self.iy + (43 - self.bwidth) / 2 - abs(self.bychange * 50)+17)
            else:
                self.blastxy = (self.ix + (43 - self.bwidth) / 2 - abs(self.bxchange * 50), self.iy + (43 - self.bwidth) / 2 - abs(self.bychange * 50))
            screen.blit(self.blastimg, self.blastxy)
        screen.blit(rotate_center(self.image, self.direction), (self.x, self.y))
class Bone:
    def __init__(self, timer, x, y, angle, length, speed, direction, lifespan):
        self.x = int(x)
        self.y = int(y)
        angle = int(angle)
        length = int(length)
        self.speed = int(speed)
        self.direction = int(direction)
        self.starttime = timer
        self.lifespan = int(lifespan)
        self.remove = False
        self.colorkey = (195, 134, 255)
        if angle == 0:
            self.topbone = pygame.image.load('Images/topbone.png').convert_alpha()
            self.bottombone = pygame.image.load('Images/bottombone.png').convert_alpha()
            self.centerbone = pygame.image.load('Images/centerbone.png').convert_alpha()
            self.topbone.set_colorkey(self.colorkey)
            self.bottombone.set_colorkey(self.colorkey)
            self.centerbone.set_colorkey(self.colorkey)
            self.bone = pygame.Surface([10, length], pygame.SRCALPHA)
            self.bone.blit(self.topbone, (0, 0))
            self.bone.blit(self.bottombone, (0, length-6))
            for i in range(length-12):
                self.bone.blit(self.centerbone, (0, 6+i))
        elif angle == 1:
            self.topbone = pygame.image.load('Images/leftbone.png').convert_alpha()
            self.bottombone = pygame.image.load('Images/rightbone.png').convert_alpha()
            self.centerbone = pygame.image.load('Images/middlebone2.png').convert_alpha()
            self.topbone.set_colorkey(self.colorkey)
            self.bottombone.set_colorkey(self.colorkey)
            self.centerbone.set_colorkey(self.colorkey)
            self.bone = pygame.Surface([length, 10], pygame.SRCALPHA)
            self.bone.blit(self.topbone, (0, 0))
            self.bone.blit(self.bottombone, (length-6, 0))
            for i in range(length-12):
                self.bone.blit(self.centerbone, (6+i, 0))
    def update(self, timer):
        if self.direction == 1:
            self.x += self.speed
        elif self.direction == 2:
            self.y += self.speed
        elif self.direction == 3:
            self.x -= self.speed
        elif self.direction == 4:
            self.y -= self.speed
        if timer-self.starttime > self.lifespan:
            self.remove = True
    def draw(self, screen):
        screen.blit(self.bone, (self.x, self.y))
class BlueBone:
    def __init__(self, timer, x, y, angle, length, speed, direction, lifespan):
        self.x = int(x)
        self.y = int(y)
        self.speed = int(speed)
        self.direction = int(direction)
        self.starttime = timer
        self.lifespan = int(lifespan)
        angle = int(angle)
        length = int(length)
        self.remove = False
        self.colorkey = (195, 134, 255)
        if angle == 0:
            self.topbone = pygame.image.load('Images/bluetopbone.png').convert_alpha()
            self.bottombone = pygame.image.load('Images/bluebottombone.png').convert_alpha()
            self.centerbone = pygame.image.load('Images/bluecenterbone.png').convert_alpha()
            self.topbone.set_colorkey(self.colorkey)
            self.bottombone.set_colorkey(self.colorkey)
            self.centerbone.set_colorkey(self.colorkey)
            self.bone = pygame.Surface([10, length], pygame.SRCALPHA)
            self.bone.blit(self.topbone, (0, 0))
            self.bone.blit(self.bottombone, (0, length-6))
            for i in range(length-12):
                self.bone.blit(self.centerbone, (0, 6+i))
        elif angle == 1:
            self.topbone = pygame.image.load('Images/blueleftbone.png').convert_alpha()
            self.bottombone = pygame.image.load('Images/bluerightbone.png').convert_alpha()
            self.centerbone = pygame.image.load('Images/bluemiddlebone2.png').convert_alpha()
            self.topbone.set_colorkey(self.colorkey)
            self.bottombone.set_colorkey(self.colorkey)
            self.centerbone.set_colorkey(self.colorkey)
            self.bone = pygame.Surface([length, 10], pygame.SRCALPHA)
            self.bone.blit(self.topbone, (0, 0))
            self.bone.blit(self.bottombone, (length-6, 0))
            for i in range(length-12):
                self.bone.blit(self.centerbone, (6+i, 0))
    def update(self, timer):
        if self.direction == 1:
            self.x += self.speed
        elif self.direction == 2:
            self.y += self.speed
        elif self.direction == 3:
            self.x -= self.speed
        elif self.direction == 4:
            self.y -= self.speed
        if timer-self.starttime > self.lifespan:
            self.remove = True
    def draw(self, screen):
        screen.blit(self.bone, (self.x, self.y))
class BoneStab:
    def __init__(self, timer, battlebox, face, maxheight, warntime, stabtime):
        self.colorkey = (195, 134, 255)
        self.maxheight = int(maxheight)
        self.warntime = int(warntime)
        self.remove = False
        self.warninging = False
        self.stabbing = False
        self.stabtime = int(stabtime)
        self.starttime = timer
        self.boneheight = 0
        self.face = face
        self.bbrh = battlebox.rect.height
        self.bbrw = battlebox.rect.width
        if face == "up" or face == "down":
            self.topbone = pygame.image.load('Images/topbone.png').convert_alpha()
            self.bottombone = pygame.image.load('Images/bottombone.png').convert_alpha()
            self.centerbone = pygame.image.load('Images/centerbone.png').convert_alpha()
            self.topbone.set_colorkey(self.colorkey)
            self.bottombone.set_colorkey(self.colorkey)
            self.centerbone.set_colorkey(self.colorkey)
            self.width = battlebox.rect.width
            self.bones = pygame.Surface([self.width, 12+self.boneheight], pygame.SRCALPHA)
        if face == "left" or face == "right":
            self.topbone = pygame.image.load('Images/leftbone.png').convert_alpha()
            self.bottombone = pygame.image.load('Images/rightbone.png').convert_alpha()
            self.centerbone = pygame.image.load('Images/middlebone2.png').convert_alpha()
            self.topbone.set_colorkey(self.colorkey)
            self.bottombone.set_colorkey(self.colorkey)
            self.centerbone.set_colorkey(self.colorkey)
            self.width = battlebox.rect.height
            self.bones = pygame.Surface([12+self.boneheight, self.width], pygame.SRCALPHA)
        self.bbx, self.bby = battlebox.rect.x, battlebox.rect.y
        if face == "up":
            self.warningrect = pygame.Rect(self.bbx+5, self.bby+5, self.width-10, self.maxheight+12)
        elif face == "down":
            self.warningrect = pygame.Rect(self.bbx+5, self.bby-5+self.bbrh-self.maxheight-12, self.width-10, self.maxheight+12)
        elif face == "left":
            self.warningrect = pygame.Rect(self.bbx+5, self.bby+5, self.maxheight+12, self.width-10)
        elif face == "right":
            self.warningrect = pygame.Rect(self.bbx-5+self.bbrw-self.maxheight-12, self.bby+5, self.maxheight+12, self.width-10)
    def update(self, timer):
        if timer - self.starttime > self.stabtime+self.warntime:
            self.stabbing = False
            self.remove = True
        elif timer - self.starttime == self.warntime:
            BONESTAB.play()
            self.warninging = False
            self.stabbing = True
        elif timer - self.starttime == 0:
            ALERT.play()
            self.warninging = True
        if self.stabbing:
            if self.face == "up" or self.face == "down":
                self.bones = pygame.Surface([self.width, 12 + self.boneheight], pygame.SRCALPHA)
                for bone in range(math.floor(self.width/10)):
                    self.bones.blit(self.topbone, (bone*10, 0))
                    self.bones.blit(self.bottombone, (bone*10, 6+self.boneheight))
                    for i in range(self.boneheight):
                        self.bones.blit(self.centerbone, (bone*10, 6+i))
                if self.boneheight < self.maxheight:
                    self.boneheight += 10
                if self.boneheight > self.maxheight:
                    self.boneheight = self.maxheight
            elif self.face == "left" or self.face == "right":
                self.bones = pygame.Surface([12 + self.boneheight, self.width], pygame.SRCALPHA)
                for bone in range(math.ceil(self.width/10)):
                    self.bones.blit(self.topbone, (0, bone*10))
                    self.bones.blit(self.bottombone, (6+self.boneheight, bone*10))
                    for i in range(self.boneheight):
                        self.bones.blit(self.centerbone, (6+i, bone*10))
                if self.boneheight < self.maxheight:
                    self.boneheight += 10
                if self.boneheight > self.maxheight:
                    self.boneheight = self.maxheight
    def draw(self, screen):
        if self.warninging:
            pygame.draw.rect(screen, RED, self.warningrect, 2)
        elif self.stabbing:
            if self.face == "up":
                screen.blit(self.bones, (self.bbx + 5, self.bby + 5))
            elif self.face == "down":
                screen.blit(self.bones, (self.bbx + 5, self.bby - 5 + self.bbrh - self.boneheight - 12))
            elif self.face == "left":
                screen.blit(self.bones, (self.bbx + 5, self.bby + 5))
            elif self.face == "right":
                screen.blit(self.bones, (self.bbx - 5 + self.bbrw - self.boneheight, self.bby + 5))
class Platform:
    def __init__(self, timer, x, y, width, speed, life):
        self.starttime = timer
        self.x, self.y = int(x), int(y)
        self.speed = int(speed)
        self.life = int(life)
        self.width = int(width)
        self.greenrect = pygame.Rect(self.x, self.y, self.width, 6)
        self.whiterect = pygame.Rect(self.x, self.y+4, self.width, 6)
        self.remove = False
    def update(self, timer):
        if timer - self.starttime > self.life:
            self.remove = True
        self.x += self.speed
    def draw(self, screen):
        self.greenrect = pygame.Rect(self.x, self.y, self.width, 6)
        self.whiterect = pygame.Rect(self.x, self.y + 4, self.width, 6)
        pygame.draw.rect(screen, FAKEWHITE, self.whiterect, 1)
        pygame.draw.rect(screen, GREEN, self.greenrect, 1)
def main():
    global state
    attacklist = []
    truescreen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("UNDERTALE")
    soul = Soul()
    buttons = Buttons()
    clock = pygame.time.Clock()
    done = False
    attackcount = 0
    health = Health()
    options = Options()
    skipped = False
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(soul)
    battle_box = BattleBox(200, 200)
    sans = Sans(battle_box)
    soul.rect.center = battle_box.rect.center
    dialog_box = DialogBox(determination_mono, 570, 140, 45, 260)
    BIRDS.play(-1)
    skippable = False
    oldstate = state
    slashimation = Slashimation()
    choosing = False
    timer = 0
    lines = []
    facelist = []
    faceno = 0
    with open('Text/dialogue.txt') as file:
        for line in file:
            lines.append(line.rstrip())
    with open('Text/sans.txt') as file:
        content = file.read()
        sanslines = content.split('split')
        for line in range(len(sanslines)):
            sanslines[line] = sanslines[line].rstrip()
    with open('Text/faces.txt') as file:
        for line in file:
            facelist.append(line.rstrip())
    while not done:
        screen.fill(BLACK)
        draw_text(screen, "CHARA", info_font, WHITE, 35, 400)
        draw_text(screen, "LV 19", info_font, WHITE, 135, 400)
        draw_text(screen, "HP", HPKR_font, WHITE, 225, 403)
        draw_text(screen, "KR", HPKR_font, WHITE, 375, 403)
        if soul.karma > 0:
            draw_text(screen, str(soul.health) + " / 92", info_font, MAGENTA, 415, 400)
        else:
            draw_text(screen, str(soul.health) + " / 92", info_font, WHITE, 415, 400)
        if not oldstate == state: #check for state change
            oldstate = state
            timer = 0
            soul.up = False
            soul.down = False
            soul.left = False
            soul.right = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if state == 'yourturn':
                if choosing:
                    if event.type == pygame.KEYDOWN:
                        if len(options.sequence) == 1:
                            if event.key == pygame.K_LEFT:
                                buttons.choice -= 1
                                CURSOR.play()
                            if event.key == pygame.K_RIGHT:
                                buttons.choice += 1
                                CURSOR.play()
                        if event.key == pygame.K_z:
                            options.z(buttons.choice, dialog_box.completed)
                        if event.key == pygame.K_x:
                            options.x()
                if 'food' in options.sequence:
                    soul.healthyhealth = 92 - soul.karma
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
            if state == 'talk':
                if event.type == pygame.KEYDOWN:
                    if skippable == True:
                        if event.key == pygame.K_z:
                            skipped = True
            if event.type == pygame.KEYDOWN:  #hacks!
                if event.key == pygame.K_p:
                    if soul.godmode == True:
                        soul.godmode = False
                    elif soul.godmode == False:
                        soul.godmode = True
                    DING.play()
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
        health.update(soul.healthyhealth, soul.karma)
        health.draw(screen)
        sans.draw(screen, battle_box)
        buttons.update(choosing)
        buttons.draw(screen)
        battle_box.update()
        battle_box.draw(screen)
        if state == 'yourturn':
            battle_box.resize(570, 140)
            if timer == 0:
                options.sequence = ['flavortext']
                choosing = True
            if timer == 20:
                options.text = '*'
                if attackcount == 0:
                    number = 0
                    MEGALOVANIA.play(-1)
                elif attackcount == 4:
                    number = 2
                elif attackcount == 9:
                    number = 3
                elif attackcount == 12:
                    number = 4
                elif attackcount == 22:
                    number = 9
                elif attackcount == 23:
                    number = 10
                elif 30 <= soul.karma < 40:
                    number = 14
                elif 20 <= soul.karma < 30:
                    number = 13
                elif 10 <= soul.karma < 20:
                    number = 12
                elif 0 < soul.karma < 10:
                    number = 11
                elif attackcount < 12:
                    number = 1
                else:
                    number = random.randint(5, 8)
            elif timer > 20:  # waited until box animation is finished
                options.update(dialog_box, lines[number])
                dialog_box.update()
                dialog_box.draw(screen)
                if 'done' in options.sequence: #end turn here
                    if buttons.choice == 1: #if attack
                        if not slashimation.active and not slashimation.completed:
                            slashimation.start()
                            starttime = timer
                        slashimation.update()
                        if slashimation.frame >= 0:
                            sans.slash = slashimation.frame * 20
                        slashimation.draw(screen, SCREEN_WIDTH/2-13, SCREEN_HEIGHT/2-150)
                        if slashimation.completed:
                            draw_text(screen, "MISS", damage_font, WHITE, SCREEN_WIDTH/2-64, 50)
                            if timer-starttime > 30 and sans.slash > 0:
                                sans.slash -= 10
                            if sans.slash == 0:
                                state = 'talk'
                                attackcount += 1
                                slashimation.completed = False
                    else:
                        state = 'histurn'
            #soul follow buttons
            if choosing:
                if options.soulpos == 0:
                    soul.rect.x = 44 + 155 * buttons.choice - 155
                    soul.rect.y = 444
                    if soul.soulmode == 'BLUE':
                        soul.image = soul.blueimg
                    elif soul.soulmode == 'RED':
                        soul.image = soul.redimg
                elif options.soulpos == 1:
                    soul.rect.x = 60
                    soul.rect.y = 280
                    if soul.soulmode == 'BLUE':
                        soul.image = soul.blueimg
                    elif soul.soulmode == 'RED':
                        soul.image = soul.redimg
                elif options.soulpos == 2:
                    soul.image = soul.transparent_img
        elif state == 'histurn':
            if timer == 0:  # sans attack here.
                sans.update(0)
                battle_box.resize(200, 200)
                soul.rect.center = battle_box.rect.center
                soul.direction = 1
                attacklist = []
                if attackcount == 0:
                    wtl = 'Intro'
                elif attackcount == 1:
                    wtl = 'bonegap1'
                elif attackcount == 2:
                    wtl = 'bluebone'
                elif attackcount == 3:
                    wtl = 'bonegap2'
                elif attackcount == 4:
                    wtl = 'platforms1'
                elif attackcount == 5:
                    wtl = 'platforms2'
                elif attackcount == 6:
                    wtl = 'platforms3'
                elif attackcount == 7:
                    wtl = 'platforms4'
                elif attackcount == 8:
                    wtl = 'boneslideh'
                elif attackcount == 9:
                    wtl = 'platformblaster'
                elif attackcount <= 13:
                    wtl = random.choice(['bonegap1fast', 'bonegap2', 'boneslideh', 'platformblasterfast', 'platforms4hard'])
                elif attackcount == 14:
                    wtl = 'bonestab1'
                elif attackcount == 15:
                    wtl = 'boneslidev'
                elif attackcount < 24:
                    wtl = random.choice(['bonegap1fast', 'bonegap2', 'boneslideh', 'platformblasterfast', 'platforms4hard', 'boneslidev', 'bonestab2', 'bonestab3'])
                elif attackcount == 24:
                    wtl = 'Spare'
                if 'spare' in options.sequence:
                    wtl = 'Spare'
                with open('Attacks/' + wtl, 'r') as file:
                    raw_attacks = file.read().strip().split('\n')
                precomputed_attacks = []
                for attack_line in raw_attacks:
                    p = attack_line.split(' ')
                    attack_info = {
                        'time': int(p[0]),
                        'type': p[1],
                        'params': p[2:]
                    }
                    precomputed_attacks.append(attack_info)
                precomputed_attacks.sort(key=lambda x: x['time'])
            for attack in precomputed_attacks:
                if attack['time'] == timer:
                    if attack['type'] == 'GB':
                        attacklist.append(GasterBlaster(timer, *map(int, attack['params'])))
                    elif attack['type'] == 'GBB':
                        attacklist.append(BigGasterBlaster(timer, *map(int, attack['params'])))
                    elif attack['type'] == 'GBS':
                        attacklist.append(SkinnyGasterBlaster(timer, *map(int, attack['params'])))
                    elif attack['type'] == 'B':
                        attacklist.append(Bone(timer, *map(int, attack['params'])))
                    elif attack['type'] == 'BB':
                        attacklist.append(BlueBone(timer, *map(int, attack['params'])))
                    elif attack['type'] == 'BS':
                        attacklist.append(BoneStab(timer, battle_box, *map(str, attack['params'])))
                    elif attack['type'] == 'P':
                        attacklist.append(Platform(timer, *map(str, attack['params'])))
                    elif attack['type'] == 'SM':
                        if not soul.soulmode == attack['params'][0]:
                            DING.play()
                            soul.soulmode = attack['params'][0]
                    elif attack['type'] == 'S':
                        soul.direction = int(attack['params'][0])
                        soul.slam = True
                    elif attack['type'] == 'resize':
                        battle_box.resize(int(attack['params'][0]), int(attack['params'][1]))
                    elif attack['type'] == 'TP':
                        soul.rect.x, soul.rect.y = int(attack['params'][0]), int(attack['params'][1])
                    elif attack['type'] == 'END':
                        attacklist = []
                        state = 'yourturn'
            for i in attacklist:
                i.update(timer)
                i.draw(screen)
                if i.remove:
                    attacklist.remove(i)
        elif state == 'talk':
            if timer == 0:
                sansbubble = SansBubble(SCREEN_WIDTH / 2 + 50, sans.y+20)
                text = sanslines[attackcount]
                text = text.split('\n')
                lineno = 0
                sansbubble.set_text(text[lineno])
                sans.update(int(facelist[faceno][0]))
                faceno+=1
                choosing = False
            skippable = False
            if sansbubble.completed:
                skippable = True
                if skipped:
                    lineno += 1
                    if lineno < len(text):
                        sansbubble.set_text(text[lineno])
                        sans.update(int(facelist[faceno][0]))
                        faceno += 1
                    else:
                        if attackcount == 0:
                            BIRDS.stop()
                        state = 'histurn'
                    skipped = False
            sansbubble.update()
            sansbubble.draw(screen)
        active_sprite_list.update(battle_box, screen, attacklist)
        active_sprite_list.draw(screen)
        if soul.gameover:
            done = True

        truescreen.blit(screen, screenshake(soul.shake))
        timer += 1
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
