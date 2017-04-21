# coding: utf-8

import numpy as np
from   numpy.linalg import inv
from   numpy import matmul as mult
import matplotlib.pyplot as plt
from   matplotlib import pyplot

class LinUCB:

  alpha      = 20
  n_arms     = 2
  n_features = 3

  def __init__(self):
    self.A      = [None] * self.n_arms
    self.b      = [None] * self.n_arms
    self.theta  = np.repeat(0.0, self.n_features * self.n_arms).reshape(self.n_arms, self.n_features)
    self.p      = self.n_arms * [0.0]
    self.best_a = None
    self.r      = [0.0]

    for i in range(self.n_arms):
      self.A[i] = np.identity(self.n_features)
      self.b[i] = np.repeat(0.0, self.n_features)

  def algo(self, X):
    for i in range(self.n_arms):
      inv_A = inv(self.A[i])
      self.theta[i, ] = mult(inv_A, self.b[i])
      self.p[i] = mult(self.theta[i, ], X[i]) + self.alpha * np.sqrt(mult(mult(np.transpose(X[i]), inv_A), X[i]))

      self.best_a = np.argmax(self.p)

      # return theta, best_a
      return

x = LinUCB()
print(x.A)
#x.algo('4')

# alpha = 20

# n_arms = 20
# n_features = 3

# Commercial (human) reward
# def reward(x):
#   if x[0] < 0.5:
#     return 0 # simulate 'non pertinent' if too far away
#     return x[0] * 5 + x[1] * 3 + x[2] * 3

# Need to keep A, b and theta
# A      = [None] * n_arms
# b      = [None] * n_arms
# theta  = np.repeat(0.0, n_features * n_arms).reshape(n_arms, n_features)
# p      = n_arms * [0.0]
# best_a = None
# r      = [0.0]

# # initialize at null values
# for i in range(n_arms):
#   A[i] = np.identity(n_features)
#   b[i] = np.repeat(0.0, n_features)

# def algo(X, A, b, theta):
#   for i in range(n_arms):
#     inv_A      = inv(A[i])
#     theta[i, ] = mult(inv_A, b[i])
#     p[i]       = mult(theta[i, ], X[i]) + alpha * np.sqrt(mult(mult(np.transpose(X[i]), inv_A), X[i]))

#     best_a = np.argmax(p)

#     return theta, best_a


# # Create vectors of unknown size (dynamic array), I will use method append type method
# best_a_seq, r_seq, theta_seq = np.array([]), np.array([]), np.array([]).reshape(0, 3)

# # We fix T just know, we dont need before
# # Tu peux voir fabien que dans tout mon script, rien ne dépend de t ou T (sauf le nombre d'itération dans la boucle)
# T = 4000

# for t in range(T): # Simulate each time a piste has to choice an account into the same context
#   x = np.random.random((n_arms, n_features)) # online features, tu remarques que niveau dimension ça passe bien dans
#   # la fonction algo car sur python faire x[i], revient à sélectionner la LIGNE i c'est à dire x[i, :]
#   # print(x)

#   theta, best_a= algo(X= x, A = A, b=b, theta=theta)

#   # Simulate that commercial choose proposed account
#   r = reward(x[best_a])

#   # Update algo variables
#   A[best_a] += np.outer(x[best_a], np.transpose(x[best_a]))
#   b[best_a] += r * x[best_a]

#   #Updating array dynamically
#   best_a_seq = np.append(best_a_seq, best_a)
#   theta_seq = np.append(arr=theta_seq, values = np.mean(theta, axis = 0).reshape(1, n_features), axis = 0)
#   r_seq = np.append(r_seq, r)

# # Répartition des tirages sur les bras, en principe équiprobable car pas de bras meilleur que l'autre
# # et alpha élevé (stratégie d'exploration)
# plt.hist(best_a_seq)

# # On s'assure qu'on retrouve bien les coeff de reward i.e 5 et 3, 3
# plt.plot(theta_seq)

# print(best_a)
