import pygame as py
from utils import Screen, Button
import subprocess

# INITIALIZATION OF THE PYGAME
py.init()
# INITIALIZATION OF SYSTEM FONTS
py.font.init()


class Button(object):
    def __init__(self, rect, command, event_trigger, **kwargs):
        self.rect = py.Rect(rect)
        self.command = command
        self.event_trigger = event_trigger
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self, kwargs):
        settings = {
            "color": py.Color('red'),
            "text": None,
            "font": None,  # py.font.Font(None,16),
            "call_on_release": True,
            "hover_color": None,
            "clicked_color": None,
            "font_color": py.Color("white"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
            'border_color': py.Color('black'),
            'border_hover_color': py.Color('yellow'),
            'disabled': False,
            'disabled_color': py.Color('grey'),
            'radius': 3,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text, True, color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text, True, color)
            self.text = self.font.render(self.text, True, self.font_color)

    def get_event(self, event):
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == py.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        global app_mode
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if self.event_trigger == 1:
                subprocess.call("python plain.py", shell=True)
            elif self.event_trigger == 2:
                subprocess.call("python app.py", shell=True)
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            # if user is still within button rect upon mouse release
            if self.rect.collidepoint(py.mouse.get_pos()):
                self.command()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(py.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def draw(self, surface):
        color = self.color
        text = self.text
        border = self.border_color
        self.check_hover()
        if not self.disabled:
            if self.clicked and self.clicked_color:
                color = self.clicked_color
                if self.clicked_font_color:
                    text = self.clicked_text
            elif self.hovered and self.hover_color:
                color = self.hover_color
                if self.hover_font_color:
                    text = self.hover_text
            if self.hovered and not self.clicked:
                border = self.border_hover_color
        else:
            color = self.disabled_color

        if self.radius:
            rad = self.radius
        else:
            rad = 0
        self.round_rect(surface, self.rect, border, rad, 1, color)
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def round_rect(self, surface, rect, color, rad=20, border=0, inside=(0, 0, 0, 0)):
        rect = py.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0, 0
        image = py.Surface(rect.size).convert_alpha()
        image.fill((0, 0, 0, 0))
        self._render_region(image, zeroed_rect, color, rad)
        if border:
            zeroed_rect.inflate_ip(-2 * border, -2 * border)
            self._render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)

    def _render_region(self, image, rect, color, rad):
        corners = rect.inflate(-2 * rad, -2 * rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            py.draw.circle(image, color, getattr(corners, attribute), rad)
        image.fill(color, rect.inflate(-2 * rad, 0))
        image.fill(color, rect.inflate(0, -2 * rad))

    def update(self):
        # for completeness
        pass


def update_mode(mode):
    global app_mode
    # for completeness
    app_mode = mode


# CREATING THE OBJECT OF THE CLASS Screen FOR MENU SCREEN
menuScreen = Screen("Menu Screen")

# CALLING OF THE FUNCTION TO MAKE THE SCREEN FOR THE WINDOW
win = menuScreen.makeCurrentScreen()

# MENU BUTTON
btn_settings = {
    "clicked_font_color": (0, 0, 0),
    "hover_font_color": (205, 195, 100),
    'font': py.font.Font(None, 16),
    'font_color': (255, 255, 255),
    'border_color': (0, 0, 0),
}

plain_btn = Button(rect=(150, 450, 105, 25), command=lambda: print('plain button clicked'), event_trigger=1, text='PLAIN MODE',
             **btn_settings)
game_btn = Button(rect=(150, 550, 105, 25), command=lambda: print('game button clicked'), event_trigger=2, text='GAME MODE',
             **btn_settings)

done = False

bg = py.image.load('images/background.png')
screen = py.display.set_mode((600, 600), py.RESIZABLE)

# MAIN LOOPING
while not done:
    for event in py.event.get():
        if event.type == py.QUIT:
            done = True
        plain_btn.get_event(event)
        game_btn.get_event(event)

    screen.blit(py.transform.scale(bg, (600, 600)), (0, 0))
    plain_btn.draw(screen)
    game_btn.draw(screen)
    py.display.update()

# CLOSE THE PROGRAM
py.quit()



