# Класс машины игрока
import random
import pygame


class Car:
    def __init__(self, game_surf, x, y, color):
        self.game_surf = game_surf
        self.x = x
        self.y = y
        self.color = color
        self.dx = random.randint(0, 330)

    w_car = 60
    h_car = 100

    dy = -100

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
