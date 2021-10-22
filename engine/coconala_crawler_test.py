from engine.coconala_crawler import *

def test_search_job():
    crawler = CoconalaCrawler()
    items = crawler.search_job_items("Web")
    print(items[0].to_dict())
    

def test_fetch_detail():
    crawler = CoconalaCrawler()
    item = crawler.fetch_work_detail("1240686")
    print(item.to_dict())
    