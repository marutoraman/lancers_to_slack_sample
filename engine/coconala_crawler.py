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
from lxml import html

from sqlalchemy.orm.session import Session
from sqlalchemy import or_ 

from engine.base_crawler import *
from engine.searched_item import *
from common.selenium_manager import *
from common.logger import *
from common.utility import datetime_to_string, download_img, exists_or_create_dir, now_time_delta, re_search, to_datetime

from common.logger import set_logger
logger = set_logger(__name__)


class CoconalaCrawler(BaseCrawler):
    WORK_DETAIL_URL = "https://coconala.com/requests/{work_id}"
    WORK_SEARCH_URL = "https://coconala.com/requests/categories/11"
    # https://crowdworks.jp/public/jobs/search?category_id=226&search%5Bkeywords%5D=%E3%83%87%E3%83%BC%E3%82%BF&keep_search_criteria=true&order=score&hide_expired=true


    def search_job_items(self, keyword: str="", exclude_keyword: str="", page_limit: int=3, exclude_work_ids: list=[]):        
        results = []
        for page in range(page_limit):
            try:
                results.extend(self.search_job_items_for_page(keyword=keyword, exclude_keyword=exclude_keyword, exclude_work_ids=exclude_work_ids, page=page+1))
                logger.info(f"page crawled: {page+1}")
            except Exception as e:
                logger.error(f"page crawle failed: {page+1} | {e}")
            
        return results


    def search_job_items_for_page(self, keyword: str="", exclude_keyword: str="", exclude_work_ids: list=[], page: int=1):
        params = {
            "categoryId": "11",
            "recruiting": "true",
            "keyword": keyword,
            "page": page
        }
        #https://www.lancers.jp/work/search/system?open=1&ref=header_menu&show_description=0&work_rank%5B%5D=0&work_rank%5B%5D=1&work_rank%5B%5D=2&work_rank%5B%5D=3
        #https://www.lancers.jp/work/search/system?type%5B%5D=project&open=1&work_rank%5B%5D=3&work_rank%5B%5D=2&work_rank%5B%5D=1&work_rank%5B%5D=0&budget_from=&budget_to=&keyword=&not=
        try:
            soup = self.fetch_html_to_bs(self.WORK_SEARCH_URL, params=params)
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        # 詳細ページへのリンクを取得
        detail_link_elms = soup.select(".c-itemInfo_title > a")
        
        # SearchedItemに格納
        items = []
        for detail_elm in detail_link_elms:
            try:
                link = str(detail_elm.get("href"))
                if not link:
                    logger.error(f"job detail link is not found")
                    continue
                print(link)
                work_id = re_search(r"/requests/(.*)", link)
                if work_id in exclude_work_ids:
                    logger.info(f"[skip] already crawled: {link}")
                    continue
                if work_id == None:
                    logger.info(f"純粋なCoconala以外の案件はスキップ: {link}")
                    continue
                #work_id = link.split("/")[-1]
                items.append(
                    SearchedItem(
                        work_id = work_id,
                        site = "coconala"
                    )
                )
            except Exception as e:
                logger.error(e)
                continue
        return items
        
    
    def fetch_work_detail(self, work_id: str):
        soup = self.fetch_html_to_bs(self.WORK_DETAIL_URL.format(work_id = work_id))
    
        try:
            title = soup.select_one(".c-requestTitle > h1").text.strip()
        except:
            title = None
            
        try:
            description = soup.select_one(".c-detail .c-detailRowContentText").text.strip()
            #description = lxml_soup.xpath("span[contains(text(), '依頼の目的・背景')]")
        except Exception as e:
            print(e)
            description = None
        
        try:
            proposales_count = int(soup.select_one(".c-requestOutlineRowContent_emphasis.c-requestOutlineRowContent_emphasis-proposals").text)
        except Exception as e:
            proposales_count = None
        
        item = SearchedItem(
            title = title,
            description = description,
            proposales_count = proposales_count
        )
        
        return item