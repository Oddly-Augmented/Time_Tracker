import tkinter as tk

class Timer:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")


        # Initialize timer
        self.seconds = 0 
        self.timer_running = False

        #Label for timer
        self.timer_label = tk.Label(root, text="00:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        #Buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.update_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running:
            self.seconds += 1
            minutes = self.seconds // 60
            seconds = self.seconds % 60
            time_str = f"{minutes:02}:{seconds:02}"
            self.timer_label.config(text=time_str)
            self.root.after(1000, self.update_timer) #Update every 1 second

if __name__ == "__main__":
    root = tk.Tk()
    app = Timer(root)
    root.mainloop()