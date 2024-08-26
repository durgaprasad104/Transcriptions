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

def download_video_with_audio(video_url):
    """Download video with audio and return the video path."""
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'original_video.mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return 'original_video.mp4'
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
    try:
        translator = Translator()
        translated = translator.translate(text, dest=dest_language)
        return translated.text
    except Exception as e:
        st.error(f"Error translating text: {e}")
        return None

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

def replace_audio_in_video(video_path, audio_path):
    """Replace the original audio in the video with the new audio."""
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        output_path = "final_video_with_translated_audio.mp4"
        final_clip.write_videofile(output_path, codec='libx264')
        return output_path
    except Exception as e:
        st.error(f"Error replacing audio: {e}")
        return None

def main():
    st.title("YouTube Video Translator & Audio Replacer")

    video_url = st.text_input("YouTube Video URL")
    language = st.selectbox("Select Language", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("english"))

    if st.button("Process Video"):
        video_id = get_video_id(video_url)
        if video_id:
            st.write("Downloading video with original audio...")
            video_path = download_video_with_audio(video_url)
            
            if video_path:
                st.success("Video downloaded successfully!")
                st.write("Extracting transcript...")
                transcript_text = download_transcript(video_id)
                
                if transcript_text:
                    st.write("Original Transcript:")
                    st.write(transcript_text)
                    
                    st.download_button("Download Original Transcript", data=transcript_text, file_name="transcript.txt", mime="text/plain")
                    
                    lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(language)]
                    
                    st.write("Translating transcript...")
                    translated_text = translate_text(transcript_text, lang_code)
                    
                    if translated_text:
                        st.write("Translated Transcript:")
                        st.write(translated_text)
                        
                        st.download_button("Download Translated Transcript", data=translated_text, file_name="translated_transcript.txt", mime="text/plain")
                        
                        st.write("Generating audio...")
                        audio_path = generate_audio_from_text(translated_text, lang_code)
                        
                        if audio_path:
                            st.success("Audio generated successfully!")
                            st.download_button("Download Translated Audio", data=open(audio_path, 'rb'), file_name="translated_audio.mp3", mime="audio/mp3")
                            
                            st.write("Replacing original audio with translated audio...")
                            final_video_path = replace_audio_in_video(video_path, audio_path)
                            
                            if final_video_path:
                                st.success("Final video created successfully!")
                                st.video(final_video_path)
                                st.download_button("Download Final Video", data=open(final_video_path, 'rb'), file_name="final_video.mp4", mime="video/mp4")

if __name__ == "__main__":
    main()
