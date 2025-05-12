import os
import re
from typing import Dict, Any
import requests
import json

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
        """
        Generate Manim code for animation using Groq.
        """
        # For all prompts, first generate a narration script if not provided
        if narration_script is None:
            narration_script = self.generate_narration_script(prompt)
            
        # Create an explicit code template to help the model understand the expected format
        code_template = '''
from manim import *
import math
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        # Define regions for organization
        title_region = UP * 3.5
        main_region = ORIGIN
        explanation_region = DOWN * 3
        
        # Create a title
        title = Text("Title Text", color=BLUE).move_to(title_region)
        self.play(Write(title))
        self.wait(1)
        
        # Create content
        text1 = Text("First explanation point", color=WHITE).scale(0.7).move_to(explanation_region)
        self.play(FadeIn(text1))
        self.wait(1.5)
        
        # Create visual elements
        circle = Circle(radius=1.5, color=GREEN).move_to(main_region)
        self.play(Create(circle))
        self.wait(1)
        
        # Show relationships
        arrow = Arrow(start=text1.get_top(), end=circle.get_bottom(), color=YELLOW)
        self.play(Create(arrow))
        self.wait(1)
        
        # Clean up and transition
        self.play(FadeOut(text1), FadeOut(arrow))
        
        # Add more content
        text2 = Text("Second explanation point", color=WHITE).scale(0.7).move_to(explanation_region)
        self.play(FadeIn(text2))
        self.wait(1.5)
        
        # Final cleanup
        self.play(FadeOut(circle), FadeOut(text2), FadeOut(title))
        self.wait(1)
'''

        # Enhanced prompt with explicit instructions for Groq
        enhanced_prompt = f"""Generate Manim animation code based on this prompt: 
{prompt}

FOLLOW THESE REQUIREMENTS EXACTLY:
1. The code MUST start with 'from manim import *' and include all necessary imports
2. The class MUST follow the exact pattern seen in this template:

{code_template}

3. IMPORTANT: Your response should ONLY contain Python code with no explanations outside of the code
4. Use Text objects instead of MathTex or Tex
5. Use Create() instead of ShowCreation()
6. Make sure all code is properly indented inside methods

For your reference, here are the key elements your code MUST contain:
- All necessary imports at the top
- A class that extends Scene
- A construct method taking self parameter
- Proper use of self.play() and self.wait()
- Text positioning that stays within visible boundaries (-6 to 6 coordinate range)
- Proper cleanup with FadeOut for elements no longer needed

DO NOT include any markdown formatting or explanation - ONLY RETURN VALID PYTHON CODE.
"""

        # Add narration script context if provided
        if narration_script:
            enhanced_prompt += f"\n\nFollow this narration script timing and content for your animation:\n{narration_script}\n"

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "messages": [
                    {"role": "system", "content": "You are an expert Manim programmer who generates perfect Python code for animations."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                "model": "llama3-70b-8192",
                "max_tokens": 8192,
                "temperature": 0.7
            }
            
            print("Sending request to Groq API...")
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                print(f"API request failed with status {response.status_code}: {response.text}")
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
            
            result = response.json()
            
            # Extract the code from the response
            raw_code = result['choices'][0]['message']['content']
            print(f"Raw response from Groq:\n{raw_code[:100]}...")
            
            # Ensure we're only returning code, not explanation
            code = self._extract_code(raw_code)
            
            if not code or len(code) < 150:  # Basic validation for code length
                print("Generated code is too short or empty")
                raise Exception("Generated code is too short or empty")
            
            return code
            
        except Exception as e:
            print(f"Error in generate_manim_code: {str(e)}")
            raise Exception(f"Script generation API request failed: {str(e)}")
            
    def _extract_code(self, raw_response: str) -> str:
        """Extract just the code from the raw LLM response, removing any explanations."""
        # If the response contains code blocks, extract them
        code_block_pattern = r'```(?:python)?(.*?)```'
        code_blocks = re.findall(code_block_pattern, raw_response, re.DOTALL)
        
        if code_blocks:
            # Join all code blocks, excluding the language identifier
            return '\n'.join(block.strip() for block in code_blocks)
        
        # Look for essential markers of Python code (imports and class definitions)
        if "from manim import" in raw_response and "class" in raw_response and "def construct" in raw_response:
            return raw_response
            
        # Try to find the code beginning with common imports
        if "from manim import" in raw_response:
            code_start = raw_response.find("from manim import")
            return raw_response[code_start:].strip()
            
        # If nothing works, just return the whole response for further processing
        return raw_response
    
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