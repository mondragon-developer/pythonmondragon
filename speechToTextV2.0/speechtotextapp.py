import tkinter as tk
from tkinter import filedialog, messagebox
from speech_recognition import Recognizer, AudioFile, Microphone
import pyaudio
import wave

class SpeechToTextApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("Speech to Text")

        # Initialize the speech recognizer
        self.recognizer = Recognizer()

        # Create and place the Record button
        self.record_button = tk.Button(root, text="Record", command=self.record_audio)
        self.record_button.pack(pady=20)

        # Create and place the Convert to Text button (initially disabled)
        self.convert_button = tk.Button(root, text="Convert to Text", command=self.convert_to_text, state=tk.DISABLED)
        self.convert_button.pack(pady=20)

        # Create and place the text output box
        self.text_output = tk.Text(root, wrap='word', height=10, width=50)
        self.text_output.pack(pady=20)

        # Create and place the Save to .txt button (initially disabled)
        self.save_button = tk.Button(root, text="Save to .txt", command=self.save_to_file, state=tk.DISABLED)
        self.save_button.pack(pady=20)

        # Variable to store the file path of the recorded audio
        self.file_path = None

    def record_audio(self):
        # File path to save the recorded audio
        self.file_path = 'recorded_audio.wav'
        
        # Parameters for audio recording
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 60  # Duration of recording
        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')

        # Open a stream for recording
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 5 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(self.file_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Enable the Convert to Text button after recording
        self.convert_button.config(state=tk.NORMAL)

    def convert_to_text(self):
        # Check if an audio file has been recorded
        if not self.file_path:
            messagebox.showerror("Error", "No audio file recorded.")
            return

        try:
            # Load and process the recorded audio file
            with AudioFile(self.file_path) as audio_file:
                audio = self.recognizer.record(audio_file)
                # Recognize speech using Google Web Speech API
                text = self.recognizer.recognize_google(audio)
                # Insert recognized text into the text output box
                self.text_output.insert(tk.END, text)
                # Enable the Save to .txt button after converting to text
                self.save_button.config(state=tk.NORMAL)
        except Exception as e:
            # Display an error message if speech recognition fails
            messagebox.showerror("Error", str(e))

    def save_to_file(self):
        # Check if there is text to save
        if not self.text_output.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "No text to save.")
            return

        # Open a file dialog to choose where to save the .txt file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            # Save the recognized text to the chosen file
            with open(file_path, 'w') as file:
                file.write(self.text_output.get("1.0", tk.END))
            messagebox.showinfo("Success", "File saved successfully.")

if __name__ == "__main__":
    # Create the main window and run the application
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()
