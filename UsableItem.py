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
            hp = 50+round((multiplier*50)/10)*10
            mp=0
            ap=0
        elif flag=='Stamina':
            hp=0
            mp = 50+round((multiplier*50)/10)*10
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
            hp = -(50+round((multiplier*50)/10)*10)
            mp=0
            ap=0
        elif flag=='Stamina':
            hp=0
            mp = -(50+round((multiplier*50)/10)*10)
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
        hp_bk = player.hp
        mp_bk = player.mp
        ap_bk = player.ap
        player.hp = player.hp + current_item['hp']
        if player.hp > player.max_hp:
            player.hp = player.max_hp
        player.mp = player.mp + current_item['mp']
        if player.mp > player.max_mp:
            player.mp = player.max_mp
        player.ap = player.ap + current_item['ap']
        print('\nUsed '+ current_item['name'])
        print('HP: '+str(hp_bk)+'->'+str(player.hp))
        print('MP: '+str(mp_bk)+'->'+str(player.mp))
        print('AP: '+str(ap_bk)+'->'+str(player.ap))

    elif (current_item['type']=='opponent'):
        hp_bk = npc.hp
        mp_bk = npc.mp
        ap_bk = npc.ap
        npc.hp = npc.hp + current_item['hp']
        npc.mp = npc.mp + current_item['mp']
        npc.ap = npc.ap + current_item['ap']
        if npc.ap < 0:
            npc.ap = 0
        if npc.ap < 0:
            npc.ap = 0
        if npc.ap < 0:
            npc.ap = 0
        print('\nUsed on opponent '+ current_item['name'])
        print('HP: '+str(hp_bk)+'->'+str(npc.hp))
        print('MP: '+str(mp_bk)+'->'+str(npc.mp))
        print('AP: '+str(ap_bk)+'->'+str(npc.ap))

'''inventory = []
inventory = addItem(inventory, item01)
inventory = addItem(inventory, item02)
print(inventory[1]['hp'])'''

