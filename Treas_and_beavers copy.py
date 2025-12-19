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


class Beaver(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.speed = speed
        self.start_time = tm.time()

    def update(self):
        global play
        self.rect.x -= self.speed
        if self.rect.x <= 0:
            play = False

        
    def health1(self):
        if self.health <= 0:
            self.kill()

    def fire1(self):
        if self.health > 0:
            if tm.time() - self.start_time >= 1:
                if shoting == False:
                    bullet = Bullets("bullet.png", 30, 6, self.rect.x, self.rect.y, 4, 100)
                    bullets_enemy.add(bullet)
                self.start_time = tm.time()



beavers = pygame.sprite.Group()
beaver1 = Beaver("beaver2.png", 90, 50, 1650, 400, 2, 2)
beavers.add(beaver1)

shoting = False

f1 = pygame.font.SysFont('Caladea', 36)
text1 = f1.render("You loose", True, (0, 0, 0))

class Seed(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)


seed1 = Seed("seed1.png", 60, 60, 60, 400, 1000)

tree_list = []

seeds = pygame.sprite.Group()

class Tree(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.start_time2 = tm.time()
        

    def health1(self):
        if self.health <= 0:
            self.kill()
        

    def fire2(self):
        if self.health > 0:          
            if tm.time() - self.start_time2 >= 1:
                if shoting == False:
                    bullet = TreesBullets("tree_bullet.png", 30, 6, self.rect.x, self.rect.y, 6, 100)
                    bullets_trees.add(bullet)
                self.start_time2 = tm.time()



tree1 = Tree("tree2.png", 100, 100, 600, 400, 3)
trees = pygame.sprite.Group()
#tree_list.append(tree1)

trees.add(tree1)

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

woodpecker_flag = True

woodpecker_chose = {}

class Woodpecker(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health, speed):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.health = health
        self.speed = speed
        self.wood = False


    def health1(self):
        if self.health <= 0:
            self.kill()

    def update(self):
        global play
        if self.rect.x > 500:
            self.rect.x -= self.speed
        elif self.rect.x <= 500:
            for hunnting_trees in tree_list:
                hunnting_tree_posision = random.randint(1, len(tree_list) - 1)
                woodpecker_chose[self] = tree_list[hunnting_tree_posision]
                if self in woodpecker_chose:
                    print("кординаты дятла", self.rect.x, self. rect.y)
                    if len(tree_list) > 1:
                        tree_in_dikt = woodpecker_chose[self]
                        cord_x = tree_in_dikt.rect.x
                        cord_y = tree_in_dikt.rect.y
                        if self.rect.x > cord_x:
                            print (1)
                            self.rect.x -= self.speed

                        if self.rect.x < cord_x:
                            print (2)

                            self.rect.x += self.speed

                        if self.rect.y < cord_y:
                            print (3)

                            self.rect.y += self.speed

                        if self.rect.y > cord_y:
                            print (4)

                            self.rect.y -= self.speed
                            

woodpecker1 = Woodpecker("shovel3.png", 50, 50, 1650, 257, 10, 2)
woodpeckers = pygame.sprite.Group()
woodpeckers.add(woodpecker1)

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
tree1_id = id(tree1)
tree_rect_dict = {tree1_id : 4}


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
grid_color = (255, 255, 255, 0)

for rect_in_list in rect_list:
    pygame.draw.rect(grid_syrface, grid_color, rect_in_list, 1)
    
def is_cell_ocuped(cell_rect):
    """проверяет, занятали клетка деревом"""
    for tree in trees:
        tenp_rect = pygame.Rect(cell_rect.left, cell_rect.top, 100, 100)
        if tree.rect.colliderect(tenp_rect):
            return True
    return False

def get_cell_center(cell_rect):
    """возвращает координаты центра клетки для посадки дерева"""
    return cell_rect.left, cell_rect.top

curent_seed = None
seed_cooldown = False
last_seed_time = 0


shovel2 = None


while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if seed1.rect.collidepoint(event.pos) and not seed_cooldown:
                if curent_seed is None:
                    curent_seed = Seed("tree2.png", 60, 60, event.pos[0], event.pos[1], 1000)
                    last_seed_time = tm.time()
                    seed_cooldown = True
            elif curent_seed is not None:
                for cell_rect in rect_list:
                    if cell_rect.collidepoint(event.pos):
                        if not is_cell_ocuped(cell_rect):
                            tree_x, tree_y = get_cell_center(cell_rect)
                            tree2 = Tree("tree2.png", 100, 100, tree_x, tree_y, 3)
                            trees.add(tree2)
                            tree_list.append(tree2)
                            print(f"Дерево посаженно в клетку({tree_x}, {tree_y})")
                        else:
                            print("Клетка уже занята")
                
                curent_seed = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if shovel1.rect.collidepoint(event.pos):
                if shovel2 is None:
                    shovel2 = Shovel("shovel2.png", 50, 50, event.pos[0], event.pos[1], 10000)
                    shovels.add(shovel2)
            elif shovel2 is not None:
                for cell_rect in rect_list:
                    if is_cell_ocuped(cell_rect):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            collies_showels = pygame.sprite.groupcollide(shovels, trees, True, True)
                            for collide_showel in collies_showels:
                                collide_showel.kill()
                                shovel2.kill()
                shovel2 = None


    if seed_cooldown and tm.time() - last_seed_time >= 0:
        seed_cooldown = False

    if curent_seed is not None:
        curent_seed.rect.x = pygame.mouse.get_pos()[0] - curent_seed.rect.width // 2
        curent_seed.rect.y = pygame.mouse.get_pos()[1] - curent_seed.rect.height // 2
    
    if shovel2 is not None:
        shovel2.rect.x = pygame.mouse.get_pos()[0] - shovel2.rect.width // 2
        shovel2.rect.y = pygame.mouse.get_pos()[1] - shovel2.rect.height // 2

    if play:
        #print(len(trees))
        
        screen.blit(backgraund, (0, 0))

        trees.draw(screen)
        #print(len(trees), "колл. деревьев")

        seed1.reset() # коробка с семянами

        if curent_seed is not None:
            curent_seed.reset()

        if shovel2 is not None:
            shovel2.reset()

        seeds.draw(screen)

        beavers.draw(screen)
        beavers.update()

        woodpeckers.draw(screen)
        woodpeckers.update()

        for wodpiker in woodpeckers:
            wodpiker.health1()

        shovel1.reset()

        for tree in trees:
            tree.health1()
            tree.fire2()

        for beaver in beavers:
            beaver.fire1()
            beaver.health1()


        screen.blit(grid_syrface, (0, 0))

        if tm.time() - start_time >= 5:
            if beaver_road == 1:
                beaver2 = Beaver("beaver2.png", 90, 50, 1650, 130, 2, 2)
                beavers.add(beaver2)

            if beaver_road == 2:
                beaver3 = Beaver("beaver2.png", 90, 50, 1650, 257, 2, 2)
                beavers.add(beaver3)

            if beaver_road == 3:
                beaver4 = Beaver("beaver2.png", 90, 50, 1650, 384, 2, 2)
                beavers.add(beaver4)

            if beaver_road == 4:
                beaver5 = Beaver("beaver2.png", 90, 50, 1650, 511, 2, 2)
                beavers.add(beaver5)

            if beaver_road == 5:
                beaver6 = Beaver("beaver2.png", 90, 50, 1650, 638, 2, 2)
                beavers.add(beaver6)
                
            beaver_road = random.randint(1, 5)

            start_time = tm.time()


        if tm.time() - woodpecker_spawn_time >= 10:
            if woodpecker_road == 1:
                woodpecker2 = Woodpecker("beaver2.png", 90, 50, 1650, 130, 2, 2)
                woodpeckers.add(woodpecker2)

            if woodpecker_road == 2:
                woodpecker3 = Woodpecker("beaver2.png", 90, 50, 1650, 257, 2, 2)
                woodpeckers.add(woodpecker3)

            if woodpecker_road == 3:
                woodpecker4 = Woodpecker("beaver2.png", 90, 50, 1650, 384, 2, 2)
                woodpeckers.add(woodpecker4)

            if woodpecker_road == 4:
                woodpecker5 = Woodpecker("beaver2.png", 90, 50, 1650, 511, 2, 2)
                woodpeckers.add(woodpecker5)

            if woodpecker_road == 5:
                woodpecker6 = Woodpecker("beaver2.png", 90, 50, 1650, 638, 2, 2)
                woodpeckers.add(woodpecker6)

            woodpecker_road = random.randint(1, 5)

            woodpecker_spawn_time = tm.time()


        bullets_enemy.draw(screen)
        bullets_enemy.update()

        bullets_trees.draw(screen)
        bullets_trees.update()

        collies_enemys = pygame.sprite.groupcollide(trees, bullets_enemy, False, True)
        for collide_enemy in collies_enemys:
            collide_enemy.health -= 1


        collies_trees = pygame.sprite.groupcollide(beavers, bullets_trees, False, True)
        for collide_tree in collies_trees:
            collide_tree.health -= 2

    else:
        screen.blit(text1, (700, 390))


    clock.tick(60)
    pygame.display.flip()
pygame.quit()
