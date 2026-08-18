"""
============================================================
PROJECT: AUTOMATED AI README GENERATOR ENGINE
MODULE: code_reader.py

DESCRIPTION:
    Recursively traverses a project directory, skips sensitive,
    binary, and irrelevant files, and safely reads source code
    with a configurable character limit.
============================================================
"""

import os


# Directories that should be ignored during project scanning.
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
    ".vscode",
    ".pytest_cache",
    ".venv",
    "venv",
}


# Specific files that should be ignored to protect sensitive
# information and avoid processing unnecessary files.
IGNORE_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "secrets.json",
    "package-lock.json",
    ".DS_Store",
    "test_setup.py",
}


# File extensions that are normally binary or not useful
# for source-code analysis.
IGNORE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".webp",
    ".bmp",
    ".svg",
    ".pyc",
    ".pyo",
    ".class",
    ".exe",
    ".dll",
    ".so",
}


def read_project_files(root_dir=".", max_chars=100000):
    """
    Recursively read relevant project files and combine their contents.

    Args:
        root_dir (str): Root directory of the project.
        max_chars (int): Maximum number of characters to return.

    Returns:
        tuple:
            combined_code (str): Combined source code from readable files.
            file_count (int): Number of successfully read files.

    Raises:
        ValueError: If root_dir is invalid or max_chars is not positive.
    """

    # Validate the maximum character limit.
    if max_chars <= 0:
        raise ValueError("max_chars must be greater than 0")

    # Validate the project directory.
    if not os.path.isdir(root_dir):
        raise ValueError(f"Invalid project directory: {root_dir}")

    combined_code = ""
    file_count = 0

    # Traverse the directory tree recursively.
    for root, dirs, files in os.walk(root_dir, followlinks=False):

        # Remove ignored directories from traversal.
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORE_DIRS
        ]

        for file_name in files:

            # Normalize the filename for case-insensitive checks.
            file_lower = file_name.lower()

            # Skip explicitly ignored files.
            if file_name in IGNORE_FILES or file_lower in IGNORE_FILES:
                continue

            # Skip binary and irrelevant file types.
            _, extension = os.path.splitext(file_lower)

            if extension in IGNORE_EXTENSIONS:
                continue

            file_path = os.path.join(root, file_name)

            try:
                # Read the file as UTF-8 text.
                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="strict",
                ) as file:
                    content = file.read()

            except (UnicodeDecodeError, PermissionError, OSError):
                # Skip files that cannot be safely read as text.
                continue

            # Add a clear separator before each file.
            file_header = (
                "\n\n"
                "======================================\n"
                f"FILE: {file_path}\n"
                "======================================\n\n"
            )

            # Calculate how much space is still available.
            remaining_space = max_chars - len(combined_code)

            # Stop if there is no space left for another file.
            if remaining_space <= len(file_header):
                combined_code += (
                    "\n\n"
                    "[TRUNCATED: SOURCE CODE EXCEEDED "
                    "THE MAXIMUM CHARACTER LIMIT]"
                )
                return combined_code[:max_chars], file_count

            # Add the file header.
            combined_code += file_header
            remaining_space = max_chars - len(combined_code)

            # If the complete file fits, add it normally.
            if len(content) <= remaining_space:
                combined_code += content
                file_count += 1
                continue

            # If the file is too large, add only the portion that fits.
            truncated_message = (
                "\n\n"
                "[TRUNCATED: FILE CONTENT EXCEEDED "
                "THE MAXIMUM CHARACTER LIMIT]"
            )

            available_content_space = (
                remaining_space - len(truncated_message)
            )

            if available_content_space > 0:
                combined_code += content[:available_content_space]
                combined_code += truncated_message

            # The character limit has been reached.
            return combined_code[:max_chars], file_count

    return combined_code[:max_chars], file_count


if __name__ == "__main__":
    print("Scanning project files...")

    try:
        code, count = read_project_files()

        print(
            f"[SUCCESS] Scanned {count} files "
            f"({len(code)} total characters)"
        )

    except ValueError as error:
        print(f"[ERROR] {error}")
