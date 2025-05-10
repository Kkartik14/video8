import os
import re
from typing import Dict, Any
import requests

class GroqHandler:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        # Load animation patterns if available
        patterns_file = os.path.join(os.path.dirname(__file__), "animation_patterns.txt")
        animation_patterns = ""
        if os.path.exists(patterns_file):
            with open(patterns_file, 'r') as f:
                animation_patterns = f.read()
        
        # System prompt for script generation
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
11. IMPORTANT: Be COMPREHENSIVE and THOROUGH in your explanations - don't limit yourself
12. Include ALL necessary details and don't rush your explanations

Focus on clarity, engagement, educational value, and COMPLETENESS. Make the explanation as thorough as possible while maintaining audience engagement."""

        # System prompt for generating Manim code based on script
        self.animation_system_prompt = """You are an expert mathematical animator specializing in Manim, the powerful Python library for creating precise and beautiful mathematical animations. Your task is to generate comprehensive, production-ready Manim code that transforms abstract concepts into visually stunning educational animations that align perfectly with a provided narration script.

USE CASE:
This system serves educators, students, and content creators who need to visualize complex concepts through animation but lack the technical expertise to code these visualizations from scratch. Your generated code will be directly executed to create videos that explain mathematical, scientific, or educational concepts visually. The quality, detail, and educational value of your code directly impacts learners' understanding of complex topics.

REQUIREMENTS (EXTREMELY IMPORTANT):
1. Generate COMPLETE, READY-TO-RUN Manim code that needs no modifications
2. Create animations that PRECISELY align with the provided narration script
3. Time the visual elements to match the narration flow (use self.wait() appropriately)
4. Provide EXTREMELY DETAILED animations with thorough comments explaining the mathematical/conceptual significance of each element
5. Include comprehensive docstrings at the beginning of the code explaining the animation's purpose
6. Structure animations to follow the script sections exactly
7. Use vibrant colors strategically to highlight important elements
8. Include detailed Text labels that match key phrases from the script
9. Add thoughtful transitions between animation segments that align with script transitions
10. Incorporate appropriate timing (self.wait()) to allow for narration of each section
11. Use precise positioning and scaling for all objects
12. Exploit Manim's powerful animation capabilities fully (transforms, fades, indicates, etc.)
13. Include mathematical formulas where relevant, using appropriate formatting
14. Design animations that would work well with voiceover narration
15. Add camera movements and zooms when they enhance understanding
16. Use background grids, axes, or reference frames where appropriate
17. EXTREMELY IMPORTANT: Do NOT include any triple backticks (```) or markdown formatting in your code
18. EXTREMELY IMPORTANT: Only return pure Python code that can be executed directly
19. CRITICAL: Always remove or fade out text and objects before adding new ones in the same area
20. CRITICAL: Never leave old objects on screen when they're no longer relevant
21. CRITICAL: Use spatial planning - define clear regions (title, main content, explanation)
22. CRITICAL: When explaining step-by-step, use transforms to show progression clearly
23. CRITICAL: Create a COMPREHENSIVE and IN-DEPTH animation - don't rush the explanation
24. CRITICAL: Take as much time as needed to fully explain each concept - do not limit the animation length

TECHNICAL REQUIREMENTS:
- Start with 'from manim import *'
- Always include 'import math' and 'import numpy as np'
- Use Text() instead of Tex()/MathTex() where appropriate for compatibility
- Use Create() instead of ShowCreation() (deprecated)
- Name the main Scene class 'CustomAnimation'
- Make the animation match the script length, however long it needs to be for a complete explanation
- Pay special attention to timing - allow time for narration of each concept
- Never include triple backticks (```) or other markdown syntax anywhere in the code
- Always use FadeOut() for any object before creating a new one in the same space
- Use Transform() to show evolution of concepts instead of creating new elements
- Always group related objects together (using VGroup) for easier management
- Use consistent positioning with UP, DOWN, LEFT, RIGHT constants

The key is to create an animation that perfectly complements the script, with visual elements appearing exactly when they would be mentioned in the narration and disappearing when no longer needed."""
        
        # Add animation patterns if available
        if animation_patterns:
            self.animation_system_prompt += f"\n\nHere are detailed best practices for Manim animations that you MUST follow:\n\n{animation_patterns}"
        
    def generate_narration_script(self, prompt: str) -> str:
        """Generate a narration script for the animation based on the prompt"""
        # Enhance the user prompt for script generation
        enhanced_prompt = f"""Create a detailed narration script for an educational video about:
{prompt}

The script should:
1. Have a clear introduction that engages the viewer and explains what they'll learn
2. Break down the concept into clear, logical sections
3. Include timestamps or markers for transitions between key points
4. Use conversational language that's easy to understand
5. Explain any complex terminology
6. Include 1-2 relatable examples or analogies
7. End with a clear summary of the key takeaways
8. Be COMPREHENSIVE and THOROUGH - don't limit the length or rush explanations
9. Cover all aspects of the topic in sufficient detail for complete understanding
10. Take as much time as needed to properly explain the concept - there is NO time limit

Format the script like this:
[00:00] INTRODUCTION
[Script text goes here...]

[00:30] MAIN CONCEPT 1
[Script text goes here...]

[01:15] MAIN CONCEPT 2
[Script text goes here...]

[02:00] ADDITIONAL CONCEPTS (as many sections as needed)
[Script text goes here...]

[XX:XX] CONCLUSION
[Script text goes here...]"""

        # Use direct HTTP request to Groq API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "messages": [
                {"role": "system", "content": self.script_system_prompt},
                {"role": "user", "content": enhanced_prompt}
            ],
            "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
            "max_tokens": 4000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Script generation API request failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        script = result["choices"][0]["message"]["content"].strip()
        
        # For debugging
        print("Generated narration script:")
        print(script[:200] + "..." if len(script) > 200 else script)
        
        if not script or len(script) < 50:
            raise Exception("Generated narration script is too short or empty")
            
        return script
    
    def generate_manim_code(self, prompt: str, narration_script: str = None) -> str:
        # For all prompts, first generate a narration script if not provided
        if narration_script is None:
            narration_script = self.generate_narration_script(prompt)
        
        # Enhance the user prompt for Manim code generation
        enhanced_prompt = f"""Create Manim animation code for the following educational concept:
{prompt}

Here is the narration script that the animation should follow exactly:
{narration_script}

Requirements:
1. Create animations that PRECISELY match the narration script sections and timing
2. Include all necessary imports (start with "from manim import *")
3. Always include "import math" and "import numpy as np"
4. Name the scene class 'CustomAnimation'
5. Include detailed comments that reference the script timestamps
6. Use appropriate self.wait() durations to match narration timing - typically:
   - 1-2 seconds for short sentences
   - 2-3 seconds for complex concepts
   - 0.5-1 seconds for transitions
7. Time visual elements to appear exactly when they would be mentioned in the narration
8. Use vibrant colors to enhance understanding and visual distinction
9. Add clear text labels that match key phrases from the script
10. IMPORTANT: Do NOT use Tex or MathTex objects as they require LaTeX. Use Text instead.
11. IMPORTANT: Use Create() instead of ShowCreation() as it's deprecated
12. EXTREMELY IMPORTANT: Do NOT include any triple backticks (```) or markdown formatting in your code
13. EXTREMELY IMPORTANT: Only return pure Python code that can be executed directly
14. CRITICALLY IMPORTANT: Always remove or fade out text and objects before adding new ones in the same space
15. CRITICALLY IMPORT: Use Transform() to update text/objects rather than creating new ones and leaving old ones
16. CRITICALLY IMPORTANT: Define clear spatial zones on the screen and maintain consistent positioning:
    - title_region = UP * 3.5
    - main_region = ORIGIN
    - explanation_region = DOWN * 3
17. Always group related objects with VGroup for easier management
18. When explaining step-by-step processes, use transforms to show progressive changes
19. Always use FadeOut() for objects that are no longer needed to keep the scene clean
20. When showing multiple items, arrange them with proper spacing using arrange() or position them with UP/DOWN/LEFT/RIGHT
21. CRITICALLY IMPORTANT: Create a COMPREHENSIVE and IN-DEPTH animation - don't rush the explanation
22. Take as much time as needed to fully explain the concept - there is NO time limit
23. The animation should match the narration script length, however long that may be

If you can't create a specific animation for this prompt, do NOT use a generic template. Instead, create a targeted animation that addresses the prompt as specifically as possible.

The code MUST start exactly like this:
from manim import *
import math
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        # Define screen regions for better organization
        title_region = UP * 3.5
        main_region = ORIGIN
        explanation_region = DOWN * 3 + LEFT * 3
        
        # Your code here aligned with narration timestamps
"""

        # Use direct HTTP request to Groq API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "messages": [
                {"role": "system", "content": self.animation_system_prompt},
                {"role": "user", "content": enhanced_prompt}
            ],
            "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
            "max_tokens": 8000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Animation generation API request failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        raw_generated_code = result["choices"][0]["message"]["content"].strip()
        
        # For debugging
        print("Raw response from Groq:")
        print(raw_generated_code[:100] + "..." if len(raw_generated_code) > 100 else raw_generated_code)
        
        # Check if response starts with explanatory text and remove it
        if not raw_generated_code.startswith("from manim import"):
            # Find the first line that looks like code
            code_start = raw_generated_code.find("from manim import")
            if code_start != -1:
                raw_generated_code = raw_generated_code[code_start:]
            else:
                raise Exception("Could not find proper Manim import statement in generated code")
        
        # Check for common issues
        if "MathTex(" in raw_generated_code or "Tex(" in raw_generated_code:
            raise Exception("Generated code contains LaTeX objects which are not supported")
            
        if "math.sqrt" in raw_generated_code and "import math" not in raw_generated_code:
            # Add math import if missing
            raw_generated_code = "import math\n" + raw_generated_code
            
        if "np." in raw_generated_code and "import numpy as np" not in raw_generated_code:
            # Add numpy import if missing
            raw_generated_code = "import numpy as np\n" + raw_generated_code
        
        # Replace deprecated methods
        raw_generated_code = raw_generated_code.replace("ShowCreation(", "Create(")
        
        # Validate the basic structure
        if not self.validate_code(raw_generated_code):
            raise Exception("Generated code does not have required elements")
            
        # Combine the script and animation code into a single result
        # Add the narration script as a comment at the top of the animation code
        script_comment = """
# NARRATION SCRIPT:
# ----------------
"""
        for line in narration_script.split('\n'):
            script_comment += f"# {line}\n"
        
        # Insert the script comment after the imports
        manim_import_end = raw_generated_code.find('\n', raw_generated_code.find('from manim import'))
        final_code = raw_generated_code[:manim_import_end+1] + script_comment + raw_generated_code[manim_import_end+1:]
        
        return final_code
    
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