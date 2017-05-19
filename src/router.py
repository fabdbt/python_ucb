import cgi
import numpy as np
from linucb import ucb

class Router(object):
  def __init__(self, command, path, args):
    self.command = command
    self.path = path
    self.args = args

  def process(self):
    message = None

    try:
      if (self.command == 'POST'):
        self.postvars = cgi.parse_qs(self.args, keep_blank_values=1)

        if (self.path == '/arms'):
          self.__create_arms()
        elif (self.path == '/tirages'):
          message = self.__post_tirages()
        elif (self.path == '/reward'):
          message = self.__post_reward()
        elif (self.path == '/features'):
          message = self.__create_features()

      elif (self.command == 'GET'):
        if self.path == '/':
          message =  'Welcome to LinUCB API !'
        elif (self.path == '/thetas'):
          message = self.__get_thetas()
        elif (self.path == '/a'):
          message = self.__get_a()
        elif (self.path == '/b'):
          message = self.__get_b()

      elif (self.command == 'DELETE'):
        resource = '/arms/'

        if self.path.startswith(resource):
          message = self.__delete_arms(self.path[len(resource):])
    except Exception as e:
      print(e)
      return str(e), False

    return message, message != None

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

  def __create_features(self):
    n_features = int(''.join(self.postvars['n']))

    return ucb.store.add_features(n_features)

  def __delete_arms(self, arm):
    return ucb.store.delete([arm])

  def __post_tirages(self):
    # Simulate random features for each arm
    # TODO : get from request
    x = dict()

    for n in ucb.store.theta:
      x[n] = np.random.random(ucb.store.n_features())

    return ucb.pick_arm(x)

  def __post_reward(self):
    reward = int(''.join(self.postvars['reward']))
    n = str(''.join(self.postvars['arm']))
    X = list()

    for i in self.postvars['x']:
      X.append(float(i))

    X = np.asarray(X)

    return ucb.reward(X, n, reward)
