import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types

from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    parser = argparse.ArgumentParser()
    prompt_argument_strings = []
    for value in sys.argv[1:]:
        if isinstance(value, str):
            prompt_argument_strings.append(value)

    parser.add_argument('prompt', help='Your prompt for the LLM')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    user_prompt = args.prompt
    if len(sys.argv) < 2:
        print("No prompt was provided, try again")
        sys.exit(1)

    messages = [
        genai_types.Content(role="user", parts=[genai_types.Part(text=user_prompt)]),
    ]

    client = genai.Client(api_key=api_key)
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    schema_get_files_info = genai_types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=genai_types.Schema(
            type=genai_types.Type.OBJECT,
            properties={
                "directory": genai_types.Schema(
                    type=genai_types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    schema_get_file_content = genai_types.FunctionDeclaration(
        name="get_file_content",
        description="Get the content of a specified file.",
        parameters=genai_types.Schema(
            type=genai_types.Type.OBJECT,
            properties={
                "file_path": genai_types.Schema(
                    type=genai_types.Type.STRING,
                    description="Get the content of a specified file.",
                ),
            },
        ),
    )
    schema_run_python_file = genai_types.FunctionDeclaration(
        name="run_python_file",
        description="Run a specified python file.",
        parameters=genai_types.Schema(
            type=genai_types.Type.OBJECT,
            properties={
                "file_path": genai_types.Schema(
                    type=genai_types.Type.STRING,
                    description="Run a specified python file.",
                ),
            },
        ),
    )
    schema_write_file = genai_types.FunctionDeclaration(
        name="write_file",
        description="Write to a file.",
        parameters=genai_types.Schema(
            type=genai_types.Type.OBJECT,
            properties={
                "file_path": genai_types.Schema(
                    type=genai_types.Type.STRING,
                    description="The file name and location for the file to be written.",
                ),
                "content": genai_types.Schema(
                    type=genai_types.Type.STRING,
                    description="The content to be written into the file.",
                )
            },
        ),
    )

    available_functions = genai_types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    model_response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=genai_types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    function_call_part = model_response.candidates[0].content.parts[0].function_call
    function_result = call_function(function_call_part, verbose=args.verbose)

    if function_result.parts[0].function_response.response == "":
        raise Exception(f'Fatal exception: failed to run function')
    if function_result.parts[0].function_response.response != "" and args.verbose:
        print(f"-> {function_result.parts[0].function_response.response}")
    
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {model_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {model_response.usage_metadata.candidates_token_count}")
    else:
        function_calls = model_response.function_calls
        if function_calls and len(function_calls) > 0:
            for function_call in function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(model_response.text)
        
if __name__ == "__main__":
    main()