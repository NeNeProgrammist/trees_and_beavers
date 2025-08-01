import pygame
import time as tm

screen_x = 1550
screen_y = 800

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
        if self.rect.x > 1300:
            self.kill()

bullets_trees = pygame.sprite.Group()


class Beaver(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def health1(self):
        if self.health <= 0:
            self.kill()

    def fire1(self):
        bullet = Bullets("bullet.png", 30, 6, self.rect.x, self.rect.y, 4, 100)
        bullets_enemy.add(bullet)


beavers = pygame.sprite.Group()
beaver1 = Beaver("beaver1.png", 20, 20, 1300, 400, 2, 2)
beavers.add(beaver1)

class Tree(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)

    def health1(self):
        if self.health <= 0:
            self.kill()

    def fire2(self):
        bullet = TreesBullets("tree_bullet.png", 30, 6, self.rect.x, self.rect.y, 6, 100)
        bullets_trees.add(bullet)


tree1 = Tree("tree1.png", 20, 20, 100, 400, 3)

trees = pygame.sprite.Group()

trees.add(tree1)

clock = pygame.time.Clock()

runing = True

shoting = False

start_time = tm.time()
start_time2 = tm.time()

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    screen.blit(backgraund, (0, 0))

    trees.draw(screen)

    beaver1.health1()

    beavers.draw(screen)
    beavers.update()

    tree1.health1()

    if beaver1.health > 0:
        bullets_enemy.draw(screen)
        bullets_enemy.update()

    if tree1.health > 0:
        bullets_trees.draw(screen)
        bullets_trees.update()

    collies_enemys = pygame.sprite.spritecollide(tree1, bullets_enemy, True)
    if collies_enemys:
        tree1.health -= 1

    if tm.time() - start_time2 >= 1:
        if shoting == False:
            tree1.fire2()
        start_time2 = tm.time()

    collies_trees = pygame.sprite.spritecollide(beaver1, bullets_trees, True)
    if collies_trees:
        beaver1.health -= 2




    if tm.time() - start_time >= 1:
        if shoting == False:
            beaver1.fire1()
        start_time = tm.time()

    clock.tick(60)
    pygame.display.flip()
pygame.quit()