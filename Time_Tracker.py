import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from datetime import datetime
import uuid
import os

DATA_FILE = "time_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": [], "sessions": []}
    except json.JSONDecodeError:
        backup_name = f"time_data_corrupt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.rename(DATA_FILE, backup_name)

        messagebox.showwarning(
            "Data error",
            f"time_data.json is corrupted.\n"
            f"It was renamed to {backup_name}.\nStarting with a new file."
        )
        data = {"tasks": [], "sessions": []}
        save_data(data)  # writes a clean time_data.json
        return data
    
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_id():
   return str(uuid.uuid4())
    
class Timer:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")

        # shared data
        self.data = load_data()

        # task selector
        self.task_selector = TaskSelector(root, self.data["tasks"], self.on_tasks_changed)
        self.task_selector.pack(fill="x")

        # timer state
        self.seconds = 0
        self.timer_running = False
        self.start_time = None

        # UI for timer
        self.timer_label = tk.Label(root, text="00:00:00", font=("Helvetica", 36))
        self.timer_label.pack(pady=20)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_button = tk.Button(btn_frame, text="Start", command=self.start_timer)
        self.stop_button = tk.Button(btn_frame, text="Stop", command=self.stop_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.update_timer()

    def on_tasks_changed(self, tasks):
            self.data["tasks"] = tasks
            save_data(self.data)

    def start_timer(self):
        if self.timer_running:
            return

        # validate + add task if new
        if not self.task_selector.add_task_if_new():
            return

        self.timer_running = True
        self.start_time = datetime.now()
        self.update_timer()

    def stop_timer(self):
        if not self.timer_running:
            return

        self.timer_running = False
        end_time = datetime.now()

        task = self.task_selector.get_current_task()
        task_id = task["id"] if task else None
        task_name = task["name"] if task else self.task_selector.get_task_name()

        session = {
            "task_id": task_id,
            "task": task_name,
            "start": self.start_time.isoformat(),
            "end": end_time.isoformat(),
            "duration_seconds": self.seconds,
            "id": get_id(),
        }
        self.data["sessions"].append(session)
        save_data(self.data)

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


class TaskSelector(tk.Frame):
    def __init__(self, parent, tasks, on_change):
        super().__init__(parent)
        self.tasks = tasks
        self.on_change = on_change

        self.data = load_data()

        tk.Label(self, text="Task:").pack(anchor="w", padx=10, pady=(10, 0))
        self.task_entry = tk.Entry(self, width=30)
        self.task_entry.pack(padx=10, pady=5)

        tk.Label(self, text="Saved Tasks:").pack(anchor="w", padx=10)
        self.task_listbox = tk.Listbox(self, height=5)
        self.task_listbox.pack(fill="x", padx=10)
        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)

        self.refresh_task_list()

    def get_task_name(self):
        return self.task_entry.get().strip()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task["name"])

    def on_task_select(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            task = self.tasks[selection[0]]
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task["name"])

    def get_current_task(self):
        name = self.get_task_name()
        for t in self.tasks:
            if t["name"] == name:
                return t
        return None
        

    def add_task_if_new(self):
        task_name = self.get_task_name()
        if not task_name:
            messagebox.showwarning("No task", "Please enter a task first.")
            return False

        if not any(t['name'] == task_name for t in self.tasks):
            new_task = {"id": get_id(), "name": task_name}
            self.tasks.append(new_task)
            self.refresh_task_list()
            self.on_change(self.tasks)


        return True

    def get_all_tasks(self):
        return list(self.tasks)



if __name__ == "__main__":
    root = tk.Tk()
    app = Timer(root)
    root.mainloop()