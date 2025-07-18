import pygame

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

class Beaver(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

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

class Bullets(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y)
        self.speed = speed
        
    def update1(self):
        self.rect.x -= self.speed

clock = pygame.time.Clock()

runing = True

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

    screen.blit(backgraund, (0, 0))


    beaver1.reset()
    beaver1.update()
    
    tree1.reset()

    clock.tick(60)
    pygame.display.flip()
pygame.quit()