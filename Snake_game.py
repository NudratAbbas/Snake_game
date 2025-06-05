import tkinter as tk
import random

# Game Constants
GAME_WIDTH = 600
GAME_HEIGHT = 400
SNAKE_ITEM_SIZE = 20
SNAKE_SPEED = 100  # milliseconds
INITIAL_SNAKE_LENGTH = 3

# Colors
BACKGROUND_COLOR = "#1e1e1e"
SNAKE_COLOR = "#00ff00"
FOOD_COLOR = "#ff0000"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game 🐍")
        self.canvas = tk.Canvas(root, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        # Direction tracking
        self.direction = 'Right'
        self.running = True

        # Snake and food
        self.snake = []
        self.food = None

        self.create_snake()
        self.create_food()
        self.bind_keys()
        self.move_snake()

    def create_snake(self):
        """Initialize the snake with segments"""
        for i in range(INITIAL_SNAKE_LENGTH):
            x = 100 - i * SNAKE_ITEM_SIZE
            y = 100
            segment = self.canvas.create_rectangle(x, y, x + SNAKE_ITEM_SIZE, y + SNAKE_ITEM_SIZE, fill=SNAKE_COLOR)
            self.snake.append(segment)

    def create_food(self):
        """Spawn food at a random location"""
        x = random.randint(0, (GAME_WIDTH - SNAKE_ITEM_SIZE) // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
        y = random.randint(0, (GAME_HEIGHT - SNAKE_ITEM_SIZE) // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
        if self.food:
            self.canvas.delete(self.food)
        self.food = self.canvas.create_oval(x, y, x + SNAKE_ITEM_SIZE, y + SNAKE_ITEM_SIZE, fill=FOOD_COLOR)

    def bind_keys(self):
        """Bind arrow keys to control snake direction"""
        self.root.bind("<Left>", lambda event: self.change_direction('Left'))
        self.root.bind("<Right>", lambda event: self.change_direction('Right'))
        self.root.bind("<Up>", lambda event: self.change_direction('Up'))
        self.root.bind("<Down>", lambda event: self.change_direction('Down'))

    def change_direction(self, new_direction):
        """Change snake direction, prevent reverse"""
        opposites = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
        if self.direction != opposites.get(new_direction):
            self.direction = new_direction

    def move_snake(self):
        """Move the snake in the current direction"""
        if not self.running:
            return

        head_coords = self.canvas.coords(self.snake[0])
        x1, y1, x2, y2 = head_coords

        if self.direction == 'Left':
            x1 -= SNAKE_ITEM_SIZE
            x2 -= SNAKE_ITEM_SIZE
        elif self.direction == 'Right':
            x1 += SNAKE_ITEM_SIZE
            x2 += SNAKE_ITEM_SIZE
        elif self.direction == 'Up':
            y1 -= SNAKE_ITEM_SIZE
            y2 -= SNAKE_ITEM_SIZE
        elif self.direction == 'Down':
            y1 += SNAKE_ITEM_SIZE
            y2 += SNAKE_ITEM_SIZE

        # Check collision with walls
        if x1 < 0 or y1 < 0 or x2 > GAME_WIDTH or y2 > GAME_HEIGHT:
            self.game_over()
            return

        # Check collision with itself
        for segment in self.snake[1:]:
            if self.canvas.coords(segment) == [x1, y1, x2, y2]:
                self.game_over()
                return

        # Move snake
        new_segment = self.canvas.create_rectangle(x1, y1, x2, y2, fill=SNAKE_COLOR)
        self.snake = [new_segment] + self.snake

        # Check if snake ate the food
        if self.canvas.coords(self.food) == [x1, y1, x2, y2]:
            self.create_food()
        else:
            self.canvas.delete(self.snake[-1])
            self.snake.pop()

        self.root.after(SNAKE_SPEED, self.move_snake)

    def game_over(self):
        """End the game"""
        self.running = False
        self.canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, text="GAME OVER!", fill="white", font=("Arial", 32))

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
