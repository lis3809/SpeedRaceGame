import numpy as np
import pygame

from car import Car
from db_manger import DBManager
from game_dialog import GameDialog


class RunGame:
    WINDOW_RES_X = 800
    WINDOW_RES_Y = 700
    GAME_RES_X = WINDOW_RES_X * 0.5
    GAME_RES_Y = WINDOW_RES_Y

    W_CAR = 70
    H_CAR = 100
    FPS = 60  # Скорость обновления кадров

    # Инициализация библиотеки шрифтов
    pygame.font.init()
    # Шрифт и размер текста
    font = pygame.font.Font(None, 28)

    # Создаем объект класса DBManager, отвечающий за работу с базой данных
    db_manger = DBManager()
    # Создаем объект класса GameDialog
    game_dialog = GameDialog()

    # Запрашиваем имя игрока
    player_name = game_dialog.show_dialog_login()

    current_player_score = 0  # Текущее значение очков игрока
    first_player_score = db_manger.get_best_player_score()  # Лучший результат всей игры
    if first_player_score is None or first_player_score == 0:
        first_player_score = 10
    best_result_current_player = 0  # Лучший результат текущего игрока

    # Сохраняем игрока в базу данных
    if db_manger.save_new_player(player_name):
        print(f"Подключился новый игрок с логином: {player_name}")
    else:
        # Если игрок уже был зарегистрирован, получаем его лучший результат
        best_result_current_player = db_manger.get_user_score(player_name)
        print(best_result_current_player)

    # Создаем объект основной сцены
    scene = pygame.display.set_mode((WINDOW_RES_X, WINDOW_RES_Y))
    scene.fill('#02a831')
    # Создаем объект игрового поля
    game_sc = pygame.Surface((GAME_RES_X, GAME_RES_Y))
    game_sc.fill('#6b6969')

    pygame.display.set_caption("Speed Race Game")

    # Поверхность для машины игрока
    surf_car_player = pygame.Surface((W_CAR, H_CAR), pygame.SRCALPHA)

    clock = pygame.time.Clock()

    # Скорость движения
    speed = 3

    # Список машин соперников
    list_enemy = [
        Car(pygame.Surface((W_CAR, H_CAR), pygame.SRCALPHA), 5, 0,
            "red")]  # x = 5, y = 0 - координаты внутри поверхности
    list_enemy[0].draw()
    # Объект машины игрока
    player_car = Car(surf_car_player, 5, 0, "blue")  # x = 5, y = 0 - координаты внутри поверхности
    player_car.draw()

    # Определяем начальное положение машины игрока
    player_car.dx = GAME_RES_X * 0.5
    player_car.dy = GAME_RES_Y - H_CAR - 10

    def restart_game(self):
        # Создаем объект основной сцены
        self.scene = pygame.display.set_mode((self.WINDOW_RES_X, self.WINDOW_RES_Y))
        self.scene.fill('#02a831')
        # Создаем объект игрового поля
        self.game_sc = pygame.Surface((self.GAME_RES_X, self.GAME_RES_Y))
        self.game_sc.fill('#6b6969')

        pygame.display.set_caption("Speed Race Game")

        # Поверхность для машины игрока
        self.surf_car_player = pygame.Surface((self.W_CAR, self.H_CAR), pygame.SRCALPHA)

        # Скорость движения
        self.speed = 3

        # Список машин соперников
        self.list_enemy = [
            Car(pygame.Surface((self.W_CAR, self.H_CAR), pygame.SRCALPHA), 5, 0,
                "red")]  # x = 5, y = 0 - координаты внутри поверхности
        self.list_enemy[0].draw()
        # Объект машины игрока
        self.player_car = Car(self.surf_car_player, 5, 0, "blue")  # x = 5, y = 0 - координаты внутри поверхности
        self.player_car.draw()

        # Определяем начальное положение машины игрока
        self.player_car.dx = self.GAME_RES_X * 0.5
        self.player_car.dy = self.GAME_RES_Y - self.H_CAR - 10

    def update_score_and_speed(self):
        self.current_player_score += 1
        self.speed += 0.1

    def create_enemy(self):
        i = len(self.list_enemy) - 1
        if self.list_enemy[i].dy > 300:
            enemy_surf = pygame.Surface((self.W_CAR, self.H_CAR), pygame.SRCALPHA)
            color = list(np.random.choice(range(256), size=3))
            enemy = Car(enemy_surf, 5, 0, color)  # x = 5, y = 0 - координаты внутри поверхности
            enemy.draw()
            self.list_enemy.append(enemy)

    def destroy_enemy(self):
        enemy_car = self.list_enemy[0]
        if enemy_car.dy > self.GAME_RES_Y:
            self.list_enemy.remove(enemy_car)
            self.update_score_and_speed()

    def draw_enemy(self):
        self.create_enemy()  # Добавляем новые машины
        for enemy_car in self.list_enemy:
            enemy_car.dy += self.speed
            self.game_sc.blit(enemy_car.game_surf, (enemy_car.dx, enemy_car.dy))
        self.destroy_enemy()  # Удаляем уехавшие машины

    def draw_scene(self):
        # Перерисовываем основную сцену и игровое поле
        self.scene.fill('#02a831')
        self.scene.blit(self.game_sc, (self.WINDOW_RES_X * 0.25, 0))

        # Игровая трасса
        self.game_sc.fill('#6b6969')
        self.game_sc.blit(self.player_car.game_surf, (self.player_car.dx, self.player_car.dy))
        self.draw_enemy()

        # Надпись с именем игрока
        text_name = self.font.render(f"Игрок: {self.player_name}", True, 'black')
        text_name_rect = text_name.get_rect(topleft=(10, 30))
        self.scene.blit(text_name, text_name_rect)

        # Надпись с текущими очками игрока
        text_score = self.font.render(f"Очки: {self.current_player_score}", True, 'black')
        text_score_rect = text_score.get_rect(topleft=(10, 50))
        self.scene.blit(text_score, text_score_rect)

        # Обновляем экран
        pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def check_collision(self):
        rect1 = pygame.Rect(self.list_enemy[0].dx, self.list_enemy[0].dy, self.W_CAR, self.H_CAR)
        rect2 = pygame.Rect(self.player_car.dx, self.player_car.dy, self.W_CAR, self.H_CAR)
        if rect1.colliderect(rect2):
            print("STOP GAME")
            return True
        else:
            return False

    def refresh_and_save_score(self):
        # Храним только лучший результат игрока
        if self.current_player_score > self.best_result_current_player:
            self.best_result_current_player = self.current_player_score
            self.db_manger.update_player_data(self.player_name, self.best_result_current_player)
        self.current_player_score = 0

    def run_race(self, game_is_run):
        # Основной цикл игры
        while game_is_run:
            # Обрабатываем событие закрытия окна
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Сохраняем данные пользователя
                    self.refresh_and_save_score()
                    self.db_manger.close_connection()
                    exit()

            # Обрабатываем события нажатия клавиш
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_car.dx -= self.speed * 2
                # Ограничиваем движение игрока влево
                if self.player_car.dx < 0:
                    self.player_car.dx = 0
            elif keys[pygame.K_RIGHT]:
                self.player_car.dx += self.speed * 2
                # Ограничиваем движение игрока вправо
                if self.player_car.dx > self.GAME_RES_X - self.W_CAR:
                    self.player_car.dx = self.GAME_RES_X - self.W_CAR
            # Отрисовываем всё
            self.draw_scene()
            # Если обнаружено столкновение - выходим из гонки
            if self.check_collision():
                self.refresh_and_save_score()  # Сбрасываем текущее значение набранных очков
                top_5_users = self.db_manger.get_top_5_users()
                print(top_5_users)
                if self.game_dialog.show_dialog_game_over(top_5_users):
                    self.restart_game()
                    print("Начать сначала")
                else:
                    print("Выйти из игры")
                    exit()

            elif self.current_player_score > self.first_player_score:
                self.best_result_current_player = self.current_player_score
                self.db_manger.update_player_data(self.player_name, self.best_result_current_player)
                top_5_users = self.db_manger.get_top_5_users()
                if self.game_dialog.show_dialog_win_game(top_5_users):
                    # Чтобы продолжить игру, немного увеличим лучший результат
                    self.first_player_score += 1000
                    print("Продолжить игру")
                else:
                    self.refresh_and_save_score()  # Сбрасываем текущее значение набранных очков
                    print("Выйти из игры")
                    exit()
