# Prompt-to-2D-Video Generator Backend

This is the FastAPI backend for the Prompt-to-2D-Video Generator application. It handles prompt processing, code generation via LLMs, and video rendering using Manim.

## Features

- FastAPI REST API for video generation
- Integration with Claude and Groq LLMs
- Manim-based rendering engine
- Pre-built templates for common mathematical concepts
- Video storage and retrieval

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_api_key_here
GROQ_API_KEY=your_api_key_here
```

3. Start the API server:

```bash
python main.py
```

The server will be available at http://localhost:8000.

## API Endpoints

### POST /generate

Generates a video from a natural language prompt.

Request:
```json
{
  "prompt": "Visualize the Pythagorean theorem",
  "model": "claude" // or "groq"
}
```

Response:
```json
{
  "video_path": "outputs/12345.mp4",
  "message": "Video generated successfully!"
}
```

### GET /video/{video_id}

Retrieves a previously generated video.

## Components

- `main.py`: Entry point and FastAPI server
- `llm_handler.py`: Claude API integration for prompt processing
- `groq_handler.py`: Groq API integration for prompt processing
- `scene_generator.py`: Manim scene generation logic

## Requirements

- Python 3.9+
- LaTeX installation (MacTeX on macOS, TeX Live on Linux, MiKTeX on Windows)
- API keys for Claude and/or Groq 