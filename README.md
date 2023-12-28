# Chinese Chess AI

This is the project about creating a simple Chinese Chess AI using for education purpose in module *IT3160E - Introduction to AI* of Hanoi University of Science and Technology

## Table of Contents
- [Chinese Chess AI](#chinese-chess-ai)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [How to use](#how-to-use)
    - [Python guide:](#python-guide)
    - [PyPy guide:](#pypy-guide)
  - [Details about our code](#details-about-our-code)
    - [game\_state.py:](#game_statepy)
    - [game\_tree.py:](#game_treepy)
    - [gui\_utilities.py:](#gui_utilitiespy)
    - [main.py:](#mainpy)
    - [node.py:](#nodepy)
    - [piece.py:](#piecepy)
    - [resources.py:](#resourcespy)
    - [team.py:](#teampy)

## Introduction

Chinese chess, also known as Xiangqi, is a popular two-player board game in China, dating back to the Song Dynasty. The game is played on a battlefield-like board with a river in the middle. Each player has a set of pieces: one General, two Horses, two Elephants, two Advisors, two Rooks, two Cannons, and five Pawns. Each piece has its own movement rules and strategic role in the game. The objective is to capture the opponent’s General or immobilize the opponent’s pieces.

We aim to develop an intelligent program that can play Chinese chess. The goal is to make the program’s decisions as rational as possible, comparable to intermediate or experienced human players. To achieve this, several methods were implemented, including a heuristic function for rating game states, the Minimax algorithm with Alpha-Beta pruning, and the Monte Carlo Tree Search (MCTS). Variants of these algorithms were also explored.

## Features

We have incorporated a user interface (UI) using Pygame to enhance the visualization of the game, improve testing capabilities, and increase user-friendliness. Two game modes are available: PvE Mode, where a human player competes against our bot, providing a realistic gaming experience and serving as the primary interface for testing against previous Chinese chess-playing machines and experienced players. The EvE Mode involves two bots playing against each other on the computer, with a selected value pack and search depth for each bot.

## How to use

For optimal performance, we strongly advise executing our code using the Pypy compiler. Utilizing Pypy can enhance performance by 2-3 times for each operation. It's worth noting that all results presented in our report were obtained using Pypy for measurement purposes. Nevertheless, you can still execute this code in Python with a reduced performance level. Below is a step-by-step installation guide:

### Python guide:
1. Clone the repository:
```bash
git clone https://github.com/auphong2707/chinese-chess-ai-agent.git
```
2. Navigate to the project directory:
```bash
cd chinese-chess-ai-agent
```
3. Intall required modules:
```bash
pip install -q -r requirements.txt
```
4. Run the game:
```bash
python main.py
```
### PyPy guide:
1. Clone the repository:
```bash
git clone https://github.com/auphong2707/chinese-chess-ai-agent.git
```
2. Navigate to the project directory:
```bash
cd chinese-chess-ai-agent
```
3. Prepare PyPy **(for Window user)**:
- For **Command Prompt (Powershell)**
```bash
curl -o pypy3.10-v7.3.14-win64.zip https://downloads.python.org/pypy/pypy3.10-v7.3.14-win64.zip
tar -xf pypy3.10-v7.3.14-win64.zip
ren pypy3.10-v7.3.14-win64 pypy
pypy\pypy.exe -m ensurepip
pypy\pypy.exe -m pip install pygame-ce
```
- For **Git Bash**
```bash
curl -O https://downloads.python.org/pypy/pypy3.10-v7.3.14-win64.zip
unzip pypy3.10-v7.3.14-win64.zip
mv pypy3.10-v7.3.14-win64 pypy
pypy/pypy.exe -m ensurepip
pypy/pypy.exe -m pip install pygame-ce
```
4. Run the game
- For **Command Prompt (Powershell)**
```bash
pypy\pypy.exe main.py
```
- For **Git Bash**
```bash
pypy/pypy.exe main.py
```
**Notice**: At step 3, if you are using an OS other than Windows, you may need to download Pypy from [here](https://www.pypy.org/download.html), and add the extracted folder to PATH. Atfer that, you need to install the Pygame community edition by using these commands:
```bash
pypy -m ensurepip
pypy -m pip install pygame-ce
```
Finally, you can run the game:
```bash
pypy main.py
```

## Details about our code
To clearly understand our code structure, we highly recommend taking a glance at our UML diagram. Please find the link here for easy navigation: [Link to UML Diagram](https://lucid.app/lucidchart/ec68185f-a423-46e4-ae54-d047a4e859fc/edit?invitationId=inv_6149075f-f988-44a2-bd3b-41b02c10e651&page=0_0#).

### game_state.py:
This module represents the game state. It includes methods for evaluating the game state, generating possible moves, and handling game progression.

### game_tree.py:
This module defines several classes representing game trees.

### gui_utilities.py:
This module contains essential components for building the UI, including buttons, dropdown lists, and input boxes.

### main.py:
This module creates the user interface (UI).

### node.py:
This module defines classes for creating nodes in a game tree.

### piece.py:
This module provides classes for specific chess pieces like Advisor, Cannon, Rook, Elephant, General, Pawn, and Horse, each inheriting from the abstract Piece class.

### resources.py:
This module handles image processing tasks and various conversion functions.

### team.py:
This module represents different teams in a game.

