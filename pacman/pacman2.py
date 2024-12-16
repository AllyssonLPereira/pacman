import pygame


pygame.init()

YELLOW: tuple[int, int, int] = (255, 255, 0) # Color for Pac-Man
BLUE: tuple[int, int, int] = (0, 0, 255) #
BLACK: tuple[int, int, int] = (0, 0, 0) # Background color
SPEED: float = 0.25 # Movement speed


class Scenario:
    """Represents the game scenario, including the maze, pellets, and power-ups.

    """
    def __init__(self, size):
        self.size = size
        self.matrix = [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1],
        ]

    def paint_column(self, screen, row_number, row):
        for column_number, column in enumerate(row):
            x = column_number * self.size
            y = row_number * self.size
            color = BLACK

            if column == 2:
                color = BLUE

            pygame.draw.rect(screen, color, (x, y, self.size, self.size), 0)

    def paint(self, screen):
        for row_number, row in enumerate(self.matrix):
            self.paint_column(screen, row_number, row)


class Pacman:
    """Represents the Pac-Man character.

    """
    def __init__(self):
        self.column: int = 1
        self.line: int = 1
        self.center_x: int = 400
        self.center_y: int = 300
        self.size: int = 800 // 30
        self.speed_x: float = 0.0
        self.speed_y: float = 0.0
        self.radius: int = self.size // 2

    def calculate_rules(self):
        self.column += self.speed_x
        self.line += self.speed_y
        self.center_x = int(self.column * self.size + self.radius)
        self.center_y = int(self.line * self.size + self.radius)

    def paint(self, surface):
        # draw pacman's body
        pygame.draw.circle(surface, YELLOW, (self.center_x, self.center_y), self.radius, 0)

        # draw the mouth
        corner_mouth = (self.center_x, self.center_y)
        upper_lip = (self.center_x + self.radius, self.center_y - self.radius)
        lower_lip = (self.center_x + self.radius, self.center_y)

        points = [corner_mouth, upper_lip, lower_lip]

        pygame.draw.polygon(screen, BLACK, points, 0)

    def process_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.speed_x = SPEED
                    self.speed_y = 0.0
                elif e.key == pygame.K_LEFT:
                    self.speed_x = -SPEED
                    self.speed_y = 0.0
                elif e.key == pygame.K_DOWN:
                    self.speed_y = SPEED
                    self.speed_x = 0.0
                elif e.key == pygame.K_UP:
                    self.speed_y = -SPEED
                    self.speed_x = 0.0


if __name__ == "__main__":
    pacman = Pacman()
    scenario = Scenario(600 // 30)
    screen = pygame.display.set_mode((800, 600), 0)

    while True:
        # calculate the rules
        pacman.calculate_rules()

        # paint the screen
        screen.fill(BLACK)
        scenario.paint(screen)
        pacman.paint(screen)
        pygame.display.update()
        pygame.time.delay(50)

        # captures the events
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                exit()
        pacman.process_events(events)