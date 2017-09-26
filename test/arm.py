import numpy as np

def assert_it_gives_best_rewarded_arm(ucb):
  # Assert that rewarding only arm 1 and not 0 set the best arm to 1
  ucb.store.create(['a', 'b', 'c'])

  for i in range(1000):
    x = dict()

    # Set random scores
    for n in ucb.store.theta:
      x[n] = np.random.random(ucb.store.n_features()).tolist()

    data = ucb.pick_arm(x)

    arm_n = data['arms'][0]

    if (arm_n == 'a'):
      reward = 100
    else:
      reward = 0

    ucb.reward(np.asarray(x[arm_n]), arm_n, reward)

  assert (arm_n == 'a')

def assert_it_can_create_arms(ucb):
  # Assert that we can create arms
  n_arms = ucb.store.n_arms()

  arms = ['a', 'b', 'c']
  ucb.store.create(arms)

  assert(ucb.store.n_arms() == (n_arms + len(arms)))
  assert(len(ucb.store.theta) == (n_arms + len(arms)))
