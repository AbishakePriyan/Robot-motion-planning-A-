import tkinter as tk
import heapq

# Grid size
GRID_SIZE = 5
CELL_SIZE = 100
START = (0, 0)
GOAL = (GRID_SIZE - 1, GRID_SIZE - 1)

# Obstacles (more added for complexity)
OBSTACLES = {
    (0, 4),
    (1, 1), (1, 2),
    (2, 3), 
    (3, 0), (3, 1), (3, 3), 
    (4, 0), (4, 1)
}

class GridWorld:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="white")
        self.canvas.pack()

        self.text_box = tk.Text(master, width=50, height=10)
        self.text_box.pack(pady=10)
        self.text_box.insert(tk.END, "Step 1: Initial state\n")
        self.text_box.config(state=tk.DISABLED)

        self.robot = START  # Initial robot position
        self.path = None  # No path initially
        self.robot_icon = None
        self.start_button = tk.Button(master, text="Start", command=self.start)
        self.start_button.pack(pady=10)

        self.draw_grid()
        self.draw_obstacles()
        self.draw_initial_and_goal()
        self.draw_robot()  # Ensure robot is visible initially

    def draw_grid(self):
        """Draw the grid lines."""
        for i in range(GRID_SIZE + 1):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE, fill="gray")
            self.canvas.create_line(0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE, i * CELL_SIZE, fill="gray")

    def draw_obstacles(self):
        """Draw obstacles as rock emojis."""
        for (x, y) in OBSTACLES:
            self.canvas.create_text(
                x * CELL_SIZE + 50, y * CELL_SIZE + 50,
                text="🪨", font=("Helvetica", 40)
            )

    def draw_initial_and_goal(self):
        """Label the initial and goal state."""
        self.canvas.create_text(
            0 * CELL_SIZE + 50, 0 * CELL_SIZE + 50, 
            text="Initial State", font=("Helvetica", 10, "bold"), fill="blue"
        )
        self.canvas.create_text(
            (GRID_SIZE - 1) * CELL_SIZE + 50, (GRID_SIZE - 1) * CELL_SIZE + 50, 
            text="Goal State", font=("Helvetica", 10, "bold"), fill="green"
        )

    def draw_robot(self):
        """Draw the robot as a red circle."""
        x, y = self.robot
        self.robot_icon = self.canvas.create_oval(
            x * CELL_SIZE + 25, y * CELL_SIZE + 25,  # coordinates for the red circle
            x * CELL_SIZE + 75, y * CELL_SIZE + 75,  # size of the circle
            fill="red", outline="red"
        )

    def move_robot(self):
        """Move the robot slowly along the computed path and display step messages."""
        if self.path:
            current = self.robot
            next_step = self.path.pop(0)

            # Update the robot's position
            self.robot = next_step
            self.canvas.coords(
                self.robot_icon,
                self.robot[0] * CELL_SIZE + 25, self.robot[1] * CELL_SIZE + 25,
                self.robot[0] * CELL_SIZE + 75, self.robot[1] * CELL_SIZE + 75
            )

            # Message about the movement
            step_message = f"Moving from {current} to {self.robot}"

            # Check if there is an obstacle
            if self.robot in OBSTACLES:
                step_message += " (Obstacle detected, changing path!)"

            self.display_message(step_message)

            # Wait and continue moving robot in 500 ms
            self.master.after(1500, self.move_robot)
        else:
            self.display_message("Final Step: Goal state reached")

    def display_message(self, message):
        """Display the message in the Tkinter text box."""
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.config(state=tk.DISABLED)
        self.text_box.yview(tk.END)

    def heuristic(self, a, b):
        """Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self, start, goal):
        """A* pathfinding algorithm."""
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {start: None}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # Return the correct path order

            neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
            for dx, dy in neighbors:
                neighbor = (current[0] + dx, current[1] + dy)

                if (0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE
                    and neighbor not in OBSTACLES):
                    
                    temp_g_score = g_score[current] + 1
                    if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))
                        came_from[neighbor] = current

        return None  # No path found

    def start(self):
        """Start or restart the robot motion."""
        # Clear the text box and reset everything
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, "Step 1: Initial state\n")
        self.text_box.config(state=tk.DISABLED)

        # If the robot has already completed the path, reset everything
        if self.robot_icon is not None:
            self.canvas.delete(self.robot_icon)
            self.robot = START  # Reset robot to the start
            self.path = None
            self.draw_robot()  # Redraw robot at the initial position

        # Compute path and move the robot
        self.display_message("Step 2: Finding the shortest path")
        self.path = self.a_star(START, GOAL)  # Compute path
        if self.path:
            self.move_robot()  # Start moving the robot
        else:
            self.display_message("No path found!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Robot Motion Planning (A* Algorithm) - 5x5 Grid")
    app = GridWorld(root)
    root.mainloop()
