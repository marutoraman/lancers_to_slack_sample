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
    crawler = LancersCrawler()
    # 特定の検索条件でCrawle
    items = crawler.search_job_items("https://www.lancers.jp/work/search/system?open=1&ref=header_menu&show_description=0&work_rank%5B%5D=0&work_rank%5B%5D=1&work_rank%5B%5D=2&work_rank%5B%5D=3")
    
    db: Session = get_db_instance()
    for item in items:
        # 新規のjobのみDBに登録
        job = db.query(Job).filter_by(work_id=item.work_id).first()
        if job is None:
            # Insert
            db.add(
                Job(
                    work_id = item.work_id 
                )
            )
            # 確定
            db.commit()
    

if __name__ == "__main__":
    fire.Fire(crawle)