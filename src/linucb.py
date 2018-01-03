# coding: utf-8

import numpy as np
from   numpy.linalg import inv
from   numpy import matmul as mult
import storage as store

class LinUCB:
  def __init__(self, alpha = 20, storage = True):
    self.alpha = alpha

    self.store = store.Storage(persistent = storage)

    # print(self.store.n_arms(), 'arms')
    # print(self.store.n_features(), 'features')

  # x are features of arm n
  def reward(self, x, n, reward):
    self.store.A[n] += np.outer(x, np.transpose(x))
    self.store.b[n] += reward * x

    inv_A = inv(self.store.A[n])
    self.store.theta[n] = mult(inv_A, self.store.b[n])

    self.store.save()

    return True

  # X is a hash of features of all arms
  def pick_arm(self, X, i = 1):
    if i > self.store.n_arms():
      i = self.store.n_arms()

    p = dict()

    for n in self.store.A:
      if type(X.get(n)) != list:
        raise Exception('Features for arm ' + n + ' are required')

      inv_A = inv(self.store.A[n])

      p[n] = mult(self.store.theta[n], X[n]) + self.alpha * np.sqrt(mult(mult(np.transpose(X[n]), inv_A), X[n]))

    best_arms = sorted(p, key=p.get, reverse=True)[:i]

    return best_arms
