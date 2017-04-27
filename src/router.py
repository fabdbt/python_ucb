import cgi
import numpy as np
from linucb import ucb

class Router(object):
  def __init__(self, command, path, args):
    self.command = command
    self.path = path
    self.args = args

  def process(self):
    if (self.command == 'POST'):
      self.postvars = cgi.parse_qs(self.args, keep_blank_values=1)

      if (self.path == '/arms'):
        return (self.__post_arms())
      elif (self.path == '/tirages'):
        return self.__post_tirages()
      elif (self.path == '/reward'):
        return self.__post_reward()


    elif (self.command == 'GET'):
      if self.path == '/':
        return 'Welcome to LinUCB API !'
      elif (self.path == '/thetas'):
        return self.__get_thetas()

    return False

  # Actions

  def __get_thetas(self):
    return { k: v.tolist() for k, v in ucb.store.theta.items() }

  def __post_arms(self):
    arms = self.postvars['arms']

    return ucb.create_arms(arms)

  def __post_tirages(self):
    # Simulate random features for each arm
    x = dict()

    for n in ucb.store.theta:
      x[n] = np.random.random(ucb.n_features)
    # x = np.random.random(len(ucb.store.arms), ucb.n_features)

    return str(ucb.get_arm(x))

  def __post_reward(self):
    reward = int(''.join(self.postvars['reward']))
    n = str(''.join(self.postvars['arm']))
    x = ''.join(self.postvars['x'])

    return ucb.reward(x, n, reward)
