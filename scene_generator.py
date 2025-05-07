import os
import tempfile
import subprocess
from typing import Optional
import glob
import shutil
import re

class SceneGenerator:
    def __init__(self):
        self.quality = "medium_quality"
        self.preview = False
        
    def _fix_manim_code(self, code: str) -> str:
        """
        Fix common issues in generated Manim code to make it compatible with the installed version.
        """
        # Replace ShowCreation (old name) with Create (new name)
        fixed_code = re.sub(r'ShowCreation\(', 'Create(', code)
        
        # Add other replacements as needed
        
        return fixed_code
        
    def create_video(
        self,
        manim_code: str,
        output_dir: str,
        generation_id: str
    ) -> str:
        """
        Creates a video from Manim code.
        
        Args:
            manim_code: The generated Manim code
            output_dir: Directory to store temporary files
            generation_id: Unique identifier for this generation
            
        Returns:
            Path to the generated video file
        """
        try:
            # Make sure outputs directory exists
            os.makedirs("outputs", exist_ok=True)
            
            # Fix any known issues in the code
            fixed_code = self._fix_manim_code(manim_code)
            
            # Create a temporary Python file with the Manim code
            temp_file_path = os.path.join(output_dir, f"scene_{generation_id}.py")
            with open(temp_file_path, "w") as f:
                f.write(fixed_code)
            
            # Print generated code for debugging
            print(f"\nGenerated Manim code for scene_{generation_id}.py:")
            print("--------------------------------------------------")
            print(fixed_code[:500] + "..." if len(fixed_code) > 500 else fixed_code)
            print("--------------------------------------------------\n")
            
            # Prepare the output path
            final_output_path = os.path.join("outputs", f"{generation_id}.mp4")
            
            # Build the Manim command to output directly to our target directory
            command = [
                "manim",
                "-qm",  # medium quality
                "--format=mp4",
                "--output_file", f"{generation_id}",
                "--media_dir", "outputs",
                temp_file_path,
                "CustomAnimation"
            ]
            
            # Print the command for debugging
            print(f"Running command: {' '.join(command)}")
            
            # Run Manim
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            
            print(f"Manim stdout: {stdout}")
            if stderr:
                print(f"Manim stderr: {stderr}")
            
            if process.returncode != 0:
                raise Exception(f"Manim rendering failed: {stderr}")
            
            # Find the generated video file in the outputs directory
            output_video_path = os.path.join("outputs", "videos", "scene_{generation_id}", "1080p60", f"{generation_id}.mp4")
            
            # If the file exists at the expected location, move it
            if os.path.exists(output_video_path):
                shutil.move(output_video_path, final_output_path)
                return final_output_path
            
            # If not found at expected location, check other locations
            potential_paths = [
                os.path.join("outputs", "videos", "*", "1080p60", f"{generation_id}.mp4"),
                os.path.join("outputs", "videos", "*", "*", f"{generation_id}.mp4"),
                os.path.join("outputs", "**", f"{generation_id}.mp4")
            ]
            
            for pattern in potential_paths:
                matches = glob.glob(pattern, recursive=True)
                if matches:
                    # Found a match, move it to our final destination
                    if matches[0] != final_output_path:  # Only move if it's not already there
                        shutil.copy(matches[0], final_output_path)
                    return final_output_path
            
            # If we're here, we didn't find a file
            # Attempt a direct render to the final path as a last resort
            direct_output_command = [
                "manim",
                "-qm",
                "-o", f"{generation_id}.mp4",
                "--media_dir", "outputs",
                temp_file_path,
                "CustomAnimation"
            ]
            
            print(f"Attempting direct output with command: {' '.join(direct_output_command)}")
            
            process = subprocess.Popen(
                direct_output_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            
            if os.path.exists(final_output_path):
                return final_output_path
            
            # If we still can't find it, look one more time with a broader search
            matches = glob.glob(os.path.join("outputs", "**", "*.mp4"), recursive=True)
            if matches:
                newest_file = max(matches, key=os.path.getmtime)
                if newest_file != final_output_path:
                    shutil.copy(newest_file, final_output_path)
                return final_output_path
                
            raise Exception("Video file not found after rendering")
            
        except Exception as e:
            raise Exception(f"Error generating video: {str(e)}")
            
    def cleanup(self, file_path: str) -> None:
        """
        Cleans up temporary files after video generation.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not clean up file {file_path}: {str(e)}") 