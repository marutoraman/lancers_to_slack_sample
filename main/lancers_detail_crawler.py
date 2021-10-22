import os
import sys
from sqlalchemy.orm.session import Session
import fire

# 独自モジュールのインポートは、これ以降で行う
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common.database import get_db_instance
from engine.lancers_crawler import *
from models.job import *


def crawle():
    db: Session = get_db_instance()
    job_list = db.query(Job).filter(Job.title != None).all()
    crawler = LancersCrawler()
    # 特定の検索条件でCrawle
    for job in job_list:
        item = crawler.fetch_work_detail(job.work_id)
        job.title = item.title
        job.description = item.description
        
        db.commit()
    

if __name__ == "__main__":
    fire.Fire(crawle)