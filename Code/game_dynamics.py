def simulate_game_dynamics(profile, steps=10):
    player1_strategy, player2_strategy = profile
    
    def get_action(strategy, opponent_action):
        return strategy[0] if opponent_action == 'C' else strategy[1]
    
    current_state = 'S'  # Starting state
    dynamic = [current_state]
    
    for i in range(steps):
        if i % 2 == 0:  # Player 1's turn
            action = get_action(player1_strategy, current_state)
        else:  # Player 2's turn
            action = get_action(player2_strategy, current_state)
        
        dynamic.append(action)
        current_state = action
    
    return '—>'.join(dynamic)

# Example usage
profiles = [
    ("SS", "CC"),
    ("SC", "CS"),
    ("CS", "SC"),
    ("CC", "SS")
]

for profile in profiles:
    print(f"Profile {profile}:")
    result = simulate_game_dynamics(profile)
    print(result)
    print()