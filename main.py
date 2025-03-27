# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
import psutil

# Function to update CPU and memory stats
def update_stats():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    cpu_label.config(text=f"CPU: {cpu_usage:.2f}%")
    cpu_bar['value'] = cpu_usage

    memory_label.config(text=f"Memory: {memory_usage:.2f}%")
    memory_bar['value'] = memory_usage

    list_processes()
    root.after(2000, update_stats)  # Update every 2 seconds

# Function to list top processes by CPU usage
def list_processes():
    process_tree.delete(*process_tree.get_children())
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            info = proc.info
            processes.append((info['pid'], info['name'], info['cpu_percent']))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes = sorted(processes, key=lambda x: x[2], reverse=True)[:10]
    for proc in processes:
        process_tree.insert("",
                            "end",
                            values=(proc[0], proc[1], f"{proc[2]:.1f}%"))

# Function to kill a selected process
def kill_process():
    selected_item = process_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a process to kill.")
        return

    try:
        pid = int(process_tree.item(selected_item[0])['values'][0])
        psutil.Process(pid).kill()
        messagebox.showinfo("Success", f"Process {pid} terminated.")
        list_processes()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to kill process: {e}")

# Create main window
root = tk.Tk()
root.title("Real-Time Process Monitoring DashBoard")
root.geometry("500x350")

# CPU and Memory Frame
stats_frame = ttk.LabelFrame(root, text="System Stats", padding=5)
stats_frame.pack(fill="x", padx=5, pady=5)

cpu_label = ttk.Label(stats_frame, text="CPU: 0%")
cpu_label.pack(anchor="w", padx=5, pady=2)
cpu_bar = ttk.Progressbar(stats_frame, mode='determinate')
cpu_bar.pack(fill="x", padx=5, pady=2)

memory_label = ttk.Label(stats_frame, text="Memory: 0%")
memory_label.pack(anchor="w", padx=5, pady=2)
memory_bar = ttk.Progressbar(stats_frame, mode='determinate')
memory_bar.pack(fill="x", padx=5, pady=2)

# Process List Frame
process_frame = ttk.LabelFrame(root, text="Top Processes", padding=5)
process_frame.pack(fill="both", expand=True, padx=5, pady=5)

columns = ("PID", "Name", "CPU %")
process_tree = ttk.Treeview(process_frame,
                            columns=columns,
                            show="headings",
                            height=8)
for col in columns:
    process_tree.heading(col, text=col)
    process_tree.column(col,
                        width=150 if col == "Name" else 70,
                        anchor="center")
process_tree.pack(fill="both", expand=True)

# Kill Button
kill_button = ttk.Button(root, text="Kill Process", command=kill_process)
kill_button.pack(pady=5)

# Start updating stats
update_stats()
root.mainloop()
