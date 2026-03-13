import tkinter as tk
from tkinter import ttk, messagebox

class GreedySolver:
    @staticmethod
    def solve(amount, denominations):
        """
        Giải bài toán đổi tiền bằng thuật toán Greedy.
        Trả về dictionary {mệnh_giá: số_tờ} và số tiền còn thừa (nếu có).
        """
        # Sắp xếp mệnh giá giảm dần
        sorted_denoms = sorted(denominations, reverse=True)
        result = {}
        remaining = amount
        
        for d in sorted_denoms:
            if d <= 0: continue
            count = remaining // d
            if count > 0:
                result[d] = count
                remaining %= d
                
        return result, remaining

class CoinChangeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Đổi tiền - Thuật toán Greedy")
        self.root.geometry("700x600")
        
        # Cấu hình màu sắc & font
        self.bg_color = "#f0f2f5"
        self.primary_color = "#1a73e8"
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=60)
        header.pack(fill="x")
        tk.Label(header, text="BÀI TOÁN ĐỔI TIỀN (GREEDY ALGORITHM)", 
                 fg="white", bg=self.primary_color, font=("Arial", 16, "bold")).pack(pady=15)

        # Tab control
        tabControl = ttk.Notebook(self.root)
        self.tab1 = tk.Frame(tabControl, bg="white")
        self.tab2 = tk.Frame(tabControl, bg="white")
        
        tabControl.add(self.tab1, text=' Thực nghiệm ')
        tabControl.add(self.tab2, text=' Cơ sở Lý thuyết ')
        tabControl.pack(expand=1, fill="both", padx=10, pady=10)
        
        self.setup_execution_tab()
        self.setup_theory_tab()

    def setup_execution_tab(self):
        # Input Section
        input_frame = tk.LabelFrame(self.tab1, text=" Nhập dữ liệu ", font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(input_frame, text="Số tiền cần đổi:", bg="white").grid(row=0, column=0, sticky="w")
        self.amount_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.amount_entry.insert(0, "125000")
        
        tk.Label(input_frame, text="Hệ thống tiền tệ:", bg="white").grid(row=1, column=0, sticky="w")
        self.currency_var = tk.StringVar(value="VND")
        tk.Radiobutton(input_frame, text="VND (1k, 2k, 5k, 10k, 20k, 50k, 100k, 200k, 500k)", 
                       variable=self.currency_var, value="VND", bg="white").grid(row=1, column=1, sticky="w")
        tk.Radiobutton(input_frame, text="USD (1, 5, 10, 25, 50, 100)", 
                       variable=self.currency_var, value="USD", bg="white").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(input_frame, text="Tùy chỉnh", 
                       variable=self.currency_var, value="CUSTOM", bg="white").grid(row=3, column=1, sticky="w")
        
        self.custom_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.custom_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.custom_entry.insert(0, "1, 3, 4")

        # Solve Button
        solve_btn = tk.Button(self.tab1, text="THỰC HIỆN ĐỔI TIỀN", bg="#28a745", fg="white", 
                              font=("Arial", 11, "bold"), command=self.solve_problem)
        solve_btn.pack(pady=10)

        # Result Section
        result_frame = tk.LabelFrame(self.tab1, text=" Kết quả thực nghiệm ", font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.result_text = tk.Text(result_frame, font=("Courier New", 11), height=10, bg="#f8f9fa")
        self.result_text.pack(fill="both", expand=True)

    def setup_theory_tab(self):
        theory_content = """
THUẬT TOÁN THAM LAM (GREEDY ALGORITHM)
--------------------------------------

1. Ý tưởng chính:
   Tại mỗi bước, thuật toán luôn chọn lựa phương án tốt nhất
   tại thời điểm hiện tại (mệnh giá tiền lớn nhất còn có thể lấy)
   với hy vọng kết quả cuối cùng sẽ là tối ưu toàn cục.

2. Các bước thực hiện:
   Bước 1: Sắp xếp các mệnh giá tiền theo thứ tự giảm dần.
   Bước 2: Duyệt qua từng mệnh giá:
      - Lấy tối đa số tờ của mệnh giá hiện tại.
      - Cập nhật số tiền còn lại sau khi đã lấy.
   Bước 3: Tiếp tục cho đến khi số tiền còn lại bằng 0 hoặc
           đã duyệt hết các mệnh giá.

3. Đánh giá độ phức tạp:
   - Thời gian: O(n log n) - chủ yếu do sắp xếp.
   - Không gian: O(n) - lưu trữ kết quả.

4. Lưu ý quan trọng:
   Thuật toán Greedy không phải lúc nào cũng cho kết quả tối ưu
   (số tờ ít nhất) cho mọi bộ tiền. Tuy nhiên, với các hệ thống
   tiền thực tế như VND hay USD, nó Luôn đạt tối ưu.
        """
        text_area = tk.Text(self.tab2, font=("Arial", 11), padx=20, pady=20, bg="#fff")
        text_area.insert("1.0", theory_content)
        text_area.config(state="disabled")
        text_area.pack(fill="both", expand=True)

    def solve_problem(self):
        try:
            amount_str = self.amount_entry.get().replace(",", "").replace(".", "")
            amount = int(amount_str)
            if amount < 0: raise ValueError
            
            mode = self.currency_var.get()
            if mode == "VND":
                denoms = [500000, 200000, 100000, 50000, 20000, 10000, 5000, 2000, 1000]
            elif mode == "USD":
                denoms = [100, 50, 25, 10, 5, 1]
            else:
                custom_str = self.custom_entry.get()
                denoms = [int(x.strip()) for x in custom_str.split(",") if x.strip()]
            
            if not denoms:
                messagebox.showerror("Lỗi", "Vui lòng nhập danh sách mệnh giá!")
                return

            result, remaining = GreedySolver.solve(amount, denoms)
            
            # Display results
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Số tiền cần đổi: {amount:,}\n")
            self.result_text.insert(tk.END, f"Hệ thống tiền: {mode}\n")
            self.result_text.insert(tk.END, "-" * 40 + "\n")
            
            total_coins = 0
            if result:
                for d in sorted(result.keys(), reverse=True):
                    count = result[d]
                    total_coins += count
                    self.result_text.insert(tk.END, f"Mệnh giá {d:>12,}: {count:>5} tờ\n")
                
                self.result_text.insert(tk.END, "-" * 40 + "\n")
                self.result_text.insert(tk.END, f"TỔNG CỘNG: {total_coins} tờ\n")
            else:
                if amount > 0:
                    self.result_text.insert(tk.END, "Không thể đổi bằng các mệnh giá đã cho.\n")
                else:
                    self.result_text.insert(tk.END, "Số tiền là 0, không cần đổi.\n")
            
            if remaining > 0:
                self.result_text.insert(tk.END, f"\nCHÚ Ý: Còn dư {remaining:,} không thể đổi tiếp.\n")

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số tiền hợp lệ (số nguyên dương)!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoinChangeApp(root)
    root.mainloop()
