import streamlit as st
import re

def extract_youtube_video_id(url):
    # Regular expression to match YouTube video URLs
    regex = (
        r'(?:https?:\/\/)?(?:www\.)?'
        '(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|'
        'youtu\.be\/)([a-zA-Z0-9_-]{11})'
    )

    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        return None

def main():
    st.title('Youtube Video ID Finder')

    # Input field for the URL
    url = st.text_input('Enter a YouTube URL')

    # Button to trigger video ID extraction
    if st.button('DP i want my id'):
        if url:
            video_id = extract_youtube_video_id(url)
            if video_id:
                st.success(f' Idhugoo raa nii video ID : {video_id}')
            else:
                st.warning('Please enter a valid YouTube URL')

if __name__ == "__main__":
    main()
