import cgi
import numpy as np
from linucb import ucb

class Router(object):
  def __init__(self, command, path, args):
    self.command = command
    self.path = path
    self.args = args

  def process(self):
    try:
      if (self.command == 'POST'):
        self.postvars = cgi.parse_qs(self.args, keep_blank_values=1)

        if (self.path == '/arms'):
          return (self.__create_arms())
        elif (self.path == '/tirages'):
          return self.__post_tirages()
        elif (self.path == '/reward'):
          return self.__post_reward()

      elif (self.command == 'GET'):
        if self.path == '/':
          return 'Welcome to LinUCB API !'
        elif (self.path == '/thetas'):
          return self.__get_thetas()
        elif (self.path == '/a'):
          return self.__get_a()
        elif (self.path == '/b'):
          return self.__get_b()

      elif (self.command == 'DELETE'):
        resource = '/arms/'

        if self.path.startswith(resource):
          return self.__delete_arms(self.path[len(resource):])
    except Exception as e:
      return 'An error occured'
    else:
      return False

  # Actions

  def __get_thetas(self):
    return { k: v.tolist() for k, v in ucb.store.theta.items() }

  def __get_a(self):
    return { k: v.tolist() for k, v in ucb.store.A.items() }

  def __get_b(self):
    return { k: v.tolist() for k, v in ucb.store.b.items() }

  def __create_arms(self):
    arms = self.postvars['arms']

    return ucb.store.create(arms)

  def __delete_arms(self, arm):
    return ucb.store.delete(arm)

  def __post_tirages(self):
    # Simulate random features for each arm
    # TODO : get from request
    x = dict()

    for n in ucb.store.theta:
      x[n] = np.random.random(ucb.store.n_features())

    return ucb.get_arm(x)

  def __post_reward(self):
    reward = int(''.join(self.postvars['reward']))
    n = str(''.join(self.postvars['arm']))
    x = ''.join(self.postvars['x'])

    return ucb.reward(x, n, reward)
