import streamlit as st
import google.generativeai as genai
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Streamlit Page Configurations
st.set_page_config(page_title="YouTube Video Summarizer", page_icon="📺", layout="wide")

# 🌟 Custom CSS for a modern and colorful UI
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #2F80ED, #56CCF2);
            font-family: 'Poppins', sans-serif;
            color: white;
        }

        /* Main Title */
        .main-title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: white;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }

        /* Subtitle */
        .sub-title {
            font-size: 22px;
            text-align: center;
            color: #E0F7FA;
            margin-bottom: 30px;
        }

        /* Input box */
        .stTextInput>div>div>input {
            background: white !important;
            color: black !important;
            border: 2px solid #2F80ED !important;
            border-radius: 10px !important;
            font-size: 18px !important;
            padding: 12px !important;
        }

        /* Stylish Button */
        .stButton>button {
            background: linear-gradient(45deg, #ff5733, #ff9900);
            color: white;
            padding: 12px 30px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(45deg, #ff2e00, #ff6600);
            box-shadow: 0px 0px 12px rgba(255, 87, 51, 0.6);
            transform: scale(1.05);
        }

        /* Summary Box */
        .summary-box {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            font-size: 18px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease-in-out;
            color: white;
        }
        .summary-box:hover {
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

# 🌟 Title and Subtitle
st.markdown("<h1 class='main-title'>📺 YouTube Video Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-title'>Summarize YouTube videos in seconds! 🚀</h3>", unsafe_allow_html=True)

# 🔗 User Input for YouTube Video URL
video_url = st.text_input("🔗 Enter YouTube Video URL:", key="video_url", help="Paste a valid YouTube video link here")

# 📌 Extract Video ID Function
def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# 🚀 Fetch Transcript and Generate Summary
if st.button("✨ Generate Summary", key="summarize", help="Click to generate summary"):
    video_id = get_video_id(video_url)

    if not video_id:
        st.error("⚠️ Invalid YouTube URL. Please enter a valid video link.")
    else:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([t["text"] for t in transcript])

            # Use Generative AI to summarize
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Summarize this video transcript: {transcript_text}")
            summary = response.text

            # 📜 Display Summary
            st.markdown("<h2 style='color:#E0F7FA;'>📄 Summary:</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}") 
