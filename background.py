class BackGround:
    def __init__(self, surface, img, x, y, scrollSpeed):
        self.surface = surface
        self.img = img
        self.x = x
        self.y = y
        self.scrollSpeed = scrollSpeed

        self.x2 = self.x + self.img.get_width()
        self.y2 = self.y

        self.startX = self.x

    def draw(self):
        self.surface.blit(self.img, (self.x, self.y))
        self.surface.blit(self.img, (self.x2, self.y2))

    def scroll_left(self):
        WINDOW_WIDTH, WINDOW_HEIGHT = self.surface.get_size()
        if self.x > WINDOW_WIDTH or self.x2 > WINDOW_WIDTH:
            self.x = self.startX
            self.x2 = self.x - self.img.get_width()
        else:
            self.x += self.scrollSpeed
            self.x2 += self.scrollSpeed

    def scroll_right(self):
        if self.x <= 0 and self.x2 <= 0:
            self.x = self.startX
            self.x2 = self.x + self.img.get_width()
        else:
            self.x -= self.scrollSpeed
            self.x2 -= self.scrollSpeed
