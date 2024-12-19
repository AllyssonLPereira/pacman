import pygame
from pygame import SurfaceType, Surface
from abc import ABCMeta, abstractmethod
from pygame.event import Event
from typing import Any
import random
import math


# Pygame initialization
pygame.init()

# Game screen size
screen: Surface = pygame.display.set_mode((800, 600), 0)

# Font of texts to be displayed
font = pygame.font.SysFont("arial", 24, True, False)

# Colors
BLACK: tuple[int, int, int] = (0, 0, 0) # Background color
RED: tuple[int, int, int] = (255, 0, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
ORANGE: tuple[int, int, int] = (255, 165, 0)
YELLOW: tuple[int, int, int] = (255, 255, 0) # Color for Pac-Man
BLUE: tuple[int, int, int] = (0, 0, 255) #
CYAN: tuple[int, int, int] = (0, 255, 255)
ROSE: tuple[int, int, int] = (241, 126, 161)
WHITE: tuple[int, int, int] = (255, 255, 255)

# Character speed
SPEED: float = 0.25  # Movement speed

# Dividing the height by the number of lines
SIZE: int = 600 // 30

# Ghost movements
UP: int = 1
DOWN: int = 2
RIGHT: int = 3
LEFT: int = 4


class GameElements(metaclass=ABCMeta):
    """
    This abstract class serves as a base for all game elements, providing a common interface

    """

    # Renders the element visually onto the specified screen surface.
    @abstractmethod
    def paint(self, screen: SurfaceType):
        pass

    # Implements the specific logic and rules governing the element's
    # behavior, such as movement, interactions, and state changes.
    @abstractmethod
    def calculate_rules(self):
        pass

    # Handles events, like user input or game-related triggers, and responds accordingly.
    @abstractmethod
    def process_events(self, events: list[Event]):
        pass


class Moviments(metaclass=ABCMeta):
    """
    This abstract class defines the movement behaviors shared by game characters

    """

    # Updates the character's position based on the intended movement.
    @abstractmethod
    def accept_movement(self):
        pass

    # Rejects the intended movement and potentially chooses a new direction.
    @abstractmethod
    def refuse_movement(self):
        pass

    # Determines the possible movement paths available to the character.
    @abstractmethod
    def paths(self):
        pass


class Scenario(GameElements):
    """Represents the game scenario, including the maze, pellets, and power-ups.

    """

    def __init__(self, size: int, pac: object):
        """
        Initializes the game scenario with the following attributes:

        :type pac: object
        :type size: int
        """

        self.pacman = pac
        self.characters = []
        self.score = 0
        self.status = 1 # 0 (paused), 1 (playing), 2 (game_over), 3 (victory)
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
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 3, 3, 3, 3, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
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

    def add_characters(self, obj: object):
        """
        Appends a character object (like a ghost) to the `characters` list.

        :param obj: object - Character object to be added (e.g., Ghost)
        """

        self.characters.append(obj)

    def get_direction(self, line: int, column: int):
        """
        Takes the current row and column of a character and returns a list of possible directions the character can move based on the maze layout

        :param line: int - Row position of the character.
        :param column: int - Column position of the character.
        :return: list - List of possible directions (UP, DOWN, LEFT, RIGHT) based on open paths in the maze.
        """

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
        """
        Main game logic loop. Calls different methods based on the current game state (`status`).

        """

        if self.status == 1:
            self.calculate_rules_playing()
        elif self.status == 0:
            self.calculate_rules_paused()
        elif self.status == 2:
            self.calculate_rules_game_over()

    def calculate_rules_playing(self):
        """
        Handles logic for the playing state.
        Iterates through all characters, checks for valid movements, updates positions and
        handles collisions between Pacman and ghosts.

        """

        for character in self.characters:
            line = int(character.line)
            column = int(character.column)
            line_intention = character.line_intention
            column_intention = character.column_intention

            if line_intention > line:
                line_intention = int(math.ceil(line_intention))
            elif line_intention < line:
                line_intention = int(math.floor(line_intention))

            if column_intention > column:
                column_intention = int(math.ceil(column_intention))
            elif column_intention < column:
                column_intention = int(math.floor(column_intention))


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
                        self.matrix[int(line_intention)][int(column_intention)] != 1:
                    if isinstance(character, Ghost):
                        character.accept_movement()

                    elif isinstance(character, Pacman) and self.matrix[int(line_intention)][int(column_intention)] != 3:
                        character.accept_movement()

                    if isinstance(character, Pacman) and self.matrix[line][column] == 0:
                        self.score += 1
                        self.matrix[line][column] = 2

                        if self.score >= 306:
                            self.status = 3
                else:
                    character.refuse_movement(directions)

    def calculate_rules_paused(self):
        """
        Placeholder for logic related to the paused game state. Currently, does nothing.

        """
        pass

    def calculate_rules_game_over(self):
        """
        Placeholder for logic related to the game over state. Currently, does nothing.

        """
        pass

    def paint(self, screen: SurfaceType):
        """
        Paints the game scenario onto the Pygame screen. Calls different methods based on the current game state.

        :param screen: SurfaceType - Pygame surface object where the text will be rendered.
        """

        if self.status == 1:
            self.paint_playing(screen)
        elif self.status == 0:
            self.paint_playing(screen)
            self.paint_paused(screen)
        elif self.status == 2:
            self.paint_game_over(screen)
        elif self.status == 3:
            self.paint_victory(screen)

    @staticmethod
    def paint_text_status(screen: SurfaceType, text: str):
        """
        Helper function to render text and display it centered on the screen with a specific color.

        :param screen: SurfaceType - Pygame surface object where the text will be rendered.
        :param text: str - Text to be displayed.
        """

        img_text = font.render(text, True, YELLOW)
        position_line = ((screen.get_width() - img_text.get_width()) // 2)
        position_column = ((screen.get_height() - img_text.get_height()) // 2)

        screen.blit(img_text, (position_line, position_column))

    def paint_playing(self, screen: SurfaceType):
        """
        This function is responsible for drawing the game scene when the game is in the "playing" state (status is 1).

        :param screen: SurfaceType - Pygame surface object where the text will be rendered.
        """

        for row_number, row in enumerate(self.matrix):
            self.paint_matrix(screen, row_number, row)
        self.paint_score(screen)

    def paint_paused(self, screen: SurfaceType):
        """
        This function is called when the game is paused (status is 0).

        :param screen: SurfaceType - Pygame surface object where the text will be rendered.
        """

        self.paint_text_status(screen, "P A U S E D")

    def paint_game_over(self, screen: SurfaceType):
        """
        This function is called when the game is over (status is 2).

        :param screen: SurfaceType - Pygame surface object where the text will be rendered.
        """

        self.paint_text_status(screen, "GAME OVER")

    def paint_victory(self, screen: SurfaceType):
        """
        This function is called when the game is won (status is 3).

        :param screen: SurfaceType
        """

        self.paint_text_status(screen, "VICTORY")

    def paint_matrix(self, screen: SurfaceType, row_number: int, row: list[int | Any] | Any):
        """
        This function iterates through each cell (column) in a specific row (row_number) of the maze.

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

            if column == 3:
                pygame.draw.line(screen, WHITE, (x, y + 9), (x + self.size, y + 9), 5)

    def paint_score(self, screen: SurfaceType):
        """
        This function defines a line position for the score display.

        :param screen: SurfaceType - Pygame surface object where the text will be rendered.
        """

        line = 30 * self.size
        img_score = font.render(f"score {self.score}", True, YELLOW)
        img_life = font.render(f"Life: {self.life}", True, YELLOW)

        screen.blit(img_score, (line, 50))
        screen.blit(img_life, (line, 100))

    def process_events(self, events: list[Event]):
        """
        This function iterates through a list of Pygame events (events).

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

    This class handles the movement, animation, and visual representation of the Pacman character.
    """

    def __init__(self, size: int):
        """
        Initializes the Pacman object with the following attributes

        :param size: int - Size of each cell in the maze.
        """

        self.column: float = 1.0
        self.line: float = 1.0
        self.center_x: int = 0
        self.center_y: int = 0
        self.size: int = size
        self.speed_x: float = 0.0
        self.speed_y: float = 0.0
        self.radius: int = self.size // 2
        self.column_intention: float = self.column
        self.line_intention: float = self.line
        self.abertura = 0

    def calculate_rules(self):
        """
        Calculates the intended movement for Pacman based on speed and updates the center coordinates

        This function doesn't modify the actual position (`column` and `line`)
        until it's confirmed with `accept_movement`.
        """

        self.column_intention = self.column + self.speed_x
        self.line_intention = self.line + self.speed_y
        self.center_x = int(self.column * self.size + self.radius)
        self.center_y = int(self.line * self.size + self.radius)

    def accept_movement(self):
        """
        Updates the actual position (`column` and `line`) of Pacman to the intended position

        This function is typically called after confirming that the intended movement is valid (no collisions).
        """

        self.column = self.column_intention
        self.line = self.line_intention

    def refuse_movement(self, directions: list[int]):
        """
        Placeholder for logic when a movement is not possible due to obstacles

        :param directions: list - List of possible directions (e.g., UP, DOWN, LEFT, RIGHT) where movement is blocked.
        """

        self.column_intention = self.column
        self.line_intention = self.line

    def paths(self, directions: list[int]):
        """
        Placeholder for logic to analyze possible movement paths based on the maze layout and current direction.

        This function is not implemented and might be used for more advanced pathfinding.

        :param directions: list - List of possible directions (e.g., UP, DOWN, LEFT, RIGHT) based on the maze layout.
        """
        pass

    def paint(self, surface: SurfaceType):
        """
        Draws Pacman's body and animated mouth on the Pygame surface.

        :param surface: SurfaceType - Pygame surface object where Pacman will be drawn.
        """

        # Draw pacman's body
        pygame.draw.circle(surface, YELLOW, (self.center_x, self.center_y), self.radius, 0)

        # Animate the mouth opening
        self.abertura += 1

        if self.abertura > self.radius:
            self.abertura = 0

        # Calculate mouth corner points
        corner_mouth: tuple[int, int] = (self.center_x, self.center_y)
        upper_lip: tuple[int, int] = (self.center_x + self.radius, self.center_y - self.abertura)
        lower_lip: tuple[int, int] = (self.center_x + self.radius, self.center_y + self.abertura)

        # Draw the black mouth polygon using calculated points
        points: list[tuple[int, int]] = [corner_mouth, upper_lip, lower_lip]

        pygame.draw.polygon(screen, BLACK, points, 0)

    def process_events(self, events: list[Event]):
        """
        Processes user input events (keyboard presses) to control Pacman's movement.

        :param events: list[Event] - List of Pygame events.
        """

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.speed_x = SPEED
                    self.speed_y = 0.0
                elif event.key == pygame.K_LEFT:
                    self.speed_x = -SPEED
                    self.speed_y = 0.0
                elif event.key == pygame.K_DOWN:
                    self.speed_y = SPEED
                    self.speed_x = 0.0
                elif event.key == pygame.K_UP:
                    self.speed_y = -SPEED
                    self.speed_x = 0.0


class Ghost(GameElements):
    def __init__(self, size, color):
        """
        Initializes the ghost's attributes

        :param size: int - Size of each cell in the maze (used for ghost size).
        :param color: tuple[int, int, int] - RGB color tuple for the ghost's body.
        """

        self.column: float = 13.0
        self.line: float = 15.0
        self.column_intention: float = self.column
        self.line_intention: float = self.line
        self.speed: float = 0.75
        self.direction: int = UP
        self.size = size
        self.color: tuple[int, int, int] = color

    def paint(self, screen: SurfaceType):
        """
        Draws the ghost's shape and eyes on the Pygame surface.

        :param screen: SurfaceType - Pygame surface object where the ghost will be drawn.
        """

        piece = self.size // 8
        pixel_x = int(self.column * self.size)
        pixel_y = int(self.line * self.size)

        # Define the ghost's body shape as a list of corner coordinates
        shape = [(pixel_x, pixel_y + self.size),
                 (pixel_x + piece, pixel_y + piece * 2),
                 (pixel_x + piece * 2, pixel_y + piece // 2),
                 (pixel_x + piece * 3, pixel_y),
                 (pixel_x + piece * 5, pixel_y),
                 (pixel_x + piece * 6, pixel_y + piece //2),
                 (pixel_x + piece * 7, pixel_y + piece * 2),
                 (pixel_x + self.size, pixel_y + self.size)]

        # Draw the ghost's body as a polygon using the calculated shape
        pygame.draw.polygon(screen, self.color, shape, 0)

        # Calculate eye radius for white and black parts
        eye_external_ray = piece
        eye_inner_ray = piece // 2

        # Calculate center coordinates for each eye
        left_eye_x = int(pixel_x + piece * 2.5)
        left_eye_y = int(pixel_y + piece * 2.5)
        right_eye_x = int(pixel_x + piece * 5.5)
        right_eye_y = int(pixel_y + piece * 2.5)

        # Draw the left eye (white circle with black center)
        pygame.draw.circle(screen, WHITE, (left_eye_x, left_eye_y), eye_external_ray, 0)
        pygame.draw.circle(screen, BLACK, (left_eye_x, left_eye_y), eye_inner_ray, 0)

        # Draw the right eye (white circle with black center)
        pygame.draw.circle(screen, WHITE, (right_eye_x, right_eye_y), eye_external_ray, 0)
        pygame.draw.circle(screen, BLACK, (right_eye_x, right_eye_y), eye_inner_ray, 0)

    def calculate_rules(self):
        """
        Updates the intended position (column and line) based on the current direction and speed.

        """

        if self.direction == UP:
            self.line_intention -= self.speed
        if self.direction == DOWN:
            self.line_intention += self.speed
        if self.direction == RIGHT:
            self.column_intention += self.speed
        if self.direction == LEFT:
            self.column_intention -= self.speed

    def change_movement(self, directions: list[int]):
        """
        This method is used to randomly change the ghost's direction of movement.

        :param directions: list - List of possible directions (e.g., UP, DOWN, LEFT, RIGHT) based on the maze layout.
        """
        self.direction = random.choice(directions)

    def accept_movement(self):
        """
        This method updates the ghost's current position to the intended position.

        """
        self.column = self.column_intention
        self.line = self.line_intention

    def refuse_movement(self, directions):
        """
        This method is called when the ghost's intended movement is blocked.

        :param directions: list - List of possible directions (e.g., UP, DOWN, LEFT, RIGHT) based on the maze layout.
        """
        self.column_intention = self.column
        self.line_intention = self.line

        self.change_movement(directions)

    def paths(self, directions):
        """
        This method is similar to refuse_movement.
        It's used when the ghost has multiple possible paths and needs to choose one.

        :param directions: list - List of possible directions (e.g., UP, DOWN, LEFT, RIGHT) based on the maze layout.
        """
        self.change_movement(directions)

    def process_events(self, events: list[Event]):
        """
        This method is currently empty.
        It's a placeholder for potential future functionality that might involve
        reacting to specific events or user input.
        In this case, the ghost's movement is primarily controlled

        :param events: list[Event]
        """
        pass


if __name__ == "__main__":
    # Instantiating pacman
    pacman: Pacman = Pacman(SIZE)

    # Instantiating the ghosts
    blinky = Ghost(SIZE, RED)
    inky = Ghost(SIZE, CYAN)
    clyde = Ghost(SIZE, ORANGE)
    pinky = Ghost(SIZE, ROSE)

    # Instantiating the scenario, passing the characters
    scenario: Scenario = Scenario(SIZE, pacman)
    scenario.add_characters(pacman)
    scenario.add_characters(blinky)
    scenario.add_characters(inky)
    scenario.add_characters(clyde)
    scenario.add_characters(pinky)

    while True:
        # Calculate the rules
        pacman.calculate_rules()
        blinky.calculate_rules()
        inky.calculate_rules()
        clyde.calculate_rules()
        pinky.calculate_rules()
        scenario.calculate_rules()

        # Paint the screen
        screen.fill(BLACK)
        scenario.paint(screen)

        # Painting the pacman
        pacman.paint(screen)

        # Painting the ghosts
        blinky.paint(screen)
        inky.paint(screen)
        clyde.paint(screen)
        pinky.paint(screen)

        # Updating the scenario and adding delay
        pygame.display.update()
        pygame.time.delay(50)

        # Captures the events
        events: list[Event] = pygame.event.get()

        pacman.process_events(events)
        scenario.process_events(events)