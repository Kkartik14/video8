#!/usr/bin/env python3
"""
Test script to verify that markdown cleaning functions work correctly.
"""
import os
import sys

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.scene_generator import SceneGenerator

def test_markdown_cleaning():
    """Test that the markdown artifact cleaning works correctly."""
    scene_gen = SceneGenerator()
    
    # Test case 1: Code with triple backticks at start and end
    test_code_1 = """```python
from manim import *
import math

class CustomAnimation(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```"""
    
    fixed_code_1 = scene_gen._remove_markdown_artifacts(test_code_1)
    print("\nTest Case 1: Triple backticks at start and end")
    print("Before:")
    print(test_code_1)
    print("\nAfter:")
    print(fixed_code_1)
    
    # Test case 2: Code with backticks in the middle
    test_code_2 = """from manim import *
import math

class CustomAnimation(Scene):
    def construct(self):
        # Here is a circle
        circle = Circle()
        self.play(Create(circle))
        
        # Here is a ```code block```
        square = Square()
        self.play(Create(square))
"""
    
    fixed_code_2 = scene_gen._remove_markdown_artifacts(test_code_2)
    print("\nTest Case 2: Backticks in the middle")
    print("Before:")
    print(test_code_2)
    print("\nAfter:")
    print(fixed_code_2)
    
    # Test case 3: Code with only line containing backticks
    test_code_3 = """from manim import *
import math

class CustomAnimation(Scene):
    def construct(self):
        # First animation
        circle = Circle()
        self.play(Create(circle))
        
```
        
        # Second animation
        square = Square()
        self.play(Create(square))
"""
    
    fixed_code_3 = scene_gen._remove_markdown_artifacts(test_code_3)
    print("\nTest Case 3: Line containing only backticks")
    print("Before:")
    print(test_code_3)
    print("\nAfter:")
    print(fixed_code_3)
    
    # Test case 4: Code with syntax error containing backticks
    test_code_4 = """from manim import *
import math

class CustomAnimation(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        
        # This line has a syntax error ```
        square = Square()
        self.play(Create(square))
"""
    
    fixed_code_4 = scene_gen._fix_common_syntax_errors(
        scene_gen._remove_markdown_artifacts(test_code_4)
    )
    print("\nTest Case 4: Syntax error with backticks")
    print("Before:")
    print(test_code_4)
    print("\nAfter:")
    print(fixed_code_4)
    
    # Test last resort fixes
    problem_code = """```python
from manim import *

class CustomAnimation(Scene):
    def construct(self):
        # This has syntax errors ```
        circle = Circle()
        self.play(Create(circle)
        
        # Missing parenthesis above
        square = Square(
        # Missing parenthesis here too
```"""
    
    fixed_code = scene_gen._apply_last_resort_fixes(problem_code)
    print("\nTest Case 5: Last resort fixes for broken code")
    print("Before:")
    print(problem_code)
    print("\nAfter:")
    print(fixed_code)
    
if __name__ == "__main__":
    test_markdown_cleaning() 