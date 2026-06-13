# game.py

import json
import os
import random
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static
from rich.text import Text

# Import constants from our new config module
from config import GRID_WIDTH, GRID_HEIGHT, STEADY_SPEED, HIGHSCORE_FILE

class SnakeGameApp(App):
    """A classic Snake game built with Textual and Rich with Persistent High Scores."""

    CSS = f"""
    Container {{
        align: center middle;
    }}
    #game-screen {{
        width: {GRID_WIDTH * 2 + 2};       /* Automatically scales with configuration */
        height: {GRID_HEIGHT + 2};
        border: heavy green;
        background: $surface;
        content-align: left top;
    }}
    #score-board {{
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }}
    """

    BINDINGS = [
        ("up,w", "move_up", "Move Up"),
        ("down,s", "move_down", "Move Down"),
        ("left,a", "move_left", "Move Left"),
        ("right,d", "move_right", "Move Right"),
        ("p", "toggle_pause", "Pause/Unpause"),
        ("r", "reset", "Restart"),
        ("q", "quit", "Quit")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container():
            yield Static("Score: 0  |  High Score: 0", id="score-board")
            yield Static("", id="game-screen")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Terminal Snake"
        self.load_high_score()  
        self.reset_game()

    def load_high_score(self) -> None:
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
            except (json.JSONDecodeError, KeyError):
                self.high_score = 0
        else:
            self.high_score = 0

    def save_high_score(self) -> None:
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except IOError:
            pass  

    def reset_game(self) -> None:
        self.score = 0
        self.game_over = False
        self.is_paused = False
        self.new_high_score_achieved = False
        
        self.snake = [(GRID_HEIGHT // 2, 5), (GRID_HEIGHT // 2, 4)]
        self.direction = (0, 1)  
        self.next_direction = (0, 1)
        
        self.spawn_food()
        self.update_ui()
        
        if hasattr(self, 'game_timer'):
            self.game_timer.stop()
        self.game_timer = self.set_interval(STEADY_SPEED, self.game_tick)

    def spawn_food(self) -> None:
        while True:
            self.food = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
            if self.food not in self.snake:
                break

    def game_tick(self) -> None:
        if self.game_over or self.is_paused:
            return

        self.direction = self.next_direction
        head_r, head_c = self.snake[0]
        dr, dc = self.direction
        new_head = (head_r + dr, head_c + dc)

        if not (0 <= new_head[0] < GRID_HEIGHT and 0 <= new_head[1] < GRID_WIDTH):
            self.trigger_game_over()
            return

        if new_head in self.snake:
            self.trigger_game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
                self.new_high_score_achieved = True
            self.spawn_food()
        else:
            self.snake.pop()

        self.update_ui()

    def update_ui(self) -> None:
        if self.is_paused:
            self.query_one("#score-board").update(
                Text(f"⏸️ PAUSED | Score: {self.score}  |  High Score: {self.high_score} (Press 'P' to resume)", style="bold yellow")
            )
            return

        hs_style = "bold cyan" if self.new_high_score_achieved else "white"
        score_text = Text()
        score_text.append(f"Score: {self.score}  |  ")
        score_text.append(f"High Score: {self.high_score}", style=hs_style)
        
        self.query_one("#score-board").update(score_text)
        
        screen_lines = []
        for r in range(GRID_HEIGHT):
            line = Text()
            for c in range(GRID_WIDTH):
                if (r, c) == self.snake[0]:
                    line.append("██", style="bold green")  
                elif (r, c) in self.snake:
                    line.append("▓▓", style="green")       
                elif (r, c) == self.food:
                    line.append("🍎", style="red")         
                else:
                    line.append("  ")                       
            screen_lines.append(line)

        render_output = Text("\n").join(screen_lines)
        self.query_one("#game-screen").update(render_output)

    def trigger_game_over(self) -> None:
        self.game_over = True
        if hasattr(self, 'game_timer'):
            self.game_timer.stop()
            
        self.save_high_score()
        
        if self.new_high_score_achieved:
            msg = f"🏆 NEW HIGH SCORE! Final Score: {self.score} (Press 'R' to restart)"
            style = "bold cyan"
        else:
            msg = f"💥 GAME OVER! Final Score: {self.score}  |  Best: {self.high_score} (Press 'R' to restart)"
            style = "bold red"
            
        self.query_one("#score-board").update(Text(msg, style=style))

    def action_toggle_pause(self) -> None:
        if self.game_over:
            return
            
        self.is_paused = not self.is_paused
        
        if hasattr(self, 'game_timer'):
            self.game_timer.stop()

        if self.is_paused:
            self.update_ui()
        else:
            self.game_timer = self.set_interval(STEADY_SPEED, self.game_tick)
            self.update_ui()

    def action_move_up(self) -> None:
        if self.direction != (1, 0) and not self.is_paused:
            self.next_direction = (-1, 0)

    def action_move_down(self) -> None:
        if self.direction != (-1, 0) and not self.is_paused:
            self.next_direction = (1, 0)

    def action_move_left(self) -> None:
        if self.direction != (0, 1) and not self.is_paused:
            self.next_direction = (0, -1)

    def action_move_right(self) -> None:
        if self.direction != (0, -1) and not self.is_paused:
            self.next_direction = (0, 1)

    def action_reset(self) -> None:
        self.reset_game()


if __name__ == "__main__":
    app = SnakeGameApp()
    app.run()
