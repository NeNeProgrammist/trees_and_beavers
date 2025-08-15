import pygame
from pygame.locals import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

rects_H = pygame.sprite.Group()
rects_V = pygame.sprite.Group()

rects = []
x_rem, y_rem = -1, -1
y_new = 0
x_new = 0
click = False
resize = False
color = 'green'
other_rects = {}
press_ctrl = False
press_left = False
press_right = False
press_up = False
press_down = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    screen.fill("purple")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
            click = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            press_left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            press_right = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            press_up = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            press_down = True    
        
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            press_left = False
            other_rects.clear()
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            press_right = False
            other_rects.clear()
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            press_up = False
            other_rects.clear()
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            press_down = False
            other_rects.clear()

        if event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
            click = False
            press_ctrl = False
            other_rects.clear()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            print(x, y)
            rects.append(pygame.Rect(x, y, 100, 50))
            
            #rects_H.add(rect_H)
            print('Левая клавиша')
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            print('Правая клавиша')
            x, y = event.pos
            print(x, y)
            rects.append(pygame.Rect(x, y, 50, 100))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            print('Колёсико')
            x_rem, y_rem = event.pos
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            resize = True
        if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
            resize = False
        if (event.type == pygame.MOUSEMOTION and resize) or (event.type == pygame.MOUSEMOTION and click):
            x_pos, y_pos = event.pos  # Получаем текущие координаты курсора
            print(x_pos, y_pos)
            x_old = x_pos
            y_old = y_pos
            

            for rect in rects:
                if rect.collidepoint(x_pos, y_pos) and not click and resize:
                    if y_new > y_old:
                        y_new = y_pos
                        rect.height += 1
                    print("Курсор внутри прямоугольника!")
                if rect.collidepoint(x_pos, y_pos) and not click and resize:
                    if y_new < y_old:
                        y_new = y_pos
                        rect.height -= 1
                    print("Курсор внутри прямоугольника!")
                if rect.collidepoint(x_pos, y_pos) and not click and resize:
                    if x_new < x_old:
                        x_new = x_pos
                        rect.width += 1
                    print("Курсор внутри прямоугольника!")
                if rect.collidepoint(x_pos, y_pos) and not click and resize:
                    if x_new > x_old:
                        x_new = x_pos
                        rect.width -= 1
                    print("Курсор внутри прямоугольника!")

                if rect.collidepoint(x_pos, y_pos) and click:
                    rect.centerx = x_pos
                    rect.centery = y_pos
                    other_rects[rects.index(rect)] = rect
                    press_ctrl = True
                    print('Поймал', other_rects)
                

                #other_rects = {}
        

    # fill the screen with a color to wipe away anything from last frame
    
    #rects_H.draw(screen)
    if len(rects) != 0:
        for rect in rects:
            if rect.collidepoint(x_rem, y_rem):
                rects.remove(rect)
            if rect.collidepoint(pygame.mouse.get_pos()) and press_left and not click:
                other_rects[rects.index(rect)] = rect
                rect.x -= 1
            if rect.collidepoint(pygame.mouse.get_pos()) and press_right and not click:
                other_rects[rects.index(rect)] = rect
                rect.x += 1
            if rect.collidepoint(pygame.mouse.get_pos()) and press_up and not click:
                other_rects[rects.index(rect)] = rect
                rect.y -= 1
            if rect.collidepoint(pygame.mouse.get_pos()) and press_down and not click:
                other_rects[rects.index(rect)] = rect
                rect.y += 1
            
            if len(other_rects) != 0:
                for other in other_rects:
                    print(other)
                    if (other_rects[other].colliderect(rect) and click and press_ctrl) or (other_rects[other].colliderect(rect) and (press_down or press_right or press_left or press_up)):
                        color = 'red'
                        print(color)
                    else:
                        color = 'green'
            else:
                color = 'green'
                #pygame.draw.rect(screen, color, rect)
            
            '''collision_rect = rect.collidelist(rects)
            if collision_rect != -1:
                print('Пересекаюсь', collision_rect)'''

            '''for rect_any in range(1, len(rects)):
                if rects[rect_any].colliderect(rects[rect_any-1]):
                    color = 'red'
                else:
                    color = 'green'
                pygame.draw.rect(screen, color, rects[rect_any-1])'''
            pygame.draw.rect(screen, color, rect)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()