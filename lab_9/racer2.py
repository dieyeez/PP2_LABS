import pygame
import sys
import math
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple paint')

# цвета
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)


class Button:
    def __init__(self, x, y, width, height, text, color, action):
        # нужно для создания прямоугольной кнпоки
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text  # текст
        self.color = color  # цвет
        self.action = action  # функция работает при нажатий

    def draw(self, screen):
        # функция которая рисует рект с определенным цветам на экране
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 24)  # текст без шрифта размером 24
        # рендерит текст на кнопке
        text_surface = font.render(self.text, True, white)
        # отображает текст
        screen.blit(text_surface, (self.rect.x + 12, self.rect.y + 12))

    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # если нажата кнопка мыши
            # Проверяет находится ли позиция курсора внутри прямоугольника
            if self.rect.collidepoint(event.pos):
                self.action()  # если да то вызывает функция кнопки


drawing = False
brush_color = black
mode = "brush"
start_pos = None

# Функций обработчик


def set_black():
    global brush_color, mode
    brush_color = black
    mode = "brush"


def set_green():
    global brush_color, mode
    brush_color = green
    mode = "brush"


def set_red():
    global brush_color, mode
    brush_color = red
    mode = "brush"


def set_blue():
    global brush_color, mode
    brush_color = blue
    mode = "brush"


def clear_screen():
    screen.fill(white)


def exit_app():
    pygame.quit()
    sys.exit()


def set_eraser():
    global brush_color, mode
    brush_color = white
    mode = "brush"


def set_brush():
    global mode
    mode = "brush"


def set_rectangle():
    global mode
    mode = "rect"


def set_circle():
    global mode
    mode = "circle"


def set_square():
    global mode
    mode = "square"


def set_right_triangle():
    global mode
    mode = "right_triangle"


def set_equilateral_triangle():
    global mode
    mode = "equilateral_triangle"


def set_rhombus():
    global mode
    mode = "rhombus"


# Создаем лист элементы которого объекты (кнопка с ее функцией)
buttons = [
    Button(10, 10, 60, 30, 'Black', black, set_black),
    Button(80, 10, 60, 30, 'Green', green, set_green),
    Button(150, 10, 60, 30, 'Red', red, set_red),
    Button(220, 10, 60, 30, 'Blue', blue, set_blue),
    Button(290, 10, 60, 30, 'Clear', gray, clear_screen),
    Button(360, 10, 60, 30, 'Eraser', gray, set_eraser),
    Button(430, 10, 60, 30, 'Brush', gray, set_brush),
    Button(500, 10, 60, 30, 'Rect', gray, set_rectangle),
    Button(570, 10, 60, 30, 'Circle', gray, set_circle),
    Button(640, 10, 60, 30, 'Exit', black, exit_app),
    Button(710, 10, 80, 30, 'Square', gray, set_square),
    Button(10, 50, 80, 30, 'Right ⊿', gray, set_right_triangle),
    Button(100, 50, 80, 30, 'Equi ⊿', gray, set_equilateral_triangle),
    Button(190, 50, 80, 30, 'Rhombus', gray, set_rhombus),

]

clear_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  # если зажата кнопка мыши
            if event.button == 1:  # если зажата именно левая
                drawing = True  # мы рисуем
                start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                if mode == "rect" and start_pos:  # формула для рисовки на экране именно прямоугольника
                    x = min(start_pos[0], event.pos[0])
                    y = min(start_pos[1], event.pos[1])
                    width = abs(event.pos[0] - start_pos[0])
                    height = abs(event.pos[1] - start_pos[1])

                    pygame.draw.rect(screen, brush_color,
                                     (x, y, width, height), 2)

                elif mode == "circle" and start_pos:  # формула для рисовки на экране именно круга
                    radius = max(
                        abs(event.pos[0] - start_pos[0]), abs(event.pos[1] - start_pos[1]))
                    pygame.draw.circle(screen, brush_color,
                                       start_pos, radius, 2)

                elif mode == "square" and start_pos:  # формула для рисовки на экране именно квадрата
                    x = min(start_pos[0], event.pos[0])
                    y = min(start_pos[1], event.pos[1])
                    side = max(abs(event.pos[0] - start_pos[0]),
                               abs(event.pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, brush_color,
                                     (x, y, side, side), 2)

                elif mode == "right_triangle" and start_pos:  # формула для рисовки на экране именно прямоугольника
                    x1, y1 = start_pos
                    x2, y2 = event.pos
                    points = [(x1, y1), (x1, y2), (x2, y2)]
                    pygame.draw.polygon(screen, brush_color, points, 2)

                # формула для рисовки на экране именно равностороннего трехугольника
                elif mode == "equilateral_triangle" and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = event.pos
                    base = abs(x2 - x1)
                    height = int((3**0.5 / 2) * base)
                    mid_x = (x1 + x2) // 2
                    if y2 > y1:
                        top = (mid_x, y1)
                        left = (x1, y1 + height)
                        right = (x2, y1 + height)
                    else:
                        top = (mid_x, y1)
                        left = (x1, y1 - height)
                        right = (x2, y1 - height)
                    pygame.draw.polygon(screen, brush_color, [
                                        top, left, right], 2)  # polygon универсальный: позволяет рисовать любые многоугольники, задавая их вершины.

                elif mode == "rhombus" and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = event.pos
                    mid_x = (x1 + x2) // 2
                    mid_y = (y1 + y2) // 2
                    points = [(mid_x, y1), (x2, mid_y),
                              (mid_x, y2), (x1, mid_y)]
                    pygame.draw.polygon(screen, brush_color, points, 2)

        for button in buttons:
            button.check_action(event)
    if drawing and mode == "brush":
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 50:
            pygame.draw.circle(screen, brush_color, (mouse_x, mouse_y), 5)

    # рисует рект на левом верхнем углу
    pygame.draw.rect(screen, gray, (0, 0, width, 50))
    buttons[0].draw(screen)

    pygame.display.flip()
