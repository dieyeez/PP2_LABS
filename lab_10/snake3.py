import pygame
import sys
import random
import psycopg2


def connect():
    return psycopg2.connect(
        database="snake_db",
        user="postgres",
        password="Ggg123ddd",
        host="localhost",
        port="5432"
    )


def get_or_create_user():
    username = input("Enter your username: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cur.fetchone()

    if result:
        user_id = result[0]
        cur.execute(
            "SELECT level, score FROM user_score WHERE user_id = %s", (user_id,))
        level_score = cur.fetchone()
        if level_score:
            level, score = level_score
        else:
            level, score = 0, 0
            cur.execute(
                "INSERT INTO user_score (user_id) VALUES (%s)", (user_id,))
    else:
        cur.execute(
            "INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        level, score = 0, 0
        cur.execute("INSERT INTO user_score (user_id) VALUES (%s)", (user_id,))

    conn.commit()
    cur.close()
    conn.close()
    return user_id, username, level, score


def save_score(user_id, level, score):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_score SET level = %s, score = %s WHERE user_id = %s
    """, (level, score, user_id))
    conn.commit()
    cur.close()
    conn.close()


pygame.init()
x, y = 500, 500
screen = pygame.display.set_mode((x, y))
cell_size = 10
pygame.display.set_caption("Snake game")
bg_clr = pygame.Color("white")
snake_color = pygame.Color("red")

snake_pos = [100, 100]
snake_body = [[100, 100], [90, 100], [80, 100]]
direction = "RIGHT"
change_to = direction

user_id, username, level, score = get_or_create_user()
speed = 6 + level * 2

clock = pygame.time.Clock()
food_types = [
    {"color": pygame.Color("red"), "score": 1, "lifetime": 10000},
    {"color": pygame.Color("blue"), "score": 2, "lifetime": 15000},
    {"color": pygame.Color("gold"), "score": 5, "lifetime": 5000}
]


def generate_food():
    while True:
        pos = [random.randrange(0, x, cell_size),
               random.randrange(0, y, cell_size)]
        if pos not in snake_body:
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
paused = False

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
            elif event.key == pygame.K_p:
                save_score(user_id, level, score)
                paused = True
                print("Paused. Press P to resume.")

        if paused and event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = False
            print("Resumed.")

    if paused:
        continue

    direction = change_to

    if direction == "UP":
        snake_pos[1] -= cell_size
    elif direction == "DOWN":
        snake_pos[1] += cell_size
    elif direction == "LEFT":
        snake_pos[0] -= cell_size
    elif direction == "RIGHT":
        snake_pos[0] += cell_size

    if (snake_pos[0] < 0 or snake_pos[0] >= x or
            snake_pos[1] < 0 or snake_pos[1] >= y):
        save_score(user_id, level, score)
        running = False

    snake_body.insert(0, list(snake_pos))

    if food["pos"] == snake_pos:
        score += food["score"]
        food = generate_food()
        if score % 5 == 0:
            level += 1
            speed += 2
    else:
        snake_body.pop()

    if snake_pos in snake_body[1:]:
        save_score(user_id, level, score)
        running = False

    if pygame.time.get_ticks() - food["spawn_time"] > food["lifetime"]:
        food = generate_food()

    screen.fill(bg_clr)
    for block in snake_body:
        pygame.draw.rect(screen, snake_color, pygame.Rect(
            block[0], block[1], cell_size, cell_size))

    pygame.draw.rect(screen, food["color"], pygame.Rect(
        food["pos"][0], food["pos"][1], cell_size, cell_size))

    font = pygame.font.Font(None, 24)
    score_text = font.render(
        f"User: {username} | Score: {score} | Level: {level}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    border_color = pygame.Color("black")
    pygame.draw.rect(screen, border_color, pygame.Rect(0, 0, x, y), 5)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()
