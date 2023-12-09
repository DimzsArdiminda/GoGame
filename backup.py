import pygame
from sys import exit

BACKGROUND = 'images/ramin2.jpg'  # Nama file gambar latar belakang
BOARD_SIZE = (1000, 820)  # Ukuran papan
WHITE = (255, 255, 255)  # Warna putih
BLACK = (0, 0, 0)  # Warna hitam
JENIS_FONT = 'font/monofonto rg.otf'  # Jenis font



class Stone(object):
    def __init__(self, board, point, color):
        """Create, initialize, and draw a stone."""
        self.board = board
        self.point = point
        self.color = color
        self.group = self.find_group()
        self.coords = (5 + self.point[0] * 40, 5 + self.point[1] * 40)
        self.draw()

    def draw(self):
        """Draw the stone as a circle."""
        pygame.draw.circle(screen, self.color, self.coords, 20, 0)
        pygame.display.update()

    def remove(self):
        """Remove the stone from the board."""
        blit_coords = (self.coords[0] - 20, self.coords[1] - 20)
        area_rect = pygame.Rect(blit_coords, (40, 40))
        screen.blit(background, blit_coords, area_rect)
        pygame.display.update()
        self.group.stones.remove(self)
        del self

    @property
    def neighbors(self):
        """Return a list of neighboring points."""
        neighboring = [(self.point[0] - 1, self.point[1]),
                       (self.point[0] + 1, self.point[1]),
                       (self.point[0], self.point[1] - 1),
                       (self.point[0], self.point[1] + 1)]
        for point in neighboring:
            if not 0 < point[0] < 20 or not 0 < point[1] < 20:
                neighboring.remove(point)
        return neighboring

    @property
    def liberties(self):
        """Find and return the liberties of the stone."""
        liberties = self.neighbors
        stones = self.board.search(points=self.neighbors)
        for stone in stones:
            liberties.remove(stone.point)
        return liberties

    def find_group(self):
        """Find or create a group for the stone."""
        groups = []
        stones = self.board.search(points=self.neighbors)
        for stone in stones:
            if stone.color == self.color and stone.group not in groups:
                groups.append(stone.group)
        if not groups:
            group = Group(self.board, self)
            return group
        else:
            if len(groups) > 1:
                for group in groups[1:]:
                    groups[0].merge(group)
            groups[0].stones.append(self)
            return groups[0]

    def __str__(self):
        """Return the location of the stone, e.g., 'D17'."""
        return 'ABCDEFGHJKLMNOPQRST'[self.point[0]-1] + str(20-(self.point[1]))

class Group(object):
    def __init__(self, board, stone):
        """Create and initialize a new group."""
        self.board = board
        self.board.groups.append(self)
        self.stones = [stone]
        self.liberties = None

    def merge(self, group):
        """Merge two groups."""
        for stone in group.stones:
            stone.group = self
            self.stones.append(stone)
        self.board.groups.remove(group)
        del group

    def remove(self):
        """Remove the entire group."""
        while self.stones:
            self.stones[0].remove()
        self.board.groups.remove(self)
        del self

    def update_liberties(self):
        """Update the group's liberties."""
        liberties = []
        for stone in self.stones:
            for liberty in stone.liberties:
                liberties.append(liberty)
        self.liberties = set(liberties)
        if len(self.liberties) == 0:
            self.remove()

    def __str__(self):
        """Return a list of the group's stones as a string."""
        return str([str(stone) for stone in self.stones])

class Board(object):
    def __init__(self):
        """Create, initialize, and draw an empty board."""
        self.groups = []
        self.next = BLACK
        self.outline = pygame.Rect(45, 45, 720, 720)
        self.black_score = 0
        self.white_score = 0
        self.draw()

    def calculate_score(self):
        """Calculate the score of each player."""
        self.black_score = 0
        self.white_score = 0

        for group in self.groups:
            for stone in group.stones:
                if stone.color == BLACK:
                    self.black_score += 1
                elif stone.color == WHITE:
                    self.white_score += 1

    def search(self, point=None, points=[]):
        """Search the board for a stone."""
        stones = []
        for group in self.groups:
            for stone in group.stones:
                if stone.point == point and not points:
                    return stone
                if stone.point in points:
                    stones.append(stone)
        return stones

    def turn(self):
        """Keep track of the turn by flipping between BLACK and WHITE."""
        if self.next == BLACK:
            self.next = WHITE
            return BLACK
        else:
            self.next = BLACK
            return WHITE

    def draw(self):
        """Draw the board to the background and blit it to the screen."""
        pygame.draw.rect(background, BLACK, self.outline, 3)
        self.outline.inflate_ip(20, 20)
        for i in range(18):
            for j in range(18):
                rect = pygame.Rect(45 + (40 * i), 45 + (40 * j), 40, 40)
                pygame.draw.rect(background, BLACK, rect, 1)
        for i in range(3):
            for j in range(3):
                coords = (165 + (240 * i), 165 + (240 * j))
                pygame.draw.circle(background, BLACK, coords, 5, 0)
        screen.blit(background, (0, 0))

    def update_liberties(self, added_stone=None):
        """Updates the liberties of the entire board, group by group."""
        for group in self.groups:
            if added_stone:
                if group == added_stone.group:
                    continue
            group.update_liberties()
        if added_stone:
            added_stone.group.update_liberties()

def draw_score(board):
    """Draw the score on the right side of the board."""
    font = pygame.font.Font(JENIS_FONT, 25)
    
        # Hapus area skor sebelum menggambar yang baru
    screen.fill(WHITE, (780, 100, 200, 100))
    
    black_text = font.render(f"Black: {board.black_score}", True, BLACK)
    white_text = font.render(f"White: {board.white_score}", True, BLACK)
    screen.blit(black_text, (780, 100))
    screen.blit(white_text, (780, 150))
    pygame.display.update()

class Button(object):
    def __init__(self, text, position, action):
        self.text = text
        self.position = position
        self.action = action
        self.font = pygame.font.Font(JENIS_FONT, 25)
        self.rect = pygame.Rect(position, (200, 50))
        self.color = WHITE
        self.draw()

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text = self.font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

def toggle_pause():
    global is_game_running
    is_game_running = not is_game_running

def calculate_and_draw_score():
    board.calculate_score()
    draw_score(board)

def main():
    global is_game_running
    is_game_running = True
    pause_button = Button("Pause", (780, 250), toggle_pause)

    while True:
        pygame.time.wait(250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            pause_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and is_game_running:
                if event.button == 1 and board.outline.collidepoint(event.pos):
                    x = int(round(((event.pos[0] - 5) / 40.0), 0))
                    y = int(round(((event.pos[1] - 5) / 40.0), 0))
                    stone = board.search(point=(x, y))
                    if stone:
                        stone.remove()
                    else:
                        added_stone = Stone(board, (x, y), board.turn())
                    board.update_liberties(added_stone)
                    # Update and draw the score in real-time
                    board.calculate_score()
                    draw_score(board)

        if is_game_running:
            notification_text = ""
        else:
            notification_text = "Game Paused"

        # Hapus teks yang sudah ada sebelum menggambar yang baru
        screen.fill(WHITE, (780, 200, 200, 50))

        small_font = pygame.font.Font(JENIS_FONT, 24)
        notification_surface = small_font.render(notification_text, True, BLACK)
        screen.blit(notification_surface, (780, 200))

        pygame.display.update()  # Tambahkan pembaruan layar di sini

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Go Game Board')
    screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
    background = pygame.image.load(BACKGROUND).convert()
    board = Board()
    main()