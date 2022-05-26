import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect

import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect


def create_win_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont(None, font_size)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class CreateScreen(Sprite):
    def __init__(self, font_size, text_rgb, bg_rgb):
        super().__init__()
        self.text = ["2 PLAYER", "3 PLAYER", " 4 PLAYER", ]

        self.state = 0
        self.font_size = font_size
        self.text_rgb = text_rgb
        self.bg_rgb = bg_rgb

        default_image_twoplayer = create_win_text(
            self.text[0], font_size, (0, 0, 0), (0, 255, 0))
        default_image_threeplayer = create_win_text(
            self.text[1], font_size, text_rgb, bg_rgb)
        default_image_fourplayer = create_win_text(
            self.text[2], font_size, text_rgb, bg_rgb)

        self.image = [default_image_twoplayer,
                      default_image_threeplayer, default_image_fourplayer]
        default_image_create = create_win_text(
            "Confrim", font_size, text_rgb, bg_rgb)

        self.create = default_image_create

    def get_countplayer(self):
        return self.image

    def update(self, vector):
        temp = self.state
        if vector:
            if self.state >= 2:
                self.state = 0
            else:
                self.state += 1
        else:
            if self.state <= 0:
                self.state = 2
            else:
                self.state -= 1
        default_image_hover = create_win_text(
            self.text[self.state], self.font_size, (0, 0, 0), (0, 255, 0))
        default_image_goback = create_win_text(
            self.text[temp], self.font_size, self.text_rgb, self.bg_rgb)
        self.image[self.state] = default_image_hover
        self.image[temp] = default_image_goback

    def get_state(self):
        return self.state

    def draw(self, win):

        count_x = 0
        spaceSprites = pygame.image.load(
            r'.\space_bg.jpg')
        spaceSprites = pygame.transform.smoothscale(spaceSprites, (500, 500))
        win.blit(spaceSprites, (0, 0))
        for my_image in self.image:
            win.blit(my_image, (25+count_x, 200))
            count_x += 150
        win.blit(self.create, (388, 450))

    def get_confrim(self):
        return (self.create.get_rect())
