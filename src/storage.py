import numpy as np
import os

REQUIRED_STORAGE_FILES = ['theta.npy', 'A.npy', 'b.npy']
CORRUPTED_MESSAGE = 'Corrupted storage. Please fix it or remove files into folder '
DEFAULT_N_FEATURES = 1

class Storage:

  def __init__(self, persistent = True, path = './storage/'):
    self.folder = path
    self.persistent = persistent

    self.A = dict()
    self.b = dict()
    self.theta = dict()

    if self.persistent == True:
      # Only used at initialization
      self.files = self.__get_storage_files()

      if self.has_storage():
        self.__check_storage_files()
        self.load()
        print('Storage loaded')

  def has_storage(self):
    return bool(self.files)

  def load(self):
    data = { os.path.splitext(k)[0]: v for k, v in self.files.items() }

    if data:
      self.theta = data['theta']
      self.A = data['A']
      self.b = data['b']

      return True
    else:
      return False

  def create(self, arms = []):
    for n in arms:
      if n in self.theta:
        raise ValueError('Arm(s) already exists')

    if self.n_arms() > 0:
      n_features = self.n_features()
    else:
      n_features = DEFAULT_N_FEATURES # First arm features

    for n in arms:
      self.A[n] = np.identity(n_features)
      self.b[n] = np.repeat(0.0, n_features)
      self.theta[n] = np.repeat(0.0, n_features)

    self.save()

    return arms

  def delete(self, arms = []):
    for n in arms:
      if ((n not in self.theta) or (n not in self.A) or (n not in self.b)):
        raise ValueError(n + ' is not a registered arm')

    for n in arms:
      self.theta.pop(n)
      self.A.pop(n)
      self.b.pop(n)

    return self.save()

  def add_features(self, total = 1):
    for t in range(total):
      for n in self.A:
        self.A[n] = self.__extend_identity_map(self.A[n])
        self.b[n] = np.append(self.b[n], [0.0])
        self.theta[n] = np.append(self.theta[n], [0.0])

    return self.save()

  def save(self):
    if self.persistent == True:
      self.__save('A', self.A)
      self.__save('b', self.b)
      self.__save('theta', self.theta)

    return True

  def n_arms(self):
    return len(self.theta)

  def n_features(self):
    if self.n_arms() > 0 and len(list(self.A.values())[0]) > 0:
      return len(list(self.A.values())[0][0])
    else:
      return 0

  # Private

  def __extend_identity_map(self, identity):
    copy = identity

    copy = np.append(copy, [[0] * len(copy)], axis=0)
    copy = np.append(copy, [[0]] * len(copy), axis=1)
    copy[len(copy) - 1][len(copy) - 1] = 1

    return copy

  def __check_storage_files(self):
    # Check all files are presents
    if (len(self.files) < len(REQUIRED_STORAGE_FILES)):
      raise Exception(CORRUPTED_MESSAGE + self.folder)
    else:
      # Check size of file contents are equals
      sizes = []
      for v in self.files.values():
        sizes.append(len(v))

        if not (all(sizes[0] == size for size in sizes)):
          raise Exception(CORRUPTED_MESSAGE + self.folder)

  def __get_storage_files(self):
    files = {}
    # Prevent from listing directory on each call if files are found
    for filename in np.intersect1d(REQUIRED_STORAGE_FILES, os.listdir(self.folder)):
      files[filename] = self.__get(filename)

    return files

  def __get(self, filename):
    # np.save method save dict as array
    # http://stackoverflow.com/a/8361740/4792408

    return np.load(self.folder + filename).item()

  def __save(self, filename, content):
    return np.save(self.folder + filename, content)
