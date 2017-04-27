# coding: utf-8
# Singleton LinUcb

import numpy as np
from   numpy.linalg import inv
from   numpy import matmul as mult
import storage as store

class LinUCB:
  def __init__(self, alpha = 20, arms = [], n_features = 3, storage = True):
    self.alpha = alpha

    self.store = store.Storage(persistent = storage)

    if storage == True and self.store.has_storage():
      print('Storage found')
      self.store.load()

      if (self.store.n_arms() > 0):
        self.n_features = len(list(self.store.A.values())[0][0])
      else:
        self.n_features = n_features
    else:
      print('Storage not found or disabled')
      self.n_features = n_features

      self.store.create(self.n_features, arms)

    print(self.store.n_arms(), 'arms')
    print(self.n_features, 'features')

  def create_arms(self, arms = []):
    # TODO : Check arm ID does not exists

    for n in arms:
      self.store.A[n] = np.identity(self.n_features)
      self.store.b[n] = np.repeat(0.0, self.n_features)
      self.store.theta[n] = np.repeat(0.0, self.n_features)

    self.store.save()

    return arms

  # x is required into request to prevent 2 people making
  # a simultaneous request and updating same arm. X[i] (arm's features)
  # shouldn't be the same for each tirage, so we need to differentiate them

  def reward(self, x, n, reward):
    X = np.ndarray((self.n_features), buffer=np.array(x))

    self.store.A[n] += np.outer(X, np.transpose(X))
    self.store.b[n] += reward * X

    self.store.save()

  def get_arm(self, x):
    if self.store.n_arms() > 0:
      best_arm = self.process(x)

      return { 'arm': best_arm, 'x': list(x[best_arm]) }
    else:
      return None

  def process(self, X):
    p = dict()

    for n in self.store.A:
      inv_A = inv(self.store.A[n])
      self.store.theta[n] = mult(inv_A, self.store.b[n])
      p[n] = mult(self.store.theta[n], X[n]) + self.alpha * np.sqrt(mult(mult(np.transpose(X[n]), inv_A), X[n]))

    self.store.save()

    return max(p, key=p.get)

ucb = LinUCB()
