import numpy as np
import os

REQUIRED_STORAGE_FILES = ['theta.npy', 'A.npy', 'b.npy']

class Storage:

  def __init__(self, persistent = True, path = './storage/'):
    self.folder = path
    self.persistent = persistent

    if self.persistent == True:
      self.files = self.__get_storage_files() # Only used at initialization

      if self.has_storage():
        self.__check_storage_files()

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

  def create(self, n_features, arms = []):
    self.A = dict()
    self.b = dict()
    self.theta = dict()

    for n in arms:
      self.A[n] = np.identity(n_features)
      self.b[n] = np.repeat(0.0, n_features)
      self.theta[n] = np.repeat(0.0, n_features)

    self.save()

  def save(self):
    if self.persistent == True:
      self.__save('A', self.A)
      self.__save('b', self.b)
      self.__save('theta', self.theta)

  def n_arms(self):
    return len(self.theta)

  # Private

  def __check_storage_files(self):
    # Check all files are presents
    if (len(self.files) < len(REQUIRED_STORAGE_FILES)):
      raise Exception('Corrupted storage. Please fix it or remove files into folder ' + self.folder)
    else:
      # Check size of file contents are equals
      sizes = []
      for v in self.files.values():
        sizes.append(len(v))

        if not (all(sizes[0] == size for size in sizes)):
          raise Exception('Corrupted storage. Please fix it or remove files into folder ' + self.folder)

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
