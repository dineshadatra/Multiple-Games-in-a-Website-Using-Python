# Importing the required modules
import pygame  # pip install pygame
import random
import sys

# Constants
size = 4  # The size of the grid (4x4)
win = 2048  # The target value to win the game
background_colour = (187, 173, 160)  # Background color of the grid
tile_colours = {  # Colors for each tile value
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
font_colour = (119, 110, 101)  # Color of the text
font = 'freesansbold.ttf'  # Font for the text

class Game2048:
    def __init__(self):
        self.size = size
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.board = [[0] * self.size for l in range(self.size)]  # Initialize the board with zeros
        self.spawn()  # Spawn the first tile
        self.spawn()  # Spawn the second tile
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set the window to fullscreen
        self.screen_width, self.screen_height = self.screen.get_size()  # Get screen size
        self.grid_size = min(self.screen_width, self.screen_height) * 0.8  # Grid size is 80% of the smaller screen dimension
        self.tile_size = self.grid_size // self.size  # Size of each tile
        self.grid_gap = self.tile_size * 0.1  # Gap between the tiles is 10% of tile size
        self.font = pygame.font.Font(font, int(self.tile_size // 3))  # Set the font size for tiles
        self.small_font = pygame.font.Font(font, int(self.tile_size // 6))  # Set the font size for score and messages
        pygame.display.set_caption('2048 Game')  # Set the window title

    def reset(self):
        self.score = 0
        self.board = [[0] * self.size for m in range(self.size)]
        self.spawn()
        self.spawn()

    def spawn(self):
        new_value = 4 if random.random() > 0.9 else 2  # 10% chance to spawn a 4, otherwise spawn a 2
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)  # Choose a random empty cell
            self.board[i][j] = new_value  # Place the new value in the chosen cell

    def move(self, direction):
        def move_row_left(row):
            new_row = [i for i in row if i != 0]  # Remove zeros from the row
            while len(new_row) < self.size:
                new_row.append(0)  # Fill the rest of the row with zeros
            for i in range(len(new_row) - 1):
                if new_row[i] == new_row[i + 1]:  # Combine adjacent tiles with the same value
                    new_row[i] *= 2  # Double the value
                    new_row[i + 1] = 0  # Empty the combined tile
                    self.score += new_row[i]  # Add the value to the score
            new_row = [i for i in new_row if i != 0]  # Remove zeros again
            while len(new_row) < self.size:
                new_row.append(0)  # Fill the rest of the row with zeros
            return new_row

        # Define movement directions and their corresponding transformations
        moves = {
            'Left': lambda board: [move_row_left(row) for row in board],
            'Right': lambda board: [move_row_left(row[::-1])[::-1] for row in board],
            'Up': lambda board: list(map(list, zip(*[move_row_left(row) for row in zip(*board)]))),
            'Down': lambda board: list(map(list, zip(*[move_row_left(row[::-1])[::-1] for row in zip(*board)]))),
        }

        if direction in moves:
            if self.can_move(direction):  # Check if the move is possible
                self.board = moves[direction](self.board)  # Apply the move
                self.spawn()
                return True
        return False

    def can_move(self, direction):
        def can_move_row_left(row):
            for i in range(len(row) - 1):
                if row[i] == 0 and row[i + 1] != 0:  # Check if tiles can be moved
                    return True
                if row[i] != 0 and row[i] == row[i + 1]:  # Check if tiles can be combined
                    return True
            return False

        # Define movement directions and their corresponding checks
        checks = {
            'Left': lambda board: any(can_move_row_left(row) for row in board),
            'Right': lambda board: checks['Left']([row[::-1] for row in board]),
            'Up': lambda board: checks['Left'](list(map(list, zip(*board)))),
            'Down': lambda board: checks['Right'](list(map(list, zip(*board)))),
        }

        return checks[direction](self.board)

    def is_win(self):
        return any(any(cell >= self.win_value for cell in row) for row in self.board)  # Check if the player has won

    def is_gameover(self):
        return not any(self.can_move(move) for move in ['Up', 'Down', 'Left', 'Right'])  # Check if no moves are possible

    def draw(self, game_over=False, game_won=False):
        self.screen.fill(background_colour)
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                rect = pygame.Rect(j * (self.tile_size + self.grid_gap) + self.grid_gap,
                                   i * (self.tile_size + self.grid_gap) + self.grid_gap + 50,
                                   self.tile_size, self.tile_size)  # Calculate the position and size of each tile
                pygame.draw.rect(self.screen, tile_colours[value], rect)  # Draw the tile
                if value:
                    text_surface = self.font.render(str(value), True, font_colour)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)

        # Draw the score and highscore
        score_text = self.small_font.render(f'Score: {self.score}', True, font_colour)
        self.screen.blit(score_text, (10, 10))
        highscore_text = self.small_font.render(f'Highscore: {self.highscore}', True, font_colour)
        self.screen.blit(highscore_text, (10, 30))

        # Show end messages if the game is over or won
        if game_over:
            self.draw_end_message('Game Over! Press Enter to Restart.')
        elif game_won:
            self.draw_end_message('You Win! Press Enter to Restart.')

        pygame.display.update()  # Update the display

    def draw_end_message(self, message):
        message_surface = self.small_font.render(message, True, font_colour)
        message_rect = message_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(message_surface, message_rect)

def main():
    game = Game2048()
    running = True
    game_over = False
    game_won = False

    while running:
        game.draw(game_over, game_won)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle window close
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_over or game_won:
                    if event.key == pygame.K_RETURN:
                        game.reset()
                        game_over = False
                        game_won = False
                elif event.key == pygame.K_r:
                    game.reset()
                    game_over = False
                    game_won = False
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_UP:
                    game.move('Up')
                elif event.key == pygame.K_DOWN:
                    game.move('Down')
                elif event.key == pygame.K_LEFT:
                    game.move('Left')
                elif event.key == pygame.K_RIGHT:
                    game.move('Right')

        if game.is_win():
            game_won = True
        elif game.is_gameover():
            game_over = True

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
