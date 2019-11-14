import numpy as np
import pandas as pd
from RPG import save_battle_as_dataframe
from RPG import battle
# Non so come importare le funzioni da altri file

hero = Character.init_given_character(Wizard, False)
enemy = Character.init_given_character(Cleric, False)

num = 5

for i in range(num):
    battle(hero, enemy)

def suggestion(hero, enemy, current_hp_1, current_mp_1, current_hp_2, current_mp_2, num_battle):
    hp_tol = 10
    mp_tol = 15

    total_dataframe = pd.DataFrame()

    for i in range(num_battle):
        A = pd.read_csv('battle' + str(i) + '.csv', index_col=0)
        if (A.iloc[0].loc['1_race'] == 'hero') and (A.iloc[0].loc['2_race'] == 'enemy'):
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

    overall_damage = total_dataframe['1_damage'] - total_dataframe['2_damage']
    idx = overall_damage.idxmin()

    return A.iloc[idx].loc['1_action']


selected_action = suggestion(Wizard, Cleric, 4000, 100, 10000, 0, num)

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
