import numpy as np
import os

REQUIRED_STORAGE_FILES = ['thetas.npy', 'A.npy', 'b.npy']

class Storage:

  def __init__(self, path = './storage/'):
    self.folder = path
    self.__check_corrupted_storage()

  def has_storage(self):
    return (self.__storage_files() != [])

  def load(self):
    ucb = { os.path.splitext(k)[0]: v for k, v in self.__get_files().items() }

    if ucb:
      self.theta = ucb['theta']
      self.A = ucb['A']
      self.b = ucb['b']

      return True
    else:
      return False

  def create(self, n_arms, n_features):
    self.A = [None] * n_arms
    self.b = [None] * n_arms

    for i in range(n_arms):
      self.A[i] = np.identity(n_features)
      self.b[i] = np.repeat(0.0, n_features)

    self.theta = np.repeat(0.0, n_features * n_arms).reshape(n_arms, n_features)

    self.save()

  def save(self):
    self.__save('A', self.A)
    self.__save('b', self.b)
    self.__save('theta', self.theta)

  # Private

  def __check_corrupted_storage(self):
    if self.has_storage():
      files = list(self.__get_files().keys())

      if (files.sort() != REQUIRED_STORAGE_FILES.sort()):
        raise Exception('Corrupted storage. Please fix it or remove files into folder ' + self.folder)

      return True

  def __get_files(self):
    if self.has_storage():
      files = {}

      for filename in self.__storage_files():
        files[filename] = self.__get(filename)

      return files
    else:
      return False

  def __storage_files(self):
    return os.listdir(self.folder)

  def __get(self, filename):
    return np.load(self.folder + filename)

  def __save(self, filename, content):
    return np.save(self.folder + filename, content)
