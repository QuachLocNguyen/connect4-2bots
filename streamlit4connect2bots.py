import streamlit as st
import numpy as np
from easyAI import TwoPlayerGame, AI_Player, Negamax
import time

class GameController(TwoPlayerGame):
    def __init__(self, players, board=None):
        # Define the players
        self.players = players
        
        # Define the configuration of the board
        self.board = board if (board is not None) else (
            np.array([[0 for _ in range(7)] for _ in range(6)]))
        
        # Define who starts the game 
        self.current_player = 1
        
        # Define the positions for checking win conditions
        self.pos_dir = np.array([[[i, 0], [0, 1]] for i in range(6)] +
                     [[[0, i], [1, 0]] for i in range(7)] +
                     [[[i, 0], [1, 1]] for i in range(1, 3)] +
                     [[[0, i], [1, 1]] for i in range(4)] +
                     [[[i, 6], [1, -1]] for i in range(1, 3)] +
                     [[[0, i], [1, -1]] for i in range(3, 7)])

    def possible_moves(self):
        return [i for i in range(7) if (self.board[:, i].min() == 0)]

    def make_move(self, column):
        line = np.argmin(self.board[:, column] != 0)
        self.board[line, column] = self.current_player

    def win(self):
        # Check for a win condition
        for pos, direction in self.pos_dir:
            streak = 0
            while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
                if self.board[pos[0], pos[1]] == 3 - self.current_player:
                    streak += 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
                pos = pos + direction
        return False

    def is_over(self):
        return (self.board.min() > 0) or self.win()

    def scoring(self):
        return -100 if self.win() else 0

def play_game(search_depth1, search_depth2):
    # Define the algorithms that will be used
    algo_neg1 = Negamax(search_depth1)
    algo_neg2 = Negamax(search_depth2)

    # Start the game
    game = GameController([AI_Player(algo_neg1), AI_Player(algo_neg2)])
    
    # Placeholder for game steps to visualize
    game_steps = []
    game_steps.append(game.board.copy())

    # Play the game
    while not game.is_over():
        # Make a move
        move = game.players[game.current_player - 1].play(game)
        game.make_move(move)
        
        # Store board state after each move
        game_steps.append(game.board.copy())
        
        # Switch players
        game.current_player = 3 - game.current_player

    # Determine winner
    winner = 3 - game.current_player if game.win() else 0

    return game_steps, winner

def visualize_board(board):
    """Create a visual representation of the board."""
    board_html = "<table style='border-collapse: collapse;'>"
    for row in reversed(board):
        board_html += "<tr>"
        for cell in row:
            color = "white"
            if cell == 1:
                color = "red"
            elif cell == 2:
                color = "yellow"
            board_html += f"<td style='border: 1px solid black; width: 50px; height: 50px; background-color: {color};'></td>"
        board_html += "</tr>"
    board_html += "</table>"
    return board_html

def main():
    st.title("Connect Four AI Battle")
    
    # Sidebar for game configuration
    st.sidebar.header("Game Configuration")
    search_depth1 = st.sidebar.slider("Player 1 Search Depth", 1, 10, 5)
    search_depth2 = st.sidebar.slider("Player 2 Search Depth", 1, 10, 5)
    
    # Button to start the game
    if st.sidebar.button("Start Game"):
        # Run the game
        st.write("Game in progress...")
        game_steps, winner = play_game(search_depth1, search_depth2)
        
        # Visualize game progression
        st.header("Game Progression")
        progress_bar = st.progress(0)
        
        for i, board_state in enumerate(game_steps):
            # Update progress bar
            progress_bar.progress((i + 1) / len(game_steps))
            
            # Create columns for board and info
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"### Move {i}")
                st.markdown(visualize_board(board_state), unsafe_allow_html=True)
            
            with col2:
                st.write(f"Current Board State:")
                st.code(board_state)
            
            # Add a small delay to make progression visible
            time.sleep(0.5)
        
        # Show final result
        if winner == 1:
            st.success("Player 1 (Red) Wins!")
        elif winner == 2:
            st.success("Player 2 (Yellow) Wins!")
        else:
            st.warning("The game ended in a draw!")

if __name__ == "__main__":
    main()
