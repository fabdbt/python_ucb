import numpy as np

# Assert that rewarding only if feature 0 is good increase theta of feature 0
def assert_it_increases_theta_of_best_rewarded_feature(ucb):
  ucb.store.create(['a', 'b', 'c'])

  for i in range(1000):
    x = dict()

    # Set random scores
    for n in ucb.store.theta:
      x[n] = np.random.random(ucb.store.n_features()).tolist()

    data = ucb.pick_arm(x)
    arm_n = data['arms'][0]

    if (x[arm_n][0] > 0.5):
      reward = 100
    else:
      reward = 0

    ucb.reward(np.asarray(x[arm_n]), arm_n, reward)

  for k in ucb.store.theta.keys():
    assert (np.argmax(ucb.store.theta[k]) == 0)

# Assert that we can create features
def assert_it_can_create_features(ucb):
  ucb.store.create(['a', 'b', 'c'])

  new_features = 10
  n_features = ucb.store.n_features()
  ucb.store.add_features(new_features)

  assert(ucb.store.n_features() == (n_features + new_features))
