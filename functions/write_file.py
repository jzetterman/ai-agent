import os
from google.genai import types

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

schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Write to a file.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file name and location for the file to be written.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to be written into the file.",
                )
            },
        ),
    )