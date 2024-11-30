import streamlit as st
import numpy as np
import time

class ConnectFourGame:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.current_player = 1

    def make_move(self, column):
        for row in range(5, -1, -1):
            if self.board[row, column] == 0:
                self.board[row, column] = self.current_player
                return True
        return False

    def is_valid_move(self, column):
        return self.board[0, column] == 0

    def get_valid_moves(self):
        return [col for col in range(7) if self.is_valid_move(col)]

    def check_win(self):
        # Horizontal check
        for row in range(6):
            for col in range(4):
                if (self.board[row, col] == self.board[row, col+1] == 
                    self.board[row, col+2] == self.board[row, col+3] != 0):
                    return True

        # Vertical check
        for row in range(3):
            for col in range(7):
                if (self.board[row, col] == self.board[row+1, col] == 
                    self.board[row+2, col] == self.board[row+3, col] != 0):
                    return True

        # Diagonal checks
        for row in range(3):
            for col in range(4):
                # Positive slope diagonal
                if (self.board[row, col] == self.board[row+1, col+1] == 
                    self.board[row+2, col+2] == self.board[row+3, col+3] != 0):
                    return True
                
                # Negative slope diagonal
                if (self.board[row+3, col] == self.board[row+2, col+1] == 
                    self.board[row+1, col+2] == self.board[row, col+3] != 0):
                    return True

        return False

    def is_draw(self):
        return len(self.get_valid_moves()) == 0

    def simple_ai_move(self, player):
        # Simple AI that tries to block opponent or make winning move
        valid_moves = self.get_valid_moves()
        
        # Try to win
        for move in valid_moves:
            self.make_move(move)
            if self.check_win():
                self.board[self.board[:, move] != 0][0] = 0  # Undo move
                return move
            self.board[self.board[:, move] != 0][0] = 0  # Undo move
        
        # Try to block opponent
        opponent = 3 - player
        self.current_player = opponent
        for move in valid_moves:
            self.make_move(move)
            if self.check_win():
                self.board[self.board[:, move] != 0][0] = 0  # Undo move
                self.current_player = player
                return move
            self.board[self.board[:, move] != 0][0] = 0  # Undo move
        
        self.current_player = player
        # If no strategic move, choose random valid move
        return np.random.choice(valid_moves)

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

def play_game(ai_depth1=3, ai_depth2=3):
    game = ConnectFourGame()
    game_steps = [game.board.copy()]
    
    while True:
        # Player 1's turn
        move = game.simple_ai_move(1)
        game.make_move(move)
        game_steps.append(game.board.copy())
        
        if game.check_win():
            return game_steps, 1
        
        if game.is_draw():
            return game_steps, 0
        
        # Player 2's turn
        move = game.simple_ai_move(2)
        game.make_move(move)
        game_steps.append(game.board.copy())
        
        if game.check_win():
            return game_steps, 2
        
        if game.is_draw():
            return game_steps, 0

def main():
    st.title("Connect Four AI Battle")
    
    # Sidebar for game configuration
    st.sidebar.header("Game Configuration")
    ai_depth1 = st.sidebar.slider("Player 1 AI Complexity", 1, 5, 3)
    ai_depth2 = st.sidebar.slider("Player 2 AI Complexity", 1, 5, 3)
    
    # Button to start the game
    if st.sidebar.button("Start Game"):
        # Run the game
        st.write("Game in progress...")
        game_steps, winner = play_game(ai_depth1, ai_depth2)
        
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
