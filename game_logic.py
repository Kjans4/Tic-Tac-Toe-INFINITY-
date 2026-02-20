from collections import deque

class RollingLogic:
    def __init__(self):
        # Using deque with maxlen=3 automatically handles the "Rolling"
        # When a 4th item is added, the 1st one is automatically dropped.
        self.moves_x = deque(maxlen=3)
        self.moves_o = deque(maxlen=3)
        self.current_player = "X"
        self.scores = {"X": 0, "O": 0}

    def record_move(self, r, c):
        """
        Processes a move. Returns the coordinate that needs to be 
        cleared from the board if the 'Rolling' limit was reached.
        """
        vanished_coord = None
        current_queue = self.moves_x if self.current_player == "X" else self.moves_o
        
        # If queue is full, the oldest move will disappear when we append the new one
        if len(current_queue) == 3:
            vanished_coord = current_queue[0] 

        current_queue.append((r, c))
        return vanished_coord

    def check_winner(self, board_dict):
        """
        Scans the current board state (dictionary of coordinates) 
        to see if the current player has 3 in a row.
        """
        p = self.current_player
        win_conditions = [
            [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)], # Rows
            [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)], # Cols
            [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]             # Diagonals
        ]
        
        for condition in win_conditions:
            if all(board_dict.get(coord) == p for coord in condition):
                self.scores[p] += 1
                return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def reset_game_state(self):
        self.moves_x.clear()
        self.moves_o.clear()
        self.current_player = "X"