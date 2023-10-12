import tkinter as tk
import random
import math

class WheelOfFortune:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Spinner")
        self.root.geometry("600x650")
        self.root.configure(bg="lightblue")

        self.choices = []
        self.is_spinning = False

        self.canvas = tk.Canvas(
            self.root, 
            width=500, 
            height=500, 
            bg="white")
        self.canvas.grid(
            row=0, 
            column=0, 
            columnspan=3, 
            padx=10, 
            pady=20)

        self.input_entry = tk.Entry(
            self.root, 
            width=30, 
            font=("Helvetica", 14))
        self.input_entry.grid(
            row=1, 
            column=0, 
            columnspan=2, 
            padx=10, 
            pady=(0, 10))

        self.add_button = tk.Button(
            self.root, 
            text="Add Choice", 
            command=self.add_choice, 
            bg="green", 
            fg="white",
            font=("Helvetica", 14))
        self.add_button.grid(
            row=1,
            column=2, 
            padx=10, 
            pady=(0, 10))

        self.clear_button = tk.Button(
            self.root, 
            text="Clear Choices", 
            command=self.clear_choices, 
            bg="red", 
            fg="white",
            font=("Helvetica", 14))
        self.clear_button.grid(
            row=2, 
            column=0, 
            padx=10, 
            pady=(0, 10))

        self.spin_button = tk.Button(
            self.root, 
            text="Spin", 
            command=self.spin, 
            bg="blue", 
            fg="white",
            font=("Helvetica", 14))
        self.spin_button.grid(
            row=2, 
            column=1, 
            columnspan=2, 
            padx=10, 
            pady=(0, 10))

        self.arrow = None
        self.create_wheel()

    def create_wheel(self):
        self.canvas.delete("wheel")
        if not self.choices:
            return

        radius = 200
        cx, cy = 250, 250

        if len(self.choices) == 1:
            # Draw circle
            self.canvas.create_oval(
                50, 
                50, 
                450, 
                450, 
                outline="black", 
                width=2, 
                tags="wheel", 
                fill="#FF5733")
            text_x = cx
            text_y = cy
            choice = self.choices[0]
            self.canvas.create_text(
                cx, cy, 
                text=choice, 
                font=("Helvetica", 20, "bold"), 
                tags="wheel")
        else:
            num_choices = len(self.choices)
            angle_increment = 360 / num_choices

            colors = ["#FF5733", "#33FF57", 
                      "#5733FF", "#FF33B8", 
                      "#33B8FF", "#B8FF33"]
            arc_tags = []

            for i, choice in enumerate(self.choices):
                start_angle = i * angle_increment
                end_angle = start_angle + angle_increment
                start_angle_rad = math.radians(
                    start_angle)
                end_angle_rad = math.radians(
                    end_angle)
                x1 = cx + radius * math.cos(
                    start_angle_rad)
                y1 = cy + radius * math.sin(
                    start_angle_rad)
                x2 = cx + radius * math.cos(
                    end_angle_rad)
                y2 = cy + radius * math.sin(
                    end_angle_rad)
                color = colors[i % len(colors)]

                # Draw wheel segments and store tags
                arc_tag = "arc_{}".format(i)
                arc_tags.append(arc_tag)
                self.canvas.create_arc(
                    50, 50, 450, 450, 
                    start=start_angle,
                    extent=angle_increment, 
                    outline="black", 
                    width=2,
                    tags=("wheel", arc_tag), 
                    fill=color)

            for i, choice in enumerate(self.choices):
                # Draw text on top of arc segments
                mid_angle_rad = math.radians(
                    i * angle_increment + angle_increment / 2)
                text_x = cx + radius * 0.7 * math.cos(
                    mid_angle_rad)
                text_y = cy + radius * 0.7 * math.sin(
                    mid_angle_rad)

                self.canvas.create_text(
                    text_x, 
                    text_y, 
                    text=choice, 
                    font=("Helvetica", 12, "bold"), 
                    tags=("wheel", "text"))

            # Allow spinning when only one choice
            if len(self.choices) == 1:
                self.spin_button.config(state=tk.NORMAL)

    def add_choice(self):
        choice = self.input_entry.get()
        if choice:
            self.choices.append(choice)
            self.input_entry.delete(0, tk.END)
            self.create_wheel()

    def clear_choices(self):
        self.choices = []
        self.canvas.delete("wheel")
        self.canvas.delete("arrow")

    def spin(self):
        if not self.is_spinning and self.choices:
            self.is_spinning = True
            self.spin_button.config(state=tk.DISABLED)
            self.spin_arrow()

    def spin_arrow(self):
        if self.arrow:
            self.canvas.delete(self.arrow)
        
        if len(self.choices) == 1:
            winner_angle = 0
        else:
            winner_angle = random.uniform(360, 1080)
        
        self.rotate_arrow(0, winner_angle, 5)

    def rotate_arrow(
            self, current_angle, target_angle, step):
        if current_angle < target_angle:
            self.canvas.delete("arrow")
            self.arrow = self.draw_arrow(current_angle)
            current_angle += step
            self.root.after(
                10, 
                self.rotate_arrow, 
                current_angle, 
                target_angle, 
                step)
        else:
            self.is_spinning = False
            self.spin_button.config(state=tk.NORMAL)

    def draw_arrow(self, angle):
        cx, cy = 250, 250
        arrow_length = 100
        radians = math.radians(angle)
        x1 = cx + arrow_length * math.cos(radians)
        y1 = cy + arrow_length * math.sin(radians)
        return self.canvas.create_line(
            cx, cy, x1, y1, 
            fill="black", 
            width=12, 
            arrow=tk.LAST, 
            tags="arrow")

if __name__ == "__main__":
    root = tk.Tk()
    app = WheelOfFortune(root)
    root.mainloop()
