import os
import sys
from sqlalchemy.orm.session import Session
import fire

from dotenv import load_dotenv
load_dotenv()

# 独自モジュールのインポートは、これ以降で行う
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common.logger import set_logger
import common.sudachi as sudachi
from engine.slack import Slack
from common.database import get_db_instance
from engine.lancers_crawler import *
from engine.cw_crawler import *
from engine.coconala_crawler import *
from models.job import *

logger = set_logger(__name__)

LANCERS_ITEM_URL = "https://www.lancers.jp/work/detail/{work_id}"
CW_ITEM_URL = "https://crowdworks.jp/public/jobs/{work_id}"
COCONALA_ITEM_URL = "https://coconala.com/requests/{work_id}"

def crawle(site: str, page_limit: int=3):
    db: Session = get_db_instance()
    if site == "lancers":
        crawler = LancersCrawler()
    elif site == "cw":
        crawler = CWCrawler()
    elif site == "coconala":
        crawler = CoconalaCrawler()
    else:
        raise Exception(f"site is invalid: {site}")
    
    # 既に取得済のidは除外
    crawled_word_ids = [job.work_id for job in db.query(Job).filter_by(site=site).all()]
    logger.info(f"exclude word_ids count: {len(crawled_word_ids)}")
    
    # 特定の検索条件でCrawle
    items = crawler.search_job_items(page_limit=page_limit, exclude_work_ids=crawled_word_ids)
    logger.info(f"searched items count: {len(items)}")
    
    # 詳細ページを取得
    for item in items:
        try:
            detail_item = crawler.fetch_work_detail(item.work_id)
            item.merge(detail_item)
            # item.title = detail_item.title
            # item.description = detail_item.description
            logger.info(f"item detail crawled: [{item.work_id}] {detail_item.title}")
        except Exception as e:
            logger.error(f"error! item detail crawle: {item.work_id}")
    
    for item in items:
        job = db.query(Job).filter_by(work_id=item.work_id).first()
        if job is None:
            job = Job(work_id=item.work_id)
        
        # 検索用のindexキーワードリストを作成
        _search_sentence = item.title
        if item.description:
            _search_sentence += " " + item.description
        search_index_words = list(set(sudachi.sudachi_tokenize(_search_sentence)))
        
        job.merge(item, exclude_keys=["work_id"])
        # job.title = item.title
        # job.description = item.description
        job.search_index_words = json.dumps(search_index_words, ensure_ascii=False)
        db.add(job)
        db.commit()
        
    db.close()
    
    
def send_slack():
    # 検索ワードを作成
    SEAECH_WORDS = ["スクレピング", "データ取得", "Amazon", 
                    "楽天", "ヤフー", "ショッピング", "EC", 
                    "初心者", "自動操作", "API", "Aliexpress", 
                    "アリエク", "自動出品", "ヤフオク", "Python", 
                    "物販", "Twitter", "Instagram", "Youtube",
                    "Django", "インスタ"]
    MESSAGE_TEMPLATE = "{title}\n提案数(データ取得時点): {proposales_count} 件\n{url}\n"
    
    normalized_search_words = []
    for word in SEAECH_WORDS:
        normalized_search_words.extend(["".join(sudachi.normalize(word))])
    normalized_search_words.extend(SEAECH_WORDS)
    logger.info(normalized_search_words)
    
    # 未送信のJobリストを取得
    db: Session = get_db_instance()
    jobs = db.query(Job).filter(Job.is_send==False).all()
    logger.info(f"jobs count: {len(jobs)}")
    
    # 検索
    hit_jobs = []
    for job in jobs:
        if len(set(normalized_search_words) & set(json.loads(job.search_index_words))) >= 1:
            hit_jobs.append(job)
    
    logger.info(f"hit jobs count: {len(hit_jobs)}")
    
    # Slack送信
    messages = []
    for hit_job in hit_jobs:
        if not hit_job.title or not hit_job.work_id:
            continue
        if hit_job.site == "lancers":
            item_url = LANCERS_ITEM_URL.format(work_id=hit_job.work_id)
        elif hit_job.site == "cw":
            item_url = CW_ITEM_URL.format(work_id=hit_job.work_id)
        elif hit_job.site == "coconala":
            item_url = COCONALA_ITEM_URL.format(work_id=hit_job.work_id)
        else:
            continue
        messages.append(
            MESSAGE_TEMPLATE.format(title = hit_job.title, 
                                    proposales_count = hit_job.proposales_count,
                                    url = item_url)
        )
        hit_job.is_send = True
    
    Slack.send_message_webhook(os.environ.get("SLACK_WEBHOOK_URL"), 
                               "\n\n------------\n\n".join(messages))
    
    db.commit()
    db.close()


def loop(page_limit:int=3):
    while True:
        crawle(site="lancers", page_limit=page_limit)
        crawle(site="cw", page_limit=page_limit)
        crawle(site="coconala", page_limit=page_limit)
        send_slack()
        logger.info("send completed")
        time.sleep(180)
    
    
if __name__ == "__main__":
    fire.Fire()