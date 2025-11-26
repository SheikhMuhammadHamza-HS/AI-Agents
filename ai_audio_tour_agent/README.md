# 🎧 AI Audio Tour Agent

**Your Personal AI Tour Guide** that generates immersive audio tours with **Images** and **Voice Narration** for any location worldwide. Powered by **Google Gemini 2.5 Flash**.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/AI-Gemini%202.5-orange)

---

## ✨ Key Features

### 🧠 Intelligent Core
*   **🤖 Google Gemini Powered**: Uses `gemini-2.5-flash` for smart, context-aware content.
*   **🕵️ Multi-Agent System**: 6 Specialized Agents (Planner, History, Architecture, Culinary, Culture, Orchestrator).
*   **🔍 Live Research**: Real-time web search for up-to-date information.

### 🎨 Rich Media Experience
*   **🖼️ AI Image Generation**: Automatically generates cinematic images of the location (via Pollinations AI).
*   **🎙️ Advanced Audio Engine**:
    *   **Edge TTS**: High-quality neural voices (10+ options, multiple accents).
    *   **Google TTS**: Fast and reliable backup.
    *   **Speed Control**: Adjust playback speed (0.5x - 2.0x).

### 🛠️ User Flexibility
*   **⏱️ Flexible Duration**: Tours from **1 to 60 minutes**.
*   **🎯 Custom Interests**: Choose from History, Architecture, Food, or Culture.
*   **📥 Downloadable**: Save tours as **MP3 Audio** or **Text Script**.

---

## 🚀 Quick Start

### 1. Prerequisites
*   Python 3.10 or higher installed.
*   A **Google Gemini API Key** (Get it [here](https://aistudio.google.com/apikey)).

### 2. Installation
Clone the repo and install dependencies:

```bash
# Install required packages
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the App
Launch the Streamlit interface:

```bash
streamlit run ai_audio_tour_agent.py
```

---

## 🎮 How to Use

1.  **📍 Enter Location**: Type any city, landmark, or hidden gem (e.g., "Lahore Fort", "Eiffel Tower").
2.  **⏱️ Set Duration**: Use the slider to choose tour length (1-60 mins).
3.  **🎯 Select Interests**: Check boxes for History, Architecture, Culinary, etc.
4.  **🎬 Generate Tour**: Click the button to create the script and image.
5.  **🎙️ Generate Audio**:
    *   Scroll down to **Audio Options**.
    *   Select **Voice Engine** (Edge TTS recommended).
    *   Choose a **Voice** (US, UK, AU, IN accents available).
    *   Click **Generate Audio** to listen or download MP3.

---

## 📂 Project Structure

```
ai_audio_tour_agent/
├── audio_tours/           # 🎵 Generated MP3 files saved here
├── agent.py               # 🤖 AI Agent definitions (Gemini 2.5)
├── ai_audio_tour_agent.py # 🖥️ Main Streamlit Application
├── manager.py             # ⚙️ Tour orchestration logic
├── config.py              # 🔑 API Key management
├── printer.py             # 🖨️ Console output utility
├── requirements.txt       # 📦 Project dependencies
└── .env                   # 🔒 API Keys (not committed)
```

---

## 🎙️ Voice Options

| Voice | Gender | Accent | Best For |
|-------|--------|--------|----------|
| **Aria/Guy** | F/M | 🇺🇸 US | General/Professional |
| **Sonia/Ryan** | F/M | 🇬🇧 UK | Historical/Documentary |
| **Natasha** | F | 🇦🇺 AU | Casual/Friendly |
| **Neerja/Prabhat** | F/M | 🇮🇳 IN | Local/Cultural |

---

## 🛠️ Tech Stack

*   **Frontend**: Streamlit
*   **AI Model**: Google Gemini 2.5 Flash
*   **Orchestration**: Phidata
*   **Audio**: Edge TTS, gTTS
*   **Image**: Pollinations AI
*   **Search**: Google Search Tools

---

## 🤝 Troubleshooting

*   **Audio not generating?** Try switching to "Google TTS (Fast)" in the dropdown.
*   **Image not showing?** Check your internet connection (Pollinations AI requires internet).
*   **API Error?** Ensure your Gemini API key is correct in `.env` or the sidebar.

---

Made with ❤️ by **Antigravity**
