# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 22:17:06 2017

@author: Dhaval-PC
"""
import numpy as np

class Env:
    def __init__(self):
        self.new_game()

    def new_game(self):
        self.player = np.random.randint(1, 11)
        self.dealer_first_card = self.dealer = np.random.randint(1, 11)
        self.game_over=False
        
    def getCard(self):
        card = np.random.randint(1, 11)
        color_card = np.random.randint(3)
        if color_card <= 1:
            return card
        else:
            return -card
    
    def isBurst(self, score):
        return score < 1 or score > 21
    
    def isGameOver(self):
        return self.game_over
    
    def getCurrentState(self):
        return [self.dealer_first_card, self.player]
        
    def step(self, state, action):
        if self.game_over:
            self.new_game()
        if action == 1:
            self.player += self.getCard()
            if self.isBurst(self.player):
                self.game_over = True
                reward = -1
                self.player = 0
            else:
                reward = 0
                self.game_over = False
        else:
            while self.dealer < 17:
                self.dealer += self.getCard()
                if self.isBurst(self.dealer):
                    self.dealer = 0
                    self.game_over = True
                    reward = 1
                    return ((self.dealer_first_card, self.player), reward)
                else:
                    continue
            if self.dealer > self.player:
                reward = -1
            elif self.player == self.dealer:
                reward = 0
            else:
                reward = 1
            self.game_over = True
        return ((self.dealer_first_card, self.player), reward)