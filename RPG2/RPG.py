import random
from time import sleep
import numpy as np
from UsableItem import *
import pandas as pd
import os

class Character:
    def __init__(self, name, character_type, max_hp, max_mp, ap, actions):
        self.name = name
        self.character_type = character_type
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.ap = ap
        self.actions = actions

    # Providing info about the Character
    def show_stats(self):
        print('HP: %4d/%4d, MP: %4d/%4d' % (self.hp, self.max_hp, self.mp, self.max_mp))

    def rest(self, print_mssg=True):
        self.hp = self.max_hp
        self.mp = self.max_mp
        if print_mssg:
            print('Your points have been restored to the maximum value!')

    def can_do_action(self, action_number):
        actions = self.get_actions()
        action = actions[action_number]
        try:
            result = action['mp_cost'] <= self.mp
        except:
            a=0
        return result

    def has_possible_action(self):
        for action_number in range(0, len(self.get_actions())):
            if self.can_do_action(action_number):
                return True
        return False

    def is_choice_fight_action(self, choice, num):
        return (choice <= len(self.get_actions()))

    def is_player(self):
        return self.character_type == 'Player'

    def is_dead(self):
        return self.hp <= 0

    def is_alive(self):
        return not(self.is_dead())

    def get_actions(self):
        action_list = []
        for action in self.actions:
            action_list.append(action)
        return action_list

    def get_action_names(self):
        actions = self.get_actions()
        action_names = [action['name'] for action in actions]
        if self.is_player():
            action_names.append('Run')
        return action_names

    def choose_random_action(self):
        while True:
            actions = self.get_actions()
            action_number = random.randrange(len(actions))
            if self.can_do_action(action_number):
                return actions[action_number], action_number

    def print_status(self):
        print('HP: {}'.format(self.hp))
        print('MP: {}'.format(self.mp))

    def action_consequences(self, B, action, AP_low, AP_high):
        damage_self = 0
        damage_enemy = 0
        if action['type'] == 'heal':
            recovered_health = random.randrange(self.max_hp*0.05, self.max_hp*0.15)
            old_hps = self.hp
            self.hp = min(self.max_hp, self.hp+recovered_health)
            # recovered_health = self.hp - old_hps
            damage_self = -1*recovered_health
        else:
            self.mp -= action['mp_cost']
            damage = random.randrange(AP_low, AP_high+1) * action['dmg']
            B.hp -= damage
            B.hp = max(0, B.hp)
            damage_enemy = damage
        return damage_enemy, damage_self

    @staticmethod
    def action_succeeds(act, wait=True):
        prob = act['succ']
        succ = random.random() < prob
        if wait:
            sleep(1 + 2*random.random())
        return succ

    @staticmethod
    def get_character_list():
        char_list = [subclass.__name__ for subclass in Character.__subclasses__()]
        return char_list

    @staticmethod
    def init_given_character(character_name, is_player):
        for subclass in Character.__subclasses__():
            if character_name == subclass.__name__:
                return subclass(is_player)

    @staticmethod
    def init_random_character():
        character_list = Character.__subclasses__()
        character_index = random.randrange(0, len(character_list))
        return character_list[character_index](False)

    def fight(self, inventory):
        AP_low = self.ap - 5
        AP_high = self.ap + 5

        B = Character.init_random_character()
        # B = Character.init_given_character('Wizard', False)

        AP_enemy_low = B.ap - 2
        AP_enemy_high = B.ap +2
        print('You have encountered the mighty {}!'.format(B.name))
        while True:
            print('\nHero stats:')
            self.print_status()
            print('\nEnemy stats:')
            B.print_status()
            print('\nTurn of the hero:')

            action_names = self.get_action_names()
            inventory_list = get_inventory_list(inventory)
            actions = self.get_actions()
            print('Actions available:')
            sensible_user_choice = False
            while not(sensible_user_choice):
                i = 1
                for item in action_names:
                    print(str(i) + ': ', item)
                    i += 1
                l = 1
                print('Items available:')
                for item in inventory_list:
                    print(str(l+i-1) + ': ', item)
                    l += 1
                choice = input('Choose action: ')
                if is_integer(choice):
                    choice = int(choice)
                    sensible_user_choice = (choice > 0) and (choice < l+i)

                if not(sensible_user_choice):
                    print('Choice not recognized')
                else:
                    if self.is_choice_fight_action(choice, i):
                        sensible_user_choice = self.can_do_action(choice-1)
                        if not(sensible_user_choice):
                            print("Not enough MPs to perform action")
            #we have a sensible user choice
            if choice == len(action_names): #Run away
                print('You chose to run away')
                prob = 0.7
                succ = random.random() < prob
                if succ:
                    print('Successful escaping!')
                    return
                else:
                    print('Too slow! Failed to escape...')
            elif choice > len(action_names):
                useItem(inventory, choice - i +1, self, B)
            else: #attack
                curr_act = actions[choice - 1]
                print('Aiming at the opponent for the powerful {}...'.format(action_names[choice - 1]))
                succ = Character.action_succeeds(curr_act)
                if succ:
                    damage, _ = self.action_consequences(B, curr_act, AP_low, AP_high)
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
                if not(B.has_possible_action()):
                    print('Enemy cannot perform any move')
                else:
                    enemy_action, _ = B.choose_random_action()
                    print('The enemy is loading {} move...'.format(enemy_action['name']))

                    succ2 = Character.action_succeeds(enemy_action)

                    if succ2:
                        # B.mp -= enemy_action['mp_cost']
                        # damage2 = random.randrange(AP_enemy_low, AP_enemy_high) * enemy_action['dmg']
                        # A.hp -= damage2
                        damage2, _ = B.action_consequences(self, enemy_action, AP_enemy_low, AP_enemy_high)
                        print('You have been hitted for {} HP!'.format(damage2))
                    else:
                        print('You dogded the enemy attack!')
                    if (self.is_dead()):
                        print('Bad news...')
                        return


    @staticmethod
    def save_battle_as_dataframe(df):
        folder = './battles/'
        if not os.path.exists(folder):
            os.makedirs(folder)
        num_last_battle = -1
        for file in os.listdir(folder):
            if file.endswith(".csv") and file.startswith('battle'):
                file = file.strip('battle')
                file = file.strip('.csv')
                num_last_battle =  max(int(file), num_last_battle)
        new_file_name = folder+"battle" + str(num_last_battle+1) + ".csv"
        df.to_csv(new_file_name)


    @staticmethod
    def battle(char1, char2):
        stat_names = ['1_race', '2_race', '1_hps', '2_hps', '1_mps', '2_mps',
                      '1_action', '2_action', '1_damage', '2_damage']
        battle_list = []
        battle_stats = pd.DataFrame(columns=stat_names)
        turn = 0
        char1.rest(False)
        char2.rest(False)
        #reporting battle stats for char1
        turn = 0
        while True:
            assert(char1.has_possible_action())
            row = [char1.__class__.__name__, char2.__class__.__name__, char1.hp, char2.hp, char1.mp, char2.mp]
            char1_action, char1_action_num = char1.choose_random_action()
            if Character.action_succeeds(char1_action, False):
                damage2, damage1 = char1.action_consequences(char2, char1_action, char1.ap, char1.ap)
                row = row + [char1_action_num, -1, damage1, damage2]
            else:
                row = row + [char1_action_num, -1, 0, 0]
            battle_list.append(row)
            # battle_stats.loc[turn] = row
            turn += 1

            if char2.is_alive():
                assert(char2.has_possible_action())
                row = [char1.__class__.__name__, char2.__class__.__name__, char1.hp, char2.hp, char1.mp, char2.mp]
                char2_action, char2_action_num = char2.choose_random_action()
                if Character.action_succeeds(char2_action, False):
                    damage1, damage2 = char2.action_consequences(char1, char2_action, char2.ap, char2.ap)
                    row = row + [-1, char2_action_num, damage1, damage2]
                else:
                    row = row + [-1, char2_action_num, 0, 0]
            battle_list.append(row)
            # battle_stats.loc[turn] = row
            turn += 1
            assert(char1.has_possible_action() or char2.has_possible_action())
            #we are assuming at least one player can always fight. If we explode here something went wrong
            if char1.is_dead() or char2.is_dead():
                char1_won = char2.is_dead()
                char2_won = char1.is_dead()
                assert not(char1_won and char2_won)
                hp1_perc = char1.hp / char1.max_hp
                mp1_perc = char1.mp / char1.max_mp
                assert(hp1_perc == 0 or char1_won)
                battle_stats = pd.DataFrame(battle_list, columns=stat_names)
                Character.save_battle_as_dataframe(battle_stats)
                return char1_won, char2_won, turn, hp1_perc, mp1_perc


class Warrior(Character):
    def __init__(self, is_player=True):
        if (is_player):
            character_type = 'Player'
        else:
            character_type = 'NPC'
        max_hp = 10000
        max_mp = 10
        ap = 20
        actions = [{'name': 'Punch', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                   {'name': 'Kick', 'type': 'physical', 'dmg': 60, 'succ': 0.80, 'mp_cost': 0},
                   {'name': 'Chuck Norris roundhouse kick', 'type': 'physical', 'dmg': 9999, 'succ': 0.001,
                    'mp_cost': 0},
                   {'name': 'Chuck Norris roundhouse kick', 'type': 'physical', 'dmg': 9999, 'succ': 0.001,'mp_cost': 0},
                   {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]
        super().__init__(type(self).__name__, character_type, max_hp, max_mp, ap, actions)


class Wizard(Character):
    def __init__(self, is_player=True):
        if (is_player):
            character_type = 'Player'
        else:
            character_type = 'NPC'
        max_hp = 5000
        max_mp = 200
        ap = 30
        actions = [{'name': 'Fire', 'type': 'spell', 'dmg': 60, 'succ': 0.80, 'mp_cost': 10},
                   {'name': 'Thunder', 'type': 'spell', 'dmg': 80, 'succ': 0.75, 'mp_cost': 20},
                   {'name': 'Blizzard', 'type': 'spell', 'dmg': 60, 'succ': 0.80, 'mp_cost': 10},
                   {'name': 'Punch', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                   {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]

        super().__init__(type(self).__name__, character_type, max_hp, max_mp, ap, actions)


class Cleric(Character):
    def __init__(self, is_player=True):
        if (is_player):
            character_type = 'Player'
        else:
            character_type = 'NPC'
        max_hp = 50000
        max_mp = 80
        ap = 10
        actions = [{'name': 'Divine Intervention', 'type': 'spell', 'dmg': 500, 'succ': 0.30, 'mp_cost': 40},
                   {'name': 'Beads Throw', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                   {'name': 'Excommunication', 'type': 'spell', 'dmg': 60, 'succ': 0.80, 'mp_cost': 10},
                   {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]

        super().__init__(type(self).__name__, character_type, max_hp, max_mp, ap, actions)


class TelenuovoAnchorman(Character):
    def __init__(self, is_player=True):
        if (is_player):
            character_type = 'Player'
        else:
            character_type = 'NPC'
        max_hp = 50000
        max_mp = 20
        ap = 50
        actions = [{'name': 'Punio', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                   {'name': 'Sbatti Porta', 'type': 'physical', 'dmg': 50, 'succ': 0.90, 'mp_cost': 0},
                   {'name': 'Ma Che Oh', 'type': 'spell', 'dmg': 600, 'succ': 0.50, 'mp_cost': 100},
                   {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]

        super().__init__(type(self).__name__, character_type, max_hp, max_mp, ap, actions)


class Bard(Character):
    def __init__(self, is_player=True):
        if (is_player):
            character_type = 'Player'
        else:
            character_type = 'NPC'
        max_hp = 500
        max_mp = 20
        ap = 50
        actions = [{'name': 'Lute Hit', 'type': 'physical', 'dmg': 80, 'succ': 0.70, 'mp_cost': 0},
                   {'name': 'Arrow', 'type': 'physical', 'dmg': 100, 'succ': 0.60, 'mp_cost': 0},
                   {'name': 'Song Of Death', 'type': 'spell', 'dmg': 50, 'succ': 0.80, 'mp_cost': 100},
                   {'name': 'Heal yourself', 'type': 'heal', 'dmg': 0, 'succ': 1, 'mp_cost': 0}]

        super().__init__(type(self).__name__, character_type, max_hp, max_mp, ap, actions)


class Story():
    locations = ['Home', 'Castle', 'Cave']

    def __init__(self, name, player_level='novice'):
        self.name = name
        self.location = 'Home'
        self.is_alive = True
        self.player_level = player_level

    def get_player_level(self):
        return self.player_level

def display_option(sentence, options):
    i = 1
    print(sentence)
    for item in options:
        print(str(i) + ':', item)
        i += 1
    choice = input('Choose action:')
    return choice

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def update_story(story, player, inventory):
    flag_quit = False
    locations = ['Castle', 'Cave', 'Shore', 'Mountains', 'Fortress']

    while (not (player.is_dead()) and not (flag_quit)):
        if (story.location == 'Home'):
            options = ['Quit the game', 'Explore the neighborhood', 'Rest and restore health']
            user_input = get_user_input(options)
            if (user_input == 1):  # Quit
                flag_quit = True
                print('Your adventure is terminated')
                print('')
            elif (user_input == 2):  # Esplora
                probability = 0.5
                go_into_battle = random.random() < probability
                if go_into_battle:
                    print('!!! You''ve found an opponent !!!')
                    player.fight(inventory)
                    print('')
                else:
                    print('No one''s around. You''re moving to ' + random.choice(locations))
                    print('')

            elif (user_input == 3):  # Return
                player.rest()
                story.location = 'Home'
                print('')

            else:  # comando sbagliato
                print('Wrong command, retry')
                print('')

    if player.is_dead():
        print('Wasted')

def test_function_story(story):
    print(story.name)
    print(story.is_alive)

def get_user_input(options, mssg='\nWhat do you want to do?'):
    sensible_input = False
    while not (sensible_input):
        user_input = display_option(mssg, options)
        if is_integer(user_input):
            user_input = int(user_input)
            sensible_input = user_input > 0 and user_input <= len(options)
        if not(sensible_input):
            print("\nAction not recognized!")
    return user_input
