import pygame
import time as tm
import random

screen_x = 1550
screen_y = 800

start_time = tm.time()

pygame.init()

screen = pygame.display.set_mode((screen_x, screen_y), vsync = 1)
backgraund = pygame.transform.scale(pygame.image.load("fon3_4.png").convert_alpha(), (screen_x, screen_y))

clock = pygame.time.Clock()

class Parent_class(pygame.sprite.Sprite):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.health = health

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Bullets(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.speed = speed
        
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -100:
            self.kill()
bullets_enemy = pygame.sprite.Group()


class TreesBullets(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 1700:
            self.kill()

bullets_trees = pygame.sprite.Group()
tree_list = []

beaver_kill_count = 0

class Beaver(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed, health, tree_near_beaver, beaver_road_f):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.speed = speed
        self.start_time = tm.time()
        self.tree_near_beaver = tree_near_beaver
        self.beaver_road_f = beaver_road_f

    def is_beaver_cell_ocuped(self):
        self.tree_near_beaver = False
        for tree in tree_list:
            if 20 >= (self.rect.y - tree.rect.y) and (tree.rect.y - self.rect.y) <= 20:
                if 0 < (self.rect.x - tree.rect.x) <= 100:
                    if tree in tree_list:
                        self.tree_near_beaver = True
                        #print(self.tree_near_beaver)

    def is_beaver_road_ocuped(self):
        self.beaver_road_f = False
        for tree in tree_list:
            if 20 >= (self.rect.y - tree.rect.y) and (tree.rect.y - self.rect.y) <= 20:
                if tree in tree_list:
                    self.beaver_road_f = True

    def update(self):
        global play
        self.is_beaver_cell_ocuped()
        if self.tree_near_beaver == False:
            self.rect.x -= self.speed
            self.is_beaver_cell_ocuped()
        if self.rect.x <= 0:
            play = False

    def health1(self):
        global beaver_kill_count
        if self.health <= 0:
            beaver_kill_count += 1
            enemy_list.remove(self)
            self.kill()

    def fire1(self):
        self.is_beaver_road_ocuped()
        if self.health > 0:
            if self.beaver_road_f == True:
                if tm.time() - self.start_time >= 1:
                    if shoting == False:
                        bullet = Bullets("bullet.png", 30, 6, self.rect.x, self.rect.y, 4, 100)
                        bullets_enemy.add(bullet)
                    self.start_time = tm.time()

beavers = pygame.sprite.Group()

shoting = False

sun_amount = 1300

f1 = pygame.font.SysFont('Caladea', 36)
text1 = f1.render("You lose", True, (0, 0, 0))


class Seed(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health, tree_number):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.tree_number = tree_number

seed1 = Seed("seed1.png", 60, 60, 60, 400, 1000, 1)

seed_oak = Seed("oak1.png", 60, 60, 60, 330, 1000, 2)

seeds = pygame.sprite.Group()
seeds_pakages = pygame.sprite.Group()

seeds_pakages.add(seed1)
seeds_pakages.add(seed_oak)

class Tree(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health, beaver_near_tree):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.start_time2 = tm.time()
        self.amount = 100
        self.beaver_near_tree = beaver_near_tree


    def is_tree_road_ocuped(self):
        self.beaver_near_tree = False
        for beaver in enemy_list:
            if 10 >= (self.rect.y - beaver.rect.y) and (beaver.rect.y - self.rect.y) <= 10:
                if beaver in enemy_list:
                    self.beaver_near_tree = True
                    #print(self.tree_near_beaver)
   

    def health1(self):
        if self.health <= 0:
            tree_list.remove(self)
            self.kill()

    def fire2(self):
        self.is_tree_road_ocuped()
        if self.health > 0:
            if self.beaver_near_tree == True:        
                if tm.time() - self.start_time2 >= 1:
                    if shoting == False:
                        bullet = TreesBullets("tree_bullet.png", 30, 6, self.rect.x, self.rect.y, 6, 100)
                        bullets_trees.add(bullet)
                    self.start_time2 = tm.time()

    def take_hit(self):
        """Дерево получает удар от дятла"""
        self.health -= 1
        if self.health <= 0:
            # Уничтожаем дерево
            return True
        return False

#tree1 = Tree("tree1.png", 100, 100, 600, 400, 200)
trees = pygame.sprite.Group()
#tree_list.append(tree1)
#trees.add(tree1)
enemy_list = []


class Shovel(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)

shovel1 = Shovel("shovel3.png", 50, 50, 1455, 720, 10000)
shovels = pygame.sprite.Group()
shovels.add(shovel1)

f2 = pygame.font.SysFont('Caladea', 36)
text2 = f2.render(f"{sun_amount}", True, (252, 236, 0))

sun_ikon = Shovel("sun.png", 50, 50, 100, 15, 100000)



class Woodpecker(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health, speed):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.images = []
        for i in range(1, 6):
            img = pygame.image.load(f"anim_pecking/woodpicker{i}.png")
            img = pygame.transform.scale(img, (size_x, size_y))
            self.images.append(img)
        self.curent_frame = 0
        self.image = self.images[self.curent_frame]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.health = health
        self.speed = speed
        self.target_tree = None  # Текущее целевое дерево
        self.pecking = False  # Клюет ли дятел
        self.animacion_counter = 0
        self.animacion_speed = 3
        self.peck_derektion = 1
        self.original_x = pos_x
        self.original_y = pos_y

    def health1(self):
        if self.health <= 0:
            enemy_list.remove(self)
            self.kill()

    def find_nearest_tree(self):
        """Находит ближайшее дерево"""
        if not tree_list:
            return None
        
        nearest_tree = None
        min_distance = float('inf')
        
        for tree in tree_list:
            if tree.health > 0:  # Только живые деревья
                distance = ((self.rect.x - tree.rect.x) ** 2 + (self.rect.y - tree.rect.y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_tree = tree
        
        return nearest_tree
    
    def update_animasion(self):
        if self.pecking:
            self.animacion_counter += 1
            if self.animacion_counter >= self.animacion_speed:
                self.animacion_counter = 0
                self.curent_frame = (self.curent_frame + 1) % len(self.images)
                self.image = self.images[self.curent_frame]

            if self.curent_frame <= 2:
                self.rect.x = self.original_x - 5
                self.rect.y = self.original_y + 3
            else:
                self.rect.x = self.original_x
                self.rect.y = self.original_y

    def update(self):
        current_time = tm.time()
        
        # Если дятел клюет дерево
        if self.pecking and self.target_tree:
            # Проверяем, не уничтожено ли дерево
            if self.original_x == 0:
                self.original_x = self.original_x
                self.original_y = self.original_y

            self.update_animasion()

            if self.target_tree.health <= 0:
                self.pecking = False
                self.target_tree = None
                self.curent_frame = 0
                self.image = self.images[self.curent_frame]
                self.original_x = 0
                self.original_y = 0
                return
            
            if self.curent_frame == 2 and self.animacion_counter == 0:
                if self.target_tree.take_hit():
                    if self.target_tree in tree_list:
                        tree_list.remove(self.target_tree)
                    self.pecking = False
                    self.target_tree = None
                    self.curent_frame = 0
                    self.image = self.images[self.curent_frame]
                    self.original_x = 0
                    self.original_y = 0
            return
        if self.target_tree and self.target_tree.health > 0:
            target_x = self.target_tree.rect.x + self.target_tree.rect.width // 2
            target_y = self.target_tree.rect.y + self.target_tree.rect.height // 2

            dx = target_x - (self.rect.x + self.rect.width // 2)
            dy = target_y - (self.rect.y + self.rect.height // 2)
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 0:
                dx /= distance
                dy /= distance
                move_distance = min(self.speed, distance)
                self.rect.x += dx * move_distance
                self.rect.y += dy * move_distance

            if distance < 30:
                self.pecking = True
                self.original_x = self.rect.x
                self.original_y = self.rect.y
                self.animacion_counter = 0
                self.curent_frame = 0
        else:
            self.target_tree = self.find_nearest_tree()
            if not self.target_tree:
                return


woodpeckers = pygame.sprite.Group()

class Anim_pecking(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"anim_pecking/woodpicker{num}.png")
            img = pygame.transform.scale(img, (45, 75))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
          

    def update(self):
        explosion_speed = 6
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

anim_pecking_group = pygame.sprite.Group()

class Anim_exploushen(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.size_x = size_x
        self.size_y = size_y
        for num in range(1, 6):
            img = pygame.image.load(f"eplou/exp{num}.png")
            img = pygame.transform.scale(img, (size_x, size_y))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
          

    def update(self):
        explosion_speed = 6
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

anim_exp_groop = pygame.sprite.Group()

class Sun(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health, speed, sun_cord_y):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.sun_cord_y = sun_cord_y

    def update(self):
        if self.rect.y != self.sun_cord_y:
            self.rect.y += self.speed

    def click(self):
        global sun_amount, text2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.kill()
                sun_amount += 50
                f2 = pygame.font.SysFont('Caladea', 36)
                text2 = f2.render(f"{sun_amount}", True, (252, 236, 0))


sun1 = Sun("sun.png", 50, 50, random.randint(100, 1000), -100, 10, 1, random.randint(200, 700))
suns = pygame.sprite.Group()
sun1.add(suns)

class Oak(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.start_time2 = tm.time()
        self.amount = 50

    def take_hit(self):
        """Дерево получает удар от дятла"""
        self.health -= 1
        if self.health <= 0:
            # Уничтожаем дерево
            return True
        return False
    
    def health1(self):
        if self.health <= 0:
            if self in tree_list:
                tree_list.remove(self)
            self.kill()
oaks = pygame.sprite.Group()

class Bug(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed, health, tree_near_bug):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.speed = speed
        self.start_time = tm.time()
        self.tree_near_bug = tree_near_bug

    def is_bug_cell_ocuped(self):
        self.tree_near_bug = False
        for tree in tree_list:
            if 20 >= (self.rect.y - tree.rect.y) and (tree.rect.y - self.rect.y) <= 20:
                if 0 < (self.rect.x - tree.rect.x) <= 100:
                    if tree in tree_list:
                        self.tree_near_bug = True
                        #print(self.tree_near_beaver)
    def update(self):
        global play
        self.is_bug_cell_ocuped()
        if self.tree_near_bug == False:
            self.rect.x -= self.speed
            self.is_bug_cell_ocuped()
        else:
            self.exploshen()
            exp = Anim_exploushen(self.rect.centerx - 245, self.rect.centery - 245, 390, 351)
            anim_exp_groop.add(exp)
        if self.rect.x <= 0:
            play = False
        

    def health1(self):
        if self.health <= 0:
            enemy_list.remove(self)
            self.kill()

    def exploshen(self):
        for tree in tree_list:
            if (self.rect.height * 3) >= (self.rect.y - tree.rect.y) and (tree.rect.y - self.rect.y) <= (self.rect.height * 3):
                if (self.rect.x - tree.rect.x) <= 390:
                    if tree in tree_list:
                        tree_list.remove(tree)
                        tree.kill()
                        self.kill()


bugs = pygame.sprite.Group()

clock = pygame.time.Clock()

runing = True

play = True

beaver_road = random.randint(1, 5)
woodpecker_road = random.randint(1, 5)

start_time = tm.time()
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

bug_wave_count = 1

kord_list = [130, 257, 384, 511, 638]
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for seed in seeds_pakages:
                if seed.rect.collidepoint(event.pos):
                    if sun_amount >= 100:
                        curent_seed = Seed(f"tree{seed.tree_number}.png", 60, 60, event.pos[0], event.pos[1], 1000, seed.tree_number)
                        last_seed_time = tm.time()
                    break
            if curent_seed is not None:
                for cell_rect in rect_list:
                    if cell_rect.collidepoint(event.pos): #не выполняется условие
                        if not is_cell_ocuped(cell_rect):
                            tree_x, tree_y = get_cell_center(cell_rect)
                            if curent_seed.tree_number == 1:
                                if sun_amount >= 100:
                                    tree2 = Tree("tree1.png", 100, 100, tree_x, tree_y, 3, False)
                                    trees.add(tree2)
                                    tree_list.append(tree2)
                                    sun_amount -= 100
                                    print("обычное дерево")
                                else:
                                    break
                            elif curent_seed.tree_number == 2:
                                if sun_amount >= 50:
                                    oak2 = Oak("tree2.png", 100, 100, tree_x, tree_y, 100000)
                                    oaks.add(oak2)
                                    tree_list.append(oak2)
                                    sun_amount -= 50
                                    print("дуб")
                                else:
                                    break
                            f2 = pygame.font.SysFont('Caladea', 36)
                            text2 = f2.render(f"{sun_amount}", True, (252, 236, 0))
                            print(f"Дерево посаженно в клетку({tree_x}, {tree_y})")

                            curent_seed.kill()
                            curent_seed = None
                            break
                        else:
                            print("Клетка уже занята")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if shovel1.rect.collidepoint(event.pos):
                if shovel2 is None:
                    shovel2 = Shovel("shovel2.png", 50, 50, event.pos[0], event.pos[1], 100)
                    shovels.add(shovel2)
            elif shovel2 is not None:
                for cell_rect in rect_list:
                    if is_cell_ocuped(cell_rect):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            collies_showels = pygame.sprite.groupcollide(trees, shovels, True, True)
                            for collide_showel in collies_showels:
                                #if collide_showel in tree_list:
                                print(collide_showel)
                                tree_list.remove(collide_showel)
                                collide_showel.kill()
                                shovel2.kill()

                            collies_showels_oak = pygame.sprite.groupcollide(oaks, shovels, True, True)
                            for collide_showel_oak in collies_showels_oak:
                                #if collide_showel_oak in tree_list:
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

        anim_exp_groop.draw(screen)
        anim_exp_groop.update()

        if tm.time() - sun_spawn_time >= 15:
            sun2 = Sun("sun.png", 50, 50, random.randint(100, 1000), -100, 10, 1, random.randint(200, 700))
            suns.add(sun2)
            sun_spawn_time = tm.time()

        suns.draw(screen)
        for sunn in suns:
            sunn.update()
        
        for sun in suns:
            sun.click()

        if curent_seed is not None:
            curent_seed.reset()

        if shovel2 is not None:
            shovel2.reset()

        seeds.draw(screen)
        beavers.draw(screen)
        beavers.update()

        #beavers.update()
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

        for bug in bugs:
            bug.health1()
            bug.is_bug_cell_ocuped()

        bugs.draw(screen)
        bugs.update()

        oaks.draw(screen)
        for oak in oaks:
            oak.health1()

        screen.blit(grid_syrface, (0, 0))

        if tm.time() - start_time >= 5:
            if beaver_road == 1:
                beaver2 = Beaver("beaver2.png", 90, 50, 1650, 130, 2, 2, False, False)
                beavers.add(beaver2)
                enemy_list.append(beaver2)
            if beaver_road == 2:
                beaver3 = Beaver("beaver2.png", 90, 50, 1650, 257, 2, 2, False, False)
                beavers.add(beaver3)
                enemy_list.append(beaver3)
            if beaver_road == 3:
                beaver4 = Beaver("beaver2.png", 90, 50, 1650, 384, 2, 2, False, False)
                beavers.add(beaver4)
                enemy_list.append(beaver4)
            if beaver_road == 4:
                beaver5 = Beaver("beaver2.png", 90, 50, 1650, 511, 2, 2, False, False)
                beavers.add(beaver5)
                enemy_list.append(beaver5)
            if beaver_road == 5:
                beaver6 = Beaver("beaver2.png", 90, 50, 1650, 638, 2, 2, False, False)
                beavers.add(beaver6)
                enemy_list.append(beaver6)
                
            beaver_road = random.randint(1, 5)
            start_time = tm.time()

        if tm.time() - woodpecker_spawn_time >= 10:
            if woodpecker_road == 1:
                woodpecker2 = Woodpecker("woodpicker1.png", 45, 75, 1650, 130, 6, 2)
                woodpeckers.add(woodpecker2)
                enemy_list.append(woodpecker2)
            if woodpecker_road == 2:
                woodpecker3 = Woodpecker("woodpicker1.png", 45, 75, 1650, 257, 6, 2)
                woodpeckers.add(woodpecker3)
                enemy_list.append(woodpecker3)
            if woodpecker_road == 3:
                woodpecker4 = Woodpecker("woodpicker1.png", 45, 75, 1650, 384, 6, 2)
                woodpeckers.add(woodpecker4)
                enemy_list.append(woodpecker4)
            if woodpecker_road == 4:
                woodpecker5 = Woodpecker("woodpicker1.png", 45, 75, 1650, 511, 6, 2)
                woodpeckers.add(woodpecker5)
                enemy_list.append(woodpecker5)
            if woodpecker_road == 5:
                woodpecker6 = Woodpecker("woodpicker1.png", 45, 75, 1650, 638, 6, 2)
                woodpeckers.add(woodpecker6)
                enemy_list.append(woodpecker6)

            woodpecker_road = random.randint(1, 5)
            woodpecker_spawn_time = tm.time()

        if tm.time() - bug_spawn_time >= 15:
            if bug_road == 1:
                bug2 = Bug("bug.png", 45, 75, 1650, 130, 6, 12, False)
                bugs.add(bug2)
                enemy_list.append(bug2)
            if bug_road == 2:
                bug2 = Bug("bug.png", 45, 75, 1650, 257, 6, 12, False)
                bugs.add(bug2)
                enemy_list.append(bug2)
            if bug_road == 3:
                bug2 = Bug("bug.png", 45, 75, 1650, 384, 6, 12, False)
                bugs.add(bug2)
                enemy_list.append(bug2)
            if bug_road == 4:
                bug2 = Bug("bug.png", 45, 75, 1650, 511, 6, 12, False)
                bugs.add(bug2)
                enemy_list.append(bug2)
            if bug_road == 5:
                bug2 = Bug("bug.png", 45, 75, 1650, 638, 6, 12, False)
                bugs.add(bug2)
                enemy_list.append(bug2)

            bug_road = random.randint(1, 5)
            bug_spawn_time = tm.time()


        if tm.time() - wave_time >= 60:
            wave_flag = True
            wave_time = tm.time()

        if wave_flag == True:
            for i in range(beaver_wawe_count):
                if wave_beaver_road == 1:
                    beaver2 = Beaver("beaver2.png", 90, 50, random.randint(1650, 1850), 130, 2, 2, False, False)
                    beavers.add(beaver2)
                    enemy_list.append(beaver2)
                if wave_beaver_road == 2:
                    beaver3 = Beaver("beaver2.png", 90, 50, random.randint(1650, 1850), 257, 2, 2, False, False)
                    beavers.add(beaver3)
                    enemy_list.append(beaver3)
                if wave_beaver_road == 3:
                    beaver4 = Beaver("beaver2.png", 90, 50, random.randint(1650, 1850), 384, 2, 2, False, False)
                    beavers.add(beaver4)
                    enemy_list.append(beaver4)
                if wave_beaver_road == 4:
                    beaver5 = Beaver("beaver2.png", 90, 50, random.randint(1650, 1850), 511, 2, 2, False, False)
                    beavers.add(beaver5)
                    enemy_list.append(beaver5)
                if wave_beaver_road == 5:
                    beaver6 = Beaver("beaver2.png", 90, 50, random.randint(1650, 1850), 638, 2, 2, False, False)
                    beavers.add(beaver6)
                    enemy_list.append(beaver6)
                    
                wave_beaver_road = random.randint(1, 5)
            if beaver_wawe_count >= 6:
                for i in range(woodpecker_wave_count):
                    woodpecker4 = Woodpecker("woodpicker1.png", 45, 75, 1650, random.randint(130, 638), 6, 2)
                    woodpeckers.add(woodpecker4)
                    enemy_list.append(woodpecker4)
                if beaver_wawe_count % 2 == 0:
                    woodpecker_wave_count += 1

            if beaver_kill_count > 5:
                for i in range(beaver_kill_count // 10):
                    bug3 = Bug("bug.png", 45, 75, 1650, kord_list[random.randint(1, len(kord_list) - 1)], 6, 12, False)
                    bugs.add(bug3)
                    enemy_list.append(bug3)

            beaver_wawe_count += 1
            wave_flag = False


        bullets_enemy.draw(screen)
        bullets_enemy.update()
        bullets_trees.draw(screen)
        bullets_trees.update()

        collies_enemys = pygame.sprite.groupcollide(trees, bullets_enemy, False, True)
        for collide_enemy in collies_enemys:
            collide_enemy.health -= 2
            exp = Anim_exploushen(collide_enemy.rect.x, collide_enemy.rect.y, 50, 50)
            anim_exp_groop.add(exp)


        collies_trees = pygame.sprite.groupcollide(beavers, bullets_trees, False, True)
        for collide_tree in collies_trees:
            collide_tree.health -= 3
            exp = Anim_exploushen(collide_tree.rect.x, collide_tree.rect.y, 50, 50)
            anim_exp_groop.add(exp)


        collies_woodpickers = pygame.sprite.groupcollide(woodpeckers, bullets_trees, False, True)
        for collide_woodpicker in collies_woodpickers:
            collide_woodpicker.health -= 3
            exp = Anim_exploushen(collide_woodpicker.rect.x, collide_woodpicker.rect.y, 50, 50)
            anim_exp_groop.add(exp)


        collies_bugs = pygame.sprite.groupcollide(bugs, bullets_trees, False, True)
        for collide_bug in collies_bugs:
            collide_bug.health -= 2
            exp = Anim_exploushen(collide_bug.rect.x, collide_bug.rect.y, 50, 50)
            anim_exp_groop.add(exp)


        collies_oaks = pygame.sprite.groupcollide(oaks, bullets_enemy, False, True)
        for collide_oak in collies_oaks:
            collide_oak.health -= 1
            exp = Anim_exploushen(collide_oak.rect.x, collide_oak.rect.y, 50, 50)
            anim_exp_groop.add(exp)


    else:
        screen.blit(text1, (700, 390))

    clock.tick(60)
    pygame.display.flip()
pygame.quit()