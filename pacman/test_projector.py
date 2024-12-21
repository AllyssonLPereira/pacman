import pytest
from project import Pacman, Ghost, Scenario

UP: int = 1

def test_pacman_initialization():
    pacman = Pacman(20)
    assert pacman.column == 1.0
    assert pacman.line == 1.0
    assert pacman.size == 20

def test_ghost_movement():
    ghost = Ghost(20, (255, 0, 0))
    ghost.direction = UP
    ghost.calculate_rules()
    assert ghost.line_intention < ghost.line

def test_pacman_ghost_collision():
    pacman = Pacman(20)
    ghost = Ghost(20, (255, 0, 0))

    # Posicione o Pac-Man e o fantasma para simular uma colisão
    pacman.column = 10
    pacman.line = 10
    ghost.column = 10
    ghost.line = 10
    scenario = Scenario(20, pacman)
    scenario.add_characters(ghost)
    scenario.calculate_rules()

    # Verifique se a vida do Pac-Man diminuiu
    assert scenario.life == 2