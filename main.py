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
    model_response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {model_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {model_response.usage_metadata.candidates_token_count}")
    else:
        print(model_response.text)
        
if __name__ == "__main__":
    main()