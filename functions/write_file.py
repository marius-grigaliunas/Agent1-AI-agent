from ntpath import isdir
import os

from google.genai import types

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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="overwrites the specified file, relative to the working directory, with the specified contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath" : types.Schema(
                type= types.Type.STRING,
                description="File path to list the contents of, relative to the working directory (default is the working directory itself)"
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description="string of contents to overwrite the file with."
            )
        },
        required=["filepath", "content"]
    )
)