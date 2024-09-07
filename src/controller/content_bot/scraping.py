from html2text import HTML2Text

from src import utils


def scraping(urls: list[str]):
    html2text = HTML2Text()

    markdowns = []
    scraped_pages_list = [utils.use_scraped_page(url) for url in urls]

    for page in scraped_pages_list:
        article = utils.update_dom(page.find('article'))

        title = article.find('h1').get_text()
        title = html2text.handle(title)
        
        text = html2text.handle(str(article))
        text = utils.split_text(text)
        
        markdown_content = utils.concat_content([f"# {title}", text])

        markdowns.append(markdown_content)

    return markdowns