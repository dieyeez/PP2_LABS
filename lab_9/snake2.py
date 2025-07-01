import pygame
import sys
import random
pygame.init()

x, y = 500, 500
screen = pygame.display.set_mode((x, y))
cell_size = 10
pygame.display.set_caption("Snake game")
bg_clr = pygame.Color("white")
snake_color = pygame.Color("red")
food_color = pygame.Color("Green")


snake_pos = [100, 100]
snake_body = [[100, 100], [80, 100], [60, 100]]
direction = "RIGHT"
change_to = direction

# skorocst' level i o4ki
speed = 6
level = 0
score = 0

clock = pygame.time.Clock()

# дикшинори
food_types = [
    {"color": "red", "score": 1, "lifetime": 10000},
    {"color": "blue", "score": 2, "lifetime": 15000},
    {"color": "gold", "score": 5, "lifetime": 5000}
]

# функция для генераций позиций еды и его веса


def generate_food():
    while True:
        pos = [random.randrange(
            0, x, cell_size), random.randrange(0, x, cell_size)]
        if pos not in snake_body:  # размещаем еду если он не в теле змейки
            food_type = random.choice(food_types)
            return {
                "pos": pos,
                "color": food_type["color"],
                "score": food_type["score"],
                "lifetime": food_type["lifetime"],
                "spawn_time": pygame.time.get_ticks()
            }


food = generate_food()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
    direction = change_to

    # перемешение змейки (1)
    if direction == "UP":
        snake_pos[1] -= cell_size
    elif direction == "DOWN":
        snake_pos[1] += cell_size
    elif direction == "LEFT":
        snake_pos[0] -= cell_size
    elif direction == "RIGHT":
        snake_pos[0] += cell_size

    # не дает змейке уйти за границу экрана телепортируя в противоположенное место
    if snake_pos[0] < 0:
        snake_pos[0] = x
    elif snake_pos[0] > x:
        snake_pos[0] = 0
    elif snake_pos[1] > y:
        snake_pos[1] = 0
    elif snake_pos[1] < 0:
        snake_pos[1] = y

    # эта строка перемещают змейку вперед
    snake_body.insert(0, list(snake_pos))

    # проверим съела ли змейка еду
    if food["pos"] == snake_pos:
        score += food["score"]
        food = generate_food()
        if score % 2 == 0:
            level += 1
            speed += 2
    # если не сьела удаляем хвостик
    else:
        snake_body.pop()
    # проверим на столкнавение с самим собой
    if snake_pos in snake_body[1:]:
        running = False

    #
    if pygame.time.get_ticks() - food["spawn_time"] > food["lifetime"]:
        food = generate_food()

    # рисует каждый блок змейки в красном цвете
    screen.fill(bg_clr)
    for block in snake_body:
        pygame.draw.rect(screen, snake_color, pygame.Rect(
            block[0], block[1], cell_size, cell_size))

    # рисуем еду
    pygame.draw.rect(screen, food["color"], pygame.Rect(
        food["pos"][0], food["pos"][1], cell_size, cell_size))

    # выводим счет и уровень
    font = pygame.font.Font(None, 24)
    score_text = font.render(
        f"Score: {score}  Level: {level}", True, (0, 0, 0))
    screen.blit(score_text, (320, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()
