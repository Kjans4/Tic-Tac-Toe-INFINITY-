# Tic-Tac-Toe INFINITY

A persistent-state, rolling Tic-Tac-Toe game built with Python and Tkinter.

## 🕹 Features
- **Rolling Logic:** Each player can only have 3 marks on the board. When the 4th mark is placed, the 1st one vanishes.
- **Infinity Loop:** When a player wins, the winning move is carried over to a fresh board for the next round.
- **AI Engine:** Play against a computer that understands the rolling mechanic.
- **Dynamic UI:** Real-time arrow indicators and victory highlights.

## 🛠 Project Structure
- `main.py`: Handles the UI, animations, and the infinity reset loop.
- `game_logic.py`: Manages the FIFO (First-In-First-Out) queues for the rolling moves.
- `ai_engine.py`: The "brain" of the computer opponent.

## 🚀 How to Play
1. Run `python main.py`.
2. Choose "Play Against Computer" or "2 Player Mode".
3. Watch for the **Pink** highlight—it warns you which of your marks will disappear next!