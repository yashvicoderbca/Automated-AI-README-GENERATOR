#===============================================================================================================================================================

# AI-Powered README Generator

# Transform Your Codebase into Clear, Professional Documentation

# An intelligent automation tool that analyzes a software project's source code and generates a structured, professional `README.md` using AI. It scans the project, securely ignores sensitive files, detects an available AI model, and creates documentation based on the actual codebase.

# **Key Highlights**

# 🤖 AI-powered README generation
# 📂 Automatic project source-code scanning
# 🔐 Sensitive file protection
# ⚙️ Multiple documentation styles
 # 📏 Configurable source-code limits
 # 🚀 Simple command-line interface
 #📝 Automatically generates and saves `README.md`

# Built for developers and remote engineering teams who want to turn code into high-quality documentation quickly and consistently.**

#===============================================================================================================================================================
import os
import argparse
import logging

from dotenv import load_dotenv
from openai import OpenAI
from code_reader import read_project_files


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("AI_README_Generator")


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    logger.error(
        "GROQ_API_KEY is missing. Please add it to your .env file."
    )
    raise SystemExit(1)


# ============================================================
# GROQ CLIENT
# ============================================================

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
)


# ============================================================
# MODEL CONFIGURATION
# ============================================================

# Preferred models are checked dynamically against the models
# available to the current Groq API key.
PREFERRED_MODELS = [
    "openai/gpt-oss-120b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]


def get_available_model():
    """
    Find the first available model from our preferred model list.

    This prevents the application from crashing simply because
    a particular model is unavailable for the current API key.
    """

    try:
        logger.info("Checking available Groq models...")

        models_response = client.models.list()

        available_models = {
            model.id
            for model in models_response.data
        }

        logger.info(
            "Found %d models available for this API key.",
            len(available_models),
        )

        for model_name in PREFERRED_MODELS:
            if model_name in available_models:
                logger.info(
                    "Selected Groq model: %s",
                    model_name,
                )
                return model_name

        logger.error(
            "None of the preferred models are available."
        )

        logger.error(
            "Available models are: %s",
            ", ".join(sorted(available_models)),
        )

        return None

    except Exception as error:
        logger.exception(
            "Failed to retrieve available Groq models: %s",
            error,
        )
        return None


# ============================================================
# CLI ARGUMENTS
# ============================================================

def setup_cli_args():
    """
    Configure command-line arguments for the README generator.
    """

    parser = argparse.ArgumentParser(
        description="Production-grade AI README Generator CLI Tool"
    )

    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help=(
            "Target project directory path "
            "(default: current directory '.')"
        ),
    )

    parser.add_argument(
        "--output",
        type=str,
        default="README.md",
        help=(
            "Output Markdown file name "
            "(default: 'README.md')"
        ),
    )

    parser.add_argument(
        "--style",
        type=str,
        choices=["detailed", "minimal", "beginner"],
        default="detailed",
        help=(
            "Documentation style: detailed, minimal, "
            "or beginner"
        ),
    )

    parser.add_argument(
        "--max-chars",
        type=int,
        default=100000,
        help=(
            "Maximum source-code character limit "
            "(default: 100,000)"
        ),
    )

    return parser.parse_args()


# ============================================================
# DOCUMENTATION STYLE
# ============================================================

def get_style_instructions(style_choice):
    """
    Return documentation instructions based on the selected style.
    """

    if style_choice == "minimal":
        return (
            "Keep the documentation concise, clean, professional, "
            "and focused only on the most important information."
        )

    if style_choice == "beginner":
        return (
            "Write in an easy-to-understand, beginner-friendly tone "
            "with clear step-by-step explanations and practical examples."
        )

    return (
        "Provide a comprehensive, professional, technically accurate, "
        "and architecturally detailed technical guide."
    )


# ============================================================
# PROMPT GENERATION
# ============================================================

def build_prompt(code_text, style):
    """
    Build the README generation prompt.
    """

    style_instructions = get_style_instructions(style)

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
- Keep explanations clear enough for developers of different
  experience levels.
- Include code blocks where useful.
- Preserve actual commands and filenames found in the project.
- Do not mention that you are an AI.
- Return ONLY the final README content.
- Do not wrap the entire README inside a Markdown code block.

Project Source Code:
--------------------
{code_text}
--------------------
"""

    return prompt


# ============================================================
# README GENERATION
# ============================================================

def generate_readme():
    """
    Analyze a software project and generate a professional README.md.
    """

    args = setup_cli_args()

    # --------------------------------------------------------
    # Validate source directory
    # --------------------------------------------------------

    if not os.path.isdir(args.dir):
        logger.error(
            "Project directory does not exist: '%s'",
            args.dir,
        )
        return

    if args.max_chars <= 0:
        logger.error(
            "--max-chars must be greater than 0."
        )
        return

    # --------------------------------------------------------
    # Read project files
    # --------------------------------------------------------

    logger.info(
        "Scanning project directory: '%s'...",
        args.dir,
    )

    try:
        code_text, file_count = read_project_files(
            args.dir,
            max_chars=args.max_chars,
        )

    except Exception as error:
        logger.exception(
            "Failed to read project files: %s",
            error,
        )
        return

    if file_count == 0:
        logger.error(
            "No supported source files were found to analyze."
        )
        return

    logger.info(
        "Successfully read %d files (%d total characters).",
        file_count,
        len(code_text),
    )

    # --------------------------------------------------------
    # Select available model
    # --------------------------------------------------------

    model = get_available_model()

    if not model:
        logger.error(
            "No compatible Groq model is available for this API key."
        )
        return

    logger.info(
        "Analyzing source code using Groq model '%s' (%s style)...",
        model,
        args.style.upper(),
    )

    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    prompt = build_prompt(
        code_text=code_text,
        style=args.style,
    )

    # --------------------------------------------------------
    # Call Groq API
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(
            model=model,
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
            temperature=0.3,
        )

        # ----------------------------------------------------
        # Extract response
        # ----------------------------------------------------

        if not response.choices:
            logger.error(
                "Groq returned no response choices."
            )
            return

        readme_content = response.choices[0].message.content

        if not readme_content or not readme_content.strip():
            logger.error(
                "The AI model returned an empty README."
            )
            return

        readme_content = readme_content.strip()

        # ----------------------------------------------------
        # Create output directory if required
        # ----------------------------------------------------

        output_directory = os.path.dirname(
            os.path.abspath(args.output)
        )

        os.makedirs(
            output_directory,
            exist_ok=True,
        )

        # ----------------------------------------------------
        # Save README
        # ----------------------------------------------------

        with open(
            args.output,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(readme_content)
            file.write("\n")

        logger.info(
            "README successfully generated and saved to '%s'.",
            args.output,
        )

        logger.info(
            "README size: %d characters.",
            len(readme_content),
        )

    # --------------------------------------------------------
    # API errors
    # --------------------------------------------------------

    except Exception as error:

        logger.exception(
            "Failed to generate README due to an API or "
            "system error: %s",
            error,
        )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    generate_readme()
