import numpy as np
import csv
import os

def create_game(I, M_A, M_B, SAVE_PATH):
    """
    Generates payoff matrices for players A and B based on the game rules
    and saves them to a CSV file.

    Parameters:
    - I (int): Investment budget available to the investor.
    - M_A (int): Maximum investment for player A.
    - M_B (int): Maximum investment for player B.
    - SAVE_PATH (str): Path (including filename) to save the CSV file.
    """
    # Initialize payoff matrices
    payoff_A = np.zeros((M_A + 1, M_B + 1))
    payoff_B = np.zeros((M_A + 1, M_B + 1))

    # Compute payoffs for each combination of strategies (C_A, C_B)
    for C_A in range(M_A + 1):
        for C_B in range(M_B + 1):
            if C_A > C_B:
                payoff_A[C_A, C_B] = I - C_A
                payoff_B[C_A, C_B] = -C_B
            elif C_A < C_B:
                payoff_A[C_A, C_B] = -C_A
                payoff_B[C_A, C_B] = I - C_B
            else:  # C_A == C_B
                payoff_A[C_A, C_B] = I / 2 - C_A
                payoff_B[C_A, C_B] = I / 2 - C_B

    # Write the game to a CSV file
    # Ensure directory exists
    directory = os.path.dirname(SAVE_PATH)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(SAVE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header (player B strategies)
        header = [""]
        header.extend(range(M_B + 1))
        writer.writerow(header)

        # Write rows with player A strategies and corresponding payoffs
        for C_A in range(M_A + 1):
            row = [C_A]
            for C_B in range(M_B + 1):
                row.append(f'{payoff_A[C_A, C_B]},{payoff_B[C_A, C_B]}')
            writer.writerow(row)
