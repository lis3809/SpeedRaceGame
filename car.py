# Класс машины игрока
import random
import pygame

import game_config as config


class Car:

    def __init__(self, game_surf, x, y, color):
        self.game_surf = game_surf
        self.x = x
        self.y = y
        self.color = color
        self.dx = random.randint(0, config.GAME_RES_X - config.W_CAR)
        self.w_car = config.W_CAR - 10
        self.h_car = config.H_CAR
        self.dy = -config.H_CAR

    def draw(self):
        # Рисуем кузов
        pygame.draw.rect(self.game_surf,
                         self.color,
                         (self.x, self.y, self.w_car, self.h_car))

        # Рисуем колеса
        pygame.draw.rect(self.game_surf,
                         "black",
                         (self.x - 5, self.y + 10, 10, 25))
        pygame.draw.rect(self.game_surf,
                         "black",
                         (self.x + self.w_car - 5, self.y + 10, 10, 25))
        pygame.draw.rect(self.game_surf,
                         "black",
                         (self.x - 5, self.y + self.h_car - 35, 10, 25))
        pygame.draw.rect(self.game_surf,
                         "black",
                         (self.x + self.w_car - 5, self.y + self.h_car - 35, 10, 25))
