from RPG import Character
import numpy as np

def check_novice(arr):
    tot = (arr[0] > 0.96) and (arr[3] > 0.7) and (arr[4] > 0.5)
    return tot

def check_novice2(arr):
    tot = (arr[0] > 0.7) and (arr[0] < 0.9) #and (arr[3] > 0.6) and (arr[4] > 0.5)
    return tot

def check_skilled(arr):
    tot = (arr[0] > 0.57 and arr[0] < 0.63) and (arr[2] > 7)
    return tot

def check_skilled2(arr):
    tot = (arr[0] > 0.5 and arr[0] < 0.7) and (arr[2] > 3)
    return tot

def select_reasonable_enemy(A, C):
    B = np.zeros((A.shape[1], A.shape[2]))
    # B2 = np.zeros((A.shape[1], A.shape[2]))
    for j in range(A.shape[2]):  # j enemies
        for i in range(A.shape[1]):  # i 5 parametri
            # B1[i][j] = np.mean(A[:,i,j]) #20x5x1000
            B[i][j] = np.mean(A.T[j], axis=1)[i]
    if C == 'Novice':
        for i in range(B.shape[1]):  # i nemici
            if check_novice(B.T[i]):
                return i
        return -1
    elif C == 'Skilled':
        for i in range(B.shape[1]):  # i column index
            print(B.T)
            if check_skilled2(B.T[i]):
                return i
        return -1

action_set_1 = [{'name': 'Punch', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                {'name': 'Kick', 'type': 'physical', 'dmg': 60, 'succ': 0.80, 'mp_cost': 0},
                {'name': 'Chuck Norris roundhouse kick', 'type': 'physical', 'dmg': 9999, 'succ': 0.001, 'mp_cost': 0}]

action_set_2 = [{'name': 'Punch', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                {'name': 'Fire', 'type': 'spell', 'dmg': 60, 'succ': 0.80, 'mp_cost': 10},
                {'name': 'Thunder', 'type': 'spell', 'dmg': 80, 'succ': 0.75, 'mp_cost': 20},
                {'name': 'Blizzard', 'type': 'spell', 'dmg': 60, 'succ': 0.80, 'mp_cost': 10}]

action_set_3 = [{'name': 'Divine Intervention', 'type': 'spell', 'dmg': 500, 'succ': 0.30, 'mp_cost': 40},
                {'name': 'Beads Throw', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                {'name': 'Excommunication', 'type': 'spell', 'dmg': 60, 'succ': 0.80, 'mp_cost': 10}]

action_set_4 = [{'name': 'Punio', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                {'name': 'Sbatti Porta', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                {'name': 'Ma Che Oh', 'type': 'spell', 'dmg': 600, 'succ': 0.50, 'mp_cost': 100}]

action_set_5 = [{'name': 'Lute Hit', 'type': 'physical', 'dmg': 80, 'succ': 0.70, 'mp_cost': 0},
                {'name': 'Arrow', 'type': 'physical', 'dmg': 100, 'succ': 0.60, 'mp_cost': 0},
                {'name': 'Song Of Death', 'type': 'spell', 'dmg': 50, 'succ': 0.80, 'mp_cost': 100}]

ranges = {'HPs': np.linspace(20, 2000, 6),
          'MPs': np.linspace(20, 2000, 6),
          'APs': np.linspace(20, 1000, 6),
          'Actions': [action_set_1, action_set_2, action_set_3, action_set_4, action_set_5]}

enemy_table = np.array(np.meshgrid(ranges['HPs'], ranges['MPs'], ranges['APs'], ranges['Actions']))
enemy_table = enemy_table.T.reshape(-1, 4)

# character01 = Character('custom01', 'NPC', max_hp=player.hp, max_mp=player.mp, ap=player.ap, actions=player.actions)
character01 = Character.init_given_character('Warrior', False)
epochs = 20
enemies = len(enemy_table)
data = 5

data_fight = np.empty([epochs, 5, enemies])
for epoc in range(0, epochs):
    for i in range(0, enemies):
        character02 = Character('custom02', 'NPC', max_hp=enemy_table[i][0], max_mp=enemy_table[i][1],
                                ap=enemy_table[i][2], actions=enemy_table[i][3])
        f01, f02, n_round, remain_hp, remaining_mp = Character.battle(character01, character02)
        data_fight[epoc, 0, i] = 1 if f01 else 0
        data_fight[epoc, 1, i] = 1 if f02 else 0
        data_fight[epoc, 2, i] = n_round
        data_fight[epoc, 3, i] = remain_hp
        data_fight[epoc, 4, i] = remaining_mp

# print(data_fight[0])
idx = select_reasonable_enemy(data_fight, 'Skilled')
chosen_enemy = data_fight[:, :, idx]
for epoch in range(epochs):
    assert(chosen_enemy[epoc, 0] + chosen_enemy[epoc, 1] == 1)
print(data_fight.shape)
print(chosen_enemy.shape)

avg_wins = np.mean(chosen_enemy[:, 0])
avg_loss = np.mean(chosen_enemy[:, 1])
print("idx=", idx)
print("avg wins=", avg_wins)
print("avg loss=", avg_loss)
