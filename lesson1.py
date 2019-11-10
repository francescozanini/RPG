from RPG import *

story = Story('Storia 1')
options = Character.get_character_list()
user_input = get_user_input(options, mssg='\nChoose character')
player = Character.init_given_character(options[user_input], True)
player.show_stats()
update_story(story, player)