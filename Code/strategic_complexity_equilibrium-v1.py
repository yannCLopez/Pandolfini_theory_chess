import numpy as np
from itertools import product

def F(M, q, tau, b_Ss, b_Sc, b_Cs, b_Cc):
    if M == 'S' and q == 's':
        return tau + (1 - tau) * b_Ss
    elif M == 'S' and q == 'c':
        return tau + (1 - tau) * b_Sc
    elif M == 'C' and q == 's':
        return tau + (1 - tau) * b_Cs
    elif M == 'C' and q == 'c':
        return tau + (1 - tau) * b_Cc

# Checked
def payoff(strategy_profile, tau, b_Ss, b_Sc, b_Cs, b_Cc):
    if strategy_profile in [('SS','SS'), ('SS','SC'), ('SC','SS'), ('SC','SC')]:
        return (tau + (1-tau)*(1-b_Ss)*F('S','s',tau,b_Ss,b_Sc,b_Cs,b_Cc)) / (tau + (1-tau)*(b_Ss+(1-b_Ss)*F('S','s',tau,b_Ss,b_Sc,b_Cs,b_Cc)))
    elif strategy_profile in [('CC','CC'), ('SC','CC'), ('CC','SC')]:
        return (tau + (1-tau)*(1-b_Cc)*F('C','c',tau,b_Ss,b_Sc,b_Cs,b_Cc)) / (tau + (1-tau)*(b_Cc+(1-b_Cc)*F('C','c',tau,b_Ss,b_Sc,b_Cs,b_Cc)))
    elif strategy_profile in [('SS','CC'), ('SS','CS'), ('CS','CC'), ('CS','SC')]:
        return (tau + (1-tau)*(1-b_Sc)*F('C','s',tau,b_Ss,b_Sc,b_Cs,b_Cc)) / (tau + (1-tau)*(b_Sc+(1-b_Sc)*F('C','s',tau,b_Ss,b_Sc,b_Cs,b_Cc)))
    elif strategy_profile in [('CC','SS'), ('CS','SS'), ('CC','CS'), ('SC','CS'), ('CS','CS')]:
        return (tau + (1-tau)*(1-b_Cs)*F('S','c',tau,b_Ss,b_Sc,b_Cs,b_Cc)) / (tau + (1-tau)*(b_Cs+(1-b_Cs)*F('S','c',tau,b_Ss,b_Sc,b_Cs,b_Cc)))

def is_equilibrium(strategy_profile, tau, b_Ss, b_Sc, b_Cs, b_Cc):
    player1_strategy, player2_strategy = strategy_profile
    equilibrium_payoff = payoff(strategy_profile, tau, b_Ss, b_Sc, b_Cs, b_Cc)
    
    # Check Player 1's deviations
    for player1_deviation in ['SS', 'SC', 'CS', 'CC']:
        if payoff((player1_deviation, player2_strategy), tau, b_Ss, b_Sc, b_Cs, b_Cc) > equilibrium_payoff:
            return False
    
    # Check Player 2's deviations
    for player2_deviation in ['SS', 'SC', 'CS', 'CC']:
        if payoff((player1_strategy, player2_deviation), tau, b_Ss, b_Sc, b_Cs, b_Cc) < equilibrium_payoff:
            return False
    
    return True

def find_equilibria(tau, b_Ss, b_Sc, b_Cs, b_Cc):
    strategies = ['SS', 'SC', 'CS', 'CC']
    equilibria = []
    # product(strategies, repeat=2) generates all possible combinations of two strategies, one for each player. The repeat=2 argument tells the function to use the strategies list twice (once for each player).
    for strategy_profile in product(strategies, repeat=2):
        if is_equilibrium(strategy_profile, tau, b_Ss, b_Sc, b_Cs, b_Cc):
            equilibria.append(strategy_profile)
    return equilibria

def main():
    tau = 0.05
    cc_ss_payoff = None
    cc_ss_params = None
    
    # Grid search
    for b_Ss in np.arange(0.01, 0.99, 0.01):
        for b_Cs in np.arange(b_Ss + 0.01, 0.99, 0.01):
            for b_Sc in np.arange(0.01, 0.99, 0.01):
                for b_Cc in np.arange(b_Sc + 0.01, 0.99, 0.01):
                    equilibria = find_equilibria(tau, b_Ss, b_Sc, b_Cs, b_Cc)
                    for eq in equilibria:
                        eq_payoff = payoff(eq, tau, b_Ss, b_Sc, b_Cs, b_Cc)
                        # "or" statement to allow for rounding errors.
                        if eq == ('CC', 'SS') or abs(eq_payoff - payoff(('CC', 'SS'), tau, b_Ss, b_Sc, b_Cs, b_Cc)) < 1e-6:
                            cc_ss_payoff = eq_payoff
                            cc_ss_params = (tau, b_Ss, b_Sc, b_Cs, b_Cc)
                            print(f"Equilibrium with (CC, SS) payoff found: {eq}")
                            print(f"Parameters: tau={tau}, b_Ss={b_Ss}, b_Sc={b_Sc}, b_Cs={b_Cs}, b_Cc={b_Cc}")
                            print(f"Payoff: {eq_payoff}")
                            return

    if cc_ss_payoff is None:
        print("No equilibrium with (CC, SS) payoff found.")
        print("Analyzing deviations...")
        
        # Deviation Analysis
# This section analyzes why (CC, SS) is not an equilibrium (or why no equilibrium 
# with the same payoff exists) by examining profitable deviations across the parameter space.

# 1. Initialize a dictionary to count profitable deviations for each possible move.

# 2. Iterate over all valid parameter combinations (b_Ss, b_Sc, b_Cs, b_Cc).

# 3. For each parameter combination:
#    a) Calculate the payoff of (CC, SS)
#    b) Check if Player 1 can profitably deviate to CS, SC, or SS
#    c) Check if Player 2 can profitably deviate to SC, CS, or CC
#    Increment the respective counter for each profitable deviation.

# 4. Print the count of profitable deviations for each move.

        deviations = {
            'Player 1 to CS': 0,
            'Player 1 to SC': 0,
            'Player 1 to SS': 0,
            'Player 2 to SC': 0,
            'Player 2 to CS': 0,
            'Player 2 to CC': 0
        }
        
        for b_Ss in np.arange(0.01, 0.99, 0.01):
            for b_Cs in np.arange(b_Ss + 0.01, 0.99, 0.01):
                for b_Sc in np.arange(0.01, 0.99, 0.01):
                    for b_Cc in np.arange(b_Sc + 0.01, 0.99, 0.01):
                        cc_ss_payoff = payoff(('CC', 'SS'), tau, b_Ss, b_Sc, b_Cs, b_Cc)
                        
                        if payoff(('CS', 'SS'), tau, b_Ss, b_Sc, b_Cs, b_Cc) > cc_ss_payoff:
                            deviations['Player 1 to CS'] += 1
                        if payoff(('SC', 'SS'), tau, b_Ss, b_Sc, b_Cs, b_Cc) > cc_ss_payoff:
                            deviations['Player 1 to SC'] += 1
                        if payoff(('SS', 'SS'), tau, b_Ss, b_Sc, b_Cs, b_Cc) > cc_ss_payoff:
                            deviations['Player 1 to SS'] += 1
                        if payoff(('CC', 'SC'), tau, b_Ss, b_Sc, b_Cs, b_Cc) < cc_ss_payoff:
                            deviations['Player 2 to SC'] += 1
                        if payoff(('CC', 'CS'), tau, b_Ss, b_Sc, b_Cs, b_Cc) < cc_ss_payoff:
                            deviations['Player 2 to CS'] += 1
                        if payoff(('CC', 'CC'), tau, b_Ss, b_Sc, b_Cs, b_Cc) < cc_ss_payoff:
                            deviations['Player 2 to CC'] += 1
        
        print("Deviation analysis:")
        for deviation, count in deviations.items():
            print(f"{deviation}: {count}")

if __name__ == "__main__":
    main()