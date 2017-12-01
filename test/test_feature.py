import os, sys
import numpy as np
import unittest
import random
import string

sys.path.insert(0, os.getcwd() + '/src')

from linucb import LinUCB

class TestFeatures(unittest.TestCase):

  # Assert that rewarding only if feature 0 is good increase theta of feature 0
  def test_it_increases_theta_of_best_rewarded_feature(self):
    ucb = LinUCB(storage = False)

    # Create arms
    ucb.store.create(['a', 'b', 'c'])

    # Create features
    n_features = 10
    ucb.store.add_features(n_features)

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
  def test_it_can_create_features(self):
    ucb = LinUCB(storage = False)

    # Create arms
    ucb.store.create(['a', 'b', 'c'])

    new_features = 10
    n_features = ucb.store.n_features()
    ucb.store.add_features(new_features)

    assert(ucb.store.n_features() == (n_features + new_features))

  # Assert that rewarding randomly an arm increases it constant feature
  def test_it_increses_constant_feature(self):
    ucb = LinUCB(storage = False)

    # Create arms
    ucb.store.create(['a']) # It will also create one feature, constant

    # Create features
    n_features = 100
    ucb.store.add_features(n_features)

    for i in range(1000):
      # Set random scores
      # Send 1 for feature constant and random features for others
      x = [1] + np.random.random(ucb.store.n_features() - 1).tolist()

      # set random reward
      reward = random.randint(0, 100)

      ucb.reward(np.asarray(x), 'a', reward)

    assert (np.argmax(ucb.store.theta['a']) == 0)

if __name__ == '__main__':
  unittest.main()
