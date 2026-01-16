import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

DATA_FILE = "time_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": [], "sessions": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
           
    

class Timer:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")

        #Load data
        self.data = load_data()

        # Initialize timer
        self.seconds = 0 
        self.timer_running = False
        self.start_time = None

        #Task entry
        tk.Label(root, text="Task:").pack(anchor="w", padx=10, pady=(10,0))
        self.task_entry = tk.Entry(root, width=30)
        self.task_entry.pack(padx=10, pady=5)

        #Listbox of saved task
        tk.Label(root, text="Saved Tasks:").pack(anchor="w", padx=10)
        self.task_listbox = tk.Listbox(root, height=5)
        self.task_listbox.pack(fill="x", padx=10)
        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)

        self.refresh_task_list()

        #Label for timer
        self.timer_label = tk.Label(root, text="00:00:00", font=("Helvetica", 36))
        self.timer_label.pack(pady=20)

        #Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.update_timer()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.data["tasks"]:
            self.task_listbox.insert(tk.END, task)

    def on_task_select(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            task_name = self.task_listbox.get(selection[0])
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task_name)


    def start_timer(self):
        if self.timer_running:
           return
        
        task_name = self.task_entry.get().strip()
        if not task_name:
            messagebox.showwarning("No task", "Please enter a task first.")
            return
        
        #Add task to list if new
        if task_name not in self.data["tasks"]:
            self.data["tasks"].append(task_name)
            save_data(self.data)
            self.refresh_task_list()

        self.timer_running = True
        self.start_time = datetime.now()
        self.update_timer()


    def stop_timer(self):
        if not self.timer_running:
            return
        
        self.timer_running = False
        end_time = datetime.now()

        #Save session
        task_name = self.task_entry.get().strip()
        session = {
            "task": task_name,
            "start": self.start_time.isoformat(),
            "end": end_time.isoformat(),
            "duration_seconds": self.seconds
        }
        self.data["sessions"].append(session)
        save_data(self.data)

        #Reset timer
        self.seconds = 0
        self.timer_label.config(text="00:00:00")
        self.start_time = None


    def update_timer(self):
        if self.timer_running:
            self.seconds += 1
            minutes = self.seconds // 60
            seconds = self.seconds % 60
            hours = self.seconds // 3600
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.timer_label.config(text=time_str)
            self.root.after(1000, self.update_timer) #Update every 1 second

if __name__ == "__main__":
    root = tk.Tk()
    app = Timer(root)
    root.mainloop()