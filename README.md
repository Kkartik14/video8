# 🎬 Prompt-to-2D-Video Generator

An intelligent system that converts natural language prompts into beautiful 2D animated videos using LLM and Manim.

## 🌟 Features

- Natural language prompt processing
- Automatic Manim animation code generation with Claude or Groq
- Script viewing and downloading for learning and customization
- Video rendering and delivery
- Educational and conceptual visualization support
- Modern Next.js frontend with a clean, responsive UI
- FastAPI backend with straightforward REST API

## 🚀 Quick Start

The easiest way to get started is using our setup script:

```bash
# Run the interactive setup script
npm run setup
```

This will guide you through:
- Creating necessary directories
- Setting up environment variables
- Installing dependencies
- Building the frontend

After setup is complete, start the application:

```bash
# Start both backend and frontend in development mode
npm start
```

This will start both the backend server at http://localhost:8000 and the frontend at http://localhost:3000.

## 📦 Production Deployment

To build and run the application in production mode:

```bash
# Build the frontend
npm run build

# Start both services in production mode
npm run start:prod
```

## 🔧 Manual Setup

If you prefer to set up each component separately:

1. Install backend dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_api_key_here
GROQ_API_KEY=your_api_key_here
```

3. Run the API server:
```bash
npm run backend
# Or directly: python3 backend/main.py
```

4. Install and run the frontend:
```bash
npm run install:frontend
npm run frontend
# Or directly: cd frontend && npm install && npm run dev
```

## 🎯 Usage

### Via Next.js Frontend

Open your browser to `http://localhost:3000` to access the modern UI.

1. Enter your animation prompt in the text area
2. Select your preferred LLM (Claude or Groq)
3. Click "Generate Animation"
4. View and download your animation
5. View and download the generated Manim script to learn or modify

### Via API

Send a POST request to `/generate` with your prompt:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Visualize the Pythagorean theorem with animated squares and triangles", "model": "claude"}'
```

The response will include paths to both the video and the generated script:

```json
{
  "video_path": "/outputs/video_id",
  "script_path": "/scripts/script_id",
  "message": "Video and script generated successfully!"
}
```

You can access the generated script via the `/scripts/{script_id}` endpoint.

## 🔍 Troubleshooting

### Backend Connection Issues

If you see a "Connection Refused" error:

1. Make sure the backend is running:
```bash
python3 backend/main.py
```

2. Check if the port 8000 is in use by another application:
```bash
lsof -i :8000
```

3. Verify your `.env` file has the required API keys:
```
ANTHROPIC_API_KEY=your_api_key_here
GROQ_API_KEY=your_api_key_here
```

### Video Generation Issues

1. Check that LaTeX is properly installed (required by Manim):
   - macOS: Install MacTeX (`brew install --cask mactex`)
   - Linux: Install TexLive (`apt-get install texlive-full`)
   - Windows: Install MiKTeX

2. Ensure the `outputs` directory exists and is writable:
```bash
mkdir -p outputs
chmod 755 outputs
```

3. Check the logs for specific error messages:
```bash
python3 -m pip install manim --upgrade
```

4. If you encounter "self reference" or "indentation" errors in the generated code:
   - These errors are usually fixed automatically by our error handling system
   - For persistent issues, try using a simpler prompt or one of our template animations

### Video Not Found Issues

If you receive a 404 error when trying to view a generated video:

1. Make sure the video was successfully generated without errors
2. Check that the URL path matches the format returned by the API (`/outputs/{video_id}`)
3. If using a custom setup, ensure the frontend is correctly configured to access the backend URL

## 🛠️ Project Structure

- `backend/`: Backend FastAPI application
  - `main.py`: Entry point and FastAPI server
  - `llm_handler.py`: Claude API integration
  - `groq_handler.py`: Groq API integration
  - `scene_generator.py`: Manim scene generation logic
- `frontend/`: Next.js frontend application
  - `pages/`: Next.js pages
  - `components/`: React components
  - `styles/`: CSS styles
  - `utils/`: Utility functions
- `outputs/`: Generated video storage
- `index.js`: Unified startup script for development
- `setup.js`: Interactive setup script
- `docker-compose.yml`: Docker configuration

## 🐳 Docker Deployment

You can also run the application using Docker Compose:

```bash
docker-compose up -d
```

This will build and start both the backend and frontend services.

## 🎨 Requirements

- Python 3.9+
- Node.js 16+
- LaTeX installation (MacTeX on macOS, TeX Live on Linux, MiKTeX on Windows)
- API keys for Claude and/or Groq

## 📝 Example Prompts

- "Visualize the Pythagorean theorem with animated squares and triangles"
- "Show how binary search works with an array of numbers"
- "Demonstrate the concept of gravitational force between two objects"
- "Illustrate the quadratic formula solving process"
- "Visualize sorting algorithms like bubble sort and quick sort"

## 🔄 Switching from Streamlit

This application includes both the original Streamlit interface (`app.py`) and the new Next.js frontend (`frontend/`).
To use the Streamlit version instead of Next.js, run:

```bash
streamlit run app.py
```

## 🧹 Cleaning Up

To remove unnecessary files and clean up generated content, use the provided cleanup script:

```bash
# Make the script executable if needed
chmod +x cleanup.sh

# Run the cleanup script
./cleanup.sh
```

This script removes:
- Redundant duplicate Python files in the root directory
- Python cache files (__pycache__ directories)
- Test media files
- Generated temporary output files

The script preserves the necessary directory structure while removing unnecessary content 