# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 23:39:09 2017

@author: Dhaval-PC
"""

import numpy as np
from enviroment import Env
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

def epsilon_greedy(eps, stateActionValues):
    if np.random.uniform(0, 1) > eps:
        action = np.argmax(stateActionValues)
    else:
        action = np.random.randint(0, 2)        
    return action

def getAction(state, N0, stateActionValues, stateActionValuesCount):
    epsilon = N0 / (N0 + np.sum(stateActionValuesCount[state[0] - 1, state[1] - 1, :]))
    return epsilon_greedy(epsilon, stateActionValues[state[0] - 1, state[1] - 1, :])

def stateActionUpdate(reward, stateActions, actionValues, actionValuesCount):
    for state, action in stateActions:
        current_value = actionValues[state[0] - 1, state[1] - 1, action]
        error = (1.0 / actionValuesCount[state[0] - 1, state[1] - 1, action]) * (reward - current_value)
        actionValues[state[0] - 1, state[1] - 1, action] = current_value + error
        
def monteCarlo(numberOfIterations, N0):
    actionValues = np.zeros([10, 21, 2])
    actionValuesCount = np.ones([10, 21, 2])
    for i in range(numberOfIterations):
        game = Env()
        state = game.getCurrentState()
        total_reward = 0
        stateActionsVisited = []
        while not game.isGameOver():
            action = getAction(state, N0, actionValues, actionValuesCount)
            actionValuesCount[state[0] - 1, state[1] - 1, action] += 1
            stateActionsVisited.append((state, action))
            new_state, reward = game.step(state, action)
            total_reward += reward
            state = new_state
        stateActionUpdate(total_reward, stateActionsVisited, actionValues, actionValuesCount)
    return actionValues, actionValuesCount

def plotValueFunction(actionValues):
    stateValue = np.amax(actionValues, axis=2)
    x = np.arange(1, 11)
    y = np.arange(1, 22)
    xs, ys = np.meshgrid(x, y)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_wireframe(xs, ys, stateValue.T, rstride=1, cstride=1)
    plt.show()