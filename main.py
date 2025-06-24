import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    prompt_string = sys.argv
    if len(sys.argv) < 2:
        print("No prompt was provided, try again")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    prompt = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt_string
    )
    print(prompt.text)
    print(f"Prompt tokens: {prompt.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {prompt.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()