from engine.lancers_crawler import *

def test_search_job():
    crawler = LancersCrawler()
    items = crawler.search_job_items("https://www.lancers.jp/work/search?open=1&ref=header_menu")
    print(items[0].to_dict())