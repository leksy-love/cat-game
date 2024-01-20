import pygame
import os
import sys
import time

xb = 0
yb = 0
coords = []
pygame.init()
size = 700, 700
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()

def game_screen():
    fon = pygame.transform.scale(load_image('game.png'), (700, 700))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)




def end_screen():
    intro_text = ["Поздравляю! Вы прошли игру!" "",
                  "Надеюсь вам понравилось играть",
                  "По всем вопросам и предложениям обращаться к автору",
                  "Спасибо за прохождение"]

    fon = pygame.transform.scale(load_image('end.jpg'), (700, 700))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ИГРА ПОЙМАЙ КОТА", "",
                  "Правила игры: не дай коту выйти за край поля,",
                  "преграждая ему путь нажатием на клетки.",
                  "Для начала игры нажмите мышкой на любое место"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (700, 700))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image.set_colorkey((255, 255, 255))
    return image




all_sprites = pygame.sprite.Group()

    # создадим спрайт
cat = pygame.sprite.Sprite()
    # определим его вид
cat.image = load_image("cat.png")
    # и размеры
cat.rect = cat.image.get_rect()
    # добавим спрайт в группу
all_sprites.add(cat)
start_screen()
class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self):
        colors = [pygame.Color("black"), pygame.Color("green")]
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, colors[self.board[y][x]], (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color("white"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        global xb, yb
        x, y = cell
        xb = cell[0]
        yb = cell[1]
        self.board[y][x] = (self.board[y][x] + 1) % 2
        coords.append(cell)


    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


# считаем количество клеток исходя из размера экрана и размера клетки
w = 700 // 70 - 1
h = 700 // 70 - 1
board = Board(w, h)
board.set_view(10, 10, 70)
x, y = 4, 4
cat.rect = cat.image.get_rect().move(
    70 * x + 25, 70 * y + 15)

def proverka():
    global x
    global y
    global coords
    if (x,  (y - 1)) not in coords:
        cat.rect.top -= 70
        y -= 1
    elif (x, (y + 1)) not in coords:
        cat.rect.top += 70
        y += 1
    elif ((x - 1), y) not in coords:
        cat.rect.left -= 70
        x -=1
    elif ((x + 1), y) not in coords:
        cat.rect.left += 70
        x += 1
    else:
        end_screen()
        time.sleep(10)
        pygame.quit()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or x < 0 or y < 0:
            game_screen()
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
            
            if xb >= x and yb <= y:
                if ((x - 1), y) not in coords:
                    cat.rect.left -= 70
                    x -= 1
                elif ((x - 1) , y) in coords and (x, (y + 1)) not in coords:
                    cat.rect.top += 70
                    y += 1
                else:
                    proverka()
            elif xb <= x and yb <= y:
                if (x, (y + 1)) not in coords:
                    cat.rect.top += 70
                    y += 1
                elif (x, (y + 1)) in coords and ((x + 1), y) not in coords:
                    cat.rect.left += 70
                    x += 1
                else:
                    proverka()
            elif xb >= x and yb >= y:
                if (x, (y - 1)) not in coords:
                    cat.rect.top -= 70
                    y -= 1
                elif (x, (y - 1)) in coords and ((x - 1), y) not in coords:
                    cat.rect.left -= 70
                    x -= 1
                else:
                    proverka()
            elif xb <= x and yb >= y:
                if (x, (y - 1)) not in coords:
                    cat.rect.top -= 70
                    y -= 1
                elif (x, (y - 1)) in coords and ((x + 1), y) not in coords:
                    cat.rect.left += 70
                    x += 1
                else:
                    proverka()



    screen.fill((0, 0, 0))
    board.render()
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()