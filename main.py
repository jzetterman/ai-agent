import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    client = genai.Client(api_key=api_key)
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
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
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )
    model_response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    
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