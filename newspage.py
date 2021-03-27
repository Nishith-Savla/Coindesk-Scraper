import logging
import time
from sys import exit
from typing import Union

from requests_html import HTMLSession


class NewsPage:
    start_time = time.time()
    logging.basicConfig(filename="NewsPage.log", level=logging.INFO,
                        format='%(asctime)s+05:30 | %(levelname)s | %(module)s | %(message)s')
    url = None
    source = None
    file = None
    new_articles = []

    def __init__(self):
        self.session = None

    def add_article(self, title, content, url, published_at, author="", category="", language="", image_url=""):
        article = [published_at, title, image_url, language, url, author, category, content]
        self.new_articles.append(article)

    def get_url_content(self, url: str, headers: Union[dict[str], None] = None):
        try:
            self.session: HTMLSession = HTMLSession()
            source = self.session.get(url, headers=headers).html
            logging.info(f"--- {url} took {time.time() - self.start_time} seconds ---")
            return source
        except Exception:
            logging.error(f"-- In retrieving content of {url} --")
            print(f"Error in retrieving content of {url}")
            exit(1)
