"""
============================================================
             PROJECT PART 2 — CODE READER ENGINE
============================================================

import os

# Directories that should be ignored during scanning
IGNORE_DIRS = {
    '.git',
    '__pycache__',
    'node_modules',
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


def read_project_files(root_dir='.',max_chars = 100000):
    # Traverses the project directory tree,
    # ignores non-relevant files and folders,
    # and consolidates  source code into a single string and safely truncates if it exceeds max_chars limit.

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
            # Edge-case safeguard: truncate if character count exceeds limit
            if len(combined_code)> max_chars:
                combined_code = combined_code[:max_chars]+ "\n\n....[TRUNCATED: SOURCE CODE EXCEEDS MAX SAFETY THRESHOLD]....."

    return combined_code, file_count


if __name__ == "__main__":
    print("Scanning project files....")

    code_text, count = read_project_files()

    print("[SUCCESS] CODE READER ENGINE READY")
    print(f"TOTAL FILES READ: {count}")
    print(f"TOTAL CHARACTERS PROCESSED: {len(code_text)}")
