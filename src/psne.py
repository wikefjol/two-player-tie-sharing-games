import numpy as np
import pandas as pd


def __show_best_responses(payoff_matrix, is_best_response):
    # convert payoff matrix to a 2d string array with best responses marked with *
    payoffs_2d = []
    for i in range(payoff_matrix.payoffs.shape[0]):
        row = []
        for j in range(payoff_matrix.payoffs.shape[1]):
            entry = '{}{},'.format(payoff_matrix.payoffs[i, j, 0], '*' if is_best_response[i, j, 0] else '')
            entry += ' {}{}'.format(payoff_matrix.payoffs[i, j, 1], '*' if is_best_response[i, j, 1] else '')
            row.append(entry)
        payoffs_2d.append(row)
    # create pandas dataframe, convert it to a string, and print it
    payoffs_df = pd.DataFrame(payoffs_2d, index=payoff_matrix.p1_strategies, columns=payoff_matrix.p2_strategies)
    print(payoffs_df.to_string() + '\n\n')


def best_responses(payoff_matrix, show_steps=True):
    log_steps = []
    def log(msg):
        if show_steps:
            print(msg)
        log_steps.append(msg)

    p1_strats = payoff_matrix.p1_strategies
    p2_strats = payoff_matrix.p2_strategies

    # First, find best responses of Player 1 to each of Player 2's strategies
    p1_best_responses = {}  # dict mapping p2_strategy -> list of p1 best responses
    for p2_s in p2_strats:
        p1_br = payoff_matrix.best_responses(player=1, opp_strategy=p2_s)
        p1_best_responses[p2_s] = p1_br
        for br_s in p1_br:
            log(f"{br_s} is player 1's best response to player 2 playing {p2_s}.")

    # Next, find best responses of Player 2 to each of Player 1's strategies
    p2_best_responses = {}  # dict mapping p1_strategy -> list of p2 best responses
    for p1_s in p1_strats:
        p2_br = payoff_matrix.best_responses(player=2, opp_strategy=p1_s)
        p2_best_responses[p1_s] = p2_br
        for br_s in p2_br:
            log(f"{br_s} is player 2's best response to player 1 playing {p1_s}.")

    # Check for pure strategy Nash equilibria:
    # A pure strategy (p1_s, p2_s) is a Nash equilibrium if p1_s is a best response to p2_s
    # AND p2_s is a best response to p1_s.
    nash_equilibria = []
    for p1_s in p1_strats:
        for p2_s in p2_strats:
            if (p1_s in p1_best_responses[p2_s]) and (p2_s in p2_best_responses[p1_s]):
                nash_equilibria.append((p1_s, p2_s))

    if nash_equilibria:
        log("Found pure strategy Nash equilibria:")
        for eq in nash_equilibria:
            log(f"NE: <{eq[0]}, {eq[1]}>")
        return (nash_equilibria, log_steps)
    else:
        log("There are no pure strategy Nash equilibria.")
        return ([], log_steps)


def IESDS(payoff_matrix, show_steps=True):
    log_steps = []
    def log(msg):
        # A small helper to either print (if show_steps) and store the msg.
        if show_steps:
            print(msg)
        log_steps.append(msg)

    # Get player 1's and player 2's dominated strategies
    p1_dominated_strategies = payoff_matrix.dominated_strategies(player=1)
    p2_dominated_strategies = payoff_matrix.dominated_strategies(player=2)

    # Print initial payoff matrix
    if show_steps:
        payoff_matrix.output()
        print()
    log_steps.append(payoff_matrix.output_to_string())  # store payoff matrix state

    # Iterate while there are dominated strategies to be eliminated
    while len(p1_dominated_strategies) > 0 or len(p2_dominated_strategies) > 0:
        if len(p1_dominated_strategies) > 0:
            # Eliminate first dominated player 1 strategy
            dominated_strategy = list(p1_dominated_strategies)[0]
            dominating_strategy = p1_dominated_strategies[dominated_strategy]
            payoff_matrix.eliminate_strategy(player=1, strategy=dominated_strategy)
            log("Player 1's strategy {} is strictly dominated by {}.\n".format(dominated_strategy, dominating_strategy))
        else:
            # Eliminate first dominated player 2 strategy
            dominated_strategy = list(p2_dominated_strategies)[0]
            dominating_strategy = p2_dominated_strategies[dominated_strategy]
            payoff_matrix.eliminate_strategy(player=2, strategy=dominated_strategy)
            log("Player 2's strategy {} is strictly dominated by {}.\n".format(dominated_strategy, dominating_strategy))

        # Update dominated strategies
        p1_dominated_strategies = payoff_matrix.dominated_strategies(player=1)
        p2_dominated_strategies = payoff_matrix.dominated_strategies(player=2)

        # Print updated payoff matrix
        if show_steps:
            payoff_matrix.output()
            print()
        log_steps.append(payoff_matrix.output_to_string())

    # If there is only one strategy left for each player, return it as a PSNE
    if len(payoff_matrix.p1_strategies) == 1 and len(payoff_matrix.p2_strategies) == 1:
        p1_strategy = payoff_matrix.p1_strategies[0]
        p2_strategy = payoff_matrix.p2_strategies[0]
        log('<{}, {}> is a pure strategy Nash equilibrium.'.format(p1_strategy, p2_strategy))
        return ([(p1_strategy, p2_strategy)], log_steps)

    # Otherwise, continue with best responses
    log('There are no strictly dominated strategies left to eliminate. Continuing with best responses...\n')
    br_results, br_log = best_responses(payoff_matrix, show_steps=show_steps)
    log_steps.extend(br_log)

    return (br_results, log_steps)
