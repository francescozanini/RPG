import numpy as np
import pandas as pd
from RPG import Character
from RLsuggestion import *

hero = Character.init_given_character('Warrior', False)
enemy = Character.init_given_character('Warrior', False)

num = 100


for i in range(num):
    Character.battle(hero, enemy)

print('*************************************')

table = mc_control(num)

print(table)


ones = 10*np.ones(len(table[0]))

dist = np.zeros((len(table), len(table[0])))
for i in range(len(table)):
    dist[i] = np.exp(table[i])/sum(np.exp(table[i]))
    
#dist2 = np.zeros((len(table), len(table[0])))
#for i in range(len(table)):
    #dist2[i] = (table[i] + ones)/sum(table[i] + ones)
    
print(dist)
#print(dist2)
    



