def assert_each_arm_has_theta(ucb):
  n_arms = ucb.store.n_arms()

  # Create arms
  arms = ['a', 'b', 'c']
  ucb.store.create(arms)

  theta_keys = list(ucb.store.theta.keys())

  assert (set(arms) == set(theta_keys)) # 'set' => regardless of list orderings

# Assert that thetas are well constructed depending of arms and features
def assert_theta_of_each_arm_correspond_to_features(ucb):
  n_arms = ucb.store.n_arms()

  # Create arms
  arms = ['a', 'b', 'c']
  ucb.store.create(arms)

  # Create features
  n_features = 10
  ucb.store.add_features(n_features)

  for a in arms:
    assert (len(ucb.store.theta[a]) == n_features + 1)
