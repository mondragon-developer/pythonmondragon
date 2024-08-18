import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import threading
import time
import queue
import ctypes
from screeninfo import get_monitors

class LockScreen:
    def __init__(self, image_path=None, message="Say the magic word to lock or unlock", activation_phrase="mondragon"):
        """
        Initialize the LockScreen object.

        :param image_path: Path to the background image file (optional)
        :param message: Message to display on the lock screen
        :param activation_phrase: Phrase to trigger both locking and unlocking
        """
        self.image_path = image_path
        self.message = message
        self.activation_phrase = activation_phrase.lower()
        self.is_locked = True
        self.is_listening = False
        self.running = True
        self.command_queue = queue.Queue()

        # Get information about all connected monitors
        self.monitors = get_monitors()

        # Create a root window and a fullscreen window for each monitor
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.windows = []
        for monitor in self.monitors:
            window = tk.Toplevel(self.root)
            window.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
            self.windows.append(window)

        # Setup the lock screen UI for each monitor
        self.setup_screens()

        # Bind custom key combination for manual unlock to all windows
        self.root.bind('<Control-j>', self.ctrl_j_pressed)
        self.root.bind('<Control-m>', self.ctrl_m_pressed)

        # Start listening for voice commands in a separate thread
        self.listen_thread = threading.Thread(target=self.listen_for_commands)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        # Start processing commands in the main thread
        self.root.after(100, self.process_commands)

    def setup_screens(self):
        """Set up the lock screen user interface on all monitors."""
        for i, window in enumerate(self.windows):
            window.withdraw()  # Hide the window initially
            window.overrideredirect(True)  # Remove window decorations
            window.lift()
            window.attributes('-topmost', True)

            frame = tk.Frame(window, bg="black")
            frame.pack(fill="both", expand=True)

            if self.image_path:
                # Load and display background image if provided
                img = Image.open(self.image_path)
                img = img.resize((self.monitors[i].width, self.monitors[i].height), Image.ANTIALIAS)
                bg_image = ImageTk.PhotoImage(img)
                bg_label = tk.Label(frame, image=bg_image)
                bg_label.image = bg_image  # Keep a reference
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                frame.configure(bg="black")

            label = tk.Label(frame, text=self.message, font=("Helvetica", 32), fg="white", bg="black")
            label.pack(fill="both", expand=True)

            if i == 0:  # Only show status on the primary monitor
                self.status_label = tk.Label(frame, text="Not listening", font=("Helvetica", 16), fg="red", bg="black")
                self.status_label.pack(pady=10)

            window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Handle the window close event."""
        self.running = False
        self.root.quit()

    def ctrl_j_pressed(self, event):
        """Handle the Ctrl+J key press event."""
        self.j_pressed = True

    def ctrl_m_pressed(self, event):
        """Handle the Ctrl+M key press event and trigger unlock if Ctrl+J was pressed before."""
        if self.j_pressed:
            print("Ctrl+J+M combination detected, toggling lock state...")
            self.command_queue.put("toggle")

    def listen_for_commands(self):
        """
        Continuously listen for voice commands in a separate thread.
        Recognized commands are put into a queue for processing.
        """
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)

        while self.running:
            try:
                with microphone as source:
                    self.update_status(True)
                    print("Listening for commands...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                self.update_status(False)
                print("Processing audio...")
                recognized_text = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {recognized_text}")

                if self.activation_phrase in recognized_text:
                    print("Activation phrase recognized, toggling lock state...")
                    self.command_queue.put("toggle")
            except sr.WaitTimeoutError:
                print("No speech detected, continuing to listen...")
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError:
                print("Could not request results from the speech recognition service")
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Retrying in 5 seconds...")
                time.sleep(5)

    def process_commands(self):
        """Process commands from the queue in the main thread."""
        try:
            while not self.command_queue.empty():
                command = self.command_queue.get_nowait()
                if command == "toggle":
                    self.toggle_lock_state()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_commands)

    def update_status(self, is_listening):
        """Update the status label to show the current state of the voice recognition."""
        self.is_listening = is_listening
        status_text = "Listening..." if is_listening else "Processing..."
        status_color = "green" if is_listening else "orange"
        self.root.after(0, lambda: self.status_label.config(text=status_text, fg=status_color))

    def toggle_lock_state(self):
        """Toggle between locked and unlocked states."""
        if self.is_locked:
            self.unlock()
        else:
            self.lock()

    def unlock(self):
        """Unlock the screen by hiding the lock screen windows."""
        self.is_locked = False
        for window in self.windows:
            window.withdraw()

    def lock(self):
        """
        Lock the screen by showing the lock screen windows and bringing them to the foreground.
        Uses platform-specific methods to ensure the windows stay on top.
        """
        self.is_locked = True
        for window in self.windows:
            window.deiconify()
            window.lift()
            window.attributes('-topmost', True)
            window.focus_force()
            window.update()

        # Force the windows to be on top (Windows-specific)
        if hasattr(ctypes, 'windll'):
            ctypes.windll.user32.LockSetForegroundWindow(2)

    def run(self):
        """Start the lock screen application."""
        self.lock()  # Start in locked state
        self.root.mainloop()
        self.running = False

# Example usage
if __name__ == "__main__":
    lock_screen = LockScreen()
    lock_screen.run()