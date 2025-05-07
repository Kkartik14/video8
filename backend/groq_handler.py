import os
import re
from typing import Dict, Any
from groq import Groq

class GroqHandler:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        self.client = Groq(api_key=self.api_key)
        
        # System prompt for generating Manim code
        self.system_prompt = """You are an expert at generating Manim animation code. 
Given a natural language prompt, you will generate Python code using Manim to create 
beautiful and educational 2D animations. Follow these instructions EXACTLY:
1. ONLY return Python code with no explanations or additional text before or after
2. Do not include markdown code blocks or any other formatting
3. Do not include any statements like 'Here's the code', just start directly with the imports
4. Ensure the code is fully functional and can run on its own
5. Use Text instead of Tex/MathTex where appropriate
6. Always include 'import math' if you need mathematical functions
7. Use Create() instead of ShowCreation() as it's deprecated in newer versions"""
        
        # Dictionary of pre-built templates for specific prompts
        self.templates = {
            "pythagorean": '''from manim import *
import math
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        # Create a right triangle
        right_triangle = Polygon(
            ORIGIN, 
            RIGHT * 3, 
            UP * 4, 
            color=WHITE,
            fill_opacity=0.2
        )
        
        # Create squares on each side
        side_a = 3  # base
        side_b = 4  # height
        side_c = 5  # hypotenuse (calculated using Pythagorean theorem)
        
        # Square on side a (base)
        square_a = Square(side_length=side_a, color=RED, fill_opacity=0.5)
        square_a.move_to(RIGHT * (side_a/2))
        square_a.shift(DOWN * (side_a/2 + 0.5))
        
        # Square on side b (height)
        square_b = Square(side_length=side_b, color=BLUE, fill_opacity=0.5)
        square_b.move_to(RIGHT * 3 + UP * (side_b/2))
        square_b.shift(RIGHT * (side_b/2 + 0.5))
        
        # Square on side c (hypotenuse)
        square_c = Square(side_length=side_c, color=GREEN, fill_opacity=0.5)
        square_c.rotate(math.atan2(4, 3))
        square_c.move_to(RIGHT * 1.5 + UP * 2)
        square_c.shift((UP + RIGHT) * (side_c/4))
        
        # Add labels
        label_a = Text("a = 3", font_size=24).next_to(square_a, DOWN)
        label_b = Text("b = 4", font_size=24).next_to(square_b, RIGHT)
        label_c = Text("c = 5", font_size=24).next_to(square_c, UP + RIGHT)
        
        # Add area labels
        area_a = Text("Area = 9", font_size=20, color=RED).move_to(square_a)
        area_b = Text("Area = 16", font_size=20, color=BLUE).move_to(square_b)
        area_c = Text("Area = 25", font_size=20, color=GREEN).move_to(square_c)
        
        # Add formula
        formula = Text("a² + b² = c²", font_size=36).to_edge(UP)
        formula_values = Text("3² + 4² = 5²", font_size=30).next_to(formula, DOWN)
        formula_result = Text("9 + 16 = 25", font_size=30).next_to(formula_values, DOWN)
        
        # Animations
        self.play(Create(right_triangle))
        self.wait(0.5)
        
        self.play(Create(square_a), Write(label_a))
        self.wait(0.3)
        
        self.play(Create(square_b), Write(label_b))
        self.wait(0.3)
        
        self.play(Create(square_c), Write(label_c))
        self.wait(0.5)
        
        self.play(Write(area_a))
        self.play(Write(area_b))
        self.play(Write(area_c))
        self.wait(0.5)
        
        self.play(Write(formula))
        self.wait(0.3)
        
        self.play(Write(formula_values))
        self.wait(0.3)
        
        self.play(Write(formula_result))
        self.wait(1)
        
        self.play(
            Indicate(area_a),
            Indicate(area_b),
            run_time=1
        )
        self.wait(0.3)
        
        self.play(Indicate(area_c), run_time=1)
        self.wait(1)
'''
        }
        
        # Default template for other prompts
        self.default_template = '''from manim import *
import math
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        # Title
        title = Text("Animation", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Create a simple object
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        self.wait(1)
        
        # Transform to another shape
        square = Square(side_length=4, color=RED)
        self.play(Transform(circle, square))
        self.wait(1)
        
        # Add some text
        text = Text("Simple Animation", font_size=30)
        text.next_to(square, DOWN)
        self.play(Write(text))
        self.wait(2)
'''
        
    def generate_manim_code(self, prompt: str) -> str:
        # Check if prompt is about Pythagorean theorem
        if any(keyword in prompt.lower() for keyword in ["pythagorean", "theorem", "square", "triangle"]):
            print("Using pre-built Pythagorean theorem template")
            return self.templates["pythagorean"]
            
        # For other prompts, try to generate with Groq
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
8. IMPORTANT: Use Text instead of Tex/MathTex where appropriate
9. IMPORTANT: Use Create() instead of ShowCreation() as the latter is deprecated

The code MUST start exactly like this:
from manim import *
import math  # Include this if you need mathematical functions
import numpy as np  # Include this if you need numpy

class CustomAnimation(Scene):
    def construct(self):
        # Your code here
"""

            # Use Groq to generate code
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": enhanced_prompt}
                ],
                model="mixtral-8x7b-32768",
                max_tokens=2000,
                temperature=0.7,
            )
            
            # Extract the generated code
            raw_generated_code = response.choices[0].message.content.strip()
            
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
                    # If we can't find proper imports, use the default template
                    print("Could not find proper code in Groq's response, using default template")
                    return self.default_template
            
            # Check for common issues
            if "MathTex(" in raw_generated_code or "Tex(" in raw_generated_code:
                print("Found LaTeX objects in code, using default template instead")
                return self.default_template
                
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
                print("Generated code does not have required elements, using default template")
                return self.default_template
                
            return raw_generated_code
            
        except Exception as e:
            print(f"Error in Groq handler: {str(e)}")
            # Return the default template in case of any error
            return self.default_template
            
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