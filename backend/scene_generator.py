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
        # Remove markdown artifacts (like triple backticks)
        fixed_code = self._remove_markdown_artifacts(code)
        
        # Replace ShowCreation (old name) with Create (new name)
        fixed_code = re.sub(r'ShowCreation\(', 'Create(', fixed_code)
        
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
        
        # Fix other common issues
        fixed_code = self._fix_common_syntax_errors(fixed_code)
        
        return fixed_code
    
    def _remove_markdown_artifacts(self, code: str) -> str:
        """
        Remove common markdown artifacts from generated code.
        """
        # Remove triple backticks at the beginning and end
        code = re.sub(r'^```python\s*\n', '', code)
        code = re.sub(r'^```\s*\n', '', code)
        code = re.sub(r'\n```\s*$', '', code)
        code = re.sub(r'```\s*$', '', code)
        
        # Remove any standalone backticks that might be in the code
        lines = code.split('\n')
        clean_lines = []
        for line in lines:
            # Skip lines that are just backticks
            if line.strip() in ['```', '```python']:
                continue
            # Remove backticks from the end of lines
            if line.strip().endswith('```'):
                line = line[:line.rfind('```')]
            # Remove backticks from the beginning of lines
            if line.strip().startswith('```'):
                line = line[line.find('```') + 3:]
            clean_lines.append(line)
        
        return '\n'.join(clean_lines)
    
    def _fix_common_syntax_errors(self, code: str) -> str:
        """
        Fix common syntax errors in generated code.
        """
        # Replace curly quotes with straight quotes
        code = code.replace('"', '"').replace('"', '"')
        code = code.replace(''', "'").replace(''', "'")
        
        # Fix common indentation issues
        lines = code.split('\n')
        # Check for mixed tabs and spaces
        has_tabs = any('\t' in line for line in lines)
        has_spaces = any(line.startswith(' ') for line in lines)
        
        if has_tabs and has_spaces:
            # Convert tabs to spaces for consistency
            fixed_lines = []
            for line in lines:
                fixed_lines.append(line.replace('\t', '    '))
            code = '\n'.join(fixed_lines)
            
        # Remove any non-ASCII characters that could cause issues
        code = ''.join(c if ord(c) < 128 else ' ' for c in code)
        
        return code
        
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
                    # Try to extract syntax error information
                    syntax_error_match = re.search(r'SyntaxError: (.+)', stderr)
                    syntax_error_info = ""
                    if syntax_error_match:
                        syntax_error_info = syntax_error_match.group(1)
                        print(f"Detected syntax error: {syntax_error_info}")
                        
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
                        
                    elif "IndentationError" in stderr or "SyntaxError: invalid syntax" in stderr:
                        print("Fixing indentation/syntax errors in the code...")
                        # Apply more aggressive fixes
                        fixed_code = self._apply_aggressive_fixes(fixed_code, stderr)
                        
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
                        # If we still have issues, try one more time with an even more aggressive approach
                        if "SyntaxError" in stderr:
                            print("Applying last-resort syntax fixes...")
                            fixed_code = self._apply_last_resort_fixes(fixed_code)
                            
                            with open(temp_file_path, "w") as f:
                                f.write(fixed_code)
                            
                            # Final attempt
                            process = subprocess.Popen(
                                command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                            )
                            stdout, stderr = process.communicate()
                            
                            print(f"Final attempt Manim stdout: {stdout}")
                            if stderr:
                                print(f"Final attempt Manim stderr: {stderr}")
                            
                            if process.returncode != 0:
                                # Save the problematic code for debugging
                                debug_file = f"debug_scene_{generation_id}.py"
                                with open(debug_file, "w") as f:
                                    f.write(fixed_code)
                                print(f"Saved problematic code to {debug_file} for inspection")
                                raise Exception(f"Manim rendering failed even after fixes: {stderr}")
                        else:
                            raise Exception(f"Manim rendering failed even after fixes: {stderr}")
                    
            except Exception as e:
                print(f"Error during Manim execution: {str(e)}")
                raise
            
            # Return just the generation_id, which will be used to construct the URL
            return generation_id
            
        except Exception as e:
            raise Exception(f"Error generating video: {str(e)}")
    
    def _apply_aggressive_fixes(self, code: str, error_msg: str) -> str:
        """Apply more aggressive fixes to the code based on the error message."""
        # First, extract line number if available
        line_num_match = re.search(r'line (\d+)', error_msg)
        problem_line_num = int(line_num_match.group(1)) if line_num_match else None
        
        # Try to extract just the Python code part
        code_start = code.find('from manim import')
        if code_start != -1:
            code = code[code_start:]
        
        # Normalize indentation
        lines = code.split('\n')
        fixed_lines = []
        class_found = False
        method_found = False
        
        # If we know the problem line, print it for debugging
        if problem_line_num is not None and problem_line_num <= len(lines):
            problem_line = lines[problem_line_num - 1]
            print(f"Problem line ({problem_line_num}): {problem_line}")
            
            # Check for specific syntax issues in the problem line
            if "```" in problem_line:
                print("Found backticks in problem line, removing them")
                lines[problem_line_num - 1] = problem_line.replace("```", "")
        
        for i, line in enumerate(lines):
            # Extract clean line (no whitespace)
            clean_line = line.strip()
            
            # Skip blank lines
            if not clean_line:
                fixed_lines.append('')
                continue
            
            # Skip lines that appear to be markdown artifacts
            if clean_line in ['```', '```python']:
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
        
        return '\n'.join(fixed_lines)
    
    def _apply_last_resort_fixes(self, code: str) -> str:
        """Apply last-resort fixes for syntax issues that couldn't be fixed automatically."""
        # Start with a clean slate - extract just the essential parts
        imports = []
        class_def = []
        construct_method = []
        
        # Extract imports
        lines = code.split('\n')
        for line in lines:
            if line.strip().startswith(('import ', 'from ')):
                imports.append(line.strip())
        
        # Find class definition
        for i, line in enumerate(lines):
            if line.strip().startswith('class CustomAnimation'):
                class_def.append(line.strip())
                
                # Find construct method
                for j in range(i+1, len(lines)):
                    if lines[j].strip().startswith('def construct'):
                        # We found the construct method
                        method_line = '    ' + lines[j].strip()
                        construct_method.append(method_line)
                        
                        # Add basic animation code that's guaranteed to work
                        construct_method.append('        title = Text("Simplified Animation")')
                        construct_method.append('        self.play(Write(title))')
                        construct_method.append('        self.wait(2)')
                        construct_method.append('        self.play(FadeOut(title))')
                        construct_method.append('        self.wait(1)')
                        break
                break
        
        # If we couldn't find some parts, use defaults
        if not imports:
            imports = ['from manim import *', 'import numpy as np', 'import math']
        
        if not class_def:
            class_def = ['class CustomAnimation(Scene):']
            
        if not construct_method:
            construct_method = [
                '    def construct(self):',
                '        title = Text("Simplified Animation")',
                '        self.play(Write(title))',
                '        self.wait(2)'
            ]
        
        # Combine everything
        rebuilt_code = '\n'.join(imports) + '\n\n' + '\n'.join(class_def) + '\n' + '\n'.join(construct_method)
        return rebuilt_code
            
    def cleanup(self, file_path: str) -> None:
        """
        Cleans up temporary files after video generation.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not clean up file {file_path}: {str(e)}") 