import os
import time

import click
from html2text import HTML2Text
from openai import OpenAI
from tqdm import tqdm

import instructions
import prompts
import utils


@click.command()
def main():
    """
    This is a CLI tool that scrapes an article 
    from medium.com and saves it as a PDF or 
    Markdown file.
    """
    url = prompts.url
    extensions = prompts.extensions
    chatgpt = OpenAI(api_key=prompts.OPENAI_API_KEY)

    with tqdm(total=100, desc="Processing", unit="%", ncols=100) as pbar:
        html2text = HTML2Text()
        scraped_page = utils.use_scraped_page(url)
        
        pbar.update(13)

        article = utils.update_dom(scraped_page.find('article'))
        title = article.find('h1').get_text()
        filename = utils.create_unique_name_file(title, extensions)
        title = html2text.handle(title)
        text = html2text.handle(str(article))
        text = utils.split_text(text)
        markdown_content = utils.concat_content([f"# {title}", text])

        time.sleep(0.5)
        pbar.update(34)

        response = chatgpt.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instructions.copywriter},
                {"role": "user", "content": markdown_content},
            ],
            temperature=0.5,
        )

        markdown_content = response.choices[0].message.content

        time.sleep(0.5)
        pbar.update(25)

        utils.create_file(filename, markdown_content)

        time.sleep(0.5)
        pbar.update(28)

    path = os.path.join(os.getcwd(), "docs", filename)
    click.echo(f"Your article has been saved here: {path}.")


if __name__ == '__main__':
    main()
