import os
import re
from typing import Dict, Any
import requests

class GroqHandler:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
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

The script should be approximately 2-3 minutes when read aloud at a natural pace. Focus on clarity, engagement, and educational value above all else."""

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

TECHNICAL REQUIREMENTS:
- Start with 'from manim import *'
- Always include 'import math' and 'import numpy as np'
- Use Text() instead of Tex()/MathTex() where appropriate for compatibility
- Use Create() instead of ShowCreation() (deprecated)
- Name the main Scene class 'CustomAnimation'
- Make animations match the script length (typically 2-3 minutes)
- Pay special attention to timing - allow time for narration of each concept

The key is to create an animation that perfectly complements the script, with visual elements appearing exactly when they would be mentioned in the narration."""
        
        # Universal template that can be adapted to any concept
        self.universal_template = '''from manim import *
import math
import numpy as np

# NARRATION SCRIPT:
# ----------------
# [00:00] INTRODUCTION
# Welcome to this educational video. Today we'll explore an important concept and break it down into easy-to-understand components.
# 
# [00:30] MAIN CONCEPTS
# Let's examine the key aspects of this topic and understand how it works in practice.
# 
# [01:30] CONCLUSION
# To summarize what we've learned, remember these key points about the topic. Thank you for watching!

class CustomAnimation(Scene):
    """
    A universal template for creating educational animations.
    This template is designed to be flexible and adaptable to any educational concept.
    It includes standard sections for introduction, main content, and summary.
    """
    def construct(self):
        # Title section [00:00]
        title = Text("Educational Animation", font_size=40)
        self.play(Write(title))
        self.wait(1)  # Give time for narration
        self.play(title.animate.scale(0.7).to_edge(UP))
        
        # Introduction section
        intro_text = Text("This animation explains an educational concept", font_size=28)
        intro_text.next_to(title, DOWN, buff=0.5)
        self.play(Write(intro_text))
        self.wait(1.5)  # Time for narration
        self.play(FadeOut(intro_text))
        
        # Main content area - center of the screen [00:30]
        main_area = Rectangle(height=5, width=8, color=BLUE_E)
        main_area.set_fill(BLUE_E, opacity=0.1)
        self.play(Create(main_area))
        
        # Placeholder for main content
        main_content = Text("Main educational content will appear here", font_size=24)
        main_content.move_to(main_area.get_center())
        self.play(Write(main_content))
        self.wait(1)
        
        # Interactive element example
        self.play(FadeOut(main_content))
        
        # Create an example visualization - can be adapted to any concept
        circle = Circle(radius=1.5, color=BLUE)
        circle.move_to(main_area.get_center())
        self.play(Create(circle))
        
        # Add labels or information points around the visualization
        info_points = []
        labels = ["Point 1", "Point 2", "Point 3", "Point 4"]
        
        for i, label_text in enumerate(labels):
            angle = i * PI/2  # Evenly space around the circle
            point_pos = circle.get_center() + 2 * np.array([np.cos(angle), np.sin(angle), 0])
            
            dot = Dot(point_pos, color=YELLOW)
            label = Text(label_text, font_size=18).next_to(dot, direction=point_pos - circle.get_center(), buff=0.2)
            
            info_points.append(VGroup(dot, label))
            
        for point in info_points:
            self.play(Create(point[0]), Write(point[1]))
            self.wait(0.3)  # Brief pause between points
        
        # Transform to another shape to show concept evolution
        square = Square(side_length=3, color=GREEN)
        square.move_to(circle.get_center())
        self.play(Transform(circle, square))
        self.wait(1)
        
        # Example of showing a relationship or connection
        arrow = Arrow(start=info_points[0][0].get_center(), end=info_points[2][0].get_center(), color=RED)
        relation_text = Text("Relationship", font_size=20).next_to(arrow, RIGHT)
        self.play(Create(arrow), Write(relation_text))
        self.wait(1)
        
        # Cleanup for summary
        self.play(
            *[FadeOut(point) for point in info_points],
            FadeOut(arrow),
            FadeOut(relation_text),
            FadeOut(circle)  # This is now the square due to transform
        )
        
        # Summary section [01:30]
        summary_title = Text("Summary", font_size=36)
        summary_title.move_to(main_area.get_center() + UP * 1.5)
        
        summary_points = VGroup(
            Text("• Key point 1", font_size=24),
            Text("• Key point 2", font_size=24),
            Text("• Key point 3", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        summary_points.next_to(summary_title, DOWN, buff=0.5)
        
        self.play(Write(summary_title))
        for point in summary_points:
            self.play(Write(point))
            self.wait(0.3)
        
        self.wait(1)
        
        # Final cleanup
        self.play(
            FadeOut(summary_title),
            FadeOut(summary_points),
            FadeOut(main_area)
        )
        
        # End card
        end_text = Text("Thank you for watching!", font_size=36)
        self.play(Write(end_text))
        self.wait(2)
'''
        
    def generate_narration_script(self, prompt: str) -> str:
        """Generate a narration script for the animation based on the prompt"""
        try:
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

Format the script like this:
[00:00] INTRODUCTION
[Script text goes here...]

[00:30] MAIN CONCEPT 1
[Script text goes here...]

[01:15] MAIN CONCEPT 2
[Script text goes here...]

[02:00] CONCLUSION
[Script text goes here...]

Keep the total narration length to approximately 2-3 minutes when read at a natural pace."""

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
                "model": "mixtral-8x7b-32768",
                "max_tokens": 2000,
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
            
            return script
            
        except Exception as e:
            print(f"Error in narration script generation: {str(e)}")
            # Return a simple script in case of any error
            return f"""[00:00] INTRODUCTION
Welcome to this educational video about {prompt}. Today we'll explore this concept and break it down into simple components.

[00:30] MAIN CONCEPTS
Let's dive into the key aspects of this topic and understand how it works.

[01:30] CONCLUSION
To summarize what we've learned about {prompt}, remember these key points. Thank you for watching!"""
    
    def generate_manim_code(self, prompt: str) -> str:
        # For all prompts, first generate a narration script
        try:
            # Generate the narration script
            narration_script = self.generate_narration_script(prompt)
            
            # Now use the script to generate the Manim animation
            enhanced_prompt = f"""Create a Manim animation that aligns perfectly with this narration script:

{narration_script}

The animation should:
1. Follow the exact structure and flow of the script
2. Time visual elements to appear when they would be mentioned in the narration
3. Include all key concepts mentioned in the script
4. Use appropriate visual metaphors and representations
5. Include text labels that reflect key phrases from the script
6. Time transitions to align with the script sections
7. Allow appropriate pauses for narration (use self.wait() where needed)

If you can't create a specific animation for this prompt, adapt the universal template to fit the script.

TECHNICAL REQUIREMENTS:
1. Use the Scene class named 'CustomAnimation'
2. Include ALL necessary imports (start with 'from manim import *', and include 'import math' and 'import numpy as np')
3. Use appropriate animations and transitions with proper timing
4. Add DETAILED text labels and explanations for ALL elements
5. Include appropriate pauses (self.wait()) to allow for narration
6. Use vibrant colors to enhance understanding and visual appeal
7. Design the animation to match the script length (approximately 2-3 minutes)
8. IMPORTANT: Use Text instead of Tex/MathTex where appropriate
9. IMPORTANT: Use Create() instead of ShowCreation() as the latter is deprecated

The code MUST start exactly like this:
from manim import *
import math
import numpy as np

class CustomAnimation(Scene):
    \"\"\"
    Animation that visually represents: {prompt}
    This animation is designed to accompany the following narration script:
    {narration_script[:300]}...
    \"\"\"
    def construct(self):
        # Your DETAILED code here with comprehensive comments
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
                "model": "mixtral-8x7b-32768",
                "max_tokens": 4000,
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
                    # If we can't find proper imports, use the universal template
                    print("Could not find proper code in Groq's response, using universal template")
                    return self.adapt_universal_template(prompt, narration_script)
            
            # Check for common issues
            if "MathTex(" in raw_generated_code or "Tex(" in raw_generated_code:
                print("Found LaTeX objects in code, using universal template instead")
                return self.adapt_universal_template(prompt, narration_script)
                
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
                print("Generated code does not have required elements, using universal template")
                return self.adapt_universal_template(prompt, narration_script)
                
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
            
        except Exception as e:
            print(f"Error in Groq handler: {str(e)}")
            # Return the universal template in case of any error
            return self.adapt_universal_template(prompt, "Error generating script")
    
    def adapt_universal_template(self, prompt: str, narration_script: str) -> str:
        """Adapt the universal template to the specific prompt and script"""
        # Replace generic title with prompt-specific title
        modified_template = self.universal_template.replace(
            "Educational Animation", 
            prompt[:40] + "..." if len(prompt) > 40 else prompt
        )
        
        # Replace generic narration script with the generated one
        script_comment = "# NARRATION SCRIPT:\n# ----------------\n"
        for line in narration_script.split('\n'):
            script_comment += f"# {line}\n"
        
        # Replace the default script in the template
        start_script = modified_template.find("# NARRATION SCRIPT:")
        end_script = modified_template.find("class CustomAnimation")
        if start_script != -1 and end_script != -1:
            modified_template = modified_template[:start_script] + script_comment + modified_template[end_script:]
        
        # Replace the docstring
        docstring_start = modified_template.find('"""', modified_template.find("class CustomAnimation"))
        docstring_end = modified_template.find('"""', docstring_start + 3) + 3
        if docstring_start != -1 and docstring_end != -1:
            new_docstring = f'"""\n    Animation that visually represents: {prompt}\n    This animation is designed to accompany the generated narration script.\n    """'
            modified_template = modified_template[:docstring_start] + new_docstring + modified_template[docstring_end:]
        
        return modified_template
    
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