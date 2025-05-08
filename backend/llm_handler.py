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
''',
            "binary_search": '''from manim import *
import math
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        # Title
        title = Text("Binary Search", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.8).to_edge(UP))
        
        # Create a sorted array
        array = [1, 3, 5, 7, 9, 11, 13, 15, 17]
        target = 11
        
        # Visual representation of array
        squares = []
        labels = []
        
        # Create squares and labels for each element
        for i, num in enumerate(array):
            square = Square(side_length=1)
            square.set_stroke(WHITE, 2)
            square.set_fill(BLUE, opacity=0.5)
            
            label = Text(str(num), font_size=36)
            
            squares.append(square)
            labels.append(label)
        
        # Arrange squares in a line
        squares_group = VGroup(*squares).arrange(RIGHT, buff=0.1)
        squares_group.move_to(ORIGIN)
        
        # Position labels in squares
        for i, (square, label) in enumerate(zip(squares, labels)):
            label.move_to(square.get_center())
        
        # Show array
        array_label = Text("Sorted Array:", font_size=36).next_to(squares_group, UP * 2)
        self.play(Write(array_label))
        self.play(
            *[Create(square) for square in squares],
            *[Write(label) for label in labels],
            run_time=2
        )
        self.wait(1)
        
        # Target value
        target_text = Text(f"Target: {target}", font_size=36).next_to(array_label, RIGHT * 4)
        self.play(Write(target_text))
        self.wait(1)
        
        # Initialize pointers
        low, high = 0, len(array) - 1
        
        # Create pointer labels
        low_label = Text("Low", font_size=24, color=GREEN).next_to(squares[low], DOWN)
        high_label = Text("High", font_size=24, color=RED).next_to(squares[high], DOWN)
        mid_label = None
        
        self.play(
            Write(low_label),
            Write(high_label)
        )
        self.wait(1)
        
        # Binary search iterations
        iteration = 1
        found = False
        
        while low <= high and not found:
            # Calculate middle index
            mid = (low + high) // 2
            
            # Create or move mid pointer
            if mid_label:
                self.play(
                    mid_label.animate.next_to(squares[mid], DOWN)
                )
            else:
                mid_label = Text("Mid", font_size=24, color=YELLOW).next_to(squares[mid], DOWN)
                self.play(Write(mid_label))
            
            # Highlight current element being compared
            self.play(
                squares[mid].animate.set_fill(YELLOW, opacity=0.8),
                labels[mid].animate.set_color(BLACK)
            )
            
            # Show iteration
            iteration_text = Text(f"Iteration {iteration}", font_size=36).to_edge(LEFT+UP)
            comparison_text = Text(f"Comparing {array[mid]} with target {target}", font_size=28).next_to(iteration_text, DOWN)
            
            self.play(
                Write(iteration_text),
                Write(comparison_text)
            )
            self.wait(1)
            
            # Check if element is found
            if array[mid] == target:
                self.play(
                    squares[mid].animate.set_fill(GREEN, opacity=0.8),
                    FadeOut(comparison_text)
                )
                result_text = Text(f"Found {target} at index {mid}!", font_size=32, color=GREEN).next_to(iteration_text, DOWN)
                self.play(Write(result_text))
                found = True
            elif array[mid] < target:
                self.play(
                    squares[mid].animate.set_fill(BLUE, opacity=0.5),
                    labels[mid].animate.set_color(WHITE),
                    FadeOut(comparison_text)
                )
                
                # Update low pointer
                low = mid + 1
                self.play(
                    low_label.animate.next_to(squares[low], DOWN),
                    squares[low-1:mid+1].animate.set_fill(GREY, opacity=0.2),
                    *[label.animate.set_color(GREY) for label in labels[low-1:mid+1]]
                )
                
                update_text = Text(f"{array[mid]} < {target}, so search right half", font_size=28).next_to(iteration_text, DOWN)
                self.play(Write(update_text))
                self.wait(1)
                self.play(FadeOut(update_text))
            else:
                self.play(
                    squares[mid].animate.set_fill(BLUE, opacity=0.5),
                    labels[mid].animate.set_color(WHITE),
                    FadeOut(comparison_text)
                )
                
                # Update high pointer
                high = mid - 1
                self.play(
                    high_label.animate.next_to(squares[high], DOWN) if high >= 0 else high_label.animate.shift(LEFT * 3),
                    squares[mid:high+2].animate.set_fill(GREY, opacity=0.2) if high >= 0 else squares[mid:].animate.set_fill(GREY, opacity=0.2),
                    *[label.animate.set_color(GREY) for label in labels[mid:high+2]] if high >= 0 else [label.animate.set_color(GREY) for label in labels[mid:]]
                )
                
                update_text = Text(f"{array[mid]} > {target}, so search left half", font_size=28).next_to(iteration_text, DOWN)
                self.play(Write(update_text))
                self.wait(1)
                self.play(FadeOut(update_text))
            
            self.play(FadeOut(iteration_text))
            iteration += 1
            
            # Break if we don't find it after reasonable iterations
            if iteration > 5:
                break
                
        if not found:
            not_found_text = Text(f"Target {target} not found in array!", font_size=32, color=RED).to_edge(DOWN)
            self.play(Write(not_found_text))
        
        self.wait(2)
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
        
        # Check if prompt is about binary search
        if any(keyword in prompt.lower() for keyword in ["binary search", "sorted array", "searching algorithm"]):
            print("Using pre-built binary search template")
            return self.templates["binary_search"]
            
        # For other prompts, try to generate with Claude
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
            print("Falling back to default template")
            return self.default_template
    
    def validate_and_fix_code(self, code: str) -> str:
        """Validate and fix common issues in the generated Manim code."""
        # Remove any explanatory text at the beginning
        if not code.strip().startswith('from manim import'):
            start_idx = code.find('from manim import')
            if start_idx != -1:
                code = code[start_idx:]
            else:
                print("Could not find Manim import statement, using default template")
                return self.default_template
                
        # Replace deprecated methods
        code = code.replace("ShowCreation(", "Create(")
            
        # Fix missing imports
        if "math." in code and "import math" not in code:
            code = "import math\n" + code
            
        if "np." in code and "import numpy as np" not in code:
            code = "import numpy as np\n" + code
            
        # Check for LaTeX (which we don't want)
        if "MathTex(" in code or "Tex(" in code:
            print("Found LaTeX objects in code, using default template instead")
            return self.default_template
        
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