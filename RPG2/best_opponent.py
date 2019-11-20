# import Character
from RPG import Character
from fight import *
import numpy as np
import pandas as pd

num_battles = 10

Hero_Name = []
Won1_prob = []
Won2_prob = []
Mean_Nturns = []
EnemyHP = []
EnemyMP = []
EnemyAP = []
Enemy_Action_Set = []
Enemy_Name = []

action1 = [{'name': 'Punch', 'type': 'physical', 'dmg': 5, 'succ': 0.90, 'mp_cost': 0},
           {'name': 'Kick', 'type': 'physical', 'dmg': 10, 'succ': 0.70, 'mp_cost': 0},
           {'name': 'Chuck Norris roundhouse kick', 'type': 'physical', 'dmg': 20, 'succ': 0.01,'mp_cost': 0},
           {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]
action2 = [{'name': 'Fire', 'type': 'spell', 'dmg': 6, 'succ': 0.80, 'mp_cost': 10},
           {'name': 'Thunder', 'type': 'spell', 'dmg': 9, 'succ': 0.75, 'mp_cost': 20},
           {'name': 'Blizzard', 'type': 'spell', 'dmg': 6, 'succ': 0.80, 'mp_cost': 10},
           {'name': 'Punch', 'type': 'physical', 'dmg': 5, 'succ': 0.90, 'mp_cost': 0},
           {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]
action3 = [{'name': 'Divine Intervention', 'type': 'spell', 'dmg': 10, 'succ': 0.50, 'mp_cost': 40},
           {'name': 'Beads Throw', 'type': 'physical', 'dmg': 5, 'succ': 0.90, 'mp_cost': 0},
           {'name': 'Excommunication', 'type': 'spell', 'dmg': 6, 'succ': 0.80, 'mp_cost': 10},
           {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]
action4 = [{'name': 'Punio', 'type': 'physical', 'dmg': 8, 'succ': 0.70, 'mp_cost': 0},
           {'name': 'Sbatti Porta', 'type': 'physical', 'dmg': 5, 'succ': 0.90, 'mp_cost': 0},
           {'name': 'Ma Che Oh', 'type': 'spell', 'dmg': 20, 'succ': 0.10, 'mp_cost': 20},
           {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]
action5 = [{'name': 'Lute Hit', 'type': 'physical', 'dmg': 8, 'succ': 0.70, 'mp_cost': 0},
           {'name': 'Arrow', 'type': 'physical', 'dmg': 10, 'succ': 0.60, 'mp_cost': 0},
           {'name': 'Song Of Death', 'type': 'spell', 'dmg': 5, 'succ': 0.80, 'mp_cost': 20},
           {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]

ranges = {'HPs': np.linspace(400, 1200, 6),
          'MPs': np.linspace(10, 200, 6),
          'APs': np.linspace(10, 30, 6),
          'Actions': [action1, action2, action3, action4, action5]}

enemy_table = np.array(np.meshgrid(ranges['HPs'], ranges['MPs'], ranges['APs'], ranges['Actions']))
enemy_table = enemy_table.T.reshape(-1, 4)
enemies = len(enemy_table)

heroes = Character.get_character_list()

for hero in heroes:
    char1 = Character.init_given_character(hero, True)
    for i in range(0, enemies):
        char2 = Character('evil_character', 'NPC', max_hp=enemy_table[i][0], max_mp=enemy_table[i][1],
                            ap=enemy_table[i][2], actions=enemy_table[i][3])
        num_win1 = 0
        num_win2 = 0
        num_turns = 0
        for j in range(0, num_battles):
            char1_won, char2_won, turns, _, _  = battle(char1, char2, save_battle=False)
            if not (char1_won and char2_won):
                num_win1 +=char1_won
                num_win2 +=char2_won
                num_turns+=turns

        Hero_Name.append(char1.name)
        Won1_prob.append(num_win1/num_battles)
        Won2_prob.append(num_win2/num_battles)
        Mean_Nturns.append(num_turns/num_battles)
        EnemyHP.append(enemy_table[i][0])
        EnemyMP.append(enemy_table[i][1])
        EnemyAP.append(enemy_table[i][2])
        Enemy_Action_Set.append(enemy_table[i][3])
        if enemy_table[i][3] == action1:
                Enemy_Name.append('Ninja')
        elif enemy_table[i][3] == action2:
                Enemy_Name.append('Shaman')
        elif enemy_table[i][3] == action3:
                Enemy_Name.append('Assassin')
        elif enemy_table[i][3] == action4:
                Enemy_Name.append('Mastrota')
        elif enemy_table[i][3] == action5:
                Enemy_Name.append('Pirate')

battles_record = pd.DataFrame(data=[Hero_Name,Won1_prob,Won2_prob,Mean_Nturns,EnemyHP,EnemyMP,EnemyAP,Enemy_Action_Set,Enemy_Name]).T
battles_record.columns=['Hero_Name','Prob_Hero_Won','Prob_Hero_Lose','mean_Nturns','Enemy_HP','Enemy_MP','Enemy_AP', 'Enemy_Action_Set', 'Enemy_Name']

battles_record.to_csv(r'best_opponent_LUT.csv')
