## Part 1 — Secure Project Setup & OpenAI API Integration

This part establishes the foundation of the AI README Generator by:
- Loading environment variables securely using python-dotenv
- Validating the OpenAI API key before execution
- Initializing the OpenAI client
- Preparing the project for AI-powered documentation generation

import os
from dotenv import load_dotenv
from openai import OpenAI

# Step 1: Load environment variables from .env
load_dotenv()

# Step 2: Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Step 3: Validate API key
if not api_key:
    print("[ERROR] OpenAI API Key not found! Please check your .env file")
    exit()

# Step 4: Initialize OpenAI client
client = OpenAI(api_key=api_key)

print("[SUCCESS] Security guard and OpenAI API connection ready!")
