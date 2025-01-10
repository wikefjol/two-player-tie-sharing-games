import os
import csv
import pandas as pd
from src.payoff_matrix import PayoffMatrix
from src.psne import IESDS
from src.create_game import create_game
from src.predict_signature import predict_signature
from src.predict_nash import predict_pure_nash_with_locations


def print_rule_performance(performance_dict):
    """
    Prints the accuracy of predictions for each rule based on the performance dictionary.

    Args:
        performance_dict (dict): A dictionary containing performance statistics for each rule.
    """
    for rule, counts in performance_dict.items():
        total = counts["correct"] + counts["incorrect"]
        accuracy = counts["correct"] / total if total > 0 else 0
        print(f"{rule}: Correct = {counts['correct']}, Incorrect = {counts['incorrect']}, Accuracy = {accuracy:.2%}")
        

def sort_csv_by_columns(input_csv):
    """
    Sorts a CSV file by specified columns and saves the sorted file with "_sorted" appended to the filename.
    
    Args:
        input_csv (str): Path to the input CSV file.
    """
    data = pd.read_csv(input_csv)
    sorted_data = data.sort_values(by=["SigRuleUsed", "R", "M_A", "M_B"], ascending=True)
    sorted_csv_path = input_csv.replace(".csv", "_sorted.csv")
    sorted_data.to_csv(sorted_csv_path, index=False)
    print(f"Sorted results saved to: {sorted_csv_path}")

def simulate_games_with_nash_predictions(mode="all"):
    """
    Simulates games, evaluates Nash equilibrium predictions, and logs the results.
    
    Args:
        mode (str): Game mode, either "all", "symmetric", or "asymmetric".
    """
    # Directory and file paths
    games_dir = "./games"
    logs_dir = "./logs"
    results_csv = f"results_{mode}.csv"

    os.makedirs(games_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    # Parameter ranges
    max_players, max_M_A, max_M_B = 10, 10, 10
    player_range = range(1, max_players)
    strategy_a_range = range(1, max_M_A)

    # Performance trackers for different prediction types
    rule_performance_signature = {}
    rule_performance_nash_count = {}
    rule_performance_nash_location = {}

    with open(results_csv, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            "R", "M_A", "M_B",
            "PredictedSignature", "TrueSignature", "SigPredTrue?", "SigRuleUsed",
            "PredictedNumPureNash", "TrueNumPureNash", "NumPredTrue?", "NumRuleUsed",
            "PredNashLoc", "TrueNashLoc", "LocPredTrue?", "LocRuleUsed"
        ])

        for R in player_range:
            for M_A in strategy_a_range:
                for M_B in range(M_A, max_M_B):
                    if mode == "symmetric" and M_A != M_B:
                        continue
                    if mode == "asymmetric" and M_A == M_B:
                        continue

                    game_filename = f"{R}_{M_A}_{M_B}.csv"
                    game_path = os.path.join(games_dir, game_filename)

                    if not os.path.exists(game_path):
                        create_game(R, M_A, M_B, SAVE_PATH=game_path)

                    # Predict signature and rule
                    predicted_p1, predicted_p2, sig_rule_used = predict_signature(R, M_A, M_B)
                    predicted_signature = (sorted(predicted_p1 or []), sorted(predicted_p2 or []))

                    # Load game and calculate Nash equilibria
                    game_instance = PayoffMatrix(file_source=game_path)
                    equilibrium_results, _ = IESDS(game_instance, show_steps=False)
                    equilibrium_results = [(int(eq[0]), int(eq[1])) for eq in equilibrium_results]

                    num_nash_equilibria = len(equilibrium_results)
                    true_signature = (
                        sorted([int(s) for s in game_instance.p1_strategies]),
                        sorted([int(s) for s in game_instance.p2_strategies])
                    )

                    # Predict the number and locations of pure Nash equilibria
                    predicted_nash_count, predicted_nash_locs, nash_rule_used = predict_pure_nash_with_locations(R, M_A, M_B)
                    predicted_nash_locs_str = str(predicted_nash_locs)
                    true_nash_locs_str = str(equilibrium_results)

                    # Determine prediction correctness
                    sig_pred_correct = "Yes" if predicted_signature == true_signature else "No"
                    num_pred_correct = "Yes" if predicted_nash_count == num_nash_equilibria else "No"
                    loc_pred_correct = "Yes" if predicted_nash_locs_str == true_nash_locs_str else "No"

                    # Update performance trackers
                    for rule, correct, tracker in [
                        (sig_rule_used, sig_pred_correct, rule_performance_signature),
                        (nash_rule_used, num_pred_correct, rule_performance_nash_count),
                        (nash_rule_used, loc_pred_correct, rule_performance_nash_location)
                    ]:
                        if rule not in tracker:
                            tracker[rule] = {"correct": 0, "incorrect": 0}
                        if correct == "Yes":
                            tracker[rule]["correct"] += 1
                        else:
                            tracker[rule]["incorrect"] += 1

                    # Write results to CSV
                    csv_writer.writerow([
                        R, M_A, M_B,
                        str(predicted_signature), str(true_signature), sig_pred_correct, sig_rule_used,
                        predicted_nash_count, num_nash_equilibria, num_pred_correct, nash_rule_used,
                        predicted_nash_locs_str, true_nash_locs_str, loc_pred_correct, nash_rule_used
                    ])

    # Print accuracy for each prediction type
    print("\n=== Signature Prediction Accuracy ===")
    print_rule_performance(rule_performance_signature)

    print("\n=== Nash Count Prediction Accuracy ===")
    print_rule_performance(rule_performance_nash_count)

    print("\n=== Nash Location Prediction Accuracy ===")
    print_rule_performance(rule_performance_nash_location)

    print(f"Results saved to {results_csv}.")
    sort_csv_by_columns(results_csv)

if __name__ == "__main__":
    simulate_games_with_nash_predictions(mode="all")
