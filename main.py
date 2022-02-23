import pygame
import sys

from button import Button
from background import BackGround
from textbox import TextBox

pygame.init()

WINDOW_SIZE = (1100, 550)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Our Solar System")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCROLL_SPEED = 8

title_font = pygame.font.SysFont("Berlin Sans FB Demi", 80, "bold")
secondTitle_font = pygame.font.SysFont("Arial", 30, "bold")

background_img = pygame.image.load("SpaceBG.png")
background_img = pygame.transform.scale(background_img, WINDOW_SIZE)


class Planet:
    def __init__(self, surface, img, x, y, scrollSpeed):
        self.surface = surface
        self.img = img
        self.x = x
        self.y = y
        self.scrollSpeed = scrollSpeed

        self.rect = self.get_rect()
        self.text_box = None

    def draw(self):
        self.surface.blit(self.img, (self.x, self.y))

        if self.text_box is not None:
            self.text_box.draw()

        # code for testing collision rect:
        # pygame.draw.rect(self.surface, (255, 0, 0), self.rect, 3)

    def scroll(self, side):
        if side == "l":
            self.x += self.scrollSpeed
        else:
            self.x -= self.scrollSpeed
        self.rect = self.get_rect()

    def check_click(self, pos):
        if self.text_box is None:
            if self.rect.collidepoint(pos):
                clicked_planet = ordered_planets[planets_imgs.index(self.img)]
                self.text_box = TextBox(self.surface, BLACK, WINDOW_SIZE[0]//6.5, WINDOW_SIZE[1]//20,
                                   WINDOW_SIZE[0]//1.5, WINDOW_SIZE[1]//1.1, clicked_planet)
            else:
                self.text_box = None
        else:
            self.text_box.check_close()
            if self.text_box.closed:
                self.text_box = None

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())


# Planets
ordered_planets = ["sun", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
y_positions = (50, 300, 285, 250, 270, 185, 230, 240, 240)
planets_imgs = [pygame.image.load(f"Planets/{name}.png") for name in ordered_planets]
planets = []
x = 0
for image, y in zip(planets_imgs, y_positions):
    planets.append(Planet(window, image, x, y, SCROLL_SPEED))
    x += image.get_width() + 100


def quit_game():
    pygame.quit()
    sys.exit(0)


def scroll_all(bg, side):
    for planet in planets:
        planet.scroll(side)

    if side == "l":
        bg.scroll_left()
    else:
        bg.scroll_right()


def rect_contains_rect(r1, r2):
    return r2.x + r2.w <= r1.x + r1.w and r2.y + r2.h <= r1.y + r1.h


def main():
    clock = pygame.time.Clock()
    bg = BackGround(window, background_img, 0, 0, SCROLL_SPEED)
    fps_font = pygame.font.SysFont("Arial", 30, "bold")
    text_box = None

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if text_box is not None:
                        text_box.closed = True
                        text_box.check_close()
                    menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for planet in planets:
                    planet.check_click(event.pos)

        if text_box is None:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if (planets[0].x + planets[0].img.get_width()) < WINDOW_SIZE[0] // 2:
                    scroll_all(bg, "l")

            if keys[pygame.K_RIGHT]:
                if (planets[-1].x + planets[-1].img.get_width()) >= WINDOW_SIZE[0]:
                    scroll_all(bg, "r")

        window.fill(BLACK)
        bg.draw()
        clock.tick(60)
        window.blit(fps_font.render(f"FPS:{int(clock.get_fps())}", True, WHITE), (10, 10))

        for planet in planets:
            if planet.x <= WINDOW_SIZE[0]:
                if planet.text_box is not None:
                    text_box = planet.text_box

                if text_box is not None:
                    if rect_contains_rect(text_box.rect, planet.rect) and planet.text_box is None:
                        continue

                if text_box is not None and text_box.closed:
                    text_box = None
                planet.draw()

        pygame.display.update()

    quit_game()


def menu():
    viewButton = Button(window, "View", "#120091", WHITE, 320, 250, 400, 160)
    secondTitle_text = "View and learn about the planets of our solar system"
    secondTitle_label = secondTitle_font.render(secondTitle_text, True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if viewButton.rect.collidepoint(event.pos):
                    main()

        window.fill(BLACK)
        window.blit(background_img, (0, 0))
        window.blit(title_font.render("Our Solar System", True, WHITE), (240, 20))
        window.blit(secondTitle_label, (180, 110))
        window.blit(secondTitle_font.render("Made By: Roni", True, WHITE), (10, WINDOW_SIZE[1]-45))
        viewButton.draw()

        pygame.display.update()


if __name__ == "__main__":
    menu()
