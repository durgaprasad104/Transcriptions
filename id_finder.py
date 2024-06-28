import streamlit as st
import re
import pyperclip  # This package helps in copying text to clipboard

def extract_youtube_video_id(url):
    # Regular expression to match YouTube video URLs, including Shorts
    video_id = None
    regex_shorts = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})'
    regex_video = (
        r'(?:https?:\/\/)?(?:www\.)?'
        '(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|'
        'youtu\.be\/)([a-zA-Z0-9_-]{11})'
    )

    match_shorts = re.search(regex_shorts, url)
    match_video = re.search(regex_video, url)

    if match_shorts:
        video_id = match_shorts.group(1)
    elif match_video:
        video_id = match_video.group(1)

    return video_id

def main():
    st.title('YouTube Video ID Extractor')

    # Input field for the URL
    url = st.text_input('Enter a YouTube URL')

    # Button to trigger video ID extraction
    if st.button('Get Video ID'):
        if url:
            video_id = extract_youtube_video_id(url)
            if video_id:
                st.success(f'The extracted video ID is: {video_id}')
                # Button to copy video ID to clipboard
                if st.button('Copy Video ID'):
                    pyperclip.copy(video_id)
                    st.info('Video ID copied to clipboard!')
            else:
                st.warning('Please enter a valid YouTube URL')

if __name__ == "__main__":
    main()
