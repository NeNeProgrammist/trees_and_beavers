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


seed1 = Seed("seed1.png", 60, 60, 100, 400, 1000)

seeds = pygame.sprite.Group()

tree_list = []


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



tree1 = Tree("tree2.png", 60, 60, 600, 400, 3)
tree_list.append(tree1)

trees = pygame.sprite.Group()

trees.add(tree1)

clock = pygame.time.Clock()

runing = True

play = True

sedds_flag = False

reset_flag = False

beaver_road = random.randint(1, 5)

beaver_list = []
start_time = tm.time()
rect = pygame.Rect(30, 30, 30, 70)

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
                if x < 1550 and y < 750:
                    tree2 = Tree("tree2.png", 60, 60, x, y, 3)
                    trees.add(tree2)
                    tree_list.append(tree2)
                sedds_flag = False

    if play:

        screen.blit(backgraund, (0, 0))

        trees.draw(screen)

        seed1.reset() # коробка с семянами

        if reset_flag == True:
            seeds.draw(screen)

        beavers.draw(screen)
        beavers.update()

        pygame.draw.rect(screen, (0, 0, 255), rect, 10)

        for i in tree_list:
            i.health1()

        for tree in trees:
            tree.fire2()

        for beaver in beavers:
            beaver.fire1()

        if tm.time() - start_time >= 5:
            if beaver_road == 1:
                beaver2 = Beaver("beaver2.png", 90, 50, 1650, 100, 2, 2)
                beavers.add(beaver2)
                beaver_list.append(beaver2)


            if beaver_road == 2:
                beaver3 = Beaver("beaver2.png", 90, 50, 1650, 200, 2, 2)
                beavers.add(beaver3)
                beaver_list.append(beaver3)

            if beaver_road == 3:
                beaver4 = Beaver("beaver2.png", 90, 50, 1650, 300, 2, 2)
                beavers.add(beaver4)
                beaver_list.append(beaver4)

            if beaver_road == 4:
                beaver5 = Beaver("beaver2.png", 90, 50, 1650, 400, 2, 2)
                beavers.add(beaver5)
                beaver_list.append(beaver5)

            if beaver_road == 5:
                beaver6 = Beaver("beaver2.png", 90, 50, 1650, 500, 2, 2)
                beavers.add(beaver6)
                beaver_list.append(beaver6)




            beaver_road = random.randint(1, 5)

            start_time = tm.time()

        for i in beaver_list:
            i.health1()


        bullets_enemy.draw(screen)
        bullets_enemy.update()

        bullets_trees.draw(screen)
        bullets_trees.update()

        collies_enemys = pygame.sprite.groupcollide(trees, bullets_enemy, False, True)
        for collide_enemy in collies_enemys:
            collide_enemy.health -= 1


        collies_trees = pygame.sprite.groupcollide(beavers, bullets_trees, False, True)
        for collide_enemy in collies_enemys:
            collide_enemy.health -= 1

    else:
        screen.blit(text1, (700, 390))


    clock.tick(60)
    pygame.display.flip()
pygame.quit()