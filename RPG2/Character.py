import random
from time import sleep
import numpy as np
from UsableItem import *
from story import *
from tools import *

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