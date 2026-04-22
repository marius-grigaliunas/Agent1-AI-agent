from ntpath import isdir
import os

def write_file(working_directory, filepath, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)

        target_file = os.path.normpath(os.path.join(abs_working_directory, filepath))

        valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory

        if not valid_target_file:
            return f'Error: Cannot write to "{filepath}" as it is outside the permitted working directory'
        elif os.path.isdir(target_file):
            return f'Error: Cannot write to "{filepath}" as it is a directory'

        parent_dirs = os.path.dirname(target_file)

        if len(parent_dirs) > 0:
            os.makedirs(parent_dirs, exist_ok=True)

        with open(target_file, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{filepath}" ({len(content)} characters written)'

    except Exception as e:
        return (f"Error: executing Python file: {e}")