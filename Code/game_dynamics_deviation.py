def simulate_game_dynamics(profile, steps=20, deviation=None):
    player1_strategy, player2_strategy = profile
    
    def get_action(strategy, opponent_action):
        return strategy[0] if opponent_action == 'S' else strategy[1]
    
    current_state = 'S'  # Starting state
    dynamic = [current_state]
    deviation_step = None
    
    for i in range(steps):
        if i % 2 == 0:  # Player 1's turn
            original_action = get_action(player1_strategy, current_state)
            if deviation and deviation[0] == 1 and deviation_step is None:
                deviation_action = get_action(deviation[1], current_state)
                if deviation_action != original_action:
                    action = deviation_action
                    deviation_step = i
                else:
                    action = original_action
            else:
                action = original_action
        else:  # Player 2's turn
            original_action = get_action(player2_strategy, current_state)
            if deviation and deviation[0] == 2 and deviation_step is None:
                deviation_action = get_action(deviation[1], current_state)
                if deviation_action != original_action:
                    action = deviation_action
                    deviation_step = i
                else:
                    action = original_action
            else:
                action = original_action
        
        dynamic.append(action)
        current_state = action
    
    return '—>'.join(dynamic), deviation_step


def get_possible_deviations(strategy):
    all_strategies = ['SS', 'SC', 'CS', 'CC']
    return [s for s in all_strategies if s != strategy]

def run_simulations(profile):
    print(f"\nStrategy Profile: {profile}")
    print("No Deviation:")
    result, _ = simulate_game_dynamics(profile)
    print(result)
    print("Deviation step: N/A")
    print()

    player1_strategy, player2_strategy = profile
    
    # Player 1 deviations
    for deviation in get_possible_deviations(player1_strategy):
        print(f"Player 1 Deviation to {deviation}:")
        result, step = simulate_game_dynamics(profile, deviation=(1, deviation))
        print(result)
        print(f"Deviation step: {step}")
        print()
    
    # Player 2 deviations
    for deviation in get_possible_deviations(player2_strategy):
        print(f"Player 2 Deviation to {deviation}:")
        result, step = simulate_game_dynamics(profile, deviation=(2, deviation))
        print(result)
        print(f"Deviation step: {step}")
        print()

# Run simulations for specified strategy profiles
strategy_profiles = [('CC', 'SS'), ('CS', 'SS'), ('CC', 'CS'), ('CS', 'CS')]

for profile in strategy_profiles:
    run_simulations(profile)