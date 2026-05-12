import pickle
import numpy as np

# Load the results file
path = "log/exp/exp_sac_ordinary_seed_0/training_results/results.pkl"
try:
    with open(path, 'rb') as f:
        data = pickle.load(f)

    rewards = data['episode_reward']
    print(f"Total Episodes Completed: {len(rewards)}")
    print(f"Reward at Episode 10: {rewards[10]}")
    print(f"Reward at Episode 50: {rewards[50]}")
    print(f"Reward at Last Episode: {rewards[-1]}")
    
    # Check the average of the last 10 episodes
    recent_avg = np.mean(rewards[-10:])
    print(f"Average Reward (Last 10): {recent_avg}")

    if recent_avg > 1000:
        print("\nSUCCESS: The agent has learned! You are done with Exercise 2.")
    else:
        print("\nWARNING: Reward is still low. You might need to resume training.")

except Exception as e:
    print(f"Error reading file: {e}")
