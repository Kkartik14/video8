import os
import re
from typing import Dict, Any
import requests

class GroqHandler:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        # System prompt for generating Manim code
        self.system_prompt = """You are an expert mathematical animator specializing in Manim, the powerful Python library for creating precise and beautiful mathematical animations. Your task is to generate comprehensive, production-ready Manim code that transforms abstract concepts into visually stunning educational animations.

USE CASE:
This system serves educators, students, and content creators who need to visualize complex concepts through animation but lack the technical expertise to code these visualizations from scratch. Your generated code will be directly executed to create videos that explain mathematical, scientific, or educational concepts visually. The quality, detail, and educational value of your code directly impacts learners' understanding of complex topics.

REQUIREMENTS (EXTREMELY IMPORTANT):
1. Generate COMPLETE, READY-TO-RUN Manim code that needs no modifications
2. Provide EXTREMELY DETAILED animations with thorough comments explaining the mathematical/conceptual significance of each element
3. Include comprehensive docstrings at the beginning of the code explaining the animation's purpose, concepts illustrated, and mathematical foundations
4. Structure animations pedagogically - build concepts step by step with clear visual progression
5. Use vibrant colors strategically to highlight important elements
6. Include detailed Text labels that explain each step of the concept
7. Add thoughtful transitions between animation segments
8. Incorporate appropriate timing (self.wait()) to allow viewers to process information
9. Use precise positioning and scaling for all objects
10. Exploit Manim's powerful animation capabilities fully (transforms, fades, indicates, etc.)
11. Include mathematical formulas where relevant, using appropriate formatting
12. Design animations that would work well in educational videos (clear, focused, purposeful)
13. Add camera movements and zooms when they enhance understanding
14. Use background grids, axes, or reference frames where appropriate
15. Include extra educational details that might not be explicitly requested but enhance understanding

TECHNICAL REQUIREMENTS:
- Start with 'from manim import *'
- Always include 'import math' and 'import numpy as np'
- Use Text() instead of Tex()/MathTex() where appropriate for compatibility
- Use Create() instead of ShowCreation() (deprecated)
- Name the main Scene class 'CustomAnimation'
- Make animations approximately 30-60 seconds in length
- Pay special attention to timing - give viewers time to process information

Remember: The generated code MUST be production-ready and execute without errors. Your work directly impacts educational outcomes, so provide the most detailed, comprehensive, and visually effective animations possible without concern for code length or verbosity. MORE DETAIL IS BETTER!"""
        
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
            enhanced_prompt = f"""Create an EXTREMELY DETAILED Manim animation for the following prompt:
{prompt}

I need a comprehensive, production-ready animation that explains this concept thoroughly with visual clarity and educational depth. The animation should:

1. Begin with a clear introduction to the concept
2. Break down each component step-by-step with detailed visual explanations
3. Use color strategically to highlight important elements and relationships
4. Include detailed text annotations explaining each step and its significance
5. Utilize camera movements, zooms, or highlights to emphasize key points
6. Show mathematical relationships explicitly where relevant
7. Build complexity gradually to ensure viewer understanding
8. Include thoughtful transitions between different stages of the explanation
9. End with a comprehensive summary that reinforces the key insights

TECHNICAL REQUIREMENTS:
1. Use the Scene class named 'CustomAnimation'
2. Include ALL necessary imports (start with 'from manim import *', and include 'import math' and 'import numpy as np')
3. Use appropriate animations and transitions with proper timing
4. Add DETAILED text labels and explanations for ALL elements
5. Include appropriate pauses (self.wait()) to allow viewers time to process information
6. Use vibrant colors to enhance understanding and visual appeal
7. Design the animation to be approximately 30-60 seconds in length
8. IMPORTANT: Use Text instead of Tex/MathTex where appropriate
9. IMPORTANT: Use Create() instead of ShowCreation() as the latter is deprecated

The code MUST start exactly like this:
from manim import *
import math
import numpy as np

class CustomAnimation(Scene):
    \"\"\"
    [Include a detailed docstring explaining the animation's purpose, mathematical foundations, and educational goals]
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
                    {"role": "system", "content": self.system_prompt},
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
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
            
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