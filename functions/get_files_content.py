import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000

    if not file_path:
        return f'Error: File path not provided'
    
    abs_file_path = os.path.join(os.path.abspath(working_directory), file_path)
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{abs_file_path}"'

    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS]
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as err:
        return f'Error: Cannot read file'
    
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Get the content of a specified file.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Get the content of a specified file.",
                ),
            },
        ),
    )