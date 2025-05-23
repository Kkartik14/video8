#!/usr/bin/env python3
"""
Test script to demonstrate the improved animation quality.
This script generates a test animation using both Claude and Groq to compare results.
"""

import os
import sys
import time
import argparse
from pathlib import Path

# Add the backend directory to the path
script_dir = Path(__file__).parent.absolute()
backend_dir = script_dir / "backend"
sys.path.append(str(backend_dir))

# Import the necessary modules
try:
    from llm_handler import LLMHandler
    from groq_handler import GroqHandler
    from scene_generator import SceneGenerator
    from prompt_optimizer import PromptOptimizer
except ImportError:
    print("Error: Could not import required modules from backend directory.")
    print("Make sure you're running this script from the project root directory.")
    sys.exit(1)

# Set up argument parser
parser = argparse.ArgumentParser(description='Test animation quality improvements')
parser.add_argument('--model', type=str, choices=['claude', 'groq', 'both'], default='claude',
                    help='Which model to use for generating the animation')
parser.add_argument('--prompt', type=str, 
                    default="Explain the Pythagorean theorem with a step-by-step visual proof showing how the squares on each side relate to each other.",
                    help='The prompt to use for generating the animation')
parser.add_argument('--optimize', action='store_true',
                    help='Whether to use the prompt optimizer')
parser.add_argument('--no-optimize', action='store_false', dest='optimize',
                    help='Disable the prompt optimizer')
parser.add_argument('--optimize-only', action='store_true',
                    help='Only run the prompt optimization step without generating the animation')
parser.set_defaults(optimize=True)
args = parser.parse_args()

def generate_test_animation(model_name, prompt, optimize=True):
    """Generate a test animation using the specified model."""
    print(f"\n{'='*80}")
    print(f"Generating animation using {model_name.upper()} with prompt:")
    print(f"'{prompt}'")
    print(f"{'='*80}\n")
    
    # Create output directories if they don't exist
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("outputs/scripts", exist_ok=True)
    os.makedirs("outputs/narrations", exist_ok=True)
    os.makedirs("outputs/prompts", exist_ok=True)
    
    # Optimize the prompt if requested
    enhanced_prompt = prompt
    if optimize:
        try:
            print("Optimizing prompt...")
            start_time = time.time()
            prompt_optimizer = PromptOptimizer()
            enhanced_prompt = prompt_optimizer.enhance_prompt(prompt)
            optimize_time = time.time() - start_time
            print(f"Prompt optimized in {optimize_time:.2f} seconds")
            print(f"Enhanced prompt: {enhanced_prompt[:200]}...")
            
            # Save enhanced prompt
            prompt_path = os.path.join("outputs", "prompts", f"test_{model_name}.txt")
            with open(prompt_path, "w") as f:
                f.write(f"Original prompt: {prompt}\n\nEnhanced prompt: {enhanced_prompt}")
            print(f"Enhanced prompt saved to {prompt_path}")
        except Exception as e:
            print(f"Warning: Could not optimize prompt: {str(e)}")
            print("Continuing with original prompt...")
            enhanced_prompt = prompt
    
    # Initialize the appropriate handler
    if model_name == "claude":
        handler = LLMHandler()
    else:  # groq
        handler = GroqHandler()
    
    # Generate narration script
    print("Generating narration script...")
    start_time = time.time()
    narration_script = handler.generate_narration_script(enhanced_prompt)
    script_time = time.time() - start_time
    print(f"Narration script generated in {script_time:.2f} seconds")
    
    # Save narration script
    narration_path = os.path.join("outputs", "narrations", f"test_{model_name}.txt")
    with open(narration_path, "w") as f:
        f.write(narration_script)
    print(f"Narration script saved to {narration_path}")
    
    # Generate Manim code
    print("Generating Manim code...")
    start_time = time.time()
    manim_code = handler.generate_manim_code(enhanced_prompt, narration_script)
    code_time = time.time() - start_time
    print(f"Manim code generated in {code_time:.2f} seconds")
    
    # Save Manim code
    script_path = os.path.join("outputs", "scripts", f"test_{model_name}.py")
    with open(script_path, "w") as f:
        f.write(manim_code)
    print(f"Manim code saved to {script_path}")
    
    # Generate the video
    print("Rendering the animation...")
    scene_generator = SceneGenerator()
    try:
        start_time = time.time()
        video_id = scene_generator.create_video(
            manim_code,
            output_dir="outputs",
            generation_id=f"test_{model_name}"
        )
        render_time = time.time() - start_time
        print(f"Animation rendered in {render_time:.2f} seconds")
        print(f"Animation saved with ID: {video_id}")
        
        # Print possible video paths
        base_dir = os.path.abspath(os.path.dirname(__file__))
        possible_locations = [
            os.path.join(base_dir, "outputs", f"{video_id}.mp4"),
            os.path.join(base_dir, "outputs", "videos", f"scene_{video_id}", "720p30", f"{video_id}.mp4"),
            os.path.join(base_dir, "outputs", "videos", f"scene_{video_id}", "1080p60", f"{video_id}.mp4"),
        ]
        
        print("\nPossible video locations:")
        for location in possible_locations:
            if os.path.exists(location):
                print(f"✅ {location} (EXISTS)")
            else:
                print(f"❌ {location} (NOT FOUND)")
        
        return True
    except Exception as e:
        print(f"Error rendering animation: {str(e)}")
        return False

def optimize_prompt_only(prompt):
    """Just run the prompt optimization step."""
    print(f"\n{'='*80}")
    print(f"Optimizing prompt:")
    print(f"'{prompt}'")
    print(f"{'='*80}\n")
    
    try:
        # Create output directory
        os.makedirs("outputs/prompts", exist_ok=True)
        
        # Initialize optimizer
        prompt_optimizer = PromptOptimizer()
        
        # Time the optimization
        start_time = time.time()
        enhanced_prompt = prompt_optimizer.enhance_prompt(prompt)
        optimize_time = time.time() - start_time
        
        # Display results
        print(f"Prompt optimized in {optimize_time:.2f} seconds")
        print("\nORIGINAL PROMPT:")
        print(f"{prompt}\n")
        print("\nENHANCED PROMPT:")
        print(f"{enhanced_prompt}\n")
        
        # Save the result
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        prompt_path = os.path.join("outputs", "prompts", f"optimized_{timestamp}.txt")
        with open(prompt_path, "w") as f:
            f.write(f"Original prompt: {prompt}\n\nEnhanced prompt: {enhanced_prompt}")
        print(f"\nOptimized prompt saved to {prompt_path}")
        
        return True
    except Exception as e:
        print(f"Error optimizing prompt: {str(e)}")
        return False

def main():
    # Print the current Python version
    print(f"Python version: {sys.version}")
    
    # Check for required environment variables
    if not args.optimize_only:
        if args.model in ['claude', 'both'] and not os.getenv("ANTHROPIC_API_KEY"):
            print("Error: ANTHROPIC_API_KEY environment variable is not set.")
            sys.exit(1)
        
        if args.model in ['groq', 'both'] and not os.getenv("GROQ_API_KEY"):
            print("Error: GROQ_API_KEY environment variable is not set.")
            sys.exit(1)
    
    # If optimize-only flag is set, just run prompt optimization
    if args.optimize_only:
        result = optimize_prompt_only(args.prompt)
        if result:
            print("\nPrompt optimization completed successfully!")
        else:
            print("\nError during prompt optimization.")
        return
    
    # Generate animations based on the specified model
    if args.model == 'both':
        print("Generating animations using both Claude and Groq...")
        claude_result = generate_test_animation('claude', args.prompt, args.optimize)
        groq_result = generate_test_animation('groq', args.prompt, args.optimize)
        
        if claude_result and groq_result:
            print("\nBoth animations generated successfully!")
        else:
            print("\nThere were errors generating one or both animations.")
    else:
        result = generate_test_animation(args.model, args.prompt, args.optimize)
        if result:
            print("\nAnimation generated successfully!")
        else:
            print("\nThere was an error generating the animation.")

if __name__ == "__main__":
    main()

# Usage instructions
"""
Usage examples:

1. Generate a test animation with the default prompt using Claude:
   ./test_animation_quality.py

2. Generate a test animation with a custom prompt using Groq:
   ./test_animation_quality.py --model groq --prompt "Explain how a neural network learns"

3. Generate animations with both Claude and Groq:
   ./test_animation_quality.py --model both

4. Generate animation without prompt optimization:
   ./test_animation_quality.py --no-optimize

5. Only run prompt optimization without generating animation:
   ./test_animation_quality.py --optimize-only --prompt "Explain quantum computing"
""" 