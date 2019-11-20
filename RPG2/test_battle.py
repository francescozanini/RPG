from RPG import Character
import numpy as np
import fight
from RLsuggestion import mc_control

num_battles = 10

'''
arr_char1_won = []
arr_char2_won = []
arr_num_turns = []
arr_num_turns = []
arr_hp1 = []
arr_mp1 = []
# char2_won, num_turns, hp1, mp1
# classes = ['Warrior', 'Wizard', '']
classes = Character.get_character_list()
levels = [0,1]
for i in range(0, num_battles):
    print(i)

    # char1 = Character.init_random_character()
    for race in classes:
        for l in levels:
            char1 = Character.init_given_character(race, False)
            char2 = fight.choose_best_opponent(char1, l) #novice
            # char2 = Character.init_random_character()
            char1_won, char2_won, num_turns, hp1, mp1 = fight.battle(char1, char2, save_battle=True)
            arr_char1_won.append(1 if char1_won else 0)
            arr_char2_won.append(1 if char2_won else 0)
            arr_num_turns.append(num_turns)
            arr_hp1.append(hp1)
            arr_mp1.append(mp1)

print("W1 avg:", sum(arr_char1_won) / len(arr_char1_won))
print("L1 avg:", sum(arr_char2_won) / len(arr_char2_won))
print("Num turns avg:", sum(arr_num_turns) / len(arr_char2_won))
print("HP1 avg:", sum(arr_hp1) / len(arr_hp1))
print("HP2 avg:", sum(arr_mp1) / len(arr_mp1))
'''

import best_opponent

def key_dict(level, character):
    if level:
        lstr = 'skilled'
    else:
        lstr = 'novice'
    nstr = character.name.lower()

    return lstr + '_' + nstr

dict_optimal_move = dict()

classes = Character.get_character_list()
levels = [0,1]
for race in classes:
    char1 = Character.init_given_character(race, False)
    for l in levels:
        for i in range(num_battles):
            char2 = fight.choose_best_opponent(char1, l)
            fight.battle(char1, char2, save_battle=True)
        dict_optimal_move[key_dict(l, char1)] = mc_control(num_battles)
            # volendo qui si può pulire la cartella dai file creati sopra

print(dict_optimal_move)
