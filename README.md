# Two-Player Tie-Sharing Games Analysis

This repository contains a project dedicated to analyzing **two-player tie-sharing games**, a specific class of strategic games where two players compete for shared rewards. The project investigates structural patterns, reduced action spaces, and Nash equilibria through numerical simulations and rule-based predictions.

## Features
- **Numerical Simulations**: Generates game matrices and simulates two-player tie-sharing games with varying parameters.
- **Signature Reduction**: Applies Iterated Elimination of Strictly Dominated Strategies (IESDS) to identify reduced action spaces.
- **Nash Equilibria Analysis**: Computes pure strategy Nash equilibria, including their count and location.
- **Prediction Framework**: Implements rules to predict game signatures, equilibrium count, and equilibrium locations based on parameters.

---

## Project Structure
```plaintext
|-- games/                # Contains generated game matrices.
|-- logs/                 # Logs and outputs from simulations.
|-- reduced_forms/        # Simplified forms of game matrices after IESDS.
|-- src/                  # Source code for the project.
    |-- create_game.py         # Generates payoff matrices for tie-sharing games.
    |-- payoff_matrix.py       # Handles game matrices, dominated strategies, and payoffs.
    |-- predict_signature.py   # Predicts reduced signatures based on conjecture 1.
    |-- predict_nash.py        # Predicts nr of nash and locations based on conjecture 2.
    |-- psne.py                # Computes pure strategy Nash equilibria using IESDS -  from https://github.com/carlosgoe/game-theory.
    |-- nr_nash_map.py         # Generates heatmaps of Nash equilibria for various game parameters.
|-- main.py                # Orchestrates simulations, predictions, and evaluation.
|-- requirements.txt       # Python dependencies.
|-- results_all.csv        # Raw simulation results.
|-- results_all_sorted.csv # Sorted simulation results.
|-- .gitignore             # Files and directories excluded from version control.
|-- venv/                  # Virtual environment (excluded from Git).
```

---

## Installation
### Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`.

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tie-sharing-games.git
   cd tie-sharing-games
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
### Simulate Games
Run the `main.py` script to simulate games, classify reduced forms, and analyze Nash equilibria:
```bash
python main.py
```
Results will be saved in the `logs/` directory.

### Visualize Results
Generate heatmaps for Nash equilibria across parameters using `nr_nash_map.py`:
```bash
python src/nr_nash_map.py
```

---

## Results
- **Raw Results**: Contained in `results_all.csv`.
- **Sorted Results**: Contained in `results_all_sorted.csv` for easier analysis.

---

## Contribution
This project will not be maintained. 

---

## Acknowledgments
This project builds on concepts from game theory, including iterated elimination, Nash equilibria, and utility analysis. Special thanks to Carlos Goe's [game-theory](https://github.com/carlosgoe/game-theory) repository for foundational libraries.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
