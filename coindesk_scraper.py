from newspage import NewsPage


class CoindeskScraper:
    def __init__(self):
        self.news_page = NewsPage()
        self.news_page.url = "https://coindesk.com"

    def parse_articles(self):
        self.news_page.get_url_content(self.news_page.url)


if __name__ == '__main__':
    coindesk_scraper = CoindeskScraper()
    coindesk_scraper.parse_articles()
