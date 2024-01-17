import pygame
import game_config as config


class GameDialog:

    def __init__(self):
        # Создание окна
        self.__screen = pygame.display.set_mode(config.WINDOW_SIZE)
        # Инициализация библиотеки шрифтов
        pygame.font.init()
        # Шрифт и размер текста
        self.__font = pygame.font.Font(None, 36)
        self.__font_players = pygame.font.Font(None, 30)
        self.__input_font = pygame.font.Font(None, 28)

    def __show_top_5_users(self, top_5_users, x, y):
        i = 1
        for user in top_5_users:
            text_top_5_users = self.__font_players.render(f"{i}.  {user[0]}:  {user[1]}", True, 'white')
            self.__screen.blit(text_top_5_users, (x, y))
            y += 28
            i += 1

    def show_dialog_login(self):
        login = ""
        pygame.display.set_caption("Авторизация")
        start_text = self.__font.render("Играть", True, 'black')
        button_start = start_text.get_rect(midleft=(config.WINDOW_SIZE[0] * 0.5, 160))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(login) != 0:
                            return login
                    elif event.key == pygame.K_BACKSPACE:
                        login = login[:-1]
                    else:
                        login += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_start.collidepoint(mouse_pos):
                        if len(login) != 0:
                            return login

            self.__screen.fill('white')

            # Отрисовка текста и полей ввода
            text = self.__font.render("Авторизация", True, 'black')
            text_rect = text.get_rect(center=(config.WINDOW_SIZE[0] * 0.5, 50))

            login_text = self.__input_font.render("Логин:", True, 'black')
            login_text_rect = login_text.get_rect(center=(config.WINDOW_SIZE[0] * 0.25, 120))

            login_input = self.__input_font.render(login, True, 'black')
            login_input_rect = login_input.get_rect(midleft=(config.WINDOW_SIZE[0] * 0.5, 120))

            self.__screen.blit(text, text_rect)
            self.__screen.blit(login_text, login_text_rect)

            pygame.draw.rect(self.__screen, 'black', login_input_rect, 1)
            self.__screen.blit(login_input, login_input_rect)

            pygame.draw.rect(self.__screen, 'gray', button_start)
            self.__screen.blit(start_text, button_start)

            text_description = self.__font.render("Стань первым в этой беспощадной гонке!", True, 'black')
            text_description_rect = text_description.get_rect(midleft=(config.WINDOW_SIZE[0] * 0.2, 230))
            self.__screen.blit(text_description, text_description_rect)

            pygame.display.flip()

    def show_dialog_game_over(self, top_5_users):
        pygame.display.set_caption("GAME OVER")
        text = self.__font.render("Вы проиграли!", True, 'red')
        text_rect = text.get_rect(center=(config.WINDOW_SIZE[0] * 0.5, config.WINDOW_SIZE[1] * 0.3))

        restart_text = self.__font.render("Начать заново", True, 'white')
        exit_text = self.__font.render("Выйти", True, 'white')

        # Создание кнопок
        button_restart = pygame.Rect(text_rect.left - 10, text_rect.y + 50, 210, 40)
        button_exit = pygame.Rect(text_rect.left - 10, button_restart.y + 50, 210, 40)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_restart.collidepoint(mouse_pos):
                        print("Начать заново")
                        return True
                    elif button_exit.collidepoint(mouse_pos):
                        print("Выйти")
                        return False

            # Отображение диалогового окна с кнопками
            self.__screen.blit(text, text_rect)

            pygame.draw.rect(self.__screen, 'gray', button_restart)
            pygame.draw.rect(self.__screen, 'gray', button_exit)

            self.__screen.blit(restart_text, (text_rect.left + 10, text_rect.y + 60))
            self.__screen.blit(exit_text, (text_rect.left + 10, button_restart.y + 60))

            self.__show_top_5_users(top_5_users, text_rect.left, button_exit.y + 60)

            pygame.display.flip()

    def show_dialog_win_game(self, top_5_users):
        pygame.display.set_caption("WINNER")
        text = self.__font.render("Вы выиграли!", True, 'green')
        text_rect = text.get_rect(center=(config.WINDOW_SIZE[0] * 0.5, config.WINDOW_SIZE[1] * 0.3))

        restart_text = self.__font.render("Продолжить", True, 'white')
        exit_text = self.__font.render("Выйти", True, 'white')

        # Создание кнопок
        button_restart = pygame.Rect(text_rect.left - 10, text_rect.y + 50, 210, 40)
        button_exit = pygame.Rect(text_rect.left - 10, button_restart.y + 50, 210, 40)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_restart.collidepoint(mouse_pos):
                        print("Продолжить")
                        return True
                    elif button_exit.collidepoint(mouse_pos):
                        print("Выйти")
                        return False

            # Отображение диалогового окна с кнопками
            self.__screen.blit(text, text_rect)

            pygame.draw.rect(self.__screen, 'gray', button_restart)
            pygame.draw.rect(self.__screen, 'gray', button_exit)

            self.__screen.blit(restart_text, (text_rect.left + 10, text_rect.y + 60))
            self.__screen.blit(exit_text, (text_rect.left + 10, button_restart.y + 60))

            self.__show_top_5_users(top_5_users, text_rect.left, button_exit.y + 60)

            pygame.display.flip()
