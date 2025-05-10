"""
Test file to verify that the boundary checking implementation in SceneGenerator works correctly.
"""

import sys
import os
import re

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.scene_generator import SceneGenerator

def test_boundary_checking():
    # Create a scene generator instance
    sg = SceneGenerator()
    
    # Test code with text that would go out of bounds
    test_code = '''from manim import *
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        text = Text("This text would go out of bounds").move_to(LEFT * 10)
        self.play(Write(text))
        self.wait(1)
'''
    
    # Apply the _improve_animation_quality method to fix the code
    fixed_code = sg._improve_animation_quality(test_code)
    
    # Print the results
    print("Original code:")
    print("=============")
    print(test_code)
    print("\nFixed code:")
    print("==========")
    print(fixed_code)
    
    # Check if the fix was applied
    if "ensure_within_boundaries" in fixed_code:
        print("\n✅ Boundary checking was successfully applied!")
    else:
        print("\n❌ Boundary checking was not applied!")
    
    # Test with extreme values to ensure boundary check is triggered
    test_extreme = '''from manim import *
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        # These positions are all well beyond the visible boundaries
        far_left = Text("Far Left").move_to(LEFT * 15)
        far_right = Text("Far Right").move_to(RIGHT * 15)
        far_up = Text("Far Up").move_to(UP * 15)
        far_down = Text("Far Down").move_to(DOWN * 15)
        
        # Show the objects
        self.play(Write(far_left))
        self.play(Write(far_right))
        self.play(Write(far_up))
        self.play(Write(far_down))
        self.wait(1)
'''
    
    # Apply the improvement
    fixed_extreme = sg._improve_animation_quality(test_extreme)
    
    # Print the results
    print("\n\nExtreme values test:")
    print("===================")
    print("Original code:")
    print("=============")
    print(test_extreme)
    print("\nFixed code:")
    print("==========")
    print(fixed_extreme)
    
    # Check for boundary checking modifications
    boundary_func_added = "def ensure_within_boundaries" in fixed_extreme
    positions_fixed = re.search(r'\.move_to\(ensure_within_boundaries\(', fixed_extreme) is not None
    
    if boundary_func_added and positions_fixed:
        print("\n✅ Boundary checking for extreme values was successfully applied!")
    else:
        print("\n❌ Boundary checking for extreme values was not applied!")
    
    # Test multiple text objects with boundary issues
    test_code_2 = '''from manim import *
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        # Define regions
        title_region = UP * 8  # This is too far up, out of bounds
        
        # Create some text objects
        title = Text("Title").move_to(title_region)
        explanation = Text("This is a very long explanation").move_to(RIGHT * 9)
        
        # Show the objects
        self.play(Write(title))
        self.play(Write(explanation))
        self.wait(1)
'''
    
    # Apply the improvement
    fixed_code_2 = sg._improve_animation_quality(test_code_2)
    
    # Print the results
    print("\n\nSecond test - Multiple texts out of bounds:")
    print("=======================================")
    print("Original code:")
    print("=============")
    print(test_code_2)
    print("\nFixed code:")
    print("==========")
    print(fixed_code_2)
    
    # Check for specific boundary check patterns in the code
    has_boundary_func = "def ensure_within_boundaries" in fixed_code_2
    # Fix the regex pattern to search for our boundary checks
    boundary_check_pattern = r'\.move_to\(ensure_within_boundaries\('
    has_boundary_checks = re.search(boundary_check_pattern, fixed_code_2) is not None
    
    print(f"\nDetailed analysis of second test:")
    print(f"Has boundary function: {has_boundary_func}")
    print(f"Has boundary checks on move_to: {has_boundary_checks}")
    
    # Print all move_to calls found in the code
    move_to_calls = re.findall(r'\.move_to\([^)]+\)', fixed_code_2)
    print(f"Found {len(move_to_calls)} move_to calls:")
    for call in move_to_calls:
        print(f"  {call}")
        if "ensure_within_boundaries" in call:
            print("    ✅ Has boundary check")
        else:
            print("    ❌ Missing boundary check")
    
    # Only check for the boundary checks, not the function declaration
    if has_boundary_checks:
        print("\n✅ Boundary checking was successfully applied to text objects!")
    else:
        print("\n❌ Text boundary checking was not applied correctly to text objects!")

    # Test with explicit out-of-bounds values for debugging
    test_explicit = '''from manim import *
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        # Explicitly out of bounds positions
        text_left_10 = Text("Left 10").move_to(LEFT * 10)
        text_right_10 = Text("Right 10").move_to(RIGHT * 10)
        
        self.play(Write(text_left_10))
        self.play(Write(text_right_10))
        self.wait(1)
'''
    
    # Apply the improvement with debug prints
    print("\nDebugging the boundary checking implementation...")
    sg._debug_mode = True  # Add a debug flag for extra output
    fixed_explicit = sg._improve_animation_quality(test_explicit)
    
    # Print the results
    print("\nExplicit out-of-bounds test:")
    print("========================")
    print("Original code:")
    print(test_explicit)
    print("\nFixed code:")
    print(fixed_explicit)
    
    # Detailed check for each move_to call
    move_to_calls = re.findall(r'\.move_to\([^)]+\)', fixed_explicit)
    print("\nMove_to calls in fixed code:")
    for call in move_to_calls:
        print(f"  {call}")
        if "ensure_within_boundaries" in call:
            print("    ✅ Has boundary check")
        else:
            print("    ❌ Missing boundary check")

if __name__ == "__main__":
    # Run the test
    test_boundary_checking() 