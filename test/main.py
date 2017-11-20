# python3 test/main.py
import unittest

if __name__ == '__main__':
  testsuite = unittest.TestLoader().discover('./test')
  unittest.TextTestRunner(verbosity=1).run(testsuite)
