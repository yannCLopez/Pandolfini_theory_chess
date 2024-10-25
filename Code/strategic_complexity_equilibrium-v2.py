import numpy as np
from itertools import product
from collections import defaultdict

def F(M, q, tau, b_Ss, b_Sc, b_Cs, b_Cc):
    if M == 'S' and q == 's':
        return tau + (1 - tau) * b_Ss
    elif M == 'S' and q == 'c':
        return tau + (1 - tau) * b_Sc
    elif M == 'C' and q == 's':
        return tau + (1 - tau) * b_Cs
    elif M == 'C' and q == 'c':
        return tau + (1 - tau) * b_Cc

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
    for strategy_profile in product(strategies, repeat=2):
        if is_equilibrium(strategy_profile, tau, b_Ss, b_Sc, b_Cs, b_Cc):
            equilibria.append(strategy_profile)
    return equilibria

def main():
    tau = 0.05
    equilibria_data = defaultdict(lambda: {'count': 0, 'params': {'b_Ss': [], 'b_Sc': [], 'b_Cs': [], 'b_Cc': []}})
    
    # Grid search
    for b_Ss in np.arange(0.01, 0.99, 0.01):
        for b_Cs in np.arange(b_Ss + 0.01, 0.99, 0.01):
            for b_Sc in np.arange(0.01, 0.99, 0.01):
                for b_Cc in np.arange(b_Sc + 0.01, 0.99, 0.01):
                    equilibria = find_equilibria(tau, b_Ss, b_Sc, b_Cs, b_Cc)
                    for eq in equilibria:
                        equilibria_data[eq]['count'] += 1
                        equilibria_data[eq]['params']['b_Ss'].append(b_Ss)
                        equilibria_data[eq]['params']['b_Sc'].append(b_Sc)
                        equilibria_data[eq]['params']['b_Cs'].append(b_Cs)
                        equilibria_data[eq]['params']['b_Cc'].append(b_Cc)

    print("All Pure Strategy Equilibria:")
    for eq, data in equilibria_data.items():
        print(f"\nEquilibrium: {eq}")
        print(f"Occurrences: {data['count']}")
        print("Parameter Ranges:")
        for param, values in data['params'].items():
            if values:
                print(f"  {param}: [{min(values):.2f}, {max(values):.2f}]")
            else:
                print(f"  {param}: No occurrences")

    # Check if (CC, SS) or equivalent payoff equilibrium exists
    # (CC, SS), (CS, SS), (CC,CS), (SC,CS), (CS,CS)

    cc_ss_equilibrium = equilibria_data[('CC', 'SS')]
    cs_ss_equilibrium = equilibria_data[('CS', 'SS')]
    cc_cs_equilibrium = equilibria_data[('CC', 'CS')]
    sc_cs_equilibrium = equilibria_data[('SC', 'CS')]
    cs_cs_equilibrium = equilibria_data[('CS', 'SS')]

    if cc_ss_equilibrium['count'] > 0:
        print("\n(CC, SS) is an equilibrium in some parameter ranges.")
    elif cs_ss_equilibrium['count'] > 0:
        print("\n(CS, SS) is an equilibrium in some parameter ranges.")
    elif cc_cs_equilibrium['count'] > 0:
        print("\n(CC, CS) is an equilibrium in some parameter ranges.")
    elif sc_cs_equilibrium['count'] > 0:
        print("\n(SC, CS) is an equilibrium in some parameter ranges.")
    elif cs_cs_equilibrium['count'] > 0:
        print("\n(CS, CS) is an equilibrium in some parameter ranges.")
    else:
        print("\n An equilibrium with the same payoff as(CS, CS) never occurs.")


if __name__ == "__main__":
    main()



# Check if my grid search algorithm is good.
# Create a code that allows me to give parameters and search for any profitable deviations.
# When does the code end?
# Ask it to print something anytime a suitable equilibrium is found