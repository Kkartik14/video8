import os
import requests
import json
import re
from typing import Dict, Any

class LLMHandler:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        # Load animation patterns if available
        patterns_file = os.path.join(os.path.dirname(__file__), "animation_patterns.txt")
        animation_patterns = ""
        if os.path.exists(patterns_file):
            with open(patterns_file, 'r') as f:
                animation_patterns = f.read()
        
        # System prompt for generating Manim code
        self.system_prompt = """You are an expert at generating Manim animation code. 
Given a natural language prompt, you will generate Python code using Manim to create 
beautiful and educational 2D animations. Follow these instructions EXACTLY:
1. ONLY return Python code with no explanations or additional text before or after
2. Do not include markdown code blocks or any other formatting
3. Do not include any statements like 'Here's the code', just start directly with the imports
4. Do not include triple backticks (```) in your response anywhere
5. Ensure the code is fully functional and can run on its own
6. IMPORTANT: Do NOT use Tex or MathTex objects as they require LaTeX. Use Text instead.
7. Always include 'import math' if you need mathematical functions
8. Use Create() instead of ShowCreation() as it's deprecated in newer versions
9. CRITICAL: Always remove or fade out text and objects before adding new ones in the same area
10. CRITICAL: Be mindful of spatial composition - place elements with proper spacing and avoid overlap
11. CRITICAL: When explaining step-by-step concepts, use FadeOut or Transform to remove old elements before adding new ones
12. Always plan the visual space in advance by defining clear regions for different elements
13. When animating mathematical concepts, use a clean, organized layout with consistent positioning"""
        
        # Add animation patterns if available
        if animation_patterns:
            self.system_prompt += f"\n\nHere are best practices for Manim animations that you MUST follow:\n\n{animation_patterns}"
        
        # System prompt for narration script generation
        self.script_system_prompt = """You are an expert educational content creator specializing in clear, engaging narration scripts for educational videos. Your task is to create a detailed narration script that explains complex concepts in an accessible, engaging manner.

USE CASE:
This script will be used as the narration for an educational animation. The script needs to align perfectly with a visual animation that will be generated to accompany it. Your script will guide the development of the animation and serve as the voiceover that explains the concepts as they appear visually.

REQUIREMENTS:
1. Write a COMPLETE, PROFESSIONAL narration script
2. Structure the script in clear sections (Introduction, Main Concepts, Conclusion)
3. Include timestamps or markers for key transition points
4. Write in a conversational, engaging tone appropriate for educational content
5. Explain complex concepts clearly with appropriate analogies
6. Include pauses for viewers to process visual information
7. Keep sentences concise for easier narration
8. Use a logical progression that builds understanding step-by-step
9. Include questions or points of reflection to engage viewers
10. End with a clear summary of key takeaways
11. IMPORTANT: Be COMPREHENSIVE and THOROUGH in your explanations - include all necessary details
12. Don't rush or abbreviate explanations - take the time needed to properly explain the concept

Focus on clarity, engagement, educational value, and COMPLETENESS. Aim to make the explanation as thorough as possible while maintaining audience engagement."""
        
    def generate_narration_script(self, prompt: str) -> str:
        """Generate a narration script for the animation based on the prompt"""
        # Enhance the user prompt for script generation
        enhanced_prompt = f"""Create a detailed narration script for an educational video about:
{prompt}

The script should:
1. Have a clear introduction that engages the viewer and explains what they'll learn
2. Break down the concept into clear, logical sections
3. Include timestamps or markers for transitions between key points
4. Use clear, accessible language to explain complex ideas
5. Have a compelling conclusion that summarizes key takeaways
6. Be COMPREHENSIVE and THOROUGH - don't limit the length or rush explanations
7. Cover all aspects of the topic in sufficient detail for full understanding

Format the script with timestamps like this:
[00:00] INTRODUCTION
(Introduction content here)

[00:30] FIRST CONCEPT
(First concept content here)

[01:15] SECOND CONCEPT
(Second concept content here)

[02:00] ADDITIONAL CONCEPTS (as many as needed)
(Additional content here)

[XX:XX] CONCLUSION
(Conclusion content here)
"""

        # Using direct API call instead of the library
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-2.0",
            "prompt": f"\n\nHuman: {self.script_system_prompt}\n\n{enhanced_prompt}\n\nAssistant:",
            "max_tokens_to_sample": 4000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/complete",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        script = result.get("completion", "")
        print(f"Raw narration script from Claude:\n{script[:100]}...")
        
        if not script or len(script) < 50:
            raise Exception("Generated narration script is too short or empty")
            
        return script
            
    def generate_manim_code(self, prompt: str, narration_script: str = None) -> str:
        # For all prompts, try to generate with Claude
        # Enhance the user prompt with specific requirements
        enhanced_prompt = f"""Create a Manim animation for the following prompt:
{prompt}

"""
        
        # Add narration script if provided
        if narration_script:
            enhanced_prompt += f"Here is the narration script that the animation should follow precisely:\n{narration_script}\n\n"
        
        enhanced_prompt += """Requirements:
1. Use the Scene class named 'CustomAnimation'
2. Include all necessary imports (always start with 'from manim import *', and include 'import math' if needed)
3. Use appropriate animations and transitions
4. Add text labels and explanations where needed
5. Ensure smooth animations with appropriate timing
6. Use color to enhance understanding
7. IMPORTANT: Create a COMPREHENSIVE and IN-DEPTH animation that fully explains the concept - don't rush
8. IMPORTANT: Do NOT use Tex, MathTex, or any LaTeX-dependent objects as they require LaTeX. Use Text instead.
9. IMPORTANT: Use Create() instead of ShowCreation() as the latter is deprecated
10. IMPORTANT: Do NOT include any self.wait() or other self references outside of the construct method
11. IMPORTANT: All code that references 'self' MUST be properly indented inside the construct method
12. Include a final self.wait(2) at the end of the construct method to allow viewing the final state
13. EXTREMELY IMPORTANT: Do NOT include any triple backticks (```) or markdown formatting in your code
14. EXTREMELY IMPORTANT: Only return pure Python code that can be executed directly
15. CRITICALLY IMPORTANT: Ensure all text elements stay within visible screen boundaries
16. ESSENTIAL: Keep text positioning within a safe distance from screen edges:
    - Use max values of ±6 for x or y coordinates to avoid text going off-screen
    - Implement boundary checking with helper functions if needed
    - When text has dynamic positioning, verify it stays visible

"""

        # Add narration-specific requirements if a script is provided
        if narration_script:
            enhanced_prompt += """17. EXTREMELY IMPORTANT: Ensure the animations align with the timestamps and sections in the narration script provided
18. Use appropriate self.wait() durations to match narration timing - typically:
   - 1-2 seconds for short sentences
   - 2-3 seconds for complex concepts
   - 0.5-1 seconds for transitions
19. Time visual elements to appear exactly when they would be mentioned in the narration
20. EXTREMELY IMPORTANT: Always clean up the scene by using FadeOut() for objects no longer needed
21. EXTREMELY IMPORTANT: Avoid text overlay problems by using text replacement techniques:
    - Use Transform(old_text, new_text) when updating related concepts
    - Use FadeOut(old_text) followed by FadeIn(new_text) when changing topics
    - Group related text elements to manage them together
22. Define clear spatial zones on the screen (e.g., title area, main demonstration area, explanation area)
23. Use shifting techniques (text.shift(UP/DOWN/LEFT/RIGHT)) to ensure elements don't overlap
24. When showing progressive steps, use consistent positioning and transitions to show the evolution
25. IMPORTANT: Ensure all text stays within visible screen boundaries by:
    - Keeping coordinate values between -6 and 6 for both x and y
    - Scaling text if needed to fit within boundaries
    - Using helper functions to ensure positions stay within boundaries
"""

        enhanced_prompt += """
If you can't create a specific animation for this prompt, do NOT use a generic template. Instead, create a targeted animation that addresses the prompt as specifically as possible.

The code MUST start exactly like this:
from manim import *
import math  # Include this if you need mathematical functions
import numpy as np  # Include this if you need numpy

class CustomAnimation(Scene):
    def construct(self):
        # Define screen regions for better organization
        title_region = UP * 3.5
        main_region = ORIGIN
        explanation_region = DOWN * 3 + LEFT * 3
        
        # Define safe boundaries for text placement
        boundary_threshold = 6  # Max distance from origin to stay in bounds
        
        def ensure_within_boundaries(position, threshold=boundary_threshold):
            \"\"\"Ensure a position is within the safe boundaries of the screen.\"\"\"
            if isinstance(position, np.ndarray):
                # Normalize the position if it's too far from origin
                magnitude = np.linalg.norm(position)
                if magnitude > threshold:
                    return position * (threshold / magnitude)
            return position
"""
        # Add appropriate comment based on whether there's a narration script
        if narration_script:
            enhanced_prompt += "        # Your code here aligned with narration timestamps"
        else:
            enhanced_prompt += "        # Your code here"

        # Using direct API call instead of the library
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-2.0",
            "prompt": f"\n\nHuman: {self.system_prompt}\n\n{enhanced_prompt}\n\nAssistant:",
            "max_tokens_to_sample": 8000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/complete",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        code = result.get("completion", "")
        print(f"Raw response from Claude:\n{code[:100]}...")
        
        if not code or len(code) < 50:
            raise Exception("Generated Manim code is too short or empty")
        
        # Validate and fix the generated code
        code = self.validate_and_fix_code(code)
        
        return code
    
    def validate_and_fix_code(self, code: str) -> str:
        """Validate and fix common issues in the generated Manim code."""
        # Remove any explanatory text at the beginning
        if not code.strip().startswith('from manim import'):
            start_idx = code.find('from manim import')
            if start_idx != -1:
                code = code[start_idx:]
            else:
                raise Exception("Could not find Manim import statement in generated code")
                
        # Replace deprecated methods
        code = code.replace("ShowCreation(", "Create(")
            
        # Fix missing imports
        if "math." in code and "import math" not in code:
            code = "import math\n" + code
            
        if "np." in code and "import numpy as np" not in code:
            code = "import numpy as np\n" + code
            
        # Check for LaTeX (which we don't want)
        if "MathTex(" in code or "Tex(" in code:
            raise Exception("Generated code contains LaTeX objects which are not supported")
        
        # Check if all code is inside the class and method
        fixed_lines = []
        in_class = False
        in_method = False
        class_indent = ""
        method_indent = ""
        
        lines = code.split('\n')
        for i, line in enumerate(lines):
            # Track if we're in the CustomAnimation class
            if line.strip().startswith("class CustomAnimation"):
                in_class = True
                class_indent = line[:line.find("class")]
                fixed_lines.append(line)
                continue
                
            # Track if we're in the construct method
            if in_class and "def construct(self" in line:
                in_method = True
                method_indent = line[:line.find("def")]
                fixed_lines.append(line)
                continue
                
            # Remove any self references outside of the method
            if "self." in line and not in_method:
                # Skip this line
                continue
                
            # Add line normally
            fixed_lines.append(line)
        
        # Ensure the code ends with a wait
        # Find the last line inside the construct method
        for i in range(len(fixed_lines) - 1, 0, -1):
            line = fixed_lines[i]
            if line.strip() and in_method and line.startswith(method_indent + " "):
                # Check if the last line is already a wait
                if not "self.wait" in line:
                    # Add a wait as the last line
                    fixed_lines.insert(i + 1, method_indent + "    self.wait(2)  # Final wait")
                break
                
        fixed_code = "\n".join(fixed_lines)
        
        # Final validation
        if not self.validate_code(fixed_code):
            raise Exception("Generated code is missing required elements")
            
        return fixed_code

    def validate_code(self, code: str) -> bool:
        """
        Basic validation of generated Manim code.
        Returns True if the code appears valid, False otherwise.
        """
        required_elements = [
            "from manim import",
            "class CustomAnimation(Scene):",
            "def construct(self):"
        ]
        
        is_valid = all(element in code for element in required_elements)
        return is_valid 