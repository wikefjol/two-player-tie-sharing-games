# def predict_pure_nash_with_conjecture(R, M_A, M_B, applied_rule):
#     """
#     Predicts the number of pure Nash equilibria based on the conjecture rules.
    
#     Args:
#         R (int): Number of players in the game (R).
#         M_A (int): Number of strategies available to Player A (M_A).
#         M_B (int): Number of strategies available to Player B (M_B).
#         is_symmetric (bool): Indicates whether the game is symmetric.

#     Returns:
#         int: Predicted number of pure Nash equilibria (N_A).
#     """
#     # Ensure M_A <= M_B (without loss of generality)
#     M_A, M_B = sorted([M_A, M_B])
#     symmetric = M_A==M_B
#     # Rule A: R = 1
#     if R == 1:
#         return 1

#     # Rule B: R = 2
#     if R == 2:
#         return 4

#     # Rule C: R > 2
#     if R > 2:
#         if symmetric and M_A <= (R) // 2:
#             return 1
#         else:
#             return 0

#     # Default fallback
#     return 0

# def predict_pure_nash(R, M_A, M_B, rule):
#     """
#     Predicts the number of pure Nash equilibria based on game parameters and rule applied.

#     Args:
#         R (int): Number of players in the game.
#         M_A (int): Number of strategies available to Player A.
#         M_B (int): Number of strategies available to Player B.
#         rule (str): Rule applied to predict Nash equilibria.

#     Returns:
#         int: Predicted number of pure Nash equilibria.
#     """
#     print(rule)
#     if R == 2:
#         return 4
#     if rule in {"Rule 1", "Rule 2"}:
#         return 1
#     if rule == "Rule 3":
#         return 1 if M_A == R / 2 else 0
#     if rule in {"Rule 4", "Rule 5", "Rule 6"}:
#         return 0
#     return 0

def predict_pure_nash_with_locations(R, M_A, M_B):
    """
    Predicts the number and locations of pure Nash equilibria based on the conjecture rules.

    Args:
        R (int): Number of players in the game (R).
        M_A (int): Number of strategies available to Player A (M_A).
        M_B (int): Number of strategies available to Player B (M_B).

    Returns:
        tuple: A tuple containing:
            - int: Predicted number of pure Nash equilibria (N_A).
            - list of tuples: Predicted locations of the pure Nash equilibria.
    """
    # Ensure M_A <= M_B (without loss of generality)
    M_A, M_B = sorted([M_A, M_B])
    symmetric = M_A == M_B

    # Rule A: R = 1
    if R == 1:
        return 1, [(0, 0)], "Rule A" # One Nash equilibrium at (0, 0)

    # Rule B: R = 2
    if R == 2:
        return 4, [(0, 0), (0, 1), (1, 0), (1, 1)], "Rule B" # Four Nash equilibria at the corners of the unit square

    # Rule C: R > 2
    if R > 2:
        if symmetric and M_A <= R // 2:
            return 1, [(M_A, M_A)], "Rule Ca"  # One Nash equilibrium at (M_A, M_A)
        else:
            return 0, [], "Rule Cb"  # No pure Nash equilibria

    # Default fallback
    return 0, [], "No Rule"