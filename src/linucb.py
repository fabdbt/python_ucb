# coding: utf-8
# Singleton LinUcb

import numpy as np
from   numpy.linalg import inv
from   numpy import matmul as mult
import storage as store

class LinUCB:
  def __init__(self, alpha = 20, n_arms = 20, n_features = 3, storage = True):
    self.alpha = alpha

    self.store = store.Storage(persistent = storage)

    if storage == True and self.store.has_storage():
      print('Storage found')
      self.store.load()

      self.n_arms = len(self.store.A)
      self.n_features = list(self.store.A.shape)[1]
    else:
      print('Storage not found or disabled')
      self.n_arms = n_arms
      self.n_features = n_features

      self.store.create(self.n_arms, self.n_features)

  def create_arms(self, n_arms):
    self.store.A = np.concatenate((self.store.A, [np.identity(self.n_features)] * n_arms), axis = 0)
    self.store.b = np.concatenate((self.store.b, [np.repeat(0.0, self.n_features)] * n_arms), axis = 0)
    self.store.theta = np.concatenate((self.store.theta, np.repeat(0.0, self.n_features * n_arms).reshape(n_arms, self.n_features)), axis=0)

    self.store.save()

    self.n_arms += n_arms
    return self.n_arms

  # x is required into request to prevent 2 people making
  # a simultaneous request and updating same arm. X[i] (arm's features)
  # shouldn't be the same for each tirage, so we need to differentiate them

  def reward(self, x, i, reward):
    X = np.ndarray((self.n_features), buffer=np.array(x))

    self.store.A[i] += np.outer(X, np.transpose(X))
    self.store.b[i] += reward * X

    self.store.save()

  def get_arm(self, x):
    best_a = self.process(x)

    return { 'arm': best_a, 'x': list(x[best_a]) }

  def process(self, X):
    p = [0.0] * self.n_arms

    for i in range(self.n_arms):
      inv_A = inv(self.store.A[i])
      self.store.theta[i, ] = mult(inv_A, self.store.b[i])
      p[i] = mult(self.store.theta[i, ], X[i]) + self.alpha * np.sqrt(mult(mult(np.transpose(X[i]), inv_A), X[i]))

    self.store.save()

    return np.argmax(p)

ucb = LinUCB()
