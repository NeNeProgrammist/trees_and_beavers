import pygame
import time as tm

screen_x = 1550
screen_y = 800

pygame.init()

screen = pygame.display.set_mode((screen_x, screen_y))
backgraund = pygame.transform.scale(pygame.image.load("fon1.jpg"), (screen_x, screen_y))

clock = pygame.time.Clock()

class Parent_class(pygame.sprite.Sprite):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Bullets(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y)
        self.speed = speed
        
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -100:
            self.kill()


bullets = pygame.sprite.Group()
bullets_enemy = pygame.sprite.Group()

class Beaver(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed


    def fire1(self):
        bullet = Bullets("bullet.png", 30, 6, self.rect.x, self.rect.y, 4)
        bullets_enemy.add(bullet)



beaver1 = Beaver("beaver1.png", 20, 20, 1300, 710, 2)

class Tree(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)

tree1 = Tree("tree1.png", 20, 20, 100, 400)


clock = pygame.time.Clock()

runing = True

shoting = False

start_time = tm.time()
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

    screen.blit(backgraund, (0, 0))


    beaver1.reset()
    beaver1.update()
    
    tree1.reset()

    bullets_enemy.draw(screen)
    bullets_enemy.update()

    if tm.time() - start_time >= 1:
        if shoting == False:
            beaver1.fire1()
        start_time = tm.time()

    clock.tick(60)
    pygame.display.flip()
pygame.quit()