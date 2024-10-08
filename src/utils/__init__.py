import os
import random
import shutil
from uuid import uuid4

import click
import requests
from bs4 import BeautifulSoup
from md2pdf.core import md2pdf


def get_filename(title: str, extensions) -> str:
    converted_title = title.strip().replace("/", "-").replace(" ", "-").replace(":", "-")
    return converted_title + f".{extensions}"


def create_file(filename: str, markdown_content: str) -> None:
    if not os.path.isdir("docs"):
        os.mkdir("docs")
    
    if filename.endswith(".pdf"):
        md2pdf(filename, markdown_content, css_file_path="./src/styles/markdown.css")
    elif filename.endswith(".md"):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(markdown_content)

    shutil.move(filename, f"docs/{filename}")


def use_scraped_page(url: str) -> BeautifulSoup:
    raw_html = ""

    try:
        raw_html = requests.get(url, timeout=30).text
    except requests.exceptions.RequestException as e:
        click.echo(click.style(f"An error occurred: {e}", fg='red'))

    return BeautifulSoup(raw_html, 'html.parser')


def split_text(text: str) -> str:
    try:
        text = text.split("Share")[1]
        return text
    except IndexError:
        click.echo(click.style("The article could not be processed. Please try again.", fg='red'))
        return ""    

def concat_content(args: list[str]) -> str:
    return "\n\n".join(args)


def update_dom(article: BeautifulSoup) -> BeautifulSoup:
    pictures = article.find_all('picture')

    for picture in pictures:
        source = picture.find('source')

        if source:
            img_url = source['srcset'].split(' ')[0]

            picture.replace_with(f"![image]({img_url})")

    return article


def create_divider(index):
            return f"\n\nArticle {index}\n\n"


def generate_numbers():
    numbers = sorted(random.sample(range(1, 100), 3))
    numbers = [numbers[0], numbers[1] - numbers[0], numbers[2] - numbers[1], 100 - numbers[2]]
    random.shuffle(numbers)

    return numbers