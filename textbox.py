import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import html2text

import pygame
import sys
from button import Button
import webbrowser
pygame.init()

title_font = pygame.font.SysFont("Berlin Sans FB Demi", 80, "bold")
text_font = pygame.font.SysFont("Arial", 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = pygame.Color("dodgerblue2")


class TextBox:
    def __init__(self, surface, color, x, y, width, height, planet:str):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.planet = planet.capitalize()
        self.close_button = Button(surface, "X", RED, WHITE,
                                   self.x+self.width-70, self.y+20, 50, 50)
        self.closed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        data = self.get_data()
        self.text = data[0]
        self.url = data[1]
        self.link = None

    def draw(self):
        if not self.closed:
            pygame.draw.rect(self.surface, self.color, self.rect)
            pygame.draw.rect(self.surface, WHITE, self.rect, 3)
            self.close_button.draw()

            self.surface.blit(title_font.render(self.planet, True, WHITE),
                                  (self.x*2.5, self.y+20))

            y = self.y + 150
            for line in self.text.split("\n"):
                self.surface.blit(text_font.render(line, True, WHITE), (self.x+50, y))
                y += 20

            self.surface.blit(text_font.render("Source:", True, WHITE),
                              (self.x+50, self.y+self.height-50))
            self.link = self.surface.blit(text_font.render(self.url, True, BLUE),
                                     (self.x+110, self.y+self.height-50))

    def check_close(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.close_button.rect.collidepoint(mouse_pos):
            self.closed = True
        elif self.link is not None and self.link.collidepoint(mouse_pos):
            webbrowser.open(self.url)

    def get_data(self):
        if self.planet == "Mercury":
            url = "https://en.wikipedia.org/wiki/Mercury_(planet)"
        else:
            url = f"https://en.wikipedia.org/wiki/{self.planet}"

        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        page = session.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        list(soup.children)

        html = "".join([str(element) for element in soup.find_all('p')])
        h = html2text.HTML2Text()
        h.ignore_links = True
        text = h.handle(html)

        if self.planet == "Uranus":
            start_index = text.find(self.planet)
            text = text[start_index:]
        text = text[:text.find("\n\n")].replace("*", "")
        return text, url
