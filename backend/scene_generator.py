import os
import tempfile
import subprocess
from typing import Optional
import glob
import shutil
import re
import importlib.util

class SceneGenerator:
    def __init__(self):
        self.quality = "medium_quality"
        self.preview = False
        # Check if example animations are available
        self.has_examples = os.path.exists(os.path.join(os.path.dirname(__file__), "example_animations.py"))
        
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
        
        # Improve animation quality and fix text overlay issues
        fixed_code = self._improve_animation_quality(fixed_code)
        
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
            
            # If we have examples available, copy the example_animations.py to the output dir
            # so it can be referenced by the scene
            if self.has_examples:
                example_file = os.path.join(os.path.dirname(__file__), "example_animations.py")
                shutil.copy(example_file, output_dir)
            
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

    def _improve_animation_quality(self, code: str) -> str:
        """
        Detect and fix common issues with animation clarity, text overlays, and object management.
        """
        # Check if we have multiple text objects without removal
        lines = code.split('\n')
        text_creations = []
        text_removals = []
        text_names = set()
        section_comments = []
        
        # First pass - collect information
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Track section comments for better organization
            if stripped.startswith('#') and len(stripped) > 2:
                section_comments.append((i, stripped))
            
            # Track text object creations
            text_creation_match = re.search(r'(\w+)\s*=\s*Text\(', stripped)
            if text_creation_match:
                text_name = text_creation_match.group(1)
                text_names.add(text_name)
                text_creations.append((i, text_name))
            
            # Track text object removals (FadeOut, Transform, etc.)
            for name in text_names:
                if f"FadeOut({name})" in stripped or f"Transform({name}" in stripped:
                    text_removals.append((i, name))
        
        # Fix missing FadeOut for text objects
        fixed_lines = lines.copy()
        created_but_not_removed = []
        
        # Find text objects that were created but never removed
        for i, text_name in text_creations:
            # Check if this text was ever removed
            if not any(name == text_name for _, name in text_removals):
                created_but_not_removed.append((i, text_name))
        
        # Add FadeOut for text objects that weren't removed
        if created_but_not_removed:
            # Find the last wait call in the method to insert before it
            last_wait_index = -1
            for i, line in enumerate(reversed(lines)):
                if "self.wait" in line.strip():
                    last_wait_index = len(lines) - i - 1
                    break
            
            # If no wait call found, find the end of the construct method
            if last_wait_index == -1:
                for i, line in enumerate(lines):
                    if line.strip() == "def construct(self):":
                        # Find the end of the method by indentation
                        method_indent = len(line) - len(line.lstrip())
                        for j in range(i+1, len(lines)):
                            if lines[j].strip() and len(lines[j]) - len(lines[j].lstrip()) <= method_indent:
                                last_wait_index = j - 1
                                break
                        if last_wait_index == -1:  # If we couldn't find the end, use the last line
                            last_wait_index = len(lines) - 1
                        break
            
            # If we found a place to insert, add FadeOut for all objects
            if last_wait_index != -1:
                # Create a list of text objects to fade out
                text_objects = [name for _, name in created_but_not_removed]
                if text_objects:
                    # Add a comment explaining the fix
                    fixed_lines.insert(last_wait_index, "        # Cleaning up text objects to avoid cluttering")
                    
                    # For multiple objects, use a group
                    if len(text_objects) > 1:
                        fade_out_line = f"        self.play(FadeOut(VGroup({', '.join(text_objects)})))"
                    else:
                        fade_out_line = f"        self.play(FadeOut({text_objects[0]}))"
                    
                    fixed_lines.insert(last_wait_index + 1, fade_out_line)
        
        # Check for missing spatial organization and add comments to help
        if len(text_creations) > 3 and len(section_comments) < 2:
            # Find the start of the construct method
            for i, line in enumerate(fixed_lines):
                if line.strip() == "def construct(self):":
                    # Add a spatial organization tip
                    fixed_lines.insert(i + 1, "        # Define screen regions for better organization")
                    fixed_lines.insert(i + 2, "        title_region = UP * 3.5")
                    fixed_lines.insert(i + 3, "        main_region = ORIGIN")
                    fixed_lines.insert(i + 4, "        explanation_region = DOWN * 3 + LEFT * 3")
                    break
        
        # Check if we need to add text replacement example
        has_text_transform = any("Transform(" in line for line in fixed_lines)
        if not has_text_transform and len(text_creations) > 2:
            # Add a comment with an example of text transformation technique
            for i, line in enumerate(fixed_lines):
                if "Text(" in line:
                    indent = len(line) - len(line.lstrip())
                    # Add the comment after this text creation
                    example = " " * indent + "# Example: To update this text use self.play(Transform(text1, text2))"
                    fixed_lines.insert(i + 1, example)
                    break
        
        # If we have examples available and there are still issues, add import for our example patterns
        if self.has_examples and (len(created_but_not_removed) > 2 or (len(text_creations) > 3 and not has_text_transform)):
            # Add a comment with references to example patterns
            for i, line in enumerate(fixed_lines):
                if line.strip().startswith('from manim import'):
                    # Find the best example class to reference based on the issues
                    if len(created_but_not_removed) > 2:
                        example_class = "GoodTextManagement"
                        comment = "# Refer to the GoodTextManagement example for proper text cleanup techniques"
                    else:
                        example_class = "ProgressiveSteps"
                        comment = "# Refer to the ProgressiveSteps example for how to show sequential information"
                    
                    # Add comment and optional import
                    fixed_lines.insert(i + 1, comment)
                    break
                    
        return '\n'.join(fixed_lines) 