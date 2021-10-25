# Game of Life

### A pygame implementation of the Conway's Game of Life

## Installation

Clone the repo and navigate into it.
```bash
git clone https://github.com/ethanavatar/Game-of-Life.git
cd Game-of-Life/
```

Install pygame if you don't have it already,
```bash
python -m pip install pygame
```

## Usage

Run the source file using:
```bash
python Life.py
```

A window will open with a random initial state and start simulating immediately.

You can also use:
 - `SPACE` to pause the simulation
 - `ESCAPE` to clear the current board
 - `R` to create a new random board
 - `LEFT MOUSE` to add or remove cells

By default, the window is 1600x900 pixels, the game board is 160x90 cells, and it runs at 24 FPS. These constants are stored at the top of the source file if you feel like changing them.

<img title="Running Example" alt="Running Example" src="images/life.gif">

## TODO

 - Allow for easier loading of initial states, as well as premade rules
 - Allow for easier changing of the simulation's rules
 - Make it faster for bigger board sizes