import tkinter as tk
from tkinter import messagebox, ttk
import copy
import random
import math
from collections import deque

class Node:
    def __init__(self, state, parent=None, move=None, cost=0, h=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost 
        self.h = h       
        self.f = self.cost + self.h 

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

class VacuumAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacuum Cleaner AI System - Advanced Tabs")
        self.root.geometry("1920x960")

        # Cấu hình Tab điều khiển chính
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="15 Thuật toán Cơ bản")
        self.notebook.add(self.tab2, text="Nhóm thuật toán trong môi trường phức tạp")

        # --- BIẾN TOÀN CỤC TAB 1 ---
        self.algo_choice = tk.StringVar(value="BFS_1")
        self.grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.path = []
        self.current_step = -1

        # --- BIẾN TOÀN CỤC TAB 2 ---
        self.tab2_grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.tab2_paths = {}       # Lưu trữ các đường đi tìm được { 'Goal 1': [...], 'Start 1': [...] }
        self.tab2_current_key = None # Key hiện tại đang chọn hiển thị (Ví dụ: 'Goal 1')
        self.tab2_current_step = -1

        # Setup giao diện cho cả 2 tab
        self.setup_tab1()
        self.setup_tab2()

    # =========================================================================
    # GIAO DIỆN & LOGIC TAB 1 (GIỮ NGUYÊN BẢN GỐC)
    # =========================================================================
    def setup_tab1(self):
        left_frame = tk.Frame(self.tab1, width=240, bg="lightgray", relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left_frame, text="Algorithms", font=("Arial", 14, "bold"), bg="lightgray").pack(pady=10)
        
        algos = [
            ("BFS Cách 1", "BFS_1"), ("BFS Cách 2", "BFS_2"), 
            ("DFS Cách 1", "DFS_1"), ("DFS Cách 2", "DFS_2"),
            ("DLS (Limit=15)", "DLS"), ("UCS", "UCS"),
            ("Greedy Search", "GREEDY"), ("A* Search", "ASTAR"),
            ("IDA* Search", "IDA_STAR"), 
            ("Simple Hill Climbing", "HC_SIMPLE"),
            ("Steepest Ascent HC", "HC_STEEPEST"),
            ("Stochastic HC", "HC_STOCHASTIC"),
            ("Random Restart HC", "HC_RANDOM_RESTART"),
            ("Simulated Annealing", "SIMULATED_ANNEALING"),
            ("Local Beam Search (k=2)", "LOCAL_BEAM")
        ]
                 
        for text, val in algos:
            tk.Radiobutton(left_frame, text=text, variable=self.algo_choice, value=val, 
                           bg="lightgray", font=("Arial", 10), indicatoron=0, 
                           width=22, height=1, selectcolor="lightblue").pack(pady=2, padx=10)

        center_frame = tk.Frame(self.tab1, bg="gray")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        grid_frame = tk.Frame(center_frame, bg="black")
        grid_frame.pack(pady=20)
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(grid_frame, text=" ", font=("Arial", 24, "bold"), width=4, height=2,
                                command=lambda row=r, col=c: self.toggle_cell(row, col))
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[r][c] = btn

        self.console_label = tk.Label(center_frame, text="Console", bg="white", fg="black", font=("Arial", 12), anchor="w", relief=tk.SUNKEN)
        self.console_label.pack(fill=tk.X, side=tk.BOTTOM, pady=10, padx=20, ipady=5)

        control_frame = tk.Frame(center_frame, bg="gray")
        control_frame.place(relx=0.85, rely=0.5, anchor=tk.CENTER)
        
        tk.Button(control_frame, text="Start", font=("Arial", 9, "bold"), bg="green", fg="white", width=8, height=1, command=self.run_algo).pack(pady=10)
        tk.Button(control_frame, text="Prev", font=("Arial", 9, "bold"), bg="khaki", width=8, height=1, command=self.prev_step).pack(pady=10)
        tk.Button(control_frame, text="Next", font=("Arial", 9, "bold"), bg="khaki", width=8, height=1, command=self.next_step).pack(pady=10)
        tk.Button(control_frame, text="Reset", font=("Arial", 9, "bold"), bg="red", fg="white", width=8, height=1, command=self.reset_app).pack(pady=10)

        right_frame = tk.Frame(self.tab1, width=300, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(right_frame, text="Log", font=("Arial", 16, "bold"), fg="blue").pack(pady=5)
        self.log_text = tk.Text(right_frame, width=38, state=tk.DISABLED, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # =========================================================================
    # GIAO DIỆN & LOGIC TAB 2: MÔI TRƯỜNG PHỨC TẠP (THÊM MỚI)
    # =========================================================================
    def setup_tab2(self):
        # Khung trái điều khiển các chức năng phức tạp
        left_frame = tk.Frame(self.tab2, width=260, bg="#e6e6e6", relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(left_frame, text="Môi Trường Phức Tạp", font=("Arial", 13, "bold"), bg="#e6e6e6", fg="darkgreen").pack(pady=10)
        
        # Nhóm chức năng 1
        lb1 = tk.LabelFrame(left_frame, text="Yêu cầu 1: Nhập Start -> 3 Đích", font=("Arial", 10, "bold"), bg="#e6e6e6", fg="blue")
        lb1.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(lb1, text="Hãy thiết lập Start trên lưới bên\nsau đó bấm nút chạy bên dưới.", font=("Arial", 9, "italic"), bg="#e6e6e6").pack(pady=5)
        tk.Button(lb1, text="Chạy Yêu cầu 1", bg="dodgerblue", fg="white", font=("Arial", 10, "bold"), command=self.run_complex_req1).pack(pady=5, padx=10, fill=tk.X)
        
        # Nhóm chức năng 2
        lb2 = tk.LabelFrame(left_frame, text="Yêu cầu 2: 3 Start -> Đích Sạch", font=("Arial", 10, "bold"), bg="#e6e6e6", fg="purple")
        lb2.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(lb2, text="Hệ thống tự sinh ngẫu nhiên lưới.", font=("Arial", 9, "italic"), bg="#e6e6e6").pack(pady=5)
        tk.Button(lb2, text="Chạy Yêu cầu 2", bg="purple", fg="white", font=("Arial", 10, "bold"), command=self.run_complex_req2).pack(pady=5, padx=10, fill=tk.X)

        # Bộ chọn xem lộ trình sau khi chạy xong
        self.route_select_frame = tk.LabelFrame(left_frame, text="Xem Lộ Trình Chi Tiết", font=("Arial", 10, "bold"), bg="#e6e6e6")
        self.route_select_frame.pack(fill=tk.X, padx=10, pady=15)
        self.route_combo = ttk.Combobox(self.route_select_frame, state="disabled")
        self.route_combo.pack(pady=5, padx=10, fill=tk.X)
        self.route_combo.bind("<<ComboboxSelected>>", self.on_route_changed)

        # Khung trung tâm chứa bản đồ lưới hiển thị bước đi
        center_frame = tk.Frame(self.tab2, bg="silver")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        grid_frame = tk.Frame(center_frame, bg="black")
        grid_frame.pack(pady=20)
        
        self.tab2_buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(grid_frame, text=" ", font=("Arial", 24, "bold"), width=4, height=2,
                                command=lambda row=r, col=c: self.toggle_tab2_cell(row, col))
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.tab2_buttons[r][c] = btn

        self.tab2_console = tk.Label(center_frame, text="Vui lòng thiết lập bản đồ hoặc chọn thuật toán.", bg="white", fg="black", font=("Arial", 11), anchor="w", relief=tk.SUNKEN)
        self.tab2_console.pack(fill=tk.X, side=tk.BOTTOM, pady=10, padx=20, ipady=5)

        # Nút điều khiển bước đi (Next / Prev / Reset) cho Tab 2
        control_frame = tk.Frame(center_frame, bg="silver")
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="◀ Bước trước", font=("Arial", 10, "bold"), bg="khaki", width=12, command=self.tab2_prev_step).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Bước sau ▶", font=("Arial", 10, "bold"), bg="khaki", width=12, command=self.tab2_next_step).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Xóa sạch lưới", font=("Arial", 10, "bold"), bg="red", fg="white", width=12, command=self.reset_tab2).pack(side=tk.LEFT, padx=10)

        # Khung Log bên phải của Tab 2
        right_frame = tk.Frame(self.tab2, width=320, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(right_frame, text="Nhật Ký Thực Thi (Tab 2)", font=("Arial", 12, "bold"), fg="darkgreen").pack(pady=5)
        self.tab2_log_text = tk.Text(right_frame, width=38, state=tk.DISABLED, font=("Consolas", 9))
        self.tab2_log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log_tab2(self, message):
        self.tab2_log_text.config(state=tk.NORMAL)
        self.tab2_log_text.insert(tk.END, message + "\n")
        self.tab2_log_text.see(tk.END)
        self.tab2_log_text.config(state=tk.DISABLED)

    def toggle_tab2_cell(self, r, c):
        # Nếu đang xem kết quả (combobox mở) thì tạm thời chặn tương tác sửa lưới cho đến khi reset
        if self.route_combo['state'] == 'normal' and self.tab2_current_key is not None:
            self.tab2_console.config(text="Hãy bấm 'Xóa sạch lưới' trước khi muốn tự liên kết lại thiết lập!", fg="red")
            return
        current = self.tab2_grid_state[r][c]
        if current == ' ': self.tab2_grid_state[r][c] = 'X'
        elif current == 'X': self.tab2_grid_state[r][c] = 'O'
        else: self.tab2_grid_state[r][c] = ' '
        self.tab2_buttons[r][c].config(text=self.tab2_grid_state[r][c])

    def update_tab2_grid_ui(self, state):
        for r in range(3):
            for c in range(3):
                self.tab2_buttons[r][c].config(text=state[r][c])

    def reset_tab2(self):
        self.tab2_grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.update_tab2_grid_ui(self.tab2_grid_state)
        self.tab2_log_text.config(state=tk.NORMAL)
        self.tab2_log_text.delete(1.0, tk.END)
        self.tab2_log_text.config(state=tk.DISABLED)
        self.tab2_console.config(text="Đã xóa sạch lưới Tab 2.", fg="black")
        self.tab2_paths = {}
        self.tab2_current_key = None
        self.tab2_current_step = -1
        self.route_combo['values'] = []
        self.route_combo.set('')
        self.route_combo['state'] = 'disabled'

    # =========================================================================
    # CHẠY CÁC YÊU CẦU PHỨC TẠP (YÊU CẦU 1 & 2)
    # =========================================================================
    def run_complex_req1(self):
        """ Yêu cầu 1: Nhập vào Start chủ động, tự sinh ra 3 Đích ngẫu nhiên và dùng BFS """
        o_count = sum(row.count('O') for row in self.tab2_grid_state)
        if o_count != 1:
            self.tab2_console.config(text="Lỗi: Lưới phải có đúng 1 máy hút bụi 'O' làm trạng thái Start!", fg="red")
            return

        self.tab2_log_text.config(state=tk.NORMAL)
        self.tab2_log_text.delete(1.0, tk.END)
        self.tab2_log_text.config(state=tk.DISABLED)
        self.tab2_paths = {}

        start_node = Node(copy.deepcopy(self.tab2_grid_state))
        self.log_tab2("=== THỰC THI YÊU CẦU 1: BFS TỚI 3 ĐÍCH NGẪU NHIÊN ===")

        # Sinh ngẫu nhiên 3 đích khác nhau
        goals_generated = []
        attempts = 0
        while len(goals_generated) < 3 and attempts < 100:
            attempts += 1
            # Đích ngẫu nhiên có 1 'O' và số lượng rác ngẫu nhiên (từ 0 đến 3 cục rác)
            num_x = random.randint(0, 3)
            g_state = self.generate_random_state(num_x)
            if g_state not in goals_generated and g_state != start_node.state:
                goals_generated.append(g_state)

        if len(goals_generated) < 3:
            self.tab2_console.config(text="Lỗi sinh ngẫu nhiên trạng thái đích, hãy thử lại!", fg="red")
            return

        # Thực hiện tìm kiếm BFS cho từng đích một
        combo_options = []
        for idx, target_state in enumerate(goals_generated):
            key = f"Đích ngẫu nhiên {idx+1}"
            self.log_tab2(f"\n* Đang tìm kiếm đường đi tới [{key}]:")
            
            # Hàm kiểm tra đạt mục tiêu cụ thể
            def specific_goal_check(s): return s == target_state

            path = self.bfs_generic(start_node, specific_goal_check)
            if path:
                self.tab2_paths[key] = path
                combo_options.append(key)
                moves = [n.move for n in path if n.move is not None]
                self.log_tab2(f" -> Thành công! Số bước: {len(path)-1}. Lộ trình: {' -> '.join(moves) if moves else 'Đứng yên'}")
            else:
                self.log_tab2(f" -> Thất bại! Không tìm được đường đi.")

        if combo_options:
            self.route_combo['state'] = 'normal'
            self.route_combo['values'] = combo_options
            self.route_combo.current(0)
            self.on_route_changed(None)
            self.tab2_console.config(text="Chạy hoàn tất Yêu cầu 1! Chọn Đích ở danh sách bên để xem.", fg="green")
        else:
            self.tab2_console.config(text="Không tìm được đường đi tới đích nào!", text_color="red")

    def run_complex_req2(self):
        """ Yêu cầu 2: Không cho nhập start, tự tạo 3 trạng thái start random rồi đi tới đích sạch hoàn toàn """
        self.tab2_log_text.config(state=tk.NORMAL)
        self.tab2_log_text.delete(1.0, tk.END)
        self.tab2_log_text.config(state=tk.DISABLED)
        self.tab2_paths = {}

        self.log_tab2("=== THỰC THI YÊU CẦU 2: 3 START NGẪU NHIÊN -> TRẠNG THÁI ĐÍCH SẠCH BỤI ===")

        # Sinh ngẫu nhiên 3 trạng thái xuất phát khác nhau
        starts_generated = []
        attempts = 0
        while len(starts_generated) < 3 and attempts < 100:
            attempts += 1
            num_x = random.randint(1, 4) # Có từ 1 đến 4 vết rác bẩn để máy dọn dẹp
            s_state = self.generate_random_state(num_x)
            if s_state not in starts_generated and not self.is_goal(s_state):
                starts_generated.append(s_state)

        combo_options = []
        for idx, start_state in enumerate(starts_generated):
            key = f"Trạng thái xuất phát (Start) {idx+1}"
            self.log_tab2(f"\n* Đang tìm kiếm từ [{key}]:")
            
            start_node = Node(copy.deepcopy(start_state))
            # Đi tới trạng thái đích chuẩn (sạch bóng bụi bẩn)
            path = self.bfs_generic(start_node, self.is_goal)
            if path:
                self.tab2_paths[key] = path
                combo_options.append(key)
                moves = [n.move for n in path if n.move is not None]
                self.log_tab2(f" -> Đã tìm ra đường dọn rác! Số bước: {len(path)-1}.\n    Hướng đi: {' -> '.join(moves)}")
            else:
                self.log_tab2(f" -> Không thể giải quyết trạng thái xuất phát này.")

        if combo_options:
            self.route_combo['state'] = 'normal'
            self.route_combo['values'] = combo_options
            self.route_combo.current(0)
            self.on_route_changed(None)
            self.tab2_console.config(text="Chạy hoàn tất Yêu cầu 2! Chọn Khởi đầu ở danh sách bên để xem.", fg="purple")
        else:
            self.tab2_console.config(text="Không tìm thấy lộ trình làm sạch lưới!", fg="red")

    def bfs_generic(self, start_node, goal_check_func):
        """ Hàm lõi BFS tổng quát nhận vào điều kiện check đích linh hoạt """
        frontier = deque([start_node])
        reached = {start_node}
        while frontier:
            node = frontier.popleft()
            if goal_check_func(node.state):
                # Khôi phục lộ trình từ Node kết quả
                path = []
                curr = node
                while curr:
                    path.append(curr)
                    curr = curr.parent
                path.reverse()
                return path
                
            for child in self.get_successors(node):
                if child not in reached:
                    reached.add(child)
                    frontier.append(child)
        return None

    # =========================================================================
    # XỬ LÝ SỰ KIỆN XEM ĐƯỜNG ĐI LÊN / XUỐNG CỦA CÁC CHÙM ĐƯỜNG ĐI
    # =========================================================================
    def on_route_changed(self, event):
        key = self.route_combo.get()
        if key in self.tab2_paths:
            self.tab2_current_key = key
            self.tab2_current_step = 0
            curr_node = self.tab2_paths[key][0]
            self.update_tab2_grid_ui(curr_node.state)
            self.tab2_console.config(text=f"Đang hiển thị [{key}] - Bước 0: Trạng thái ban đầu", fg="black")

    def tab2_prev_step(self):
        if not self.tab2_current_key or self.tab2_current_key not in self.tab2_paths:
            return
        path = self.tab2_paths[self.tab2_current_key]
        if self.tab2_current_step > 0:
            self.tab2_current_step -= 1
            node = path[self.tab2_current_step]
            self.update_tab2_grid_ui(node.state)
            self.tab2_console.config(text=f"[{self.tab2_current_key}] - Bước {self.tab2_current_step}: {node.move if node.move else 'Bắt đầu'}", fg="black")

    def tab2_next_step(self):
        if not self.tab2_current_key or self.tab2_current_key not in self.tab2_paths:
            return
        path = self.tab2_paths[self.tab2_current_key]
        if self.tab2_current_step < len(path) - 1:
            self.tab2_current_step += 1
            node = path[self.tab2_current_step]
            self.update_tab2_grid_ui(node.state)
            self.tab2_console.config(text=f"[{self.tab2_current_key}] - Bước {self.tab2_current_step}: {node.move}", fg="black")

    # =========================================================================
    # CÁC PHƯƠNG THỨC HỖ TRỢ TÍNH TOÁN (GIỮ NGUYÊN TỪ MÃ GỐC)
    # =========================================================================
    def toggle_cell(self, r, c):
        current = self.grid_state[r][c]
        if current == ' ': self.grid_state[r][c] = 'X'
        elif current == 'X': self.grid_state[r][c] = 'O'
        else: self.grid_state[r][c] = ' '
        self.buttons[r][c].config(text=self.grid_state[r][c])

    def reset_app(self):
        self.grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3): self.buttons[r][c].config(text=" ")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.set_console("Console")
        self.path = []
        self.current_step = -1

    def update_grid_ui(self, state):
        for r in range(3):
            for c in range(3): self.buttons[r][c].config(text=state[r][c])

    def prev_step(self):
        if self.path and self.current_step > 0:
            self.current_step -= 1
            self.update_grid_ui(self.path[self.current_step].state)
            self.set_console(f"Step {self.current_step}: {self.path[self.current_step].move}")

    def next_step(self):
        if self.path and self.current_step < len(self.path) - 1:
            self.current_step += 1
            self.update_grid_ui(self.path[self.current_step].state)
            self.set_console(f"Step {self.current_step}: {self.path[self.current_step].move}")

    def is_goal(self, state):
        for row in state:
            if 'X' in row: return False
        return True

    def get_successors(self, node):
        successors = []
        state = node.state
        r_O, c_O = -1, -1
        for r in range(3):
            for c in range(3):
                if state[r][c] == 'O':
                    r_O, c_O = r, c
                    break
            if r_O != -1: break

        moves = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        for move_name, (dr, dc) in moves.items():
            new_r, new_c = r_O + dr, c_O + dc
            if 0 <= new_r < 3 and 0 <= new_c < 3:
                new_state = copy.deepcopy(state)
                new_state[r_O][c_O] = ' '
                new_state[new_r][new_c] = 'O'
                successors.append(Node(new_state, parent=node, move=move_name, cost=node.cost + 1))
        return successors

    def count_dirt(self, state):
        return sum(row.count('X') for row in state)

    def get_value(self, state):
        return -self.count_dirt(state)

    def generate_random_state(self, num_x):
        cells = ['O'] + ['X'] * num_x + [' '] * (8 - num_x)
        random.shuffle(cells)
        return [cells[i:i+3] for i in range(0, 9, 3)]

    def set_console(self, message, error=False):
        color = "red" if error else "black"
        self.console_label.config(text=message, fg=color)

    def run_algo(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        o_count = sum(row.count('O') for row in self.grid_state)
        if o_count != 1:
            self.set_console("Lỗi: Phải có đúng 1 máy hút bụi 'O'!", error=True)
            return
            
        start_node = Node(copy.deepcopy(self.grid_state))
        algo = self.algo_choice.get()
        self.log(f"--- Bắt đầu {algo} ---")
        
        if algo == "BFS_1": goal_node = self.bfs_cach_1(start_node)
        elif algo == "BFS_2": goal_node = self.bfs_cach_2(start_node)
        elif algo == "DFS_1": goal_node = self.dfs_cach_1(start_node)
        elif algo == "DFS_2": goal_node = self.dfs_cach_2(start_node)
        elif algo == "DLS": goal_node = self.dls(start_node, limit=15)
        elif algo == "UCS": goal_node = self.ucs(start_node)
        elif algo == "GREEDY": goal_node = self.solve_greedy(start_node)
        elif algo == "ASTAR": goal_node = self.solve_astar(start_node)
        elif algo == "IDA_STAR": goal_node = self.ida_star(start_node)
        elif algo == "HC_SIMPLE": goal_node = self.simple_hill_climbing(start_node)
        elif algo == "HC_STEEPEST": goal_node = self.steepest_ascent_hill_climbing(start_node)
        elif algo == "HC_STOCHASTIC": goal_node = self.stochastic_hill_climbing(start_node)
        elif algo == "HC_RANDOM_RESTART": goal_node = self.random_restart_hill_climbing(start_node)
        elif algo == "SIMULATED_ANNEALING": goal_node = self.simulated_annealing(start_node)
        elif algo == "LOCAL_BEAM": goal_node = self.local_beam_search(start_node, k=2)
        else: goal_node = None

        if goal_node:
            self.path = []
            curr = goal_node
            while curr:
                self.path.append(curr)
                curr = curr.parent
            self.path.reverse()
            moves = [n.move for n in self.path if n.move is not None]
            if not self.is_goal(goal_node.state):
                self.set_console(f"Kết thúc tại chỗ kẹt! Đường đi: {' -> '.join(moves)}", error=True)
            else:
                self.set_console(f"Đường đi: {' -> '.join(moves)}" if moves else "Đã ở trạng thái đích!")
            self.current_step = 0
            self.update_grid_ui(self.path[0].state)
        else:
            self.set_console("Không tìm thấy đường đi hoặc thuật toán thất bại!", error=True)

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    # 15 Thuật toán gốc của bạn
    def bfs_cach_1(self, start_node):
        frontier = deque([start_node])
        reached = {start_node}
        while frontier:
            node = frontier.popleft()
            self.log(f"Xét Node (Step: {node.cost}): {node.move if node.move else 'Start'}")
            if self.is_goal(node.state): return node
            for child in self.get_successors(node):
                if child not in reached:
                    reached.add(child)
                    frontier.append(child)
        return None

    def bfs_cach_2(self, start_node):
        if self.is_goal(start_node.state): return start_node
        frontier = deque([start_node])
        reached = {start_node}
        while frontier:
            node = frontier.popleft()
            self.log(f"Xét Node (Step: {node.cost}): {node.move if node.move else 'Start'}")
            for child in self.get_successors(node):
                if child not in reached:
                    if self.is_goal(child.state): return child
                    reached.add(child)
                    frontier.append(child)
        return None

    def dfs_cach_1(self, start_node):
        frontier = [start_node]
        reached = {start_node}
        while frontier:
            node = frontier.pop()
            self.log(f"Xét Node (Step: {node.cost}): {node.move if node.move else 'Start'}")
            if self.is_goal(node.state): return node
            for child in self.get_successors(node):
                if child not in reached:
                    reached.add(child)
                    frontier.append(child)
        return None

    def dfs_cach_2(self, start_node):
        if self.is_goal(start_node.state): return start_node
        frontier = [start_node]
        reached = {start_node}
        while frontier:
            node = frontier.pop()
            self.log(f"Xét Node (Step: {node.cost}): {node.move if node.move else 'Start'}")
            for child in self.get_successors(node):
                if child not in reached:
                    if self.is_goal(child.state): return child
                    reached.add(child)
                    frontier.append(child)
        return None

    def dls(self, start_node, limit=15):
        frontier = [start_node]
        reached = {str(start_node.state): 0} 
        while frontier:
            node = frontier.pop()
            self.log(f"Xét Node (Depth: {node.cost}): {node.move if node.move else 'Start'}")
            if self.is_goal(node.state): return node
            if node.cost >= limit: continue
            for child in self.get_successors(node):
                state_str = str(child.state)
                if state_str not in reached or reached[state_str] > child.cost:
                    reached[state_str] = child.cost
                    frontier.append(child)
        return None

    def ucs(self, start_node):
        frontier = [start_node]
        reached = {start_node}
        while frontier:
            frontier.sort(key=lambda n: self.count_dirt(n.state))
            node = frontier.pop(0) 
            self.log(f"Xét Node (Cost rác: {self.count_dirt(node.state)}): {node.move if node.move else 'Start'}")
            if self.is_goal(node.state): return node
            for child in self.get_successors(node):
                if child not in reached:
                    reached.add(child)
                    frontier.append(child)
        return None

    def solve_greedy(self, start_node):
        start_node.h = self.count_dirt(start_node.state)
        frontier = [start_node]
        reached = {str(start_node.state)} 
        while len(frontier) > 0:
            frontier.sort(key=lambda n: n.h)
            current_node = frontier.pop(0)
            self.log(f"Xét Node (h={current_node.h}): {current_node.move if current_node.move else 'Start'}")
            if self.is_goal(current_node.state): return current_node
            for child in self.get_successors(current_node):
                child.h = self.count_dirt(child.state)
                state_str = str(child.state)
                if state_str not in reached:
                    reached.add(state_str)
                    frontier.append(child)
        return None

    def solve_astar(self, start_node):
        start_node.h = self.count_dirt(start_node.state)
        start_node.f = start_node.cost + start_node.h
        if self.is_goal(start_node.state): return start_node
        frontier = [start_node]
        reached = {str(start_node.state): start_node.f}
        while len(frontier) > 0:
            frontier.sort(key=lambda n: (n.f, n.h))
            current_node = frontier.pop(0)
            self.log(f"Xét Node (f={current_node.f}): {current_node.move if current_node.move else 'Start'}")
            if self.is_goal(current_node.state): return current_node
            for child in self.get_successors(current_node):
                child.h = self.count_dirt(child.state)
                child.f = child.cost + child.h
                state_str = str(child.state)
                if state_str not in reached or child.f < reached[state_str]:
                    reached[state_str] = child.f
                    frontier.append(child)
        return None

    def ida_star(self, start_node):
        start_node.h = self.count_dirt(start_node.state)
        start_node.f = start_node.cost + start_node.h
        limit = start_node.f
        while True:
            self.log(f"\n--- Bắt đầu vòng lặp với Limit = {limit} ---")
            path = [start_node]
            temp = self.ida_search(path, 0, limit)
            if temp == "FOUND": return path[-1]
            if temp == float('inf'): return None
            limit = temp

    def ida_search(self, path, g, limit):
        node = path[-1]
        f = g + self.count_dirt(node.state)
        self.log(f"Xét Node (g={g}, h={f-g}, f={f})")
        if f > limit: return f
        if self.is_goal(node.state): return "FOUND"
        min_limit = float('inf')
        for child in self.get_successors(node):
            if child not in path:
                path.append(child)
                temp = self.ida_search(path, g + 1, limit)
                if temp == "FOUND": return "FOUND"
                if temp < min_limit: min_limit = temp
                path.pop()
        return min_limit

    def simple_hill_climbing(self, start_node):
        current = start_node
        while True:
            self.log(f"Current State (Value={self.get_value(current.state)})")
            if self.is_goal(current.state): return current
            found_better = False
            for child in self.get_successors(current):
                if self.get_value(child.state) > self.get_value(current.state):
                    current = child
                    found_better = True
                    self.log(f"  -> Chọn Next_State: {child.move} (Value={self.get_value(child.state)})")
                    break 
            if not found_better:
                self.log("  -> Bị kẹt ở cực đại cục bộ (Local Maxima)")
                return current

    def steepest_ascent_hill_climbing(self, start_node):
        current = start_node
        while True:
            self.log(f"Current State (Value={self.get_value(current.state)})")
            if self.is_goal(current.state): return current
            neighbors = self.get_successors(current)
            if not neighbors: return current
            best_neighbor = max(neighbors, key=lambda n: self.get_value(n.state))
            if self.get_value(best_neighbor.state) > self.get_value(current.state):
                current = best_neighbor
                self.log(f"  -> Chọn Best_Neighbor: {current.move} (Value={self.get_value(current.state)})")
            else:
                self.log("  -> Bị kẹt ở cực đại cục bộ (Local Maxima)")
                return current

    def stochastic_hill_climbing(self, start_node):
        current = start_node
        while True:
            self.log(f"Current State (Value={self.get_value(current.state)})")
            if self.is_goal(current.state): return current
            neighbors = self.get_successors(current)
            better_neighbors = [n for n in neighbors if self.get_value(n.state) > self.get_value(current.state)]
            if not better_neighbors:
                self.log("  -> Bị kẹt ở cực đại cục bộ (Local Maxima)")
                return current
            current = random.choice(better_neighbors)
            self.log(f"  -> Chọn ngẫu nhiên Next_State: {current.move} (Value={self.get_value(current.state)})")

    def random_restart_hill_climbing(self, start_node):
        num_x = self.count_dirt(start_node.state)
        max_restart = 10
        for i in range(1, max_restart + 1):
            self.log(f"\n=== LƯỢT CHẠY THỨ {i}/{max_restart} ===")
            if i == 1: current = Node(copy.deepcopy(start_node.state))
            else:
                current = Node(self.generate_random_state(num_x))
                self.log("-> Khởi tạo lại bản đồ ngẫu nhiên mới!")
            while True:
                if self.is_goal(current.state): return current
                neighbors = self.get_successors(current)
                if not neighbors: break
                better_neighbors = [n for n in neighbors if self.get_value(n.state) > self.get_value(current.state)]
                if not better_neighbors: break
                else:
                    best_neighbor = max(better_neighbors, key=lambda n: self.get_value(n.state))
                    current = best_neighbor
        return current

    def simulated_annealing(self, start_node):
        current = start_node
        T = 100.0
        Tmin = 20.0
        alpha = 0.95
        while T > Tmin:
            self.log(f"Xét Node (T={T:.2f}, Rác={self.count_dirt(current.state)}): {current.move if current.move else 'Start'}")
            if self.is_goal(current.state): return current
            neighbors = self.get_successors(current)
            if not neighbors: break
            next_node = random.choice(neighbors)
            delta = self.count_dirt(next_node.state) - self.count_dirt(current.state)
            if delta < 0:
                current = next_node
                self.log(f"  -> Chấp nhận tốt hơn (Delta={delta}): {current.move}")
            else:
                p = math.exp(-delta / T)
                rand_val = random.random()
                if rand_val < p:
                    current = next_node
                    self.log(f"  -> Chấp nhận tệ hơn với p={p:.4f} > {rand_val:.4f}: {current.move}")
                else: self.log(f"  -> Từ chối trạng thái tệ hơn")
            T = alpha * T
        return current

    def local_beam_search(self, start_node, k=2):
        current_state_set = [start_node]
        self.log(f"Khởi tạo chùm: Node 1 (Rác={self.count_dirt(start_node.state)})")
        attempts = 0
        while len(current_state_set) < k and attempts < 20:
            attempts += 1
            temp_node = start_node
            for _ in range(random.randint(1, 3)):
                succs = self.get_successors(temp_node)
                if succs: temp_node = random.choice(succs)
            if temp_node not in current_state_set:
                current_state_set.append(temp_node)
                self.log(f"Khởi tạo chùm: Node {len(current_state_set)} (Rác={self.count_dirt(temp_node.state)})")
        while True:
            self.log(f"\n--- Vòng lặp chùm hiện tại (Size={len(current_state_set)}) ---")
            neighbor_states = []
            for node in current_state_set:
                for child in self.get_successors(node):
                    if child not in neighbor_states: neighbor_states.append(child)
            if not neighbor_states: return current_state_set[0] if current_state_set else None
            for neighbor in neighbor_states:
                if self.is_goal(neighbor.state): return neighbor
            neighbor_states.sort(key=lambda n: self.count_dirt(n.state))
            current_state_set = neighbor_states[:k]
            self.log(f"  -> Giữ lại {len(current_state_set)} node tốt nhất.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumAIApp(root)
    root.mainloop()