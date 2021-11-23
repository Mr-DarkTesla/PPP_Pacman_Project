import pygame
import os

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
FPS = 24

game_state = 1
difficulty = 1

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
    exit()

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, func, text="Hello world", image_name=None):
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
            


def start_screen():
    global buttons
    intro_text = ["PACMAN", "",
                    "Created by myself",
                    "Bad luck c:"]
    background = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    io = 'yellow'
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color(io))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        io = 'red'

    for event in pygame.event.get():
        for but in buttons:
            but.check_event(event)
        if event.type == pygame.QUIT:
            terminate()

'''game states
4 моя менюшка приветственная
5 моя менюшка с уровнями
6 моя менюшка со сложностью'''
# buttons = pygame.sprite.Group()

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
    background = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    screen.fill((0, 0, 0))

    buttons = pygame.sprite.Group()
    bnumber = 3
    pos = [(WIDTH//2, HEIGHT*0.2 + i*HEIGHT*0.8/bnumber) for i in range(bnumber)]
    def start_playing():
        global game_state
        game_state = 2
    play = Button(*pos[0], start_playing, text="Play", image_name="buttons/play.png") #todo change to level choosing
    buttons.add(play)
    diff_butt = Button(*pos[1], lambda: start_difficulty_menu(screen), image_name="buttons/difficulty.png")
    buttons.add(diff_butt)
    quit_game = Button(*pos[2], quit, image_name="buttons/quit.png")
    buttons.add(quit_game)
    buttons.draw(screen)


def start_diff_menu(screen):
    global game_state, buttons
    game_state = 6
    screen.fill((0, 0, 0))

    buttons = pygame.sprite.Group()
    bnumber = 3
    pos = [(WIDTH // 2, HEIGHT * 0.2 + i * HEIGHT * 0.8 / bnumber) for i in range(bnumber)]

    def start_playing():
        global game_state
        game_state = 2

    play = Button(*pos[0], start_playing, text="Play", image_name="buttons/play.png")  # todo change to level choosing
    buttons.add(play)
    difficulty = Button(*pos[1], start_difficulty_menu, image_name="buttons/difficulty.png")
    buttons.add(difficulty)
    quit_game = Button(*pos[2], quit, image_name="buttons/quit.png")
    buttons.add(quit_game)
    buttons.draw(screen)


def check_buttons(buttons):
    for event in pygame.event.get():
        for but in buttons:
            but.check_event(event)
        if event.type == pygame.QUIT:
            terminate()


# game_state = 4
buttons = pygame.sprite.Group()
start_main_menu(screen)
while True:
    delta_time = clock.tick(FPS) / 100

    if game_state == 1:
        start_screen()
        # buttons.draw(screen)
        time_start = pygame.time.get_ticks()
    elif game_state == 4:   
        check_buttons(buttons)
    elif game_state == 2:
        game_step(delta_time)
        spirits_control(delta_time)
    elif game_state == 3:
        game_over_screen()  # game_over_screen1()
    elif game_state == 6:
        check_buttons(buttons)
    # if eat_cnt == 0:
    #     game_win_screen()

    pygame.display.flip()
    clock.tick(FPS)