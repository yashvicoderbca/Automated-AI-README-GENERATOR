# Part 3 — AI-Powered README Generator

**An LLM-powered tool that automatically analyzes project code and generates professional README documentation using Groq and Llama 3.
import os
from dotenv import load_dotenv
from openai import OpenAI
from code_reader import read_project_files


# Step 1: Load environment variables from the local .env file
load_dotenv()


# Step 2: Retrieve the GROQ API key from the environment variables
api_key = os.getenv("GROQ_API_KEY")


# Check whether the API key exists
if not api_key:
    print("[ERROR] GROQ_API_KEY is missing from the .env file.")
    exit()


# Step 3: Initialize the OpenAI client pointing to groq's servers
client = OpenAI(base_url="https://api.groq.com/openai/v1",api_key=api_key)


def generate_readme():
    """
    generates a professional README.md using free groq Llama-3 AI,
    
    """

    print("[INFO] Reading project source code...")

    # Read all supported project files
    code_text, file_count = read_project_files()

    # Check whether any files were found
    if file_count == 0:
        print("[ERROR] No code files were found to analyze.")
        return

    print(f"[INFO] Analyzing {file_count} files with free Llama-3 AI...")


    # Step 4: Create the prompt for the OpenAI model
    prompt = f"""
You are an expert technical writer and software architect.

Analyze the following project's source code and generate a professional,
high-quality, and comprehensive README.md file in Markdown format.

Include the following sections:

1. Project Title and Catchy Tagline
2. Overview and Purpose
3. Key Features
4. Technology Stack and Dependencies
5. Installation and Setup Guide
6. Usage Examples and Commands
7. Project Structure
8. Configuration
9. Future Improvements
10. License

Important instructions:
- Base the documentation only on the provided source code.
- Do not invent features that do not exist in the project.
- Use clean and professional Markdown.
- Include code blocks wherever useful.
- Make the README easy for beginners to understand.

Project Source Code:
--------------------
{code_text}
--------------------
"""


    try:
        # Step 5: Send the request to the OpenAI API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert technical writer. "
                        "Create clean, professional, accurate, "
                        "and well-structured Markdown documentation."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,
        )


        # Step 6: Extract the generated README content
        readme_content = response.choices[0].message.content


        # Make sure the response contains content
        if not readme_content:
            print("[ERROR] OpenAI returned an empty response.")
            return


        # Step 7: Save the generated content to README.md
        with open("README.md", "w", encoding="utf-8") as file:
            file.write(readme_content)


        print("[SUCCESS] README.md has been generated successfully!")


    except Exception as error:
        print(f"[ERROR] Failed to generate README: {error}")


# Step 8: Run the README generator when this file is executed directly
if __name__ == "__main__":
    generate_readme()
