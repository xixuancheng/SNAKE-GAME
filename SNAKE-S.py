import pygame
import random
import json
import os

class Snake:
    def __init__(self, start_pos):
        self.body = [list(start_pos)]
        self.direction = (1, 0)
        self.grow_flag = False

    def move(self):
        head = self.body[0].copy()
        head[0] += self.direction[0]
        head[1] += self.direction[1]
        self.body.insert(0, head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def change_dir(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def head(self):
        return self.body[0]

    def self_collision(self):
        return self.head() in self.body[1:]

    def draw(self, screen, block):
        for seg in self.body:
            pygame.draw.rect(screen, (0,255,0), (seg[0]*block, seg[1]*block, block, block))

class Game:
    def __init__(self, width=20, height=15, block=40):
        self.width = width
        self.height = height
        self.block = block
        self.screen = pygame.display.set_mode((width*block, height*block))
        pygame.display.set_caption("贪吃蛇")
        self.clock = pygame.time.Clock()
        self.snake = Snake((width//2, height//2))
        self.food = self._new_food()
        self.score = 0
        self.high_score = self._load_high_score()
        self.game_over = False

    def _load_high_score(self):
        if not os.path.exists("highscore.json"):
            return 0
        with open("highscore.json", "r") as f:
            data = json.load(f)
            return data.get("high_score", 0)

    def _save_high_score(self):
        with open("highscore.json", "w") as f:
            json.dump({"high_score": self.high_score}, f)

    def _new_food(self):
        while True:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            if [x, y] not in self.snake.body:
                return (x, y)

    def _check_boundary(self):
        hx, hy = self.snake.head()
        return hx < 0 or hx >= self.width or hy < 0 or hy >= self.height

    def _check_food(self):
        if tuple(self.snake.head()) == self.food:
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                self._save_high_score()
            self.snake.grow()
            self.food = self._new_food()

    def _game_over_screen(self):
        font_big = pygame.font.Font(None, 72)
        text = font_big.render("GAME OVER", True, (255,0,0))
        rect = text.get_rect(center=(self.width*self.block//2, self.height*self.block//2))
        self.screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def run(self):
        pygame.init()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.change_dir((0,-1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_dir((0,1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_dir((-1,0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_dir((1,0))

            if self.game_over:
                self._game_over_screen()
                running = False
                break

            self.snake.move()
            if self._check_boundary() or self.snake.self_collision():
                self.game_over = True
                continue
            self._check_food()

            self.screen.fill((0,0,0))
            self.snake.draw(self.screen, self.block)
            pygame.draw.rect(self.screen, (255,0,0),
                             (self.food[0]*self.block, self.food[1]*self.block, self.block, self.block))

            font = pygame.font.Font(None, 36)
            text = font.render(f"Score: {self.score}  High: {self.high_score}", True, (255,255,255))
            self.screen.blit(text, (10,10))

            pygame.display.flip()
            self.clock.tick(5)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()