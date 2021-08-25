from common.database import get_db_instance
import re
import time
import traceback
import datetime 
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs 
import csv
import json
import requests

from sqlalchemy.orm.session import Session
from sqlalchemy import or_ 

from engine.base_crawler import *
from engine.searched_item import *
from common.selenium_manager import *
from common.logger import *
from common.utility import datetime_to_string, download_img, exists_or_create_dir, now_time_delta, re_search, to_datetime

from common.logger import set_logger
logger = set_logger(__name__)


class LancersCrawler(BaseCrawler):

    def search_job_items(self, url: str):
        try:
            soup = self.fetch_html_to_bs(url)
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        # 詳細ページへのリンクを取得
        detail_link_elms = soup.select("a.c-media__title")
        
        # SearchedItemに格納
        items = []
        for detail_elm in detail_link_elms:
            try:
                link = detail_elm.get("href")
                work_id = link.split("/")[-1]
                items.append(
                    SearchedItem(
                        work_id = work_id
                    )
                )
            except Exception as e:
                logger.error(e)
                continue
        return items