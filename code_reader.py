"""
============================================================
             PROJECT: AUTOMATED AI README GENERATOR ENGINE
             MODULE:  code_reader.py
             DESCRIPTION: TRAVERSES DIRECTORY TREE, IGNORES BINARY/ SENSITIVE FILES, AND READS CODE SAFELY
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
    '.vscode',
    '.pytest_cache'
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
    # and returned combined code with safety truncation.

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
                    # strict character limit safely check 
                    if len(combined_code) + len(content) > max_chars:
                        combined_code += f"\n\n=== FILE: {file_path}(PARTICAL/TRUNCATED)===\n\n"
                        remaining_space = max_chars - len(combined_code)
                        combined_code += "\n\n.....[TRUNCATED : SOURCE CODE EXCEEDED MAX SAFETY THRESHOLD]........"
                        return combined_code, file_count

                combined_code += (
                    f"\n\n======================================"
                    f"FILE: {file_path}"
                    f"======================================\n\n"
                )

                combined_code += content
                file_count += 1

            except (UnicodeDecodeError,PermissionError,OSError):
                # safely ignore binary or protected files
                continue
            

    return combined_code, file_count


if __name__ == "__main__":
    print("Scanning project files....")

    code, count = read_project_files()
    print(f"[SUCCESS] SCANNED {count} files ({len(code)}total characters....)")

    
