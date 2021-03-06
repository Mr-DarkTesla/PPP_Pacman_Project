import pygame
import os
import sys


pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
FPS = 24
level_names = ["map.txt", "map2.txt", "map3.txt"]

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if color_key is not None:
        image = pygame.image.load(fullname).convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = pygame.image.load(fullname).convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return [list(i) for i in list(map(lambda x: x.ljust(max_width, '-'), level_map))]


def terminate():
    pygame.quit()
    sys.exit()


def valid_coord(x, y):
    return game_map[y % level_y][x % level_x] != '#'


def get_ch(x, y):
    return game_map[y % level_y][x % level_x]


def change_ch(x, y, ch):
    game_map[y % level_y][x % level_x] = ch





def game_over_screen():
    background = pygame.transform.scale(load_image('wasted.png'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_main_menu(screen)

def game_over_screen1():
    line = "You lose!"
    font = pygame.font.Font(None, 100)
    screen.fill((0, 0, 0))
    io = 'white'
    string_rendered = font.render(line, True, pygame.Color(io))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = HEIGHT / 2 - intro_rect.height / 2
    intro_rect.x = WIDTH / 2 - intro_rect.width / 2
    screen.blit(string_rendered, intro_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            terminate()


def game_win_screen():
    global eat_cnt
    line = "You win!"
    font = pygame.font.Font(None, 100)
    screen.fill((0, 0, 0))
    io = 'white'
    string_rendered = font.render(line, True, pygame.Color(io))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = HEIGHT / 2 - intro_rect.height / 2
    intro_rect.x = WIDTH / 2 - intro_rect.width / 2
    screen.blit(string_rendered, intro_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            eat_cnt = 1
            start_main_menu(screen)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_y, tile_height * pos_x)
        # self.sprite = pygame.sprite.Sprite()
        # self.sprite.image = self.image
        # self.sprite.rect = self.rect
        # all_sprites.add(self.sprite)
        # tiles_group.add(self.sprite)
        # all_sprites.remove(list(all_sprites)[-1])
        # tiles_group.remove(list(tiles_group)[-1])


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(player_image, 3, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.img_right = self.frames
        self.img_left = [pygame.transform.flip(image, True, False) for image in self.img_right]
        self.img_up = [pygame.transform.rotate(image, 90) for image in self.img_right]
        self.img_down = [pygame.transform.flip(image, False, True) for image in self.img_up]
        self.rect = self.rect.move(tile_width * pos_y + 5, tile_height * pos_x + 4)
        self.pos = [pos_y, pos_x]
        self.d_pos = [0, 0]
        self.dir = [0, 0]
        self.current_time = 0
        self.anim_time = 1

        sprite = pygame.sprite.Sprite()
        sprite.image = self.image
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        sprite.rect = self.rect
        all_sprites.add(sprite)
        player_group.add(sprite)
        player_group.remove(list(player_group)[-1])
        all_sprites.remove(list(all_sprites)[-1])

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def go(self, event):
        global eat_cnt
        p_x, p_y = self.pos
        self.d_pos = [0, 0]
        ch = None
        if event.key == pygame.K_UP:  # up
            ch = get_ch(p_x, p_y - 1)
            if ch in '.-':
                self.d_pos[1] -= 1
        elif event.key == pygame.K_DOWN:  # down
            ch = get_ch(p_x, p_y + 1)
            if ch in '.-':
                self.d_pos[1] += 1
        elif event.key == pygame.K_RIGHT:  # right
            ch = get_ch(p_x + 1, p_y)
            if ch in '.-':
                self.d_pos[0] += 1
        elif event.key == pygame.K_LEFT:  # left
            ch = get_ch(p_x - 1, p_y)
            if ch in '.-':
                self.d_pos[0] -= 1
        elif event.key == pygame.K_1:
            eat_cnt = 0
        if ch is not None and self.d_pos != [0, 0]:
            if ch == '.':
                eat_cnt -= 1
                xx, yy = (p_x + player.d_pos[0]) % level_x, (p_y + player.d_pos[1]) % level_y
                all_sprites.remove(game_spr_map[xx][yy])
                tiles_group.remove(game_spr_map[xx][yy])
                game_spr_map[xx][yy].kill()
                game_spr_map[xx][yy] = Tile('empty', yy, xx)
            change_ch(p_x, p_y, '-')
            change_ch(p_x + self.d_pos[0], p_y + self.d_pos[1], '@')
        self.dir = self.d_pos

    def update(self, delta_time):
            if self.d_pos[0] > 0:
                self.frames = self.img_right
            elif self.d_pos[0] < 0:
                self.frames = self.img_left
            elif self.d_pos[1] > 0:
                self.frames = self.img_down
            elif self.d_pos[1] < 0:
                self.frames = self.img_up

            dy, dx = 0, 0

            self.pos[0] += self.d_pos[0]
            self.pos[1] += self.d_pos[1]

            if self.pos[0] < 0:
                self.pos[0] = level_x - 1
                dx = level_x * tile_width
            if self.pos[1] < 0:
                self.pos[1] = level_y - 1
                dy = level_y * tile_height
            if self.pos[0] >= level_x:
                self.pos[0] = 0
                dx = -level_x * tile_width
            if self.pos[1] >= level_y:
                self.pos[1] = 0
                dy = level_y * tile_height

            self.rect.move_ip(self.d_pos[0] * tile_width + dx, self.d_pos[1] * tile_height + dy)

            self.d_pos = [0, 0]
            self.current_time += delta_time
            if self.current_time >= self.anim_time:
                self.current_time = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)

            self.image = self.frames[self.cur_frame]


class Spirit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, color, ind):
        global speedy_ind
        super().__init__(player_group, all_sprites)
        self.frames = []
        image = load_image('sprt.png')
        self.cut_sheet(image, 8, 4, color)
        self.color = color
        self.image = self.frames[0]
        self.img_right = self.frames[0]
        self.img_left = self.frames[2]
        self.img_up = self.frames[4]
        self.img_down = self.frames[6]
        self.rect = self.rect.move(tile_width * pos_y + 5, tile_height * pos_x + 4)
        self.pos = [pos_y, pos_x]
        self.prev_pos = [-1, -1]
        self.is_active = False
        self.d_pos = [0, 0]
        self.current_time = 0
        self.anim_time = 2.5

        if color % 4 == 0:
            self.select_point = self.point_to0
            self.run_up = [20, -1]
            speedy_ind = ind
            self.is_active = True
        elif color % 4 == 1:
            self.select_point = self.point_to1
            self.run_up = [-1, -1]
            self.is_active = True
        elif color % 4 == 2:
            self.select_point = self.point_to2
            self.run_up = [20, 20]
        elif color % 4 == 3:
            self.select_point = self.point_to3
            self.run_up = [-1, 20]
        self.point_to = self.run_up

        sprite = pygame.sprite.Sprite()
        sprite.image = self.image
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        sprite.rect = self.rect
        all_sprites.add(sprite)
        player_group.add(sprite)
        player_group.remove(list(player_group)[-1])
        all_sprites.remove(list(all_sprites)[-1])

    def cut_sheet(self, sheet, columns, rows, color):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(columns):
            frame_location = (self.rect.w * i, self.rect.h * color)
            self.frames.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self, delta_time):
        if not self.is_active:
            return

        global game_state
        self.current_time += delta_time
        if self.current_time >= self.anim_time:
            self.current_time = 0
            self.go()
            self.prev_pos[0] = self.pos[0]
            self.prev_pos[1] = self.pos[1]
            self.pos[0] += self.d_pos[0]
            self.pos[1] += self.d_pos[1]

            if get_ch(*self.pos) == '@' or get_ch(*self.prev_pos) == '@':
                game_state = 3

            if self.d_pos[0] > 0:
                self.image = self.img_right
            elif self.d_pos[0] < 0:
                self.image = self.img_left
            elif self.d_pos[1] > 0:
                self.image = self.img_down
            elif self.d_pos[1] < 0:
                self.image = self.img_up

            dx, dy = 0, 0
            if self.pos[0] < 0:
                self.pos[0] = level_x - 1
                dx = level_x * tile_width
            if self.pos[1] < 0:
                self.pos[1] = level_y - 1
                dy = level_y * tile_height
            if self.pos[0] >= level_x:
                self.pos[0] = 0
                dx = -level_x * tile_width
            if self.pos[1] >= level_y:
                self.pos[1] = 0
                dy = level_y * tile_height
            self.rect.move_ip(self.d_pos[0] * tile_width + dx, self.d_pos[1] * tile_height + dy)
            self.d_pos = [0, 0]

    def go(self):
        if get_ch(*self.pos) in list('0123'):
            self.point_to = [7, 8]
        goes = [(self.pos[0] - 1, self.pos[1]), (self.pos[0] + 1, self.pos[1]), (self.pos[0], self.pos[1] - 1), (self.pos[0], self.pos[1] + 1)]
        invalid = set()
        invalid.add((self.prev_pos[0], self.prev_pos[1]))
        for i in goes:
            if not valid_coord(*i):
                invalid.add(i)
        cc = list(set(goes) - invalid)
        cc_len = 10000
        pos_to = None
        for i in cc:
            k = (i[0] - self.point_to[0]) ** 2 + (i[1] - self.point_to[1]) ** 2
            if k < cc_len:
                cc_len = k
                pos_to = i
        if pos_to is not None:
            self.d_pos = [pos_to[j] - self.pos[j] for j in range(2)]

    def point_to0(self):
        return player.pos

    def point_to1(self):
        return [player.pos[i] + player.dir[i] * 4 for i in range(2)]

    def point_to2(self):
        return [(spirits[spirits_ind[0]].pos[i] + player.pos[i] + player.dir[i] * 2) * 2 for i in range(2)]

    def point_to3(self):
        if (self.pos[0] - player.pos[0]) ** 2 + (self.pos[1] - player.pos[1]) ** 2 < 16:
            return player.pos
        return self.run_up


def spirits_control(delta_time):
    if max_eat - eat_cnt > 30 and not spirits[spirits_ind[2]].is_active:
        spirits[spirits_ind[2]].is_active = True
    if eat_cnt < max_eat * 2 / 3 and not spirits[spirits_ind[3]].is_active:
        spirits[spirits_ind[3]].is_active = True
        spirits[spirits_ind[3]].point_to = spirits[spirits_ind[3]].run_up
        spirits[spirits_ind[3]].update(delta_time)
    tt = pygame.time.get_ticks() - time_start
    if tt < 7000 or 27000 < tt < 34000 or 54000 < tt < 59000 or 79000 < tt < 83000:
        for sp in spirits:
            sp.point_to = sp.run_up
            sp.update(delta_time)
    else:
        # 7000 < pygame.time.get_ticks() < 27000 or 34000 < pygame.time.get_ticks() < 54000 or \
        #   59000 < pygame.time.get_ticks() < 79000 or 83000 < pygame.time.get_ticks():
        for sp in spirits:
            sp.point_to = sp.select_point()
            sp.update(delta_time)


def generate_level(level):
    global all_sprites, tiles_group, player_group, eat_cnt
    eat_cnt = 0
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    new_player, x, y = None, None, None
    mm = []
    ss = []
    ss1 = dict()
    for y in range(len(level[0])):
        mm1 = []
        for x in range(len(level)):
            if level[x][y] in '.+':
                mm1 += [Tile('dot', x, y)]
                level[x][y] = '.'
                eat_cnt += 1
            elif level[x][y] == '#':
                mm1 += [Tile('wall', x, y)]
            elif level[x][y] == '@':
                mm1 += [Tile('empty', x, y)]
                new_player = Player(x, y)
            elif level[x][y] in '0123':
                mm1 += [Tile('empty', x, y)]
                ss1[int(level[x][y]) % 4] = len(ss)
                ss += [Spirit(x, y, int(level[x][y]) % 4, len(ss))]
        mm += [mm1]
    all_sprites.draw(screen)
    return new_player, y + 1, x + 1, mm, ss, ss1


def game_step(delta_time):
    global player, game_map, game_spr_map, all_sprites, tiles_group, eat_cnt


    player.update(delta_time)
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    line = "Eat left: " + str(eat_cnt)
    font = pygame.font.Font(None, 30)
    io = 'white'
    string_rendered = font.render(line, True, pygame.Color(io))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = HEIGHT - intro_rect.height
    intro_rect.x = 0
    screen.blit(string_rendered, intro_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                start_main_menu(screen)
            else:
                player.go(event)

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, func, image_name=None):
        pygame.sprite.Sprite.__init__(self)
        if image_name is None:
            GREY = (100, 100, 100)
            self.image = pygame.Surface((100, 50))
        else:
            self.image = pygame.transform.scale(load_image(image_name), (200, 50))
        # self.image.fill(GREY)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.func = func

    def inside(self, x, y):
        return x >= self.rect.left and x <= self.rect.right and y >= self.rect.top and y <= self.rect.bottom

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.inside(*event.pos):
            self.func()


def start_difficulty_menu(screen):
    global game_state, difficulty, buttons
    game_state = 6
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 30)
    string_rendered = font.render(f"Current difficulty is {difficulty}", True, pygame.Color("white"))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 30
    intro_rect.x = 150
    # text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    buttons = pygame.sprite.Group()
    bnumber = 3
    pos = [(WIDTH // 2, HEIGHT * 0.2 + i * HEIGHT * 0.8 / bnumber) for i in range(bnumber)]

    def change_diff(diff):
        global difficulty, screen
        difficulty = diff
        start_main_menu(screen)

    one = Button(*pos[0], lambda: change_diff(1), image_name="buttons/1.png")
    buttons.add(one)
    two = Button(*pos[1], lambda: change_diff(2), image_name="buttons/2.png")
    buttons.add(two)
    three = Button(*pos[2], lambda: change_diff(3), image_name="buttons/3.png")
    buttons.add(three)
    buttons.draw(screen)


def start_main_menu(screen):
    global game_state, buttons
    game_state = 4
    background = pygame.transform.scale(load_image('main_menu.png'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    buttons = pygame.sprite.Group()
    bnumber = 3
    pos = [(WIDTH//2, HEIGHT*0.2 + i*HEIGHT*0.8/bnumber) for i in range(bnumber)]
    play = Button(*pos[0], lambda: start_level_menu(screen), image_name="buttons/play.png")
    buttons.add(play)
    diff_butt = Button(*pos[1], lambda: start_difficulty_menu(screen), image_name="buttons/difficulty.png")
    buttons.add(diff_butt)
    quit_game = Button(*pos[2], quit, image_name="buttons/quit.png")
    buttons.add(quit_game)
    buttons.draw(screen)


def start_level_menu(screen):
    global game_state, buttons
    game_state = 5
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 30)
    string_rendered = font.render("Choose level", True, pygame.Color("white"))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 30
    intro_rect.x = 150
    # text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    buttons = pygame.sprite.Group()
    bnumber = 4
    pos = [(WIDTH // 2, HEIGHT * 0.2 + i * HEIGHT * 0.8 / bnumber) for i in range(bnumber)]

    def start_level(level_n):
        global game_state, game_map, player, level_x, level_y, game_spr_map, spirits, spirits_ind, max_eat
        game_state = 2
        game_map = load_level(level_names[level_n-1])
        player, level_x, level_y, game_spr_map, spirits, spirits_ind = generate_level(game_map)
        max_eat = eat_cnt

    one = Button(*pos[0], lambda: start_level(1), image_name="buttons/1.png")
    buttons.add(one)
    two = Button(*pos[1], lambda: start_level(2), image_name="buttons/2.png")
    buttons.add(two)
    three = Button(*pos[2], lambda: start_level(3), image_name="buttons/3.png")
    buttons.add(three)
    back = Button(*pos[3], lambda: start_main_menu(screen), image_name="buttons/Back.png")
    buttons.add(back)
    buttons.draw(screen)


def check_buttons(buttons):
    for event in pygame.event.get():
        for but in buttons:
            but.check_event(event)
        if event.type == pygame.QUIT:
            terminate()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png'), 'dot': load_image('dot.png')}
player_image = load_image('pac.png')
tile_width = tile_height = 25
game_state = 4
difficulty = 1
eat_cnt = 1
time_start = pygame.time.get_ticks()

buttons = pygame.sprite.Group()
start_main_menu(screen)

'''game states
2 ???????? ????????
3 ?????????? ????????
4 ?????? ?????????????? ????????????????????????????
5 ?????? ?????????????? ?? ????????????????
6 ?????? ?????????????? ???? ????????????????????
'''
while True:
    delta_time = difficulty*clock.tick(FPS) / 100

    if game_state == 1:
        # start_screen()
        # buttons.draw(screen)
        time_start = pygame.time.get_ticks()
    elif game_state in [4, 5, 6]:
        check_buttons(buttons)
    elif game_state == 2 and eat_cnt != 0:
        game_step(delta_time)
        spirits_control(delta_time)
    elif game_state == 3:
        game_over_screen()  # game_over_screen1()
    if eat_cnt == 0:
        game_win_screen()

    pygame.display.flip()
    clock.tick(FPS)



