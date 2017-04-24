import numpy as np
import linucb

ucb = linucb.LinUCB()

# Assert that rewarding only arm 1 and not 0 set the best arm to 1
for i in range(1000):
  # Set random scores
  x = np.random.random((ucb.n_arms, ucb.n_features))

  data = ucb.get_arm(x)
  arm_x = data['x']
  arm_n = int(data['arm'])

  if (arm_n == 1):
    reward = 100
  else:
    reward = 0

  ucb.reward(arm_x, arm_n, reward)

assert (arm_n == 1)


# Reset ucb
ucb = linucb.LinUCB()

# Assert that rewarding only if feature 0 is good augmente theta of feature 0
for i in range(1000):
  # Set random scores
  x = np.random.random((ucb.n_arms, ucb.n_features))

  data = ucb.get_arm(x)
  arm_x = data['x']
  arm_n = int(data['arm'])

  if (arm_x[0] > 0.5):
    reward = 100
  else:
    reward = 0

  ucb.reward(arm_x, arm_n, reward)

for i in range(ucb.n_arms):
  assert (np.argmax(ucb.theta[i]) == 0)


# Reset ucb
ucb = linucb.LinUCB()

# Assert that we can create arms
n_arms = ucb.n_arms
ucb.create_arms(10)

assert(ucb.n_arms == (n_arms + 10))
assert(len(ucb.theta) == (n_arms + 10))
