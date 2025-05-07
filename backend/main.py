import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import tempfile
import uuid
from typing import Literal, Optional

# Add the current directory to sys.path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_handler import LLMHandler
from groq_handler import GroqHandler
from scene_generator import SceneGenerator

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Prompt-to-2D-Video Generator",
    description="Convert natural language prompts into animated videos using LLM and Manim",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str
    model: Optional[Literal["claude", "groq"]] = "claude"

class GenerationResponse(BaseModel):
    video_path: str
    message: str

@app.post("/generate", response_model=GenerationResponse)
async def generate_video(request: PromptRequest):
    try:
        # Create unique ID for this generation
        generation_id = str(uuid.uuid4())
        
        # Initialize handlers
        if request.model == "claude":
            llm_handler = LLMHandler()
        else:
            llm_handler = GroqHandler()
            
        scene_generator = SceneGenerator()
        
        # Generate Manim code from prompt
        manim_code = llm_handler.generate_manim_code(request.prompt)
        
        # Create temporary directory for video output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate and render the video
            video_path = scene_generator.create_video(
                manim_code,
                output_dir=temp_dir,
                generation_id=generation_id
            )
            
            # Ensure the path is relative to the root directory
            if not video_path.startswith('/'):
                if video_path.startswith('outputs/'):
                    video_path = video_path
                else:
                    video_path = f"outputs/{os.path.basename(video_path)}"
            
            return GenerationResponse(
                video_path=video_path,
                message="Video generated successfully!"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/video/{video_id}")
async def get_video(video_id: str):
    video_path = f"outputs/{video_id}.mp4"
    
    # Ensure outputs directory is relative to script path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    full_path = os.path.join(parent_dir, video_path)
    
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail=f"Video not found at {full_path}")
    return FileResponse(full_path)

if __name__ == "__main__":
    import uvicorn
    # Create outputs directory if it doesn't exist
    # Ensure it's created in the parent directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    outputs_dir = os.path.join(parent_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000) 