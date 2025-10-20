import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        # Bảng trò chơi
        self.board = [" "] * 9
        self.current_player = "X"

        # Tạo các nút cho bảng trò chơi
        self.buttons = [tk.Button(root, text=" ", font=("Arial", 20), width=5, height=2, 
                                  command=lambda i=i: self.make_move(i)) for i in range(9)]

        # Đặt các nút vào lưới
        for i, button in enumerate(self.buttons):
            row = i // 3
            col = i % 3
            button.grid(row=row, column=col)

    def make_move(self, index):
        # Nếu ô đã được chọn, không làm gì
        if self.board[index] != " ":
            return

        # Đặt dấu của người chơi hiện tại
        self.board[index] = self.current_player
        self.buttons[index].config(text=self.current_player)

        # Kiểm tra xem người chơi hiện tại có thắng không
        if self.check_win():
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_game()
        # Kiểm tra xem trò chơi có hòa không
        elif " " not in self.board:
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()
        else:
            # Chuyển lượt cho người chơi khác
            self.current_player = "O" if self.current_player == "X" else "X"

    def check_win(self):
        # Các điều kiện chiến thắng
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Hàng
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Cột
            [0, 4, 8], [2, 4, 6]              # Chéo
        ]
        
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != " ":
                return True
        return False

    def reset_game(self):
        # Khởi tạo lại bảng trò chơi
        self.board = [" "] * 9
        for button in self.buttons:
            button.config(text=" ")
        self.current_player = "X"  # Người chơi "X" bắt đầu

# Tạo cửa sổ chính
root = tk.Tk()

# Tạo trò chơi Tic Tac Toe
game = TicTacToe(root)

# Chạy giao diện Tkinter
root.mainloop()

