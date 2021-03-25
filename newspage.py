from requests_html import HTMLSession
from cfscrape import create_scraper
import time
from bs4 import BeautifulSoup
import logging


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

    def get_url_content(self, url):
        try:
            self.session = HTMLSession()
            self.source = self.session.get(url).html
            print(self.source)
            logging.info("--- %s took %s seconds ---" % (__name__, time.time() - self.start_time))
            return self.source
        except Exception:
            logging.error("-- ERROR in %s retrieving content  --" % (__name__))

