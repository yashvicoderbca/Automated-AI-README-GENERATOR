# ====================================================================================================================================================
# Automated Code Scanner Testing

# Ensuring Secure, Reliable, and Efficient Project File Analysis
#======================================================================================================================================================
import os
import tempfile

from code_reader import read_project_files


def test_read_project_files_executes():
    """
    Ensure the project scanner executes successfully and discovers
    at least one project file without raising unexpected errors.
    """

    code_text, file_count = read_project_files(".")

    assert file_count > 0
    assert isinstance(code_text, str)


def test_sensitive_files_ignored():
    """
    Ensure sensitive files such as .env are not included
    in the generated project content.
    """

    with tempfile.TemporaryDirectory() as temp_dir:

        # Create a normal source file.
        source_file = os.path.join(temp_dir, "app.py")

        with open(
            source_file,
            "w",
            encoding="utf-8",
        ) as file:
            file.write("print('Hello World')")

        # Create a sensitive .env file.
        env_file = os.path.join(temp_dir, ".env")

        with open(
            env_file,
            "w",
            encoding="utf-8",
        ) as file:
            file.write("GROQ_API_KEY=secret-key")

        code_text, file_count = read_project_files(temp_dir)

        # The normal source file should be discovered.
        assert file_count == 1

        assert "Hello World" in code_text

        # Sensitive .env content must never appear.
        assert "GROQ_API_KEY" not in code_text
        assert "secret-key" not in code_text

        # .env itself must not appear in the scanner output.
        assert ".env" not in code_text


def test_max_chars_truncation():
    """
    Ensure the scanner respects the configured character limit.
    """

    with tempfile.TemporaryDirectory() as temp_dir:

        # Create a large source file.
        large_file = os.path.join(
            temp_dir,
            "large_file.py",
        )

        with open(
            large_file,
            "w",
            encoding="utf-8",
        ) as file:
            file.write("A" * 5000)

        small_limit = 500

        code_text, file_count = read_project_files(
            temp_dir,
            max_chars=small_limit,
        )

        # The returned content should never exceed max_chars.
        assert len(code_text) <= small_limit

        # At least part of the file should have been processed.
        assert isinstance(code_text, str)


