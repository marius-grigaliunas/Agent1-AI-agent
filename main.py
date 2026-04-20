import os
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()
gemini_api = os.environ.get("GEMINI_API_KEY")

def main():
    if gemini_api == None:
        raise RuntimeError("No api loaded")

    client = genai.Client(api_key=gemini_api)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    args = parser.parse_args()

    prompt = args.user_prompt

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    prompt_tokens = response.usage_metadata.prompt_token_count  # pyright: ignore[reportOptionalMemberAccess]
    response_tokens = response.usage_metadata.candidates_token_count  # pyright: ignore[reportOptionalMemberAccess]
    
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print("Response:")
    print(response.text)



if __name__ == "__main__":
    main()
