from itertools import count

import matplotlib.pyplot as plt
import torch

from src.game_window import GameWindow
from src.ml.DQN import device
from src.ml.InputExtraction import screen, clock
from src.ml.Training import memory, policy_net, target_net, get_screen, select_action, \
    episode_durations, plot_durations, scores, TARGET_UPDATE, plot_score
from src.ml.TrainingLoop import optimize_model

game = GameWindow(screen)

# while not done:
done = game.process_events()
game.run_logic()
game.display_frame()
clock.tick(1)

plt.figure()
plt.imshow(get_screen().cpu().squeeze(0).permute(1, 2, 0).numpy(),
           interpolation='none')
plt.title('Example extracted screen')
plt.show()

num_episodes = 100
for i_episode in range(num_episodes):
    # Initialize the environment and state
    game.reset()
    last_screen = get_screen()
    current_screen = get_screen()
    state = current_screen - last_screen
    for t in count():
        # Select and perform an action
        previous_score = game.game.score
        action = select_action(state)
        game.step(action.item())
        game.process_events()
        done = game.game.game_over
        game.run_logic()
        game.display_frame()
        reward = game.game.score - previous_score
        reward = torch.tensor([reward], device=device)

        # Observe new state
        last_screen = current_screen
        current_screen = get_screen()
        if not done:
            next_state = current_screen - last_screen
        else:
            next_state = None

        # Store the transition in memory
        memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        optimize_model()
        if done:
            episode_durations.append(t + 1)
            plot_durations()
            scores.append(game.game.score)
            break
    # Update the target network, copying all weights and biases in DQN
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())

print('Complete')
plt.ioff()
plt.clf()
plot_score()
