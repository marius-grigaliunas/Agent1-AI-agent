
from ast import arg
import os
import subprocess

from google.genai import types


def run_python_file(working_directory, filepath, args=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)

        target_file = os.path.normpath(os.path.join(abs_working_directory, filepath))

        valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory

        if not valid_target_file:
            return f'Error: Cannot execute "{filepath}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: "{filepath}" does not exist or is not a regular file'
        elif not target_file.endswith(".py"):
            return f'Error: "{filepath}" is not a Python file'

        command_string = ["python", target_file]
        if args: 
            command_string.extend(args)

        completed_command = subprocess.run(command_string, capture_output=True, text=True, timeout=30)

        output_string = ""
        if completed_command.returncode != 0:
            output_string += f"Process exited with code {completed_command.returncode}\n"
        
        if len(completed_command.stdout) > 0:
            output_string += f"STDOUT: {completed_command.stdout}\n"
        elif len(completed_command.stderr) > 0:
            output_string += f"STDERR: {completed_command.stderr}\n"
        else:
            output_string += "No output produced.\n"

        return output_string  

        
    except Exception as e:
        return (f"Error: executing Python file: {e}")

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the specified python file, relative to the working directory, and any stated arguments returns and output string, consisting of the return code (if nonzero), STDOUT and STDERR",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath" : types.Schema(
                type= types.Type.STRING,
                description="File path to list the contents of, relative to the working directory (default is the working directory itself)"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments passed to the Python file."
            )
        },
        required=["filepath"]
    )
)