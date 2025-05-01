'''Sans Fight'''
__version__ = "April 17 2025"
__author__ = "Ryan Xue"

import pygame, random, math

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (210, 0, 0)
YELLOW = (255, 252, 4)
MAGENTA = (255, 0, 255)
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
CHOICE = pygame.mixer.Sound('Sound/The_Choice.ogg')
MEGALOVANIA.set_volume(0.6)
TEXT = pygame.mixer.Sound('Sound/BattleText.ogg')
DING = pygame.mixer.Sound('Sound/Ding.ogg')
HURT = pygame.mixer.Sound('Sound/PlayerDamaged.ogg')
CURSOR = pygame.mixer.Sound('Sound/MenuCursor.ogg')
SELECT = pygame.mixer.Sound('Sound/MenuSelect.ogg')
SLASH = pygame.mixer.Sound('Sound/snd_laz.wav')

class Options:
    def __init__(self):
        self.items = ["I. Noodles", "Pie", "SnowPiece", "SnowPiece", "SnowPiece", "Steak", "L. Hero", "L. Hero"]
        self.sequence = ['flavortext']
        self.text = None
        self.oldtext = self.text
        self.sigma = 'no'
        self.soulpos = 0

    def update(self, dialog_box, flavortext):
        if not self.oldtext == self.text:
            if not self.text == None:
                if self.sigma == 'yes':
                    dialog_box.set_text(self.text, False)
                    self.soulpos = 2
                else:
                    dialog_box.set_text(self.text, True)
                    self.soulpos = 1
            else:
                dialog_box.set_text(flavortext, False)
                self.soulpos = 0
            self.oldtext = self.text
        self.sigma = 'no'
        if len(self.sequence) == 1:
            self.text = None
        elif len(self.sequence) == 2:
            if self.sequence[1] == 'sans':
                self.text = '   * Sans'
            elif self.sequence[1] == 'spare':
                self.text = '   * Spare'
            elif self.sequence[1] == 'food':
                self.text = '* You ate the ' + self.items[0] + '.'  #temporary?
                self.sigma = 'yes'
        elif len(self.sequence) == 3:
            if self.sequence[2] == 'check':
                self.text = '   * Check'
        elif len(self.sequence) == 4:
            if self.sequence[3] == 'check1':
                self.text = '* Sans 1 ATK 1 DEF                * The easiest enemy.              * Can only deal 1 damage.'
                self.sigma = 'yes'
        elif len(self.sequence) == 5:
            if self.sequence[4] == 'check2':
                self.text = '* Can\'t keep dodging forever.       Keep attacking.'
                self.sigma = 'yes'

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
        self.left = False
        self.right = False
        self.up = False
        self.down = False
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
        self.height = 0
        self.olddirection = self.direction
        self.shake = 0
        self.impacting = False
        self.hurting = False
        self.karmaframes = 0

    def update(self, battle_box):
        if state == 'histurn':
            if self.soulmode == 'RED':
                self.image = self.redimg
                self.direction = 1
                self.height = 0
                self.impacting = False
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

                if ((self.up and self.direction == 1) or (self.left and self.direction == 2) or (
                        self.down and self.direction == 3) or (
                            self.right and self.direction == 4)) and self.height <= 10:
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
                    SLAM.play()
                    self.height = 0
                if self.shake == 5:
                    self.shake = -1
                self.shake += 1
            if self.velocity == 0:
                self.height = 0
                if self.impacting:
                    self.shake = 1
        else:  #menu choosing
            self.direction = 1
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
        if self.health > 1:
            if self.hurting:
                HURT.stop()
                HURT.play()
                if self.healthyhealth == 1:
                    self.karma -= 1
                else:
                    self.karma += 5  #for now
                    self.healthyhealth = self.health - self.karma - 1
        else:
            self.karma = 0
        self.health = self.healthyhealth + self.karma


class BattleBox(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((640 - width) / 2, 390 - height, width, height)
        self.target_rect = None
        self.speed = 25
        self.animating = False
        self.sans = pygame.image.load('tempsans.gif').convert_alpha()

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 5)
        screen.blit(self.sans, (SCREEN_WIDTH / 2 - 59, self.rect.y - 160))

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


class SpriteSheet():
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



def rotate_center(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image


def load_font(font_path, size):
    font = pygame.font.Font(font_path, size)
    return font


info_font = load_font('Fonts/Mars.ttf', 24)
HPKR_font = load_font('Fonts/8-BIT WONDER.TTF', 12)
sans_font = load_font('Fonts/pixel-comic-sans-undertale-sans-font.ttf', 12)
determination_mono = load_font('Fonts/DeterminationMonoWebRegular-Z5oq.ttf', 32)


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


def main():
    global state
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
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(soul)
    battle_box = BattleBox(200, 200)
    soul.rect.center = battle_box.rect.center
    dialog_box = DialogBox(determination_mono, 570, 140, 45, 260)
    oldstate = state
    slashimation = Slashimation()
    choosing = False
    timer = 0
    lines = []
    with open('Text/dialogue.txt') as file:
        for line in file:
            lines.append(line.rstrip())
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
            if event.type == pygame.KEYDOWN:  #debug keys
                if event.key == pygame.K_s:
                    soul.direction = 1
                elif event.key == pygame.K_d:
                    soul.direction = 2
                elif event.key == pygame.K_w:
                    soul.direction = 3
                elif event.key == pygame.K_a:
                    soul.direction = 4
                elif event.key == pygame.K_1:
                    if soul.soulmode == 'BLUE':
                        soul.soulmode = 'RED'
                    else:
                        soul.soulmode = 'BLUE'
                    DING.play()
                elif event.key == pygame.K_RETURN:
                    if state == 'histurn':
                        state = 'yourturn'
                        timer = 0
                    else:
                        state = 'histurn'
                elif event.key == pygame.K_SPACE:
                    soul.hurting = True
                elif event.key == pygame.K_p:
                    print(pygame.mouse.get_pos())
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    soul.hurting = False
        health.update(soul.healthyhealth, soul.karma)
        health.draw(screen)
        buttons.update(choosing)
        buttons.draw(screen)
        battle_box.update()
        active_sprite_list.update(battle_box)
        battle_box.draw(screen)
        active_sprite_list.draw(screen)
        if state == 'yourturn':
            battle_box.resize(570, 140)
            if timer == 0:
                options.sequence = ['flavortext']
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
                        if not slashimation.active:
                            slashimation.start()
                        slashimation.update()
                        slashimation.draw(screen, SCREEN_WIDTH/2-13, SCREEN_HEIGHT/2-100)
                        if slashimation.completed:
                            state = 'histurn'
                            attackcount += 1
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
            timer += 1
        elif state == 'histurn':
            battle_box.resize(200, 200)
        if not oldstate == state:
            oldstate = state
            if state == 'yourturn':
                if attackcount == 12:
                    pygame.mixer.pause()
                    CHOICE.play(-1)
                elif attackcount == 13:
                    CHOICE.stop()
                    pygame.mixer.unpause()
                choosing = True
            else:
                choosing = False
                soul.rect.x = SCREEN_WIDTH / 2 - 8
                soul.rect.y = SCREEN_HEIGHT
            soul.up = False
            soul.down = False
            soul.left = False
            soul.right = False
        truescreen.blit(screen, screenshake(soul.shake))
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
