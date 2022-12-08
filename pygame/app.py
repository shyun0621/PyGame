from lua_generation import *
import pygame
import textboxify
from threading import Thread
from os import system, chdir, getcwd
import os

IMAGE_PATH = "/Users/hykim/project/hackathon/PyGame/pygame/images"

YELLOW = (255, 204, 0)
PUPPLE = (153, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (3, 140, 252)
GREEN = (132, 252, 3)
RED = (252, 3, 65)


class WasherObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def render(self, display):
        global selectedItem
        isAllSet = True
        for item in selectedItem:
            if item < 0:
                isAllSet = False
                break

        if isAllSet:
            self.image = pygame.image.load(os.path.join(IMAGE_PATH + '/thumb.png'))
        else:
            self.image = pygame.image.load(os.path.join(IMAGE_PATH + '/ready.png'))

        self.image = pygame.transform.scale(self.image, (300, 300))

        surface = pygame.display.get_surface()
        x, y = size = surface.get_width(), surface.get_height()
        self.rect = self.image.get_rect(center=(1100, y - 30 - self.image.get_height() / 2))
        display.blit(self.image, self.rect)


class CycleObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, index):
        super().__init__()
        self.index = index
        self.image = pygame.image.load(image)
        # self.image = pygame.transform.scale(self.image, (self.image.get_width() / 2, self.image.get_height() / 2))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=(x, y))
        self.clicked = False

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                global dialog_step
                if dialog_step >= FINAL_STEP:
                    if self.rect.collidepoint(event.pos):
                        global menuSoundEffect
                        menuSoundEffect.play()
                        global clickedMenuIndex
                        global clickedItemIndex
                        global dialog_box
                        self.clicked = not self.clicked
                        if self.clicked:
                            clickedMenuIndex = self.index
                            clickedItemIndex = 0
                            dialog_box.reset(hard=True)
                            dialog_box.set_text(dialog_text[FINAL_STEP + clickedMenuIndex + 1])
                        elif not self.clicked:
                            clickedMenuIndex = -1
                            clickedItemIndex = 0
                            dialog_box.reset(hard=True)
                            dialog_box.set_text(dialog_text[10])


class InventoryObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_PATH + '/inventory.png'))
        self.image = pygame.transform.scale(self.image, (300, 180))
        self.rect = self.image.get_rect()
        self.rect.topleft = (30, 150)

    def render(self, display, index):
        if index >= 0:
            display.blit(self.image, self.rect)


class InventorySlotObject(pygame.sprite.Sprite):
    def __init__(self, name, pos, index):
        super().__init__()
        self.index = index
        self.image = pygame.image.load(name)
        self.image = pygame.transform.scale(self.image, (80, 70))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.clicked = False
        self.index = index

    def update(self, event_list):
        text = "0"
        global clickedMenuIndex
        if clickedMenuIndex == 0:
            text = itemText[0][self.index]
        else:
            text = itemText[1][self.index]

        self.textSurf = myFont.render(text, True, (255, 255, 255))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [0, 0])

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = not self.clicked
                    itemSoundEffect.play()
                    global clickedItemIndex
                    global selectedItem
                    # if self.clicked:
                    clickedItemIndex = self.index

                    selectedItem[clickedMenuIndex] = clickedItemIndex
                    if self.index == 0:
                        cycle[clickedMenuIndex] = 0
                    elif self.index == 1:
                        cycle[clickedMenuIndex] += 1
                    elif self.index == 2:
                        cycle[clickedMenuIndex] += 2
                    elif self.index == 3:
                        cycle[clickedMenuIndex] += 4
                    elif self.index == 4:
                        cycle[clickedMenuIndex] += 8

                    if clickedMenuIndex == 0:
                        if cycle[clickedMenuIndex] > 8:
                            cycle[clickedMenuIndex] = 8
                    else:
                        if cycle[clickedMenuIndex] > 40:
                            cycle[clickedMenuIndex] = 40


class BarObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_PATH + '/bar.png'))
        self.image = pygame.transform.scale(self.image, (603, 300))
        self.rect = self.image.get_rect(topleft=(1250, 750))

    def render(self, display):
        display.blit(self.image, self.rect)
        global clickedMenuIndex
        global selectedItem
        global isAllSet
        global itemText
        color = YELLOW
        offsetH = 0
        offsetW = 0

        pygame.draw.rect(display, YELLOW,
                         (DEFAULT_BAR_X, DEFAULT_BAR_Y + 213, DEFAULT_BAR_WIDTH * 60, DEFAULT_BAR_HEIGHT), 0)

        for idx in range(len(selectedItem)):
            if selectedItem[idx] >= 0:
                if clickedMenuIndex == 0:
                    title = myFont.render(str(cycle[idx]), True, BLACK)
                else:
                    title = myFont.render(str(cycle[idx]), True, BLACK)

                if idx == 0:
                    offsetH = 0
                    offsetW = cycle[idx] * 60 / 8
                    color = PUPPLE
                elif idx == 1:
                    offsetH = 53
                    offsetW = cycle[idx] * 60 / 40
                    color = GREEN
                elif idx == 2:
                    offsetH = 106
                    offsetW = cycle[idx] * 60 / 40
                    color = BLUE
                elif idx == 3:
                    offsetH = 161
                    offsetW = cycle[idx] * 60 / 40
                    color = RED

                pygame.draw.rect(display, color, (
                DEFAULT_BAR_X, DEFAULT_BAR_Y + offsetH, DEFAULT_BAR_WIDTH * offsetW, DEFAULT_BAR_HEIGHT), 0)
                screen.blit(title, [1450, DEFAULT_BAR_Y + offsetH])


class badgeGroupObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        surface = pygame.display.get_surface()
        self.x, self.y = size = surface.get_width(), surface.get_height()
        self.board_image = pygame.image.load(os.path.join(IMAGE_PATH + '/board.png'))
        self.game_surf = pygame.Surface((self.x // 2, self.y // 1.2))
        self.rect = self.board_image.get_rect(center=(self.x // 2, self.y - self.game_surf.get_height() // 2))

        self.board_image = pygame.image.load(os.path.join(IMAGE_PATH + '/board.png'))
        self.board_image = pygame.transform.scale(self.board_image,
                                                  (self.game_surf.get_width() - 20, self.game_surf.get_height() - 20))
        self.rect_board = self.board_image.get_rect(
            center=(self.x // 2 - 20, self.y - self.board_image.get_height() // 2 - 120))

        self.badge1 = pygame.image.load(os.path.join(IMAGE_PATH + '/badge1.png'))
        self.badge1 = pygame.transform.scale(self.badge1, (240, 180))
        self.rect1 = self.badge1.get_rect(center=(self.x // 4 + 170, self.y - self.board_image.get_height() // 2 - 100))

        self.badge2 = pygame.image.load(os.path.join(IMAGE_PATH + '/badge2.png'))
        self.badge2 = pygame.transform.scale(self.badge2, (240, 180))
        self.rect2 = self.badge2.get_rect(
            center=(self.x // 4 * 3 - 200, self.y - self.board_image.get_height() // 2 - 100))

        self.badge3 = pygame.image.load(os.path.join(IMAGE_PATH + '/badge3.png'))
        self.badge3 = pygame.transform.scale(self.badge3, (240, 180))
        self.rect3 = self.badge3.get_rect(center=(self.x // 4 + 170, self.y - self.board_image.get_height() // 2 + 80))

    def render(self, display):
        global badge_clicked
        if badge_clicked:
            display.blit(self.game_surf, self.rect)
            display.blit(self.board_image, self.rect_board)
            display.blit(self.badge1, self.rect1)
            display.blit(self.badge2, self.rect2)
            display.blit(self.badge3, self.rect3)

    def update(self, event_list, display):
        global badge_clicked
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    badge_clicked = False
                    # print('badge_clicked to false')
            if event.type == pygame.MOUSEMOTION:
                # put the collide check for mouse hover here for each button
                if self.rect1.collidepoint(pygame.mouse.get_pos()):
                    badge1_message = myFont.render('make less than 10 min cycle', False, (255, 255, 255), (128, 128, 128))
                    mouse_pos = pygame.mouse.get_pos()
                    display.blit(badge1_message, (mouse_pos[0] + 16, mouse_pos[1]))
                elif self.rect2.collidepoint(pygame.mouse.get_pos()):
                    badge2_message = myFont.render('less than 100 Wh energy per cycle', False, (255, 255, 255), (128, 128, 128))
                    mouse_pos = pygame.mouse.get_pos()
                    display.blit(badge2_message, (mouse_pos[0] + 16, mouse_pos[1]))
                elif self.rect3.collidepoint(pygame.mouse.get_pos()):
                    badge3_message = myFont.render('run more than 20 cold cycle', False, (255, 255, 255), (128, 128, 128))
                    mouse_pos = pygame.mouse.get_pos()
                    display.blit(badge3_message, (mouse_pos[0] + 16, mouse_pos[1]))


class badgeObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_PATH + '/trophy.png'))
        self.image = pygame.transform.scale(self.image, (150, 150))

        surface = pygame.display.get_surface()
        x, y = size = surface.get_width(), surface.get_height()
        self.rect = self.image.get_rect(center=(x - 100, 100))

    def render(self, display):
        display.blit(self.image, self.rect)

    def update(self, event_list):
        global badge_clicked
        for event in event_list:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                badge_clicked = True


class startButtonObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_PATH + '/start.png'))
        self.image = pygame.transform.scale(self.image, (150, 150))

        surface = pygame.display.get_surface()
        x, y = size = surface.get_width(), surface.get_height()
        self.rect = self.image.get_rect(center=(1250, y - self.image.get_height() * 2.5))

    def render(self, display):
        global selectedItem
        isAllSet = True
        for item in selectedItem: # [0 3 1 1 4]
            if item < 0:
                isAllSet = False
                break
        if isAllSet:
            display.blit(self.image, self.rect)

    def onlyForTest(self):
        SaveToLua(selectedItem, "diy_cycle.lua", "Diy Cycle")
        game_dir = getcwd()
        dpath = "/Users/hykim/project/frontLoad/laundry.washer-global-front-load-2019-source-snapshot/"

        # dpath = "/Users/gea_hs/Documents/projects/hackathon/2022_2nd/laundry.washer-global-front-load-2019-source-snapshot/"
        chdir(dpath)
        system("dmake -f gfl-mc-target.mk RELEASE=Y DEBUG=N build_parametric")
        # system("dmake -f gfl-mc-target.mk package -j16 RELEASE=N DEBUG=N")
        chdir(game_dir)


    def update(self, event_list):
        for event in event_list:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                t = Thread(target=self.onlyForTest, args=())
                t.start()
                # SaveToLua(selectedItem, "diy_cycle.lua", "Diy Cycle")
                game_dir = getcwd()
                dpath = "/Users/gea_hs/Documents/projects/hackathon/2022_2nd/laundry.washer-global-front-load-2019-source-snapshot/Parametric/lua/data/global_front_load/model_data/cycles"
                chdir(dpath)
                SaveToLua(cycle, "diy_cycle.lua", "Diy Cycle")

                gpath = "/Users/jessie/GEA_Code/laundry.washer-global-front-load-2019-source-snapshot/Parametric/lua/data/global_front_load/model_data/cycles"
                chdir(gpath)
                system("dmake -f gfl-mc-target.mk package -j16 RELEASE=N DEBUG=N")
                chdir(game_dir)


DEFAULT_BAR_X = 1391
DEFAULT_BAR_Y = 768
DEFAULT_BAR_WIDTH = 7.4
DEFAULT_BAR_HEIGHT = 34

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
badge_clicked = False

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
bg = pygame.image.load(os.path.join(IMAGE_PATH + '/background.png'))
clock = pygame.time.Clock()
myFont = pygame.font.SysFont("arial", 30, True, False)

cycleItem_width = cycleItem_height = 100

item_group = pygame.sprite.Group()
item_group.add(CycleObject(10 + cycleItem_width / 2, 30, os.path.join(IMAGE_PATH + '/fill.png'), 0))
item_group.add(CycleObject(100 + cycleItem_width / 2, 30, os.path.join(IMAGE_PATH + '/wash.png'), 1))
item_group.add(CycleObject(190 + cycleItem_width / 2, 30, os.path.join(IMAGE_PATH + '/spin.png'), 2))
item_group.add(CycleObject(280 + cycleItem_width / 2, 30, os.path.join(IMAGE_PATH + '/rinse.png'), 3))

fill_group = pygame.sprite.Group()
fill_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_fill.png'), ( 41, 162), 0))
fill_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_fill.png'), (139, 162), 1))
fill_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_fill.png'), (238, 162), 2))
fill_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_fill.png'), ( 41, 248), 3))
fill_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_fill.png'), (139, 248), 4))

wash_group = pygame.sprite.Group()
wash_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_wash.png'), ( 41, 162), 0))
wash_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_wash.png'), (139, 162), 1))
wash_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_wash.png'), (238, 162), 2))
wash_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_wash.png'), ( 41, 248), 3))
wash_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_wash.png'), (139, 248), 4))

spin_group = pygame.sprite.Group()
spin_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_spin.png'), ( 41, 162), 0))
spin_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_spin.png'), (139, 162), 1))
spin_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_spin.png'), (238, 162), 2))
spin_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_spin.png'), ( 41, 248), 3))
spin_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_spin.png'), (139, 248), 4))

rinse_group = pygame.sprite.Group()
rinse_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_rinse.png'), ( 41, 162), 0))
rinse_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_rinse.png'), (139, 162), 1))
rinse_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_rinse.png'), (238, 162), 2))
rinse_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_rinse.png'), ( 41, 248), 3))
rinse_group.add(InventorySlotObject(os.path.join(IMAGE_PATH + '/potion_rinse.png'), (139, 248), 4))

washer = WasherObject()
inventory = InventoryObject()
badge = badgeObject()
start_button = startButtonObject()
bar = BarObject()

clickedMenuIndex = -1
clickedItemIndex = 0
isAllSet = False
dialog_step = 0
FINAL_STEP = 4
dialog_text = [
    "HoyLee: Hello~ Washer",
    "Washer: Hi~ HyoLee",
    "HoyLee: How can I make a custom cycle?",
    "Washer: You can make it by clicking the items!!",
    "Washer: Let's click first item",
    "Washer: Select your Fill Item (Gallon)",
    "Washer: Select your Wash Item (Minutes)",
    "Washer: Select your Spin Item (Minutes)",
    "Washer: Select your Rinse Item (Minutes)",
    # "Washer: Select your Drain Item (Minutes)",
    "Washer: You didn't select any cylcle, please click cycle icon!"
]

dialog_box = textboxify.TextBoxFrame(
        text=dialog_text[dialog_step],
        text_width=600,
        lines=2,
        pos=(100, 800),
        padding=(150, 100),
        font_color=(92, 53, 102),
        font_size=40,
        bg_color=(173, 127, 168),
    )
dialog_box.set_indicator()
dialog_box.set_portrait()
dialog_group = pygame.sprite.LayeredDirty()

MENU_COUNT = 4
selectedItem = [-1 for i in range(MENU_COUNT)]
cycle = [0 for i in range(MENU_COUNT)]
itemText = [["0", "1", "2", "4", "8"],["0", "1", "2", "4", "8"]]

menuSoundEffect = pygame.mixer.Sound('sounds/menu.wav')
menuSoundEffect.set_volume(0.1)
itemSoundEffect = pygame.mixer.Sound('sounds/item.wav')
itemSoundEffect.set_volume(0.1)

run = True
while run:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                dialog_box.reset(hard=True)
                dialog_step += 1
                if dialog_step <= FINAL_STEP:
                    dialog_box.set_text(dialog_text[dialog_step])
                else:
                    dialog_box.set_text(dialog_text[FINAL_STEP])

    screen.blit(pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    item_group.update(event_list)
    item_group.draw(screen)

    inventory.render(screen, clickedMenuIndex)

    if clickedMenuIndex == 0:
        fill_group.update(event_list)
        fill_group.draw(screen)
    elif clickedMenuIndex == 1:
        wash_group.update(event_list)
        wash_group.draw(screen)
    elif clickedMenuIndex == 2:
        spin_group.update(event_list)
        spin_group.draw(screen)
    elif clickedMenuIndex == 3:
        rinse_group.update(event_list)
        rinse_group.draw(screen)

    washer.render(screen)
    start_button.update(event_list)
    start_button.render(screen)

    # if dialog_step <= FINAL_STEP:
    dialog_group.add(dialog_box)
    dialog_group.update()
    rects = dialog_group.draw(screen)

    bar.render(screen)
    badgeGroup = badgeGroupObject()
    badgeGroup.render(screen)
    badgeGroup.update(event_list, screen)

    badge.update(event_list)
    badge.render(screen)

    pygame.display.update(rects)
    pygame.display.flip()

pygame.quit()
exit()
