import pygame
import random
import numpy as np

# 初始化Pygame
pygame.init()

# 游戏窗口大小
WIDTH, HEIGHT = 600, 450
GRID_SIZE = 20

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, BLUE, YELLOW]  # 四个障碍物的颜色

# 初始化窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-Learning Snake Game")

# 字体初始化
font = pygame.font.SysFont("Arial", 16)

# 蛇和食物的初始位置
snake = [(WIDTH // 2, HEIGHT // 2)]
food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
        random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

# 障碍物生成函数
def generate_obstacles():
    # 将地图划分为四个区域
    regions = [
        (0, WIDTH // 2, 0, HEIGHT // 2),          # 左上
        (WIDTH // 2, WIDTH, 0, HEIGHT // 2),      # 右上
        (0, WIDTH // 2, HEIGHT // 2, HEIGHT),     # 左下
        (WIDTH // 2, WIDTH, HEIGHT // 2, HEIGHT)  # 右下
    ]
    obstacles = []
    for region in regions:
        # 确保障碍物位于区域中心附近
        center_x = (region[0] + region[1]) // 2
        center_y = (region[2] + region[3]) // 2
        x = random.randint(max(region[0], center_x - GRID_SIZE * 2), min(region[1] - GRID_SIZE, center_x + GRID_SIZE * 2))
        y = random.randint(max(region[2], center_y - GRID_SIZE * 2), min(region[3] - GRID_SIZE, center_y + GRID_SIZE * 2))
        obstacles.append((x, y))
    return obstacles

# 初始障碍物
obstacles = generate_obstacles()

# 方向控制
direction = (0, 0)

# Q-learning参数
learning_rate = 0.1
discount_factor = 0.9
epsilon = 1.0  # 初始探索概率较高
epsilon_decay = 0.995  # 每次更新后降低探索概率
min_epsilon = 0.1  # 最小探索概率

# Q-table初始化
q_table = {}

# 奖励和动作记录
current_reward = 0
current_action = "None"

# 记录蛇访问过的区域
visited = set()
visited.add(snake[0])

# 计算距离
def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取当前状态
    state = (snake[0], food, tuple(obstacles))

    # Epsilon-greedy策略
    if random.uniform(0, 1) < epsilon:
        action = random.choice([(0, -GRID_SIZE), (0, GRID_SIZE), (-GRID_SIZE, 0), (GRID_SIZE, 0)])
    else:
        if state in q_table:
            action = max(q_table[state], key=q_table[state].get)
        else:
            action = random.choice([(0, -GRID_SIZE), (0, GRID_SIZE), (-GRID_SIZE, 0), (GRID_SIZE, 0)])

    # 更新蛇的位置
    new_head = (snake[0][0] + action[0], snake[0][1] + action[1])

    # 检查碰撞
    if (new_head in snake or
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in obstacles):
        current_reward = -10
        running = False
    elif new_head == food:
        current_reward = 10
        snake.insert(0, new_head)
        food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
        # 重新生成障碍物
        obstacles = generate_obstacles()
    else:
        # 计算移动后的距离
        old_distance = calculate_distance(snake[0], food)
        new_distance = calculate_distance(new_head, food)
        if new_distance < old_distance:
            current_reward = 1  # 靠近食物
        elif new_distance > old_distance:
            current_reward = -1  # 远离食物
        else:
            current_reward = 0  # 距离不变
        snake.insert(0, new_head)
        snake.pop()

    # 记录访问过的区域
    if new_head not in visited:
        visited.add(new_head)
        current_reward += 0.5  # 探索新区域奖励

    # 记录当前动作
    if action == (0, -GRID_SIZE):
        current_action = "UP"
    elif action == (0, GRID_SIZE):
        current_action = "DOWN"
    elif action == (-GRID_SIZE, 0):
        current_action = "LEFT"
    elif action == (GRID_SIZE, 0):
        current_action = "RIGHT"

    # 更新Q-table
    next_state = (snake[0], food, tuple(obstacles))
    if state not in q_table:
        q_table[state] = {action: 0 for action in [(0, -GRID_SIZE), (0, GRID_SIZE), (-GRID_SIZE, 0), (GRID_SIZE, 0)]}
    if next_state in q_table:
        max_next_q = max(q_table[next_state].values())
    else:
        max_next_q = 0
    q_table[state][action] = (1 - learning_rate) * q_table[state][action] + learning_rate * (current_reward + discount_factor * max_next_q)

    # 降低探索概率
    epsilon = max(epsilon * epsilon_decay, min_epsilon)

    # 渲染游戏
    screen.fill(BLACK)

    # 绘制蛇
    for segment in snake:
        pygame.draw.rect(screen, WHITE, (*segment, GRID_SIZE, GRID_SIZE))

    # 绘制食物
    pygame.draw.rect(screen, RED, (*food, GRID_SIZE, GRID_SIZE))

    # 绘制障碍物
    for i, obstacle in enumerate(obstacles):
        pygame.draw.rect(screen, COLORS[i], (*obstacle, GRID_SIZE, GRID_SIZE))

    # 显示游戏状态
    state_text = font.render(f"State: Snake={snake[0]}, Food={food}, Obstacles={obstacles}", True, WHITE)
    action_text = font.render(f"Action: {current_action}", True, WHITE)
    reward_text = font.render(f"Reward: {current_reward}", True, WHITE)
    epsilon_text = font.render(f"Epsilon: {epsilon:.2f}", True, WHITE)
    screen.blit(state_text, (10, HEIGHT - 120))
    screen.blit(action_text, (10, HEIGHT - 90))
    screen.blit(reward_text, (10, HEIGHT - 60))
    screen.blit(epsilon_text, (10, HEIGHT - 30))

    pygame.display.flip()

    # 控制游戏速度
    pygame.time.wait(100)

pygame.quit()
