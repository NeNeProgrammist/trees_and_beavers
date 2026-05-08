import pygame
import time as tm

tree_list = []
enemy_list = []
shoting = False
bullets_enemy = None
bullets_trees = None
anim_exp_groop = None
screen = None
play = True
beaver_kill_count = 0

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

class TreesBullets(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 1700:
            self.kill()

class Beaver(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed, health, tree_near_beaver, beaver_road_f):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.speed = speed
        self.images = []
        self.start_time = tm.time()
        self.tree_near_beaver = tree_near_beaver
        self.beaver_road_f = beaver_road_f
        self.animacion_counter = 0
        self.animacion_speed = 3
        for i in range(2, 4):
            img = pygame.image.load(f"sprites/beaver{i}.png")
            img = pygame.transform.scale(img, (size_x, size_y))
            self.images.append(img)
        self.curent_frame = 0
        self.image = self.images[self.curent_frame]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update_animasion(self):
        if self.tree_near_beaver == False:
            self.animacion_counter += 1
            if self.animacion_counter >= self.animacion_speed:
                self.animacion_counter = 0
                self.curent_frame = (self.curent_frame + 1) % len(self.images)
                self.image = self.images[self.curent_frame]

    def is_beaver_cell_ocuped(self):
        self.tree_near_beaver = False
        for tree in tree_list:
            if 20 >= (self.rect.y - tree.rect.y) and (tree.rect.y - self.rect.y) <= 20:
                if 0 < (self.rect.x - tree.rect.x) <= 100:
                    if tree in tree_list:
                        self.tree_near_beaver = True

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
            self.update_animasion()
            self.is_beaver_cell_ocuped()

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
                        bullet = Bullets("sprites/bullet.png", 30, 6, self.rect.x, self.rect.y, 4, 100)
                        bullets_enemy.add(bullet)
                    self.start_time = tm.time()

class Seed(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health, tree_number):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.tree_number = tree_number

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
                        bullet = TreesBullets("sprites/tree_bullet.png", 30, 6, self.rect.x, self.rect.y, 6, 100)
                        bullets_trees.add(bullet)
                    self.start_time2 = tm.time()

    def take_hit(self):
        """Дерево получает удар от дятла"""
        self.health -= 1
        if self.health <= 0:
            # Уничтожаем дерево
            return True
        return False

class Shovel(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, health):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)

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

class Bug(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed, health, tree_near_bug):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y, health)
        self.speed = speed
        self.images = []
        self.start_time = tm.time()
        self.tree_near_bug = tree_near_bug
        self.animacion_counter = 0
        self.animacion_speed = 5
        for i in range(1, 3):
            img = pygame.image.load(f"sprites/bug{i}.png")
            img = pygame.transform.scale(img, (size_x, size_y))
            self.images.append(img)
        self.curent_frame = 0
        self.image = self.images[self.curent_frame]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update_animasion(self):
        self.animacion_counter += 1
        if self.animacion_counter >= self.animacion_speed:
            self.animacion_counter = 0
            self.curent_frame = (self.curent_frame + 1) % len(self.images)
            self.image = self.images[self.curent_frame]

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
        self.update_animasion()
        if self.tree_near_bug == False:
            self.rect.x -= self.speed
            self.is_bug_cell_ocuped()
        else:
            self.exploshen()
            exp = Anim_exploushen(self.rect.centerx - 245, self.rect.centery - 215, 390, 351)
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
