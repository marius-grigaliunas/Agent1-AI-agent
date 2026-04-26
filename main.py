import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from available_functions import available_functions, call_function
import prompts

load_dotenv()
gemini_api = os.environ.get("GEMINI_API_KEY")
gemini_model = "gemini-3.1-flash-lite-preview"

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

    chat = client.chats.create(
        model=gemini_model,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=prompts.system_prompt,
            temperature=0,
            thinking_config=types.ThinkingConfig(include_thoughts=True),
        ),
    )
    next_message = prompt

    for _ in range(20):
        response = chat.send_message(next_message)

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
            return

        if function_results:
            next_message = function_results
    else:
        print("The agent took too long to produce a response")
        sys.exit(1)
    



if __name__ == "__main__":
    main()
