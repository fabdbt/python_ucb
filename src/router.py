import cgi
from numpy import matrix, median, array, asarray
from linucb import LinUCB
import json

ucb = LinUCB()


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

                m = {
                    '/arms': self.__post_arms,
                    '/tirages': self.__post_tirages,
                    '/reward': self.__post_reward,
                    '/features': self.__post_features
                }

                message = m[self.path]()

            elif (self.command == 'GET'):
                if self.path == '/':
                    message = 'Welcome to LinUCB API !'
                elif (self.path == '/ping'):
                    message = 'pong'
                else:
                    m = {
                        '/thetas': self.__get_thetas,
                        '/a': self.__get_a,
                        '/b': self.__get_b,
                        '/stats': self.__get_stats,
                        '/': self.__get_arms
                    }

                    message = m[self.path]()

            elif (self.command == 'DELETE'):
                resource = '/arms/'

                if self.path.startswith(resource):
                    message = self.__delete_arms(self.path[len(resource):])
        except Exception as e:
            print(e)
            return str(e), False

        return message, message is not None

    # Actions

    def __get_thetas(self):
        return {k: v.tolist() for k, v in ucb.store.theta.items()}

    def __get_a(self):
        return {k: v.tolist() for k, v in ucb.store.A.items()}

    def __get_b(self):
        return {k: v.tolist() for k, v in ucb.store.b.items()}

    def __get_stats(self):
        thetas = self.__get_thetas()
        mean_theta = matrix(array(list(thetas.values()))).mean(0).tolist()[0]
        median_theta = median(array(list(thetas.values())), axis=0).tolist()

        stats = {
            'n_arms': ucb.store.n_arms(),
            'n_features': ucb.store.n_features(),
            'mean_theta': mean_theta,
            'median_theta': median_theta
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

        x = asarray(x)

        return ucb.reward(x, n, reward)
