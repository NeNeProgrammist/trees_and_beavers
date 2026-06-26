import pygame
import time as tm
import random
import classes
from classes import (
    Beaver as beaver_class,
    Bullets as bullets_class,
    TreesBullets as trees_bullets_class,
    Seed as seed_class,
    Tree as tree_class,
    Shovel as shovel,
    Woodpecker as woodpecker_class,
    Anim_exploushen as anim_exploushen,
    Sun as sun_class,
    Oak as oak_class,
    Bug as bug_class,
    play,
    Palm as palm_class,
    kokoses as kokoses,
    Anim_tree as anim_tree
)
import pygame_gui

screen_x = 1550
screen_y = 800

classes.kokoses = kokoses

start_time = tm.time()

pygame.init()

screen = pygame.display.set_mode((screen_x, screen_y), vsync = 1)
backgraund = pygame.transform.scale(pygame.image.load("sprites/fon3_4.png").convert_alpha(), (screen_x, screen_y))

manager = pygame_gui.UIManager((1550, 800))

clock = pygame.time.Clock()

bullets_enemy = pygame.sprite.Group()

bullets_trees = pygame.sprite.Group()
tree_list = []

beaver_kill_count = 0 #D?

beavers = pygame.sprite.Group()

shoting = False #D

sun_amount = 1300

f1 = pygame.font.SysFont('Caladea', 36)
text1 = f1.render("You lose", True, (0, 255, 0))

seed1 = seed_class("sprites/seed1.png", 60, 60, 60, 400, 1000, 1)

seed_oak = seed_class("sprites/oak1.png", 60, 60, 60, 330, 1000, 2)

seed_palm = seed_class("sprites/seed2.png", 60, 60, 60, 260, 1000, 3)


seeds = pygame.sprite.Group()
seeds_pakages = pygame.sprite.Group()

seeds_pakages.add(seed1)
seeds_pakages.add(seed_oak)
seeds_pakages.add(seed_palm)

trees = pygame.sprite.Group()
enemy_list = []

shovel1 = shovel("sprites/shovel3.png", 50, 50, 1455, 720, 10000)
shovels = pygame.sprite.Group()
shovels.add(shovel1)

f2 = pygame.font.SysFont('Caladea', 36)
text2 = f2.render(f"{sun_amount}", True, (252, 236, 0))

sun_ikon = shovel("sprites/sun1.png", 50, 50, 100, 15, 100000)

woodpeckers = pygame.sprite.Group()

anim_exp_groop = pygame.sprite.Group()

suns = pygame.sprite.Group()

oaks = pygame.sprite.Group()

palms = pygame.sprite.Group()

bugs = pygame.sprite.Group()

enemys = pygame.sprite.Group()

beaver_road = random.randint(1, 5)
woodpecker_road = random.randint(1, 5)

woodpecker_spawn_time = tm.time()

rect_list = []

cell_clones = 0
road_clones = 0

rect_x = 20
rect_y = 130

while cell_clones <= 4:
    while road_clones <= 8:
        rect2 = pygame.Rect(rect_x + 110, rect_y, 130, 127)
        rect_list.append(rect2)
        rect_x += 117
        road_clones += 1
    rect_x = 20
    road_clones = 0
    rect_y += 127
    cell_clones += 1

grid_syrface = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
grid_color = (0, 255, 0, 0)

for rect_in_list in rect_list:
    pygame.draw.rect(grid_syrface, grid_color, rect_in_list, 1)
    
def is_cell_ocuped(cell_rect):
    """проверяет, занята ли клетка деревом"""
    for tree in tree_list:
        temp_rect = pygame.Rect(cell_rect.left, cell_rect.top, 100, 100)
        if tree.rect.colliderect(temp_rect):
            return True
    return False

def get_cell_center(cell_rect):
    """возвращает координаты центра клетки для посадки дерева"""
    return cell_rect.left, cell_rect.top

button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 275), (-1, -1)),
    text="Menu",
    manager=manager
)

def create_main_buttons():
    global button, button2
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 275), (-1, -1)),
        text="Menu",
        manager=manager
    )

def destroy_main_buttons():
    global button
    button.kill()
    button = None

curent_seed = None
last_seed_time = tm.time()
shovel2 = None
wave_flag = False
wave_beaver_road = random.randint(1, 5)
wave_woodpecker_road = random.randint(1, 5)
sun_spawn_time = tm.time()
wave_time = tm.time()
beaver_wawe_count = 5
woodpecker_wave_count = 1
bug_spawn_time = tm.time()
bug_road = random.randint(1, 5)
kord_list = [130, 257, 384, 511, 638]
menu = True
menu_buttons = []

# Синхронизация глобальных переменных с модулем classes
classes.tree_list = tree_list
classes.enemy_list = enemy_list
classes.shoting = shoting
classes.bullets_enemy = bullets_enemy
classes.bullets_trees = bullets_trees
classes.anim_exp_groop = anim_exp_groop
classes.screen = screen
classes.play = play
classes.beaver_kill_count = beaver_kill_count

'''def update_dropdown():
    global dropdown
    if dropdown is not None:
        dropdown.kill()
        dropdown = None
    if rect_flag:
        options = [
            f"kooficient: {kooficient}",
            f"clicks: {clicks}",
            f"norma: {norma}"
        ]
        dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=options,
            starting_option=options[0],
            relative_rect=pygame.Rect((320, 390), (150, 50)),
            manager=manager
        )
        menu_buttons.append(dropdown)

def on_values_changed():
    update_dropdown()
'''
runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if not rect_flag:
                    rect_flag = True
                    destroy_main_buttons()
                    for btn in menu_buttons:
                        btn.kill()
                    menu_buttons.clear()

                    btn3 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((320, 205), (150, 50)),
                        text="New game",
                        manager=manager
                    )
                    btn5 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((320, 270), (150, 50)),
                        text="Close game",
                        manager=manager
                    )
                    btn4 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((320, 335), (150, 50)),
                        text="Titles",
                        manager=manager
                    )
                    menu_buttons.extend([btn3, btn5, btn4])
                    #update_dropdown()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if btn3 is not None and event.ui_element == btn3:
                play = True
                #on_values_changed()
            
            elif event.ui_element in menu_buttons:
                if event.ui_element.text == "Закрыть кликер":
                    running = False

                elif event.ui_element.text == "Закрыть меню":
                    rect_flag = False
                    for btn in menu_buttons:
                        btn.kill()
                    menu_buttons.clear()
                    if dropdown is not None:
                        dropdown.kill()
                        dropdown = None
                    create_main_buttons()
                    
        if event.type == pygame.QUIT:
            runing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                play = True
                enemy_list.clear()
                tree_list.clear()
                for tree_kill in trees:
                    tree_kill.kill()
                for oak_kill in oaks:
                    oak_kill.kill()
                for beaver_kill in beavers:
                    beaver_kill.kill()
                for woodpicker_kill in woodpeckers:
                    woodpicker_kill.kill()
                for bug_kill in bugs:
                    bug_kill.kill()
                for bullet_kill in bullets_enemy:
                    bullet_kill.kill()
                for bullet_kill2 in bullets_trees:
                    bullet_kill2.kill()
                for sun_kill in suns:
                    sun_kill.kill()
                curent_seed = None
                last_seed_time = tm.time()
                shovel2 = None
                wave_flag = False
                wave_beaver_road = random.randint(1, 5)
                wave_woodpecker_road = random.randint(1, 5)
                sun_spawn_time = tm.time()
                wave_time = tm.time()
                beaver_wawe_count = 5
                woodpecker_wave_count = 1
                bug_spawn_time = tm.time()
                bug_road = random.randint(1, 5)
                beaver_road = random.randint(1, 5)
                woodpecker_road = random.randint(1, 5)
                sun_amount = 1300
                text2 = f2.render(f"{sun_amount}", True, (252, 236, 0))


        if event.type == pygame.MOUSEBUTTONDOWN:
            for seed in seeds_pakages:
                if seed.rect.collidepoint(event.pos):
                    if sun_amount >= 100:
                        curent_seed = seed_class(f"sprites/tree{seed.tree_number}.png", 60, 60, event.pos[0], event.pos[1], 1000, seed.tree_number)
                        last_seed_time = tm.time()
                    break
            if curent_seed is not None:
                for cell_rect in rect_list:
                    if cell_rect.collidepoint(event.pos): #не выполняется условие
                        if not is_cell_ocuped(cell_rect):
                            tree_x, tree_y = get_cell_center(cell_rect)
                            if curent_seed.tree_number == 1:
                                if sun_amount >= 100:
                                    tree2 = tree_class("sprites/tree1.png", 100, 100, tree_x, tree_y, 3, False)
                                    trees.add(tree2)
                                    tree_list.append(tree2)
                                    sun_amount -= 100
                                else:
                                    break
                            elif curent_seed.tree_number == 2:
                                if sun_amount >= 50:
                                    oak2 = oak_class("sprites/tree2.png", 100, 100, tree_x, tree_y, 100000)
                                    oaks.add(oak2)
                                    tree_list.append(oak2)
                                    sun_amount -= 50
                                else:
                                    break
                            elif curent_seed.tree_number == 3:
                                if sun_amount >= 150:
                                    palm1 = palm_class("sprites/palm.png", 80, 100, tree_x, tree_y, 1)
                                    palms.add(palm1)
                                    sun_amount -= 150
                                else:
                                    break
                            f2 = pygame.font.SysFont('Caladea', 36)
                            text2 = f2.render(f"{sun_amount}", True, (252, 236, 0))

                            curent_seed.kill()
                            curent_seed = None
                            break
                        else:
                            print("Клетка уже занята")

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Обработка сбора солнца
            for sun in suns:
                if sun.rect.collidepoint(event.pos):
                    sun.kill()
                    sun_amount += 50
                    text2 = f2.render(f"{sun_amount}", True, (252, 236, 0))
                    break
            if shovel1.rect.collidepoint(event.pos):
                if shovel2 is None:
                    shovel2 = shovel("sprites/shovel2.png", 50, 50, event.pos[0], event.pos[1], 100)
                    shovels.add(shovel2)
            elif shovel2 is not None:
                for cell_rect in rect_list:
                    if is_cell_ocuped(cell_rect):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            collies_showels = pygame.sprite.groupcollide(trees, shovels, True, True)
                            for collide_showel in collies_showels:
                                print(collide_showel)
                                tree_list.remove(collide_showel)
                                collide_showel.kill()
                                shovel2.kill()

                            collies_showels_oak = pygame.sprite.groupcollide(oaks, shovels, True, True)
                            for collide_showel_oak in collies_showels_oak:
                                tree_list.remove(collide_showel_oak)
                                collide_showel_oak.kill()
                                shovel2.kill()
                shovel2 = None

    if curent_seed is not None:
        curent_seed.rect.x = pygame.mouse.get_pos()[0] - curent_seed.rect.width // 2
        curent_seed.rect.y = pygame.mouse.get_pos()[1] - curent_seed.rect.height // 2
    
    if shovel2 is not None:
        shovel2.rect.x = pygame.mouse.get_pos()[0] - shovel2.rect.width // 2
        shovel2.rect.y = pygame.mouse.get_pos()[1] - shovel2.rect.height // 2

    if play:
        screen.blit(backgraund, (0, 0))

        trees.draw(screen)

        seeds_pakages.draw(screen)

        screen.blit(text2, (15, 15))

        sun_ikon.reset()

        oaks.draw(screen)
        for oak in oaks:
            oak.health1()

        anim_exp_groop.draw(screen)
        anim_exp_groop.update()

        palms.draw(screen)
        for palm in palms:
            palm.update()

        if tm.time() - sun_spawn_time >= 15:
            sun2 = sun_class("sprites/sun1.png", 50, 50, random.randint(100, 1000), -100, 10, 1, random.randint(200, 700))
            suns.add(sun2)
            sun_spawn_time = tm.time()

        suns.draw(screen)
        for sunn in suns:
            sunn.update()
        '''
        for sun in suns: #D?
            sun.click()'''

        if curent_seed is not None:
            curent_seed.reset()

        if shovel2 is not None:
            shovel2.reset()

        seeds.draw(screen)
        beavers.draw(screen)
        beavers.update()

        kokoses.draw(screen)
        kokoses.update()
        '''for pal in palms:
            print(len(kokoses), "len", pal.enemies_in_range, "enemues")'''

        woodpeckers.draw(screen)
        woodpeckers.update()  # Обновляем дятлов каждый кадр

        for woodpecker in woodpeckers:
            woodpecker.health1()

        shovel1.reset()

        for tree in trees:
            tree.health1()
            tree.fire2()

        for beaver in beavers:
            beaver.fire1()
            beaver.health1()
            beaver.is_beaver_cell_ocuped()
            if beaver.rect.x <= 0:
                play = False


        for bug in bugs:
            bug.health1()
            bug.is_bug_cell_ocuped()

        bugs.draw(screen)
        bugs.update()

        screen.blit(grid_syrface, (0, 0))

        if tm.time() - start_time >= 5:
            if beaver_road == 1:
                beaver2 = beaver_class("sprites/beaver2.png", 90, 50, 1050, 130, 2, 2, False, False)
                beavers.add(beaver2)
                enemy_list.append(beaver2)
                enemys.add(beaver2)
            if beaver_road == 2:
                beaver3 = beaver_class("sprites/beaver2.png", 90, 50, 1050, 257, 2, 2, False, False)
                beavers.add(beaver3)
                enemy_list.append(beaver3)
                enemys.add(beaver3)
            if beaver_road == 3:
                beaver4 = beaver_class("sprites/beaver2.png", 90, 50, 1050, 384, 2, 2, False, False)
                beavers.add(beaver4)
                enemy_list.append(beaver4)
                enemys.add(beaver4)
            if beaver_road == 4:
                beaver5 = beaver_class("sprites/beaver2.png", 90, 50, 1050, 511, 2, 2, False, False)
                beavers.add(beaver5)
                enemy_list.append(beaver5)
                enemys.add(beaver5)
            if beaver_road == 5:
                beaver6 = beaver_class("sprites/beaver2.png", 90, 50, 1050, 638, 2, 2, False, False)
                beavers.add(beaver6)
                enemy_list.append(beaver6)
                enemys.add(beaver6)
                
            beaver_road = random.randint(1, 5)
            start_time = tm.time()

        if tm.time() - woodpecker_spawn_time >= 10:
            if woodpecker_road == 1:
                woodpecker2 = woodpecker_class("sprites/woodpicker1.png", 45, 75, 1650, 130, 6, 2)
                woodpeckers.add(woodpecker2)
                enemy_list.append(woodpecker2)
                enemys.add(woodpecker2)
            if woodpecker_road == 2:
                woodpecker3 = woodpecker_class("sprites/woodpicker1.png", 45, 75, 1650, 257, 6, 2)
                woodpeckers.add(woodpecker3)
                enemy_list.append(woodpecker3)
                enemys.add(woodpecker3)
            if woodpecker_road == 3:
                woodpecker4 = woodpecker_class("sprites/woodpicker1.png", 45, 75, 1650, 384, 6, 2)
                woodpeckers.add(woodpecker4)
                enemy_list.append(woodpecker4)
                enemys.add(woodpecker4)
            if woodpecker_road == 4:
                woodpecker5 = woodpecker_class("sprites/woodpicker1.png", 45, 75, 1650, 511, 6, 2)
                woodpeckers.add(woodpecker5)
                enemy_list.append(woodpecker5)
                enemys.add(woodpecker5)
            if woodpecker_road == 5:
                woodpecker6 = woodpecker_class("sprites/woodpicker1.png", 45, 75, 1650, 638, 6, 2)
                woodpeckers.add(woodpecker6)
                enemy_list.append(woodpecker6)
                enemys.add(woodpecker6)
            woodpecker_road = random.randint(1, 5)
            woodpecker_spawn_time = tm.time()

        if tm.time() - bug_spawn_time >= 15:
            if bug_road == 1:
                bug2 = bug_class("sprites/bug1.png", 45, 75, 1650, 130, 6, 12, False)
                bugs.add(bug2)
                enemys.add(bug2)
                enemy_list.append(bug2)
            if bug_road == 2:
                bug2 = bug_class("sprites/bug1.png", 45, 75, 1650, 257, 6, 12, False)
                bugs.add(bug2)
                enemy_list.append(bug2)
                enemys.add(bug2)
            if bug_road == 3:
                bug2 = bug_class("sprites/bug1.png", 45, 75, 1650, 384, 6, 12, False)
                bugs.add(bug2)
                enemy_list.append(bug2)
                enemys.add(bug2)
            if bug_road == 4:
                bug2 = bug_class("sprites/bug1.png", 45, 75, 1650, 511, 6, 12, False)
                bugs.add(bug2)
                enemy_list.append(bug2)
                enemys.add(bug2)
            if bug_road == 5:
                bug2 = bug_class("sprites/bug1.png", 45, 75, 1650, 638, 6, 12, False)
                bugs.add(bug2)
                enemys.add(bug2)
                enemy_list.append(bug2)

            bug_road = random.randint(1, 5)
            bug_spawn_time = tm.time()

        if tm.time() - wave_time >= 60:
            wave_flag = True
            wave_time = tm.time()

        if wave_flag == True:
            for i in range(beaver_wawe_count):
                if wave_beaver_road == 1:
                    beaver2 = beaver_class("sprites/beaver2.png", 90, 50, random.randint(1650, 1850), 130, 2, 2, False, False)
                    beavers.add(beaver2)
                    enemy_list.append(beaver2)
                    enemys.add(beaver2)
                if wave_beaver_road == 2:
                    beaver3 = beaver_class("sprites/beaver2.png", 90, 50, random.randint(1650, 1850), 257, 2, 2, False, False)
                    beavers.add(beaver3)
                    enemy_list.append(beaver3)
                    enemys.add(beaver3)
                if wave_beaver_road == 3:
                    beaver4 = beaver_class("sprites/beaver2.png", 90, 50, random.randint(1650, 1850), 384, 2, 2, False, False)
                    beavers.add(beaver4)
                    enemy_list.append(beaver4)
                    enemys.add(beaver4)
                if wave_beaver_road == 4:
                    beaver5 = beaver_class("sprites/beaver2.png", 90, 50, random.randint(1650, 1850), 511, 2, 2, False, False)
                    beavers.add(beaver5)
                    enemy_list.append(beaver5)
                    enemys.add(beaver5)
                if wave_beaver_road == 5:
                    beaver6 = beaver_class("sprites/beaver2.png", 90, 50, random.randint(1650, 1850), 638, 2, 2, False, False)
                    beavers.add(beaver6)
                    enemy_list.append(beaver6)
                    enemys.add(beaver6)
                    
                wave_beaver_road = random.randint(1, 5)
            if beaver_wawe_count >= 6:
                for i in range(woodpecker_wave_count):
                    woodpecker4 = woodpecker_class("sprites/woodpicker1.png", 45, 75, 1650, random.randint(130, 638), 6, 2)
                    woodpeckers.add(woodpecker4)
                    enemy_list.append(woodpecker4)
                    enemys.add(woodpecker4)
                if beaver_wawe_count % 2 == 0:
                    woodpecker_wave_count += 1

            if beaver_kill_count > 5:
                for i in range(beaver_kill_count // 10):
                    bug3 = bug_class("sprites/bug1.png", 45, 75, 1650, kord_list[random.randint(1, len(kord_list) - 1)], 6, 12, False)
                    bugs.add(bug3)
                    enemy_list.append(bug3)
                    enemys.add(bug3)

            beaver_wawe_count += 1
            wave_flag = False

        bullets_enemy.draw(screen)
        bullets_enemy.update()
        bullets_trees.draw(screen)
        bullets_trees.update()

        collies_enemys = pygame.sprite.groupcollide(trees, bullets_enemy, False, True)
        for collide_enemy in collies_enemys:
            collide_enemy.health -= 2
            exp = anim_tree(collide_enemy.rect.x + random.randint(20, 40), collide_enemy.rect.y + random.randint(10, 30), 50, 50)
            anim_exp_groop.add(exp)

        collies_trees = pygame.sprite.groupcollide(beavers, bullets_trees, False, True)
        for collide_tree in collies_trees:
            collide_tree.health -= 3
            exp = anim_exploushen(collide_tree.rect.x, collide_tree.rect.y, 50, 50)
            anim_exp_groop.add(exp)

        collies_woodpickers = pygame.sprite.groupcollide(woodpeckers, bullets_trees, False, True)
        for collide_woodpicker in collies_woodpickers:
            collide_woodpicker.health -= 3
            exp = anim_exploushen(collide_woodpicker.rect.x, collide_woodpicker.rect.y, 50, 50)
            anim_exp_groop.add(exp)

        collies_bugs = pygame.sprite.groupcollide(bugs, bullets_trees, False, True)
        for collide_bug in collies_bugs:
            collide_bug.health -= 2
            exp = anim_exploushen(collide_bug.rect.x + 20, collide_bug.rect.y, 50, 50)
            anim_exp_groop.add(exp)

        collies_oaks = pygame.sprite.groupcollide(oaks, bullets_enemy, False, True)
        for collide_oak in collies_oaks:
            collide_oak.health -= 1
            exp = anim_tree(collide_oak.rect.x + random.randint(20, 40), collide_oak.rect.y + random.randint(10, 30), 50, 50)
            anim_exp_groop.add(exp)

        collies_kokoses = pygame.sprite.groupcollide(enemys, kokoses, True, True)
        for collide_kokos in collies_kokoses:
            collide_kokos.kill()
            enemy_list.remove(collide_kokos)
            if collide_kokos in beavers:
                beavers.remove(collide_kokos)   
            elif collide_kokos in woodpeckers:
                woodpeckers.remove(collide_kokos)
            elif collide_kokos in bugs:
                bugs.remove(collide_kokos)


    else:
        screen.blit(text1, (700, 390))

    clock.tick(60)
    pygame.display.flip()
pygame.quit()