PetriDish
=========

A cellular automata simulation engine

## Description

PetriDish is a cellular automata simlation engine written using Python 2.7.5.
It has **not** been tested in Python 3, and probably wont work.

## Dependencies

PetriDish has two main module dependencies:

* [pygame](http://www.numpy.org/)
* [numpy](http://www.pygame.org/)

## Usage

To run PetriDish, run:

`python petridish.py`

If all dependencies are met, this will spawn a GUI.

Interaction is handled by clicking in the game grid to enable or disable cells.

Rules can be in either of two formats:

* `B###/S###`
* `###/###`

## To Do ##
-----------
- [ ] Extract UI elements into its own class, spin off into seperate file
- [ ] Maybe: separate game engine from app engine
