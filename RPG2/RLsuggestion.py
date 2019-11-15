import numpy as np
import pandas as pd
from RPG import Character

def mc_control(n_epi, gamma = 1):
    A = pd.read_csv('./battles/' + 'battle' + str(0) + '.csv', index_col=0)
    fake_hero = Character.init_given_character(A.iloc[0].loc['1_race'], False)
    s_space = 9
    a_space = len(fake_hero.get_actions())
    Q_table = np.zeros((s_space, a_space), dtype = np.float32)
    counter = np.zeros((s_space, a_space), dtype = np.int32)

    for i in range(n_epi):
        data = pd.read_csv('./battles/' + 'battle' + str(i) + '.csv', index_col=0)
        sequence, rewards = generate_epi(data)
        G = 0

        for t in range(len(sequence) -1, -1, -1):
            R = rewards[t]
            S_A = sequence[t]
            G = gamma * G + R

            if S_A not in sequence[:t]:
                counter[S_A[0], S_A[1]] += 1
                Q_table[S_A[0], S_A[1]] += (G - Q_table[S_A[0], S_A[1]]) / counter[S_A[0], S_A[1]]

    print(counter)
    return Q_table

def generate_epi(dataframe):
    '''
    Stato 0: hero > 50, enemy > 50
    Stato 1: hero > 50, enemy middle
    Stato 2: hero > 50, enemy < 25
    Stato 3: hero middle, enemy > 50
    Stato 4: hero middle, enemy middle
    Stato 5: hero middle, enemy < 25
    Stato 6: hero < 25, enemy > 50
    Stato 7: hero < 25, enemy middle
    Stato 8: hero < 25, enemy < 25
    '''

    fake_hero = Character.init_given_character(dataframe.iloc[0].loc['1_race'], False)
    fake_enemy = Character.init_given_character(dataframe.iloc[0].loc['2_race'], False)
    h_max_hp = fake_hero.max_hp
    e_max_hp = fake_enemy.max_hp
    

    sequence, rewards = [], []

    for i in range(0, len(dataframe), 2):

        if (dataframe.iloc[i].loc['1_hps'] / h_max_hp) > 0.50:

            if (dataframe.iloc[i].loc['2_hps'] / e_max_hp) > 0.50:
                S = 0

            elif (dataframe.iloc[i].loc['2_hps'] / e_max_hp) < 0.25:
                S = 2

            else:
                S = 1

        elif (dataframe.iloc[i].loc['1_hps'] / h_max_hp) < 0.25:

            if (dataframe.iloc[i].loc['2_hps'] / e_max_hp) > 0.50:
                S = 6

            elif (dataframe.iloc[i].loc['2_hps'] / e_max_hp) < 0.25:
                S = 8

            else:
                S = 7

        else:

            if (dataframe.iloc[i].loc['2_hps'] / e_max_hp) > 0.50:
                S = 3

            elif (dataframe.iloc[i].loc['2_hps'] / e_max_hp) < 0.25:
                S = 5

            else:
                S = 4

        A = dataframe.iloc[i].loc['1_action']

        sequence.append((S, A))

        if i+1 == len(dataframe)-1:
            
            i = i+1       

            if (dataframe.iloc[i].loc['1_hps'] - dataframe.iloc[i].loc['1_damage']) <= 0:
                rewards.append(-10)

            elif (dataframe.iloc[i].loc['2_hps'] - dataframe.iloc[i].loc['2_damage']) <= 0:
                rewards.append(10)

        else:
            
            if (dataframe.iloc[i].loc['1_hps'] - dataframe.iloc[i].loc['1_damage']) <= 0:
                rewards.append(-10)

            elif (dataframe.iloc[i].loc['2_hps'] - dataframe.iloc[i].loc['2_damage']) <= 0:
                rewards.append(10)
                
            else:
                rewards.append(0)

    return sequence, rewards
