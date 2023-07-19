# Import libraries
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from moviepy.editor import VideoFileClip
from pathlib import Path

# Create a speech recognition object
r = sr.Recognizer()

def transcribe_large_audio(path):
    #19July test
    #path = Path(audio_file_path)
    """Split audio into chunks and apply speech recognition"""
    # Open audio file with pydub
    sound = AudioSegment.from_wav(path)

    # Split audio where silence is 700ms or greater and get chunks
    chunks = split_on_silence(sound, min_silence_len=700, silence_thresh=sound.dBFS-14, keep_silence=700)
    
    # Create folder to store audio chunks
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    
    whole_text = ""
    # Process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # Export chunk and save in folder
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        # Recognize chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # Convert to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text

    # Return text for all chunks
    return whole_text

#adding on 19July code to convert audio file to wav first
def convert_mp4_to_wav(input_file, output_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file, codec='pcm_s16le', ffmpeg_params=['-ac', '1'])

input_file = 'LongAudioTSS.mp4'
output_file = 'transcribed_speech1.wav'
convert_mp4_to_wav(input_file, output_file)

result = transcribe_large_audio(output_file)

print(result)
print(result, file=open('result.txt', 'w'))