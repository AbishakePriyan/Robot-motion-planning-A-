import tkinter as tk

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
        self.robot_icon = None
        self.goal_reached = False  # Flag to check if the goal is reached
        self.draw_grid()
        self.draw_obstacles()
        self.draw_initial_and_goal()
        self.draw_robot()  # Ensure robot is visible initially

        # Bind the W, A, S, D keys to control the robot
        self.master.bind("<w>", self.move_up)
        self.master.bind("<a>", self.move_left)
        self.master.bind("<s>", self.move_down)
        self.master.bind("<d>", self.move_right)

        # Restart Button
        self.restart_button = tk.Button(master, text="Restart", command=self.restart, state=tk.DISABLED)
        self.restart_button.pack(pady=10)

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

    def display_message(self, message):
        """Display the message in the Tkinter text box and auto-scroll to the bottom."""
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.config(state=tk.DISABLED)
        self.text_box.yview(tk.END)  # Auto-scroll to the bottom

    def move_up(self, event=None):
        """Move the robot up (decrease row)."""
        if not self.goal_reached:
            self.move_robot(0, -1)

    def move_left(self, event=None):
        """Move the robot left (decrease column)."""
        if not self.goal_reached:
            self.move_robot(-1, 0)

    def move_down(self, event=None):
        """Move the robot down (increase row)."""
        if not self.goal_reached:
            self.move_robot(0, 1)

    def move_right(self, event=None):
        """Move the robot right (increase column)."""
        if not self.goal_reached:
            self.move_robot(1, 0)

    def move_robot(self, dx, dy):
        """Move the robot and handle obstacle detection."""
        new_position = (self.robot[0] + dx, self.robot[1] + dy)

        # Check if the new position is within the grid boundaries
        if 0 <= new_position[0] < GRID_SIZE and 0 <= new_position[1] < GRID_SIZE:
            # Check if there is an obstacle in the new position
            if new_position in OBSTACLES:
                self.display_message(f"Obstacle detected at {new_position}!")
            else:
                # Move robot to the new position
                self.robot = new_position
                self.canvas.coords(
                    self.robot_icon,
                    self.robot[0] * CELL_SIZE + 25, self.robot[1] * CELL_SIZE + 25,
                    self.robot[0] * CELL_SIZE + 75, self.robot[1] * CELL_SIZE + 75
                )
                self.display_message(f"Moved to {self.robot}")

                # Check if the robot has reached the goal
                if self.robot == GOAL:
                    self.display_message("Goal State Reached!")
                    self.goal_reached = True
                    self.restart_button.config(state=tk.NORMAL)  # Enable restart button
        else:
            self.display_message("Out of bounds!")

    def restart(self):
        """Reset the robot to the initial state."""
        self.robot = START
        self.goal_reached = False
        self.canvas.coords(
            self.robot_icon,
            self.robot[0] * CELL_SIZE + 25, self.robot[1] * CELL_SIZE + 25,
            self.robot[0] * CELL_SIZE + 75, self.robot[1] * CELL_SIZE + 75
        )
        self.display_message("Step 1: Initial state")
        self.restart_button.config(state=tk.DISABLED)  # Disable restart button

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Robot Motion Control - 5x5 Grid with Obstacles")
    app = GridWorld(root)
    root.mainloop()
