from google.genai import types as genai_types
from functions.get_files_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    function_name = function_call_part.name
    if function_name in function_map:
        actual_function = function_map[function_name]
        function_result = actual_function(**function_call_part.args, working_directory="./calculator")
    else:
        return genai_types.Content(
        role="tool",
        parts=[
            genai_types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )

    return genai_types.Content(
        role="tool",
        parts=[
            genai_types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
