from moviepy.editor import VideoFileClip
import speech_recognition as sr
from googletrans import Translator
import pysrt
from pydub import AudioSegment
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import TextClip, CompositeVideoClip
from datetime import datetime, timedelta
from moviepy.editor import concatenate_videoclips
from gtts import gTTS
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip


def translate_text(text, input_lang, output_lang):
    translator = Translator()
    translated = translator.translate(text, src=input_lang, dest=output_lang)
    print("Inside translate_text method")
    print(translated.text)
    return translated.text


def audio_to_text(audio_path, input_lang):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language=input_lang)
    return text


def generate_subtitles(text, output_lang, output_path):
    encoding_map = {
        'en': 'utf-8',  # Example: English encoding
        'hi': 'utf-8',  # Example: Hindi encoding
        # Add more language codes and corresponding encodings if needed
    }

    encoding = encoding_map.get(output_lang, 'utf-8')  # Default to utf-8 if encoding is not found

    subs = pysrt.SubRipFile()
    subs.append(pysrt.SubRipItem(1, start='00:00:00,000', end='00:00:02,000', text=text))
    subs.save(output_path, encoding=encoding)

def text_to_speech(text,language,video_path):
    #text = input("Enter the text: ")
    #language = input("Enter the language code (e.g., en, hi, ta): ")

    # Generate audio from text
    tts = gTTS(text, lang=language)
    tts.save('output.mp3')
    print('Audio file saved as output.mp3')

    # Hard-coded video path
    #video_path = 'testRupali.mp4'

    # Remove original audio from the video
    video = VideoFileClip(video_path)
    video_without_audio = video.set_audio(None)

    # Load generated audio
    audio = AudioFileClip('output.mp3')

    # Set the generated audio as the audio for the video
    final_video = video_without_audio.set_audio(audio)

    # Save the final video as MP4
    final_video.write_videofile('output_video.mp4', codec='libx264')

    print('Final video saved as output_video.mp4')



def add_subtitles(video_path, subs_path, output_path):
    video = VideoFileClip(video_path)
    subs = []
    start = None
    end = None

    with open(subs_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                if '-->' in line:
                    start, end = line.split('-->')
                    start = start.strip()
                    end = end.strip()
                else:
                    text = line
                    if start is not None and end is not None:
                        subs.append(((start, end), text))

    if not subs:
        print("No subtitles found in the file.")
        return

    # Create a function to generate text overlays for each subtitle
    from datetime import datetime

    def subtitle_overlay(subtitle, fontsize):
        start_time = datetime.strptime(subtitle[0][0], '%H:%M:%S,%f')
        end_time = datetime.strptime(subtitle[0][1], '%H:%M:%S,%f')
        text = subtitle[1]
    
        start_time_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second + start_time.microsecond / 1000000.0
        duration_seconds = (end_time - start_time).total_seconds()
    
        return TextClip(text, fontsize=fontsize, font='Arial', color='white').set_start(start_time_seconds).set_duration(duration_seconds)


    # Create a SubtitlesClip with the subtitle overlays
    subtitles = [subtitle_overlay(sub, 14) for sub in subs]
    subtitles = concatenate_videoclips(subtitles)

    # Set the audio of the video clip to the original audio
    video = video.set_audio(video.audio)

    # Overlay the subtitles on the video
    video = CompositeVideoClip([video, subtitles.set_position(("center", "bottom"))])

    # Write the final video with subtitles
    video.write_videofile(output_path, codec='libx264', audio_codec="aac", remove_temp=False)
    video.close()


video_path = "ENGIP.mp4"
output_audio_path = "output_audio.wav"
output_lang = input("The output language in which translation is desired: ")
input_lang = input("The input language of the Video file : ")

video = VideoFileClip(video_path)
audio = video.audio
audio.write_audiofile(output_audio_path, codec='pcm_s16le', bitrate='16k')
video.close()

text = audio_to_text(output_audio_path, input_lang)
print("Here is speech to text conversion in the original input language")
print(text)
translated_text = translate_text(text, input_lang, output_lang)

output_subs_path = "output_subtitles.srt"
generate_subtitles(translated_text, output_lang, output_subs_path)

#commenting this because now this will be done, final outputVideo would be produced inside final method text_to_speech()
#output_video_path = "output_video.mp4"

#Commenting add_subtitles so that we are not burning it immediately for editing purpose.
#add_subtitles(video_path, output_subs_path, output_video_path)

#calling our final_method text_to_speech()
text_to_speech(translated_text,output_lang,video_path)



print("Video with converted audio generated successfully, subtitles are generated in the same directory.")
#print("Output Video Path:", output_video_path)
