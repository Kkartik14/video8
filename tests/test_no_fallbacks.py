#!/usr/bin/env python3
"""
Test script to verify that errors are properly raised without fallbacks.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.llm_handler import LLMHandler
from backend.groq_handler import GroqHandler

def test_narration_script_error_handling():
    """Test narration script generation error handling."""
    try:
        handler = LLMHandler()
        # Deliberately remove API key to cause an error
        handler.api_key = None
        
        # This should raise an exception
        script = handler.generate_narration_script("Test prompt")
        print("ERROR: No exception was raised when API key is missing")
    except Exception as e:
        print(f"SUCCESS: Exception properly raised: {str(e)}")

def test_manim_code_error_handling():
    """Test Manim code generation error handling."""
    try:
        handler = LLMHandler()
        # Simulate an error in the response
        code = handler.validate_and_fix_code("This is not valid Manim code")
        print("ERROR: No exception was raised for invalid code")
    except Exception as e:
        print(f"SUCCESS: Exception properly raised: {str(e)}")

def test_groq_error_handling():
    """Test Groq handler error handling."""
    try:
        handler = GroqHandler()
        # Deliberately remove API key to cause an error
        handler.api_key = None
        
        # This should raise an exception
        script = handler.generate_narration_script("Test prompt")
        print("ERROR: No exception was raised when API key is missing")
    except Exception as e:
        print(f"SUCCESS: Exception properly raised: {str(e)}")

def print_separator():
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    print("Testing error handling without fallbacks...")
    print_separator()
    
    print("Testing LLMHandler narration script generation:")
    test_narration_script_error_handling()
    print_separator()
    
    print("Testing LLMHandler Manim code validation:")
    test_manim_code_error_handling()
    print_separator()
    
    print("Testing GroqHandler error handling:")
    test_groq_error_handling()
    print_separator()
    
    print("Tests completed.") 