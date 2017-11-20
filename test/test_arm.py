import os, sys
import numpy as np
import unittest

sys.path.insert(0, os.getcwd() + '/src')

from linucb import LinUCB

class TestArms(unittest.TestCase):

  # Assert that rewarding only arm 1 and not 0 set the best arm to 1
  def test_it_gives_best_rewarded_arm(self):
    ucb = LinUCB(storage = False)
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

  # Assert that we can create arms
  def test_it_can_create_arms(ucb):
    ucb = LinUCB(storage = False)
    arms = ['a', 'b', 'c']
    ucb.store.create(arms)

    assert(ucb.store.n_arms() == len(arms))

  # Assert that we can delete arms
  def test_it_can_delete_arm(ucb):
    ucb = LinUCB(storage = False)
    arms = ['a', 'b', 'c']
    ucb.store.create(arms)

    ucb.store.delete(arms[0])

    assert(ucb.store.n_arms() == len(arms) - 1)

if __name__ == '__main__':
  unittest.main()
