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

trees.add(tree1)

clock = pygame.time.Clock()

runing = True

play = True

sedds_flag = False

reset_flag = False

beaver_road = random.randint(1, 5)

start_time = tm.time()


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
    



while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

        if event.type == pygame.MOUSEBUTTONDOWN and seed1.rect.collidepoint(pygame.mouse.get_pos()):
            if tm.time() - start_time >= 2:
                if sedds_flag == False:
                    reset_flag = True
                    start_time = tm.time()
                    if len(seeds) > 0:
                        seed2.kill()
                    seed2 = Seed("seeds1.png", 60, 60, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1000)
                    seeds.add(seed2)
                    sedds_flag = True

        if sedds_flag == True:
            seed2.rect.x = pygame.mouse.get_pos()[0]
            seed2.rect.y = pygame.mouse.get_pos()[1]
            if event.type == pygame.MOUSEBUTTONUP:
                reset_flag = False
                x, y = event.pos
                for cell_rect in rect_list:
                    if cell_rect.collidepoint(pygame.mouse.get_pos()):
                        for tree_rect in trees:
                            if seed2.rect.bottom - cell_rect.bottom <= 65:
                                tree2 = Tree("tree2.png", 100, 100, cell_rect.left, cell_rect.top, 3)
                                if (not tree_rect.rect.colliderect(tree2.rect)) and (not tree2 in trees):
                                    trees.add(tree2)
                sedds_flag = False

    if play:
        #print(len(trees))


        screen.blit(backgraund, (0, 0))

        trees.draw(screen)
        print(len(trees), "колл. деревьев")

        seed1.reset() # коробка с семянами

        if reset_flag == True:
            seeds.draw(screen)

        beavers.draw(screen)
        beavers.update()

        for tree in trees:
            tree.health1()
            tree.fire2()

        for beaver in beavers:
            beaver.fire1()
            beaver.health1()


        for rect_in_list in rect_list:
            pygame.draw.rect(screen, (0, 0, 255), rect_in_list, 10)


        if tm.time() - start_time >= 5:
            if beaver_road == 1:
                beaver2 = Beaver("beaver2.png", 90, 50, 1650, 100, 2, 2)
                beavers.add(beaver2)


            if beaver_road == 2:
                beaver3 = Beaver("beaver2.png", 90, 50, 1650, 200, 2, 2)
                beavers.add(beaver3)

            if beaver_road == 3:
                beaver4 = Beaver("beaver2.png", 90, 50, 1650, 300, 2, 2)
                beavers.add(beaver4)

            if beaver_road == 4:
                beaver5 = Beaver("beaver2.png", 90, 50, 1650, 400, 2, 2)
                beavers.add(beaver5)

            if beaver_road == 5:
                beaver6 = Beaver("beaver2.png", 90, 50, 1650, 500, 2, 2)
                beavers.add(beaver6)




            beaver_road = random.randint(1, 5)

            start_time = tm.time()



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