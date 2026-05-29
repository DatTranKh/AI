import tkinter as tk
from tkinter import messagebox
import copy
import random
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
        self.root.title("Vacuum Cleaner AI System - Extended")
        self.root.geometry("900x700") # Mở rộng cửa sổ để chứa đủ nút

        self.algo_choice = tk.StringVar(value="BFS_1")
        self.grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.path = []
        self.current_step = -1

        self.setup_ui()

    def setup_ui(self):
        left_frame = tk.Frame(self.root, width=200, bg="lightgray", relief=tk.RAISED, borderwidth=2)
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
            ("Stochastic HC", "HC_STOCHASTIC")
        ]
                 
        for text, val in algos:
            tk.Radiobutton(left_frame, text=text, variable=self.algo_choice, value=val, 
                           bg="lightgray", font=("Arial", 10), indicatoron=0, 
                           width=18, height=1, selectcolor="lightblue").pack(pady=4, padx=10)

        center_frame = tk.Frame(self.root, bg="gray")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        grid_frame = tk.Frame(center_frame, bg="black")
        grid_frame.pack(pady=30)
        
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

        right_frame = tk.Frame(self.root, width=280, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(right_frame, text="Log", font=("Arial", 16, "bold"), fg="blue").pack(pady=5)
        self.log_text = tk.Text(right_frame, width=35, state=tk.DISABLED, font=("Consolas", 9))
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
        """Value function cho Hill Climbing: Giá trị = - Số rác (Càng ít rác càng tốt)"""
        return -self.count_dirt(state)

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
        
        # Mapping các thuật toán
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
        else: goal_node = None

        if goal_node:
            self.path = []
            curr = goal_node
            while curr:
                self.path.append(curr)
                curr = curr.parent
            self.path.reverse()
            
            moves = [n.move for n in self.path if n.move is not None]
            
            # Kiểm tra xem có bị kẹt ở Local Maxima (dành cho Hill Climbing)
            if not self.is_goal(goal_node.state):
                self.set_console(f"Kẹt ở cực đại cục bộ! Đường đi: {' -> '.join(moves)}", error=True)
            else:
                self.set_console(f"Đường đi: {' -> '.join(moves)}" if moves else "Đã ở trạng thái đích!")
                
            self.current_step = 0
            self.update_grid_ui(self.path[0].state)
        else:
            self.set_console("Không tìm thấy đường đi!", error=True)

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

    # ================== CÁC THUẬT TOÁN MỚI ==================
    
    # 1. IDA* (Iterative Deepening A*)
    def ida_star(self, start_node):
        start_node.h = self.count_dirt(start_node.state)
        start_node.f = start_node.cost + start_node.h
        limit = start_node.f
        
        while True:
            self.log(f"\n--- Bắt đầu vòng lặp với Limit = {limit} ---")
            path = [start_node]
            temp = self.ida_search(path, 0, limit)
            if temp == "FOUND":
                return path[-1]
            if temp == float('inf'):
                return None
            limit = temp

    def ida_search(self, path, g, limit):
        node = path[-1]
        f = g + self.count_dirt(node.state)
        
        self.log(f"Xét Node (g={g}, h={f-g}, f={f})")
        if f > limit:
            return f
        if self.is_goal(node.state):
            return "FOUND"
            
        min_limit = float('inf')
        for child in self.get_successors(node):
            if child not in path: # Chống lặp đơn giản
                path.append(child)
                temp = self.ida_search(path, g + 1, limit)
                if temp == "FOUND":
                    return "FOUND"
                if temp < min_limit:
                    min_limit = temp
                path.pop()
        return min_limit

    # 2. Simple Hill Climbing
    def simple_hill_climbing(self, start_node):
        current = start_node
        while True:
            self.log(f"Current State (Value={self.get_value(current.state)})")
            if self.is_goal(current.state): return current
            
            found_better = False
            for child in self.get_successors(current):
                # TÌM THẤY LÂN CẬN ĐẦU TIÊN TỐT HƠN THÌ CHỌN LUÔN
                if self.get_value(child.state) > self.get_value(current.state):
                    current = child
                    found_better = True
                    self.log(f"  -> Chọn Next_State: {child.move} (Value={self.get_value(child.state)})")
                    break 
            
            if not found_better:
                self.log("  -> Bị kẹt ở cực đại cục bộ (Local Maxima)")
                return current

    # 3. Steepest Ascent Hill Climbing
    def steepest_ascent_hill_climbing(self, start_node):
        current = start_node
        while True:
            self.log(f"Current State (Value={self.get_value(current.state)})")
            if self.is_goal(current.state): return current
            
            neighbors = self.get_successors(current)
            if not neighbors: return current
            
            # CHỌN LÂN CẬN TỐT NHẤT TRONG TẤT CẢ LÂN CẬN
            best_neighbor = max(neighbors, key=lambda n: self.get_value(n.state))
            
            if self.get_value(best_neighbor.state) > self.get_value(current.state):
                current = best_neighbor
                self.log(f"  -> Chọn Best_Neighbor: {current.move} (Value={self.get_value(current.state)})")
            else:
                self.log("  -> Bị kẹt ở cực đại cục bộ (Local Maxima)")
                return current

    # 4. Stochastic Hill Climbing
    def stochastic_hill_climbing(self, start_node):
        current = start_node
        while True:
            self.log(f"Current State (Value={self.get_value(current.state)})")
            if self.is_goal(current.state): return current
            
            neighbors = self.get_successors(current)
            
            # LỌC RA TẬP CÁC LÂN CẬN TỐT HƠN
            better_neighbors = [n for n in neighbors if self.get_value(n.state) > self.get_value(current.state)]
            
            if not better_neighbors: # TẬP BETTER RỖNG
                self.log("  -> Bị kẹt ở cực đại cục bộ (Local Maxima)")
                return current
            
            # CHỌN NGẪU NHIÊN 1 TRẠNG THÁI TỪ TẬP BETTER
            current = random.choice(better_neighbors)
            self.log(f"  -> Chọn ngẫu nhiên Next_State: {current.move} (Value={self.get_value(current.state)})")

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumAIApp(root)
    root.mainloop()