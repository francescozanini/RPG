import numpy as np
import pandas as pd
from RPG import Character
from RLsuggestion import *

hero = Character.init_given_character('Warrior', False)
enemy = Character.init_given_character('Warrior', False)

num = 1000


for i in range(num):
    Character.battle(hero, enemy)

'''
def suggestion(hero, enemy, current_hp_1, current_mp_1, current_hp_2, current_mp_2, num_battle):
    hp_tol = 10
    mp_tol = 15

    total_dataframe = pd.DataFrame()

    for i in range(num_battle):
        A = pd.read_csv('./battles/' + 'battle' + str(i) + '.csv', index_col=0)
        if (A.iloc[0].loc['1_race'] == hero) and (A.iloc[0].loc['2_race'] == enemy):
            A = A[(A['1_hps'] <= current_hp_1 + hp_tol)]
            A = A[(A['1_hps'] >= current_hp_1 - hp_tol)]
            A = A[(A['1_mps'] <= current_mp_1 + mp_tol)]
            A = A[(A['1_mps'] >= current_mp_1 - mp_tol)]
            A = A[(A['2_hps'] <= current_hp_2 + hp_tol)]
            A = A[(A['2_hps'] >= current_hp_2 - hp_tol)]
            A = A[(A['2_mps'] <= current_mp_2 + mp_tol)]
            A = A[(A['2_mps'] >= current_mp_2 - mp_tol)]
            frames = [total_dataframe, A]
            total_dataframe = pd.concat(frames, ignore_index=True)

    print(total_dataframe)
    overall_damage = total_dataframe['1_damage'] - total_dataframe['2_damage']
    print('####################')
    print(overall_damage)
    idx = overall_damage.idxmin()
    print('####################')
    print(idx)
    print('####################')
    print(total_dataframe.iloc[idx])
    print('####################')
    return total_dataframe.iloc[idx].loc['1_action']


selected_action = suggestion('Wizard', 'Cleric', 5000, 200, 50000, 80, num)

print(selected_action)
'''

'''
current_hp = 5000
current_mp = 200

total_dataframe = pd.DataFrame()

hp_tol = 10
mp_tol = 15

num_battle = 2
for i in range(num_battle):
    A = pd.read_csv('battle' + str(i+5) + '.csv', index_col=0)
    if (A.iloc[0].loc['1_race'] == 'Wizard') and (A.iloc[0].loc['2_race'] == 'Cleric'):
        A = A[(A['1_hps'] <= current_hp_1 + hp_tol)]
        A = A[(A['1_hps'] >= current_hp_1 - hp_tol)]
        A = A[(A['1_mps'] <= current_mp_1 + mp_tol)]
        A = A[(A['1_mps'] >= current_mp_1 - mp_tol)]
        A = A[(A['2_hps'] <= current_hp_2 + hp_tol)]
        A = A[(A['2_hps'] >= current_hp_2 - hp_tol)]
        A = A[(A['2_mps'] <= current_mp_2 + mp_tol)]
        A = A[(A['2_mps'] >= current_mp_2 - mp_tol)]
        frames = [total_dataframe, A]
        total_dataframe = pd.concat(frames)

print(total_dataframe)

overall_damage = total_dataframe['1_damage'] - total_dataframe['2_damage']
print('############################')
print(overall_damage)
idx = overall_damage.idxmin()
print(idx)
'''

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
    



