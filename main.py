import pygame
import sys
import random
pygame.init()

FRAME_COLOR = (0, 255, 204)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
RED = (224, 0, 0)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
MARGIN = 1

timer = pygame.time.Clock()

curier = pygame.font.SysFont('courier', 36)

COUNT_BLOCKS = 20
HEADER_MARGIN = 70
SIZE_BLOCK = 20
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS  + HEADER_MARGIN]

move_row = buf_row = 0
move_column = buf_column = 1
total = 0
speed = 1

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9,9),SnakeBlock(9, 10)]

def get_random_empty_block():
    x = random.randint(0, COUNT_BLOCKS-1)
    y = random.randint(0, COUNT_BLOCKS-1)
    empty_block = SnakeBlock (x, y)
    while empty_block in snake_blocks:
        empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
        empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
    return empty_block

apple = get_random_empty_block()

def draw_block(color, row, column):
    pygame.draw.rect(screen, color,
                     [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                      HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                      SIZE_BLOCK,
                      SIZE_BLOCK])

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Kira's baby snake")

def gameover():
    print('Game over!')
    pygame.quit()
    sys.exit()

while True:

    # получаем все происходящие события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('exit')
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            #если не шли вертикально
            if event.key == pygame.K_UP and move_column != 0:
                buf_row = -1
                buf_column = 0
            elif event.key == pygame.K_DOWN and move_column != 0:
                buf_row = 1
                buf_column = 0
            # если не шли горизонтально
            elif event.key == pygame.K_LEFT and move_row != 0:
                buf_row = 0
                buf_column = -1
            elif event.key == pygame.K_RIGHT and move_row != 0:
                buf_row = 0
                buf_column = 1

    screen.fill(FRAME_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

    text_total = curier.render(f"Total: {total}", 0, WHITE)
    text_speed = curier.render(f"Speed: {speed}", 0, WHITE)
    screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
    screen.blit(text_speed, (SIZE_BLOCK+230, SIZE_BLOCK))

    for row in range(COUNT_BLOCKS):
        for column in range(COUNT_BLOCKS):
            if (row + column) % 2 == 0:
                color = BLUE
            else:
                color = WHITE

            draw_block(color, row, column)

    head = snake_blocks[-1]
    if not head.is_inside():
        gameover()

    draw_block(RED, apple.x, apple.y)

    for block in snake_blocks:
        draw_block(SNAKE_COLOR, block.x, block.y)

    pygame.display.flip()

    if apple == head:
        total += 1
        speed += total//10
        snake_blocks.append(apple)
        apple = get_random_empty_block()

    move_row = buf_row
    move_column = buf_column
    new_head = SnakeBlock(head.x + move_row, head.y + move_column)

    if new_head in snake_blocks:
        gameover()

    snake_blocks.append(new_head)
    snake_blocks.pop(0)

    # количество кадров в секунду
    timer.tick(3+speed)