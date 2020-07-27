from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random
# Create Black magic
fire = Spell("Fire",10,100,"black")
thunder = Spell("Thunder",10,100,"black")
blizzard = Spell("Blizzard",10,100,"black")
meteor = Spell("Mateor",20,200,"black")
quake = Spell("Cure",14,140,"black")


# Create White Magic
cure = Spell("Cure",12,120,"white")
cura = Spell("Cura",18,200,"white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega-Elixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire,  meteor, cure]

player_items = [{"item":potion, "quantity":15},
                {"item":hipotion, "quantity":5},
                {"item":superpotion, "quantity":2},
                {"item":elixer, "quantity":5},
                {"item":hielixer, "quantity":1},
                {"item":grenade, "quantity":4}]
# Instantiate People 
player1 = Person("Valos:",3260,132,60,34,player_spells,player_items)
player2 = Person("Nick :",4160,188,60,34,player_spells,player_items)
player3 = Person("Robot:",3089,174,60,34,player_spells,player_items)

enemy3 =  Person("Imp  ",1200,221,100,25,enemy_spells,player_items)
enemy2 =  Person("Magus",1250,221,1000,25,enemy_spells,player_items)
enemy1 =  Person("Imp  ",1200,221,100,25,enemy_spells,player_items)


players = [player1,player2,player3]
enemies = [enemy1,enemy2,enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACK" + bcolors.ENDC)

while running:
    print("============================================")
    print("\n\n")
    print(bcolors.BOLD +"NAME:               HP:                                       MP:"+bcolors.ENDC)
    for player in players:
        player.get_stats()
    
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()  

    for player in players:   
        if player.get_hp() != 0:
            print("\n")
            player.choose_action()
            print("\n")
            choice = input("Choose action:")
            index = int(choice) - 1
            print("\n")
            print("You chose: ", player.actions[index])
            print("\n")


            if index == 0:
                dmg = player.generate_damage()
                enemy = player.choose_terget(enemies)
                enemies[enemy].take_damage(dmg)
                print(player.name+" attacked " +enemies[enemy].name+" for ", dmg, "points of damage.")
                if  enemies[enemy].get_hp() == 0:
                        print(bcolors.BOLD + bcolors.FAIL +  enemies[enemy].name+ " has died." + bcolors.ENDC) 
                        enemies.remove(enemies[enemy])
            
            elif index == 1:
                player.choose_magic()
                print("\n")
                magic_choice = int(input("Choose magic:")) - 1

                if magic_choice == -1:
                    continue


                
                spell = player.magic[magic_choice]
                magic_dmg = spell.generate_damage()
                cost = spell.cost
                
                current_mp = player.get_mp()

                if spell.cost > current_mp :
                    print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                    continue   
                player.reduce_mp(spell.cost)
                if spell.type == "white":
                    player.heal(magic_dmg)    
                    print(bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP." + bcolors.ENDC)                     
                
                elif spell.type == "black":
                    enemy = player.choose_terget(enemies)
                    enemies[enemy].take_damage(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage to "+ enemies[enemy].name + bcolors.ENDC)
                    if  enemies[enemy].get_hp() == 0:
                        print(bcolors.BOLD + bcolors.FAIL +  enemies[enemy].name+ " has died." + bcolors.ENDC)
                        enemies.remove(enemies[enemy])
                
            elif index == 2:
                player.choose_item()
                print("\n")
                item_choice = int(input("Choose item:")) - 1
                if item_choice == -1:
                    continue
                item = player.items[item_choice]["item"]
                

                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL +"\nNo More " + item.name  + bcolors.ENDC) 
                    continue

                player.items[item_choice]["quantity"] -= 1

                if item.type == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKBLUE + "\n" + item.name + "heals for", str(item.prop), "HP." + bcolors.ENDC)                     
                
                elif item.type == "elixer":
                    if item.name == "Mega-Elixer":
                        for p in players:
                            p.hp = p.maxhp
                            p.mp = p.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                    
                    print(bcolors.OKBLUE + "\n" + item.name + "fully restores HP/MP" + bcolors.ENDC)  
                
                elif item.type == "attack":
                    enemy = player.choose_terget(enemies)
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.FAIL + "\n" + item.name + "delas", str(item.prop), "points of damage to "+ enemies[enemy].name + bcolors.ENDC)
                    if  enemies[enemy].get_hp() == 0:
                        print(bcolors.BOLD + bcolors.FAIL +  enemies[enemy].name+ " has died." + bcolors.ENDC) 
                        enemies.remove(enemies[enemy])
        
        
        

    for enemy in enemies:
        enemy_choice = random.randrange(0,2)
        if enemy_choice == 0:
                    
            target = random.randrange(0,len(players))
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.OKBLUE + "\n" + enemy.name+" attacks " + players[target].name +"for", enemy_dmg)
            if players[target].get_hp() == 0:
                print(bcolors.BOLD + bcolors.FAIL + players[target].name +" has died." + bcolors.ENDC)
                players.remove(players[target])


        if enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()  
            print(bcolors.OKBLUE + "\n" + enemy.name + " choose "+spell.name+" dmg is "+str(magic_dmg)+ bcolors.ENDC)
            enemy.reduce_mp(spell.cost)
            if spell.type == "white":
                enemy.heal(magic_dmg)    
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for ", str(magic_dmg), " HP." + bcolors.ENDC)                     
                
            elif spell.type == "black":
                target = random.randrange(0,len(players))
                enemy_dmg = enemy.generate_damage()
                players[target].take_damage(enemy_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name +" attacks " + players[target].name + " with " + spell.name + "deals", str(magic_dmg), "points of damage." + bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print(bcolors.BOLD + bcolors.FAIL + players[target].name +" has died." + bcolors.ENDC)
                    players.remove(players[target])

        # if enemy_choice == 2:
        #     enemy.choose_item()
        #         print("\n")
        #         item_choice = int(input("Choose item:")) - 1
        #         if item_choice == -1:
        #             continue
        #         item = player.items[item_choice]["item"]
                

        #         if player.items[item_choice]["quantity"] == 0:
        #             print(bcolors.FAIL +"\nNo More " + item.name  + bcolors.ENDC) 
        #             continue

        #         player.items[item_choice]["quantity"] -= 1

        #         if item.type == "potion":
        #             enemy.heal(item.prop)
        #             print(bcolors.OKBLUE + "\n" + item.name + "heals for", str(item.prop), "HP." + bcolors.ENDC)                     
                
        #         elif item.type == "elixer":
        #             if item.name == "Mega-Elixer":
        #                 for e in enemies:
        #                     e.hp = e.maxhp
        #                     e.mp = e.maxmp
        #             else:
        #                 enemy.hp = enemy.maxhp
        #                 enemy.mp = enemy.maxmp
                    
        #             print(bcolors.OKBLUE + "\n" + item.name + "fully restores HP/MP" + bcolors.ENDC)  
                
        #         elif item.type == "attack":

        #             target = random.randrange(0,len(players))
        #             players[target].take_damage(item.prop)
        #             print(bcolors.OKBLUE + "\n" + enemy.name +" attacks " + players[target].name + " with " + item.name + "deals", str(item.prop), "points of damage." + bcolors.ENDC)
        #             if players[target].get_hp() == 0:
        #                 print(bcolors.BOLD + bcolors.FAIL + players[target].name +" has died." + bcolors.ENDC)
                        # players.remove(players[target])

               

    print("=================================")

    defeated_enemies = 0
    defeated_players = 0

    # for enemy in enemies:
    #     if enemy.get_hp() == 0:
    #         defeated_enemies += 1
    active_players = len(players)
    active_enemies = len(enemies)

    # for player in players:
    #     if player.get_hp() == 0:
    #         defeated_players += 1        

    if active_enemies == 1:
            print(bcolors.BOLD+bcolors.OKGREEN + "You win" + bcolors.ENDC)
            running = False        

    elif active_players == 1:
        print(bcolors.BOLD+bcolors.FAIL + "You lost: Your enemies has defeated you!" + bcolors.ENDC)
        running = False
        



print("============================================")
print("\n\n")
print(bcolors.BOLD +"NAME:               HP:                                       MP:"+bcolors.ENDC)
for player in players:
    player.get_stats()
    
print("\n")
for enemy in enemies:
    enemy.get_enemy_stats()  