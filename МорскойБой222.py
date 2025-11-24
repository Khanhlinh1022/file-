import tkinter as tk
from tkinter import messagebox
import random

class МорскойБой:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Морской Бой")
        self.root.geometry("800x600")
        
        # Размеры поля
        self.grid_size = 10
        self.cell_size = 30
        
        # Корабли
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # размеры кораблей
        
        # Игровые поля
        self.player_grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.computer_grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.computer_hidden_grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Счетчики попаданий
        self.player_hits = 0
        self.computer_hits = 0
        self.total_ship_cells = sum(self.ships)
        
        self.setup_game()
        
    def setup_game(self):
        # Создание основного фрейма
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Заголовок
        title_label = tk.Label(main_frame, text="МОРСКОЙ БОЙ", 
                              font=("Arial", 20, "bold"), fg="blue")
        title_label.pack(pady=10)
        
        # Фрейм для игровых полей
        fields_frame = tk.Frame(main_frame)
        fields_frame.pack(expand=True, fill='both')
        
        # Поле игрока
        player_frame = tk.Frame(fields_frame)
        player_frame.pack(side='left', padx=20)
        
        player_label = tk.Label(player_frame, text="Ваше поле:", font=("Arial", 12, "bold"))
        player_label.pack()
        
        self.player_canvas = tk.Canvas(player_frame, 
                                      width=self.grid_size * self.cell_size,
                                      height=self.grid_size * self.cell_size,
                                      bg='lightblue')
        self.player_canvas.pack(pady=5)
        
        # Поле компьютера
        computer_frame = tk.Frame(fields_frame)
        computer_frame.pack(side='right', padx=20)
        
        computer_label = tk.Label(computer_frame, text="Поле противника:", font=("Arial", 12, "bold"))
        computer_label.pack()
        
        self.computer_canvas = tk.Canvas(computer_frame,
                                        width=self.grid_size * self.cell_size,
                                        height=self.grid_size * self.cell_size,
                                        bg='lightblue')
        self.computer_canvas.pack(pady=5)
        self.computer_canvas.bind('<Button-1>', self.player_shot)
        
        # Статус игры
        self.status_label = tk.Label(main_frame, text="Расставьте ваши корабли!", 
                                    font=("Arial", 12), fg="red")
        self.status_label.pack(pady=10)
        
        # Кнопки управления
        control_frame = tk.Frame(main_frame)
        control_frame.pack(pady=10)
        
        self.auto_place_btn = tk.Button(control_frame, text="Авторасстановка", 
                                       command=self.auto_place_ships)
        self.auto_place_btn.pack(side='left', padx=5)
        
        self.start_btn = tk.Button(control_frame, text="Начать игру", 
                                  command=self.start_game, state='disabled')
        self.start_btn.pack(side='left', padx=5)
        
        self.restart_btn = tk.Button(control_frame, text="Новая игра", 
                                    command=self.restart_game)
        self.restart_btn.pack(side='left', padx=5)
        
        # Отрисовка сеток
        self.draw_grids()
        
        # Автоматическая расстановка кораблей
        self.auto_place_ships()
        
    def draw_grids(self):
        # Очистка canvas
        self.player_canvas.delete("all")
        self.computer_canvas.delete("all")
        
        # Рисование сетки для игрока
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Поле игрока
                self.player_canvas.create_rectangle(x1, y1, x2, y2, outline='black')
                if self.player_grid[i][j] == 'S':
                    self.player_canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, fill='gray')
                elif self.player_grid[i][j] == 'X':
                    self.player_canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, fill='red')
                elif self.player_grid[i][j] == 'O':
                    self.player_canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill='white')
                
                # Поле компьютера
                self.computer_canvas.create_rectangle(x1, y1, x2, y2, outline='black')
                if self.computer_hidden_grid[i][j] == 'X':
                    self.computer_canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, fill='red')
                elif self.computer_hidden_grid[i][j] == 'O':
                    self.computer_canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill='white')
    
    def auto_place_ships(self):
        # Очистка полей
        self.player_grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.computer_grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.computer_hidden_grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Расстановка кораблей игрока
        for ship_size in self.ships:
            self.place_ship_randomly(self.player_grid, ship_size)
        
        # Расстановка кораблей компьютера
        for ship_size in self.ships:
            self.place_ship_randomly(self.computer_grid, ship_size)
        
        self.draw_grids()
        self.start_btn.config(state='normal')
        self.status_label.config(text="Корабли расставлены! Нажмите 'Начать игру'")
    
    def place_ship_randomly(self, grid, ship_size):
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - ship_size)
            else:
                row = random.randint(0, self.grid_size - ship_size)
                col = random.randint(0, self.grid_size - 1)
            
            if self.can_place_ship(grid, row, col, ship_size, orientation):
                for i in range(ship_size):
                    if orientation == 'horizontal':
                        grid[row][col + i] = 'S'
                    else:
                        grid[row + i][col] = 'S'
                break
    
    def can_place_ship(self, grid, row, col, ship_size, orientation):
        # Проверка возможности размещения корабля
        for i in range(ship_size):
            r = row + (i if orientation == 'vertical' else 0)
            c = col + (i if orientation == 'horizontal' else 0)
            
            # Проверка границ
            if r >= self.grid_size or c >= self.grid_size:
                return False
            
            # Проверка соседних клеток
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                        if grid[nr][nc] == 'S':
                            return False
        return True
    
    def start_game(self):
        self.auto_place_btn.config(state='disabled')
        self.start_btn.config(state='disabled')
        self.status_label.config(text="Ваш ход! Стреляйте по полю противника.")
        self.game_active = True
    
    def player_shot(self, event):
        if not hasattr(self, 'game_active') or not self.game_active:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if self.computer_hidden_grid[row][col] in ['X', 'O']:
                return  # Уже стреляли сюда
            
            if self.computer_grid[row][col] == 'S':
                self.computer_hidden_grid[row][col] = 'X'
                self.player_hits += 1
                self.status_label.config(text=f"Попадание! ({row},{col})")
            else:
                self.computer_hidden_grid[row][col] = 'O'
                self.status_label.config(text=f"Промах! ({row},{col})")
            
            self.draw_grids()
            
            # Проверка победы игрока
            if self.player_hits >= self.total_ship_cells:
                self.game_active = False
                messagebox.showinfo("Победа!", "Поздравляем! Вы победили!")
                return
            
            # Ход компьютера
            self.root.after(1000, self.computer_shot)
    
    def computer_shot(self):
        if not self.game_active:
            return
        
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            
            if self.player_grid[row][col] not in ['X', 'O']:
                break
        
        if self.player_grid[row][col] == 'S':
            self.player_grid[row][col] = 'X'
            self.computer_hits += 1
            self.status_label.config(text=f"Противник попал в ({row},{col})!")
        else:
            self.player_grid[row][col] = 'O'
            self.status_label.config(text=f"Противник промахнулся в ({row},{col})")
        
        self.draw_grids()
        
        # Проверка победы компьютера
        if self.computer_hits >= self.total_ship_cells:
            self.game_active = False
            messagebox.showinfo("Поражение!", "К сожалению, вы проиграли.")
    
    def restart_game(self):
        self.player_hits = 0
        self.computer_hits = 0
        self.auto_place_btn.config(state='normal')
        self.start_btn.config(state='disabled')
        self.auto_place_ships()
    
    def run(self):
        self.root.mainloop()

# Запуск игры
if __name__ == "__main__":
    game = МорскойБой()
    game.run()