#-----------------------------------------------------------------------------#
#                                                                             #
#                         PyGame - Hex Card Generator                         #
#                            by. Gede Ria Ghosalya                            #
#                                                                             #
#-----------------------------------------------------------------------------#

import os
import sys
import math
import random
import pygame

from tcgen.constants import *
from tcgen.dataloader import FactionData, BossData, CardData

def split_list(seq, n=8):
    if len(seq) <= n:
        return seq, []
    else:
        return seq[:n], seq[n:]




class CardGenerator:
    def __init__(self):
        self._initialize_pygame()
        self._initialize_fonts()  # must be after initializing pygame
        
        self.pages = 0
        self.layouts = {
            layout.split(".")[0].lower(): pygame.image.load("layout/{}".format(layout))
            for layout in os.listdir("./layout/")
            if layout.split(".")[-1] in ("png", "jpg")
        }

    def _initialize_fonts(self):
        self.fonts = {
            NAME: pygame.font.Font('freesansbold.ttf', 40),
            FACTION: pygame.font.Font('freesansbold.ttf', 26),
            EFFECT: pygame.font.Font('freesansbold.ttf', 22),
            FLAVOR: pygame.font.Font('freesansbold.ttf', 20),
        }
        self.fonts[FACTION].set_italic(True)
        self.fonts[FLAVOR].set_italic(True)
        self.font_blank = pygame.font.Font('freesansbold.ttf', 10)

    def _initialize_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(
            (windowWidth, windowHeight)
        )
        self.metasurf = self.surface.convert_alpha()
        self.surface.fill(BGCOLOR)
        pygame.display.set_caption("Hex Card Generator")

    def draw_page(self, cards):
        """
        Draw cards to fill the entire screen.

        :param cards: A list of at most 8 CardData objects.
        """
        for i in range(len(cards)):
            self.draw_card(
                cards[i],
                position = (i % 4, i // 4)
            )

        self.surface.blit(self.metasurf, (0, 0))
        pygame.image.save(self.surface, "res/display{}.jpg".format(self.pages))
        pygame.display.update()
        self.clock.tick(FPS)
        self.pages += 1

    def draw_card(self, card, position):
        """
        Draw a card onto the display.

        :param card_data: A CardData object.
        :param position: An (X, Y) tuple indicating the position of the card
            relative to the screen grids. X must take an integer between 0 to
            3, while Y can only be 0 or 1. (For 4x2 display).
        """
        start_x = position[0] * (windowWidth / 4)
        start_y = position[1] * (windowHeight / 2)

        self.surface.blit(
            self.layouts[card.layout],
            (start_x, start_y)
        )

        name_position = (start_x + cardWidth // 2, start_y + 90)
        self.draw_text(NAME, name_position, card.name)

        faction_position = (start_x + cardWidth // 2, start_y + 150)
        self.draw_text(FACTION, faction_position, card.faction)

        # TODO: draw image
        try:
            front_img = pygame.transform.scale(
                pygame.image.load(card.image),
                (786, 600)
            )
            self.surface.blit(front_img, (start_x+47, start_y+170))
        except:
            pass

        i = 0
        blanks = 0
        for text in card.effect_strings:
            text_position = (start_x + 50, start_y + 800 + 33*i - 15*blanks)
            self.draw_text(EFFECT, text_position, text)
            if text == "": blanks += 1
            i += 1

        i = 0
        for text in card.flavor_strings[::-1]:
            text_position = (start_x + 800, start_y + 1180 - 32*i)
            self.draw_text(FLAVOR, text_position, text)
            i += 1

    def draw_text(self, field, center, text):
        text_color = BLACK if field in (NAME, EFFECT) else GREY
        text_to = self.fonts[field].render(text, True, text_color)
        text_ro = text_to.get_rect()
        if field == EFFECT:
            text_ro.topleft = center
        elif field == FLAVOR:
            text_ro.bottomright = center
        else:
            text_ro.center = center
        self.metasurf.blit(text_to, text_ro)

    def generate(self):
        os.makedirs("./res/", exist_ok=True)
        bosses = []
        for faction in os.listdir("./data/"):
            faction_data = FactionData.load_data(faction)
            cards = faction_data.get_card_instances()
            if faction_data.boss is not None:
                bosses.append(faction_data.boss)

            while len(cards) > 0:
                self.surface.fill(BGCOLOR)
                self.metasurf.fill(TRANSPARENT)
                cards_to_draw, cards = split_list(cards, n=8)
                self.draw_page(cards_to_draw)

        # bosses
        while len(bosses) > 0:
            self.surface.fill(BGCOLOR)
            self.metasurf.fill(TRANSPARENT)
            cards_to_draw, bosses = split_list(bosses, n=8)
            self.draw_page(cards_to_draw)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    CardGenerator().generate()