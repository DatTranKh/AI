import tkinter as tk
from tkinter import messagebox
import copy
from collections import deque

class Node:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

class VacuumAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacuum Cleaner AI System")
        self.root.geometry("800x500")

        self.algo_choice = tk.StringVar(value="BFS_1")
        self.grid_state = [[' ' for _ in range(3)] for _ in range(3)]
        self.path = []
        self.current_step = -1

        self.setup_ui()

    def setup_ui(self):
        left_frame = tk.Frame(self.root, width=150, bg="lightgray", relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left_frame, text="Algo", font=("Arial", 16, "bold"), bg="lightgray").pack(pady=10)
        
        algos = [("BFS Cách 1", "BFS_1"), ("BFS Cách 2", "BFS_2"), 
                 ("DFS Cách 1", "DFS_1"), ("DFS Cách 2", "DFS_2")]
        for text, val in algos:
            tk.Radiobutton(left_frame, text=text, variable=self.algo_choice, value=val, 
                           bg="lightgray", font=("Arial", 10), indicatoron=0, 
                           width=12, height=2, selectcolor="lightblue").pack(pady=5, padx=10)

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

        right_frame = tk.Frame(self.root, width=250, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(right_frame, text="Log", font=("Arial", 16, "bold"), fg="blue").pack(pady=5)
        self.log_text = tk.Text(right_frame, width=30, state=tk.DISABLED, font=("Consolas", 9))
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
            if 'X' in row:
                return False
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
        
        if algo == "BFS_1":
            goal_node = self.bfs_cach_1(start_node)
        elif algo == "BFS_2":
            goal_node = self.bfs_cach_2(start_node)
        elif algo == "DFS_1":
            goal_node = self.dfs_cach_1(start_node)
        else:
            goal_node = self.dfs_cach_2(start_node)

        if goal_node:
            self.path = []
            curr = goal_node
            while curr:
                self.path.append(curr)
                curr = curr.parent
            self.path.reverse()
            
            moves = [n.move for n in self.path if n.move is not None]
            self.set_console(f"Đường đi: {' -> '.join(moves)}" if moves else "Đã ở trạng thái đích!")
            self.current_step = 0
            self.update_grid_ui(self.path[0].state)
        else:
            self.set_console("Không tìm thấy đường đi!", error=True)

    def bfs_cach_1(self, start_node):
        frontier = deque([start_node])
        reached = {start_node}

        while frontier:
            node = frontier.popleft()
            self.log(f"Xét Node (Cost: {node.cost}): {node.move if node.move else 'Start'}")
            
            if self.is_goal(node.state):
                return node
                
            for child in self.get_successors(node):
                if child not in reached:
                    reached.add(child)
                    frontier.append(child)
                    self.log(f"  Thêm vào Frontier: {child.move}")
        return None

    def bfs_cach_2(self, start_node):
        if self.is_goal(start_node.state): return start_node
        
        frontier = deque([start_node])
        reached = {start_node}

        while frontier:
            node = frontier.popleft()
            self.log(f"Xét Node (Cost: {node.cost}): {node.move if node.move else 'Start'}")
            
            for child in self.get_successors(node):
                if child not in reached:
                    if self.is_goal(child.state):
                        self.log(f"  Tìm thấy GOAL: {child.move}")
                        return child
                    reached.add(child)
                    frontier.append(child)
                    self.log(f"  Thêm vào Frontier: {child.move}")
        return None

    def dfs_cach_1(self, start_node):
        frontier = [start_node]
        reached = {start_node}

        while frontier:
            node = frontier.pop()
            self.log(f"Xét Node (Cost: {node.cost}): {node.move if node.move else 'Start'}")
            
            if self.is_goal(node.state):
                return node
                
            for child in self.get_successors(node):
                if child not in reached:
                    reached.add(child)
                    frontier.append(child)
                    self.log(f"  Thêm vào Frontier: {child.move}")
        return None

    def dfs_cach_2(self, start_node):
        if self.is_goal(start_node.state): return start_node
        
        frontier = [start_node]
        reached = {start_node}

        while frontier:
            node = frontier.pop()
            self.log(f"Xét Node (Cost: {node.cost}): {node.move if node.move else 'Start'}")
            
            for child in self.get_successors(node):
                if child not in reached:
                    if self.is_goal(child.state):
                        self.log(f"  Tìm thấy GOAL: {child.move}")
                        return child
                    reached.add(child)
                    frontier.append(child)
                    self.log(f"  Thêm vào Frontier: {child.move}")
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumAIApp(root)
    root.mainloop()