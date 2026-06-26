import pygame
import pygame_gui
import random

pygame.init()
window = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600))

def create_main_buttons():
    global button, button2
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 275), (-1, -1)),
        text="Нажми меня",
        manager=manager
    )
    button2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 295), (-1, -1)),
        text="Улучшить клик",
        manager=manager
    )

def destroy_main_buttons():
    global button, button2
    button.kill()
    button2.kill()
    button = None
    button2 = None

create_main_buttons()

kooficient = 1
clicks = 0
norma = 10

f1 = pygame.font.SysFont("Caladea", 36)
text_surface = f1.render(f"{clicks}", True, (252, 236, 0))

clock = pygame.time.Clock()
running = True

rect_flag = False
menu_buttons = []
particles = []
dropdown = None

def update_dropdown():
    global dropdown
    if dropdown is not None:
        dropdown.kill()
        dropdown = None
    if rect_flag:
        options = [
            f"kooficient: {kooficient}",
            f"clicks: {clicks}",
            f"norma: {norma}"
        ]
        dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=options,
            starting_option=options[0],
            relative_rect=pygame.Rect((320, 390), (150, 50)),
            manager=manager
        )
        menu_buttons.append(dropdown)

def on_values_changed():
    update_dropdown()

while running:
    time_delta = clock.tick(60) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if not rect_flag:
                    rect_flag = True
                    destroy_main_buttons()
                    for btn in menu_buttons:
                        btn.kill()
                    menu_buttons.clear()

                    btn3 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((320, 205), (150, 50)),
                        text="Закрыть кликер",
                        manager=manager
                    )
                    btn5 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((320, 270), (150, 50)),
                        text="салют",
                        manager=manager
                    )
                    btn5.hide()
                    btn4 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((320, 335), (150, 50)),
                        text="Закрыть меню",
                        manager=manager
                    )
                    menu_buttons.extend([btn3, btn5, btn4])
                    update_dropdown()

        if event.type == pygame.MOUSEMOTION:
            if rect_flag and len(menu_buttons) >= 2:
                btn5 = menu_buttons[1]
                if btn5.relative_rect.collidepoint(event.pos):
                    btn5.show()
                else:
                    btn5.hide()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if button is not None and event.ui_element == button:
                button.set_text("Нажато")
                clicks += 1 * kooficient
                text_surface = f1.render(f"{clicks}", True, (252, 236, 0))
                on_values_changed()
            
            elif button2 is not None and event.ui_element == button2:
                if clicks >= norma:
                    kooficient += 1
                    norma += 10 * kooficient
                    clicks = 0
                    on_values_changed()

            elif event.ui_element in menu_buttons:
                if event.ui_element.text == "Закрыть кликер":
                    running = False

                elif event.ui_element.text == "Закрыть меню":
                    rect_flag = False
                    for btn in menu_buttons:
                        btn.kill()
                    menu_buttons.clear()
                    if dropdown is not None:
                        dropdown.kill()
                        dropdown = None
                    create_main_buttons()
                    
                elif event.ui_element.text == "салют":
                    center = event.ui_element.relative_rect.center
                    for i in range(10):
                        shape = random.choice(['circle', 'rect'])
                        if shape == 'circle':
                            color = (255, 0, 0)
                            size = 10
                        else:
                            color = (0, 0, 255)
                            size = 15
                        vx = random.uniform(-3, 3)
                        vy = random.uniform(2, 5)
                        particles.append({'x': center[0], 'y': center[1], 'vx': vx, 'vy': vy, 'size': size, 'color': color, 'shape': shape})

        manager.process_events(event)
    
    window.fill((30, 30, 30))
    
    if rect_flag:
        pygame.draw.rect(window, (100, 100, 0), pygame.Rect(100, 50, 600, 500))

    window.blit(text_surface, (15, 15))
    
    manager.update(time_delta)
    manager.draw_ui(window)
    
    particles_to_remove = []
    for p in particles:
        p['x'] += p['vx']
        p['y'] += p['vy']
        if p['y'] > 600:
            particles_to_remove.append(p)
            continue
        if p['shape'] == 'circle':
            pygame.draw.circle(window, p['color'], (int(p['x']), int(p['y'])), p['size'])
        else:
            rect = pygame.Rect(p['x'] - p['size']//2, p['y'] - p['size']//2, p['size'], p['size'])
            pygame.draw.rect(window, p['color'], rect)
    for p in particles_to_remove:
        particles.remove(p)
    
    pygame.display.update()