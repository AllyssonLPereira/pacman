# Pac-Man em Python

Este é um jogo de Pac-Man clássico implementado em Python utilizando a biblioteca Pygame. O objetivo do jogador é coletar todas as bolinhas do labirinto enquanto evita ser capturado pelos fantasmas.

<br>

## **Instalação:**

Para executar este jogo, você precisará ter Python e Pygame instalados. Você pode instalá-los usando o pip:

```
Bash

pip install pygame
```

## **Como Executar:**

1. Clone este repositório: `git clone https://github.com/AllyssonLPereira/pacman-python.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o jogo: `python main.py`

&nbsp;
## **Como Jogar**

Utilize as setas direcionais do teclado para controlar o Pac-Man. O objetivo é comer todas as bolinhas amarelas espalhadas pelo labirinto. Evite os fantasmas, pois se forem tocados, você perderá uma vida.

&nbsp;
## **Estrutura do Código**

O código está organizado em classes para representar os diferentes elementos do jogo:

* GameElements: Classe base para todos os elementos do jogo, definindo métodos para renderização, cálculo de regras e processamento de eventos.
* Moviments: Classe base para os elementos que se movem, definindo métodos para aceitar e recusar movimentos.
* Scenario: Representa o cenário do jogo, incluindo o labirinto, as bolinhas e os personagens.
* Pacman: Representa o personagem principal, com métodos para movimento, renderização e processamento de eventos.
* Ghost: Representa os fantasmas, com métodos para movimento, renderização e inteligência artificial básica.

&nbsp;
## **Funcionalidades**

* Labirinto: Um labirinto estático gerado a partir de uma matriz, definindo as paredes e os caminhos.
* Pac-Man: O personagem principal se move pelo labirinto coletando bolinhas.
* Fantasmas: Quatro fantasmas perseguem o Pac-Man com comportamentos básicos de perseguição.
* Pontuação: A pontuação é incrementada a cada bolinha coletada e exibida na tela.
* Vidas: O jogador tem um número limitado de vidas. Ao ser capturado por um fantasma, uma vida é perdida.
* Estados do jogo: O jogo possui diferentes estados (jogando, pausado, game over, vitória).
* Colisões: O jogo detecta colisões entre o Pac-Man e os fantasmas, bem como entre os personagens e as paredes do labirinto.
---

## **Autor:**

* Allysson Pereira - Desenvolvedor principal
* Video Demo: https://youtu.be/-at8P-YUxVw
