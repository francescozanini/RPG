from RPG import Character
from tools import *
from UsableItem import *
from story import Story

levels = ['Novice', 'Skilled']
user_input = get_user_input(levels, mssg='\nChoose player level')
story = Story('Storia 1', user_input-1)
options = Character.get_character_list()
user_input = get_user_input(options, mssg='\nChoose character')
player = Character.init_given_character(options[user_input-1], True)
player.show_stats()
inventory = []
item01 = Potion('pozione')
item02 = Poison('veleno')
inventory = addItem(inventory, item01)
inventory = addItem(inventory, item02)
print(inventory[1]['name'])
story.update_story(player, inventory)