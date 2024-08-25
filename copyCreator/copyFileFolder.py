import shutil
import os
import tkinter as tk
from tkinter import filedialog
import threading
from datetime import datetime
from PIL import Image, ImageTk

# Global variable to handle the copy process
stop_copy = False
stop_event = threading.Event()

def copy_file_or_folder(source, destination):
    global stop_copy
    try:
        if stop_copy:
            print("Copy operation stopped")
            return
        if os.path.isfile(source):
            print(f"Copying file {source} to {destination}")
            shutil.copy(source, destination)
            print("File copy successful.")
        elif os.path.isdir(source):
            destination_dir = os.path.join(destination, os.path.basename(source))
            if os.path.exists(destination_dir):
                shutil.rmtree(destination_dir)
            shutil.copytree(source, destination_dir)
            print("Directory copy successful.")
        else:
            print(f"Source {source} does not exist or is not accessible.")
        update_last_copy_time()
    except Exception as e:
        print(f"Error during copy operation: {e}")

def update_last_copy_time():
    now = datetime.now()
    last_copy_time = now.strftime("%Y-%m-%d %H:%M:%S")
    last_copy_label.config(text=f"Last Copy: {last_copy_time}")
    print(f"Last Copy Time: {last_copy_time}")

# Allow selection of either a file or a directory
def select_source():
    source = filedialog.askopenfilename() or filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source)

def select_destination():
    destination = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination)

def manual_copy():
    global stop_copy
    stop_copy = False
    source = source_entry.get()
    destination = destination_entry.get()
    if source and destination:
        copy_file_or_folder(source, destination)
    else:
        print("Please select both source and destination.")

def auto_copy(interval):
    if stop_event.is_set():
        print("Auto copy operation stopped.")
        return
    source = source_entry.get()
    destination = destination_entry.get()
    if source and destination:
        threading.Thread(target=copy_file_or_folder, args=(source, destination)).start()
        threading.Timer(interval, auto_copy, [interval]).start()
    else:
        print("Please select both source and destination.")

def start_auto_copy():
    try:
        interval = float(time_entry.get())
        unit = time_unit_var.get()
        if unit == "minutes":
            interval *= 60
        global stop_copy
        stop_copy = False
        stop_event.clear()   
        auto_copy(interval)
    except ValueError:
        print("Please enter a valid number for the time interval.")

def stop_copy_process():
    global stop_copy
    stop_copy = True
    stop_event.set()

def resize_background(event):
    # Get the current size of the window
    new_width = event.width
    new_height = event.height
    
    # Resize the image to fit the window size
    resized_image = background_image.resize((new_width, new_height), Image.ANTIALIAS)
    background_photo_resized = ImageTk.PhotoImage(resized_image)
    
    # Update the canvas image
    canvas.itemconfig(background_image_on_canvas, image=background_photo_resized)
    canvas.background_photo_resized = background_photo_resized  # Keep a reference to avoid garbage collection

# Setting up the GUI
root = tk.Tk()
root.title("File/Folder Copier")
root.geometry("800x400")

# Load the background image
background_image = Image.open("sim.jpg")

# Create a canvas to hold the background image
canvas = tk.Canvas(root, width=800, height=400)
canvas.pack(fill="both", expand=True)

# Display the image on the canvas and keep a reference to the image object
background_photo = ImageTk.PhotoImage(background_image)
background_image_on_canvas = canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Bind the resize event to the function
root.bind("<Configure>", resize_background)

# Add widgets on top of the background
canvas.create_text(400, 50, text="File/Folder Copier", font=("Helvetica", 20), fill="white")

source_label = tk.Label(root, text="Source:", bg='#f0f0f0')
source_entry = tk.Entry(root, width=50)
source_button = tk.Button(root, text="Browse...", command=select_source, bg='#0078D7', fg='white')

canvas.create_window(150, 100, window=source_label)
canvas.create_window(400, 100, window=source_entry)
canvas.create_window(650, 100, window=source_button)

destination_label = tk.Label(root, text="Destination:", bg='#f0f0f0')
destination_entry = tk.Entry(root, width=50)
destination_button = tk.Button(root, text="Browse...", command=select_destination, bg='#0078D7', fg='white')

canvas.create_window(150, 150, window=destination_label)
canvas.create_window(400, 150, window=destination_entry)
canvas.create_window(650, 150, window=destination_button)

manual_copy_button = tk.Button(root, text="Manual Copy", command=manual_copy, bg='#28A745', fg='white')
canvas.create_window(400, 200, window=manual_copy_button)

# Auto copy interval setup
auto_copy_frame = tk.Frame(root, bg='#f0f0f0')
canvas.create_window(400, 250, window=auto_copy_frame)

tk.Label(auto_copy_frame, text="Auto Copy Interval:", bg='#f0f0f0').pack(side='left')
time_entry = tk.Entry(auto_copy_frame, width=10)
time_entry.pack(side='left', padx=5)
time_entry.insert(0, "20")

time_unit_var = tk.StringVar(value="seconds")
time_unit_menu = tk.OptionMenu(auto_copy_frame, time_unit_var, "seconds", "minutes")
time_unit_menu.pack(side='left')

start_auto_copy_button = tk.Button(root, text="Start Auto Copy", command=start_auto_copy, bg='#FFC107', fg='black')
canvas.create_window(400, 300, window=start_auto_copy_button)

# Stop button to stop any ongoing copy process
stop_copy_button = tk.Button(root, text="Stop", command=stop_copy_process, bg='#FF5733', fg='white')
canvas.create_window(400, 375, window=stop_copy_button)

last_copy_label = tk.Label(root, text="Last Copy: N/A", bg='#f0f0f0')
canvas.create_window(400, 350, window=last_copy_label)

root.mainloop()
