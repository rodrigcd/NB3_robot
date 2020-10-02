#Code from https://towardsdatascience.com/reinforcement-learning-temporal-difference-sarsa-q-learning-expected-sarsa-on-python-9fecfda7467e
# and https://medium.com/zero-equals-false/n-step-td-method-157d3875b9cb

import numpy as np
import pickle
import pandas as pd

class NStepSarsa(object):

    def __init__(self, n_states, n_actions, n_steps=20, step_time=0.5, start_epsilon=0.9, stop_epsilon=0.1,
                 epsilon_step=0.005, discount_factor=0.99, learning_rate=0.1):
        self.n_states = n_states
        self.n_actions = n_actions
        self.n_steps = n_steps
        self.step_time = step_time
        self.start_epsilon = start_epsilon
        self.stop_epsilon = stop_epsilon
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.epsilon = start_epsilon
        self.epsilon_step = epsilon_step
        self._init_Q_values()

    def _init_Q_values(self):
        self.Q_values = np.zeros(shape=(self.n_states, self.n_actions))
        self.actions = np.arange(0, self.n_actions)
        self.states = np.arange(0, self.n_states)
        self.current_operations = {"States": [], "Rewards": [], "Actions": []}
        self.global_step = 0

    def choose_action(self, state, training=True):
        if not training or np.random.rand() > self.epsilon:
            action = np.argmax(self.Q_values[state, :])
        else:
            action = np.random.choice(self.actions[1:])
        return action

    def take_action(self, action, state, reward=0):
        new_state = action
        return new_state, reward

    def _update_epsilon(self):
        self.epsilon -= self.epsilon_step
        if self.epsilon < self.stop_epsilon:
            self.epsilon = self.stop_epsilon
        print(self.epsilon)

    def save_Q_values(self):
        pickle.dump([self.Q_values, self.epsilon], open("Q_values.pkl", "wb"), protocol=2)

    def load_Q_values(self):
        self.Q_values, self.epsilon = pd.read_pickle("Q_values.pkl")

    def run_epoch(self):
        current_state = 0
        current_action = self.choose_action(current_state)
        self.current_operations = {"States": [current_state], "Rewards": [], "Actions": [current_action]}
        for i in range(self.n_steps):
            self.global_step = i
            new_state, new_reward = self.take_action(action=current_action, state=current_state, reward=0)
            self.current_operations["Rewards"].append(new_reward)
            self.current_operations["States"].append(new_state)
            new_action = self.choose_action(new_state)
            self.current_operations["Actions"].append(new_action)
            current_state = new_state
            current_action = new_action
        return self.current_operations

    def receive_feedback(self, reward):
        self.current_operations["Rewards"][self.global_step] = reward

    def update_Q_values(self):
        G = 0
        for i in range(self.n_steps-1):
            state_i, action_i = self.current_operations["States"][i], self.current_operations["Actions"][i]
            state_i_1, action_i_1 = self.current_operations["States"][i+1], self.current_operations["Actions"][i+1]
            G = self.current_operations["Rewards"][i+1] + self.Q_values[state_i_1, action_i_1]*self.discount_factor
            self.Q_values[state_i, action_i] = self.Q_values[state_i, action_i] + self.learning_rate*(G-self.Q_values[state_i, action_i])
        print("G", G)

    def get_Q_values(self):
        return self.Q_values

    def print_current_best_actions(self, action_label):
        Q = self.get_Q_values()
        print(np.round(Q, 2))
        for i, action in enumerate(self.actions):
            print("State:", action_label[i], "Best action:", action_label[np.argmax(Q[i, :])])


if __name__ == "__main__":
    learning_function = NStepSarsa(n_states=9, n_actions=9, n_steps=10, epsilon_step=0.01, learning_rate=0.1)
    n_epochs = 500

    robot_actions = []  # 0: rest, 1: forward, 2: backward
    action_str = "ofb"
    for left_motor in range(3):
        for right_motor in range(3):
            robot_actions.append((action_str[left_motor] + action_str[right_motor]))

    print(robot_actions)
    good_actions = ["ob", "fo", "fb"]
    bad_actions = ["bo", "of", "bf"]

    for i in range(n_epochs):
        operations = learning_function.run_epoch()
        epoch_actions = operations["Actions"]
        reward = 0
        for a in epoch_actions:
            if robot_actions[a] in good_actions:
                reward += 1
            elif robot_actions[a] in bad_actions:
                reward -= 1
        learning_function.receive_feedback(reward)
        learning_function.update_Q_values()
        learning_function.print_current_best_actions(robot_actions)
        learning_function.save_Q_values()