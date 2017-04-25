import numpy as np
import os

REQUIRED_STORAGE_FILES = ['theta.npy', 'A.npy', 'b.npy']

class Storage:

  def __init__(self, path = './storage/'):
    self.folder = path
    self.files = {}

    self.__check_storage_files()

  def has_storage(self):
    return bool(self.__storage_files())

  def load(self):
    data = { os.path.splitext(k)[0]: v for k, v in self.__storage_files().items() }

    if data:
      self.theta = data['theta']
      self.A = data['A']
      self.b = data['b']

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

  def __check_storage_files(self):
    if (self.has_storage() and (len(self.__storage_files()) < len(REQUIRED_STORAGE_FILES))):
      raise Exception('Corrupted storage. Please fix it or remove files into folder ' + self.folder)

  def __storage_files(self):
    # Prevent from listing directory on each call if files are found
    if self.files:
      return self.files

    for filename in np.intersect1d(REQUIRED_STORAGE_FILES, os.listdir(self.folder)):
      self.files[filename] = self.__get(filename)

    return self.files

  def __get(self, filename):
    return np.load(self.folder + filename)

  def __save(self, filename, content):
    return np.save(self.folder + filename, content)
