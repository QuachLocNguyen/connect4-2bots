import streamlit as st
import numpy as np
from easyAI import TwoPlayerGame, AI_Player, Negamax

class ConnectFour(TwoPlayerGame):
    def __init__(self, players, board=None):
        self.players = players
        self.board = (
            board
            if (board is not None)
            else (np.array([[0 for i in range(7)] for j in range(6)]))
        )
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        return [i for i in range(7) if (self.board[:, i].min() == 0)]

    def make_move(self, column):
        line = np.argmin(self.board[:, column] != 0)
        self.board[line, column] = self.current_player

    def lose(self):
        return find_four(self.board, self.opponent_index)

    def is_over(self):
        return (self.board.min() > 0) or self.lose()

    def scoring(self):
        return -100 if self.lose() else 0

def find_four(board, current_player):
    POS_DIR = np.array(
        [[[i, 0], [0, 1]] for i in range(6)]
        + [[[0, i], [1, 0]] for i in range(7)]
        + [[[i, 0], [1, 1]] for i in range(1, 3)]
        + [[[0, i], [1, 1]] for i in range(4)]
        + [[[i, 6], [1, -1]] for i in range(1, 3)]
        + [[[0, i], [1, -1]] for i in range(3, 7)]
    )
    
    for pos, direction in POS_DIR:
        streak = 0
        while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
            if board[pos[0], pos[1]] == current_player:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
            pos = pos + direction
    return False

def render_board(board):
    board_html = "<table style='border-collapse: collapse;'>"
    for row in range(5, -1, -1):
        board_html += "<tr>"
        for col in range(7):
            cell_color = "white"
            if board[row][col] == 1:
                cell_color = "red"
            elif board[row][col] == 2:
                cell_color = "yellow"
            
            board_html += f"<td style='border: 1px solid black; width: 50px; height: 50px; text-align: center; background-color: {cell_color};'></td>"
        board_html += "</tr>"
    board_html += "</table>"
    return board_html

def main():
    st.title("Connect Four AI Game")

    # AI difficulty selection
    difficulty = st.selectbox("Select AI Difficulty", ["Easy (Depth 3)", "Medium (Depth 5)", "Hard (Depth 7)"])
    
    # Mapping difficulty to search depth
    depth_map = {
        "Easy (Depth 3)": 3,
        "Medium (Depth 5)": 5,
        "Hard (Depth 7)": 7
    }
    search_depth = depth_map[difficulty]

    # Create AI players
    ai_algo_1 = Negamax(search_depth)
    ai_algo_2 = Negamax(search_depth)
    game = ConnectFour([AI_Player(ai_algo_1), AI_Player(ai_algo_2)])

    # Game play button
    if st.button("Play Game"):
        # Reset the game
        game.board = np.array([[0 for i in range(7)] for j in range(6)])
        game.current_player = 1
        
        # Run the game
        while not game.is_over():
            # Get the current AI player
            current_ai = game.players[game.current_player - 1]
            
            # Get move using get_move()
            move = current_ai.get_move(game)
            
            # Play the move
            game.make_move(move)
            
            # Display current board state
            st.markdown(render_board(game.board), unsafe_allow_html=True)
            
            # Switch players
            game.current_player = 3 - game.current_player  # Toggle between 1 and 2
        
        # Determine and display game result
        if game.lose():
            st.write(f"Player {game.opponent_index} wins!")
        else:
            st.write("Draw! The board is full.")

if __name__ == "__main__":
    main()
