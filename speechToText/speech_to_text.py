from speech_recognition import Recognizer, AudioFile

# Initialize the recognizer
recognizer = Recognizer()

# Load the audio file (WAV format) and process it
with AudioFile('presentation.wav') as audio_file:
    # Record the audio from the file
    audio = recognizer.record(audio_file)

# Recognize speech using Google Web Speech API
text = recognizer.recognize_google(audio)
print(text)

# Save the recognized text in a new .txt file
with open('recognized_text.txt', 'w') as file:
    file.write(text)