import os


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

    except:
        raise Exception("Error: Something went wrong.")