"""
Example animations showcasing best practices for Manim

This module contains example animations that demonstrate good techniques for:
1. Proper text management (avoiding overlays)
2. Cleaning up objects when no longer needed
3. Using spatial organization
4. Progressive animations with Transforms
5. Proper timing and pacing

These examples can be used as references for the LLM to learn from.
"""

from manim import *
import numpy as np
import math

class GoodTextManagement(Scene):
    """
    Example demonstrating proper text management techniques
    to avoid overlapping text and keep the scene clean.
    """
    def construct(self):
        # Define screen regions for better organization
        title_region = UP * 3.5
        main_region = ORIGIN
        explanation_region = DOWN * 3
        
        # 1. Start with a title
        title = Text("Text Management Example", color=BLUE).move_to(title_region)
        self.play(Write(title))
        self.wait(1)
        
        # 2. Show first explanation with proper positioning
        text1 = Text("First explanation text").move_to(explanation_region)
        self.play(Write(text1))
        self.wait(2)
        
        # 3. Main demonstration - showing an object
        circle = Circle(color=RED).move_to(main_region)
        self.play(Create(circle))
        self.wait(1)
        
        # 4. Transform the first text to second text (instead of overlaying)
        text2 = Text("Second explanation text").move_to(explanation_region)
        self.play(Transform(text1, text2))
        self.wait(2)
        
        # 5. Fade out previous objects before introducing new ones in the same space
        self.play(FadeOut(circle))
        
        # 6. Add new objects in the same space after removing old ones
        square = Square(color=GREEN).move_to(main_region)
        self.play(Create(square))
        self.wait(1)
        
        # 7. Final explanation - clear previous text first
        text3 = Text("Final explanation about the square").move_to(explanation_region)
        self.play(Transform(text1, text3))  # text1 still refers to the transformed object
        self.wait(2)
        
        # 8. Clean up all objects at the end
        self.play(
            FadeOut(title),
            FadeOut(text1),  # This removes the current text (originally text1, now transformed)
            FadeOut(square)
        )
        self.wait(1)


class ProgressiveSteps(Scene):
    """
    Example demonstrating how to show progressive steps in a process
    without cluttering the screen.
    """
    def construct(self):
        # Define regions
        title_region = UP * 3.5
        step_region = ORIGIN
        formula_region = DOWN * 2
        
        # Title
        title = Text("Progressive Steps Example", color=BLUE).move_to(title_region)
        self.play(Write(title))
        self.wait(1)
        
        # Create a VGroup to manage step texts together
        step_text = Text("Step 1: Initial setup").move_to(step_region)
        self.play(Write(step_text))
        
        # Initial formula
        formula = Text("x = 5").move_to(formula_region)
        self.play(Write(formula))
        self.wait(2)
        
        # Update to step 2 - transform the text rather than creating new
        step2_text = Text("Step 2: Multiply by 2").move_to(step_region)
        self.play(Transform(step_text, step2_text))
        
        # Update the formula - transform rather than adding new text
        formula2 = Text("x × 2 = 10").move_to(formula_region)
        self.play(Transform(formula, formula2))
        self.wait(2)
        
        # Update to step 3
        step3_text = Text("Step 3: Add 7").move_to(step_region)
        self.play(Transform(step_text, step3_text))
        
        # Update the formula again
        formula3 = Text("x × 2 + 7 = 17").move_to(formula_region)
        self.play(Transform(formula, formula3))
        self.wait(2)
        
        # Final result emphasized
        self.play(
            formula.animate.set_color(GREEN),
            Flash(formula, color=GREEN, flash_radius=0.5)
        )
        self.wait(1)
        
        # Clean up
        self.play(
            FadeOut(title),
            FadeOut(step_text),
            FadeOut(formula)
        )
        self.wait(1)


class SpatialOrganization(Scene):
    """
    Example demonstrating proper spatial organization techniques.
    """
    def construct(self):
        # Define clear regions
        title_region = UP * 3.5
        left_region = LEFT * 3
        right_region = RIGHT * 3
        bottom_region = DOWN * 3
        
        # Title with proper positioning
        title = Text("Spatial Organization", color=BLUE).move_to(title_region)
        self.play(Write(title))
        self.wait(1)
        
        # Left side content
        left_title = Text("Category A", color=RED).scale(0.8).move_to(left_region + UP * 1.5)
        left_item1 = Text("• Item 1").scale(0.6).move_to(left_region)
        left_item2 = Text("• Item 2").scale(0.6).move_to(left_region + DOWN * 0.8)
        
        # Group related items together for easier management
        left_group = VGroup(left_title, left_item1, left_item2)
        self.play(Write(left_group))
        self.wait(1.5)
        
        # Right side content
        right_title = Text("Category B", color=GREEN).scale(0.8).move_to(right_region + UP * 1.5)
        right_item1 = Text("• Point 1").scale(0.6).move_to(right_region)
        right_item2 = Text("• Point 2").scale(0.6).move_to(right_region + DOWN * 0.8)
        
        # Group related items
        right_group = VGroup(right_title, right_item1, right_item2)
        self.play(Write(right_group))
        self.wait(1.5)
        
        # Bottom explanation that doesn't overlap other elements
        bottom_text = Text("Compare and contrast the categories").scale(0.7).move_to(bottom_region)
        self.play(Write(bottom_text))
        self.wait(2)
        
        # Highlight relationship with arrow
        arrow = Arrow(left_region + DOWN * 0.5, right_region + DOWN * 0.5, color=YELLOW)
        self.play(Create(arrow))
        self.wait(1)
        
        # Clean up everything at the end
        self.play(
            FadeOut(title),
            FadeOut(left_group),
            FadeOut(right_group),
            FadeOut(bottom_text),
            FadeOut(arrow)
        )
        self.wait(1)


class TimingAndPacing(Scene):
    """
    Example demonstrating proper timing and pacing in animations.
    """
    def construct(self):
        # Define regions
        title_region = UP * 3.5
        main_region = ORIGIN
        
        # Title
        title = Text("Timing & Pacing Example", color=BLUE).move_to(title_region)
        self.play(Write(title), run_time=1)  # Quick title
        self.wait(0.5)  # Short pause after title
        
        # Explanation text
        explanation = Text("Good animations match narration pace").scale(0.8).next_to(title, DOWN * 2)
        self.play(FadeIn(explanation), run_time=1)
        self.wait(2)  # Longer pause for viewer to read
        
        # Demonstrate timing patterns
        patterns = [
            "Quick transitions for simple points",
            "Longer pauses for complex concepts",
            "Emphasis on key information"
        ]
        
        demo_text = Text(patterns[0]).move_to(main_region)
        self.play(Write(demo_text), run_time=1.5)
        self.wait(1)  # Short pause for simple point
        
        # Transform to second pattern - longer pause
        demo_text2 = Text(patterns[1]).move_to(main_region)
        self.play(Transform(demo_text, demo_text2), run_time=1)
        self.wait(2.5)  # Longer pause for complex concept
        
        # Transform to third pattern with emphasis
        demo_text3 = Text(patterns[2]).move_to(main_region)
        self.play(Transform(demo_text, demo_text3), run_time=1)
        
        # Add emphasis animation
        self.play(
            demo_text.animate.set_color(YELLOW),
            Flash(demo_text)
        )
        self.wait(2)  # Pause on emphasized point
        
        # Clean conclusion
        conclusion = Text("Match timing to content complexity").scale(0.7).next_to(demo_text, DOWN * 2)
        self.play(Write(conclusion))
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(VGroup(title, explanation, demo_text, conclusion))
        )
        self.wait(1) 