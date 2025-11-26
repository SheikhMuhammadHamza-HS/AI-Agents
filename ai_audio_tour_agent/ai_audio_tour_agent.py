"""AI Audio Tour Agent - Streamlit Application"""
import streamlit as st
import os
from gtts import gTTS
from config import config
from manager import create_tour_manager
from printer import printer

# Page configuration
st.set_page_config(
    page_title="AI Audio Tour Agent",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .tour-output {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin-top: 2rem;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🎧 AI Audio Tour Agent</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Create personalized audio tours powered by Google Gemini AI</p>',
        unsafe_allow_html=True
    )
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.markdown("""
        <div class="info-box">
            <strong>🔑 Get your Gemini API Key:</strong><br>
            Visit <a href="https://aistudio.google.com/apikey" target="_blank">Google AI Studio</a>
        </div>
        """, unsafe_allow_html=True)
        
        # API Key input
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=config.get_gemini_api_key(),
            help="Enter your Google Gemini API key"
        )
        
        if api_key:
            config.set_gemini_api_key(api_key)
            st.success("✅ API Key configured!")
        else:
            st.warning("⚠️ Please enter your API key")
        
        st.divider()
        
        # About section
        st.header("ℹ️ About")
        st.markdown("""
        This app creates personalized audio tours using:
        - **Google Gemini AI** for intelligent content generation
        - **Multi-agent system** with specialized experts
        - **Web search** for accurate, current information
        
        **Features:**
        - 🎯 Interest-based content
        - ⏱️ Flexible duration (1-60 min)
        - 🌍 Any location worldwide
        - 📝 Detailed tour narratives
        - 🎙️ Audio generation (MP3)
        """)
    
    # Main content area
    if not config.is_configured():
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to get started.")
        return
    
    # Tour configuration
    st.header("🗺️ Tour Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input(
            "📍 Location",
            placeholder="e.g., Karachi, Eiffel Tower, Rome",
            help="Enter a city, landmark, or location you want to explore"
        )
    
    with col2:
        duration = st.slider(
            "⏱️ Tour Duration (minutes)",
            min_value=1,
            max_value=2,
            value=15,
            step=1,
            help="Choose how long you want your tour to be"
        )
    
    # Interest selection
    st.subheader("🎯 Select Your Interests")
    
    col1, col2, col3, col4 = st.columns(4)
    
    interests = []
    with col1:
        if st.checkbox("🏛️ Architecture", value=True):
            interests.append("Architecture")
    
    with col2:
        if st.checkbox("📜 History", value=True):
            interests.append("History")
    
    with col3:
        if st.checkbox("🍽️ Culinary", value=True):
            interests.append("Culinary")
    
    with col4:
        if st.checkbox("🎭 Culture", value=True):
            interests.append("Culture")
    
    # Generate tour button
    st.divider()
    
    # Initialize session state
    if 'tour_content' not in st.session_state:
        st.session_state.tour_content = None
    if 'audio_path' not in st.session_state:
        st.session_state.audio_path = None
    
    # Generate tour button
    st.divider()
    
    if st.button("🎬 Generate Tour", type="primary"):
        if not location:
            st.error("❌ Please enter a location!")
            return
        
        if not interests:
            st.error("❌ Please select at least one interest!")
            return
        
        # Generate tour
        with st.spinner(f"🔄 Generating your {duration}-minute tour of {location}..."):
            try:
                # Create tour manager
                manager = create_tour_manager()
                
                # Generate tour
                tour_content = manager.generate_tour(
                    location=location,
                    interests=interests,
                    duration=duration
                )
                
                # Save to session state
                st.session_state.tour_content = tour_content
                st.session_state.audio_path = None  # Reset audio when new tour generated
                
            except Exception as e:
                st.error(f"❌ Error generating tour: {str(e)}")
                printer.print_error(str(e))

    # Display Tour Content (if exists in session state)
    if st.session_state.tour_content:
        tour_content = st.session_state.tour_content
        
        # Display tour
        st.success("✅ Tour generated successfully!")
        
        st.markdown('<div class="tour-output">', unsafe_allow_html=True)
        st.markdown(f"### 🎧 Your {location} Audio Tour")
        st.markdown(f"**Duration:** {duration} minutes | **Interests:** {', '.join(interests)}")
        st.divider()
        
        # Display Generated Image
        try:
            # Construct image prompt based on location and interests
            main_interest = interests[0] if interests else "travel"
            image_prompt = f"cinematic shot of {location}, {main_interest} style, 8k, highly detailed, professional photography, dramatic lighting"
            image_url = f"https://image.pollinations.ai/prompt/{image_prompt.replace(' ', '%20')}"
            
            st.image(image_url, caption=f"AI Generated Image of {location}", use_container_width=True)
        except Exception as img_error:
            st.warning("Could not generate image, but here is your tour:")
            
        st.markdown(tour_content)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Audio Generation Section
        st.divider()
        st.subheader("🎵 Audio Generation")
        
        # Voice Settings
        st.markdown("### 🎙️ Voice Settings")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            voice_engine = st.selectbox(
                "Voice Engine",
                ["Edge TTS (High Quality)", "Google TTS (Fast)"],
                help="Choose the text-to-speech engine"
            )
        
        with col2:
            if "Edge TTS" in voice_engine:
                voice_name = st.selectbox(
                    "Voice",
                    [
                        "en-US-AriaNeural (Female)",
                        "en-US-GuyNeural (Male)",
                        "en-US-JennyNeural (Female)",
                        "en-US-DavisNeural (Male)",
                        "en-GB-SoniaNeural (Female)",
                        "en-GB-RyanNeural (Male)",
                        "en-AU-NatashaNeural (Female)",
                        "en-AU-WilliamNeural (Male)",
                        "en-IN-NeerjaNeural (Female)",
                        "en-IN-PrabhatNeural (Male)"
                    ],
                    help="Select voice type"
                )
            else:
                voice_name = "Default Google Voice"
                st.info("Google TTS uses default voice")
        
        with col3:
            speech_rate = st.slider(
                "Speech Speed",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Adjust speaking speed"
            )
        
        # Generate Audio Button
        st.markdown("### 🎬 Generate")
        col1, col2 = st.columns(2)
        
        with col1:
            # Download text
            st.download_button(
                label="📥 Download Tour as Text",
                data=tour_content,
                file_name=f"{location.replace(' ', '_')}_tour.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # Generate audio button
            if st.button("🎙️ Generate Audio", use_container_width=True, type="primary"):
                with st.spinner("🔄 Converting text to speech..."):
                    try:
                        # Create audio directory
                        audio_dir = "audio_tours"
                        os.makedirs(audio_dir, exist_ok=True)
                        
                        # Generate audio filename
                        audio_filename = f"{location.replace(' ', '_')}_tour.mp3"
                        audio_path = os.path.join(audio_dir, audio_filename)
                        
                        if "Edge TTS" in voice_engine:
                            # Use Edge TTS for high-quality voices
                            import asyncio
                            import edge_tts
                            
                            # Extract voice ID from selection
                            voice_id = voice_name.split(" (")[0]
                            
                            # Calculate rate for edge-tts
                            rate_percent = int((speech_rate - 1.0) * 100)
                            rate_str = f"{rate_percent:+d}%"
                            
                            async def generate_edge_audio():
                                communicate = edge_tts.Communicate(
                                    tour_content, 
                                    voice_id,
                                    rate=rate_str
                                )
                                await communicate.save(audio_path)
                            
                            # Run async function
                            asyncio.run(generate_edge_audio())
                            
                        else:
                            # Use Google TTS (gTTS)
                            from gtts import gTTS
                            slow_speech = speech_rate < 0.9
                            tts = gTTS(text=tour_content, lang='en', slow=slow_speech)
                            tts.save(audio_path)
                        
                        # Save audio path to session state
                        st.session_state.audio_path = audio_path
                        st.success(f"✅ Audio generated successfully with {voice_engine}!")
                        
                    except Exception as audio_error:
                        st.error(f"❌ Error generating audio: {str(audio_error)}")
                        st.info("💡 Try using Google TTS if Edge TTS fails")

        # Display Audio Player (if audio exists in session state)
        if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
            st.audio(st.session_state.audio_path, format='audio/mp3')
            
            # Download audio button
            with open(st.session_state.audio_path, 'rb') as audio_file:
                st.download_button(
                    label="📥 Download Audio (MP3)",
                    data=audio_file,
                    file_name=os.path.basename(st.session_state.audio_path),
                    mime="audio/mp3",
                    use_container_width=True
                )
        
        st.info("""
        **💡 Audio Features:**
        - 🎙️ **Edge TTS**: High-quality Microsoft voices with natural speech
        - 🌍 **Google TTS**: Fast generation with good quality
        - 🎚️ **Speed Control**: Adjust speech rate from 0.5x to 2.0x
        - 🎧 **Multiple Voices**: Choose from 10+ different voices
        - 📥 **Download**: Save as MP3 for offline listening
        """)

if __name__ == "__main__":
    main()
