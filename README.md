# Cellular Automata Simulator – Conway's Game of Life

This repository contains a Python project that implements **Conway's Game of Life**, a classic cellular automaton, using **PyQt5** for the graphical interface and **Matplotlib** for real-time metric visualization.

## Features

- Interactive 2D grid with click-to-toggle cells
- Start, stop, clear, and randomize the simulation
- Real-time graph showing:
  - 🔵 Live Cells: number of live cells per generation
  - 🟠 Occupancy %: percentage of the grid occupied
  - 🟢 Growth Δ: change in the number of live cells from the previous step

## What's included

This repository contains:

- ✅ Python source code for the simulator (`.py`)
- ✅ Graphical user interface built with PyQt5
- ✅ Real-time analysis plot using Matplotlib
- ✅ 📄 **PDF article** explaining the theory and implementation of Conway’s Game of Life
  - Includes background, rules, example patterns, and discussion
  - Suitable for academic use, learning, or documentation

## Requirements

Install dependencies with:

```bash
pip install PyQt5 matplotlib numpy
