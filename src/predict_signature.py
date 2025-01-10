import math

def predict_signature(R, M_A, M_B):
    """
    Returns a tuple (predicted_strategies_P1, predicted_strategies_P2, "Rule X"),
    with adjustments for symmetry (assumes M_A <= M_B) and swaps if needed.
    """

    # Ensure M_A <= M_B, and track whether swapping is needed
    
    swapped = False
    if M_A > M_B:
        M_A, M_B = M_B, M_A
        swapped = True
    debug = False
    if R==6 and M_A==7 and M_B==9:
        debug = True
        game = [R,M_A,M_B]

    # Precompute reusable values
    M_min = M_A
    M_max = M_B
    half_floor = math.floor(R / 2)
    half_ceil = math.ceil(R / 2)

    # Initialize outputs
    first_signature = None
    second_signature = None
    rule = ""
    
    # ------------------------------------------------
    # One general rule
    # ------------------------------------------------

    # ------------------------------------------------
    # Rule 1:
    # ------------------------------------------------
    symmetric = M_min == M_max
    if R<2: 
        first_signature = [0]  #From 0 to 0 
        second_signature = [0] #From 0 to 0 
        rule = "Rule 1"
        
        if debug:
            print(f"Game {game} in {rule}.")


    # ------------------------------------------------
    # Symmetric cases:
    # ------------------------------------------------
    # ------------------------------------------------
    # Rule 2: 
    # ------------------------------------------------
    if symmetric and not R<2 and M_min < R / 2:
        first_signature = [M_min]  #From M_A to M_A 
        second_signature = [M_min] #From M_A to M_A
        rule = "Rule 2"
        
        if debug:
            print(f"Game {game} in {rule}.")

    # ------------------------------------------------
    # Rule 3: 
    # ------------------------------------------------
    if symmetric and not R<2 and M_min >= R/2:
        top = min(M_min, R)
        first_signature =  list(range(0, top + 1, 1)) #from 0 to T
        second_signature = list(range(0, top + 1, 1)) #from 0 to T
        rule = "Rule 3"
        
        if debug:
            print(f"Game {game} in {rule}.")

    # ------------------------------------------------
    # Asymmetric cases:
    # ------------------------------------------------

    # ------------------------------------------------
    # Rule 4:
    # ------------------------------------------------
    if not symmetric and not R<2 and M_min < half_ceil:
        first_signature = list(range(0, M_min + 1, 1))  #from 0 to M_A
        second_signature = list(range(1, M_min + 2, 1)) #from 1 to M_A + 1
        rule = "Rule 4"

        if debug:
            print(f"Game {game} in {rule}.")
    
    # ------------------------------------------------
    # Rule 5:
    # ------------------------------------------------
    if not symmetric and not R<2 and half_ceil <= M_min and M_min < R:
        top = min(M_min, R)
        first_signature = list(range(0, top + 1, 1))      # From 0 to T'
        second_signature = list(range(0, top + 2, 1)) # From 0 to T'
        rule = "Rule 5"
        
        if debug:
            print(f"Game {game} in {rule}.")
    # ------------------------------------------------
    # Rule 6:
    # ------------------------------------------------
    if not symmetric and not R<2 and R <= M_min:
        first_signature = list(range(0, R + 1, 1))  # From 0 to R
        second_signature = list(range(0, R + 1, 1)) # From 0 to R
        rule = "Rule 6"
        
        if debug:
            print(f"Game {game} in {rule}.")
    
    # Swap back if necessary
    if swapped:
        first_signature, second_signature = second_signature, first_signature

    return (first_signature, second_signature, rule)
