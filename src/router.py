import cgi
import numpy as np
from linucb import ucb
import json

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
          message = self.__post_arms()
        elif (self.path == '/tirages'):
          message = self.__post_tirages()
        elif (self.path == '/reward'):
          message = self.__post_reward()
        elif (self.path == '/features'):
          message = self.__post_features()

      elif (self.command == 'GET'):
        if self.path == '/':
          message = 'Welcome to LinUCB API !'
        elif (self.path == '/thetas'):
          message = self.__get_thetas()
        elif (self.path == '/a'):
          message = self.__get_a()
        elif (self.path == '/b'):
          message = self.__get_b()
        elif (self.path == '/stats'):
          message = self.__get_stats()
        elif (self.path == '/arms'):
          message = self.__get_arms()

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

  def __get_stats(self):
    thetas = self.__get_thetas()
    mean_theta = np.matrix(np.array(list(thetas.values()))).mean(0).tolist()[0]

    stats = {
      'n_arms':     ucb.store.n_arms(),
      'n_features': ucb.store.n_features(),
      'mean_theta': mean_theta
    }

    return stats

  def __get_arms(self):
    return list(ucb.store.theta.keys())

  def __post_arms(self):
    arms = self.postvars.get('arms')

    return ucb.store.create(arms)

  def __post_features(self):
    n_features = int(''.join(self.postvars.get('n')))

    return ucb.store.add_features(n_features)

  def __delete_arms(self, arm):
    return ucb.store.delete([arm])

  def __post_tirages(self):
    X = json.loads(''.join(self.postvars.get('X')))
    n = int(''.join(self.postvars.get('n') or '1'))

    return ucb.pick_arm(X, n)

  def __post_reward(self):
    reward = int(''.join(self.postvars.get('reward')))
    n = str(''.join(self.postvars.get('arm')))
    x = list()

    for i in self.postvars.get('x'):
      x.append(float(i))

    x = np.asarray(x)

    return ucb.reward(x, n, reward)
