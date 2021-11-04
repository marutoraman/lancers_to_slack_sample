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


class MentaCrawler(BaseCrawler):
    WORK_DETAIL_URL = "https://menta.work/bosyu/{work_id}"
    WORK_SEARCH_URL = "https://menta.work/bosyu"
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
            "categoryId": "1",
            "price": "0",
            "page": page
        }
        # https://menta.work/bosyu?tag=&q=&categoryId=1&price=0
        #https://www.lancers.jp/work/search/system?open=1&ref=header_menu&show_description=0&work_rank%5B%5D=0&work_rank%5B%5D=1&work_rank%5B%5D=2&work_rank%5B%5D=3
        #https://www.lancers.jp/work/search/system?type%5B%5D=project&open=1&work_rank%5B%5D=3&work_rank%5B%5D=2&work_rank%5B%5D=1&work_rank%5B%5D=0&budget_from=&budget_to=&keyword=&not=
        try:
            soup = self.fetch_html_to_bs(self.WORK_SEARCH_URL, params=params)
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        # 詳細ページへのリンクを取得
        detail_link_elms = soup.select(".title > a")
        
        # SearchedItemに格納
        items = []
        for detail_elm in detail_link_elms:
            try:
                link = str(detail_elm.get("href"))
                if not link:
                    logger.error(f"job detail link is not found")
                    continue
                work_id = re_search("/bosyu/(.*)", link)
                if work_id in exclude_work_ids:
                    logger.info(f"[skip] already crawled: {link}")
                    continue
                if work_id == None:
                    logger.info(f"純粋なMenta以外の案件はスキップ: {link}")
                    continue
                #work_id = link.split("/")[-1]
                items.append(
                    SearchedItem(
                        work_id = work_id,
                        site = "menta"
                    )
                )
            except Exception as e:
                logger.error(e)
                continue
        return items
        
    
    def fetch_work_detail(self, work_id: str):
        soup = self.fetch_html_to_bs(self.WORK_DETAIL_URL.format(work_id = work_id))
    
        try:
            title = soup.select_one("h1").text.split("\n")[0].strip()
        except:
            title = None
            
        try:
            price = soup.select_one(".container.bosyu_price .flexbox").text
        except:
            price = None
            
        try:
            description = soup.select_one("#main p").text.strip()
            #description = lxml_soup.xpath("span[contains(text(), '依頼の目的・背景')]")
        except Exception as e:
            print(e)
            description = None
            
        try:
            _proposales_count = soup.select_one(".container.bosyu_suggest .flexbox").text
            if _proposales_count.find("提案待ち") >= 0:
                proposales_count = 0
            else:
                proposales_count = int(_proposales_count)
        except:
            proposales_count = None
        
        try:
            proposales_count = int("".join([elm.select_one("td").text.replace("人", "").strip() for elm in soup.select(".application_status_table tr") if elm.text.find("応募した人") >= 0]))
        except Exception as e:
            proposales_count = None
        
        title_price = ""
        if title: 
            title_price = title
        if price:
            title_price += "\n" + price
        
        item = SearchedItem(
            title = title_price,
            description = description,
            proposales_count = proposales_count
        )
        
        return item