import os
import sys

sys.path.insert(0, os.getcwd() + '/src')

from linucb import LinUCB
import arm, feature, theta

# Arms tests
ucb = LinUCB(storage = False)
arm.assert_it_gives_best_rewarded_arm(ucb)

ucb = LinUCB(storage = False)
arm.assert_it_can_create_arms(ucb)

# Features tests
ucb = LinUCB(storage = False)
feature.assert_it_increases_theta_of_best_rewarded_feature(ucb)

ucb = LinUCB(storage = False)
feature.assert_it_can_create_features(ucb)

# Thetas tests
ucb = LinUCB(storage = False)
theta.assert_theta_of_each_arm_correspond_to_features(ucb)

ucb = LinUCB(storage = False)
theta.assert_each_arm_has_theta(ucb)
