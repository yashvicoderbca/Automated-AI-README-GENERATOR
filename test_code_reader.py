# ====================================================================================================================================================
# AUTOMATED UNIT TESTS FOR code_reader.py USING pytest
#======================================================================================================================================================
import pytest
from code_reader import read_project_files


def test_read_project_files_executes():
    """
    Ensure the project scanner executes successfully and discovers
    at least one project file without raising any unexpected errors.
    """
    code_text, file_count = read_project_files(".")

    assert file_count > 0
    assert isinstance(code_text, str)


def test_sensitive_files_ignored():
    """
    Ensure sensitive configuration files, such as .env files,
    are excluded from the generated project content.
    
    This prevents secrets, API keys, credentials, and other
    environment-specific configuration values from being exposed.
    """
    code_text, _ = read_project_files(".")

    # Construct the expected file headers dynamically so that this
    # test file does not accidentally include the exact strings
    # being checked in the scanner output.
    env_header = "=== FILE: " + "env ==="
    dot_env_header = "=== FILE: " + ".\\.env ==="

    assert env_header not in code_text
    assert dot_env_header not in code_text


def test_max_chars_truncation():
    """
    Ensure the scanner respects the configured character limit
    when the generated project content exceeds max_chars.
    """
    small_limit = 500

    code_text, _ = read_project_files(".", max_chars=small_limit)

    # Allow a small additional buffer for the truncation message
    # or metadata appended by the file-reading implementation.
    assert len(code_text) <= small_limit + 200





