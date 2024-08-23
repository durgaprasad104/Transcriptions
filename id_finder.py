import streamlit as st
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip

def get_video_id(url):
    """Extract the video ID from the YouTube URL."""
    if "watch?v=" in url:
        return url.split("watch?v=")[-1]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1]
    else:
        st.error("Invalid YouTube URL")
        return None

def download_video_without_audio(video_url):
    """Download video without audio and return the video path."""
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]',
            'outtmpl': 'video_without_audio.mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return 'video_without_audio.mp4'
    except Exception as e:
        st.error(f"Error downloading video: {e}")
        return None

def download_transcript(video_id):
    """Fetch and return the transcript of the video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

def translate_text(text, dest_language):
    """Translate the given text to the specified language."""
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    return translated.text

def generate_audio_from_text(text, lang_code):
    """Generate audio from translated text and return the audio path."""
    try:
        tts = gTTS(text=text, lang=lang_code)
        audio_path = "translated_audio.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

def combine_video_audio(video_path, audio_path):
    """Combine the video without audio and generated audio into one file."""
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        output_path = "final_video_with_translated_audio.mp4"
        final_clip.write_videofile(output_path, codec='libx264')
        return output_path
    except Exception as e:
        st.error(f"Error combining video and audio: {e}")
        return None

def main():
    st.title("YouTube Video Translator & Combiner")

    video_url = st.text_input("YouTube Video URL")
    language = st.selectbox("Select Language", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("english"))

    if st.button("Process Video"):
        video_id = get_video_id(video_url)
        if video_id:
            st.write("Downloading video without audio...")
            video_path = download_video_without_audio(video_url)
            
            if video_path:
                st.success("Video downloaded successfully!")
                st.write("Extracting transcript...")
                transcript_text = download_transcript(video_id)
                
                if transcript_text:
                    st.write("Original Transcript:")
                    st.write(transcript_text)
                    
                    lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(language)]
                    
                    st.write("Translating transcript...")
                    translated_text = translate_text(transcript_text, lang_code)
                    
                    st.write("Translated Transcript:")
                    st.write(translated_text)
                    
                    st.write("Generating audio...")
                    audio_path = generate_audio_from_text(translated_text, lang_code)
                    
                    if audio_path:
                        st.success("Audio generated successfully!")
                        st.write("Combining video with translated audio...")
                        final_video_path = combine_video_audio(video_path, audio_path)
                        
                        if final_video_path:
                            st.success("Final video created successfully!")
                            st.video(final_video_path)
                            st.download_button("Download Final Video", data=open(final_video_path, 'rb'), file_name="final_video.mp4", mime="video/mp4")

if __name__ == "__main__":
    main()
