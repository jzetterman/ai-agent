import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import call_function, available_functions
from config import MAX_ITERS

def main():
    load_dotenv()
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
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iterations = 0
    while True:
        iterations += 1
        if iterations > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            raise Exception(f"Error in generate_content: {e}")
        
def generate_content(client, messages, verbose):
    model_response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Prompt tokens: {model_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {model_response.usage_metadata.candidates_token_count}")

    if model_response.candidates:
        for candidate in model_response.candidates:
            messages.append(candidate.content)

    if not model_response.function_calls:
        return model_response.text
    
    function_responses = []
    for function_call_part in model_response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise Exception("empty function call result")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    messages.append(types.Content(role="tool", parts=function_responses))
        
if __name__ == "__main__":
    main()