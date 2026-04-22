import os
from config import MAX_CHARS

def get_file_content(working_directory, filepath):
    try:
        abs_working_directory = os.path.abspath(working_directory)

        target_file = os.path.normpath(os.path.join(abs_working_directory, filepath))

        valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory

        if not valid_target_file:
            return f'Error: Cannot read "{filepath}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{filepath}"'

        file_content_string = ""

        with open(target_file, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            if file.read(MAX_CHARS+1):
                file_content_string += f'[...File "{filepath}" truncated at {MAX_CHARS} characters]'

        return file_content_string

    except Exception as e:
        return (f"Error: executing Python file: {e}")