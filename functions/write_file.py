import os

def write_file(working_directory, file_path, content):
    if not file_path:
        return f'Error: File path not provided'
    
    abs_file_path = os.path.join(os.path.abspath(working_directory), file_path)
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    abs_dir_path = os.path.dirname(abs_file_path)
    if not os.path.exists(abs_dir_path):
        try:
            os.makedirs(abs_dir_path)
        except Exception as err:
            return f"Error: Unable to create directory structure {abs_dir_path}"

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
    except Exception as err:
        return f'Error: Unable to write file {abs_file_path}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'