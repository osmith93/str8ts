import pygame


class UI:
    black = (0, 0, 0)
    white = (255, 255, 255)
    grid_color = (0, 0, 0)
    background_color = white

    def __init__(self, game, solver, width=900, height=900):
        pygame.init()
        self._running = True
        self._display_surface = None
        self.size = self.width, self.height = width, height
        self.game = game
        self.solver = solver
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('fonts/Product Sans Regular.ttf', 40)
        self.small_font = pygame.font.Font('fonts/Product Sans Regular.ttf', 15)
        self.grid_x = int(width / 10)
        self.grid_y = int(height / 10)
        self.grid_width = int(0.8 * width)
        self.grid_height = int(0.8 * height)

    def draw_rect(self, x, y, width, height, color):
        pygame.draw.rect(self._display_surface, color, [x, y, width, height])

    def fill_cell(self, cell, color=(0, 0, 0)):
        x_center, y_center = self.get_center(cell)
        width = self.grid_width // self.game.size
        height = self.grid_height // self.game.size
        x = x_center - height / 2
        y = y_center - width / 2
        self.draw_rect(x, y, width, height, color)

    def draw_text_centered_at(self, x, y, text, color, font):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self._display_surface.blit(text_surface, text_rect)

    def draw_grid(self):
        y_start = self.grid_y
        y_end = self.grid_y + self.grid_width
        x_start = self.grid_x
        x_end = self.grid_x + self.grid_height
        h = self.grid_height
        w = self.grid_width

        for i in range(self.game.size + 1):
            x_current = x_start + i * h / self.game.size
            pygame.draw.line(self._display_surface, UI.grid_color, (x_current, y_start), (x_current, y_end), width=3)
        for i in range(self.game.size + 1):
            y_current = y_start + i * w / self.game.size
            pygame.draw.line(self._display_surface, UI.grid_color, (x_start, y_current), (x_end, y_current), width=3)

    def draw_board(self):
        for cell in self.game.board.all_cells:
            pos = cell.pos
            if cell.is_blocked:
                self.fill_cell(pos)
                text_color = UI.white
            else:
                text_color = UI.black
            if not cell.is_empty:
                x_center, y_center = self.get_center(pos)
                self.draw_text_centered_at(x_center, y_center, str(cell.value), text_color, font=self.font)
            elif not cell.is_blocked:
                for guess in cell.guesses:
                    center_x, center_y = self.get_guess_center(pos, guess)
                    self.draw_text_centered_at(center_x, center_y, str(guess), text_color, font=self.small_font)

    def get_guess_center(self, cell, guess):
        cell_center_x, cell_center_y = self.get_center(cell)
        col = (guess - 1) % 3 - 1
        row = (guess - 1) // 3 - 1
        cell_center_x = cell_center_x + col * self.grid_width / (3 * self.game.size)
        cell_center_y = cell_center_y + row * self.grid_height / (3 * self.game.size)
        return cell_center_x, cell_center_y

    def get_center(self, cell):
        x, y = cell
        cell_width = self.grid_width / self.game.size
        cell_height = self.grid_height / self.game.size
        x_center = x * cell_width + cell_width / 2 + self.grid_x
        y_center = y * cell_height + cell_height / 2 + self.grid_y
        return x_center, y_center

    def on_init(self):
        self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Str8ts Solver")
        self._display_surface.fill(UI.white)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.solver.next_step()

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surface.fill(UI.background_color)
        self.draw_grid()
        self.draw_board()
        pygame.display.update()
        self.clock.tick(10)
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
