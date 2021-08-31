# Python Ant Colony Algorithm

This small project aims to reproduce the ant colony optimization algorithm. It is a technique used to solve problems which can be reduced to finding good paths through graphs.
It follows the pattern of a real ant colony. Go check this out on [Wikipedia](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms), it's really interesting!

## Description

This project is built in Python around three modules:

- The model, which contains all the interesting formulas and the interaction between the ants and their world.
- The GUI, which displays the world as a nice grid, great to see the evolution.
- The console, which runs in the background way faster and display a path as text (with some stats) when the model thinks it converged.

## Getting Started

### Dependencies

- Python 3
- Pygame library.

### Installing

- Grab the Python files from GitHub
- `pip install -r requirements.txt` in the project directory.

### Executing program

- Simply run GUI.py or Console.py (Model.py needs to be in the same folder).

```
python GUI.py
python Console.py
```

## Help

Both GUI.py and Console.py accept command line parameters to edit some constants.
Run this command to get the parameters:

```
python GUI.py -h
python GUI.py -h
```

## Authors

Thibault Nocchi
To contact me, [file an issue](https://github.com/ThibaultNocchi/Python-Ant-Colony-Algorithm/issues), thanks.

## License

This project is licensed under the Unlicense License - see the LICENSE file for details.
