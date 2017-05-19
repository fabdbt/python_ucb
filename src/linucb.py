# coding: utf-8
# Singleton LinUcb

import numpy as np
from   numpy.linalg import inv
from   numpy import matmul as mult
import storage as store

class LinUCB:
  def __init__(self, alpha = 20, storage = True):
    self.alpha = alpha

    self.store = store.Storage(persistent = storage)

    print(self.store.n_arms(), 'arms')
    print(self.store.n_features(), 'features')

  # x is required into request to prevent 2 people making
  # a simultaneous request and updating same arm. X[i] (arm's features)
  # shouldn't be the same for each tirage, so we need to differentiate them

  def reward(self, x, n, reward):
    self.store.A[n] += np.outer(x, np.transpose(x))
    self.store.b[n] += reward * x

    inv_A = inv(self.store.A[n])
    self.store.theta[n] = mult(inv_A, self.store.b[n])

    self.store.save()

    return True

  def pick_arm(self, X):
    if self.store.n_arms() > 0:
      p = dict()

      for n in self.store.A:
        inv_A = inv(self.store.A[n])

        p[n] = mult(self.store.theta[n], X[n]) + self.alpha * np.sqrt(mult(mult(np.transpose(X[n]), inv_A), X[n]))

      best_arm = max(p, key=p.get)

      return { 'arm': best_arm, 'x': list(X[best_arm]) }
    else:
      return None

ucb = LinUCB()
