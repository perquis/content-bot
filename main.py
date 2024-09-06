import click
from html2text import HTML2Text

import utils


@click.command()
@click.option('--url', prompt='Medium URL', help='The URL must be from the medium.com domain.')
def main(url = str):
    html2text = HTML2Text()
    scraped_page = utils.use_scraped_page(url)

    article = scraped_page.find('article')
    pictures = article.find_all('picture')

    for picture in pictures:
        source = picture.find('source')

        if source:
            img_url = source['srcset'].split(' ')[0]

            picture.replace_with(f"![image]({img_url})")

    title = article.find('h1').get_text()
    filename = utils.create_filename(title)

    title = html2text.handle(title)
    text = html2text.handle(str(article))

    text = utils.split_text(text)
    markdown_content = utils.concat_content([f"# {title}", text])

    utils.create_pdf(filename, markdown_content)
    click.echo("Your article has been saved as a PDF.")


if __name__ == '__main__':
    click.echo(click.style("Welcome to our Briefify CLI Tool!", fg='cyan'))

    main()