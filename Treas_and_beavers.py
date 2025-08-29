import pygame
import time as tm

screen_x = 1550
screen_y = 800

start_time = tm.time()

pygame.init()

screen = pygame.display.set_mode((screen_x, screen_y))
backgraund = pygame.transform.scale(pygame.image.load("fon1.jpg"), (screen_x, screen_y))

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
        self.rect.x -= self.speed

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
beaver1 = Beaver("beaver2.png", 90, 50, 1300, 400, 2, 2)
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
        if tree1.health > 0:          
            if tm.time() - self.start_time2 >= 1:
                if shoting == False:
                    bullet = TreesBullets("tree_bullet.png", 30, 6, self.rect.x, self.rect.y, 6, 100)
                    bullets_trees.add(bullet)
                self.start_time2 = tm.time()



tree1 = Tree("tree2.png", 60, 60, 600, 400, 3)

trees = pygame.sprite.Group()

trees.add(tree1)

clock = pygame.time.Clock()

runing = True

play = True

sedds_flag = False

reset_flag = False

tree_list = []

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

    if play:
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pass
        screen.blit(backgraund, (0, 0))

        trees.draw(screen)

        seed1.reset()


        if seed1.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            if sedds_flag == False:
                reset_flag = True
                seed2 = Seed("seeds1.png", 60, 60, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1000)
                seeds.add(seed2)
                sedds_flag = True


    
        if sedds_flag == True and seed2:
            seed2.rect.x = pygame.mouse.get_pos()[0]
            seed2.rect.y = pygame.mouse.get_pos()[1]
            if event.type == pygame.MOUSEBUTTONDOWN:
                #reset_flag = False
                #seed2.kill()
                #print(len(seeds))
                x, y = event.pos
                tree2 = Tree("tree2.png", 60, 60, x, y, 3)
                trees.add(tree2)
                tree_list.append(tree2)
                sedds_flag = False

        if reset_flag == True:
            print(len(seeds))
            print("fgh")
            seeds.draw(screen)
            seeds.update()

        beaver1.health1()

        beavers.draw(screen)
        beavers.update()
    
        tree1.health1()

        for i in tree_list:
            i.health1()

        for tree in trees:
            tree.fire2()

        for beaver in beavers:
            beaver.fire1()


        bullets_enemy.draw(screen)
        bullets_enemy.update()

        bullets_trees.draw(screen)
        bullets_trees.update()

        if beaver1.rect.x <= 0:
            play = False
            screen.blit(text1, (670, 410))
            print("You loose")

        collies_enemys = pygame.sprite.spritecollide(tree1, bullets_enemy, False)
        if collies_enemys:
            tree1.health -= 1


        collies_trees = pygame.sprite.spritecollide(beaver1, bullets_trees, False)
        if collies_trees:
            beaver1.health -= 2


    clock.tick(60)
    pygame.display.flip()
pygame.quit()