import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from available_functions import available_functions
import prompts

load_dotenv()
gemini_api = os.environ.get("GEMINI_API_KEY")

def main():
    if gemini_api == None:
        raise RuntimeError("No api loaded")

    client = genai.Client(api_key=gemini_api)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    prompt = args.user_prompt

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=prompts.system_prompt,
            temperature=0
            ),
        )
 
    prompt_tokens = response.usage_metadata.prompt_token_count  # pyright: ignore[reportOptionalMemberAccess]
    response_tokens = response.usage_metadata.candidates_token_count  # pyright: ignore[reportOptionalMemberAccess]

    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print("Response:")

    if response.function_calls:
        for function in response.function_calls:
            print(f"Calling function: {function.name}({function.args})")
    else:
        print(response.text)



if __name__ == "__main__":
    main()
