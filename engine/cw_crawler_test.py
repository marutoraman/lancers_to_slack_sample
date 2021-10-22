from engine.cw_crawler import *

def test_search_job():
    crawler = CWCrawler()
    items = crawler.search_job_items("データ")
    print(items[0].to_dict())
    

def test_fetch_detail():
    crawler = CWCrawler()
    item = crawler.fetch_work_detail("2485312")
    print(item.to_dict())
    