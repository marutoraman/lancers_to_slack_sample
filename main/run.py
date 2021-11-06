import os
import sys
from types import new_class
import fire

from dotenv import load_dotenv
load_dotenv()

# 独自モジュールのインポートは、これ以降で行う
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common.logger import set_logger
import common.sudachi as sudachi
from engine.slack import Slack
from engine.lancers_crawler import *


logger = set_logger(__name__)

SEND_WORKS_LIST_CSV_NAME = "send_works_list.csv"

def crawle(page_limit: int=3):
    crawler = LancersCrawler()

    # 既に取得済のidは除外
    try:
        with open(SEND_WORKS_LIST_CSV_NAME, "r") as f:
            send_work_ids = list(set(f.read().split("\n")))
    except:
        send_work_ids = []
    logger.info(f"already send work_ids: {send_work_ids}")
    
    # 特定の検索条件でCrawle
    works = crawler.search_job_items(page_limit=page_limit, exclude_work_ids=send_work_ids)
    logger.info(f"searched works count: {len(works)}")
    
    # 詳細ページを取得
    for work in works:
        try:
            detail_item = crawler.fetch_work_detail(work.work_id)
            work.merge(detail_item)
            # item.title = detail_item.title
            # item.description = detail_item.description
            logger.info(f"work detail crawled: [{work.work_id}] {detail_item.title}")
        except Exception as e:
            logger.error(f"error! work detail crawle: {work.work_id}")
    
    return works
    
    
def send_slack(works: list):
    # 検索ワードを作成
    SEAECH_WORDS = ["スクレピング", "データ取得", "Amazon", 
                    "楽天", "ヤフー", "ショッピング", "EC", 
                    "初心者", "自動操作", "API", "Aliexpress", 
                    "アリエク", "自動出品", "ヤフオク", "Python", 
                    "物販", "Twitter", "Instagram", "Youtube",
                    "Django", "インスタ"]
    MESSAGE_TEMPLATE = "{title}\n"\
                       + "提案数(データ取得時点): {proposales_count} 件\n"\
                       + "{url}\n"

    # 検索    
    hit_works = []
    for work in works:
        for word in SEAECH_WORDS:
            if work.title and work.title.find(word) >= 0:
                hit_works.append(work)
                logger.info(f"hit: {work.title} (word: {word})")
                break
            if work.description and work.description.find(word) >= 0:
                hit_works.append(work)
                logger.info(f"hit: {work.description} (word: {word})")
                break
    logger.info(f"hit jobs count: {len(hit_works)}")
    
    # Slack送信
    messages = []
    for hit_work in hit_works:
        if not hit_work.title or not hit_work.work_id:
            continue
        item_url = LancersCrawler.WORK_DETAIL_URL.format(work_id=hit_work.work_id)
        messages.append(
            MESSAGE_TEMPLATE.format(title = hit_work.title, 
                                    proposales_count = hit_work.proposales_count,
                                    url = item_url)
        )
    
    Slack.send_message_webhook(os.environ.get("SLACK_WEBHOOK_URL"), 
                               "\n\n------------\n\n".join(messages))

    # 送信済のjobリストを出力
    hit_work_ids = [hit_work.work_id for hit_work in hit_works]
    logger.info(f"hit_work_ids: {hit_work_ids}")
    with open(SEND_WORKS_LIST_CSV_NAME, "a") as f:
        f.write("\n".join(hit_work_ids))
    

def run(page_limit: int=3):
    logger.info("start")

    try:
        works = crawle(page_limit=page_limit)
    except Exception as e:
        logger.error(e)
        return None
        
    try:
        send_slack(works)
    except Exception as e:
        logger.error(e)
        return None
        
    logger.info("completed")

    
if __name__ == "__main__":
    fire.Fire(run)