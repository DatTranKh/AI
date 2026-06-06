import random
import copy

class Node:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost # cost ở đây lưu số ô sai vị trí (misplaced tiles)

def get_0_pos(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def calculate_cost(state, goal_state):
    """Hàm tính số ô sai vị trí (không tính ô trống số 0)"""
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                misplaced_tiles += 1
    return misplaced_tiles

def generate_random_start_states(goal_state, num_states=3, steps=20):
    """
    Sinh tập các trạng thái Start ngẫu nhiên (BS) bằng cách trượt ngẫu nhiên từ GOAL
    để đảm bảo tất cả các trạng thái sinh ra đều giải được.
    """
    bs_states = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while len(bs_states) < num_states:
        current_state = copy.deepcopy(goal_state)
        # Thực hiện xáo trộn ngẫu nhiên `steps` lần
        for _ in range(steps):
            r, c = get_0_pos(current_state)
            dr, dc = random.choice(moves)
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                current_state[r][c], current_state[nr][nc] = current_state[nr][nc], current_state[r][c]
        
        if current_state not in bs_states and current_state != goal_state:
            bs_states.append(current_state)
            
    return bs_states

def get_best_child(current_node, goal_state, reached):
    """
    Sinh các trạng thái con và trả về Node con có cost nhỏ nhất 
    (Greedy) mà chưa từng được duyệt qua (để tránh lặp cấu hình).
    """
    r, c = get_0_pos(current_node.state)
    moves = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
    
    best_child = None
    min_cost = float('inf')
    
    for move_name, (dr, dc) in moves.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [row[:] for row in current_node.state]
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            
            # Kiểm tra tránh lặp trạng thái để không bị vòng lặp vô hạn
            state_tuple = tuple(tuple(row) for row in new_state)
            if state_tuple not in reached:
                cost = calculate_cost(new_state, goal_state)
                # Chọn con tốt nhất theo chiến lược greddy sinh con
                if cost < min_cost:
                    min_cost = cost
                    best_child = Node(state=new_state, parent=current_node, move=move_name, cost=cost)
                    
    return best_child

def print_path(goal_node):
    """Hàm in ra chuỗi các bước di chuyển từ gốc đến đích"""
    path = []
    temp = goal_node
    while temp.move is not None:
        path.append(temp.move)
        temp = temp.parent
    return path[::-1]

def solve_multi_greedy(num_start_states=3):
    GOAL = [[8, 7, 6], 
            [1, 0, 5], 
            [2, 3, 4]]
    
    # 1. Sinh ngẫu nhiên tập các trạng thái ban đầu BS
    random_starts = generate_random_start_states(GOAL, num_states=num_start_states)
    
    # Tập BS hiện tại sẽ lưu trữ các Node đang được xét xét của mỗi nhánh
    BS = []
    print("--- CÁC TRẠNG THÁI START NGẪU NHIÊN ĐƯỢC SINH RA (BS) ---")
    for idx, state in enumerate(random_starts):
        print(f"Nhánh {idx}: {state}")
        cost = calculate_cost(state, GOAL)
        BS.append(Node(state=state, cost=cost))
    print("-" * 60)

    # Tập reached dùng để lưu các trạng thái đã đi qua của từng nhánh, tránh lặp vô hạn
    # Key: chỉ số nhánh, Value: set các trạng thái (dạng tuple)
    reached_by_branch = {i: {tuple(tuple(row) for row in BS[i].state)} for i in range(num_start_states)}
    
    loop_count = 0
    # Vòng lặp chạy cho đến khi tất cả các phần tử trong BS đều đạt GOAL
    while not all(node.state == GOAL for node in BS):
        loop_count += 1
        
        # Tìm node có min cost trong số các node *chưa đạt GOAL* của tập BS
        min_cost = float('inf')
        selected_branch_idx = -1
        
        for i, node in enumerate(BS):
            if node.state != GOAL: # Nếu trạng thái == GOAL thì bỏ qua không xét nữa
                if node.cost < min_cost:
                    min_cost = node.cost
                    selected_branch_idx = i
                    
        if selected_branch_idx == -1:
            # Trường hợp tất cả các nhánh bị kẹt không sinh được con mới hợp lệ
            print("Toàn bộ các nhánh đã rơi vào trạng thái kẹt hoặc không tìm được đường đi tiếp!")
            break

        current_node = BS[selected_branch_idx]
        
        # 2. Sinh con theo thuật toán sinh con greedy (lấy đứa con tốt nhất)
        best_child = get_best_child(current_node, GOAL, reached_by_branch[selected_branch_idx])
        
        if best_child is not None:
            # Thêm vào tập cấu hình đã đi qua của nhánh này
            state_tuple = tuple(tuple(row) for row in best_child.state)
            reached_by_branch[selected_branch_idx].add(state_tuple)
            
            # Cập nhật lại trạng thái đang xét của nhánh này trong tập BS thành trạng thái con tương ứng
            BS[selected_branch_idx] = best_child
            print(f"Bước {loop_count}: Chọn Nhánh {selected_branch_idx} (cost hiện tại={current_node.cost}) -> Đi tiếp bước '{best_child.move}' (cost mới={best_child.cost})")
            
            # Kiểm tra nếu sau bước đi này nhánh này đạt GOAL luôn
            if best_child.state == GOAL:
                print(f"==> NHÁNH {selected_branch_idx} ĐÃ ĐẠT GOAL! Các bước: {print_path(best_child)}")
        else:
            # Nếu nhánh tốt nhất hiện tại bị cụt đường (không có con nào mới), gán cost cao để giải thuật chọn nhánh khác
            print(f"Bước {loop_count}: Nhánh {selected_branch_idx} bị kẹt đường cụt. Chuyển hướng lựa chọn.")
            BS[selected_branch_idx].cost = float('inf')

    print("\n" + "="*20 + " KẾT QUẢ CUỐI CÙNG " + "="*20)
    for i, node in enumerate(BS):
        if node.state == GOAL:
            print(f"Nhánh {i}: Hoàn thành thành công! Đường đi: {print_path(node)}")
        else:
            print(f"Nhánh {i}: Không tìm thấy đường đi (Bị kẹt).")

# Chạy thử chương trình với 3 trạng thái xuất phát ngẫu nhiên
if __name__ == "__main__":
    solve_multi_greedy(num_start_states=3)