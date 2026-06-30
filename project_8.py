import tkinter as tk
from tkinter import messagebox, ttk
import copy
import random
import math
import time
from collections import deque

# =========================================================================
# LỚP NODE & CÁC HÀM TIC-TAC-TOE ĐỐI KHÁNG
# =========================================================================
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

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != 0:
            return board[condition[0]]
    if 0 not in board: return 0
    return None

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 1: return -10 + depth
    if winner == -1: return 10 - depth
    if winner == 0: return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == 0:
                board[i] = -1
                best_score = max(minimax(board, depth + 1, False), best_score)
                board[i] = 0
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == 0:
                board[i] = 1
                best_score = min(minimax(board, depth + 1, True), best_score)
                board[i] = 0
        return best_score

def alpha_beta(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner == 1: return -10 + depth
    if winner == -1: return 10 - depth
    if winner == 0: return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == 0:
                board[i] = -1
                score = alpha_beta(board, depth + 1, alpha, beta, False)
                board[i] = 0
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha: break 
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == 0:
                board[i] = 1
                score = alpha_beta(board, depth + 1, alpha, beta, True)
                board[i] = 0
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha: break 
        return best_score

# =========================================================================
# LỚP ỨNG DỤNG CHÍNH
# =========================================================================
class VacuumAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacuum Cleaner AI System & Advanced CSP & Adversarial")
        self.root.geometry("1350x850")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.tab3 = tk.Frame(self.notebook)
        self.tab4 = tk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="1. 15 Thuật toán Cơ bản")
        self.notebook.add(self.tab2, text="2. Môi trường phức tạp")
        self.notebook.add(self.tab3, text="3. CSP (Tô màu VN)")
        self.notebook.add(self.tab4, text="4. Cờ Caro (AI)")

        # --- BIẾN TOÀN CỤC TAB 1 & 2 ---
        self.algo_choice = tk.StringVar(value="BFS_1")
        self.grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.path = []
        self.current_step = -1

        self.tab2_grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.tab2_paths = {}       
        self.tab2_current_key = None 
        self.tab2_current_step = -1

        # --- BIẾN TOÀN CỤC TAB 4 ---
        self.caro_board = [0] * 9
        self.caro_algo_choice = tk.StringVar(value="ALPHA_BETA")
        self.caro_status = "Lượt của bạn (X)"

        # --- CẤU HÌNH DỮ LIỆU CSP TAB 3: BẢN ĐỒ VIỆT NAM ---
        self.map_neighbors = {
            "Lai Châu": ["Điện Biên", "Lào Cai", "Sơn La"],
            "Điện Biên": ["Lai Châu", "Sơn La"],
            "Lào Cai": ["Lai Châu", "Tuyên Quang", "Sơn La", "Yên Bái"],
            "Tuyên Quang": ["Lào Cai", "Thái Nguyên", "Phú Thọ"],
            "Sơn La": ["Lai Châu", "Điện Biên", "Lào Cai", "Yên Bái", "Phú Thọ", "Thanh Hóa"],
            "Yên Bái": ["Lào Cai", "Sơn La", "Phú Thọ"],
            "Phú Thọ": ["Tuyên Quang", "Yên Bái", "Sơn La", "Hà Nội"],
            "Thái Nguyên": ["Tuyên Quang", "Lạng Sơn", "Bắc Ninh", "Hà Nội"],
            "Cao Bằng": ["Lạng Sơn"],
            "Lạng Sơn": ["Cao Bằng", "Thái Nguyên", "Bắc Ninh", "Quảng Ninh"],
            "Bắc Ninh": ["Thái Nguyên", "Lạng Sơn", "Hà Nội", "Hải Phòng", "Quảng Ninh"],
            "Quảng Ninh": ["Lạng Sơn", "Bắc Ninh", "Hải Phòng"],
            "Hà Nội": ["Phú Thọ", "Thái Nguyên", "Bắc Ninh", "Hưng Yên", "Hà Nam", "Hòa Bình"],
            "Hải Phòng": ["Bắc Ninh", "Quảng Ninh", "Hưng Yên", "Thái Bình"],
            "Hưng Yên": ["Hà Nội", "Bắc Ninh", "Hải Phòng", "Thái Bình", "Hà Nam"],
            "Thái Bình": ["Hải Phòng", "Hưng Yên", "Hà Nam", "Nam Định"],
            "Hà Nam": ["Hà Nội", "Hưng Yên", "Thái Bình", "Nam Định", "Ninh Bình", "Hòa Bình"],
            "Nam Định": ["Thái Bình", "Hà Nam", "Ninh Bình"],
            "Ninh Bình": ["Hà Nam", "Nam Định", "Hòa Bình", "Thanh Hóa"],
            "Hòa Bình": ["Hà Nội", "Hà Nam", "Ninh Bình", "Sơn La", "Thanh Hóa"],
            "Thanh Hóa": ["Sơn La", "Hòa Bình", "Ninh Bình", "Nghệ An"],
            "Nghệ An": ["Thanh Hóa", "Hà Tĩnh"],
            "Hà Tĩnh": ["Nghệ An", "Quảng Bình"],
            "Quảng Bình": ["Hà Tĩnh", "Quảng Trị"],
            "Quảng Trị": ["Quảng Bình", "Thừa Thiên Huế"],
            "Thừa Thiên Huế": ["Quảng Trị", "Đà Nẵng"],
            "Đà Nẵng": ["Thừa Thiên Huế", "Quảng Nam"],
            "Quảng Nam": ["Đà Nẵng", "Quảng Ngãi", "Kon Tum"],
            "Quảng Ngãi": ["Quảng Nam", "Bình Định", "Kon Tum", "Gia Lai"],
            "Kon Tum": ["Quảng Nam", "Quảng Ngãi", "Gia Lai"],
            "Gia Lai": ["Kon Tum", "Quảng Ngãi", "Bình Định", "Phú Yên", "Đắk Lắk"],
            "Bình Định": ["Quảng Ngãi", "Gia Lai", "Phú Yên"],
            "Phú Yên": ["Bình Định", "Gia Lai", "Khánh Hòa"],
            "Khánh Hòa": ["Phú Yên", "Đắk Lắk", "Lâm Đồng", "Ninh Thuận"],
            "Đắk Lắk": ["Gia Lai", "Khánh Hòa", "Lâm Đồng", "Đắk Nông"],
            "Đắk Nông": ["Đắk Lắk", "Lâm Đồng", "Bình Phước"],
            "Lâm Đồng": ["Đắk Lắk", "Khánh Hòa", "Ninh Thuận", "Bình Thuận", "Đồng Nai", "Đắk Nông"],
            "Ninh Thuận": ["Khánh Hòa", "Lâm Đồng", "Bình Thuận"],
            "Bình Thuận": ["Ninh Thuận", "Lâm Đồng", "Đồng Nai", "Bà Rịa - Vũng Tàu"],
            "Bình Phước": ["Đắk Nông", "Lâm Đồng", "Đồng Nai", "Bình Dương", "Tây Ninh"],
            "Tây Ninh": ["Bình Phước", "Bình Dương", "TP. Hồ Chí Minh", "Long An"],
            "Bình Dương": ["Bình Phước", "Tây Ninh", "TP. Hồ Chí Minh", "Đồng Nai"],
            "Đồng Nai": ["Lâm Đồng", "Bình Thuận", "Bà Rịa - Vũng Tàu", "TP. Hồ Chí Minh", "Bình Dương", "Bình Phước"],
            "Bà Rịa - Vũng Tàu": ["Bình Thuận", "Đồng Nai", "TP. Hồ Chí Minh"],
            "TP. Hồ Chí Minh": ["Tây Ninh", "Bình Dương", "Đồng Nai", "Bà Rịa - Vũng Tàu", "Tiền Giang", "Long An"],
            "Long An": ["Tây Ninh", "TP. Hồ Chí Minh", "Tiền Giang", "Đồng Tháp"],
            "Đồng Tháp": ["Long An", "Tiền Giang", "Vĩnh Long", "Cần Thơ", "An Giang"],
            "An Giang": ["Đồng Tháp", "Cần Thơ", "Kiên Giang"],
            "Tiền Giang": ["Long An", "TP. Hồ Chí Minh", "Đồng Tháp", "Vĩnh Long", "Bến Tre"],
            "Bến Tre": ["Tiền Giang", "Vĩnh Long", "Trà Vinh"],
            "Vĩnh Long": ["Tiền Giang", "Bến Tre", "Trà Vinh", "Sóc Trăng", "Cần Thơ", "Đồng Tháp"],
            "Trà Vinh": ["Bến Tre", "Vĩnh Long", "Sóc Trăng"],
            "Cần Thơ": ["Đồng Tháp", "Vĩnh Long", "Sóc Trăng", "Hậu Giang", "Kiên Giang", "An Giang"],
            "Kiên Giang": ["An Giang", "Cần Thơ", "Hậu Giang", "Bạc Liêu", "Cà Mau"],
            "Hậu Giang": ["Cần Thơ", "Vĩnh Long", "Sóc Trăng", "Bạc Liêu", "Kiên Giang"],
            "Sóc Trăng": ["Vĩnh Long", "Trà Vinh", "Bạc Liêu", "Hậu Giang", "Cần Thơ"],
            "Bạc Liêu": ["Sóc Trăng", "Hậu Giang", "Kiên Giang", "Cà Mau"],
            "Cà Mau": ["Kiên Giang", "Bạc Liêu"]
        }
        
        self.map_polygons = {
            "Lai Châu": [(160, 50), (210, 60), (200, 100), (150, 90)],
            "Điện Biên": [(120, 70), (160, 50), (150, 90), (130, 130)],
            "Lào Cai": [(210, 60), (260, 70), (240, 110), (200, 100)],
            "Tuyên Quang": [(260, 70), (300, 80), (280, 130), (240, 110)],
            "Cao Bằng": [(300, 40), (350, 50), (340, 80), (300, 80)],
            "Lạng Sơn": [(340, 80), (380, 100), (360, 140), (310, 130)],
            "Thái Nguyên": [(300, 80), (340, 80), (310, 130), (280, 130)],
            "Bắc Ninh": [(310, 130), (350, 130), (340, 160), (300, 160)],
            "Quảng Ninh": [(350, 130), (410, 120), (390, 160), (340, 160)],
            "Sơn La": [(150, 90), (200, 100), (240, 110), (230, 140), (220, 180), (170, 140)],
            "Yên Bái": [(200, 100), (240, 110), (230, 140)],
            "Phú Thọ": [(240, 110), (280, 130), (270, 160), (230, 140)],
            "Hà Nội": [(270, 160), (300, 160), (290, 190), (240, 180)],
            "Hải Phòng": [(340, 160), (370, 170), (360, 200), (330, 190)],
            "Hưng Yên": [(300, 160), (340, 160), (330, 190), (290, 190)],
            "Thái Bình": [(330, 190), (370, 170), (360, 220), (320, 220)],
            "Hà Nam": [(290, 190), (330, 190), (320, 220), (280, 220)],
            "Nam Định": [(320, 220), (360, 220), (350, 250), (300, 250)],
            "Ninh Bình": [(280, 220), (320, 220), (300, 250), (270, 240)],
            "Hòa Bình": [(230, 140), (240, 180), (290, 190), (280, 220), (270, 240), (220, 180)],
            "Thanh Hóa": [(220, 180), (270, 240), (300, 250), (290, 280), (210, 250)],
            "Nghệ An": [(210, 250), (290, 280), (270, 320), (200, 290)],
            "Hà Tĩnh": [(270, 320), (310, 320), (290, 360), (240, 350)],
            "Quảng Bình": [(290, 360), (330, 360), (310, 400), (260, 400)],
            "Quảng Trị": [(310, 400), (350, 400), (330, 440), (280, 440)],
            "Thừa Thiên Huế": [(330, 440), (370, 440), (350, 480), (310, 480)],
            "Đà Nẵng": [(350, 480), (390, 480), (380, 510), (340, 510)],
            "Quảng Nam": [(340, 510), (390, 510), (370, 550), (320, 550)],
            "Quảng Ngãi": [(370, 550), (410, 550), (390, 600), (350, 600)],
            "Kon Tum": [(310, 550), (370, 550), (350, 600), (300, 600)],
            "Gia Lai": [(300, 600), (390, 600), (370, 650), (290, 650)],
            "Bình Định": [(390, 600), (430, 600), (410, 650), (370, 650)],
            "Phú Yên": [(370, 650), (420, 650), (400, 690), (360, 690)],
            "Khánh Hòa": [(360, 690), (410, 690), (390, 740), (350, 740)],
            "Đắk Lắk": [(290, 650), (370, 650), (360, 700), (280, 700)],
            "Đắk Nông": [(250, 700), (280, 700), (270, 740), (240, 740)],
            "Lâm Đồng": [(280, 700), (360, 700), (340, 750), (270, 740)],
            "Ninh Thuận": [(340, 740), (380, 740), (370, 780), (330, 780)],
            "Bình Thuận": [(270, 740), (340, 750), (380, 740), (370, 780), (340, 820), (290, 820)],
            "Bình Phước": [(200, 700), (250, 700), (240, 740), (190, 740)],
            "Tây Ninh": [(150, 730), (190, 730), (180, 770), (140, 770)],
            "Bình Dương": [(180, 730), (220, 730), (210, 770), (170, 770)],
            "Đồng Nai": [(220, 700), (270, 700), (250, 770), (210, 770)],
            "Bà Rịa - Vũng Tàu": [(210, 770), (250, 770), (240, 810), (200, 810)],
            "TP. Hồ Chí Minh": [(170, 770), (210, 770), (200, 810), (160, 810)],
            "Long An": [(120, 770), (160, 770), (150, 810), (110, 810)],
            "Đồng Tháp": [(80, 770), (120, 770), (110, 810), (70, 810)],
            "An Giang": [(40, 770), (80, 770), (70, 810), (30, 810)],
            "Tiền Giang": [(110, 810), (160, 810), (140, 840), (100, 840)],
            "Bến Tre": [(140, 810), (180, 810), (170, 840), (130, 840)],
            "Vĩnh Long": [(100, 810), (140, 810), (130, 840), (90, 840)],
            "Trà Vinh": [(120, 840), (160, 840), (150, 870), (110, 870)],
            "Cần Thơ": [(60, 810), (100, 810), (90, 840), (50, 840)],
            "Kiên Giang": [(10, 810), (50, 810), (30, 870), (0, 870)],
            "Hậu Giang": [(50, 840), (90, 840), (80, 870), (40, 870)],
            "Sóc Trăng": [(90, 840), (130, 840), (120, 870), (80, 870)],
            "Bạc Liêu": [(40, 870), (80, 870), (70, 910), (30, 910)],
            "Cà Mau": [(0, 870), (40, 870), (20, 940), (0, 940)]
        }

        max_deg = max(len(v) for v in self.map_neighbors.values())
        self.N_colors_count = max_deg + 1
        
        random.seed(100)
        self.color_palette = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(self.N_colors_count)]
        self.current_assignments = {}

        self.zoom_scale = 0.85  
        self.pan_x = 80
        self.pan_y = 10
        self.drag_start_x = 0
        self.drag_start_y = 0

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        self.setup_tab4()

    # =========================================================================
    # TAB 1: 15 THUẬT TOÁN CƠ BẢN
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

        right_frame = tk.Frame(self.tab1, width=320, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(right_frame, text="Log Tab 1", font=("Arial", 16, "bold"), fg="blue").pack(pady=5)
        self.log_text = tk.Text(right_frame, width=38, state=tk.DISABLED, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def set_console(self, message, error=False):
        color = "red" if error else "black"
        self.console_label.config(text=message, fg=color)
        
    def run_algo(self):
        self.log_text.config(state=tk.NORMAL); self.log_text.delete(1.0, tk.END); self.log_text.config(state=tk.DISABLED)
        
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

    # =========================================================================
    # TAB 2: MÔI TRƯỜNG PHỨC TẠP
    # =========================================================================
    def setup_tab2(self):
        left_frame = tk.Frame(self.tab2, width=280, bg="#e6e6e6", relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left_frame, text="Môi Trường Phức Tạp", font=("Arial", 13, "bold"), bg="#e6e6e6", fg="darkgreen").pack(pady=10)
        
        lb1 = tk.LabelFrame(left_frame, text="Yêu cầu 1: Nhập Start -> 3 Đích", font=("Arial", 10, "bold"), bg="#e6e6e6", fg="blue")
        lb1.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(lb1, text="Chạy Yêu cầu 1 (BFS)", bg="dodgerblue", fg="white", font=("Arial", 9, "bold"), command=self.run_complex_req1).pack(pady=5, padx=10, fill=tk.X)
        
        lb2 = tk.LabelFrame(left_frame, text="Yêu cầu 2: 3 Start -> Đích Sạch", font=("Arial", 10, "bold"), bg="#e6e6e6", fg="purple")
        lb2.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(lb2, text="Chạy Yêu cầu 2 (BFS Random)", bg="purple", fg="white", font=("Arial", 9, "bold"), command=self.run_complex_req2).pack(pady=5, padx=10, fill=tk.X)
        
        lb3 = tk.LabelFrame(left_frame, text="Yêu cầu 3: Không Xác Định (AND-OR)", font=("Arial", 10, "bold"), bg="#e6e6e6", fg="orange")
        lb3.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(lb3, text="Chạy AND-OR Search", bg="#e67e22", fg="white", font=("Arial", 9, "bold"), command=self.run_complex_req3).pack(pady=5, padx=10, fill=tk.X)
        
        self.route_select_frame = tk.LabelFrame(left_frame, text="Xem Lộ Trình Chi Tiết", font=("Arial", 10, "bold"), bg="#e6e6e6")
        self.route_select_frame.pack(fill=tk.X, padx=10, pady=10)
        self.route_combo = ttk.Combobox(self.route_select_frame, state="disabled")
        self.route_combo.pack(pady=5, padx=10, fill=tk.X)
        self.route_combo.bind("<<ComboboxSelected>>", self.on_route_changed)
        
        center_frame = tk.Frame(self.tab2, bg="silver")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        grid_frame = tk.Frame(center_frame, bg="black")
        grid_frame.pack(pady=20)
        
        self.tab2_buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(grid_frame, text=" ", font=("Arial", 24, "bold"), width=4, height=2, command=lambda row=r, col=c: self.toggle_tab2_cell(row, col))
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.tab2_buttons[r][c] = btn
                
        self.tab2_console = tk.Label(center_frame, text="Console", bg="white", fg="black", font=("Arial", 11), anchor="w", relief=tk.SUNKEN)
        self.tab2_console.pack(fill=tk.X, side=tk.BOTTOM, pady=10, padx=20, ipady=5)
        
        control_frame = tk.Frame(center_frame, bg="silver")
        control_frame.pack(pady=5)
        tk.Button(control_frame, text="◀ Bước trước", font=("Arial", 9, "bold"), bg="khaki", width=11, command=self.tab2_prev_step).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Bước sau ▶", font=("Arial", 9, "bold"), bg="khaki", width=11, command=self.tab2_next_step).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Xóa sạch lưới", font=("Arial", 9, "bold"), bg="red", fg="white", width=11, command=self.reset_tab2).pack(side=tk.LEFT, padx=5)
        
        right_frame = tk.Frame(self.tab2, width=340, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.tab2_log_text = tk.Text(right_frame, width=42, state=tk.DISABLED, font=("Consolas", 9))
        self.tab2_log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log_tab2(self, message):
        self.tab2_log_text.config(state=tk.NORMAL)
        self.tab2_log_text.insert(tk.END, message + "\n")
        self.tab2_log_text.see(tk.END)
        self.tab2_log_text.config(state=tk.DISABLED)

    def toggle_tab2_cell(self, r, c):
        current = self.tab2_grid_state[r][c]
        if current == ' ': self.tab2_grid_state[r][c] = 'X'
        elif current == 'X': self.tab2_grid_state[r][c] = 'O'
        else: self.tab2_grid_state[r][c] = ' '
        self.tab2_buttons[r][c].config(text=self.tab2_grid_state[r][c])

    def update_tab2_grid_ui(self, state):
        for r in range(3):
            for c in range(3): self.tab2_buttons[r][c].config(text=state[r][c])

    def reset_tab2(self):
        self.tab2_grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.update_tab2_grid_ui(self.tab2_grid_state)
        self.tab2_log_text.config(state=tk.NORMAL)
        self.tab2_log_text.delete(1.0, tk.END)
        self.tab2_log_text.config(state=tk.DISABLED)
        self.tab2_paths = {}
        self.tab2_current_key = None
        self.route_combo['values'] = []
        self.route_combo.set('')
        self.route_combo['state'] = 'disabled'

    def run_complex_req1(self):
        self.tab2_paths = {}
        start_node = Node(copy.deepcopy(self.tab2_grid_state))
        goals_generated = []
        while len(goals_generated) < 3:
            g_state = self.generate_random_state(random.randint(0, 3))
            if g_state not in goals_generated: goals_generated.append(g_state)
        combo_options = []
        for idx, target_state in enumerate(goals_generated):
            key = f"Đích ngẫu nhiên {idx+1}"
            path = self.bfs_generic(start_node, lambda s: s == target_state)
            if path: 
                self.tab2_paths[key] = path
                combo_options.append(key)
        self.route_combo['state'] = 'normal'
        self.route_combo['values'] = combo_options
        if combo_options:
            self.route_combo.current(0)
            self.on_route_changed(None)

    def run_complex_req2(self):
        self.tab2_paths = {}
        starts_generated = []
        while len(starts_generated) < 3:
            s_state = self.generate_random_state(random.randint(1, 4))
            if s_state not in starts_generated and not self.is_goal(s_state): 
                starts_generated.append(s_state)
        combo_options = []
        for idx, start_state in enumerate(starts_generated):
            key = f"Start ngẫu nhiên {idx+1}"
            path = self.bfs_generic(Node(start_state), self.is_goal)
            if path: 
                self.tab2_paths[key] = path
                combo_options.append(key)
        self.route_combo['state'] = 'normal'
        self.route_combo['values'] = combo_options
        if combo_options:
            self.route_combo.current(0)
            self.on_route_changed(None)

    def run_complex_req3(self):
        self.tab2_log_text.config(state=tk.NORMAL)
        self.tab2_log_text.delete(1.0, tk.END)
        plan = self.or_search(copy.deepcopy(self.tab2_grid_state), [])
        if plan == "FAILURE": 
            self.log_tab2("AND-OR Search: Thất bại!")
        else: 
            self.print_and_or_plan(plan, 0)

    def or_search(self, state, path):
        if self.is_goal(state): return []
        if state in path: return "FAILURE"
        actions = list(set([succ.move for succ in self.get_successors(Node(state))]))
        for action in actions:
            results = self.get_nondeterministic_results(state, action)
            plan = self.and_search(results, path + [state])
            if plan != "FAILURE": return [action, plan]
        return "FAILURE"

    def and_search(self, states, path):
        plan = {}
        for state in states:
            plan_state = self.or_search(state, path)
            if plan_state == "FAILURE": return "FAILURE"
            plan[str(state)] = plan_state
        return plan

    def get_nondeterministic_results(self, state, action):
        results = []
        successors = self.get_successors(Node(state))
        target = [s.state for s in successors if s.move == action]
        if target: results.append(target[0])
        other = [s.state for s in successors if s.move != action]
        if other: results.append(random.choice(other))
        return results[:2]

    def print_and_or_plan(self, plan, indent):
        space = " " * indent
        if plan == []: 
            self.log_tab2(f"{space}└─ Đích sạch rác.")
            return
        action, and_plan = plan
        self.log_tab2(f"{space}└─ Đi: {action}")
        if isinstance(and_plan, dict):
            for k, sub in and_plan.items(): 
                self.print_and_or_plan(sub, indent + 4)

    def bfs_generic(self, start_node, goal_check):
        frontier = deque([start_node])
        reached = {start_node}
        while frontier:
            node = frontier.popleft()
            if goal_check(node.state):
                path = []
                while node: 
                    path.append(node)
                    node = node.parent
                return path[::-1]
            for child in self.get_successors(node):
                if child not in reached: 
                    reached.add(child)
                    frontier.append(child)
        return None

    def on_route_changed(self, event):
        key = self.route_combo.get()
        if key in self.tab2_paths: 
            self.tab2_current_key = key
            self.tab2_current_step = 0
            self.update_tab2_grid_ui(self.tab2_paths[key][0].state)

    def tab2_prev_step(self):
        if self.tab2_current_key and self.tab2_current_step > 0:
            self.tab2_current_step -= 1
            self.update_tab2_grid_ui(self.tab2_paths[self.tab2_current_key][self.tab2_current_step].state)

    def tab2_next_step(self):
        if self.tab2_current_key and self.tab2_current_step < len(self.tab2_paths[self.tab2_current_key]) - 1:
            self.tab2_current_step += 1
            self.update_tab2_grid_ui(self.tab2_paths[self.tab2_current_key][self.tab2_current_step].state)

    # =========================================================================
    # TAB 3: TÌM KIẾM CÓ RÀNG BUỘC (CSP TÔ MÀU BẢN ĐỒ VIỆT NAM)
    # =========================================================================
    def setup_tab3(self):
        left_frame = tk.Frame(self.tab3, width=280, bg="#f0f0f0", relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left_frame, text="Tô Màu Bản Đồ Việt Nam", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="darkblue").pack(pady=10)
        
        info_frame = tk.LabelFrame(left_frame, text="Thông số bài toán", font=("Arial", 9, "bold"), bg="#f0f0f0")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(info_frame, text=f"- Số tỉnh thành: {len(self.map_neighbors)}", bg="#f0f0f0", anchor="w").pack(fill=tk.X, padx=5)
        tk.Label(info_frame, text=f"- Số màu tối thiểu (N=M+1): {self.N_colors_count}", font=("Arial", 9, "bold"), bg="#f0f0f0", fg="red", anchor="w").pack(fill=tk.X, padx=5)

        algo_frame = tk.LabelFrame(left_frame, text="Chọn Thuật Toán", font=("Arial", 9, "bold"), bg="#f0f0f0")
        algo_frame.pack(fill=tk.X, padx=10, pady=5)
        self.csp_algo_choice = tk.StringVar(value="BACKTRACKING")
        tk.Radiobutton(algo_frame, text="Chạy Backtracking", variable=self.csp_algo_choice, value="BACKTRACKING", bg="#f0f0f0").pack(anchor="w", padx=5, pady=2)
        tk.Radiobutton(algo_frame, text="Chạy Forward Checking", variable=self.csp_algo_choice, value="FORWARD_CHECKING", bg="#f0f0f0").pack(anchor="w", padx=5, pady=2)
        tk.Radiobutton(algo_frame, text="Sàng lọc AC-3 + Cây tìm kiếm", variable=self.csp_algo_choice, value="AC3", bg="#f0f0f0").pack(anchor="w", padx=5, pady=2)
        tk.Radiobutton(algo_frame, text="Tìm kiếm cục bộ Min-Conflicts", variable=self.csp_algo_choice, value="MIN_CONFLICTS", bg="#f0f0f0").pack(anchor="w", padx=5, pady=2)

        btn_frame = tk.Frame(left_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(btn_frame, text="Xem bản đồ trước khi tô", bg="gray", fg="white", font=("Arial", 9, "bold"), command=self.show_uncolored_map).pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="Giải toán & Tô màu bản đồ", bg="green", fg="white", font=("Arial", 10, "bold"), command=self.run_csp_coloring).pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="Đặt lại (Reset Zoom)", bg="red", fg="white", font=("Arial", 9, "bold"), command=self.reset_tab3).pack(fill=tk.X, pady=3)

        guide_frame = tk.LabelFrame(left_frame, text="Hướng dẫn tương tác", font=("Arial", 9, "bold"), bg="#f0f0f0", fg="brown")
        guide_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(guide_frame, text="• Cuộn chuột giữa: Zoom\n• Nhấn giữ & Kéo chuột trái: Di chuyển", justify=tk.LEFT, bg="#f0f0f0", font=("Arial", 9)).pack(padx=5, pady=5)

        self.canvas_frame = tk.Frame(self.tab3, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.canvas_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.canvas = tk.Canvas(self.canvas_frame, bg="#eef2f7", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_canvas_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag_move)
        self.canvas.bind("<MouseWheel>", self.on_canvas_zoom)

        right_frame = tk.Frame(self.tab3, width=280, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(right_frame, text="Nhật Ký CSP Việt Nam", font=("Arial", 12, "bold"), fg="blue").pack(pady=5)
        self.tab3_log_text = tk.Text(right_frame, width=32, state=tk.DISABLED, font=("Consolas", 9))
        self.tab3_log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.show_uncolored_map()

    def log_tab3(self, message):
        self.tab3_log_text.config(state=tk.NORMAL)
        self.tab3_log_text.insert(tk.END, message + "\n")
        self.tab3_log_text.config(state=tk.DISABLED)

    def run_csp_coloring(self):
        self.tab3_log_text.config(state=tk.NORMAL)
        self.tab3_log_text.delete(1.0, tk.END)
        self.tab3_log_text.config(state=tk.DISABLED)
        
        algo = self.csp_algo_choice.get()
        self.log_tab3(f"--- Đang khởi động thuật toán: {algo} ---")
        
        variables = list(self.map_neighbors.keys())
        domains = {v: list(range(self.N_colors_count)) for v in variables}
        assignment = {}
        self.csp_steps_count = 0
        success = False

        if algo == "BACKTRACKING":
            success = self.backtracking_csp(assignment, variables, domains)
        elif algo == "FORWARD_CHECKING":
            success = self.forward_checking_csp(assignment, variables, domains)
        elif algo == "AC3":
            self.log_tab3(" -> Đang chạy sàng lọc nhất quán cung AC-3...")
            if self.ac3_algorithm(domains):
                self.log_tab3(" -> AC-3 hoàn tất! Tiếp tục gán nghiệm tối ưu hóa không gian.")
                success = self.backtracking_csp(assignment, variables, domains)
            else:
                self.log_tab3(" -> AC-3 phát hiện mâu thuẫn miền giá trị ngay từ đầu!")
        elif algo == "MIN_CONFLICTS":
            self.log_tab3(" -> Đang chạy Tìm kiếm cục bộ Min-Conflicts...")
            assignment = self.min_conflicts_algorithm(max_steps=1500)
            success = assignment is not None

        if success:
            self.log_tab3(f"\n=> ĐÃ HOÀN THÀNH!")
            self.log_tab3(f"Số bước lặp / duyệt node: {self.csp_steps_count}")
            self.current_assignments = {var: self.color_palette[color_idx] for var, color_idx in assignment.items()}
            self.redraw_map()
        else:
            messagebox.showerror("Kết quả", "Thuật toán không tìm ra phương án hoặc vượt quá giới hạn bước lặp!")

    def ac3_algorithm(self, domains):
        queue = deque()
        for xi in self.map_neighbors:
            for xj in self.map_neighbors[xi]:
                queue.append((xi, xj))
        while queue:
            xi, xj = queue.popleft()
            if self.rm_inconsistent_values(xi, xj, domains):
                if not domains[xi]: return False
                for xk in self.map_neighbors[xi]:
                    if xk != xj: queue.append((xk, xi))
        return True

    def rm_inconsistent_values(self, xi, xj, domains):
        removed = False
        for x in list(domains[xi]):
            if all(x == y for y in domains[xj]):
                domains[xi].remove(x)
                removed = True
        return removed

    def min_conflicts_algorithm(self, max_steps=1500):
        variables = list(self.map_neighbors.keys())
        current = {v: random.randint(0, self.N_colors_count - 1) for v in variables}
        for i in range(1, max_steps + 1):
            self.csp_steps_count = i
            if self.check_solution_valid(current): return current
            conflicted_vars = [v for v in variables if any(n in current and current[n] == current[v] for n in self.map_neighbors[v])]
            if not conflicted_vars: return current
            var = random.choice(conflicted_vars)
            best_value = current[var]
            min_conflict_score = float('inf')
            possible_values = list(range(self.N_colors_count))
            random.shuffle(possible_values) 
            for val in possible_values:
                conflicts = sum(1 for neighbor in self.map_neighbors[var] if neighbor in current and current[neighbor] == val)
                if conflicts < min_conflict_score:
                    min_conflict_score = conflicts
                    best_value = val
            current[var] = best_value
        return None

    def check_solution_valid(self, assignment):
        for var in self.map_neighbors:
            for neighbor in self.map_neighbors[var]:
                if assignment.get(var) == assignment.get(neighbor): return False
        return True

    def backtracking_csp(self, assignment, variables, domains):
        self.csp_steps_count += 1
        if len(assignment) == len(variables): return True
        var = [v for v in variables if v not in assignment][0]
        for value in domains[var]:
            if all(n not in assignment or assignment[n] != value for n in self.map_neighbors[var]):
                assignment[var] = value
                if self.backtracking_csp(assignment, variables, domains): return True
                del assignment[var]
        return False

    def forward_checking_csp(self, assignment, variables, domains):
        self.csp_steps_count += 1
        if len(assignment) == len(variables): return True
        var = [v for v in variables if v not in assignment][0]
        for value in domains[var]:
            if all(n not in assignment or assignment[n] != value for n in self.map_neighbors[var]):
                assignment[var] = value
                local_domains = copy.deepcopy(domains)
                failure = False
                for neighbor in self.map_neighbors[var]:
                    if neighbor not in assignment and value in local_domains[neighbor]:
                        local_domains[neighbor].remove(value)
                        if not local_domains[neighbor]: 
                            failure = True
                            break
                if not failure and self.forward_checking_csp(assignment, variables, local_domains): return True
                del assignment[var]
        return False

    def show_uncolored_map(self):
        self.current_assignments = {var: "#fce9cc" for var in self.map_neighbors.keys()}
        self.redraw_map()

    def reset_tab3(self):
        self.zoom_scale = 0.85
        self.pan_x = 80
        self.pan_y = 10
        self.show_uncolored_map()

    def redraw_map(self):
        self.canvas.delete("all")
        for name, points in self.map_polygons.items():
            t_points = [(x * self.zoom_scale + self.pan_x, y * self.zoom_scale + self.pan_y) for (x, y) in points]
            self.canvas.create_polygon(t_points, fill=self.current_assignments.get(name, "#fce9cc"), outline="#333333", width=1)
            cx, cy = sum(p[0] for p in t_points) / len(t_points), sum(p[1] for p in t_points) / len(t_points)
            self.canvas.create_text(cx, cy, text=name, font=("Arial", max(6, int(7.5 * self.zoom_scale)), "bold"), fill="#111111")

    def on_canvas_drag_start(self, event):
        self.drag_start_x, self.drag_start_y = event.x, event.y

    def on_canvas_drag_move(self, event):
        self.pan_x += event.x - self.drag_start_x
        self.pan_y += event.y - self.drag_start_y
        self.drag_start_x, self.drag_start_y = event.x, event.y
        self.redraw_map()

    def on_canvas_zoom(self, event):
        self.zoom_scale *= 1.1 if event.delta > 0 else 0.9
        self.zoom_scale = max(0.2, min(self.zoom_scale, 4.0))
        self.redraw_map()

    # =========================================================================
    # TAB 4: TÌM KIẾM ĐỐI KHÁNG (CỜ CARO 3X3)
    # =========================================================================
    def setup_tab4(self):
        left_frame = tk.Frame(self.tab4, width=280, bg="lightgray", relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left_frame, text="AI Đối Kháng (Caro 3x3)", font=("Arial", 14, "bold"), bg="lightgray").pack(pady=10)
        
        algo_frame = tk.LabelFrame(left_frame, text="Chọn Thuật Toán AI", font=("Arial", 10, "bold"), bg="lightgray")
        algo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Radiobutton(algo_frame, text="Minimax (Thuần túy)", variable=self.caro_algo_choice, value="MINIMAX", bg="lightgray", font=("Arial", 10)).pack(anchor="w", padx=5, pady=2)
        tk.Radiobutton(algo_frame, text="Alpha-Beta Pruning", variable=self.caro_algo_choice, value="ALPHA_BETA", bg="lightgray", font=("Arial", 10)).pack(anchor="w", padx=5, pady=2)

        tk.Button(left_frame, text="Chơi Ván Mới", font=("Arial", 10, "bold"), bg="green", fg="white", command=self.reset_caro).pack(pady=20, padx=10, fill=tk.X)

        center_frame = tk.Frame(self.tab4, bg="silver")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.caro_status_label = tk.Label(center_frame, text=self.caro_status, font=("Arial", 18, "bold"), bg="silver", fg="blue")
        self.caro_status_label.pack(pady=20)
        
        grid_frame = tk.Frame(center_frame, bg="black")
        grid_frame.pack(pady=10)
        
        self.caro_buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(grid_frame, text=" ", font=("Arial", 40, "bold"), width=3, height=1,
                                command=lambda row=r, col=c: self.on_caro_click(row, col))
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.caro_buttons[r][c] = btn

        right_frame = tk.Frame(self.tab4, width=320, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(right_frame, text="Nhật Ký Suy Nghĩ AI", font=("Arial", 12, "bold"), fg="darkgreen").pack(pady=5)
        self.tab4_log_text = tk.Text(right_frame, width=42, state=tk.DISABLED, font=("Consolas", 9))
        self.tab4_log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log_tab4(self, message):
        self.tab4_log_text.config(state=tk.NORMAL)
        self.tab4_log_text.insert(tk.END, message + "\n")
        self.tab4_log_text.see(tk.END)
        self.tab4_log_text.config(state=tk.DISABLED)

    def update_caro_ui(self):
        self.caro_status_label.config(text=self.caro_status)
        for i in range(9):
            r, c = divmod(i, 3)
            val = self.caro_board[i]
            txt = " " if val == 0 else "X" if val == 1 else "O"
            color = "black" if val == 0 else "blue" if val == 1 else "red"
            self.caro_buttons[r][c].config(text=txt, fg=color)

    def reset_caro(self):
        self.caro_board = [0] * 9
        self.caro_status = "Lượt của bạn (X)"
        self.update_caro_ui()
        self.tab4_log_text.config(state=tk.NORMAL)
        self.tab4_log_text.delete(1.0, tk.END)
        self.tab4_log_text.config(state=tk.DISABLED)
        self.log_tab4("Đã khởi tạo ván mới. Bạn đánh trước (X).")

    def on_caro_click(self, r, c):
        if check_winner(self.caro_board) is not None: return
        idx = r * 3 + c
        if self.caro_board[idx] == 0:
            self.caro_board[idx] = 1 # Người chơi X
            self.log_tab4(f"\nBạn đánh X ở ô ({r}, {c})")
            self.caro_status = "AI đang suy nghĩ..."
            self.update_caro_ui()
            
            if not self.check_caro_end():
                self.root.after(200, self.ai_caro_turn)

    def ai_caro_turn(self):
        algo = self.caro_algo_choice.get()
        start_t = time.perf_counter()
        
        self.log_tab4(f"--- AI ({algo}) ĐANG ĐÁNH GIÁ ---")
        best_score = -math.inf
        best_move = -1
        
        for i in range(9):
            if self.caro_board[i] == 0:
                self.caro_board[i] = -1 
                
                if algo == "MINIMAX":
                    score = minimax(self.caro_board, 0, False)
                else:
                    score = alpha_beta(self.caro_board, 0, -math.inf, math.inf, False)
                    
                self.caro_board[i] = 0 
                
                kq = "THẮNG" if score > 0 else "THUA" if score < 0 else "HÒA"
                r, c = divmod(i, 3)
                self.log_tab4(f" + Thử ô ({r}, {c}) -> Điểm: {score:2} (Dự đoán: {kq})")
                
                if score > best_score:
                    best_score = score
                    best_move = i
                    
        if best_move != -1:
            self.caro_board[best_move] = -1
            r, c = divmod(best_move, 3)
            self.log_tab4(f"=> AI QUYẾT ĐỊNH ĐÁNH Ô ({r}, {c}) (Time: {round(time.perf_counter() - start_t, 3)}s)")

        self.caro_status = "Lượt của bạn (X)"
        self.update_caro_ui()
        self.check_caro_end()

    def check_caro_end(self):
        w = check_winner(self.caro_board)
        if w is not None:
            status = "CHÚC MỪNG! BẠN ĐÃ THẮNG AI!" if w == 1 else "AI ĐÃ CHIẾN THẮNG BẠN!" if w == -1 else "TRẬN ĐẤU HÒA NHAU!"
            self.caro_status = status
            self.update_caro_ui()
            self.log_tab4(f"*** {status} ***\n")
            return True
        return False

    # =========================================================================
    # CÁC HÀM TIỆN ÍCH CORE DÀNH CHO TAB 1 & 2 (ĐÃ BỔ SUNG ĐẦY ĐỦ UPDATE_UI & NEXT/PREV)
    # =========================================================================
    def toggle_cell(self, r, c):
        current = self.grid_state[r][c]
        if current == ' ': self.grid_state[r][c] = 'X'
        elif current == 'X': self.grid_state[r][c] = 'O'
        else: self.grid_state[r][c] = ' '
        self.buttons[r][c].config(text=self.grid_state[r][c])

    def get_successors(self, node):
        successors = []
        state = node.state
        r_O, c_O = -1, -1
        for r in range(3):
            for c in range(3):
                if state[r][c] == 'O': 
                    r_O, c_O = r, c
                    break
        moves = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        for m, (dr, dc) in moves.items():
            nr, nc = r_O + dr, c_O + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                ns = copy.deepcopy(state)
                ns[r_O][c_O] = ' '
                ns[nr][nc] = 'O'
                successors.append(Node(ns, parent=node, move=m, cost=node.cost + 1))
        return successors

    def generate_random_state(self, num_x):
        cells = ['O'] + ['X'] * num_x + [' '] * (8 - num_x)
        random.shuffle(cells)
        return [cells[i:i+3] for i in range(0, 9, 3)]
        
    def count_dirt(self, state):
        return sum(row.count('X') for row in state)

    def get_value(self, state):
        return -self.count_dirt(state)

    def is_goal(self, state):
        return not any('X' in row for row in state)

    def update_grid_ui(self, state):
        for r in range(3):
            for c in range(3): 
                self.buttons[r][c].config(text=state[r][c])

    def reset_app(self):
        self.grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.update_grid_ui(self.grid_state)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.set_console("Console")
        self.path = []
        self.current_step = -1

    def prev_step(self):
        if self.path and self.current_step > 0:
            self.current_step -= 1
            self.update_grid_ui(self.path[self.current_step].state)
            move_name = self.path[self.current_step].move if self.path[self.current_step].move else "Start"
            self.set_console(f"Step {self.current_step}: {move_name}")

    def next_step(self):
        if self.path and self.current_step < len(self.path) - 1:
            self.current_step += 1
            self.update_grid_ui(self.path[self.current_step].state)
            self.set_console(f"Step {self.current_step}: {self.path[self.current_step].move}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumAIApp(root)
    root.mainloop()