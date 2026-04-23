import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_working_directory = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))

        valid_target_dir = os.path.commonpath([abs_working_directory, target_dir]) == abs_working_directory

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        dir_list = os.listdir(target_dir)

        print(f"Result for '{directory}'")
        for item in dir_list:
            print(f"- {item}: file_size={os.path.getsize(target_dir + "/" + item)}, is_dir={os.path.isdir(target_dir + "/" + item)}")

        return ""

    except Exception as e:
        return (f"Error: executing Python file: {e}")


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Returns a string of files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"]
    ),
)