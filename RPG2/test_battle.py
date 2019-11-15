import Character as RPG
import numpy as np
import fight

num_battles = 3

arr_char1_won = []
arr_char2_won = []
arr_num_turns = []
arr_num_turns = []
arr_hp1 = []
arr_mp1 = []
# char2_won, num_turns, hp1, mp1
for i in range(0, num_battles):
    print(i)
    char1 = RPG.Character.init_random_character()
    char2 = RPG.Character.init_random_character()
    char1_won, char2_won, num_turns, hp1, mp1 = fight.battle(char1, char2, save_battle=False)
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