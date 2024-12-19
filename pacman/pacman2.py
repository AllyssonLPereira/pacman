import pygame
from pygame import SurfaceType, Surface
from abc import ABCMeta, abstractmethod
from pygame.event import Event
from typing import Any
import random


# Inicialização do pygame
pygame.init()

# Tamanho da tela do jogo
screen: Surface = pygame.display.set_mode((800, 600), 0)

# Fonte dos textos a serem exibidos
font = pygame.font.SysFont("arial", 24, True, False)

# Cores
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0) # Background color
RED: tuple[int, int, int] = (255, 0, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
ORANGE: tuple[int, int, int] = (255, 165, 0)
YELLOW: tuple[int, int, int] = (255, 255, 0) # Color for Pac-Man
BLUE: tuple[int, int, int] = (0, 0, 255) #
CYAN: tuple[int, int, int] = (0, 255, 255)
ROSE: tuple[int, int, int] = (241, 126, 161)

# Velocidade dos personagens
SPEED: int = 1 # Movement speed

# Divisão da altura pelo número de linhas
SIZE: int = 600 // 30

# Movimentos do fantasma
UP: int = 1
DOWN: int = 2
RIGHT: int = 3
LEFT: int = 4


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


class Moviments(metaclass=ABCMeta):
    @abstractmethod
    def accept_movement(self):
        pass

    @abstractmethod
    def refuse_movement(self):
        pass

    @abstractmethod
    def paths(self):
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
        self.characters = []
        self.score = 0
        self.status = 1 # 0 (pausado), 1 (jogando), 2 (game_over), 3 (vitória)
        self.life = 3
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
    def add_characters(self, obj):
        self.characters.append(obj)

    def get_direction(self, line, column):
        directions = []

        if self.matrix[int(line - 1)][int(column)] != 1:
            directions.append(UP)
        if self.matrix[int(line + 1)][int(column)] != 1:
            directions.append(DOWN)
        if self.matrix[int(line)][int(column - 1)] != 1:
            directions.append(LEFT)
        if self.matrix[int(line)][int(column + 1)] != 1:
            directions.append(RIGHT)

        return directions

    def calculate_rules(self):
        if self.status == 1:
            self.calculate_rules_playing()
        elif self.status == 0:
            self.calculate_rules_paused()
        elif self.status == 2:
            self.calculate_rules_game_over()

    def calculate_rules_playing(self):
        for character in self.characters:
            line = int(character.line)
            column = int(character.column)
            line_intention = int(character.line_intention)
            column_intention = int(character.column_intention)

            directions = self.get_direction(line, column)

            if len(directions) >= 3:
                character.paths(directions)

            if isinstance(character, Ghost) and \
                    character.line == self.pacman.line and character.column == self.pacman.column:
                self.life -= 1

                if self.life <= 0:
                    self.status = 2

                else:
                    self.pacman.line = 1
                    self.pacman.column = 1

            else:
                if 0 <= column_intention < 28 and 0 <= line_intention < 29 and \
                        self.matrix[line_intention][column_intention] != 1:
                    character.accept_movement()

                    if isinstance(character, Pacman) and self.matrix[line][column] == 0:
                        self.score += 1
                        self.matrix[line][column] = 2

                        if self.score >= 306:
                            self.status = 3

                else:
                    character.refuse_movement(directions)

    def calculate_rules_paused(self):
        pass

    def calculate_rules_game_over(self):
        pass

    def paint(self, screen):
        if self.status == 1:
            self.paint_playing(screen)
        elif self.status == 0:
            self.paint_playing(screen)
            self.paint_paused(screen)
        elif self.status == 2:
            self.paint_playing(screen)
            self.paint_game_over(screen)
        elif self.status == 3:
            self.paint_playing(screen)
            self.paint_victory(screen)

    @staticmethod
    def paint_text_status(screen, text):
        img_text = font.render(text, True, YELLOW)
        position_line = ((screen.get_width() - img_text.get_width()) // 2)
        position_column = ((screen.get_height() - img_text.get_height()) // 2)

        screen.blit(img_text, (position_line, position_column))

    def paint_playing(self, screen: SurfaceType):
        """

        :type screen: SurfaceType
        """
        for row_number, row in enumerate(self.matrix):
            self.paint_matrix(screen, row_number, row)
        self.paint_score(screen)

    def paint_paused(self, screen):
        self.paint_text_status(screen, "P A U S E D")

    def paint_game_over(self, screen):
        self.paint_text_status(screen, "GAME OVER")

    def paint_victory(self, screen):
        self.paint_text_status(screen, "VICTORY")

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

            pygame.draw.rect(screen, color_rect, (x, y, self.size, self.size), 1, border_radius=5)

            if column == 0:
                pygame.draw.circle(screen, YELLOW, (x + half_size, y + half_size), self.size // 10, 0)

    def paint_score(self, screen: SurfaceType):
        line = 30 * self.size
        img_score = font.render(f"score {self.score}", True, YELLOW)
        img_life = font.render(f"Life: {self.life}", True, YELLOW)

        screen.blit(img_score, (line, 50))
        screen.blit(img_life, (line, 100))

    def process_events(self, events: list[Event]):
        """

        :type events: list[Event]
        """
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.status == 0:
                        self.status = 1
                    else:
                        self.status = 0


class Pacman(GameElements, Moviments):
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
        self.abertura = 0

    def calculate_rules(self):
        self.column_intention = self.column + self.speed_x
        self.line_intention = self.line + self.speed_y
        self.center_x = int(self.column * self.size + self.radius)
        self.center_y = int(self.line * self.size + self.radius)

    def accept_movement(self):
        self.column = self.column_intention
        self.line = self.line_intention

    def refuse_movement(self, directions):
        self.column_intention = self.column
        self.line_intention = self.line

    def paths(self, directions):
        pass

    def paint(self, surface: SurfaceType):
        """

        :type surface: SurfaceType
        """
        # draw pacman's body
        pygame.draw.circle(surface, YELLOW, (self.center_x, self.center_y), self.radius, 0)

        self.abertura += 1

        if self.abertura > self.radius:
            self.abertura = 0

        # draw the mouth
        corner_mouth: tuple[int, int] = (self.center_x, self.center_y)
        upper_lip: tuple[int, int] = (self.center_x + self.radius, self.center_y - self.abertura)
        lower_lip: tuple[int, int] = (self.center_x + self.radius, self.center_y + self.abertura)

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
        self.column = 13.0
        self.line = 15.0
        self.column_intention = self.column
        self.line_intention = self.line
        self.speed = 1
        self.direction = UP
        self.size = size
        self.color = color

    def paint(self, screen: SurfaceType):
        piece = self.size // 8
        pixel_x = int(self.column * self.size)
        pixel_y = int(self.line * self.size)

        # Forma do fantasma
        shape = [(pixel_x, pixel_y + self.size),
                 (pixel_x + piece, pixel_y + piece * 2),
                 (pixel_x + piece * 2, pixel_y + piece // 2),
                 (pixel_x + piece * 3, pixel_y),
                 (pixel_x + piece * 5, pixel_y),
                 (pixel_x + piece * 6, pixel_y + piece //2),
                 (pixel_x + piece * 7, pixel_y + piece * 2),
                 (pixel_x + self.size, pixel_y + self.size)]

        # Desenhar a forma do fantasma
        pygame.draw.polygon(screen, self.color, shape, 0)

        # Criar o raio da parte branca e preta do olho
        eye_external_ray = piece
        eye_inner_ray = piece // 2

        # Criar do centro do olho esquerdo
        left_eye_x = int(pixel_x + piece * 2.5)
        left_eye_y = int(pixel_y + piece * 2.5)

        # Criar do centro do olho direito
        right_eye_x = int(pixel_x + piece * 5.5)
        right_eye_y = int(pixel_y + piece * 2.5)

        # Desenhar o olho esquerdo
        pygame.draw.circle(screen, WHITE, (left_eye_x, left_eye_y), eye_external_ray, 0)
        pygame.draw.circle(screen, BLACK, (left_eye_x, left_eye_y), eye_inner_ray, 0)

        # Desenhar o olho direito
        pygame.draw.circle(screen, WHITE, (right_eye_x, right_eye_y), eye_external_ray, 0)
        pygame.draw.circle(screen, BLACK, (right_eye_x, right_eye_y), eye_inner_ray, 0)

    def calculate_rules(self):
        if self.direction == UP:
            self.line_intention -= self.speed
        if self.direction == DOWN:
            self.line_intention += self.speed
        if self.direction == RIGHT:
            self.column_intention += self.speed
        if self.direction == LEFT:
            self.column_intention -= self.speed

    def change_movement(self, directions):
        self.direction = random.choice(directions)

    def accept_movement(self):
        self.column = self.column_intention
        self.line = self.line_intention

    def refuse_movement(self, directions):
        self.column_intention = self.column
        self.line_intention = self.line

        self.change_movement(directions)

    def paths(self, directions):
        self.change_movement(directions)

    def process_events(self, events: list[Event]):
        pass


if __name__ == "__main__":
    # Instanciando o pacman
    pacman: Pacman = Pacman(SIZE)

    # Instanciando os fantasmas
    blinky = Ghost(SIZE, RED)
    inky = Ghost(SIZE, CYAN)
    clyde = Ghost(SIZE, ORANGE)
    pinky = Ghost(SIZE, ROSE)

    # Instanciando o cenário, passando os personagens
    scenario: Scenario = Scenario(SIZE, pacman)
    scenario.add_characters(pacman)
    scenario.add_characters(blinky)
    scenario.add_characters(inky)
    scenario.add_characters(clyde)
    scenario.add_characters(pinky)

    while True:
        # calculate the rules
        pacman.calculate_rules()
        blinky.calculate_rules()
        inky.calculate_rules()
        clyde.calculate_rules()
        pinky.calculate_rules()
        scenario.calculate_rules()

        # paint the screen
        screen.fill(BLACK)
        scenario.paint(screen)

        # pintando o pacman
        pacman.paint(screen)

        # pintando os fantasmas
        blinky.paint(screen)
        inky.paint(screen)
        clyde.paint(screen)
        pinky.paint(screen)

        # Atualizando o cenário e colocando delay
        pygame.display.update()
        pygame.time.delay(50)

        # captures the events
        events: list[Event] = pygame.event.get()

        pacman.process_events(events)
        scenario.process_events(events)