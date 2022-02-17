import pygame,sys

serverAddr = '127.0.0.1'
if len(sys.argv) == 2:
  serverAddr = sys.argv[1]

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[black] * width for _ in range(height)]
        self.left = 20
        self.top = 20
        self.cell_size = 50
        self.way = 2

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        x, y = self.left, self.top
        for string in self.board:
            for color in string:
                pygame.draw.rect(
                    screen, black, (x, y, self.cell_size, self.cell_size), 1
                )
                if color == 1:
                    pygame.draw.line(
                        screen, blue, (x + 2, y + 2), (x + self.cell_size - 2, y + self.cell_size - 2), 2
                    )
                    pygame.draw.line(
                        screen, blue, (x + self.cell_size - 2, y + 2), (x + 2, y + self.cell_size - 2), 2
                    )
                elif color == 0:
                    pygame.draw.circle(
                        screen, red, (x + self.cell_size / 2, y + self.cell_size / 2), self.cell_size / 2 - 2, 2
                    )
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def get_cell(self, mouse_pos):
        if (self.left < mouse_pos[0] < self.width * self.cell_size + self.left) and (
                self.top < mouse_pos[1] < self.height * self.cell_size + self.top):
            x = (mouse_pos[0] - self.left) // self.cell_size
            y = (mouse_pos[1] - self.top) // self.cell_size
            return x, y
        else:
            return None

    def on_click(self, cell_coords):
        if cell_coords:
            y, x = cell_coords
            if self.board[x][y] == black:
                if self.way % 2 == 0:
                    self.board[x][y] = 1
                else:
                    self.board[x][y] = 0
                self.way += 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_board(self):
        return self.board


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Семестровка')
    colors = red, blue, black = (255, 0, 0), (0, 0, 255), (0, 0, 0)

    board = Board(3, 3)
    win = False
    drawn = False
    font = pygame.font.SysFont("Roboto Condensed", 40)

    running = True
    board.set_view(25, 25, 150)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((255, 255, 255))
        board.render(screen)

        if win:
            lb_win = font.render(f'{win}', True, pygame.Color('green'))
            lb_r = font.render('R - начать новую игру.', True, pygame.Color('green'))
            screen.blit(lb_win, (130, 0))
            screen.blit(lb_r, (110, height - 25))
            win = False

            showing_end = True
            while showing_end:
                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_r]:
                        board = Board(3, 3)
                        board.set_view(25, 25, 150)
                        showing_end = False
                pygame.display.flip()
        elif drawn:
            lb_drawn = font.render(f'{drawn}', True, pygame.Color('green'))
            lb_r = font.render('R - начать новую игру.', True, pygame.Color('green'))
            screen.blit(lb_drawn, (200, 0))
            screen.blit(lb_r, (110, height - 25))
            drawn = False

            showing_end = True
            while showing_end:
                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_r]:
                        board = Board(3, 3)
                        board.set_view(25, 25, 150)
                        showing_end = False
                pygame.display.flip()

        tb = board.get_board()
        if any([all([cell == 1 for cell in string]) for string in tb]):
            win = 'Победил крестик!'
        elif any([all([string[index] == 1 for string in tb]) for index in range(3)]):
            win = 'Победил крестик!'
        elif any([all([cell == 0 for cell in string]) for string in tb]):
            win = 'Победил нолик!'
        elif any([all([string[index] == 0 for string in tb]) for index in range(3)]):
            win = 'Победил нолик!'
        elif tb[0][0] == 1 and tb[1][1] == 1 and tb[2][-1] == 1:
            win = 'Победил крестик!'
        elif tb[0][0] == 0 and tb[1][1] == 0 and tb[2][-1] == 0:
            win = 'Победил нолик!'
        elif tb[0][2] == 1 and tb[1][1] == 1 and tb[2][0] == 1:
            win = 'Победил крестик!'
        elif tb[0][2] == 0 and tb[1][1] == 0 and tb[2][0] == 0:
            win = 'Победил нолик!'
        elif black not in [cell for string in tb for cell in string]:
            drawn = 'Ничья'

        pygame.display.flip()
pygame.quit()