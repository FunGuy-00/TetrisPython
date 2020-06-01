import pygame as pg
from dataclasses import dataclass
import random

# Window settings
window_width = 400
window_heigth = 800
block_size = 40
rows = window_width // block_size
cols = window_heigth // block_size

# Grid
grid = [0] * rows * cols

# Score
score = 0

# Pictures
pic = []
for n in range(8):
    pic.append(pg.transform.scale(pg.image.load("Pictures/{}.png".format(n)), (block_size, block_size)))

pg.init()
clock = pg.time.Clock()
window_surface = pg.display.set_mode([window_width, window_heigth])
pg.display.set_caption("Tetris")

# Shapes, 4 Zahlen pro Zeile um Formen zu definieren
shape_c = [[0, 1, 1, 0,
            0, 1, 1, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]]
shape_t = [[2, 2, 2, 0,
            0, 2, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0],
           [0, 2, 0, 0,
            0, 2, 2, 0,
            0, 2, 0, 0,
            0, 0, 0, 0],
           [0, 2, 0, 0,
            2, 2, 2, 0,
            0, 0, 0, 0,
            0, 0, 0, 0],
           [0, 2, 0, 0,
            2, 2, 0, 0,
            0, 2, 0, 0,
            0, 0, 0, 0]]
shape_s = [[0, 3, 3, 0,
            3, 3, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0],
           [0, 3, 0, 0,
            0, 3, 3, 0,
            0, 0, 3, 0,
            0, 0, 0, 0]]
shape_z = [[0, 4, 4, 0,
            0, 0, 4, 4,
            0, 0, 0, 0,
            0, 0, 0, 0],
           [0, 0, 4, 0,
            0, 4, 4, 0,
            0, 4, 0, 0,
            0, 0, 0, 0]]
shape_i = [[5, 5, 5, 5,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0],
           [0, 5, 0, 0,
            0, 5, 0, 0,
            0, 5, 0, 0,
            0, 5, 0, 0]]
shape_l2 = [[0, 6, 0, 0,
             0, 6, 0, 0,
             0, 6, 6, 0,
             0, 0, 0, 0],
            [0, 0, 6, 0,
             6, 6, 6, 0,
             0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 6, 6, 0,
             0, 0, 6, 0,
             0, 0, 6, 0,
             0, 0, 0, 0],
            [6, 6, 6, 0,
             6, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0]]
shape_l1 = [[0, 0, 7, 0,
             0, 0, 7, 0,
             0, 7, 7, 0,
             0, 0, 0, 0],
            [7, 7, 7, 0,
             0, 0, 7, 0,
             0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 7, 7, 0,
             0, 7, 0, 0,
             0, 7, 0, 0,
             0, 0, 0, 0],
            [0, 7, 0, 0,
             0, 7, 7, 7,
             0, 0, 0, 0,
             0, 0, 0, 0]]
shape_list = [shape_c, shape_i, shape_s, shape_t, shape_z, shape_l1, shape_l2]

@dataclass
class shapes():
    shape: list
    start_x = 0
    start_y = 3

    def show(self):
        for n, m in enumerate(self.shape):
            if m > 0:
                y = (self.start_x + n // 4) * block_size
                x = (self.start_y + n % 4) * block_size
                window_surface.blit(pic[m], (x, y))

    def update(self, new_x, new_y):
        if self.valid(self.start_x+new_x, self.start_y+new_y):
            self.start_x += new_x
            self.start_y += new_y
            return True
        return False

    @staticmethod
    def create():
        n = random.randint(0, 6)
        m = random.randint(0, 3)
        l = len(shape_list[n])
        if m >= l:
            m = 0
        return shapes(shape_list[n][m])

    @staticmethod
    def rotate(shape):
        for n in range(len(shape_list)):
            for m in range(len(shape_list[n])):
                if shape_list[n][m] == shape:
                    if len(shape_list[n]) > m + 1:
                        return shapes(shape_list[n][m + 1])
                    else:
                        return shapes(shape_list[n][0])

    def valid(self, x, y):
        for n, m in enumerate(self.shape):
            if m > 0:
                x1 = x + n // 4
                y1 = y + n % 4
                if x1 >= cols or y1 < 0 or y1 >= rows or grid[x1 * rows + y1] > 0:
                    return False
        return True

def savePosition():
    for n, m in enumerate(figure.shape):
        if m > 0:
            x = figure.start_x + n // 4
            y = figure.start_y + n % 4
            grid[x * rows + y] = m

def deleteRow():
    deleted_rows = 0
    for col in range(cols):
        for row in range(rows):
            if grid[col*rows+row] == 0:
                break
        else:
            del grid[col*rows:col*rows+rows]
            grid[0:0] = [0]*rows
            deleted_rows += 1
    return  deleted_rows**2*100

# Events
shape_down = pg.USEREVENT + 1
pg.time.set_timer(shape_down, 500)

figure = shapes.create()

while True:
    clock.tick(500)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == shape_down:
            if not figure.update(1, 0):
                savePosition()
                score += deleteRow()
                figure = shapes.create()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                figure.update(0, -1)
            if event.key == pg.K_RIGHT:
                figure.update(0, 1)
            if event.key == pg.K_DOWN:
                figure.update(1, 0)
            if event.key == pg.K_UP:
                figure = shapes.rotate(figure.shape)

    window_surface.fill((0, 0, 0))
    figure.show()

    for n, m in enumerate(grid):
        if m > 0:
            x = n % rows * block_size
            y = n // rows * block_size
            window_surface.blit(pic[m], (x, y))
    display_score = pg.font.SysFont('arial', 30).render(f'{score:,}', False, (255, 255, 255))
    window_surface.blit(display_score, (window_width // 2 - display_score.get_width() // 2, 5))
    pg.display.flip()
