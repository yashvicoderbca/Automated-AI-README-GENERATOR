# Part 1 — Secure LLM API Setup
# Environment-based API configuration with Groq
import os
from dotenv import load_dotenv
from openai import OpenAI

# Step 1: Load environment variables from .env
load_dotenv()

# Step 2: Get OpenAI API key
api_key = os.getenv("GROQ_API_KEY")

# Step 3: Validate API key
if not api_key:
    print("[ERROR] GROQ_API_KEY not found! Please check your .env file")
    exit()

# Step 4: Initialize OpenAI client
client = OpenAI(base_url="https:\\api.groq.com/openai/v1",api_key=api_key)

print("[SUCCESS] Security guard and Groq API connection ready !")
