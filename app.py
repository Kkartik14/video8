import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time
import base64

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Prompt-to-2D-Video Generator",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# API endpoint
API_URL = "http://localhost:8000"

def get_video_data(video_path):
    """Get video data as base64 string"""
    with open(video_path, 'rb') as video_file:
        video_data = video_file.read()
    return base64.b64encode(video_data).decode()

def main():
    # App title and description
    st.title("🎬 Prompt-to-2D-Video Generator")
    st.markdown("""
    Convert natural language prompts into animated educational videos using LLM and Manim.
    Enter a prompt describing what animation you'd like to see, and our system will create it for you!
    """)
    
    st.markdown("---")
    
    # Input form
    with st.form("generation_form"):
        # Text input for prompt
        prompt = st.text_area(
            "Enter your animation prompt:",
            placeholder="Example: Visualize the Pythagorean theorem with animated squares and triangles",
            height=100
        )
        
        # Model selection
        model = st.selectbox(
            "Choose LLM model:",
            options=["claude", "groq"],
            index=0,
            help="Select which AI model to use for code generation"
        )
        
        # Submit button
        submitted = st.form_submit_button("Generate Animation")
    
    # Handle form submission
    if submitted and prompt:
        with st.spinner("Generating your animation... This may take a minute."):
            try:
                # Make API request
                response = requests.post(
                    f"{API_URL}/generate", 
                    json={"prompt": prompt, "model": model}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    video_path = result["video_path"]
                    
                    # Display success message
                    st.success("Video generated successfully!")
                    
                    # Display the video
                    st.video(video_path)
                    
                    # Download button
                    with open(video_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Video",
                            data=file,
                            file_name=f"animation_{os.path.basename(video_path)}",
                            mime="video/mp4"
                        )
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Example gallery
    st.markdown("---")
    st.subheader("Example Prompts")
    
    example_prompts = [
        "Visualize the Pythagorean theorem with animated squares and triangles",
        "Show how binary search works with an array of numbers",
        "Demonstrate the concept of gravitational force between two objects",
        "Illustrate the quadratic formula solving process",
        "Visualize sorting algorithms like bubble sort and quick sort"
    ]
    
    for i, example in enumerate(example_prompts):
        if st.button(f"Try Example {i+1}", key=f"example_{i}"):
            st.session_state.example_prompt = example
            st.experimental_rerun()
    
    # Instructions and about section in sidebar
    with st.sidebar:
        st.subheader("About")
        st.markdown("""
        This app uses AI to generate beautiful math and physics animations from natural language prompts.
        
        **How it works:**
        1. You enter a prompt describing what you want to see
        2. An LLM (Claude or Groq) generates Manim code
        3. The Manim library renders the animation
        4. You get a downloadable video!
        
        **Tips for good prompts:**
        - Be specific about what concepts you want to visualize
        - Mention colors, shapes, and movements you'd like to see
        - Specify labels or annotations that would help explain the concept
        """)
        
        st.subheader("Credits")
        st.markdown("""
        - Powered by [Manim](https://www.manim.community/)
        - Uses AI from Anthropic (Claude) and Groq
        - Built with Streamlit and FastAPI
        """)

if __name__ == "__main__":
    main() 