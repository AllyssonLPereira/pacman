from pygame import SurfaceType, Surface
from abc import ABCMeta, abstractmethod
from pygame.event import Event
from typing import Any
import pygame


pygame.init()

screen: Surface = pygame.display.set_mode((800, 600), 0)
font = pygame.font.SysFont("arial", 24, True, False)

WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0) # Background color
RED: tuple[int, int, int] = (255, 0, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
YELLOW: tuple[int, int, int] = (255, 255, 0) # Color for Pac-Man
BLUE: tuple[int, int, int] = (0, 0, 255) #
SPEED: int = 1 # Movement speed
SIZE: int = 600 // 30


class GameElements(metaclass=ABCMeta):
    @abstractmethod
    def paint(self, screen: SurfaceType):
        pass

    @abstractmethod
    def calculate_rules(self):
        pass

    @abstractmethod
    def process_events(self, events: list[Event]):
        pass


class Scenario(GameElements):
    """Represents the game scenario, including the maze, pellets, and power-ups.

    """
    def __init__(self, size: int, pac: object):
        """

        :type pac: object
        :type size: int
        """
        self.pacman = pac
        self.score = 0
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
        column: int = self.pacman.column_intention
        line: int = self.pacman.line_intention

        if 0 <= column < 28 and 0 <= line < 29:
            if self.matrix[line][column] != 1:
                self.pacman.accept_movement()

                if self.matrix[line][column] == 0:
                    self.score += 1
                    self.matrix[line][column] = 2

    def paint(self, screen: SurfaceType):
        """

        :type screen: SurfaceType
        """
        for row_number, row in enumerate(self.matrix):
            self.paint_matrix(screen, row_number, row)
        self.paint_score(screen)

    def paint_matrix(self, screen: SurfaceType, row_number: int, row: list[int | Any] | Any):
        """

        :type screen: SurfaceType
        :type row_number: int
        :type row: list[int | Any] | Any
        """
        column_number: int
        column: int

        for column_number, column in enumerate(row):
            x = column_number * self.size
            y = row_number * self.size
            half_size: int = self.size // 2
            color_rect = BLACK

            if column == 1:
                color_rect = BLUE

            pygame.draw.rect(screen, color_rect, (x, y, self.size, self.size), 0)

            if column == 0:
                pygame.draw.circle(screen, YELLOW, (x + half_size, y + half_size), self.size // 10, 0)

    def paint_score(self, screen: SurfaceType):
        columns = 30 * self.size
        img_score = font.render(f"score {self.score}", True, YELLOW)
        screen.blit(img_score, (columns, 50))

    def process_events(self, events: list[Event]):
        """

        :type events: list[Event]
        """
        for event in events:
            if event.type == pygame.QUIT:
                exit()


class Pacman(GameElements):
    """Represents the Pac-Man character.

    """
    def __init__(self, size):
        self.column: int = 1
        self.line: int = 1
        self.center_x: int = 400
        self.center_y: int = 300
        self.size: int = size
        self.speed_x: int = 0
        self.speed_y: int = 0
        self.radius: int = self.size // 2
        self.column_intention: int = self.column
        self.line_intention: int = self.line

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

    def process_events(self, events: list[Event]):
        """

        :type events: list[Event]
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.speed_x = SPEED
                    self.speed_y = 0
                elif event.key == pygame.K_LEFT:
                    self.speed_x = -SPEED
                    self.speed_y = 0
                elif event.key == pygame.K_DOWN:
                    self.speed_y = SPEED
                    self.speed_x = 0
                elif event.key == pygame.K_UP:
                    self.speed_y = -SPEED
                    self.speed_x = 0


class Ghost(GameElements):
    def __init__(self, size, color):
        self.column = 6.0
        self.line = 8.0
        self.size = size
        self.color = color

    def paint(self, screen: SurfaceType):
        slice = self.size // 8
        pixel_x = int(self.column * self.size)
        pixel_y = int(self.line * self.size)
        shape = [(pixel_x, pixel_y + self.size),
                 (pixel_x + slice, pixel_y + slice * 2),
                 (pixel_x + slice * 2, pixel_y + slice // 2),
                 (pixel_x + slice * 3, pixel_y),
                 (pixel_x + slice * 5, pixel_y),
                 (pixel_x + slice * 6, pixel_y + slice //2),
                 (pixel_x + slice * 7, pixel_y + slice * 2),
                 (pixel_x + self.size, pixel_y + self.size)]

        pygame.draw.polygon(screen, self.color, shape, 0)

        eye_external_ray = slice
        eye_inner_ray = slice // 2

        left_eye_x = int(pixel_x + slice * 2.5)
        left_eye_y = int(pixel_y + slice * 2.5)
        right_eye_x = int(pixel_x + slice * 5.5)
        right_eye_y = int(pixel_y + slice * 2.5)

        pygame.draw.circle(screen, WHITE, (left_eye_x, left_eye_y), eye_external_ray, 0)
        pygame.draw.circle(screen, BLACK, (left_eye_x, left_eye_y), eye_external_ray, 0)

        pygame.draw.circle(screen, WHITE, (right_eye_x, right_eye_y), eye_external_ray, 0)
        pygame.draw.circle(screen, BLACK, (right_eye_x, right_eye_y), eye_external_ray, 0)

    def calculate_rules(self):
        pass

    def process_events(self, events: list[Event]):
        pass


if __name__ == "__main__":
    pacman: Pacman = Pacman(SIZE)
    scenario: Scenario = Scenario(SIZE, pacman)

    while True:
        # calculate the rules
        pacman.calculate_rules()
        blinky = Ghost(SIZE, RED)
        scenario.calculate_rules()

        # paint the screen
        screen.fill(BLACK)
        scenario.paint(screen)
        pacman.paint(screen)
        blinky.paint(screen)
        pygame.display.update()
        pygame.time.delay(50)

        # captures the events
        events: list[Event] = pygame.event.get()

        pacman.process_events(events)
        scenario.process_events(events)
