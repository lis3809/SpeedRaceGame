import numpy as np
import pygame

import game_config as config
from car import Car
from db_manger import DBManager
from game_dialog import GameDialog


class RunGame:
    """Базовый класс для запуска игры Speed Race Game"""

    def __init__(self):
        self.__GAME_RES_X = config.WINDOW_SIZE[0] * 0.5
        self.__GAME_RES_Y = config.WINDOW_SIZE[1]
        self.__W_CAR = config.W_CAR
        self.__H_CAR = config.H_CAR
        self.__FPS = config.FPS  # Скорость обновления кадров
        self.__clock = pygame.time.Clock()

        self.__current_player_score = 0  # Текущее значение очков игрока
        # Скорость движения
        self.__speed = 3
        self.__best_result_current_player = 0  # Лучший результат текущего игрока

        # Инициализация библиотеки шрифтов
        pygame.font.init()
        # Шрифт и размер текста
        self.__font = pygame.font.Font(None, 28)

        # Создаем объект класса DBManager, отвечающий за работу с базой данных
        self.__db_manger = DBManager()
        # Создаем объект класса GameDialog
        self.__game_dialog = GameDialog()

        # Запрашиваем имя игрока
        self.__player_name = self.__game_dialog.show_dialog_login()

        self.__first_player_score = self.__db_manger.get_best_player_score()  # Лучший результат всей игры
        if self.__first_player_score is None or self.__first_player_score == 0:
            self.__first_player_score = 10

        # Сохраняем игрока в базу данных
        if self.__db_manger.save_new_player(self.__player_name):
            print(f"Подключился новый игрок с логином: {self.__player_name}")
        else:
            # Если игрок уже был зарегистрирован, получаем его лучший результат
            self.__best_result_current_player = self.__db_manger.get_user_score(self.__player_name)

        # Вызываем метод инициализациии остальных параметров
        self.__init_game()

    def __init_game(self):
        # Создаем объект основной сцены
        self.__scene = pygame.display.set_mode((config.WINDOW_SIZE[0], config.WINDOW_SIZE[1]))
        self.__scene.fill('#02a831')
        # Создаем объект игрового поля
        self.__game_sc = pygame.Surface((self.__GAME_RES_X, self.__GAME_RES_Y))
        self.__game_sc.fill('#6b6969')

        pygame.display.set_caption("Speed Race Game")

        # Поверхность для машины игрока
        self.__surf_car_player = pygame.Surface((self.__W_CAR, self.__H_CAR), pygame.SRCALPHA)

        # Список машин соперников
        self.__list_enemy = [
            Car(pygame.Surface((self.__W_CAR, self.__H_CAR), pygame.SRCALPHA), 5, 0,
                "red")]  # x = 5, y = 0 - координаты внутри поверхности
        self.__list_enemy[0].draw()
        # Объект машины игрока
        self.__player_car = Car(self.__surf_car_player, 5, 0, "blue")  # x = 5, y = 0 - координаты внутри поверхности
        self.__player_car.draw()

        # Определяем начальное положение машины игрока
        self.__player_car.dx = self.__GAME_RES_X * 0.5
        self.__player_car.dy = self.__GAME_RES_Y - self.__H_CAR - 10

    def __restart_game(self):
        # Скорость движения
        self.__speed = 3
        self.__init_game()

    def __update_score_and_speed(self):
        self.__current_player_score += 1
        self.__speed += 0.1

    def __create_enemy(self):
        i = len(self.__list_enemy) - 1
        if self.__list_enemy[i].dy > 300:
            enemy_surf = pygame.Surface((self.__W_CAR, self.__H_CAR), pygame.SRCALPHA)
            color = list(np.random.choice(range(256), size=3))
            enemy = Car(enemy_surf, 5, 0, color)  # x = 5, y = 0 - координаты внутри поверхности
            enemy.draw()
            self.__list_enemy.append(enemy)

    def __destroy_enemy(self):
        enemy_car = self.__list_enemy[0]
        if enemy_car.dy > self.__GAME_RES_Y:
            self.__list_enemy.remove(enemy_car)
            self.__update_score_and_speed()

    def __draw_enemy(self):
        self.__create_enemy()  # Добавляем новые машины
        for enemy_car in self.__list_enemy:
            enemy_car.dy += self.__speed
            self.__game_sc.blit(enemy_car.game_surf, (enemy_car.dx, enemy_car.dy))
        self.__destroy_enemy()  # Удаляем уехавшие машины

    def __draw_scene(self):
        # Перерисовываем основную сцену и игровое поле
        self.__scene.fill('#02a831')
        self.__scene.blit(self.__game_sc, (config.WINDOW_SIZE[0] * 0.25, 0))

        # Игровая трасса
        self.__game_sc.fill('#6b6969')
        self.__game_sc.blit(self.__player_car.game_surf, (self.__player_car.dx, self.__player_car.dy))
        self.__draw_enemy()

        # Надпись с именем игрока
        text_name = self.__font.render(f"Игрок: {self.__player_name}", True, 'black')
        text_name_rect = text_name.get_rect(topleft=(10, 30))
        self.__scene.blit(text_name, text_name_rect)

        # Надпись с текущими очками игрока
        text_score = self.__font.render(f"Очки: {self.__current_player_score}", True, 'black')
        text_score_rect = text_score.get_rect(topleft=(10, 50))
        self.__scene.blit(text_score, text_score_rect)

        # Обновляем экран
        pygame.display.update()
        pygame.display.flip()
        self.__clock.tick(self.__FPS)

    def __check_collision(self):
        rect1 = pygame.Rect(self.__list_enemy[0].dx, self.__list_enemy[0].dy, self.__W_CAR, self.__H_CAR)
        rect2 = pygame.Rect(self.__player_car.dx, self.__player_car.dy, self.__W_CAR, self.__H_CAR)
        if rect1.colliderect(rect2):
            print("STOP GAME")
            return True
        else:
            return False

    def __refresh_and_save_score(self):
        # Храним только лучший результат игрока
        if self.__current_player_score > self.__best_result_current_player:
            self.__best_result_current_player = self.__current_player_score
            self.__db_manger.update_player_data(self.__player_name, self.__best_result_current_player)
        self.__current_player_score = 0

    def run_race(self, game_is_run):
        # Основной цикл игры
        while game_is_run:
            # Обрабатываем событие закрытия окна
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Сохраняем данные пользователя
                    self.__refresh_and_save_score()
                    self.__db_manger.close_connection()
                    exit()

            # Обрабатываем события нажатия клавиш
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.__player_car.dx -= self.__speed * 2
                # Ограничиваем движение игрока влево
                if self.__player_car.dx < 0:
                    self.__player_car.dx = 0
            elif keys[pygame.K_RIGHT]:
                self.__player_car.dx += self.__speed * 2
                # Ограничиваем движение игрока вправо
                if self.__player_car.dx > self.__GAME_RES_X - self.__W_CAR:
                    self.__player_car.dx = self.__GAME_RES_X - self.__W_CAR
            # Отрисовываем всё
            self.__draw_scene()
            # Если обнаружено столкновение - выходим из гонки
            if self.__check_collision():
                self.__refresh_and_save_score()  # Сбрасываем текущее значение набранных очков
                top_5_users = self.__db_manger.get_top_5_users()
                if self.__game_dialog.show_dialog_game_over(top_5_users):
                    self.__restart_game()
                else:
                    exit()

            elif self.__current_player_score > self.__first_player_score:
                self.__best_result_current_player = self.__current_player_score
                self.__db_manger.update_player_data(self.__player_name, self.__best_result_current_player)
                top_5_users = self.__db_manger.get_top_5_users()
                if self.__game_dialog.show_dialog_win_game(top_5_users):
                    # Чтобы продолжить игру, немного увеличим лучший результат
                    self.__first_player_score += 1000
                else:
                    self.__refresh_and_save_score()  # Сбрасываем текущее значение набранных очков
                    exit()
