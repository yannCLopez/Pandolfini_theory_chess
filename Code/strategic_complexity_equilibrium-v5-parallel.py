# CHANGE FILE PATH!

import numpy as np
from itertools import product
from collections import defaultdict
from sklearn.model_selection import ParameterGrid
import multiprocessing as mp
import csv
from tqdm import tqdm


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
        result = (tau + (1-tau)*(1-b_Ss)*F('S','s',tau,b_Ss,b_Sc,b_Cs,b_Cc)) / (tau + (1-tau)*(b_Ss+(1-b_Ss)*F('S','s',tau,b_Ss,b_Sc,b_Cs,b_Cc)))
    elif strategy_profile in [('CC','CC'), ('SC','CC'), ('CC','SC')]:
        result = (tau + (1-tau)*(1-b_Cc)*F('C','c',tau,b_Ss,b_Sc,b_Cs,b_Cc)) / (tau + (1-tau)*(b_Cc+(1-b_Cc)*F('C','c',tau,b_Ss,b_Sc,b_Cs,b_Cc)))
    elif strategy_profile in [('SS','CC'), ('SS','CS'), ('CS','CC'), ('CS','SC')]:
        result = (tau + (1-tau)*(1-b_Sc)*F('C','s',tau,b_Ss,b_Sc,b_Cs,b_Cc)) / (tau + (1-tau)*(b_Sc+(1-b_Sc)*F('C','s',tau,b_Ss,b_Sc,b_Cs,b_Cc)))
    elif strategy_profile in [('CC','SS'), ('CS','SS'), ('CC','CS'), ('SC','CS'), ('CS','CS')]:
        result = (tau + (1-tau)*(1-b_Cs)*F('S','c',tau,b_Ss,b_Sc,b_Cs,b_Cc)) / (tau + (1-tau)*(b_Cs+(1-b_Cs)*F('S','c',tau,b_Ss,b_Sc,b_Cs,b_Cc)))

    if result < 0 or result > 1:
            print(f"Warning: Payoff out of range [0, 1] for strategy profile {strategy_profile}")
            print(f"Parameters: tau={tau}, b_Ss={b_Ss}, b_Sc={b_Sc}, b_Cs={b_Cs}, b_Cc={b_Cc}")
            print(f"Payoff value: {result}")

    return result

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

def process_params(params):
    tau = params['tau'] 
    b_Ss, b_Sc, b_Cs, b_Cc = params['b_Ss'], params['b_Sc'], params['b_Cs'], params['b_Cc']
    
    # Apply the constraints
    if b_Cs <= b_Ss or b_Cc <= b_Sc:
        return None
    
    equilibria = find_equilibria(tau, b_Ss, b_Sc, b_Cs, b_Cc)
    return [(eq, tau, b_Ss, b_Sc, b_Cs, b_Cc) for eq in equilibria]  # Include tau in the return value


def main():
    tau = 0.001
    step = 0.01
    # Define parameter grid
    param_grid = {
        'tau': [tau],
        'b_Ss': np.arange(0.01, 1.00, step),
        'b_Sc': np.arange(0.01, 1.00, step),
        'b_Cs': np.arange(0.01, 1.00, step),
        'b_Cc': np.arange(0.01, 1.00, step)
    }

    # CHANGE FILE PATH 
    desired_file_path = f'/Users/yanncalvolopez/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Career/RA Ben/Chess/Code/specific_equilibria_tau_{tau}_step_{step}.csv'


    # Generate all parameter combinations
    grid = tqdm(list(ParameterGrid(param_grid)))
    
    # Set up multiprocessing
    num_cores = mp.cpu_count()-4
    print (num_cores)
    pool = mp.Pool(num_cores)
    
    # Process parameter combinations in parallel
    results = pool.map(process_params, grid)
    
    # Close the pool
    pool.close()
    pool.join()
    
    # Process parameter combinations in parallel with batching
    equilibria_data = defaultdict(lambda: {'count': 0, 'params': {'tau': [], 'b_Ss': [], 'b_Sc': [], 'b_Cs': [], 'b_Cc': []}})
    for result in results:
            if result is not None:
                for eq, tau, b_Ss, b_Sc, b_Cs, b_Cc in result:
                    equilibria_data[eq]['count'] += 1
                    equilibria_data[eq]['params']['tau'].append(tau)
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
    target_equilibria = [('CC', 'SS'), ('CS', 'SS'), ('CC', 'CS'), ('SC', 'CS'), ('CS', 'CS')]
    for eq in target_equilibria:
        if equilibria_data[eq]['count'] > 0:
            print(f"\n{eq} is an equilibrium in some parameter ranges.")
        else:
            print(f"\n{eq} never occurs as an equilibrium.")
    
    with open(desired_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Player1_Strategy', 'Player2_Strategy', 'tau', 'b_Ss', 'b_Sc', 'b_Cs', 'b_Cc'])
        
        for eq in target_equilibria:
            data = equilibria_data[eq]
            if data['count'] > 0:
                for i in range(data['count']):
                    writer.writerow([
                        eq[0],  # Player 1's strategy
                        eq[1],  # Player 2's strategy
                        data['params']['tau'][i],
                        data['params']['b_Ss'][i],
                        data['params']['b_Sc'][i],
                        data['params']['b_Cs'][i],
                        data['params']['b_Cc'][i]
                    ])

    print(f"Specific equilibria data has been written to '{desired_file_path}'")

if __name__ == "__main__":
    main()