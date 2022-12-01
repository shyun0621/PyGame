from types import BuiltinFunctionType
import pygame
import textboxify
import pdb


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  3, 140, 252)
GREEN = (132, 252,   3)
RED   = (252,   3,  65)


class startButtonObject(pygame.sprite.Sprite):
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
            self.image = pygame.image.load('images/start.png')
            self.image = pygame.transform.scale(self.image, (150, 150))

            surface = pygame.display.get_surface()
            x,y = size = surface.get_width(), surface.get_height()
            self.rect = self.image.get_rect(center = (1250, y - self.image.get_height() * 2.5))
            display.blit(self.image, self.rect)


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
        self.rect = self.image.get_rect(center = (1100, y - self.image.get_height() / 2))
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
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.clicked = False

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

class BarObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/bar.png')
        self.image = pygame.transform.scale(self.image, (600, 300))
        self.rect = self.image.get_rect(topleft = (1300, 800))

    def render(self, display):
        display.blit(self.image, self.rect)
        global selectedItem
        global isAllSet
        for idx in range(len(selectedItem)):
            if selectedItem[idx] >= 0:
                if idx == 0:
                    pygame.draw.rect(display, BLUE, (DEFAULT_BAR_X, DEFAULT_BAR_Y - 1, DEFAULT_BAR_WIDTH * (selectedItem[idx] + 1), DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(selectedItem[idx] + 1), True, (0, 0, 0))
                    screen.blit(title, [1270, DEFAULT_BAR_Y - 1])
                elif idx == 1:
                    pygame.draw.rect(display, RED, (DEFAULT_BAR_X, DEFAULT_BAR_Y + 52, DEFAULT_BAR_WIDTH * (selectedItem[idx] + 1), DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(selectedItem[idx] + 1), True, (0, 0, 0))
                    screen.blit(title, [1270, DEFAULT_BAR_Y + 52])
                elif idx == 2:
                    pygame.draw.rect(display, GREEN, (DEFAULT_BAR_X, DEFAULT_BAR_Y + 105, DEFAULT_BAR_WIDTH * (selectedItem[idx] + 1), DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(selectedItem[idx] + 1), True, (0, 0, 0))
                    screen.blit(title, [1270, DEFAULT_BAR_Y + 105])
                elif idx == 3:
                    pygame.draw.rect(display, WHITE, (DEFAULT_BAR_X, DEFAULT_BAR_Y + 159, DEFAULT_BAR_WIDTH * (selectedItem[idx] + 1), DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(selectedItem[idx] + 1), True, (0, 0, 0))
                    screen.blit(title, [1270, DEFAULT_BAR_Y + 159])
                elif idx == 4:
                    pygame.draw.rect(display, BLACK, (DEFAULT_BAR_X, DEFAULT_BAR_Y + 214, DEFAULT_BAR_WIDTH * (selectedItem[idx] + 1), DEFAULT_BAR_HEIGHT), 0)
                    title= myFont.render(str(selectedItem[idx] + 1), True, (0, 0, 0))
                    screen.blit(title, [1270, DEFAULT_BAR_Y + 214])



DEFAULT_BAR_X = 1441
DEFAULT_BAR_Y = 819
DEFAULT_BAR_WIDTH = 88
DEFAULT_BAR_HEIGHT = 34

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
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
fill_group.add(InventorySlotObject('images/potion.png', (40, 154), -1))
fill_group.add(InventorySlotObject('images/potion.png', (140, 154), 0))
fill_group.add(InventorySlotObject('images/potion.png', (240, 154), 1))
fill_group.add(InventorySlotObject('images/potion.png', (40, 242), 2))
fill_group.add(InventorySlotObject('images/potion.png', (140, 242), 3))
fill_group.add(InventorySlotObject('images/potion.png', (240, 242), 4))

washer = WasherObject()
start_button = startButtonObject()
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
        pos=(100, 880),
        padding=(150, 100),
        font_color=(92, 53, 102),
        font_size=40,
        bg_color=(173, 127, 168),
    )
dialog_box.set_indicator()
dialog_box.set_portrait()
dialog_group = pygame.sprite.LayeredDirty()

ITEM_COUNT = 5
selectedItem = [-1 for i in range(ITEM_COUNT)]

menuSoundEffect = pygame.mixer.Sound('sounds/item.wav')
itemSoundEffect = pygame.mixer.Sound('sounds/menu.wav')
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
                    # pdb.set_trace()
                    dialog_box.set_text(dialog_text[FINAL_STEP])



    screen.blit(pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    item_group.update(event_list)
    item_group.draw(screen)

    inventory.render(screen, clickedMenuIndex)

    if (clickedMenuIndex >= 0):
        fill_group.update(event_list)
        fill_group.draw(screen)

    washer.render(screen)
    start_button.render(screen)

    # if dialog_step <= FINAL_STEP:
    dialog_group.add(dialog_box)
    dialog_group.update()
    rects = dialog_group.draw(screen)
    pygame.display.update(rects)

    bar.render(screen)
    pygame.display.flip()

pygame.quit()
exit()