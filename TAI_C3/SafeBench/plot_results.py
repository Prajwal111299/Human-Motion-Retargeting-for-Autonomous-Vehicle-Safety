import matplotlib
matplotlib.use('Agg') # Use non-interactive backend (no window needed)
import matplotlib.pyplot as plt
import pickle

# Load the training data
path = "log/exp/exp_sac_ordinary_seed_0/training_results/results.pkl"
try:
    with open(path, 'rb') as f:
        data = pickle.load(f)

    rewards = data['episode_reward']
    episodes = range(len(rewards))

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(episodes, rewards, label='Episode Reward')
    plt.title('SAC Agent Training Progress')
    plt.xlabel('Episode')
    plt.ylabel('Episode Reward')
    plt.grid(True)
    plt.legend()
    
    # Save the plot
    plt.savefig('training_plot.png')
    print("Success! Plot saved as 'training_plot.png'")

except Exception as e:
    print(f"Error: {e}")
