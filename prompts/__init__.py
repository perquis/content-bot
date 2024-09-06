import os

from dotenv import load_dotenv
from InquirerPy import inquirer

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


url = inquirer.text(message="Enter a medium.com URL:").execute()
extensions = inquirer.select(message="Choose a file format:", choices=['pdf', 'md']).execute()

if OPENAI_API_KEY is None:
    OPENAI_API_KEY = inquirer.secret(
        message="Enter your OpenAI API key:",
        validate=lambda x: len(x) > 0,
        default="",
    ).execute()

    with open(".env", "w", encoding="utf-8") as f:
        f.write(f"OPENAI_API_KEY={OPENAI_API_KEY}")