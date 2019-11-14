import random

class UsableItem:
    def __init__(self, name, item_type, hp, mp, ap):
        self.name = name
        self.item_type = item_type
        self.hp = hp
        self.mp = mp
        self.ap = ap

    # Providing info about the Item
    def show_stats(self):
        print('HP: %+4d \nMP: %+4d \nAP: %+4d' % (self.hp, self.mp, self.ap))
        print(self.name)

class Potion(UsableItem):
    def __init__(self, item_name):
        item_type = 'self'
        flag = random.choice(['Health', 'Stamina', 'Attack'])
        multiplier = (random.random()-0.5)*2
        if multiplier<=-0.5:
            item_category = 'Weak'
        elif multiplier>=0.5:
            item_category = 'Strong'
        else:
            item_category = 'Normal'

        if flag=='Health':
            hp = 500+round((multiplier*500)/10)*10
            mp=0
            ap=0
        elif flag=='Stamina':
            hp=0
            mp = 500+round((multiplier*500)/10)*10
            ap=0
        elif flag=='Attack':
            hp=0
            mp=0
            ap = 5+round(multiplier*5)

        self.name = item_category+' '+flag+' '+'Potion [' +str(hp+mp+ap) +']'
        super().__init__(self.name, item_type, hp, mp, ap)

class Poison(UsableItem):
    def __init__(self, item_name):
        item_type = 'opponent'
        flag = random.choice(['Health', 'Stamina', 'Attack'])
        multiplier = (random.random()-0.5)*2
        if multiplier<=-0.5:
            item_category = 'Weak'
        elif multiplier>=0.5:
            item_category = 'Strong'
        else:
            item_category = 'Normal'

        if flag=='Health':
            hp = -(500+round((multiplier*500)/10)*10)
            mp=0
            ap=0
        elif flag=='Stamina':
            hp=0
            mp = -(500+round((multiplier*500)/10)*10)
            ap=0
        elif flag=='Attack':
            hp=0
            mp=0
            ap = -(5+round(multiplier*5))
        self.name = item_category+' '+flag+' '+'Poison [' +str(hp+mp+ap) +']'
        super().__init__(self.name, item_type, hp, mp, ap)

def addItem(inventory, usable_item):
    inventory.append({'name': usable_item.name, 'type': usable_item.item_type, 'hp': usable_item.hp, 'mp': usable_item.mp, 'ap': usable_item.ap})
    return inventory

def get_inventory_list(inventory):
    inventory_list = []
    for i in range(0, len(inventory)):
        inventory_list.append(inventory[i]['name'])
    return inventory_list

def useItem(inventory, input, player, npc):
    current_item=inventory[input-1]
    inventory.remove(inventory[input-1])
    if (current_item['type']=='self'):
        player.hp = player.hp + current_item['hp']
        player.mp = player.mp + current_item['mp']
        player.ap = player.ap + current_item['ap']
        print('\nUsed '+ current_item['name'])
        print('HP: '+str(player.hp-current_item['hp'])+'->'+str(player.hp))
        print('MP: '+str(player.mp-current_item['mp'])+'->'+str(player.mp))
        print('AP: '+str(player.ap-current_item['ap'])+'->'+str(player.ap))

    elif (current_item['type']=='opponent'):
        npc.hp = npc.hp + current_item['hp']
        npc.mp = npc.mp + current_item['mp']
        npc.ap = npc.ap + current_item['ap']
        print('\nUsed on opponent '+ current_item['name'])
        print('HP: '+str(npc.hp-current_item['hp'])+'->'+str(npc.hp))
        print('MP: '+str(npc.mp-current_item['mp'])+'->'+str(npc.mp))
        print('AP: '+str(npc.ap-current_item['ap'])+'->'+str(npc.ap))

'''inventory = []
inventory = addItem(inventory, item01)
inventory = addItem(inventory, item02)
print(inventory[1]['hp'])'''

