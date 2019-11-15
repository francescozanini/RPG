import Character as RPG
from UsableItem import *
from tools import *
import pandas as pd
import os

def fight(player, inventory):
    AP_low = player.ap - 5
    AP_high = player.ap + 5

    B = RPG.Character.init_random_character()

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
        while not (sensible_user_choice):
            i = 1
            for item in action_names:
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
            succ = RPG.Character.action_succeeds(curr_act)
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

                succ2 = RPG.Character.action_succeeds(enemy_action)

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
        row = [char1.__class__.__name__, char2.__class__.__name__, char1.hp, char2.hp, char1.mp, char2.mp]
        char1_action, char1_action_num = char1.choose_random_action()
        if RPG.Character.action_succeeds(char1_action, False):
            damage2, damage1 = action_consequences(char1, char2, char1_action, char1.ap, char1.ap)
            row = row + [char1_action_num, -1, damage1, damage2]
        else:
            row = row + [char1_action_num, -1, 0, 0]

        if save_battle:
            battle_stats.loc[turn] = row
        turn += 1

        if char2.is_alive():
            assert (char2.has_possible_action())
            row = [char1.__class__.__name__, char2.__class__.__name__, char1.hp, char2.hp, char1.mp, char2.mp]
            char2_action, char2_action_num = char2.choose_random_action()
            if RPG.Character.action_succeeds(char2_action, False):
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
        recovered_health = random.randrange(A.max_hp * 0.05, A.max_hp * 0.15)
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