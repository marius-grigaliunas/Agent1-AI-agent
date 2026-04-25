import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from available_functions import available_functions, call_function
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

    if args.verbose:
        print(f"User prompt: {prompt}")

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=[types.Content(role="user", parts=[types.Part(text=args.user_prompt)])],
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=prompts.system_prompt,
            temperature=0,
        ),
    )

    prompt_tokens = response.usage_metadata.prompt_token_count  # pyright: ignore[reportOptionalMemberAccess]
    response_tokens = response.usage_metadata.candidates_token_count  # pyright: ignore[reportOptionalMemberAccess]

    if args.verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print("Response:")

    function_results = []

    if response.function_calls:
        for function in response.function_calls:
            function_call_result = call_function(function, args.verbose)

            if not function_call_result.parts:
                raise Exception("response doesn't contain any parts")

            if not function_call_result.parts[0].function_response:
                raise Exception("function response is None")

            if not function_call_result.parts[0].function_response.response:
                raise Exception("function result is None")

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)



if __name__ == "__main__":
    main()
