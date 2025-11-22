# AI Music Generator Agent

This is an AI-powered music generation agent that creates music based on your text descriptions.

## Features
- **Text-to-Music**: Describe the music you want (e.g., "Sad piano", "Upbeat techno"), and the agent will create it.
- **AI Enhanced**: Uses Google Gemini to refine your prompts for better musical results.
- **High Quality**: Uses Facebook's MusicGen model for audio generation.
- **Modern UI**: A beautiful, dark-themed interface.

## Setup

1.  **Install Dependencies**:
    ```bash
    uv sync
    ```

2.  **Environment Variables**:
    Ensure you have a `.env` file with your Google API key:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

3.  **Run the Server**:
    ```bash
    uv run uvicorn main:app --reload
    ```

4.  **Access the App**:
    Open your browser and go to `http://localhost:8000`.

## Note on First Run
The first time you run the app, it will download the MusicGen model (approx. 1.5GB). This may take a few minutes depending on your internet connection.
