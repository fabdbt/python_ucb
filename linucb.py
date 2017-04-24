# coding: utf-8
# Singleton LinUcb

import numpy as np
from   numpy.linalg import inv
from   numpy import matmul as mult

class LinUCB:
  def __init__(self, alpha = 20, n_arms = 20, n_features = 3):
    self.alpha = alpha
    self.n_arms = n_arms
    self.n_features = n_features

    self.A = [None] * self.n_arms
    self.b = [None] * self.n_arms
    self.theta = np.repeat(0.0, self.n_features * self.n_arms).reshape(self.n_arms, self.n_features)

    for i in range(self.n_arms):
      self.A[i] = np.identity(self.n_features)
      self.b[i] = np.repeat(0.0, self.n_features)

  def create_arms(self, n_arms):
    for i in range(n_arms):
      self.A.append(np.identity(self.n_features))
      self.b.append(np.repeat(0.0, self.n_features))

    self.theta = np.concatenate((self.theta, np.repeat(0.0, self.n_features * n_arms).reshape(n_arms, self.n_features)), axis=0)

    self.n_arms += n_arms
    return self.n_arms

  # x is required into request to prevent 2 people making
  # a simultaneous request and updating same arm. X[i] (arm's features)
  # shouldn't be the same for each tirage, so we need to differentiate them

  def reward(self, x, i, reward):
    X = np.ndarray((self.n_features), buffer=np.array(x))

    self.A[i] += np.outer(X, np.transpose(X))
    self.b[i] += reward * X

  def get_arm(self, x):
    best_a = self.process(x)

    return { 'arm': best_a, 'x': list(x[best_a]) }

  def process(self, X):
    p = [0.0] * self.n_arms

    for i in range(self.n_arms):
      inv_A = inv(self.A[i])
      self.theta[i, ] = mult(inv_A, self.b[i])
      p[i] = mult(self.theta[i, ], X[i]) + self.alpha * np.sqrt(mult(mult(np.transpose(X[i]), inv_A), X[i]))

    return np.argmax(p)

ucb = LinUCB()
