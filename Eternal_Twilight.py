import sys

import pygame
import random
import time

from datetime import datetime

import button

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

pygame.mixer.pre_init(32100, -16, 2, 8192)

pygame.init()

size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Eternal Twilight")

pygame.display.set_icon(pygame.image.load("items/darkdevotionart.png"))


# главные параметры
class Settings:
    def __init__(self):
        self.startmusic_count = 1

        self.first_enemy_count = 3
        self.second_enemy_count = 4

        self.stinger_damage = 50
        self.stinger_damage_plus = 0

        self.quit_the_game = True
        self.howtoplay = False
        self.gamesettings = False

        self.change_level_1 = 1
        self.change_level_2 = 1

        self.floor = 1
        self.player_speed_procent = 100

        self.ghost_protect_procent = 0
        self.ghost_damage_plus = 0
        self.ghost_speed = 1.7
        self.ghost_damage = 1000

        self.death_count = 0

        self.multiply = 1

        self.bad_time_points = 100
        self.bad_health_points = 0
        self.points_by_time = 100

        self.point_per_item = 35
        self.items = 0
        self.items_inventory = 0

        self.health_points = 75
        self.max_points = self.health_points + self.points_by_time + self.point_per_item
        self.points = 0

        self.accessouars_list = ['speed', 'heal', 'torch', 'boots', 'armor']
        self.change_accessouars_list = False
        self.already_used_accessouar = None

        self.boots = False
        self.armor = False

        self.platform_list = pygame.sprite.Group()
        self.stinger_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()

        self.help = False
        self.end_the_game = False

        self.game_win = False
        self.game_paused = False

        self.startmenu = True

        self.menu_state = 'main'
        self.startmenu_state = 'main'

        # смерть

        self.quitlost_button = button.Button(SCREEN_WIDTH / 1.4, 600, pygame.image.load("buttons/gameoverexit.png").
                                             convert_alpha(), 1)
        self.startmenu_lost_button = button.Button(SCREEN_WIDTH / 2.6, 600,
                                                   pygame.image.load("buttons/startmenulost.png"
                                                                     "").convert_alpha(), 1)

        self.playagainlost_button = button.Button(SCREEN_WIDTH / 19, 600,
                                                  pygame.image.load("buttons/playagainlost.png").
                                                  convert_alpha(), 1)

        # стартовое меню

        continue_img = pygame.image.load("buttons/startmenu2.png").convert_alpha()
        comeback_img = pygame.image.load("buttons/backbutton.png").convert_alpha()
        pass_img = pygame.image.load("buttons/startmenu2.png").convert_alpha()
        readmore_img = pygame.image.load("buttons/readmore.png").convert_alpha()

        # start2
        self.continue_button = button.Button(SCREEN_WIDTH / 1.6, 600, continue_img, 1)
        self.comeback_button = button.Button(SCREEN_WIDTH / 7, 600, comeback_img, 1)

        # start 1
        self.pass_button = button.Button(SCREEN_WIDTH / 7, 600, pass_img, 1)
        self.readmore_button = button.Button(SCREEN_WIDTH / 1.6, 600, readmore_img, 1)

        self.newgame_button = button.Button(SCREEN_WIDTH / 2.6, 220, pygame.image.load("buttons/newgame.png").
                                            convert_alpha(), 1)
        self.aboutgame_button = button.Button(SCREEN_WIDTH / 2.6, 345, pygame.image.load("buttons/aboutgame.png").
                                              convert_alpha(), 1)

        # self.prekwil_button = button.Button(SCREEN_WIDTH / 2.6, 400, pygame.image.load("buttons/prekwil.png").
        #                                     convert_alpha(), 1)

        self.exit_button = button.Button(SCREEN_WIDTH / 2.6, 470, pygame.image.load("buttons/exitthegame.png").
                                         convert_alpha(), 1)

        self.con = True
        self.con2 = True

        # другое

        resume_img = pygame.image.load("buttons/continue.png").convert_alpha()
        options_img = pygame.image.load("buttons/aboutgame.png").convert_alpha()
        startmenu_img = pygame.image.load("buttons/startmenu.png").convert_alpha()
        quit_img = pygame.image.load("buttons/exitthegame.png").convert_alpha()

        items_img = pygame.image.load("buttons/itemsbutton.png").convert_alpha()
        back_img = pygame.image.load("buttons/backbutton.png").convert_alpha()
        enemy_img = pygame.image.load("buttons/enemybutton.png").convert_alpha()

        self.resume_button = button.Button(SCREEN_WIDTH / 2.6, 125, resume_img, 1)
        self.options_button = button.Button(SCREEN_WIDTH / 2.6, 250, options_img, 1)
        self.startmenu_button = button.Button(SCREEN_WIDTH / 2.6, 375, startmenu_img, 1)
        self.quit_button = button.Button(SCREEN_WIDTH / 2.6, 500, quit_img, 1)

        self.items_button = button.Button(SCREEN_WIDTH / 19, 600, items_img, 1)
        self.enemy_button = button.Button(SCREEN_WIDTH / 2.6, 600, enemy_img, 1)
        self.back_button = button.Button(SCREEN_WIDTH / 1.4, 600, back_img, 1)
        self.inmenu_button = button.Button(SCREEN_WIDTH / 1.4, 600, pygame.image.load("buttons/inmenu.png").
                                           convert_alpha(), 1)

        self.num = 0

        self.levellist = []
        self.current_level = None

        self.active_sprite_list = pygame.sprite.Group()

        self.ground_surf = pygame.image.load('background/pol3.jpg').convert_alpha()
        self.death_music_count = 1
        self.temp = 0

    def game_over(self):
        self.points_by_time = 100
        self.health_points = 75
        self.point_per_item = 35
        self.bad_time_points = 100
        self.points = self.bad_time_points + self.bad_health_points + self.items_inventory
        self.max_points = self.health_points + self.points_by_time + self.point_per_item * 2


settings = Settings()


# настройка персонажа
class Player(pygame.sprite.Sprite):
    # прорисовывание персонажа
    def __init__(self, file, pos, group):
        super().__init__(group)

        self.player_health = 100
        self.player_speed = 3.5

        self.file = file

        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect(center=pos)

        self.change_x = 0
        self.change_y = 0

        self.GorizontalWalking = False
        self.VerticalWalking = False

        self.Frame = 0

        self.Left = False
        self.Right = True
        self.Up = False
        self.Down = False

    # движение персонажа
    def player_moving(self):

        key = pygame.key.get_pressed()
        if key[pygame.K_d] or key[pygame.K_RIGHT]:

            if settings.end_the_game is False:
                music.sound.play()

            self.change_x = self.player_speed

            self.GorizontalWalking = True
            self.VerticalWalking = False
            self.Left = False
            self.Right = True
            self.Up = False
            self.Down = False

        if key[pygame.K_a] or key[pygame.K_LEFT]:

            if settings.end_the_game is False:
                music.sound.play()

            self.change_x = -self.player_speed + 0.55

            self.GorizontalWalking = True
            self.VerticalWalking = False
            self.Left = True
            self.Right = False
            self.Up = False
            self.Down = False

        if key[pygame.K_w] or key[pygame.K_UP]:

            if settings.end_the_game is False:
                music.sound.play()

            self.change_y = -self.player_speed + 0.55

            self.GorizontalWalking = False
            self.VerticalWalking = True
            self.Left = False
            self.Right = False
            self.Up = True
            self.Down = False

        if key[pygame.K_s] or key[pygame.K_DOWN]:

            if settings.end_the_game is False:
                music.sound.play()

            self.change_y = self.player_speed

            self.GorizontalWalking = False
            self.VerticalWalking = True
            self.Left = False
            self.Right = False
            self.Up = False
            self.Down = True

        if key[pygame.K_d] and key[pygame.K_a]:
            music.sound.stop()

            if key[pygame.K_w] or key[pygame.K_s]:
                self.VerticalWalking = True
            self.GorizontalWalking = False

            self.change_x = 0

        if key[pygame.K_w] and key[pygame.K_s]:
            music.sound.stop()

            if key[pygame.K_a] or key[pygame.K_d]:
                self.GorizontalWalking = True
            self.VerticalWalking = False
            self.change_y = 0

        if not key[pygame.K_w] and not key[pygame.K_s] and not key[pygame.K_a] and not key[pygame.K_d] \
                and not key[pygame.K_RIGHT] and not key[pygame.K_LEFT] \
                and not key[pygame.K_DOWN] and not key[pygame.K_UP]:
            self.VerticalWalking = False
            self.GorizontalWalking = False
            music.sound.stop()

    def update(self):

        if self.player_health >= 100:
            settings.bad_health_points = 75

        elif 49 < self.player_health <= 99:
            settings.bad_health_points = 40

        else:
            settings.bad_health_points = 25

        self.rect.x += self.change_x

        if self.player_health <= 0:
            self.player_health = 0
            settings.end_the_game = True

        block_hit_list = pygame.sprite.spritecollide(self, settings.platform_list, False)

        for block in block_hit_list:

            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:

                self.rect.left = block.rect.right
        self.change_x = 0

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, settings.platform_list, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

        self.change_y = 0

        if self.Right:
            self.file = 'right'
        if self.Left:
            self.file = 'left'
        if self.Up:
            self.file = 'up'
        if self.Down:
            self.file = 'down'

        if settings.end_the_game is True:
            self.image = pygame.image.load('playerimage/down/deadbody.png')

        elif self.VerticalWalking:
            self.Frame += self.player_speed / 50
            if self.Frame > 2:
                self.Frame = 0

            Personnel = ['0.png', '1.png']
            self.image = pygame.image.load(
                'playerimage/' + self.file + '/' + Personnel[int(self.Frame)]).convert_alpha()

        elif self.GorizontalWalking:
            self.Frame += self.player_speed / 50
            if self.Frame > 2:
                self.Frame = 0

            Personnel = ['0.png', '1.png']
            self.image = pygame.image.load(
                'playerimage/' + self.file + '/' + Personnel[int(self.Frame)]).convert_alpha()

        else:
            self.image = pygame.image.load('playerimage/' + self.file + '/main.png').convert_alpha()

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


# загрузка, движение, урон от призрака
class Ghost(pygame.sprite.Sprite):
    def __init__(self, file, group):
        super().__init__(group)

        self.flip_on = True

        self.speed_x = settings.ghost_speed
        self.speed_y = settings.ghost_speed

        self.max_ghost_screen_width = 1600
        self.max_ghost_screen_height = 1000

        self.damage_on = True

        self.right = True
        self.speedometr = random.choice([1, 2])

        if settings.floor == 1:
            self.max_ghost_screen_width = 1600
            self.max_ghost_screen_height = 1000
            self.max_y2 = 100
            self.max_y1 = 400

        elif settings.floor == 2:
            self.max_ghost_screen_width = 2000
            self.max_ghost_screen_height = 1500
            self.max_y2 = 400
            self.max_y1 = 100

        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect(center=(random.uniform(100, self.max_ghost_screen_width - 50),
                                                random.uniform(self.max_y2, self.max_ghost_screen_height - self.max_y1))
                                        )

    def update(self):
        if self.flip_on is True:

            if self.speedometr == 1:
                self.speed_x = settings.ghost_speed
                self.speed_y = settings.ghost_speed
            else:
                self.speed_x = -settings.ghost_speed
                self.speed_y = -settings.ghost_speed
            self.flip_on = False

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > self.max_ghost_screen_width:
            self.speed_x = -self.speed_x

        if self.rect.top < 0 or self.rect.bottom > self.max_ghost_screen_height:
            self.speed_y = -self.speed_y

        if self.speed_x >= 0:
            if self.right:
                self.flip()
                self.right = False

        if self.speed_x <= 0:
            if not self.right:
                self.flip()
                self.right = True

        if settings.armor is False and settings.end_the_game is False:
            if self.rect.x - 30 < player.rect.x < self.rect.x + 30 and \
                    self.rect.y - 60 < player.rect.y < self.rect.y + 30:

                if self.damage_on is True:
                    music.sound.stop()
                    music.ghost_smeh.play()
                    player.player_health -= settings.ghost_damage
                    self.damage_on = False

            else:
                self.damage_on = True
        else:
            settings.ghost_protect_procent = 100

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


# наложение камеры
class CameraGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.camera_borders = {'left': 300, 'right': 300, 'top': 350, 'bottom': 100}
        left = self.camera_borders['left']
        top = self.camera_borders['top']
        width = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        height = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(left, top, width, height)

        self.ground_rect = settings.ground_surf.get_rect(topleft=(0, 0))

        self.keyboard_speed = 5

        self.zoom_scale = 1
        self.internal_surf_size = (1000, 1000)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def box_target_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, player):

        self.box_target_camera(player)
        self.internal_surf.fill('#71ddee')

        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(settings.ground_surf, ground_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.top + sprite.rect.bottom +
                                                                sprite.rect.right - sprite.rect.left):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(500, 200))

        self.display_surface.blit(scaled_surf, scaled_rect)


# свиток
class MagicScroll(pygame.sprite.Sprite):
    # установка книги
    def __init__(self, flag, group):
        super().__init__(group)

        self.count = 0

        if flag == 1:
            self.svit = random.choice([[150, 150], [900, 150], [1450, 850], [900, 300]])

        elif flag == 2:
            self.svit = random.choice(
                [[955, 1355], [1700, 1350], [400, 1100], [155, 445], [550, 400],
                 [600, 1200]])

        self.image = pygame.image.load('items/book.png')
        self.rect = self.image.get_rect(center=(self.svit[0], self.svit[1]))

    def picked(self):
        global portal

        if self.count == 0:
            self.count = 1
            music.sound.stop()
            music.scroll_sound.play()
            scroll.kill()
            portal = Portal('items/blueportal.png', camera_group)
            portal.rect.x = 1350
            portal.rect.y = 150
            settings.num = 1

        elif self.count == 2:
            music.sound.stop()
            music.scroll_sound.play()
            scroll.kill()
            portal = Portal('items/greenportal.png', camera_group)
            portal.rect.x = 150
            portal.rect.y = 150
            settings.num = 1
            self.count = 3


# использование портала
class Portal(pygame.sprite.Sprite):
    def __init__(self, port, group):
        super().__init__(group)

        self.image = pygame.image.load(port)
        self.rect = self.image.get_rect(center=(-200, -200))

    @staticmethod
    def used():
        global scroll, ghost, accesouar

        if scroll.count == 1:
            settings.num = 0

            scroll.kill()
            portal.kill()
            accesouar.kill()
            accesouar.kill()

            settings.change_accessouars_list = True

            scroll = MagicScroll(2, camera_group)
            scroll.count = 2
            settings.floor = 2

            accesouar = Accessories(camera_group)

            for sprite in settings.stinger_list.sprites():
                sprite.kill()

            for sprite in settings.platform_list.sprites():
                sprite.kill()

            settings.startmenu = True
            settings.startmenu_state = 'floor_2'

            settings.levellist.append(SecondFloor())
            SecondFloor().update()

        elif scroll.count == 3:
            settings.game_win = True
            settings.menu_state = 'win'


# установка тени
class Shadow(pygame.sprite.Sprite):
    def __init__(self, blackhole, group):
        super().__init__(group)

        self.x_position = 674
        self.y_position = 668

        self.image = pygame.image.load(blackhole)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = player.rect.x - self.x_position
        self.rect.y = player.rect.y - self.y_position


# стены
class Platform(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('items/prozwall.png')
        self.rect = self.image.get_rect()


# урон шипов
class Stinger(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.music_count = 0

        self.damage = 0

        self.protect_procent = 0

        self.damage_count = 1

        self.damage_on = True

        self.image = pygame.image.load('items/stinger.png')
        self.rect = self.image.get_rect(center=(-100, -100))

    def update(self):

        if settings.boots is False:
            if self.rect.x - 40 < player.rect.x < self.rect.x + 10 and \
                    self.rect.y - 50 < player.rect.y < self.rect.y + 10:

                if self.damage_on is True:
                    if self.damage_count == 1:
                        player.player_health -= settings.stinger_damage
                        self.damage_count = 0
                    music.sound.stop()
                    music.hit.play()
                    self.damage_on = False

            else:
                self.damage_count = 1
                self.damage_on = True

        else:
            self.protect_procent = 100


# акссессуары
class Accessories(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.new_shadow = 'blackphon5.png'

        self.heal = 35
        self.speed_up = 0.5
        self.use_times = 1

        self.torch_up = False

        self.chance = random.choice([1])
        # загрузка инвентаря
        if self.chance == 1:

            if settings.change_accessouars_list is False:
                self.positions = [[150, 350], [150, 700], [1450, 400], [1450, 850], [900, 300], [900, 150], [150, 150]]

            if settings.change_accessouars_list is True:
                self.positions = [[1700, 550], [975, 925], [955, 1355], [1700, 1350], [840, 350],
                                  [400, 1100], [550, 390], [600, 1200], [150, 445], [1850, 1335]]
        else:
            self.positions = [[-100, -100]]

        for pos in self.positions:
            if pos == scroll.svit:
                self.positions.remove(pos)

        self.acces = random.choice(settings.accessouars_list)

        if self.acces != 'heal' and self.acces != 'speed':
            settings.accessouars_list.remove(self.acces)

        if self.acces == 'heal':
            self.image = pygame.image.load('items/healpotion.png')

        if self.acces == 'speed':
            self.image = pygame.image.load('items/speedpotion.png')

        if self.acces == 'torch':
            self.image = pygame.image.load('items/fonar.png')

        if self.acces == 'boots':
            self.image = pygame.image.load('items/boots.png')

        if self.acces == 'armor':
            self.image = pygame.image.load('items/armor.png')

        position = random.choice(self.positions)
        self.rect = self.image.get_rect(center=(position[0], position[1]))

    def picked(self):
        global shadow
        # условие использования инвентаря
        if self.use_times:

            if self.acces == 'heal':
                accesouar.kill()
                music.sound.stop()
                music.drink.play()
                settings.items += 1
                player.player_health += self.heal
                settings.items_inventory += settings.point_per_item
                self.use_times -= 1

            if self.acces == 'speed':
                accesouar.kill()
                music.sound.stop()
                music.drink.play()
                player.player_speed += self.speed_up
                settings.items_inventory += settings.point_per_item
                settings.player_speed_procent += 15
                settings.items += 1
                self.use_times -= 1

            if self.acces == 'boots':
                accesouar.kill()
                music.sound.stop()
                music.taked_item.play()
                settings.items_inventory += settings.point_per_item
                settings.items += 1
                settings.boots = True
                self.use_times -= 1

            if self.acces == 'armor':
                accesouar.kill()
                music.sound.stop()
                music.taked_item.play()
                settings.items_inventory += settings.point_per_item
                settings.items += 1
                settings.armor = True
                self.use_times -= 1

            if self.acces == 'torch':
                accesouar.kill()
                music.sound.stop()
                shadow.kill()
                music.taked_item.play()
                settings.items_inventory += settings.point_per_item
                settings.items += 1
                shadow = Shadow(self.new_shadow, camera_group)

                if self.new_shadow == 'blackphon5.png':
                    shadow.x_position = 822
                    shadow.y_position = 820

                self.use_times -= 1


# прорисовка первой карты
class FirstFloor:
    def __init__(self):
        self.count_switch = True

        walls = [
            # верхняя часть стен

            [100, 50],
            [150, 50],
            [200, 50],
            [250, 50],
            [300, 50],
            [350, 50],
            [400, 50],
            [450, 50],
            [500, 50],
            [550, 50],
            [600, 50],
            [650, 50],
            [700, 50],
            [750, 50],
            [800, 50],
            [850, 50],
            [900, 50],
            [950, 50],
            [1000, 50],
            [1050, 50],
            [1100, 50],
            [1150, 50],
            [1200, 50],
            [1250, 50],
            [1300, 50],
            [1350, 50],
            [1400, 50],
            [1450, 50],

            # нижняя часть стен

            [100, 900],
            [150, 900],
            [200, 900],
            [250, 900],
            [300, 900],
            [350, 900],
            [400, 900],
            [450, 900],
            [500, 900],
            [550, 900],
            [600, 900],
            [650, 900],
            [700, 900],
            [750, 900],
            [800, 900],
            [850, 900],
            [900, 900],
            [950, 900],
            [1000, 900],
            [1050, 900],
            [1100, 900],
            [1150, 900],
            [1200, 900],
            [1250, 900],
            [1300, 900],
            [1350, 900],
            [1400, 900],
            [1450, 900],

            # серединные вертикальные стены
            [200, 100],
            [250, 100],
            [100, 400],
            [450, 200],
            [950, 100],
            [950, 200],
            [950, 300],
            [950, 400],
            [850, 350],
            [800, 350],
            [950, 500],
            [950, 550],
            [1150, 50],
            [1150, 250],
            [450, 250],
            [150, 400],
            [100, 750],
            [150, 750],
            [200, 750],
            [350, 750],
            [400, 750],
            [450, 750],
            [500, 750],
            [550, 750],
            [600, 750],
            [650, 750],
            [800, 750],
            [850, 750],
            [900, 750],
            [950, 750],
            [1000, 750],
            [1050, 750],
            [1200, 750],
            [1250, 750],
            [1300, 750],
            [1350, 750],
            [1400, 750],
            [1450, 750],
            [200, 600],
            [350, 600],
            [500, 600],
            [650, 600],
            [800, 600],
            [950, 600],
            [1000, 600],
            [1050, 600],
            [1100, 600],
            [1150, 600],
            [1200, 600],
            [1250, 600],
            [1300, 600],
            [1350, 600],
            [100, 450],
            [150, 450],
            [200, 450],
            [350, 450],
            [400, 450],
            [450, 450],
            [500, 450],
            [550, 450],
            [600, 450],
            [650, 450],
            [950, 450],
            [1000, 450],
            [1150, 450],
            [1200, 450],
            [1250, 450],
            [1300, 450],
            [1350, 450],
            [1400, 450],
            [1450, 450],
            [200, 400],
            [650, 400],
            [800, 400],
            [850, 400],
            [900, 400],
            [1000, 400],
            [900, 350],
            [200, 300],
            [250, 300],
            [300, 300],
            [350, 300],
            [400, 300],
            [450, 300],
            [500, 300],
            [650, 300],
            [1000, 300],
            [1150, 300],
            [1200, 300],
            [1250, 300],
            [1300, 300],
            [1350, 300],
            [1400, 300],
            [1450, 300],
            [1200, 250],
            [1200, 100],
            [1150, 100],
            [1000, 200],
            [1000, 100],
            [1050, 850],
            [200, 700],
            [350, 700],
            [650, 700],
            [800, 700],
            [500, 500],
            [650, 200],
            [700, 200],
            [750, 200],
            [800, 200],
            [850, 200],
            [900, 200],
            [500, 200],
            [800, 550],
            [1000, 550],
            [200, 150],
            [250, 150],
            [300, 150],
            [200, 900],
            # [100, 100], # ключ

            # левая боковая стена

            [50, 50],
            [50, 150],
            [50, 250],
            [50, 350],
            [50, 450],
            [50, 550],
            [50, 650],
            [50, 750],
            [50, 850],

            #  правая боковая стена
            [1500, 100],
            [1500, 200],
            [1500, 300],
            [1500, 400],
            [1500, 500],
            [1500, 600],
            [1500, 700],
            [1500, 800],
            [1500, 900]

        ]

        for wall in walls:
            block = Platform()
            block.rect.x = wall[0]
            block.rect.y = wall[1]

            settings.platform_list.add(block)
        # установка шипов
        stingers = [[620, 300], [620, 720], [260, 200], [460, 420], [450, 800], [1350, 800], [1120, 280], [750, 100],
                    [1000, 650]]

        for stin in stingers:
            stinger = Stinger(camera_group)
            stinger.rect.x = stin[0]
            stinger.rect.y = stin[1]

            settings.stinger_list.add(stinger)

    def update(self):
        global ghost
        if self.count_switch is True:
            for i in range(settings.first_enemy_count):
                ghost = Ghost('items/whiteghost.png', camera_group)
                settings.enemy_list.add(ghost)

            self.count_switch = False
        settings.platform_list.update()

    @staticmethod
    def draw(screen):
        settings.platform_list.draw(screen)


# прорисовка второй карты
class SecondFloor:
    def __init__(self):
        self.count_switch = True

        for sprite in settings.enemy_list.sprites():
            sprite.kill()

        walls = [
            # серединные стены
            [1750, 200],
            [1700, 200],
            [1650, 200],
            [1600, 200],
            [1550, 200],
            [1500, 200],
            [1450, 200],
            [1750, 300],
            [1750, 450],
            [1750, 550],
            [1700, 450],
            [1650, 450],
            [1600, 450],
            [1600, 350],
            [1550, 350],
            [1500, 350],
            [1450, 350],
            [1450, 400],
            [1750, 600],
            [1700, 600],
            [1650, 600],
            [1600, 600],
            [1550, 600],
            [1500, 600],
            [1450, 600],
            [1450, 550],
            [1750, 550],
            [1296, 550],
            [1296, 650],
            [1246, 650],
            [1196, 650],
            [1146, 650],
            [1100, 650],
            [1300, 200],
            [1250, 200],
            [1200, 200],
            [1150, 200],
            [1100, 200],
            [1300, 300],
            [1300, 400],
            [1850, 750],
            [1800, 750],
            [1750, 750],
            [1700, 750],
            [1650, 750],
            [1750, 800],
            [1500, 750],
            [1450, 750],
            [1500, 650],
            [1450, 650],
            [1450, 800],
            [1100, 600],
            [1050, 600],
            [1000, 600],
            [950, 600],
            [900, 600],
            [850, 600],
            [800, 600],
            [750, 600],
            [700, 600],
            [650, 600],
            [600, 600],
            [550, 600],
            [500, 600],
            [350, 600],
            [300, 600],
            [250, 600],
            [200, 600],
            [250, 500],
            [200, 500],
            [250, 400],
            [200, 400],
            [250, 300],
            [200, 300],
            [300, 300],
            [200, 500],
            [300, 250],
            [300, 100],
            [150, 300],
            [100, 300],
            [150, 350],
            [100, 350],
            [100, 750],
            [150, 750],
            [200, 750],
            [250, 750],
            [300, 750],
            [350, 750],
            [400, 750],
            [450, 750],
            [500, 750],
            [550, 750],
            [550, 700],
            [100, 800],
            [150, 800],
            [100, 850],
            [450, 450],
            [500, 450],
            [550, 450],
            [600, 450],
            [450, 350],
            [450, 250],
            [450, 200],
            [500, 200],
            [550, 200],
            [600, 200],
            [600, 100],
            [600, 350],
            [750, 150],
            [750, 250],
            [750, 350],
            [750, 450],
            [800, 100],
            [800, 450],
            [850, 450],
            [800, 400],
            [850, 400],
            [900, 400],
            [900, 350],
            [950, 350],
            [1000, 350],
            [1050, 350],
            [1100, 350],
            [1150, 350],
            [1050, 450],
            [1100, 450],
            [1150, 450],
            [950, 300],
            [950, 200],
            [950, 1000],
            [900, 1000],
            [1000, 1000],
            [1046, 1000],
            [1046, 900],
            [1046, 800],
            [1000, 800],
            [950, 800],
            [900, 800],
            [850, 750],
            [850, 850],
            [700, 750],
            [700, 850],
            [700, 900],
            [650, 900],
            [600, 900],
            [550, 900],
            [500, 900],
            [450, 900],
            [400, 900],
            [350, 900],
            [350, 950],
            [300, 950],
            [300, 1000],
            [250, 1000],
            [200, 1000],
            [250, 1100],
            [250, 1200],
            [250, 1250],
            [200, 1250],
            [300, 1200],
            [350, 1200],
            [400, 1200],
            [450, 1200],
            [500, 1200],
            [300, 1150],
            [350, 1150],
            [400, 1150],
            [450, 1150],
            [500, 1150],
            [450, 1100],
            [550, 1100],
            [600, 1100],
            [650, 1100],
            [700, 1100],
            [500, 1050],
            [550, 1050],
            [600, 1050],
            [650, 1050],
            [700, 1050],
            [500, 1350],
            [450, 1350],
            [400, 1350],
            [650, 1150],
            [650, 1250],
            [650, 1350],
            [700, 1150],
            [700, 1250],
            [700, 1350],
            [850, 1250],
            [850, 1350],
            [900, 1250],
            [950, 1250],
            [1000, 1250],
            [1050, 1250],
            [1100, 1250],
            [1450, 1250],
            [1500, 1250],
            [1550, 1250],
            [1600, 1250],
            [1650, 1250],
            [1700, 1250],
            [1750, 1250],
            [1750, 1350],
            [1250, 1350],
            [1300, 1350],
            [1200, 1200],
            [1150, 1200],
            [1100, 1200],
            [1050, 1200],
            [1350, 1200],
            [1400, 1200],
            [1450, 1200],
            [1450, 1200],
            [1200, 900],
            [1200, 800],
            [1300, 800],
            [1200, 1000],
            [1250, 900],
            [1250, 800],
            [1250, 1000],
            [900, 1050],
            [850, 1050],
            [850, 1100],
            [950, 1050],
            [1450, 1050],
            [1400, 1000],
            [1400, 950],
            [1450, 950],
            [1500, 950],
            [1550, 950],
            [1600, 950],
            [1650, 950],
            [1700, 950],
            [1750, 950],
            [1750, 1000],
            [1750, 1100],
            [1700, 1100],
            [1650, 1100],
            [1600, 1100],

            # левая часть стен
            [50, 100],
            [50, 150],
            [50, 200],
            [50, 250],
            [50, 300],
            [50, 350],
            [50, 400],
            [50, 450],
            [50, 500],
            [50, 550],
            [50, 600],
            [50, 650],
            [50, 700],
            [50, 750],
            [50, 800],
            [50, 850],
            [50, 900],
            [50, 950],
            [50, 1000],
            [50, 1050],
            [50, 1100],
            [50, 1150],
            [50, 1200],
            [50, 1250],
            [50, 1300],
            [50, 1350],

            # правая часть стен
            [1900, 100],
            [1900, 150],
            [1900, 200],
            [1900, 250],
            [1900, 300],
            [1900, 350],
            [1900, 400],
            [1900, 450],
            [1900, 500],
            [1900, 550],
            [1900, 600],
            [1900, 650],
            [1900, 700],
            [1900, 750],
            [1900, 800],
            [1900, 850],
            [1900, 900],
            [1900, 950],
            [1900, 1000],
            [1900, 1050],
            [1900, 1100],
            [1900, 1150],
            [1900, 1200],
            [1900, 1250],
            [1900, 1300],
            [1900, 1350],

            # верхняя часть стен
            [100, 50],
            [150, 50],
            [200, 50],
            [250, 50],
            [300, 50],
            [350, 50],
            [400, 50],
            [450, 50],
            [500, 50],
            [550, 50],
            [600, 50],
            [650, 50],
            [700, 50],
            [750, 50],
            [800, 50],
            [850, 50],
            [800, 50],
            [850, 50],
            [900, 50],
            [950, 50],
            [1000, 50],
            [1050, 50],
            [1100, 50],
            [1150, 50],
            [1200, 50],
            [1250, 50],
            [1300, 50],
            [1350, 50],
            [1400, 50],
            [1450, 50],
            [1500, 50],
            [1550, 50],
            [1600, 50],
            [1650, 50],
            [1700, 50],
            [1750, 50],
            [1800, 50],
            [1850, 50],

            # нижняя часть стен

            [100, 1400],
            [150, 1400],
            [200, 1400],
            [250, 1400],
            [300, 1400],
            [350, 1400],
            [400, 1400],
            [450, 1400],
            [500, 1400],
            [550, 1400],
            [600, 1400],
            [650, 1400],
            [700, 1400],
            [750, 1400],
            [800, 1400],
            [850, 1400],
            [800, 1400],
            [850, 1400],
            [900, 1400],
            [950, 1400],
            [1000, 1400],
            [1050, 1400],
            [1100, 1400],
            [1150, 1400],
            [1200, 1400],
            [1250, 1400],
            [1300, 1400],
            [1350, 1400],
            [1400, 1400],
            [1450, 1400],
            [1500, 1400],
            [1550, 1400],
            [1600, 1400],
            [1650, 1400],
            [1700, 1400],
            [1750, 1400],
            [1800, 1400],
            [1850, 1400],
        ]

        for wall in walls:
            block = Platform()
            block.rect.x = wall[0]
            block.rect.y = wall[1]
            settings.platform_list.add(block)

        settings.ground_surf = pygame.image.load('background/sandfon3.jpg').convert_alpha()
        player.rect.x = 1825
        player.rect.y = 125
        # установка шипов
        stingers = [[1200, 100], [700, 100], [1270, 250], [1720, 250], [1600, 170], [860, 250], [1420, 370],
                    [1570, 470], [1210, 620], [950, 420], [800, 500], [650, 420], [420, 460], [300, 530],
                    [350, 300], [490, 100], [250, 720], [100, 500], [350, 800], [720, 720], [1000, 650], [350, 1000],
                    [600, 950], [590, 1370], [100, 1370], [100, 1130], [460, 1250], [1285, 1320], [1100, 1300],
                    [1490, 1370], [970, 1100], [1100, 1170], [750, 1190], [1450, 1100], [1250, 1050], [1650, 1220],
                    [1870, 1000], [1800, 500], [1600, 920], [1350, 620], [820, 820], [1100, 920]]

        for stin in stingers:
            stinger = Stinger(camera_group)
            stinger.rect.x = stin[0]
            stinger.rect.y = stin[1]

            settings.stinger_list.add(stinger)

        settings.stinger_damage = 25

        settings.ghost_damage = 1000

    def update(self):
        global ghost

        if self.count_switch is True:
            for i in range(settings.second_enemy_count):
                ghost = Ghost('items/whiteghost.png', camera_group)
                settings.enemy_list.add(ghost)

            self.count_switch = False
        settings.platform_list.update()

    @staticmethod
    def draw(screen):
        settings.platform_list.draw(screen)


# Звук
class Music:
    def __init__(self):
        self.music_playing = True

        self.sound = pygame.mixer.Sound("music/beg.mp3")
        self.scroll_sound = pygame.mixer.Sound("music/itemtaked.mp3")
        self.ghost_smeh = pygame.mixer.Sound("music/ghost.mp3")
        self.backsound = pygame.mixer.Sound("music/secondbackground.mp3")
        self.hit = pygame.mixer.Sound("music/damage/bol1.mp3")
        self.finalhit = pygame.mixer.Sound("music/damage/finalbol.mp3")
        self.taked_item = pygame.mixer.Sound("music/take.mp3")
        self.drink = pygame.mixer.Sound("music/drink.mp3")
        self.gameoversound = pygame.mixer.Sound('music/gameoversound.mp3')
        self.menumusic = pygame.mixer.Sound('music/menumusic.mp3')
        self.startmenumusic = pygame.mixer.Sound('music/startmenumusic.mp3')
        self.finalmusic = pygame.mixer.Sound('music/finalmusic.mp3')

        self.button_cliked = pygame.mixer.Sound('music/clicked.mp3')

        self.sound.set_volume(0.02)
        self.ghost_smeh.set_volume(0.05)
        self.scroll_sound.set_volume(0.05)
        self.drink.set_volume(0.05)
        self.taked_item.set_volume(0.05)
        self.gameoversound.set_volume(0.1)
        self.menumusic.set_volume(0.2)
        self.startmenumusic.set_volume(0.2)
        self.backsound.set_volume(0.05)
        self.finalmusic.set_volume(0.05)
        self.finalhit.set_volume(0.05)
        self.button_cliked.set_volume(0.02)

    def damage_sound_update(self):
        damage_sound = random.choice([1, 2, 3, 4, 5, 6, 7, 8])

        self.hit = pygame.mixer.Sound(f"music/damage/bol{damage_sound}.mp3")
        self.hit.set_volume(0.1)


# Секундомер
class Timer:
    def __init__(self):
        self.temp = 0
        self.f_temp = None

    # таймер
    def tick(self):
        self.f_temp = datetime.utcfromtimestamp(self.temp).strftime("%H:%M:%S")
        self.temp += 1

        if self.f_temp == '01:00:00':
            settings.bad_time_points = 85

        elif self.f_temp == '02:00:00':
            settings.bad_time_points = 70

        elif self.f_temp == '03:00:00':
            settings.bad_time_points = 55

        elif self.f_temp == '04:00:00':
            settings.bad_time_points = 40

        elif self.f_temp == '05:00:00':
            settings.bad_time_points = 0


# Секундомер Музыки
class MusicTimer:
    def __init__(self):
        self.t = 0
        self.t2 = 0
        self.t3 = 0
        self.t4 = 0
        self.f = None
        self.backmusic_count = 1
        self.start_count = 1
        self.pause_count = 1
        self.final_count = 1

    # таймер
    def tick_1(self):
        self.t += 1

        if datetime.utcfromtimestamp(self.t).strftime("%H:%M:%S") == '10:00:00':
            music.backsound.stop()
            self.t = 0
            self.backmusic_count = 1

    def tick_2(self):
        self.t2 += 1

        if datetime.utcfromtimestamp(self.t2).strftime("%H:%M:%S") == '03:10:00':
            music.startmenumusic.stop()
            self.t2 = 0
            self.start_count = 1

    def tick_3(self):
        self.t3 += 1

        if datetime.utcfromtimestamp(self.t3).strftime("%H:%M:%S") == '02:56:00':
            music.menumusic.stop()
            self.t3 = 0
            self.pause_count = 1

    def tick_4(self):
        self.t4 += 1

        if datetime.utcfromtimestamp(self.t4).strftime("%H:%M:%S") == '04:09:00':
            music.finalmusic.stop()
            self.t4 = 0
            self.final_count = 1


tem1 = 0
tem2 = 0
tem3 = 0

musictimer = MusicTimer()


# Запуск игры
def play():
    menu_image = random.choice([1, 2, 3, 4, 5, 6])

    global tem1, tem2, tem3
    music.startmenumusic.stop()
    while True:
        music.damage_sound_update()

        musictimer.tick_1()
        if musictimer.backmusic_count == 1:
            music.backsound.play()
            musictimer.backmusic_count -= 1

        if settings.startmenu is True:
            music.backsound.set_volume(0)

            if settings.startmenu_state == 'main':
                screen.blit(pygame.image.load(f'background/startmenu/DD_bg{menu_image}.jpg').convert_alpha(), (0, 0))
                tem1 += 1

                if datetime.utcfromtimestamp(tem1).strftime("%H:%M:%S") == '00:07:00':
                    settings.startmenu_state = 'startmenu'

            if settings.startmenu_state == 'floor_1':
                settings.game_paused = False
                music.startmenumusic.stop()
                if settings.change_level_1 == 1:
                    screen.blit(pygame.image.load(f'background/floor_1/Floor1_{random.choice([1, 2, 3, 4, 5])}.jpg').
                                convert_alpha(), (0, 0))
                    settings.change_level_1 = 0
                tem2 += 1

                if datetime.utcfromtimestamp(tem2).strftime("%H:%M:%S") == '00:07:00':
                    settings.startmenu = False

            if settings.startmenu_state == 'floor_2':
                settings.game_paused = False
                music.ghost_smeh.stop()
                music.sound.stop()
                music.drink.stop()
                music.hit.stop()
                if settings.change_level_2 == 1:
                    screen.blit(pygame.image.load(f'background/floor_2/Floor2_{random.choice([1, 2, 3, 4, 5])}.jpg').
                                convert_alpha(), (0, 0))
                    settings.change_level_2 = 0
                tem3 += 1

                if datetime.utcfromtimestamp(tem3).strftime("%H:%M:%S") == '00:07:00':
                    settings.startmenu = False

            # elif settings.startmenu_state == 'main_2':
            #     screen.blit(pygame.image.load('background/start1.jpg').convert_alpha(), (0, 0))
            #     if settings.pass_button.draw(screen):
            #         if settings.con:
            #             settings.startmenu_state = 'startmenu'
            #     if settings.readmore_button.draw(screen):
            #         settings.startmenu_state = 'main_3'
            #         settings.con = False
            #
            #     else:
            #         settings.con = True
            #
            # elif settings.startmenu_state == 'main_3':
            #     screen.blit(pygame.image.load('background/start2.jpg').convert_alpha(), (0, 0))
            #     if settings.continue_button.draw(screen):
            #         if settings.con:
            #             settings.startmenu_state = 'startmenu'
            #     if settings.comeback_button.draw(screen):
            #         settings.startmenu_state = 'main_2'
            #         settings.con = False
            #
            #     else:
            #         settings.con = True

            if settings.startmenu_state == 'startmenu':
                musictimer.tick_2()

                if musictimer.start_count == 1:
                    music.startmenumusic.play()
                    musictimer.start_count -= 1

                screen.blit(pygame.image.load('background/startmenu/DD_bg_menu.jpg').convert_alpha(), (0, 0))

                if settings.newgame_button.draw(screen):
                    music.button_cliked.play()
                    settings.startmenu_state = 'floor_1'

                if settings.aboutgame_button.draw(screen):
                    music.button_cliked.play()
                    settings.startmenu_state = 'about'

                # if settings.prekwil_button.draw(screen):
                #     settings.startmenu_state = 'main_2'

                if settings.exit_button.draw(screen):
                    music.button_cliked.play()
                    pygame.quit()
                    sys.exit()

            if settings.startmenu_state == 'about':
                screen.blit(pygame.image.load('background/startmenu/aboutthegame.jpg').convert_alpha(), (0, 0))

                if settings.items_button.draw(screen):
                    if not settings.con:
                        music.button_cliked.play()
                        settings.startmenu_state = 'items'

                elif settings.enemy_button.draw(screen):
                    if not settings.con:
                        music.button_cliked.play()
                        settings.startmenu_state = 'enemy'

                elif settings.inmenu_button.draw(screen):
                    if not settings.con:
                        music.button_cliked.play()
                        settings.startmenu_state = 'startmenu'

                settings.con = False

            if settings.startmenu_state == 'items':
                screen.blit(pygame.image.load('background/pause/items1.jpg').convert_alpha(), (0, 0))

                if settings.pass_button.draw(screen):

                    if settings.con:
                        music.button_cliked.play()
                        settings.startmenu_state = 'about'

                if settings.readmore_button.draw(screen):
                    music.button_cliked.play()
                    settings.startmenu_state = 'items_2'
                    settings.con = False

                else:
                    settings.con = True

            if settings.startmenu_state == 'items_2':
                screen.blit(pygame.image.load('background/pause/items2.jpg').convert_alpha(), (0, 0))

                if settings.continue_button.draw(screen):

                    if settings.con:
                        music.button_cliked.play()
                        settings.startmenu_state = 'about'

                if settings.comeback_button.draw(screen):
                    music.button_cliked.play()
                    settings.startmenu_state = 'items'
                    settings.con = False

                else:
                    settings.con = True

            if settings.startmenu_state == 'enemy':
                screen.blit(pygame.image.load('background/pause/enemyphon.jpg').convert_alpha(), (0, 0))

                if settings.back_button.draw(screen):
                    music.button_cliked.play()
                    settings.startmenu_state = 'about'
                    settings.con = True

                else:
                    settings.con = False

        elif settings.game_paused is True:
            music.backsound.set_volume(0)

            musictimer.tick_3()
            if musictimer.pause_count == 1:
                music.menumusic.play()
                musictimer.pause_count -= 1

            if settings.menu_state == "main":
                screen.blit(pygame.image.load('background/pause/pauseimage2.jpg').convert_alpha(), (0, 0))

                if settings.resume_button.draw(screen):
                    music.button_cliked.play()
                    settings.game_paused = False

                if settings.options_button.draw(screen):
                    music.button_cliked.play()
                    settings.menu_state = "options"

                if settings.startmenu_button.draw(screen):
                    music.button_cliked.play()
                    restart()

                if settings.quit_button.draw(screen):
                    music.button_cliked.play()

                    if settings.quit_the_game is True:
                        pygame.quit()
                        sys.exit()

                settings.quit_the_game = True

                for event in pygame.event.get():

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            settings.game_paused = False

            # текст, описывающий цель игры
            if settings.menu_state == "options":
                screen.blit(pygame.image.load('background/pause/aboutthegame.jpg').convert_alpha(), (0, 0))

                if settings.items_button.draw(screen):

                    if not settings.quit_the_game:
                        music.button_cliked.play()
                        settings.menu_state = 'items'

                elif settings.enemy_button.draw(screen):

                    if not settings.quit_the_game:
                        music.button_cliked.play()
                        settings.menu_state = 'enemy'

                elif settings.back_button.draw(screen):

                    if not settings.quit_the_game:
                        music.button_cliked.play()
                        settings.menu_state = 'main'

                settings.quit_the_game = False

                for event in pygame.event.get():

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            settings.menu_state = 'main'

            # текст описания предметов
            if settings.menu_state == 'items':
                screen.blit(pygame.image.load('background/pause/items1.jpg').convert_alpha(), (0, 0))

                if settings.pass_button.draw(screen):

                    if settings.quit_the_game:
                        music.button_cliked.play()
                        settings.menu_state = 'options'

                if settings.readmore_button.draw(screen):
                    music.button_cliked.play()
                    settings.menu_state = 'items_2'
                    settings.quit_the_game = False

                else:
                    settings.quit_the_game = True

            if settings.menu_state == 'items_2':
                screen.blit(pygame.image.load('background/pause/items2.jpg').convert_alpha(), (0, 0))

                if settings.continue_button.draw(screen):

                    if settings.quit_the_game:
                        music.button_cliked.play()
                        settings.menu_state = 'options'

                if settings.comeback_button.draw(screen):
                    music.button_cliked.play()
                    settings.menu_state = 'items'
                    settings.quit_the_game = False

                else:
                    settings.quit_the_game = True

            if settings.menu_state == 'enemy':
                screen.blit(pygame.image.load('background/pause/enemyphon.jpg').convert_alpha(), (0, 0))

                if settings.back_button.draw(screen):
                    music.button_cliked.play()
                    settings.menu_state = 'options'

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            settings.menu_state = 'options'

        elif settings.end_the_game is True:
            player.player_speed = 0

            if settings.death_music_count == 1:
                music.hit.stop()
                music.finalhit.play()
                settings.death_music_count = 0

            settings.temp += 1
            if datetime.utcfromtimestamp(settings.temp).strftime("%H:%M:%S") == '00:02:00':
                settings.death_count = 1

            if settings.death_count == 1:

                screen.blit(pygame.image.load('background/deathimage.jpg').convert_alpha(), (0, 0))
                music.backsound.set_volume(0)
                music.sound.stop()
                music.scroll_sound.stop()
                music.ghost_smeh.stop()
                music.hit.stop()
                music.taked_item.stop()
                music.drink.stop()
                music.menumusic.stop()
                music.gameoversound.play()

                player.kill()

                draw_the_text('YOU DIED', pygame.font.SysFont("garamond", 160), (139, 0, 0),
                              SCREEN_WIDTH / 2, 220, 2)

                if settings.quitlost_button.draw(screen):
                    music.button_cliked.play()
                    pygame.quit()
                    sys.exit()

                if settings.playagainlost_button.draw(screen):
                    music.button_cliked.play()
                    restart()
                    settings.startmenu = True
                    settings.startmenu_state = 'floor_1'

                if settings.startmenu_lost_button.draw(screen):
                    music.button_cliked.play()
                    restart()

        # текст меню, при победе
        elif settings.game_win is True:
            music.finalmusic.play(loops=0)
            music.sound.stop()
            music.scroll_sound.stop()
            music.ghost_smeh.stop()
            music.hit.stop()
            music.taked_item.stop()
            music.drink.stop()
            music.backsound.set_volume(0)
            screen.blit(pygame.image.load('background/winimage4.jpg').convert_alpha(), (0, 0))
            draw_the_text("Вы выбрались.", pygame.font.SysFont("arialblack", 50),
                          (200, 200, 200),
                          SCREEN_WIDTH / 2, 30, 2)

            draw_the_text(f"Игра пройдена за {timer.f_temp} - {round(settings.bad_time_points, 1)}"
                          f"/{round(settings.points_by_time, 1)} очков",
                          pygame.font.SysFont("arialblack", 36),
                          (200, 200, 200),
                          SCREEN_WIDTH / 2, 250, 2)

            draw_the_text(f"Найдено предметов: {settings.items} - {round(settings.items_inventory, 1)}"
                          f"/{round(settings.point_per_item * 2, 1)} очков",
                          pygame.font.SysFont("arialblack", 36),
                          (200, 200, 200),
                          SCREEN_WIDTH / 2, 310, 2)

            draw_the_text(
                f"Оставшееся здоровье: {player.player_health} - {round(settings.bad_health_points, 1)}"
                f"/{round(settings.health_points, 1)} очков",
                pygame.font.SysFont("arialblack", 36),
                (200, 200, 200),
                SCREEN_WIDTH / 2, 370, 2)

            draw_the_text(f"Всего очков: {round(settings.points, 1)}/{round(settings.max_points, 1)}",
                          pygame.font.SysFont("arialblack", 45),
                          (200, 200, 200),
                          SCREEN_WIDTH / 2, 460, 2)

            quit_button = button.Button(SCREEN_WIDTH / 1.4, 600, pygame.image.load("buttons/exitthegame.png").
                                        convert_alpha(), 1)

            startmenu_button = button.Button(SCREEN_WIDTH / 2.6, 600, pygame.image.load("buttons/startmenu.png").
                                             convert_alpha(), 1)

            playagain = button.Button(SCREEN_WIDTH / 19, 600, pygame.image.load("buttons/playagain.png").
                                      convert_alpha(), 1)

            if quit_button.draw(screen):
                music.button_cliked.play()
                pygame.quit()
                sys.exit()

            if playagain.draw(screen):
                music.button_cliked.play()
                restart()
                settings.startmenu = True
                settings.startmenu_state = 'floor_1'

            if startmenu_button.draw(screen):
                music.button_cliked.play()
                restart()

        else:
            tem1, tem2, tem3 = 0, 0, 0

            music.backsound.set_volume(0.2)
            settings.quit_the_game = True
            music.startmenumusic.stop()
            music.menumusic.stop()

            musictimer.pause_count = 1
            musictimer.t3 = 0

            if settings.end_the_game is not True:
                timer.tick()

            player.player_moving()

            settings.active_sprite_list.update()

            settings.current_level.update()

            settings.current_level.draw(screen)
            settings.active_sprite_list.draw(screen)

            camera_group.update()
            camera_group.custom_draw(player)

            # поясняющий текст в игре
            if settings.end_the_game is False:
                draw_the_text(f'{timer.f_temp}', pygame.font.SysFont("arialblack", 30),
                              (70, 70, 70),
                              SCREEN_WIDTH / 1.01, 10, 3)

                draw_the_text(f"HP: {player.player_health}", pygame.font.SysFont("arialblack", 30),
                              (200, 0, 0),
                              10, 10, 1)

                draw_the_text(f'Скорость - {settings.player_speed_procent}%', pygame.font.SysFont("arialblack", 20),
                              (150, 150, 150),
                              10, 600, 1)

                draw_the_text(f'Защита от шипов - {stinger.protect_procent}%', pygame.font.SysFont("arialblack", 20),
                              (150, 150, 150),
                              10, 630, 1)

                draw_the_text(f'Защита от призрака - {settings.ghost_protect_procent}%',
                              pygame.font.SysFont("arialblack", 20),
                              (150, 150, 150),
                              10, 660, 1)

            settings.game_over()

            # взятие книги
            if scroll.rect.x - 50 < player.rect.x < scroll.rect.x + 50 and scroll.rect.y - 50 < player.rect.y \
                    < scroll.rect.y + 50:
                scroll.picked()
            # взятие зелья, нагрудника, ботинов, фонаря
            if accesouar.rect.x - 60 < player.rect.x < accesouar.rect.x + 60 and accesouar.rect.y - 60 < \
                    player.rect.y < accesouar.rect.y + 60:
                accesouar.picked()
            # перемещение в портале
            if portal.rect.x - 40 < player.rect.x < portal.rect.x + 40 and portal.rect.y - 40 < player.rect.y \
                    < portal.rect.y + 40:
                portal.used()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if settings.game_win is False and settings.end_the_game is False:
                        settings.game_paused = True
                    else:
                        settings.game_paused = False

            if event.type == pygame.KEYUP:
                player.GorizontalWalking = False

        clock.tick(60)
        pygame.display.flip()


# рисование
def draw_the_text(text, font, text_col, x, y, flag):
    text_surface = font.render(text, True, text_col)
    text_rect = text_surface.get_rect()

    if flag == 1:
        text_rect.topleft = (x, y)
    elif flag == 2:
        text_rect.midtop = (x, y)
    elif flag == 3:
        text_rect.topright = (x, y)

    screen.blit(text_surface, text_rect)


# перезапуск игры
def restart():
    global player, scroll, accesouar, portal, ghost, stinger, shadow

    settings.startmenu = True
    settings.startmenu_state = 'startmenu'
    musictimer.start_count = 1
    musictimer.t2 = 0

    settings.change_level_1 = 1
    settings.change_level_2 = 1

    settings.player_speed_procent = 100

    settings.death_count = 0

    settings.stinger_damage = 50

    settings.items = 0
    settings.temp = 0
    settings.death_music_count = 1

    settings.menu_state = "main"

    shadow.kill()
    shadow = Shadow('blackphon1.png', camera_group)
    shadow.kill()

    player.player_health = 100
    player.player_speed = 3.5

    settings.bad_time_points = 100

    settings.items_inventory = 0
    settings.bad_health_points = 0
    settings.max_points = 0

    timer.temp = 0

    settings.end_the_game = False
    settings.game_paused = False
    settings.game_win = False

    settings.armor = False
    settings.boots = False

    settings.change_accessouars_list = False
    player.kill()
    player = Player('playerimage/right/main.png', (750, 850), camera_group)
    scroll.kill()
    scroll = MagicScroll(1, camera_group)
    portal.kill()
    portal = Portal('items/prozwall.png', camera_group)
    accesouar.kill()
    accesouar = Accessories(camera_group)

    stinger.protect_procent = 0
    settings.ghost_protect_procent = 0

    settings.ground_surf = pygame.image.load('background/pol3.jpg').convert_alpha()

    music.sound.stop()
    music.scroll_sound.stop()
    music.ghost_smeh.stop()
    music.backsound.play()
    music.hit.stop()
    music.taked_item.stop()
    music.drink.stop()
    music.gameoversound.stop()
    music.menumusic.stop()
    music.startmenumusic.stop()
    music.finalmusic.stop()

    settings.floor = 1

    for sprite in settings.enemy_list.sprites():
        sprite.kill()

    if FirstFloor().count_switch is True:
        for i in range(settings.first_enemy_count):
            ghost = Ghost('items/whiteghost.png', camera_group)
            settings.enemy_list.add(ghost)

        FirstFloor().count_switch = False
    settings.platform_list.update()

    for sprite in settings.stinger_list.sprites():
        sprite.kill()

    for sprite in settings.platform_list.sprites():
        sprite.kill()

    settings.levellist.append(FirstFloor())
    settings.current_level = settings.levellist[0]


camera_group = CameraGroup()

player = Player('playerimage/right/main.png', (750, 850), camera_group)
shadow = Shadow('blackphon1.png', camera_group)
scroll = MagicScroll(1, camera_group)
portal = Portal('items/prozwall.png', camera_group)
music = Music()
timer = Timer()
accesouar = Accessories(camera_group)
stinger = Stinger(camera_group)
ghost = Ghost('items/whiteghost.png', camera_group)
ghost.kill()
clock = pygame.time.Clock()

TEXT_COL = (255, 255, 255)

settings.levellist.append(FirstFloor())
settings.current_level = settings.levellist[0]

# запуск кода
if __name__ == '__main__':
    play()
