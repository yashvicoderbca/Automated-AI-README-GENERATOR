# ============================================================
# Part 4 — CLI Automation & Custom Documentation
# A flexible command-line interface for AI-powered README generation
# ============================================================

import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from code_reader import read_project_files


# Load environment variables from the local .env file.
load_dotenv()


# Retrieve the Groq API key securely from environment variables.
api_key = os.getenv("GROQ_API_KEY")


# Validate that the required API key is available before starting.
if not api_key:
    print("[ERROR] GROQ_API_KEY is missing from the .env file.")
    exit()


# Initialize the OpenAI-compatible client for Groq's API.
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)


def setup_cli_args():
    """
    Configure command-line arguments to provide flexible
    input and output options for the README generator.
    """

    parser = argparse.ArgumentParser(
        description="Automated AI README Generator CLI Tool"
    )

    # Allow users to specify the project directory to analyze.
    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Target project directory path (default: current directory '.')"
    )

    # Allow users to customize the generated documentation filename.
    parser.add_argument(
        "--output",
        type=str,
        default="README.md",
        help="Output Markdown file name (default: 'README.md')"
    )

    # Allow users to choose the desired documentation style.
    parser.add_argument(
        "--style",
        type=str,
        choices=["detailed", "minimal", "beginner"],
        default="detailed",
        help="Documentation style: detailed, minimal, or beginner"
    )

    return parser.parse_args()


def get_style_instructions(style_choice):
    """
    Return documentation instructions based on the
    style selected through the CLI.
    """

    if style_choice == "minimal":
        return (
            "Keep the documentation concise, clean, and "
            "straight to the point."
        )

    elif style_choice == "beginner":
        return (
            "Write in an easy-to-understand, beginner-friendly tone "
            "with clear step-by-step explanations."
        )

    else:
        return (
            "Provide a comprehensive, professional, and "
            "architecturally detailed technical guide."
        )


def generate_readme():
    """
    Analyze the target project and generate a professional
    README file based on the selected CLI options.
    """

    # Parse user-provided command-line arguments.
    args = setup_cli_args()

    print(f"[INFO] Scanning directory: '{args.dir}'...")

    # Read and combine supported project source files.
    code_text, file_count = read_project_files(args.dir)

    # Stop execution if no source files are available.
    if file_count == 0:
        print("[ERROR] No code files found to analyze.")
        return

    print(
        f"[INFO] Analyzing {file_count} files using "
        f"Groq Llama 3.3 ({args.style.upper()} style)..."
    )

    # Generate instructions according to the selected style.
    style_instructions = get_style_instructions(args.style)

    # Build a structured prompt for the LLM.
    prompt = f"""
You are an expert technical writer and software architect.

Analyze the following project source code and generate a professional
README.md file in clean Markdown format.

Documentation style:
{style_instructions}

Include the following sections:

1. Project Title and Catchy Tagline
2. Overview and Purpose
3. Key Features
4. Technology Stack and Dependencies
5. Installation and Setup Guide
6. Usage Examples and Commands

Important:
- Base the documentation only on the provided source code.
- Do not invent features that do not exist.
- Use professional and beginner-friendly Markdown.
- Include code blocks where useful.

Project Source Code:
--------------------
{code_text}
--------------------
"""

    try:
        # Send the project analysis request to the Groq LLM.
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You create clean, professional, accurate, "
                        "and well-structured Markdown documentation."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        # Extract the generated README content from the API response.
        readme_content = response.choices[0].message.content

        # Validate that the model returned usable content.
        if not readme_content:
            print("[ERROR] The AI returned an empty response.")
            return

        # Save the generated documentation to the requested output file.
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(readme_content)

        print(
            f"[SUCCESS] Documentation saved successfully "
            f"to '{args.output}'!"
        )

    except Exception as error:
        # Handle API or file-related errors gracefully.
        print(f"[ERROR] Failed to generate README: {error}")


# Run the README generator only when this file is executed directly.
if __name__ == "__main__":
    generate_readme()
