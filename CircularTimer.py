import tkinter as tk
import math

class CircularTimerApp:
    def __init__(self, root):
        # Initialize main window with title, size, and background color
        self.root = root
        self.root.title("Simple Circular Timer")
        self.root.geometry("400x500")
        self.root.configure(bg="#367860")
        
        # Timer variables
        self.time_left = 7200  # Total time in seconds (120 minutes)
        self.is_running = False  # Timer status
        self.interval = None  # Placeholder for timer event
        self.is_dragging = False  # Track dragging state for timer adjustments
        
        # Setup the main canvas for drawing
        self.canvas = tk.Canvas(root, width=300, height=300, bg="#367860", highlightthickness=0)
        self.canvas.pack(pady=20)  # Add padding to center the canvas vertically
        
        # Coordinates for the center and radius of the circle
        self.center_x = 150
        self.center_y = 150
        self.circle_radius = 100
        self.dot_radius = 15  # Radius of the dot indicator
        
        # Timer display (positioned in the middle of the circle)
        self.timer_display = tk.Label(self.canvas, text="120:00", font=("Helvetica", 28), fg="white", bg="#367860")
        self.timer_display.place(x=self.center_x, y=self.center_y, anchor="center")  # Centered inside the circle
        
        # Buttons setup (Start, Stop, Reset)
        button_frame = tk.Frame(root, bg="#367860")  # Container for the buttons
        button_frame.pack(pady=10)  # Add padding below the canvas
        
        # Start button
        self.start_button = tk.Button(button_frame, text="Start", font=("Helvetica", 18), command=self.start_timer, bg="#76D7C4", fg="white")
        self.start_button.grid(row=0, column=0, padx=10)
        
        # Stop button
        self.stop_button = tk.Button(button_frame, text="Stop", font=("Helvetica", 18), command=self.stop_timer, bg="#ff5c5c", fg="white")
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # Reset button
        self.reset_button = tk.Button(button_frame, text="Reset", font=("Helvetica", 18), command=self.reset_timer, bg="#f39c12", fg="white")
        self.reset_button.grid(row=0, column=2, padx=10)
        
        # Label to display "Congratulations!" message (hidden initially)
        self.congrats_label = tk.Label(root, text="Congratulations!", font=("Helvetica", 18), fg="white", bg="#367860")
        self.congrats_label.pack(pady=20)
        self.congrats_label.pack_forget()  # Hide the label initially
        
        # Event bindings for dragging functionality
        self.canvas.bind("<Button-1>", self.start_drag)  # Start drag
        self.canvas.bind("<B1-Motion>", self.drag_dot)  # Drag motion
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)  # Stop drag
        
        # Initial display of timer and drawing elements
        self.update_timer_display()
        self.draw_circle()
        self.draw_dot()
        
    # Starts the timer countdown
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.interval = self.root.after(1000, self.countdown)
    
    # Stops the timer countdown
    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            if self.interval:
                self.root.after_cancel(self.interval)
    
    # Resets the timer back to initial settings
    def reset_timer(self):
        self.stop_timer()  # Stop any ongoing timer
        self.time_left = 7200  # Reset time to 120 minutes
        self.update_timer_display()  # Update the displayed time
        self.draw_circle()  # Redraw the circle
        self.draw_dot()  # Reset the dot position
        self.congrats_label.pack_forget()  # Hide "Congratulations!" message if visible
    
    # Main countdown function, updates every second
    def countdown(self):
        if self.time_left > 0 and self.is_running:
            self.time_left -= 1  # Decrease time
            self.update_timer_display()  # Update display
            self.draw_circle()  # Redraw circle with new position
            self.draw_dot()  # Update dot position
            self.interval = self.root.after(1000, self.countdown)  # Repeat countdown
        else:
            self.is_running = False  # Stop when countdown ends
            self.congrats_label.pack()  # Show "Congratulations!" message when time is up
    
    # Updates the timer display with current time left
    def update_timer_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_display.config(text=f"{minutes}:{seconds:02}")  # Format time as mm:ss
    
    # Draws the main circle on the canvas
    def draw_circle(self):
        self.canvas.delete("circle")  # Remove previous circle
        self.canvas.create_oval(self.center_x - self.circle_radius, self.center_y - self.circle_radius,
                                self.center_x + self.circle_radius, self.center_y + self.circle_radius,
                                outline="white", width=4, tags="circle")  # Draw new circle
    
    # Draws the dot indicator along the circle to show progress
    def draw_dot(self):
        angle = (self.time_left / 7200) * 2 * math.pi  # Calculate angle based on remaining time
        # Position the dot using trigonometric functions
        x = self.center_x + self.circle_radius * math.cos(math.pi / 2 - angle)
        y = self.center_y - self.circle_radius * math.sin(math.pi / 2 - angle)
        
        self.canvas.delete("dot")  # Remove previous dot
        self.canvas.create_oval(x - self.dot_radius, y - self.dot_radius,
                                x + self.dot_radius, y + self.dot_radius,
                                fill="#76D7C4", tags="dot")  # Draw new dot
    
    # Start dragging event to update timer based on dot position
    def start_drag(self, event):
        self.is_dragging = True
        angle = self.get_mouse_angle(event)
        self.set_time_from_angle(angle)
    
    # Dragging the dot around the circle
    def drag_dot(self, event):
        if self.is_dragging:
            angle = self.get_mouse_angle(event)
            self.set_time_from_angle(angle)
    
    # Stop dragging event to finalize the timer position
    def stop_drag(self, event):
        self.is_dragging = False
    
    # Calculate the angle of the mouse relative to circle center
    def get_mouse_angle(self, event):
        dx = event.x - self.center_x
        dy = event.y - self.center_y
        angle = math.atan2(dy, dx)  # Get angle in radians
        angle = (angle + math.pi / 2 + 2 * math.pi) % (2 * math.pi)  # Adjust angle to be within circle range
        return angle
    
    # Update the time based on the angle of drag position
    def set_time_from_angle(self, angle):
        self.time_left = max(0, int((angle / (2 * math.pi)) * 7200))  # Set time based on angle
        self.update_timer_display()
        self.draw_circle()
        self.draw_dot()

# Run the application
root = tk.Tk()
app = CircularTimerApp(root)
root.mainloop()

