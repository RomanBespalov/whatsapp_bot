import feedparser

RSS_URL = "https://static.primamedia.ru/export/new/news_main_WhatsApp_43.rss"


def get_rss_news(RSS_URL):
    feed = feedparser.parse(RSS_URL)
    # amount = len(feed.entries)  # 50
    last_entry = feed.entries
    return last_entry[0]


# print(get_rss_news(RSS_URL)['title'])

# print(get_rss_news(RSS_URL))
# print(get_rss_news(RSS_URL)['links'][1]['href'])
