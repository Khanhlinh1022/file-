import tkinter as tk
from tkinter import filedialog, messagebox
import csv
class Rectangle:
    def __init__(self, x, y, width, height, color="black"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    def intersects(self, other):
        """Kiểm tra giao nhau với hình chữ nhật khác"""
        return not (self.x + self.width < other.x or 
                   other.x + other.width < self.x or 
                   self.y + self.height < other.y or 
                   other.y + other.height < self.y)
    def draw(self, canvas):
        """Vẽ hình chữ nhật lên canvas"""
        return canvas.create_rectangle(
            self.x, self.y, 
            self.x + self.width, self.y + self.height,
            outline=self.color, width=2)
    def move(self, dx, dy):
        """Di chuyển hình chữ nhật"""
        self.x += dx
        self.y += dy
    def set_color(self, color):
        """Thay đổi màu sắc"""
        self.color = color
    def to_csv(self):
        """Chuyển đổi thành dạng CSV"""
        return [self.x, self.y, self.width, self.height, self.color]
    @classmethod
    def from_csv(cls, row):
        """Tạo hình chữ nhật từ dữ liệu CSV"""
        try:
            x, y, width, height = map(float, row[:4])
            color = row[4] if len(row) > 4 else "black"
            return cls(x, y, width, height, color)
        except (ValueError, IndexError):
            return None
class RectangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rectangle Manager - Lab 8 OOP")
        self.rectangles = []
        self.selected_rect = None
        self.canvas_rects = []
        # Tạo giao diện
        self.create_widgets()
    def create_widgets(self):
        # Frame điều khiển
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        # Nút tạo hình chữ nhật mới
        tk.Button(control_frame, text="Thêm HCN", command=self.add_rectangle).pack(fill=tk.X, pady=5)
        # Nút kiểm tra giao nhau
        tk.Button(control_frame, text="Kiểm tra giao nhau", command=self.check_intersections).pack(fill=tk.X, pady=5)
        # Nút thay đổi màu
        tk.Button(control_frame, text="Đổi màu", command=self.change_color).pack(fill=tk.X, pady=5)
        # Nút di chuyển
        tk.Button(control_frame, text="Di chuyển", command=self.move_rectangle).pack(fill=tk.X, pady=5)
        # Nút đọc từ file
        tk.Button(control_frame, text="Đọc từ file", command=self.load_from_file).pack(fill=tk.X, pady=5)
        # Nút lưu vào file
        tk.Button(control_frame, text="Lưu vào file", command=self.save_to_file).pack(fill=tk.X, pady=5)
        # Canvas để vẽ
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)
        # Sự kiện click chuột để chọn hình
        self.canvas.bind("<Button-1>", self.select_rectangle)
    def add_rectangle(self):
        """Thêm hình chữ nhật mới với kích thước ngẫu nhiên"""
        import random
        x = random.randint(50, 400)
        y = random.randint(50, 300)
        width = random.randint(50, 150)
        height = random.randint(50, 150)
        color = random.choice(["red", "green", "blue", "yellow", "purple"])
        
        rect = Rectangle(x, y, width, height, color)
        self.rectangles.append(rect)
        self.redraw_canvas()
    def check_intersections(self):
        """Kiểm tra giao nhau giữa các hình chữ nhật"""
        if len(self.rectangles) < 2:
            messagebox.showinfo("Thông báo", "Cần ít nhất 2 hình chữ nhật để kiểm tra")
            return
        results = []
        for i in range(len(self.rectangles)):
            for j in range(i+1, len(self.rectangles)):
                if self.rectangles[i].intersects(self.rectangles[j]):
                    results.append(f"HCN {i+1} giao với HCN {j+1}")
        if results:
            messagebox.showinfo("Kết quả kiểm tra", "\n".join(results))
        else:
            messagebox.showinfo("Kết quả kiểm tra", "Không có hình chữ nhật nào giao nhau")
    def change_color(self):
        """Thay đổi màu của hình được chọn"""
        if not self.selected_rect:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một hình chữ nhật trước")
            return
        color = tk.simpledialog.askstring("Đổi màu", "Nhập màu mới (vd: red, green, #FF0000):")
        if color:
            self.selected_rect.set_color(color)
            self.redraw_canvas()
    def move_rectangle(self):
        """Di chuyển hình được chọn"""
        if not self.selected_rect:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một hình chữ nhật trước")
            return
        dx = tk.simpledialog.askinteger("Di chuyển", "Nhập khoảng di chuyển theo trục X:", initialvalue=10)
        dy = tk.simpledialog.askinteger("Di chuyển", "Nhập khoảng di chuyển theo trục Y:", initialvalue=10)
        if dx is not None and dy is not None:
            self.selected_rect.move(dx, dy)
            self.redraw_canvas()
    def select_rectangle(self, event):
        """Chọn hình chữ nhật khi click chuột"""
        for i, rect in enumerate(self.rectangles):
            if (rect.x <= event.x <= rect.x + rect.width and 
                rect.y <= event.y <= rect.y + rect.height):
                self.selected_rect = rect
                self.highlight_selected()
                return
        self.selected_rect = None
        self.highlight_selected()
    def highlight_selected(self):
        """Làm nổi bật hình được chọn"""
        self.redraw_canvas()
        if self.selected_rect:
            # Vẽ thêm đường viền đậm cho hình được chọn
            self.canvas.create_rectangle(
                self.selected_rect.x - 2, self.selected_rect.y - 2,
                self.selected_rect.x + self.selected_rect.width + 2,
                self.selected_rect.y + self.selected_rect.height + 2,
                outline="black", width=4, dash=(5, 5))
    def redraw_canvas(self):
        """Vẽ lại tất cả hình chữ nhật lên canvas"""
        self.canvas.delete("all")
        self.canvas_rects = []
        for rect in self.rectangles:
            self.canvas_rects.append(rect.draw(self.canvas))
    def load_from_file(self):
        """Đọc dữ liệu từ file CSV"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                new_rects = []
                for row in reader:
                    rect = Rectangle.from_csv(row)
                    if rect:
                        new_rects.append(rect)
                if new_rects:
                    self.rectangles = new_rects
                    self.selected_rect = None
                    self.redraw_canvas()
                    messagebox.showinfo("Thành công", f"Đã tải {len(new_rects)} hình chữ nhật từ file")
                else:
                    messagebox.showwarning("Cảnh báo", "Không tìm thấy dữ liệu hợp lệ trong file")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    def save_to_file(self):
        """Lưu dữ liệu vào file CSV"""
        if not self.rectangles:
            messagebox.showwarning("Cảnh báo", "Không có hình chữ nhật nào để lưu")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for rect in self.rectangles:
                    writer.writerow(rect.to_csv())
            messagebox.showinfo("Thành công", "Dữ liệu đã được lưu vào file")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")
if __name__ == "__main__":
    root = tk.Tk()
    app = RectangleApp(root)
    root.mainloop()