import pygame
import sys
import math
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple paint')

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)


class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 12, self.rect.y + 12))

    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


drawing = False
brush_color = black
mode = "brush"
start_pos = None


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
    Button(640, 10, 60, 30, 'Exit', black, exit_app)
]

clear_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                if mode == "rect" and start_pos:
                    if mode == "rect" and start_pos:
                        x = min(start_pos[0], event.pos[0])
                        y = min(start_pos[1], event.pos[1])
                        width = abs(event.pos[0] - start_pos[0])
                        height = abs(event.pos[1] - start_pos[1])

                        pygame.draw.rect(screen, brush_color,
                                         (x, y, width, height), 2)

                elif mode == "circle" and start_pos:
                    radius = max(
                        abs(event.pos[0] - start_pos[0]), abs(event.pos[1] - start_pos[1]))
                    pygame.draw.circle(screen, brush_color,
                                       start_pos, radius, 2)

        for button in buttons:
            button.check_action(event)
    if drawing and mode == "brush":
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 50:
            pygame.draw.circle(screen, brush_color, (mouse_x, mouse_y), 5)

    pygame.draw.rect(screen, gray, (0, 0, width, 50))
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
