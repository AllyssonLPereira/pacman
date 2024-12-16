import pygame


pygame.init()
screen = pygame.display.set_mode((800, 600), 0)

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


class Pacman:
    def __init__(self):
        self.column = 1
        self.line = 1
        self.center_x = 400
        self.center_y = 300
        self.len = 800 // 30
        self.speed_x = 0.2
        self.speed_y = 0.2
        self.radius = self.len // 2

    def calculate_rules(self):
        self.column += self.speed_x
        self.line += self.speed_y
        self.center_x = int(self.column * self.len + self.radius)
        self.center_y = int(self.line * self.len + self.radius)

        if self.center_x + self.radius > 800:
            self.speed_x = -0.2
        if self.center_x - self.radius < 0:
            self.speed_x = 0.2

        if self.center_y + self.radius > 600:
            self.speed_y = -0.2
        if self.center_y - self.radius < 0:
            self.speed_y = 0.2

    def paint(self, surface):
        # Desenhar o corpo de pacman
        pygame.draw.circle(surface, YELLOW, (self.center_x, self.center_y), self.radius, 0)

        # Desenhar a boca
        canto_boca = (self.center_x, self.center_y)
        labio_superior = (self.center_x + self.radius, self.center_y - self.radius)
        labio_inferior = (self.center_x + self.radius, self.center_y)

        pontos = [canto_boca, labio_superior, labio_inferior]

        pygame.draw.polygon(screen, BLACK, pontos, 0)


if __name__ == "__main__":
    pacman = Pacman()

    while True:
        # calcular as regras
        pacman.calculate_rules()

        # pintar a tela
        screen.fill(BLACK)
        pacman.paint(screen)
        pygame.display.update()
        pygame.time.delay(50)

        # captura os eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()