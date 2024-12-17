from pygame import SurfaceType, Surface
from pygame.event import Event
from typing import Any
import pygame


pygame.init()

YELLOW: tuple[int, int, int] = (255, 255, 0) # Color for Pac-Man
BLACK: tuple[int, int, int] = (0, 0, 0) # Background color
BLUE: tuple[int, int, int] = (0, 0, 255) #
SPEED: float = 0.25 # Movement speed
SIZE: int = 600 // 30


class Scenario:
    """Represents the game scenario, including the maze, pellets, and power-ups.

    """
    def __init__(self, size: int, pac: object):
        """

        :type pac: object
        :type size: int
        """
        self.pacman = pac
        self.size = size
        self.matrix = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 2, 2, 2, 2, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 2, 2, 2, 2, 2, 2, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 2, 2, 2, 2, 2, 2, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 2, 2, 2, 2, 2, 2, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def calculate_rules(self):
        column: int = int(self.pacman.column_intention - SPEED)
        line: int = int(self.pacman.line_intention - SPEED)

        if 0 <= column < 28 and 0 <= line < 29:
            if self.matrix[line][column] != 1:
                self.pacman.accept_movement()

    def sweep_lines(self, canvas: SurfaceType):
        """

        :type canvas: SurfaceType
        """
        for row_number, row in enumerate(self.matrix):
            self.paint_matrix(canvas, row_number, row)

    def paint_matrix(self, canvas: SurfaceType, row_number: int, row: list[int | Any] | Any):
        """

        :type canvas: SurfaceType
        :type row_number: int
        :type row: list[int | Any] | Any
        """
        column_number: int
        column: int

        for column_number, column in enumerate(row):
            x = column_number * self.size
            y = row_number * self.size
            half_size: int = self.size // 2
            color_rect = BLUE

            if column == 0:
                color_rect = BLACK

            pygame.draw.rect(canvas, color_rect, (x, y, self.size, self.size), 0)

            if column == 0:
                pygame.draw.circle(canvas, YELLOW, (x + half_size, y + half_size), self.size // 10, 0)


class Pacman:
    """Represents the Pac-Man character.

    """
    def __init__(self, size):
        self.column: float = 1.0
        self.line: float = 1.0
        self.center_x: int = 400
        self.center_y: int = 300
        self.size: int = size
        self.speed_x: float = 0.0
        self.speed_y: float = 0.0
        self.radius: int = self.size // 2
        self.column_intention: float = self.column
        self.line_intention: float = self.line

    def calculate_rules(self):
        self.column_intention = self.column + self.speed_x
        self.line_intention = self.line + self.speed_y
        self.center_x = int(self.column * self.size + self.radius)
        self.center_y = int(self.line * self.size + self.radius)

    def accept_movement(self):
        self.column = self.column_intention
        self.line = self.line_intention

    def paint(self, surface: SurfaceType):
        """

        :type surface: SurfaceType
        """
        # draw pacman's body
        pygame.draw.circle(surface, YELLOW, (self.center_x, self.center_y), self.radius, 0)

        # draw the mouth
        corner_mouth: tuple[int, int] = (self.center_x, self.center_y)
        upper_lip: tuple[int, int] = (self.center_x + self.radius, self.center_y - self.radius)
        lower_lip: tuple[int, int] = (self.center_x + self.radius, self.center_y)

        points: list[tuple[int, int]] = [corner_mouth, upper_lip, lower_lip]

        pygame.draw.polygon(screen, BLACK, points, 0)

    def process_events(self, event: list[Event]):
        """

        :type event: list[Event]
        """
        for eve in event:
            if eve.type == pygame.KEYDOWN:
                if eve.key == pygame.K_RIGHT:
                    self.speed_x = SPEED
                    self.speed_y = 0.0
                elif eve.key == pygame.K_LEFT:
                    self.speed_x = -SPEED
                    self.speed_y = 0.0
                elif eve.key == pygame.K_DOWN:
                    self.speed_y = SPEED
                    self.speed_x = 0.0
                elif eve.key == pygame.K_UP:
                    self.speed_y = -SPEED
                    self.speed_x = 0.0


if __name__ == "__main__":
    screen: Surface = pygame.display.set_mode((800, 600), 0)
    pacman: Pacman = Pacman(SIZE)
    scenario: Scenario = Scenario(SIZE, pacman)

    while True:
        # calculate the rules
        pacman.calculate_rules()
        scenario.calculate_rules()

        # paint the screen
        screen.fill(BLACK)
        scenario.sweep_lines(screen)
        pacman.paint(screen)
        pygame.display.update()
        pygame.time.delay(50)

        # captures the events
        events: list[Event] = pygame.event.get()

        e: Event
        for e in events:
            if e.type == pygame.QUIT:
                exit()
        pacman.process_events(events)