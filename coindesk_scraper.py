from datetime import datetime, timezone
from sys import exit

from newspage import NewsPage


class CoindeskScraper:
    def __init__(self):
        self.news_page = NewsPage()
        self.news_page.url = "https://coindesk.com"

    def parse_articles(self):
        self.news_page.source = self.news_page.get_url_content(self.news_page.url)
        articles = self.news_page.source.xpath(
            '//*[contains(@class, "article-card-fh")] | //*[contains(@class, "list-item-card")]')[7:9]
        for article in articles:
            href = article.xpath('//*[@class="heading"]//a | //a//*[@class="heading"]//ancestor::a', first=True)
            link = f"{self.news_page.url}{href.attrs['href']}"
            print(link)
            article_page = self.news_page.get_url_content(link)
            time = article_page.find('time', first=True)
            try:
                published_at = datetime.fromisoformat(time.attrs['datetime']).replace(tzinfo=timezone.utc)
            except KeyError:
                published_at = datetime.strptime(time.text, '%b %d, %Y').replace(tzinfo=timezone.utc)
            except Exception as e:
                print(e)
            #main_article_image


if __name__ == '__main__':
    coindesk_scraper = CoindeskScraper()
    coindesk_scraper.parse_articles()
