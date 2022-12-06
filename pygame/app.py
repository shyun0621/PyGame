from types import BuiltinFunctionType
import pygame
import textboxify
import pdb


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  3, 140, 252)
GREEN = (132, 252,   3)
RED   = (252,   3,  65)


class badgeGroupObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        surface = pygame.display.get_surface()
        self.x, self.y = size = surface.get_width(), surface.get_height()
        self.board_image = pygame.image.load('images/board.png')
        self.game_surf = pygame.Surface((self.x // 2, self.y // 1.2))
        self.rect = self.board_image.get_rect(center=(self.x // 2, self.y - self.game_surf.get_height() // 2))

        self.board_image = pygame.image.load('images/board.png')
        self.board_image = pygame.transform.scale(self.board_image,
                                                  (self.game_surf.get_width() - 20, self.game_surf.get_height() - 20))
        self.rect_board = self.board_image.get_rect(
            center=(self.x // 2 - 20, self.y - self.board_image.get_height() // 2 - 120))

        self.badge1 = pygame.image.load('images/badge1.png')
        self.badge1 = pygame.transform.scale(self.badge1, (240, 180))
        self.rect1 = self.badge1.get_rect(center=(self.x // 4 + 170, self.y - self.board_image.get_height() // 2 - 100))

        self.badge2 = pygame.image.load('images/badge2.png')
        self.badge2 = pygame.transform.scale(self.badge2, (240, 180))
        self.rect2 = self.badge2.get_rect(
            center=(self.x // 4 * 3 - 200, self.y - self.board_image.get_height() // 2 - 100))

        self.badge3 = pygame.image.load('images/badge3.png')
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
            if event.type == pygame.MOUSEMOTION:
                # put the collide check for mouse hover here for each button
                if self.rect1.collidepoint(pygame.mouse.get_pos()):
                    badge1_message = myFont.render('make less than 10 min cycle', False, (0, 0, 0), (255, 255, 0))
                    mouse_pos = pygame.mouse.get_pos()
                    display.blit(badge1_message, (mouse_pos[0] + 16, mouse_pos[1]))
                elif self.rect2.collidepoint(pygame.mouse.get_pos()):
                    badge2_message = myFont.render('less than 100Wh energy per cycle', False, (0, 0, 0), (255, 255, 0))
                    mouse_pos = pygame.mouse.get_pos()
                    display.blit(badge2_message, (mouse_pos[0] + 16, mouse_pos[1]))
                elif self.rect3.collidepoint(pygame.mouse.get_pos()):
                    badge3_message = myFont.render('run more than 100 cold cycle', False, (0, 0, 0), (255, 255, 0))
                    mouse_pos = pygame.mouse.get_pos()
                    display.blit(badge3_message, (mouse_pos[0] + 16, mouse_pos[1]))

class badgeObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.clicked = False

    def render(self, display):
        self.image = pygame.image.load('images/trophy.png')
        self.image = pygame.transform.scale(self.image, (150, 150))

        surface = pygame.display.get_surface()
        x,y = size = surface.get_width(), surface.get_height()
        self.rect = self.image.get_rect(center=(x - 100, 100))
        display.blit(self.image, self.rect)

    def update(self, event_list):
        global badge_clicked
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if self.rect.collidepoint(event.pos):
                badge_clicked = True


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

        if isAllSet:
            self.image = pygame.image.load('images/start.png')
            self.image = pygame.transform.scale(self.image, (150, 150))

            surface = pygame.display.get_surface()
            x,y = size = surface.get_width(), surface.get_height()
            self.rect = self.image.get_rect(center=(1250, y - self.image.get_height() * 2.5))
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

badge_clicked = False
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
# badge_screen = pygame.display.set_mode((SCREEN_WIDTH//3, SCREEN_HEIGHT//3 * 2), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
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

fill_group.draw(screen)

washer = WasherObject()
badge = badgeObject()
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
    badge.update(event_list)
    badge.render(screen)

    # if dialog_step <= FINAL_STEP:
    dialog_group.add(dialog_box)
    dialog_group.update()
    rects = dialog_group.draw(screen)
    pygame.display.update(rects)

    bar.render(screen)
    badgeGroup = badgeGroupObject()
    badgeGroup.render(screen)
    badgeGroup.update(event_list, screen)

    pygame.display.flip()

pygame.quit()
exit()