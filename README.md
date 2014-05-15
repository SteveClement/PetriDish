PetriDish
=========

A cellular automata simulation engine

## Description

PetriDish is a cellular automata simlation engine written using Python 2.7.5.
It has **not** been tested in Python 3, and probably wont work.

## Dependencies

PetriDish has two main module dependencies:

* [numpy](http://www.numpy.org/)
* [pygame](http://www.pygame.org/)

## Usage

To run PetriDish, run:
`python petridish.py`
If all dependencies are met, this will spawn a GUI.

Interaction is handled by clicking in the game grid to enable or disable cells.
In addition to the buttons on the menubar, the keys `p` can be used to start or pause a simulation, `c` to clean the screen when the simulation is paused, and `q` or `Esc` to exit the program.

Rules can be submitted in either of two formats:
* `B###/S###`
* `###/###`
In this first case, `B###` specifices how many neighbors must be available to spawn a new cell at the current location, and `S###` is for how many to keep it alive.
These letters stand for *B*irth and *S*urvive, respectively.
The second format implies the same thing, but the order is reversed.
Regardless of which format you choose to use, a `/` _MUST_ be present for it to be a valid ruleset (even if you leave on side or the other empty).

Neighborhood patterns are based on the [von Neumann](http://en.wikipedia.org/wiki/Von_Neumann_neighborhood) and [Moore's](http://en.wikipedia.org/wiki/Moore_neighborhood) rules, with Moore's being the most widely used.
Additionally, the radius value is called the [Manhattan distance](http://en.wikipedia.org/wiki/Manhattan_distance) and is used to determine how many cells away from the current position is checked.
With the default radius of 1, a von Neumann neighborhood is the four directly adjacent cells to the current cell, whereas Moore's is eight, including the four diagonals.

This simulator additionally has the ability to simulate more complex CA simulations, such as [Brian's Brain](http://en.wikipedia.org/wiki/Brian%27s_Brain) which uses three cell-states, and [wireworld](http://en.wikipedia.org/wiki/Wireworld) which uses four, and can be used to simulated some very basic electronics principles.
In order to use these other rulesets, the variable `self.rulesets` must be modified accordingly.
Please see the in-line documentation for more details.
When using a ruleset with more than two states, the additional states can be set by additional clicks on the cell, with the tile color cycling through the available colors.

If colors are not your thing or you are having a hard time remembering the cell-state order, feel free to set the variable `self.cellnumbers` to `True`.

## To Do ##
-----------
- [ ] Extract UI elements into its own class, spin off into seperate file
- [ ] Maybe: separate game engine from app engine
