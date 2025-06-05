import tkinter as tk
from tkinter import ttk, scrolledtext
from lab6hỗtrợlab7 import compare_methods
def calculate_and_display():
    try:
        max_n = int(entry.get())
        if max_n < 0:
            raise ValueError
        results = compare_methods(max_n)
        output_area.delete(1.0, tk.END)
        output_area.insert(tk.END, f"{'n':<5}{'рекурсивный (ms)':<15}{'петля (ms)':<15}\n")
        output_area.insert(tk.END, "-" * 35 + "\n")
        for n, time_rec, time_iter in results:
            output_area.insert(tk.END, f"{n:<5}{time_rec*1000:<15.4f}{time_iter*1000:<15.4f}\n")
    except ValueError:
        output_area.delete(1.0, tk.END)
        output_area.insert(tk.END, "Lỗi: Nhập số tự nhiên ≥ 0!")
root = tk.Tk()
root.title("So sánh Đệ quy vs Vòng lặp - Lab 7")
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.X)
ttk.Label(input_frame, text="введите n макс:").pack(side=tk.LEFT, padx=5)
entry = ttk.Entry(input_frame)
entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
button = ttk.Button(input_frame, text="вычислить", command=calculate_and_display)
button.pack(side=tk.LEFT, padx=5)
output_area = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.NONE)
output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
root.mainloop()