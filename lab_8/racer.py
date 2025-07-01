import pygame
import random
import sys
import os

# Инициализация pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 350, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game with Coins")

# Цвета
WHITE = (247, 247, 247)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)  # Цвет дороги
LINE_COLOR = (200, 200, 200)  # Разметка дороги

# Загрузка изображений
car_img = pygame.image.load(os.path.join("lab_8", "images", "car.png"))
car_img = pygame.transform.scale(car_img, (75, 150))

# Настройки машины
car = pygame.Rect(WIDTH // 2 - 37, HEIGHT - 160,
                  75, 150)  # Размеры по изображению
car_speed = 6

# Настройки монет
coin_size = 20
coins = []
coin_spawn_time = 0
coin_spawn_delay = 700  # Спавн раз в 0.7 сек
collected_coins = 0

# Настройки дороги
road_x = WIDTH // 4
road_width = WIDTH // 2
lane_marker_y = 0  # Для движения разметки

# Шрифт
font = pygame.font.Font(None, 36)

# Таймер
clock = pygame.time.Clock()

# Игровой цикл
running = True
while running:
    screen.fill(GRAY)  # Фон - дорога

    # Отрисовка дороги
    pygame.draw.rect(screen, WHITE, (road_x - 5, 0,
                     5, HEIGHT))  # Левая граница
    pygame.draw.rect(screen, WHITE, (road_x + road_width,
                     0, 5, HEIGHT))  # Правая граница

    # Разметка (движется вниз)
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, LINE_COLOR, (WIDTH // 2 - 5,
                         (i + lane_marker_y) % HEIGHT, 5, 20))

    lane_marker_y += 5
    if lane_marker_y > 40:
        lane_marker_y = 0

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление машиной
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car.x > road_x:
        car.x -= car_speed
    if keys[pygame.K_RIGHT] and car.x < road_x + road_width - car.width:
        car.x += car_speed

    # Спавн монет
    if pygame.time.get_ticks() - coin_spawn_time > coin_spawn_delay:
        coin_x = random.randint(road_x + 10, road_x + road_width - 10)
        coin_y = -coin_size
        coins.append(pygame.Rect(coin_x, coin_y, coin_size, coin_size))
        coin_spawn_time = pygame.time.get_ticks()

    # Движение монет
    for coin in coins[:]:
        coin.y += 4  # Движение вниз
        pygame.draw.circle(screen, YELLOW, (coin.x, coin.y), coin_size // 2)

        # Проверка столкновения с машиной
        if car.colliderect(coin):
            collected_coins += 1
            coins.remove(coin)

        # Удаление монет, вышедших за границы экрана
        elif coin.y > HEIGHT:
            coins.remove(coin)

    # Отрисовка машины
    screen.blit(car_img, (car.x, car.y))

    # Отображение счета
    coin_text = font.render(f"Coins: {collected_coins}", True, WHITE)
    screen.blit(coin_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
