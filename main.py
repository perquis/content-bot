import click
from html2text import HTML2Text

from utils import create_filename, create_pdf, use_scraped_page


@click.command()
@click.option('--url', prompt='Medium URL', help='The URL must be from the medium.com domain.')
def main(url = str):
    html2text = HTML2Text()
    scraped_page = use_scraped_page(url)

    article = scraped_page.find('article')

    title = article.find('h1').get_text()
    filename = create_filename(title)

    title = html2text.handle(title)
    text = html2text.handle(str(article))

    text = text.split("Share")[1]
    markdown_content = f"# {title}\n\n{text}"

    create_pdf(filename, markdown_content)
    click.echo("Your article has been saved as a PDF.")


if __name__ == '__main__':
    click.echo(click.style("Welcome to our Briefify CLI Tool!", fg='cyan'))

    main()