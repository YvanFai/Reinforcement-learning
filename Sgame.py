import random
from random import randint
import numpy as np

class Stickgame(object):

    #Number of sticks
    def __init__(self , n):
        super(Stickgame , self).__init__()
        self.original_n = n
        self.n = n

    #Game over
    def over(self):
        if self.n <= 0:
            return True
        return False
    
    #Reset
    def reset(self):
        self.n = self.original_n
        return self.n
    
    #State
    def display(self):
        print("| " , self.n)

    #step
    def step(self , action):
        self.n -= action
        if self.n <= 0:
            return None , -1
        else:
            return self.n , 0
        
class player(object): 

    def __init__(self , is_human , size , trainable = True):
        super(player , self).__init__()
        self.is_human = is_human
        self.history = []
        self.V = {}
        for s in range(1 , size + 1):
            self.V[s] = 0.
        self.win_n = 0.
        self.lose_n = 0.
        self.rewards = []
        self.eps = 0.99
        self.trainable = trainable

    def reset_stat(self):
        self.win_n = 0
        self.lose_n = 0
        self.rewards = []

    #e-greedy algorithm
    def greedy(self , state):
        action = [1 , 2 , 3]
        vmin = None
        vi = None
        for i in range(0 , 3):
            a = action[i]
            if state - a > 0 and (vmin is None or vmin > self.V[state - a]):
                vmin = self.V[state - a]
                vi = i
        return action[vi if vi is not None else 1]
    
    def play(self , state):
        if self.is_human is False:
            if random.uniform(0 , 1) < self.eps:
                action = randint(1 , 3)
            else:
                action = self.greedy(state)
        else:
            action = int(input("S>"))
        return action
    
    def add_transition(self , n_tuple):
        self.history.append(n_tuple)
        s , a , r , sp = n_tuple
        self.rewards.append(r)

    def train(self):
        if not self.trainable or self.is_human is True:
            return
        
        #Update Value function is the player is not human
        for transition in reversed(self.history):
            s , a , r , sp = transition
            if r == 0:
                self.V[s] = self.V[s] + 0.001*(self.V[sp] - self.V[s])
            else:
                self.V[s] = self.V[s] + 0.001*(r - self.V[s])

        self.history = []

def play(game , p1 , p2 , train = True):
    state = game.reset()
    players = [p1 , p2]
    random.shuffle(players)
    p = 0
    while game.over() is False:

        if players[p % 2].is_human:
            game.display()

        action = players[p % 2].play(state)
        n_state , reward = game.step(action)

        if (reward != 0):
            players[p % 2].lose_n += 1. if reward == -1 else 0
            players[p % 2].win_n += 1. if reward == 1 else 0

            #Updating stat
            player[(p + 1) % 2].lose_n +1 if reward == 1 else 0
            players[(p + 1) % 2].win_n += 1. if reward == -1 else 0

        if p != 0:
            s , a , r , sp = players[(p + 1) % 2].history[-1]
            players[(p + 1) % 2].history[-1] = (s , a , reward * -1 , n_state)

        players[p % 2].add_transition((state , action , reward , None))

        state = n_state
        p += 1

    if train:
        p1.train()
        p2.train()

if __name__ == '__main__':
    game = Stickgame(12)

    #Players to train
    p1 = player(is_human = False , size = 12 , trainable = True)
    p2 = player(is_human = False , size = 12 , trainable = True)

    #VS random player
    human = player(is_human = True , size = 12 , trainable = False)
    random_player = player(is_human = False , size = 12 , trainable = False)

    #The agent
    for i in range(0 , 10000):
        if i % 10 == 0:
            p1.eps = max(p1.eps * 0.996 , 0.05)
            p2.eps = max(p2.eps * 0.996 , 0.05)
        play(game , p1 , p2)
    p1.reset_stat()

    #Value_function
    for key in p1.V:
        print(key , p1.V[key])
    print("----------------------------------------")

    for _ in range(0 , 1000):
        play(game , p1 , random_player , train = False)
    print("p1 win rate : " ,  p1.win_n / (p1.win_n + p1.lose_n))
    print("p1 win mean : " , np.mean(p1.rewards))

    while True:
        play(game , p1 , human , train = False)

            


















        
