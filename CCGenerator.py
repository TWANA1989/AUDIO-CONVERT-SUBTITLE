import os
import moviepy.editor as mp
import subprocess
import tkinter as tk
from tkinter import filedialog
from googletrans import Translator  # Import the Translator class from googletrans

# Global variable to store the path of the text file
text_file_path = ""

# Function to convert video to MP3 and run 'whisper'
def convert_and_extract_text():
    global text_file_path  # Use the global variable to store the text file path

    video_file = filedialog.askopenfilename(title="Select a video file")

    if video_file:
        os.environ["IMAGEIO_FFMPEG_EXE"] = r'C:\ProgramData\chocolatey\lib\ffmpeg-full\tools\ffmpeg.exe'
        audio_file = os.path.splitext(video_file)[0] + ".mp3"

        video = mp.VideoFileClip(video_file)
        video.audio.write_audiofile(audio_file)

        print(f"Video converted to MP3 with the same name as the video: {audio_file}")

        whisper_command = f'whisper "{audio_file}" --model medium'
        subprocess.run(whisper_command, shell=True)

        print("Text extraction completed.")

        # Set the text file path based on the audio file and the current working directory
        text_file_path = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(audio_file))[0] + ".txt")

# Function to manually browse and translate the text file
def browse_and_translate_text():
    global text_file_path  # Use the global variable to access the text file path

    if text_file_path:
        status_label.config(text="Translating...")  # Update status label

        # Load the text from the text file
        with open(text_file_path, "r", encoding="utf-8") as file:
            text_to_translate = file.read()

        # Create a Translator object
        translator = Translator()

        # Translate the text from English to Kurdish
        translated_text = translator.translate(text_to_translate, src="en", dest="ku")

        # Save the translated text to a new file
        translated_file_path = os.path.splitext(text_file_path)[0] + "_ku.txt"
        with open(translated_file_path, "w", encoding="utf-8") as file:
            file.write(translated_text.text)

        status_label.config(text="Translation completed.")  # Update status label
    else:
        status_label.config(text="Text file not found. Make sure text extraction is completed.")  # Update status label

# Create a Tkinter root window
root = tk.Tk()
root.geometry("400x200")

# Load the animated GIF file for the background
background_image = tk.PhotoImage(file="kurdistan.gif")

# Create a label widget to display the background GIF
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)  # Set the label size to cover the whole window

# Ensure the GIF animation plays by keeping a reference to the PhotoImage object
background_label.photo = background_image

# Create a button to browse and initiate conversion
browse_button = tk.Button(root, text="Browse Video File", command=convert_and_extract_text)
browse_button.pack()

# Create a label to display status
status_label = tk.Label(root, text="", fg="green")
status_label.pack()

# Create a button to browse and translate the text file
translate_button = tk.Button(root, text="Browse Text and Translate", command=browse_and_translate_text)
translate_button.pack()

root.mainloop()
