"""
Prompt Optimizer for Animation Generation

This module enhances user prompts to generate more detailed, comprehensive,
and educational animations.
"""

import os
import requests
import json
import re
from typing import Dict, Any, Optional

class PromptOptimizer:
    def __init__(self):
        """Initialize the prompt optimizer."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            # Try to use Groq if Anthropic is not available
            self.api_key = os.getenv("GROQ_API_KEY")
            self.api_type = "groq"
        else:
            self.api_type = "anthropic"
            
        if not self.api_key:
            raise ValueError("Neither ANTHROPIC_API_KEY nor GROQ_API_KEY environment variables are set")
            
        # System prompt for enhancing user prompts
        self.system_prompt = """You are an expert at enhancing user prompts for educational animation generation. 
Your task is to take a brief user prompt and expand it into a detailed, comprehensive instruction 
that will result in a highly educational and thorough animation.

Here's what you need to do:
1. Identify the core concept or topic in the user's prompt
2. Add specific details about what aspects of the topic should be covered
3. Suggest visual elements that would enhance understanding
4. Specify a logical sequence for explaining the concept
5. Include suggestions for specific examples or analogies that could be used
6. Ensure the enhanced prompt asks for a complete, thorough explanation
7. Add guidance on what level of detail is appropriate

The goal is to transform a brief prompt like "explain photosynthesis" into a detailed prompt 
that will guide the creation of a comprehensive, visually rich, and educational animation.
"""

    def enhance_prompt(self, user_prompt: str) -> str:
        """
        Enhance a user prompt to generate more detailed and comprehensive animations.
        
        Args:
            user_prompt: The original user prompt
            
        Returns:
            An enhanced prompt with more detail and guidance
        """
        if not user_prompt or len(user_prompt.strip()) < 3:
            raise ValueError("User prompt is too short or empty")
        
        # Build the enhancement request
        enhancement_request = f"""Please enhance the following prompt for educational animation generation:

USER PROMPT: {user_prompt}

Please create a detailed, comprehensive version of this prompt that will result in a thorough, 
educational animation. The enhanced prompt should:

1. Specify what aspects of the topic should be covered
2. Suggest visual elements to include
3. Outline a logical sequence for explaining the concept
4. Include specific examples or analogies to use
5. Request a thorough and complete explanation
6. Provide guidance on the appropriate level of detail

ENHANCED PROMPT:"""

        # Make the API call based on available API
        if self.api_type == "anthropic":
            return self._enhance_with_anthropic(enhancement_request)
        else:
            return self._enhance_with_groq(enhancement_request)
            
    def _enhance_with_anthropic(self, enhancement_request: str) -> str:
        """Use Anthropic Claude to enhance the prompt."""
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-2.0",
            "prompt": f"\n\nHuman: {self.system_prompt}\n\n{enhancement_request}\n\nAssistant:",
            "max_tokens_to_sample": 1500,
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
        enhanced_prompt = result.get("completion", "")
        
        if not enhanced_prompt:
            raise Exception("Failed to generate an enhanced prompt")
            
        return enhanced_prompt.strip()
    
    def _enhance_with_groq(self, enhancement_request: str) -> str:
        """Use Groq to enhance the prompt."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": enhancement_request}
            ],
            "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
            "max_tokens": 1500,
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
        enhanced_prompt = result["choices"][0]["message"]["content"].strip()
        
        if not enhanced_prompt:
            raise Exception("Failed to generate an enhanced prompt")
            
        return enhanced_prompt 