import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import tempfile
import uuid
from typing import Literal, Optional, Dict, Any

# Add the current directory to sys.path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_handler import LLMHandler
from groq_handler import GroqHandler
from scene_generator import SceneGenerator
from prompt_optimizer import PromptOptimizer

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
    optimize_prompt: Optional[bool] = True

class GenerationResponse(BaseModel):
    video_path: str
    script_path: str
    narration_script: str
    enhanced_prompt: Optional[str] = None
    message: str

@app.post("/generate", response_model=GenerationResponse)
async def generate_video(request: PromptRequest):
    # Create unique ID for this generation
    generation_id = str(uuid.uuid4())
    
    try:
        # Initialize prompt optimizer if needed
        enhanced_prompt = request.prompt
        if request.optimize_prompt:
            try:
                prompt_optimizer = PromptOptimizer()
                enhanced_prompt = prompt_optimizer.enhance_prompt(request.prompt)
                print(f"Enhanced prompt: {enhanced_prompt[:200]}...")
            except Exception as e:
                print(f"Warning: Could not optimize prompt: {str(e)}")
                print("Continuing with original prompt...")
                enhanced_prompt = request.prompt
        else:
            enhanced_prompt = request.prompt
        
        # Initialize handlers based on selected model
        if request.model == "claude":
            llm_handler = LLMHandler()
            # Generate narration script first
            narration_script = llm_handler.generate_narration_script(enhanced_prompt)
            # Then use narration script to generate more aligned Manim code
            manim_code = llm_handler.generate_manim_code(enhanced_prompt, narration_script)
        else:
            llm_handler = GroqHandler()
            narration_script = llm_handler.generate_narration_script(enhanced_prompt)
            manim_code = llm_handler.generate_manim_code(enhanced_prompt, narration_script)
        
        # Initialize scene generator
        scene_generator = SceneGenerator()
        
        # Save the script to a file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_dir)
        scripts_dir = os.path.join(parent_dir, "outputs", "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        
        script_path = os.path.join(scripts_dir, f"{generation_id}.py")
        with open(script_path, "w") as f:
            f.write(manim_code)
        
        # Save the narration script to a file
        narration_dir = os.path.join(parent_dir, "outputs", "narrations")
        os.makedirs(narration_dir, exist_ok=True)
        narration_path = os.path.join(narration_dir, f"{generation_id}.txt")
        with open(narration_path, "w") as f:
            f.write(narration_script)
        
        # Also save the enhanced prompt if it was used
        if request.optimize_prompt:
            prompts_dir = os.path.join(parent_dir, "outputs", "prompts")
            os.makedirs(prompts_dir, exist_ok=True)
            prompt_path = os.path.join(prompts_dir, f"{generation_id}.txt")
            with open(prompt_path, "w") as f:
                f.write(f"Original prompt: {request.prompt}\n\nEnhanced prompt: {enhanced_prompt}")
        
        # Create temporary directory for video output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate and render the video
            video_id = scene_generator.create_video(
                manim_code,
                output_dir=temp_dir,
                generation_id=generation_id
            )
            
            # Return the video_id and script_id which will be used to construct the URLs
            return GenerationResponse(
                video_path=f"/outputs/{video_id}",
                script_path=f"/scripts/{generation_id}",
                narration_script=narration_script,
                enhanced_prompt=enhanced_prompt if request.optimize_prompt else None,
                message="Video and script generated successfully!"
            )
            
    except Exception as e:
        # Delete any partially created files
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_dir)
        
        # Try to delete script file if it exists
        script_path = os.path.join(parent_dir, "outputs", "scripts", f"{generation_id}.py")
        if os.path.exists(script_path):
            os.remove(script_path)
            
        # Try to delete narration file if it exists
        narration_path = os.path.join(parent_dir, "outputs", "narrations", f"{generation_id}.txt")
        if os.path.exists(narration_path):
            os.remove(narration_path)
            
        # Raise a detailed HTTP exception
        error_message = f"Error during video generation: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/outputs/{video_id}")
async def get_video(video_id: str):
    # Get the base directory and parent directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    
    # Look for the video in different possible locations where Manim might have saved it
    possible_locations = [
        # Check direct outputs folder first
        os.path.join(parent_dir, "outputs", f"{video_id}.mp4"),
        # Check in video folders with quality settings
        os.path.join(parent_dir, "outputs", "videos", f"scene_{video_id}", "720p30", f"{video_id}.mp4"),
        os.path.join(parent_dir, "outputs", "videos", f"scene_{video_id}", "1080p60", f"{video_id}.mp4"),
    ]
    
    # Try each location
    for location in possible_locations:
        if os.path.exists(location):
            return FileResponse(location)
    
    # If we got here, we couldn't find the video
    raise HTTPException(status_code=404, detail=f"Video not found. Tried locations: {possible_locations}")

@app.get("/scripts/{script_id}", response_class=PlainTextResponse)
async def get_script(script_id: str):
    # Get the base directory and parent directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    
    # Get the script path
    script_path = os.path.join(parent_dir, "outputs", "scripts", f"{script_id}.py")
    
    if os.path.exists(script_path):
        with open(script_path, "r") as f:
            script_content = f.read()
        return script_content
    
    # If we got here, we couldn't find the script
    raise HTTPException(status_code=404, detail=f"Script not found at {script_path}")

@app.get("/narrations/{script_id}", response_class=PlainTextResponse)
async def get_narration(script_id: str):
    # Get the base directory and parent directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    
    # Get the narration script path
    narration_path = os.path.join(parent_dir, "outputs", "narrations", f"{script_id}.txt")
    
    if os.path.exists(narration_path):
        with open(narration_path, "r") as f:
            narration_content = f.read()
        return narration_content
    
    # If we got here, we couldn't find the narration script
    raise HTTPException(status_code=404, detail=f"Narration script not found at {narration_path}")

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Service is running"}

# Keep the old route for compatibility
@app.get("/video/{video_id}")
async def get_video_old(video_id: str):
    return await get_video(video_id)

if __name__ == "__main__":
    import uvicorn
    # Create outputs directory if it doesn't exist
    # Ensure it's created in the parent directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    outputs_dir = os.path.join(parent_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Create scripts directory within outputs
    scripts_dir = os.path.join(outputs_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 