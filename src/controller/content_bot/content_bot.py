
import os

import click
from tqdm import tqdm

from src import utils
from src.controller.content_bot.gpt import gpt
from src.controller.content_bot.scraping import scraping


def content_bot(urls, extensions, api_key):
    """
    This function is the controller for the content bot.
    It scrapes the articles, generates the markdowns, and
    creates the file.
    """
    # Generate four random percentages for the progress bar
    [p1, p2, p3, p4] = utils.generate_numbers()

    with tqdm(total=100, desc="Processing", unit="%", ncols=100) as pbar:
        pbar.update(p1)

        # Scrape the articles and get the markdowns from the articles
        markdowns = scraping(urls)

        pbar.update(p2)
        
        # Generate the markdown content using the GPT-4o-mini
        filename, markdown_content = gpt(markdowns, extensions, api_key)

        pbar.update(p3)

        # Create the file with the markdown content
        # and save it in the docs folder
        utils.create_file(
            filename, 
            markdown_content
        )

        # Print the path where the file is saved
        path = os.path.join(os.getcwd(), "docs", filename)
        
        pbar.update(p4)

    click.echo(f"Your article has been saved here: {path}.")