===============================================================================================================================================================

PROJECT - AUTOMATED AI README GENERATOR ENGINE
FILE - main.py
DESCRIPTION - CLI-DRIVEN DOCUMENTATION GENERATOR POWERED BY GROQ Llama-3 features production logging, CLI options, and token safety limits.

===============================================================================================================================================================
import os
import argparse
import logging

from dotenv import load_dotenv
from openai import OpenAI
from code_reader import read_project_files


# Configure production-grade application logging.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("AI_README_Generator")


# Load environment variables from the local .env file.
load_dotenv()


# Retrieve the Groq API key securely from environment variables.
api_key = os.getenv("GROQ_API_KEY")


# Validate that the required API key is available before starting.
if not api_key:
    logger.error("GROQ_API_KEY is missing from the .env file.")
    raise SystemExit(1)


# Initialize the OpenAI-compatible client for Groq's API.
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
)


def setup_cli_args():
    """
    Configure command-line arguments for the README generator.
    """

    parser = argparse.ArgumentParser(
        description="Production-grade AI README Generator CLI Tool"
    )

    # Allow users to specify the project directory to analyze.
    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Target project directory path (default: current directory '.')",
    )

    # Allow users to customize the generated README filename.
    parser.add_argument(
        "--output",
        type=str,
        default="README.md",
        help="Output Markdown file name (default: 'README.md')",
    )

    # Allow users to choose the desired documentation style.
    parser.add_argument(
        "--style",
        type=str,
        choices=["detailed", "minimal", "beginner"],
        default="detailed",
        help="Documentation style: detailed, minimal, or beginner",
    )

    # Protect the application from sending an excessively large
    # amount of source code to the language model.
    parser.add_argument(
        "--max-chars",
        type=int,
        default=100000,
        help="Maximum source-code character limit (default: 100,000)",
    )

    return parser.parse_args()


def get_style_instructions(style_choice):
    """
    Return documentation instructions based on the selected style.
    """

    if style_choice == "minimal":
        return (
            "Keep the documentation concise, clean, professional, "
            "and focused only on the most important information."
        )

    elif style_choice == "beginner":
        return (
            "Write in an easy-to-understand, beginner-friendly tone "
            "with clear step-by-step explanations and practical examples."
        )

    else:
        return (
            "Provide a comprehensive, professional, technically accurate, "
            "and architecturally detailed technical guide."
        )


def generate_readme():
    """
    Analyze a software project and generate a professional README.md file.
    """

    # Parse user-provided command-line arguments.
    args = setup_cli_args()

    logger.info("Scanning project directory: '%s'...", args.dir)

    # Read and combine supported project source files.
    code_text, file_count = read_project_files(
        args.dir,
        max_chars=args.max_chars,
    )

    # Stop execution if no source files are available.
    if file_count == 0:
        logger.error("No supported source files were found to analyze.")
        return

    logger.info(
        "Successfully read %d files (%d total characters).",
        file_count,
        len(code_text),
    )

    logger.info(
        "Analyzing source code using Groq Llama 3.3 (%s style)...",
        args.style.upper(),
    )

    # Generate instructions according to the selected documentation style.
    style_instructions = get_style_instructions(args.style)

    # Build a structured prompt for the language model.
    prompt = f"""
You are an expert technical writer, software architect,
and developer documentation specialist.

Analyze the following project source code and generate a professional
README.md file in clean Markdown format.

Documentation style:
{style_instructions}

Include the following sections when they can be supported by the
provided source code:

1. Project Title and Catchy Tagline
2. Overview and Purpose
3. Key Features
4. Technology Stack and Dependencies
5. Project Structure
6. Installation and Setup Guide
7. Configuration and Environment Variables
8. Usage Examples and Commands
9. Important Notes or Limitations

Important requirements:

- Base the documentation ONLY on the provided source code.
- Do not invent features, commands, dependencies, APIs, or configuration.
- If information is unavailable, do not fabricate it.
- Use professional, technically accurate Markdown.
- Keep explanations clear enough for developers of different experience levels.
- Include code blocks where useful.
- Preserve the actual commands and filenames found in the project.
- Do not mention that you are an AI.
- Return only the final README content.

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
                        "well-structured, and maintainable Markdown "
                        "documentation for software projects."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,
        )

        # Extract the generated README content from the API response.
        readme_content = response.choices[0].message.content

        if not readme_content:
            logger.error("The AI model returned an empty README.")
            return

        # Save the generated documentation to the requested output file.
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(readme_content)

        logger.info(
            "README successfully generated and saved to '%s'.",
            args.output,
        )

    except Exception as error:
        # Log the actual exception object.
        # This fixes the original "e is not defined" error.
        logger.exception(
            "Failed to generate README due to an API or system error: %s",
            error,
        )


# Run the README generator only when this file is executed directly.
if __name__ == "__main__":
    generate_readme()

