import tkinter as tk
from game_logic import RollingLogic
from ai_engine import TicTacToeAI

class RollingTicTacToe:
    def __init__(self, root):
        """Initializes window, game logic, AI, and starting flags."""
        self.root = root
        self.root.title("Tic-Tac-Toe INFINITY")
        
        self.width = 400
        self.height = 580 
        self.center_window(self.root, self.width, self.height)
        
        self.logic = RollingLogic()
        self.ai = TicTacToeAI()
        
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(expand=True, fill="both")
        
        self.vs_computer = False
        self.buttons = {}
        self.is_resetting = False 
        self.show_home_screen()

    def center_window(self, target, w, h):
        """Centers the window on the screen."""
        target.update_idletasks()
        screen_width = target.winfo_screenwidth()
        screen_height = target.winfo_screenheight()
        x = (screen_width // 2) - (w // 2)
        y = (screen_height // 2) - (h // 2)
        target.geometry(f'{w}x{h}+{x}+{y}')

    def show_home_screen(self):
        """Displays the main menu with dramatic titles."""
        self.clear_screen()
        self.logic.scores = {"X": 0, "O": 0}
        self.logic.reset_game_state()
        
        tk.Label(self.main_container, text="Tic-Tac-Toe", font=("Arial", 18)).pack(pady=(40, 0))
        tk.Label(self.main_container, text="INFINITY", font=("Arial", 48, "bold"), fg="#FFD700").pack(pady=(0, 30))

        tk.Button(self.main_container, text="Play Against Computer", font=("Arial", 10, "bold"), 
                  width=25, height=2, command=lambda: self.start_game(True)).pack(pady=10)
        tk.Button(self.main_container, text="2 Player Mode", font=("Arial", 10, "bold"), 
                  width=25, height=2, command=lambda: self.start_game(False)).pack(pady=10)
        tk.Button(self.main_container, text="Close Program", width=25, height=2, fg="red", 
                  command=self.root.quit).pack(pady=10)

    def start_game(self, vs_comp):
        """Sets up the game board and starts the match."""
        self.vs_computer = vs_comp
        self.clear_screen()
        self.setup_game_board()
        self.update_score_display() # Initial Arrow for Player X
        self.highlight_next()

    def setup_game_board(self):
        """Initializes the score label and the 3x3 button grid."""
        tk.Label(self.main_container, text="INFINITY MODE", font=("Arial", 10, "bold"), fg="gray").pack()
        
        # Neutral background score label
        self.score_label = tk.Label(self.main_container, font=("Courier", 18, "bold"), pady=10)
        self.score_label.pack(fill="x", pady=10)

        self.board_frame = tk.Frame(self.main_container)
        self.board_frame.pack()
        
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.board_frame, text="", font=("Arial", 20, "bold"), width=5, height=2,
                                command=lambda row=r, col=c: self.handle_click(row, col))
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[(r, c)] = btn

        btn_frame = tk.Frame(self.main_container)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Again", width=10, command=self.refresh_board).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Reset Score", width=10, command=self.manual_score_reset).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Exit", width=10, fg="red", command=self.show_home_screen).pack(side="left", padx=5)

    def handle_click(self, r, c):
        """Handles player input."""
        if not self.is_resetting and self.buttons[(r, c)]["text"] == "":
            self.process_move(r, c)
            
            if self.vs_computer and self.logic.current_player == "O" and not self.is_resetting:
                self.root.after(400, self.trigger_ai)

    def process_move(self, r, c):
        """Logic for moves and checking wins."""
        vanished = self.logic.record_move(r, c)
        if vanished:
            self.buttons[vanished].config(text="", bg="SystemButtonFace")

        color = "blue" if self.logic.current_player == "X" else "red"
        self.buttons[(r, c)].config(text=self.logic.current_player, fg=color)
        
        board_state = {coord: btn["text"] for coord, btn in self.buttons.items()}
        winning_combo = self.check_logic_win(board_state)
        
        if winning_combo:
            self.is_resetting = True
            for coord in winning_combo:
                self.buttons[coord].config(bg="#FFD700") 
            
            self.logic.scores[self.logic.current_player] += 1
            # Simple text update without arrow during victory freeze
            self.score_label.config(text=f"X: {self.logic.scores['X']}  |  O: {self.logic.scores['O']}")
            
            winner_symbol = board_state[(r, c)]
            self.root.after(1500, lambda: self.auto_next_round(r, c, winner_symbol))
        else:
            self.logic.switch_player()
            self.update_score_display() 
            self.highlight_next()

    def auto_next_round(self, carry_r, carry_c, winner_symbol):
        """Carries winning move to the next round."""
        self.logic.reset_game_state()
        for coord, btn in self.buttons.items():
            btn.config(text="", bg="SystemButtonFace")
        
        self.logic.current_player = winner_symbol
        self.logic.record_move(carry_r, carry_c) 
        
        color = "blue" if winner_symbol == "X" else "red"
        self.buttons[(carry_r, carry_c)].config(text=winner_symbol, fg=color)
        
        self.logic.switch_player()
        self.is_resetting = False
        self.update_score_display() # New round, move the arrow
        self.highlight_next()

        if self.vs_computer and self.logic.current_player == "O":
            self.root.after(600, self.trigger_ai)

    def check_logic_win(self, board_state):
        """Scans for 3-in-a-row."""
        p = self.logic.current_player
        win_conditions = [
            [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
            [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
            [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]
        ]
        for condition in win_conditions:
            if all(board_state.get(coord) == p for coord in condition):
                return condition
        return None

    def highlight_next(self):
        """Warnings for fading marks."""
        for btn in self.buttons.values():
            if btn.cget("bg") != "#FFD700":
                btn.config(bg="SystemButtonFace")
        
        current_queue = self.logic.moves_x if self.logic.current_player == "X" else self.logic.moves_o
        if len(current_queue) == 3:
            oldest_coord = current_queue[0]
            self.buttons[oldest_coord].config(bg="#FFB6C1")

    def trigger_ai(self):
        """AI move logic."""
        if self.is_resetting: return
        board_state = {coord: btn["text"] for coord, btn in self.buttons.items()}
        move = self.ai.get_move(board_state, self.logic)
        if move:
            self.process_move(move[0], move[1])

    def refresh_board(self):
        """Manual reset."""
        self.logic.reset_game_state()
        for btn in self.buttons.values():
            btn.config(text="", bg="SystemButtonFace")
        self.is_resetting = False
        self.update_score_display()
        self.highlight_next()

    def manual_score_reset(self):
        """Reset scores."""
        self.logic.scores = {"X": 0, "O": 0}
        self.update_score_display()

    def update_score_display(self):
        """Moves the ▶ or ◀ arrow based on the active player."""
        x_score = self.logic.scores['X']
        o_score = self.logic.scores['O']
        
        if self.logic.current_player == "X":
            score_text = f"▶ X: {x_score}  |  O: {o_score}  "
            self.score_label.config(text=score_text, fg="blue", bg="SystemButtonFace")
        else:
            score_text = f"  X: {x_score}  |  O: {o_score} ◀"
            self.score_label.config(text=score_text, fg="red", bg="SystemButtonFace")

    def clear_screen(self):
        """Screen utility."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RollingTicTacToe(root)
    root.mainloop()