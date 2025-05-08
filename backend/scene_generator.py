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
        
        # Fix 'self' references outside of class methods (common LLM error)
        # This pattern looks for 'self.' at the module level (not indented inside a method)
        lines = fixed_code.split('\n')
        in_class = False
        in_method = False
        fixed_lines = []
        
        for line in lines:
            # Track if we're inside a class definition
            if re.match(r'^class\s+\w+.*:', line):
                in_class = True
                in_method = False
            # Track if we're inside a method definition
            elif in_class and re.match(r'^\s+def\s+\w+\s*\(self.*\):', line):
                in_method = True
            # If line is not indented, we're back at module level
            elif line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                in_class = False
                in_method = False
            
            # Fix self references at module level
            if not in_method and 'self.' in line:
                # Remove the line or comment it out
                line = '# ' + line + ' # Removed invalid self reference'
            
            fixed_lines.append(line)
        
        fixed_code = '\n'.join(fixed_lines)
        
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
            The generation_id of the video, which can be used to access it via the API
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
            
            # Run Manim to generate the video
            command = [
                "manim",
                "-qm",  # medium quality
                "--format=mp4",
                "--output_file", generation_id,
                "--media_dir", "outputs",
                temp_file_path,
                "CustomAnimation"
            ]
            
            # Print the command for debugging
            print(f"Running command: {' '.join(command)}")
            
            # First attempt to run Manim
            try:
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
                    # Check for specific errors and fix them
                    if "NameError: name 'self' is not defined" in stderr:
                        print("Fixing 'self' reference errors in the code...")
                        fixed_lines = []
                        for line in fixed_code.split('\n'):
                            if 'self.' in line and not re.match(r'^\s+', line):
                                # Skip lines with self references at module level completely
                                continue
                            fixed_lines.append(line)
                        
                        fixed_code = '\n'.join(fixed_lines)
                        
                    elif "IndentationError" in stderr:
                        print("Fixing indentation errors in the code...")
                        # Try to extract just the Python code part
                        code_start = fixed_code.find('from manim import')
                        if code_start != -1:
                            fixed_code = fixed_code[code_start:]
                        
                        # Normalize indentation
                        lines = fixed_code.split('\n')
                        fixed_lines = []
                        class_found = False
                        method_found = False
                        
                        for line in lines:
                            # Extract clean line (no whitespace)
                            clean_line = line.strip()
                            
                            # Skip blank lines
                            if not clean_line:
                                fixed_lines.append('')
                                continue
                                
                            # Handle imports and top-level statements
                            if clean_line.startswith('from ') or clean_line.startswith('import '):
                                fixed_lines.append(clean_line)
                                continue
                                
                            # Handle class definition
                            if clean_line.startswith('class CustomAnimation'):
                                class_found = True
                                method_found = False
                                fixed_lines.append(clean_line)
                                continue
                                
                            # Handle method definition
                            if class_found and clean_line.startswith('def construct'):
                                method_found = True
                                fixed_lines.append('    ' + clean_line)  # Indent method
                                continue
                                
                            # Handle method body
                            if method_found:
                                fixed_lines.append('        ' + clean_line)  # Double indent
                            elif class_found:
                                fixed_lines.append('    ' + clean_line)  # Single indent
                            else:
                                fixed_lines.append(clean_line)  # No indent
                                
                        fixed_code = '\n'.join(fixed_lines)
                        
                    # Write the fixed code
                    with open(temp_file_path, "w") as f:
                        f.write(fixed_code)
                    
                    # Try running Manim again
                    print("Trying again with fixed code...")
                    process = subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    stdout, stderr = process.communicate()
                    
                    print(f"Second attempt Manim stdout: {stdout}")
                    if stderr:
                        print(f"Second attempt Manim stderr: {stderr}")
                    
                    if process.returncode != 0:
                        raise Exception(f"Manim rendering failed even after fixes: {stderr}")
                    
            except Exception as e:
                print(f"Error during Manim execution: {str(e)}")
                raise
            
            # Return just the generation_id, which will be used to construct the URL
            return generation_id
            
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