import tkinter as tk
from tkinter import messagebox
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
        self.root.title("Vacuum Cleaner AI System - Complete 15 Algos")
        self.root.geometry("980x750")

        self.algo_choice = tk.StringVar(value="BFS_1")
        self.grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.path = []
        self.current_step = -1

        self.setup_ui()

    def setup_ui(self):
        left_frame = tk.Frame(self.root, width=240, bg="lightgray", relief=tk.RAISED, borderwidth=2)
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

        center_frame = tk.Frame(self.root, bg="gray")
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

        right_frame = tk.Frame(self.root, width=300, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(right_frame, text="Log", font=("Arial", 16, "bold"), fg="blue").pack(pady=5)
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

    def toggle_cell(self, r, c):
        current = self.grid_state[r][c]
        if current == ' ':
            self.grid_state[r][c] = 'X'
        elif current == 'X':
            self.grid_state[r][c] = 'O'
        else:
            self.grid_state[r][c] = ' '
        self.buttons[r][c].config(text=self.grid_state[r][c])

    def reset_app(self):
        self.grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=" ")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.set_console("Console")
        self.path = []
        self.current_step = -1

    def update_grid_ui(self, state):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=state[r][c])

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

    # ================== CÁC THUẬT TOÁN ĐÃ CÓ ==================
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
            if i == 1:
                current = Node(copy.deepcopy(start_node.state))
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

    # ================== CÁC THUẬT TOÁN MỚI BỔ SUNG ==================

    # 1. Simulated Annealing (Luyện kim)
    def simulated_annealing(self, start_node):
        current = start_node
        T = 100.0
        Tmin = 20.0
        alpha = 0.95
        
        while T > Tmin:
            self.log(f"Xét Node (T={T:.2f}, Rác={self.count_dirt(current.state)}): {current.move if current.move else 'Start'}")
            if self.is_goal(current.state):
                return current
                
            neighbors = self.get_successors(current)
            if not neighbors:
                break
                
            # Chọn ngẫu nhiên một trạng thái lân cận
            next_node = random.choice(neighbors)
            
            # Delta = h(next) - h(current). Hàm h tính theo số ô sai vị trí (số chữ X còn lại)
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
                else:
                    self.log(f"  -> Từ chối trạng thái tệ hơn (p={p:.4f} <= {rand_val:.4f})")
                    
            T = alpha * T
            
        return current

    # 2. Local Beam Search (k=2)
    def local_beam_search(self, start_node, k=2):
        # 1. Khởi tạo: Sinh ngẫu nhiên k trạng thái xuất phát từ Start ban đầu
        current_state_set = []
        
        # Thêm node xuất phát gốc làm node đầu tiên
        current_state_set.append(start_node)
        self.log(f"Khởi tạo chùm: Node 1 (Rác={self.count_dirt(start_node.state)})")
        
        # Sinh thêm (k-1) node ngẫu nhiên lân cận xung quanh bằng cách cho máy đi ngẫu nhiên vài bước
        attempts = 0
        while len(current_state_set) < k and attempts < 20:
            attempts += 1
            temp_node = start_node
            # Cho di chuyển ngẫu nhiên ngẫu hứng từ 1 đến 3 bước
            for _ in range(random.randint(1, 3)):
                succs = self.get_successors(temp_node)
                if succs:
                    temp_node = random.choice(succs)
            if temp_node not in current_state_set:
                current_state_set.append(temp_node)
                self.log(f"Khởi tạo chùm: Node {len(current_state_set)} ngẫu nhiên (Rác={self.count_dirt(temp_node.state)})")

        while True:
            self.log(f"\n--- Vòng lặp chùm hiện tại (Size={len(current_state_set)}) ---")
            neighbor_states = []
            
            # 2.1 Sinh tất cả các trạng thái lân cận của từng State trong Current_State_set
            for node in current_state_set:
                succs = self.get_successors(node)
                for child in succs:
                    if child not in neighbor_states:
                        neighbor_states.append(child)
                        
            self.log(f"  Sinh tổng cộng {len(neighbor_states)} trạng thái lân cận.")
            if not neighbor_states:
                self.log("  -> Không có trạng thái lân cận nào được sinh ra thêm. Dừng thuật toán!")
                return current_state_set[0] if current_state_set else None

            # 2.2 Kiểm tra Đích trong tập Neighbor_States vừa sinh ra
            for neighbor in neighbor_states:
                if self.is_goal(neighbor.state):
                    self.log(f"  -> Tìm thấy ĐÍCH trong chùm lân cận: {neighbor.move}")
                    return neighbor
                    
            # 2.3 Lựa chọn chùm tốt nhất (Nếu chưa tìm thấy Đích)
            # Sắp xếp Neighbor_States theo thứ tự giá trị hàm mục tiêu h tốt dần (số rác tăng dần -> ưu tiên ít rác nhất)
            neighbor_states.sort(key=lambda n: self.count_dirt(n.state))
            
            # Lấy k trạng thái tốt nhất làm tập Current_State_set mới
            current_state_set = neighbor_states[:k]
            
            # Ghi log trạng thái tốt nhất trong chùm hiện tại để theo dõi
            self.log(f"  -> Giữ lại {len(current_state_set)} node tốt nhất. Node tốt nhất hiện có rác = {self.count_dirt(current_state_set[0].state)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumAIApp(root)
    root.mainloop()