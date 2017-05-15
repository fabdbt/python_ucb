import numpy as np
from linucb import LinUCB

ucb = LinUCB(storage = False)

# Assert that rewarding only arm 1 and not 0 set the best arm to 1
ucb.store.create(['a', 'b', 'c'])

for i in range(1000):
  # Set random scores
  x = dict()
  for n in ucb.store.theta:
    x[n] = np.random.random(ucb.store.n_features())

  data = ucb.get_arm(x)

  arm_x = data['x']
  arm_n = data['arm']

  if (arm_n == 'a'):
    reward = 100
  else:
    reward = 0

  ucb.reward(np.asarray(arm_x), arm_n, reward)

assert (arm_n == 'a')

# Reset ucb
ucb = LinUCB(storage = False)

# Assert that rewarding only if feature 0 is good augmente theta of feature 0
ucb.store.create(['a', 'b', 'c'])

for i in range(1000):
  # Set random scores
  x = dict()
  for n in ucb.store.theta:
    x[n] = np.random.random(ucb.store.n_features())

  data = ucb.get_arm(x)
  arm_x = data['x']
  arm_n = data['arm']

  if (arm_x[0] > 0.5):
    reward = 100
  else:
    reward = 0

  ucb.reward(np.asarray(arm_x), arm_n, reward)

for k in ucb.store.theta.keys():
  assert (np.argmax(ucb.store.theta[k]) == 0)


# Reset ucb
ucb = LinUCB(storage = False)

# Assert that we can create arms
n_arms = ucb.store.n_arms()

arms = ['a', 'b', 'c']
ucb.store.create(arms)

assert(ucb.store.n_arms() == (n_arms + len(arms)))
assert(len(ucb.store.theta) == (n_arms + len(arms)))
