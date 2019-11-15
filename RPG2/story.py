from fight import *
from tools import *
import random

class Story:
    def __init__(self, name, difficulty_level):
        self.name = name
        self.location = 'Home'
        self.is_alive = True
        self.difficulty_level = difficulty_level

    def get_diffuculty_level(self):
        return self.difficulty_level == 'novice'

    def update_story(self, player, inventory):
        flag_quit = False
        locations = ['Castle', 'Cave', 'Shore', 'Mountains', 'Fortress']

        while (not (player.is_dead()) and not (flag_quit)):
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
                    fight(player, inventory)
                    print('')
                else:
                    random_location = random.choice(locations)
                    if (random_location == self.location):
                        random_location = random.choice(locations)
                    self.location = random_location
                    print('No one''s around. You''re moving to ' + self.location)
                    print('')

            elif (user_input == 3):  # Return
                player.rest()
                self.location = 'Home'
                print('')

            else:  # comando sbagliato
                print('Wrong command, retry')
                print('')

        if player.is_dead():
            print('Wasted')