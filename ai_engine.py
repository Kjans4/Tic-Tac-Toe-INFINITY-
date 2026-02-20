import random

class TicTacToeAI:
    def __init__(self, symbol="O", opponent="X"):
        self.symbol = symbol
        self.opponent = opponent

    def get_move(self, board_dict, logic_engine):
        """
        Decides the best move for the AI.
        board_dict: {(r, c): "X" or "O" or ""}
        logic_engine: The current game_logic instance to see move history.
        """
        
        # 1. Can the AI win in this move?
        move = self._find_winning_move(board_dict, self.symbol)
        if move:
            return move

        # 2. Does the AI need to block the player?
        move = self._find_winning_move(board_dict, self.opponent)
        if move:
            return move

        # 3. Strategic Move: Try to take the center if open
        if board_dict.get((1, 1)) == "":
            return (1, 1)

        # 4. Random Move: Pick any available empty spot
        empty_cells = [coord for coord, val in board_dict.items() if val == ""]
        return random.choice(empty_cells) if empty_cells else None

    def _find_winning_move(self, board_dict, player_symbol):
        """Helper to find if a player is one move away from winning."""
        win_conditions = [
            [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
            [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
            [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]
        ]

        for combo in win_conditions:
            values = [board_dict.get(coord) for coord in combo]
            # If two spots are the player's and one is empty
            if values.count(player_symbol) == 2 and values.count("") == 1:
                return combo[values.index("")]
        return None