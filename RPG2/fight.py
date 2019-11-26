from RPG import Character
from UsableItem import *
from tools import *
import pandas as pd
import os
from RLsuggestion import get_status
import pickle
import numpy as np
import ast
from RLsuggestion import mc_control


def sample_from_pdf(pdf_vec):
    probs = np.cumsum(pdf_vec)
    num = random.random()

    for i in range(len(probs)):
        if num < probs[i]:
            return i

def fight(player, inventory, story=None):
    AP_low = player.ap - 5
    AP_high = player.ap + 5

    # B = RPG.Character.init_random_character()
    B = choose_best_opponent_from_csv(player, story.difficulty_level)
    AP_enemy_low = B.ap - 2
    AP_enemy_high = B.ap + 2
    print('You have encountered the mighty {}!'.format(B.name))
    while True:
        print('\nHero stats:')
        player.print_status()
        print('\nEnemy stats:')
        B.print_status()
        print('\nTurn of the hero:')

        action_names = player.get_action_names()
        inventory_list = get_inventory_list(inventory)
        actions = player.get_actions()
        print('Actions available:')
        sensible_user_choice = False
        # story_id = story.get_diffuculty_level().lower() + '_' + player.name.lower()
        story_id = key_dict(story.difficulty_level, player)
        action_names_for_user = action_names.copy()
        if story_id in get_dict():
            s = get_status(player.hp, player.max_hp, B.hp, B.max_hp)
            optimal_moves = get_dict()[story_id]
            optimal_move_for_status = optimal_moves[s]
            suggested_action_idx = sample_from_pdf(optimal_move_for_status)
            action_names_for_user[suggested_action_idx] = action_names_for_user[suggested_action_idx]+' <--'

        while not (sensible_user_choice):
            i = 1
            for item in action_names_for_user:
                print(str(i) + ': ', item)
                i += 1
            l = 1
            print('Items available:')
            for item in inventory_list:
                print(str(l + i - 1) + ': ', item)
                l += 1
            choice = input('Choose action: ')
            if is_integer(choice):
                choice = int(choice)
                sensible_user_choice = (choice > 0) and (choice < l + i)

            if not (sensible_user_choice):
                print('Choice not recognized')
            else:
                if player.is_choice_fight_action(choice, i):
                    sensible_user_choice = player.can_do_action(choice - 1)
                    if not (sensible_user_choice):
                        print("Not enough MPs to perform action")
        # we have a sensible user choice
        if choice == len(action_names):  # Run away
            print('You chose to run away')
            prob = 0.7
            succ = random.random() < prob
            if succ:
                print('Successful escaping!')
                return
            else:
                print('Too slow! Failed to escape...')
        elif choice > len(action_names):
            useItem(inventory, choice - i + 1, player, B)
        else:  # attack
            curr_act = actions[choice - 1]
            print('Aiming at the opponent for the powerful {}...'.format(action_names[choice - 1]))
            succ = Character.action_succeeds(curr_act)
            if succ:
                damage, _ = action_consequences(player, B, curr_act, AP_low, AP_high)
                # A.mp -= curr_act['mp_cost']
                # damage = random.randrange(AP_low, AP_high) * curr_act['dmg']
                # B.hp -= damage
                print('Attack successful! You have inflicted {} HP!'.format(damage))
            else:
                print('Attack failed!')
            print('The enemy has still {} HP'.format(B.hp))
        if B.is_dead():
            print('VICTORY, the enemy is defeated')
            if random.choice([True, False]):
                item01 = Potion('pozione')
            else:
                item01 = Poison('veleno')
            print('Found ' + item01.name)
            inventory = addItem(inventory, item01)
            return
        else:
            print('\nTurn of the enemy')
            if not (B.has_possible_action()):
                print('Enemy cannot perform any move')
            else:
                enemy_action, _ = B.choose_random_action()
                print('The enemy is loading {} move...'.format(enemy_action['name']))

                succ2 = Character.action_succeeds(enemy_action)

                if succ2:
                    # B.mp -= enemy_action['mp_cost']
                    # damage2 = random.randrange(AP_enemy_low, AP_enemy_high) * enemy_action['dmg']
                    # A.hp -= damage2
                    damage2, _ = action_consequences(B, player, enemy_action, AP_enemy_low, AP_enemy_high)
                    print('You have been hitted for {} HP!'.format(damage2))
                else:
                    print('You dogded the enemy attack!')
                if (player.is_dead()):
                    print('Bad news...')
                    return


def battle(char1, char2, save_battle=True):
    stat_names = ['1_race', '2_race', '1_hps', '2_hps', '1_mps', '2_mps',
                  '1_action', '2_action', '1_damage', '2_damage']
    if save_battle:
        battle_stats = pd.DataFrame(columns=stat_names)
    turn = 0
    char1.rest(False)
    char2.rest(False)
    #reporting battle stats for char1
    while True:
        assert (char1.has_possible_action())
        row = [char1.name, char2.name, char1.hp, char2.hp, char1.mp, char2.mp]
        char1_action, char1_action_num = char1.choose_random_action()
        if Character.action_succeeds(char1_action, False):
            damage2, damage1 = action_consequences(char1, char2, char1_action, char1.ap, char1.ap)
            row = row + [char1_action_num, -1, damage1, damage2]
        else:
            row = row + [char1_action_num, -1, 0, 0]

        if save_battle:
            battle_stats.loc[turn] = row
        turn += 1

        if char2.is_alive():
            assert (char2.has_possible_action())
            row = [char1.name, char2.name, char1.hp, char2.hp, char1.mp, char2.mp]
            char2_action, char2_action_num = char2.choose_random_action()
            if Character.action_succeeds(char2_action, False):
                damage1, damage2 = action_consequences(char2, char1, char2_action, char2.ap, char2.ap)
                row = row + [-1, char2_action_num, damage1, damage2]
            else:
                row = row + [-1, char2_action_num, 0, 0]
        if save_battle:
            battle_stats.loc[turn] = row
        turn += 1
        assert (char1.has_possible_action() or char2.has_possible_action())

        #we are assuming at least one player can always fight. If we explode here something went wrong
        if char1.is_dead() or char2.is_dead():
            char1_won = char2.is_dead()
            char2_won = char1.is_dead()
            assert not(char1_won and char2_won)
            hp1_perc = char1.hp / char1.max_hp
            mp1_perc = char1.mp / char1.max_mp
            assert(hp1_perc == 0 or char1_won)
            if save_battle:
                save_battle_as_dataframe(battle_stats)
            return char1_won, char2_won, turn, hp1_perc, mp1_perc

def action_consequences(A, B, action, AP_low, AP_high):
    damage_self = 0
    damage_enemy = 0
    if action['type'] == 'heal':
        # recovered_health = random.randrange(A.max_hp * 0.05, A.max_hp * 0.15)
        recovered_health = random.randrange(round(A.max_hp * 0.005), round(A.max_hp * 0.015))
        old_hps = A.hp
        A.hp = min(A.max_hp, A.hp + recovered_health)
        # recovered_health = self.hp - old_hps
        damage_self = -1 * recovered_health
    else:
        A.mp -= action['mp_cost']
        damage = random.randrange(AP_low, AP_high + 1) * action['dmg']
        B.hp -= damage
        B.hp = max(0, B.hp)
        damage_enemy = damage
    return damage_enemy, damage_self

def save_battle_as_dataframe(df):
    folder = './battles/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    num_last_battle = -1
    for file in os.listdir(folder):
        if file.endswith(".csv") and file.startswith('battle'):
            file = file.strip('battle')
            file = file.strip('.csv')
            num_last_battle = max(int(file),num_last_battle)
    new_file_name = folder + "battle" + str(num_last_battle + 1) + ".csv"
    df.to_csv(new_file_name)


def choose_best_opponent_from_csv(player, difficulty_level):
    fname = 'best_opponent_LUT.csv'
    if os.path.isfile(fname):
        battles_record = pd.read_csv(fname)
    else:
        print("Couldn't find csv with battles. Launching battle simulation...")
        run_battle_simulations()
        battles_record = pd.read_csv(fname)
        print("Done")
    # battles_record = pd.read_csv(fname)
    evil_character_names = ['Ninja', 'Shaman', 'Assassin', 'Mastrota', 'Pirate']
    name = random.choice(evil_character_names)

    if not difficulty_level:  # easy mode
        mask = (battles_record['Hero_Name'] == player.name) & \
               (battles_record['Prob_Hero_Won'] >= 0.8) & \
               (battles_record['Enemy_Name'] == name)
    if difficulty_level:  # expert mode
        mask = (battles_record['Hero_Name'] == player.name) & \
               (battles_record['Prob_Hero_Won'] >= 0.3) & \
               (battles_record['Prob_Hero_Won'] <= 0.8) & \
               (battles_record['mean_Nturns'] >= 7) & \
               (battles_record['Enemy_Name'] == name)

    filtered_opponents = battles_record[mask]

    indexes = list(filtered_opponents.index)
    index_chosen = random.choice(indexes)

    # get evil character stats

    max_hp = filtered_opponents.loc[index_chosen, 'Enemy_HP']
    max_mp = filtered_opponents.loc[index_chosen, 'Enemy_MP']
    ap = filtered_opponents.loc[index_chosen, 'Enemy_AP']
    # randomize stats
    random_percentage = 0.05
    max_hp += round(random_percentage * max_hp * (2 * random.random() - 1))
    max_mp += round(random_percentage * max_mp * (2 * random.random() - 1))
    ap += round(random_percentage * ap * (2 * random.random() - 1))

    actions = ast.literal_eval(filtered_opponents.loc[index_chosen, 'Enemy_Action_Set'])
    opponent = Character(name, 'NPC', int(max_hp), int(max_mp), int(ap), actions)
    return opponent

def run_battle_simulations(num_battles=10):

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

def get_dict():
    fname = 'optimal_moves.pickle'
    if not os.path.isfile(fname):
        print("Loading dictionary with optimal moves...")
        compute_optimal_moves(save=True)
        print("Done")
    with open(fname, 'rb') as handle:
        dict = pickle.load(handle)
    return dict

def key_dict(level, character):
    if level:
        lstr = 'skilled'
    else:
        lstr = 'novice'
    nstr = character.name.lower()

    return lstr + '_' + nstr

def compute_optimal_moves(num_battles=10, save=False):
    dict_optimal_move = dict()

    classes = Character.get_character_list()
    levels = [0, 1]
    for race in classes:
        char1 = Character.init_given_character(race, False)
        for l in levels:
            Character.clear_battle_dataframes()
            for i in range(num_battles):
                char2 = choose_best_opponent_from_csv(char1, l)
                battle(char1, char2, save_battle=True)
            dict_optimal_move[key_dict(l, char1)] = mc_control(num_battles)
    if save:
        with open('optimal_moves.pickle', 'wb') as handle:
            pickle.dump(dict_optimal_move, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return dict_optimal_move