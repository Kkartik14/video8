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
        
        # System prompt for generating Manim code
        self.system_prompt = """You are an expert at generating Manim animation code. 
Given a natural language prompt, you will generate Python code using Manim to create 
beautiful and educational 2D animations. Follow these instructions EXACTLY:
1. ONLY return Python code with no explanations or additional text before or after
2. Do not include markdown code blocks or any other formatting
3. Do not include any statements like 'Here's the code', just start directly with the imports
4. Ensure the code is fully functional and can run on its own
5. IMPORTANT: Do NOT use Tex or MathTex objects as they require LaTeX. Use Text instead.
6. Always include 'import math' if you need mathematical functions
7. Use Create() instead of ShowCreation() as it's deprecated in newer versions"""
        
        # General purpose template that can adapt to any prompt
        self.universal_template = '''from manim import *
import math
import numpy as np

class CustomAnimation(Scene):
    """
    A generic template for creating educational animations.
    This template is designed to be flexible and adaptable to any educational concept.
    """
    def construct(self):
        # Title section
        title = Text("Educational Animation", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.7).to_edge(UP))
        self.wait(0.5)
        
        # Introduction section
        intro_text = Text("This animation explains an educational concept", font_size=28)
        intro_text.next_to(title, DOWN, buff=0.5)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(FadeOut(intro_text))
        
        # Main content area - center of the screen
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
            self.wait(0.3)
        
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
        
        # Summary section
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
        
    def generate_manim_code(self, prompt: str) -> str:
        # For all prompts, try to generate with Claude
        try:
            # Enhance the user prompt with specific requirements
            enhanced_prompt = f"""Create a Manim animation for the following prompt:
{prompt}

Requirements:
1. Use the Scene class named 'CustomAnimation'
2. Include all necessary imports (always start with 'from manim import *', and include 'import math' if needed)
3. Use appropriate animations and transitions
4. Add text labels and explanations where needed
5. Ensure smooth animations with appropriate timing
6. Use color to enhance understanding
7. Keep the animation under 1 minute
8. IMPORTANT: Do NOT use Tex, MathTex, or any LaTeX-dependent objects as they require LaTeX. Use Text instead.
9. IMPORTANT: Use Create() instead of ShowCreation() as the latter is deprecated
10. IMPORTANT: Do NOT include any self.wait() or other self references outside of the construct method
11. IMPORTANT: All code that references 'self' MUST be properly indented inside the construct method
12. Include a final self.wait(2) at the end of the construct method to allow viewing the final state

If you can't create a specific animation for this prompt, adapt the universal template to fit it.

The code MUST start exactly like this:
from manim import *
import math  # Include this if you need mathematical functions
import numpy as np  # Include this if you need numpy

class CustomAnimation(Scene):
    def construct(self):
        # Your code here
"""

            # Using direct API call instead of the library
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": "claude-2.0",
                "prompt": f"\n\nHuman: {self.system_prompt}\n\n{enhanced_prompt}\n\nAssistant:",
                "max_tokens_to_sample": 2000,
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
            
            # Validate and fix the generated code
            code = self.validate_and_fix_code(code)
            
            return code
            
        except Exception as e:
            print(f"Error generating code with Claude: {str(e)}")
            print("Falling back to universal template")
            return self.universal_template
    
    def validate_and_fix_code(self, code: str) -> str:
        """Validate and fix common issues in the generated Manim code."""
        # Remove any explanatory text at the beginning
        if not code.strip().startswith('from manim import'):
            start_idx = code.find('from manim import')
            if start_idx != -1:
                code = code[start_idx:]
            else:
                print("Could not find Manim import statement, using universal template")
                return self.universal_template
                
        # Replace deprecated methods
        code = code.replace("ShowCreation(", "Create(")
            
        # Fix missing imports
        if "math." in code and "import math" not in code:
            code = "import math\n" + code
            
        if "np." in code and "import numpy as np" not in code:
            code = "import numpy as np\n" + code
            
        # Check for LaTeX (which we don't want)
        if "MathTex(" in code or "Tex(" in code:
            print("Found LaTeX objects in code, using universal template instead")
            return self.universal_template
        
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