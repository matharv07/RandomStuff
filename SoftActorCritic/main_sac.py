import gym
import sys

# Monkeypatch for pybullet_envs compatibility with gym >= 0.21
# pybullet_envs expects registry.env_specs, which was removed.
if hasattr(gym.envs.registration, 'registry') and not hasattr(gym.envs.registration.registry, 'env_specs'):
    class RegistryWrapper(dict):
        @property
        def env_specs(self):
            return self
    gym.envs.registration.registry = RegistryWrapper(gym.envs.registration.registry)

import pybullet_envs
import numpy as np
from sac_torch import Agent
from utils import plot_learning_curve
from gym import wrappers

if __name__ == '__main__':
    # Use apply_api_compatibility=True to handle legacy pybullet envs with Gym 0.26+
    env = gym.make('InvertedPendulumBulletEnv-v0', apply_api_compatibility=True)
    agent = Agent(input_dims=env.observation_space.shape, env=env,
            n_actions=env.action_space.shape[0])
    n_games = 250
    # uncomment this line and do a mkdir tmp && mkdir video if you want to
    # record video of the agent playing the game.
    # env = wrappers.Monitor(env, 'tmp/video', video_callable=lambda episode_id: True, force=True)
    filename = 'inverted_pendulum.png'

    figure_file = 'plots/' + filename

    best_score = env.reward_range[0]
    score_history = []
    load_checkpoint = False

    if load_checkpoint:
        agent.load_models()
        env.render(mode='human')

    for i in range(n_games):
        observation = env.reset()
        if isinstance(observation, tuple):
             observation = observation[0]
        done = False
        score = 0
        while not done:
            action = agent.choose_action(observation)
            step_result = env.step(action)
            # Handle both old (4 values) and new (5 values) gym APIs
            if len(step_result) == 5:
                observation_, reward, terminated, truncated, info = step_result
                done = terminated or truncated
            else:
                 observation_, reward, done, info = step_result
            
            score += reward
            agent.remember(observation, action, reward, observation_, done)
            if not load_checkpoint:
                agent.learn()
            observation = observation_
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            if not load_checkpoint:
                agent.save_models()

        print('episode ', i, 'score %.1f' % score, 'avg_score %.1f' % avg_score)

    if not load_checkpoint:
        x = [i+1 for i in range(n_games)]
        plot_learning_curve(x, score_history, figure_file)
