import os
import shutil
from uuid import uuid4

import click
import requests
from bs4 import BeautifulSoup
from html2text import HTML2Text
from md2pdf.core import md2pdf


@click.command()
@click.option('--url', prompt='Medium URL', help='The URL must be from the medium.com domain.')
def main(url = str):
    html2text = HTML2Text()
    filename = str(uuid4()) + ".pdf"
    raw_html = ""

    try:
        raw_html = requests.get(url, timeout=30).text
    except requests.exceptions.RequestException as e:
        click.echo(click.style(f"An error occurred: {e}", fg='red'))
        return

    scraped_page = BeautifulSoup(raw_html, 'html.parser')
    article = scraped_page.find('article')

    title = article.find('h1').get_text()

    title = html2text.handle(title)
    text = html2text.handle(str(article))

    text = text.split("Share")[1]
    markdown_content = f"# {title}\n\n{text}"

    filename = title.strip().replace("/", "-").replace(" ", "-").replace(":", "-") + "." + filename

    if not os.path.isdir("docs"):
        os.mkdir("docs")
    
    md2pdf(filename, markdown_content, css_file_path="./styles/markdown.css")
    shutil.move(filename, f"docs/{filename}")

    click.echo("Your article has been saved as a PDF.")


if __name__ == '__main__':
    click.echo(click.style("Welcome to our Briefify CLI Tool!", fg='cyan'))

    main()