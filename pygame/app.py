from types import BuiltinFunctionType
import pygame
import textboxify

YELLOW = (255, 204,   0)
PUPPLE = (153,   0, 255)
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
BLUE   = (  3, 140, 252)
GREEN  = (132, 252,   3)
RED    = (252,   3,  65)

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

        if  isAllSet:
            self.image = pygame.image.load('images/thumb.png')
        else:
            self.image = pygame.image.load('images/ready.png')

        self.image = pygame.transform.scale(self.image, (300, 300))

        surface = pygame.display.get_surface()
        x,y = size = surface.get_width(), surface.get_height()
        self.rect = self.image.get_rect(center = (1100, y - 30 - self.image.get_height() / 2))
        display.blit(self.image, self.rect)

class CycleObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, index):
        super().__init__()
        self.index = index
        self.image = pygame.image.load(image)
        # self.image = pygame.transform.scale(self.image, (self.image.get_width() / 2, self.image.get_height() / 2))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center = (x, y))
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
                            clickedItemIndex = -1
                            dialog_box.reset(hard=True)
                            dialog_box.set_text(dialog_text[FINAL_STEP + clickedMenuIndex + 1])
                        elif not self.clicked:
                            clickedMenuIndex = -1
                            clickedItemIndex = -1
                            dialog_box.reset(hard=True)
                            dialog_box.set_text(dialog_text[10])


class InventoryObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/inventory.png')
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
        text = "0"
        if index == 0:
            text = "1"
        elif index == 1:
            text = "5"
        elif index == 2:
            text = "10"
        elif index == 3:
            text = "30"
        elif index == 4:
            text = "60"

        self.textSurf = myFont.render(text, True, (255, 255, 255))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [0, 0])

    def update(self, event_list):
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
                    if self.index == -1:
                        cycle[clickedMenuIndex] = 0
                    elif self.index == 0:
                        cycle[clickedMenuIndex] += 1
                    elif self.index == 1:
                        cycle[clickedMenuIndex] += 5
                    elif self.index == 2:
                        cycle[clickedMenuIndex] += 10
                    elif self.index == 3:
                        cycle[clickedMenuIndex] += 30
                    elif self.index == 4:
                        cycle[clickedMenuIndex] += 60

                    if cycle[clickedMenuIndex] > 60:
                        cycle[clickedMenuIndex] = 60

class BarObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/bar.png')
        self.image = pygame.transform.scale(self.image, (603, 300))
        self.rect = self.image.get_rect(topleft = (1250, 750))

    def render(self, display):
        display.blit(self.image, self.rect)
        global selectedItem
        global isAllSet
        for idx in range(len(selectedItem)):
            if selectedItem[idx] >= 0:
                if idx == 0:
                    pygame.draw.rect(display, PUPPLE, (DEFAULT_BAR_X, DEFAULT_BAR_Y - 1, DEFAULT_BAR_WIDTH * cycle[idx], DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(cycle[idx]), True, BLACK)
                    screen.blit(title, [1450, DEFAULT_BAR_Y - 1])
                elif idx == 1:
                    pygame.draw.rect(display, GREEN, (DEFAULT_BAR_X, DEFAULT_BAR_Y + 52, DEFAULT_BAR_WIDTH * cycle[idx], DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(cycle[idx]), True, BLACK)
                    screen.blit(title, [1450, DEFAULT_BAR_Y + 52])
                elif idx == 2:
                    pygame.draw.rect(display, BLUE, (DEFAULT_BAR_X, DEFAULT_BAR_Y + 105, DEFAULT_BAR_WIDTH * cycle[idx], DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(cycle[idx]), True, BLACK)
                    screen.blit(title, [1450, DEFAULT_BAR_Y + 105])
                elif idx == 3:
                    pygame.draw.rect(display, RED, (DEFAULT_BAR_X, DEFAULT_BAR_Y + 160, DEFAULT_BAR_WIDTH * cycle[idx], DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(cycle[idx]), True, BLACK)
                    screen.blit(title, [1450, DEFAULT_BAR_Y + 159])
                elif idx == 4:
                    pygame.draw.rect(display, YELLOW, (DEFAULT_BAR_X, DEFAULT_BAR_Y + 213, DEFAULT_BAR_WIDTH * cycle[idx], DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(cycle[idx]), True, BLACK)
                    screen.blit(title, [1450, DEFAULT_BAR_Y + 214])


DEFAULT_BAR_X = 1391
DEFAULT_BAR_Y = 769
DEFAULT_BAR_WIDTH = 7.4
DEFAULT_BAR_HEIGHT = 34

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
bg = pygame.image.load('images/background.png')
clock = pygame.time.Clock()
myFont = pygame.font.SysFont("arial", 30, True, False)

cycleItem_width = cycleItem_height = 100

item_group = pygame.sprite.Group()
item_group.add(CycleObject(10 + cycleItem_width / 2, 30, 'images/fill.png', 0))
item_group.add(CycleObject(100 + cycleItem_width / 2, 30, 'images/wash.png', 1))
item_group.add(CycleObject(190 + cycleItem_width / 2, 30, 'images/spin.png', 2))
item_group.add(CycleObject(280 + cycleItem_width / 2, 30, 'images/rinse.png', 3))
item_group.add(CycleObject(370 + cycleItem_width / 2, 30, 'images/drain.png', 4))

fill_group = pygame.sprite.Group()
fill_group.add(InventorySlotObject('images/potion_fill.png', (41, 162), -1))
fill_group.add(InventorySlotObject('images/potion_fill.png', (139, 162), 0))
fill_group.add(InventorySlotObject('images/potion_fill.png', (238, 162), 1))
fill_group.add(InventorySlotObject('images/potion_fill.png', (41, 248), 2))
fill_group.add(InventorySlotObject('images/potion_fill.png', (139, 248), 3))
fill_group.add(InventorySlotObject('images/potion_fill.png', (238, 248), 4))

wash_group = pygame.sprite.Group()
wash_group.add(InventorySlotObject('images/potion_wash.png', (41, 162), -1))
wash_group.add(InventorySlotObject('images/potion_wash.png', (139, 162), 0))
wash_group.add(InventorySlotObject('images/potion_wash.png', (238, 162), 1))
wash_group.add(InventorySlotObject('images/potion_wash.png', (41, 248), 2))
wash_group.add(InventorySlotObject('images/potion_wash.png', (139, 248), 3))
wash_group.add(InventorySlotObject('images/potion_wash.png', (238, 248), 4))

spin_group = pygame.sprite.Group()
spin_group.add(InventorySlotObject('images/potion_spin.png', (41, 162), -1))
spin_group.add(InventorySlotObject('images/potion_spin.png', (139, 162), 0))
spin_group.add(InventorySlotObject('images/potion_spin.png', (238, 162), 1))
spin_group.add(InventorySlotObject('images/potion_spin.png', (41, 248), 2))
spin_group.add(InventorySlotObject('images/potion_spin.png', (139, 248), 3))
spin_group.add(InventorySlotObject('images/potion_spin.png', (238, 248), 4))

rinse_group = pygame.sprite.Group()
rinse_group.add(InventorySlotObject('images/potion_rinse.png', (41, 162), -1))
rinse_group.add(InventorySlotObject('images/potion_rinse.png', (139, 162), 0))
rinse_group.add(InventorySlotObject('images/potion_rinse.png', (238, 162), 1))
rinse_group.add(InventorySlotObject('images/potion_rinse.png', (41, 248), 2))
rinse_group.add(InventorySlotObject('images/potion_rinse.png', (139, 248), 3))
rinse_group.add(InventorySlotObject('images/potion_rinse.png', (238, 248), 4))

drain_group = pygame.sprite.Group()
drain_group.add(InventorySlotObject('images/potion_drain.png', (41, 162), -1))
drain_group.add(InventorySlotObject('images/potion_drain.png', (139, 162), 0))
drain_group.add(InventorySlotObject('images/potion_drain.png', (238, 162), 1))
drain_group.add(InventorySlotObject('images/potion_drain.png', (41, 248), 2))
drain_group.add(InventorySlotObject('images/potion_drain.png', (139, 248), 3))
drain_group.add(InventorySlotObject('images/potion_drain.png', (238, 248), 4))

washer = WasherObject()
inventory = InventoryObject()
bar = BarObject()

clickedMenuIndex = -1
clickedItemIndex = -1
isAllSet = False
dialog_step = 0
FINAL_STEP = 4
dialog_text = [
    "HoyLee: Hello~ Washer",
    "Washer: Hi~ HyoLee",
    "HoyLee: How can I make a custom cycle?",
    "Washer: You can make it by clicking the items!!",
    "Washer: Washer:Let's click first item",
    "Washer: Select your Fill Item",
    "Washer: Select your Wash Item",
    "Washer: Select your Spin Item",
    "Washer: Select your Rinse Item",
    "Washer: Select your Drain Item",
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

MENU_COUNT = 5
selectedItem = [-1 for i in range(MENU_COUNT)]

cycle = [0 for i in range(MENU_COUNT)]

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
    elif clickedMenuIndex == 4:
        drain_group.update(event_list)
        drain_group.draw(screen)

    washer.render(screen)

    # if dialog_step <= FINAL_STEP:
    dialog_group.add(dialog_box)
    dialog_group.update()
    rects = dialog_group.draw(screen)
    pygame.display.update(rects)

    bar.render(screen)
    pygame.display.flip()

pygame.quit()
exit()