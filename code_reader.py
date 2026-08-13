"""
============================================================
             PROJECT PART 2 — CODE READER ENGINE
============================================================

Purpose:
--------
Recursively scans the project directory, filters out
sensitive, unnecessary, and binary files, and consolidates
the readable source code into a single text representation.

Key Features:
------------
• Recursively scans project files and subdirectories
• Ignores sensitive files such as .env
• Skips unnecessary directories such as venv, .git,
  node_modules, and __pycache__
• Filters out binary/image files
• Reads text files safely using UTF-8 encoding
• Combines source code from multiple files into one output
• Tracks the number of successfully processed files

Project:
--------
AI-Powered Code Analysis / Repository Understanding System

Part:
-----
Part 2 — Repository Code Reader

============================================================
"""
import os

# Directories that should be ignored during scanning
IGNORE_DIRS = {
    '.git',
    '__pycache__',
    'node_modules',
    'venv',
    '.env',
    'build',
    'dist',
    '.vscode'
}

# Specific files that should be ignored
# to protect sensitive data and save bandwidth
IGNORE_FILES = {
    '.env',
    'package-lock.json',
    '.DS_Store',
    'test_setup.py'
}


def read_project_files(root_dir='.'):
    # Traverses the project directory tree,
    # ignores non-relevant files and folders,
    # and consolidates all source code into a single string.

    combined_code = ""
    file_count = 0

    # Traverse the directory tree recursively
    for root, dirs, files in os.walk(root_dir):

        # Prune ignored directories in place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:

            # Skip ignored files or binary assets
            if file in IGNORE_FILES or file.endswith(
                ('.png', '.jpg', '.jpeg', '.ico', '.pyc')
            ):
                continue

            file_path = os.path.join(root, file)

            try:
                # Read file contents with UTF-8 encoding
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                combined_code += (
                    f"\n\n======================================"
                    f"FILE: {file_path}"
                    f"======================================\n\n"
                )

                combined_code += content
                file_count += 1

            except Exception:
                # Skip files that cannot be decoded as plain text
                continue

    return combined_code, file_count


if __name__ == "__main__":
    print("Scanning project files....")

    code_text, count = read_project_files()

    print("[SUCCESS] CODE READER ENGINE READY")
    print(f"TOTAL FILES READ: {count}")
    print(f"TOTAL CHARACTERS PROCESSED: {len(code_text)}")
