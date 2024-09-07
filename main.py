# build-in modules
import os

# third-party modules
import click
from dotenv import load_dotenv
from InquirerPy import inquirer

from src import controller

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@click.command()
@click.option(
    '--url',
    '-u',
    help='Medium.com URL',
    multiple=True,
    default=[]
)
@click.option(
    '--md',
    '-m',
    help='Save as Markdown',
    is_flag=True,
    default=False
)
@click.option(
    '--pdf',
    '-p',
    help='Save as PDF',
    is_flag=True,
    default=False
)
def main(url: list[str], md, pdf):
    """
    This is a CLI tool that scrapes an article
    from medium.com and saves it as a PDF or
    Markdown file.
    """
    urls = list(url)
    
    if len(url) == 0:
        medium_com_url = inquirer.text(message="Enter a medium.com URL:").execute()
        urls.append(medium_com_url)

        confirm = inquirer.confirm(message="Do you want to add more articles?", default=True).execute()

        while confirm:
            new_medium_com_url = inquirer.text(message="Enter a medium.com URL:").execute()
            urls.append(new_medium_com_url)
            confirm = inquirer.confirm(message="Do you want to add more articles?", default=True).execute()

    extensions = ""

    if md:
        extensions = "md"
    elif pdf:
        extensions = "pdf"
    else:
        extensions = inquirer.select(message="Choose a file format:", choices=['pdf', 'md']).execute()

    controller.content_bot(urls, extensions, OPENAI_API_KEY)


if __name__ == '__main__':
    main(url=[], md=False, pdf=False)
