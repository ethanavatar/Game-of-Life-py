# Game of Life

### An interactive pygame implementation of Conway's Game of Life

## Installation

Clone the repo and navigate into it.
```bash
git clone https://github.com/ethanavatar/Game-of-Life-py.git
cd Game-of-Life/
```

Install pygame if you don't have it already,
```bash
python -m pip install pygame
```

## Usage

Run the main module using:
```bash
python main.py
```

A window will open with an initial state and start simulating immediately.

You can also use:
 - `SPACE` to pause the simulation
 - `ESCAPE` to clear the current board
 - `R` to create a new random board
 - `LEFT MOUSE` to add or remove cells
 - `PERIOD` to pause and step one generation at a time

By default, the window is 1200x1200 pixels, the game board is 200x200 cells. It also runs as fast as it can unless the FPS cap is set manually. These constants are stored at the top of the [`App.py`](src/App.py) file if you feel like changing them.

<img title="Running Example" alt="Running Example" src="images/life-1600x900.gif">

## TODO
 - undo
### Long Term
 - Allow for easier loading of initial states, as well as premade rules
 - Allow for easier changing of the simulation's rules
 - Make it faster for bigger board sizes
    - Store the cells that changed between generations so the loop isnt going over cells that will be dead for a long time.
