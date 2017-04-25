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
    return ucb.store.theta.tolist()

  def __post_arms(self):
    n_arms = int(''.join(self.postvars['n_arms']))

    return ucb.create_arms(n_arms)

  def __post_tirages(self):
    # Simulate random features for each arm
    x = np.random.random((ucb.n_arms, ucb.n_features))

    return str(ucb.get_arm(x))

  def __post_reward(self):
    reward = int(''.join(self.postvars['reward']))
    i = int(''.join(self.postvars['arm']))
    x = ''.join(self.postvars['x'])

    return ucb.reward(x, i, reward)
