import pygame as py
from utils import Screen, Button
import subprocess

# INITIALIZATION OF THE PYGAME
py.init()
# INITIALIZATION OF SYSTEM FONTS
py.font.init()

# CREATING THE OBJECT OF THE CLASS Screen FOR MENU SCREEN
menuScreen = Screen("Menu Screen")


# CALLING OF THE FUNCTION TO MAKE THE SCREEN FOR THE WINDOW
win = menuScreen.makeCurrentScreen()

# MENU BUTTON
GAME_BUTTON = Button(150, 150, 150, 50, (255, 250, 250),
                     (255, 0, 0), "TimesNewRoman",
                     (255, 255, 255), "GAME MODE")
PLAIN_BUTTON = Button(150, 250, 150, 50, (255, 250, 250),
                     (255, 0, 0), "TimesNewRoman",
                     (255, 255, 255), "PLAIN MODE")
done = False
toggle = False

# MAIN LOOPING
while not done:
    # CALLING OF screenUpdatefunction FOR MENU SCREEN
    menuScreen.screenUpdate()

    # STORING THE MOUSE EVENT TO CHECK THE POSITION OF THE MOUSE
    mouse_pos = py.mouse.get_pos()
    # CHECKING THE MOUSE CLICK EVENT
    mouse_click = py.mouse.get_pressed()
    # KEY PRESSED OR NOT
    keys = py.key.get_pressed()

    # CHECKING MENU SCREEN FOR ITS UPDATE
    if menuScreen.checkUpdate((25, 0, 255)):
        gmbtn_pressed = GAME_BUTTON.focusCheck(mouse_pos, mouse_click)
        pbtn_pressed = PLAIN_BUTTON.focusCheck(mouse_pos, mouse_click)
        GAME_BUTTON.showButton(menuScreen.returnTitle())
        PLAIN_BUTTON.showButton(menuScreen.returnTitle())
        if gmbtn_pressed:
            # win = control_bar.makeCurrentScreen()
            menuScreen.endCurrentScreen()
            done = True
            subprocess.call("python game.py", shell=True)
        elif pbtn_pressed:
            menuScreen.endCurrentScreen()
            done = True
            subprocess.call("python plain.py", shell=True)

    # CHECKING IF THE EXIT BUTTON HAS BEEN CLICKED OR NOT
    for event in py.event.get():

        # IF CLICKED THEN CLOSE THE WINDOW
        if (event.type == py.QUIT):
            done = True

    py.display.update()

# CLOSE THE PROGRAM
py.quit()



