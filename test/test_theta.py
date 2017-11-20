import os, sys
import numpy as np
import unittest

sys.path.insert(0, os.getcwd() + '/src')

from linucb import LinUCB

class TestTheta(unittest.TestCase):

  # Assert that each arm has its own theta
  def test_each_arm_has_theta(self):
    ucb = LinUCB(storage = False)
    n_arms = ucb.store.n_arms()

    # Create arms
    arms = ['a', 'b', 'c']
    ucb.store.create(arms)

    theta_keys = list(ucb.store.theta.keys())

    assert (set(arms) == set(theta_keys)) # 'set' => regardless of list orderings

  # Assert that thetas are well constructed depending of arms and features
  def test_theta_of_each_arm_correspond_to_features(self):
    ucb = LinUCB(storage = False)
    n_arms = ucb.store.n_arms()

    # Create arms
    arms = ['a', 'b', 'c']
    ucb.store.create(arms)

    # Create features
    n_features = 10
    ucb.store.add_features(n_features)

    for a in arms:
      assert (len(ucb.store.theta[a]) == n_features + 1)

if __name__ == '__main__':
  unittest.main()
