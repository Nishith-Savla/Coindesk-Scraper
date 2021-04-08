import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pprint import pprint
from time import perf_counter
from typing import Iterator, Union

from newspage import NewsPage


class CoindeskScraper:
    def __init__(self):
        self.news_page = NewsPage()
        self.news_page.url = "https://coindesk.com"

    def parse_article(self, article):
        href = article.xpath('//*[@class="heading"]//a | //a//*[@class="heading"]//ancestor::a', first=True)
        link = f"{self.news_page.url}{href.attrs['href']}"
        if any([word in link for word in ['podcasts', 'tv']]):
            return None
        article_page = self.news_page.get_url_content(link)
        article_body = article_page.xpath('//div[contains(@class,"article-module")]',
                                          first=True)
        # pprint(f'{link}: {article_body}')
        time = article_body.find('time', first=True)
        authors = article_body.xpath('//*[contains(@class, "sidebar-profile") and contains(@class, "author")]'
                                     '/div[contains(@class, "text-block")]/a')
        categories = article_body.xpath(
            '//div[@class="category-link-wrapper"]//span[@class="related-button-text"]/strong')
        content = article_body.xpath('//*[contains(@class, "article-content")]', first=True)
        language = 'English'
        try:
            published_at = datetime.fromisoformat(time.attrs['datetime']).replace(tzinfo=timezone.utc)
        except KeyError:
            published_at = datetime.strptime(time.text, '%b %d, %Y').replace(tzinfo=timezone.utc)
        except Exception as e:
            published_at = e

        return (
            published_at,
            language,
            link,
            " / ".join([author.text for author in authors]),
            " / ".join([category.text for category in categories]),
            content.text.strip()
        )

    def parse_all_articles(self, csv_filename=f'coindesk_{str(datetime.utcnow()).replace(":", "-")}.csv',
                           headers=('Published date', 'Article language', 'Arcticle URL', 'Author(s)', 'Category(ies)',
                                    'Content')):
        self.news_page.source = self.news_page.get_url_content(self.news_page.url)
        articles = self.news_page.source.xpath(
            '//*[contains(@class, "article-card-fh")] | //*[contains(@class, "list-item-card")]')

        with ThreadPoolExecutor() as executor:
            results: Iterator[tuple[Union[Exception, datetime], str, str]] = executor.map(self.parse_article, articles)
        # results = []
        # for article in articles:
        #     results.append(self.parse_article(article))
        # pprint(list(results))
        with open(csv_filename, 'w', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"')
            csv_writer.writerow(headers)
            for result in results:
                result and csv_writer.writerow(result)


if __name__ == '__main__':
    coindesk_scraper = CoindeskScraper()
    start = perf_counter()
    coindesk_scraper.parse_all_articles()
    print(f"It took {perf_counter() - start} as per perf_counter()")
