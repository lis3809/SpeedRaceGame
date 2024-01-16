import pygame


class GameDialog:
    # Размеры окна
    window_size = (800, 700)

    # Цвета
    black = (0, 0, 0)
    green = (0, 255, 119)
    white = (255, 255, 255)
    gray = (150, 150, 150)

    # Создание окна
    screen = pygame.display.set_mode(window_size)

    # Инициализация библиотеки шрифтов
    pygame.font.init()

    # Шрифт и размер текста
    font = pygame.font.Font(None, 36)
    font_players = pygame.font.Font(None, 30)
    input_font = pygame.font.Font(None, 28)

    def show_top_5_users(self, top_5_users, x, y):

        i = 1
        for user in top_5_users:
            texttop_5_users = self.font_players.render(f"{i}.  {user[0]}:  {user[1]}", True, self.white)
            self.screen.blit(texttop_5_users, (x, y))
            y += 28
            i += 1


    def show_dialog_login(self):
        login = ""
        pygame.display.set_caption("Авторизация")

        start_text = self.font.render("Играть", True, self.black)
        button_start = start_text.get_rect(midleft=(self.window_size[0] * 0.5, 160))

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

            self.screen.fill(self.white)

            # Отрисовка текста и полей ввода
            text = self.font.render("Авторизация", True, self.black)
            text_rect = text.get_rect(center=(self.window_size[0] * 0.5, 50))

            login_text = self.input_font.render("Логин:", True, self.black)
            login_text_rect = login_text.get_rect(center=(self.window_size[0] * 0.25, 120))

            login_input = self.input_font.render(login, True, self.black)
            login_input_rect = login_input.get_rect(midleft=(self.window_size[0] * 0.5, 120))

            self.screen.blit(text, text_rect)
            self.screen.blit(login_text, login_text_rect)

            pygame.draw.rect(self.screen, self.black, login_input_rect, 1)
            self.screen.blit(login_input, login_input_rect)

            pygame.draw.rect(self.screen, self.gray, button_start)
            self.screen.blit(start_text, button_start)

            text_description = self.font.render("Стань первым в этой беспощадной гонке!", True, self.black)
            text_description_rect = text_description.get_rect(midleft=(self.window_size[0] * 0.2, 230))
            self.screen.blit(text_description, text_description_rect)

            pygame.display.flip()

    def show_dialog_game_over(self, top_5_users):
        pygame.display.set_caption("GAME OVER")
        text = self.font.render("Вы проиграли!", True, 'red')
        text_rect = text.get_rect(center=(self.window_size[0] * 0.5, self.window_size[1] * 0.3))

        restart_text = self.font.render("Начать заново", True, self.white)
        exit_text = self.font.render("Выйти", True, self.white)

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
            self.screen.blit(text, text_rect)

            pygame.draw.rect(self.screen, self.gray, button_restart)
            pygame.draw.rect(self.screen, self.gray, button_exit)

            self.screen.blit(restart_text, (text_rect.left + 10, text_rect.y + 60))
            self.screen.blit(exit_text, (text_rect.left + 10, button_restart.y + 60))

            self.show_top_5_users(top_5_users, text_rect.left, button_exit.y + 60)

            pygame.display.flip()

    def show_dialog_win_game(self, top_5_users):
        pygame.display.set_caption("WINNER")
        text = self.font.render("Вы выиграли!", True, 'green')
        text_rect = text.get_rect(center=(self.window_size[0] * 0.5, self.window_size[1] * 0.3))

        restart_text = self.font.render("Продолжить", True, self.white)
        exit_text = self.font.render("Выйти", True, self.white)

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
            self.screen.blit(text, text_rect)

            pygame.draw.rect(self.screen, self.gray, button_restart)
            pygame.draw.rect(self.screen, self.gray, button_exit)

            self.screen.blit(restart_text, (text_rect.left + 10, text_rect.y + 60))
            self.screen.blit(exit_text, (text_rect.left + 10, button_restart.y + 60))

            self.show_top_5_users(top_5_users, text_rect.left, button_exit.y + 60)

            pygame.display.flip()
