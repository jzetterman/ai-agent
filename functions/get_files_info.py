import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory == None:
        directory = os.path.join(working_directory, ".")
    else:
        directory = os.path.join(working_directory, directory)
        
    if not os.path.abspath(directory).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    # Create a list of directory contents
    try:
        dir_content = os.listdir(directory)
    except Exception as err:
        return f"Error: {err}"

    item_info = {}
    result = []
    for item in dir_content:
        item_info["name"] = item
        try:
            item_info["file_size"] = os.path.getsize(os.path.join(directory, item))
            item_info["is_dir"] = os.path.isdir(os.path.join(directory, item))
        except Exception as err:
            return f"Error: {err}"
        
        result.append(f"- {item_info["name"]}: file_size={item_info["file_size"]} bytes, is_dir={item_info["is_dir"]}")
        
    return "\n".join(result)

schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )