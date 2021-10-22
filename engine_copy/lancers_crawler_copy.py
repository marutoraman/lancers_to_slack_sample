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
    WORK_DETAIL_URL = "https://www.lancers.jp/work/detail/"

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

    
    def fetch_work_detail(self, work_id: str):
        try:
            soup = self.fetch_html_to_bs(self.WORK_DETAIL_URL + work_id)  
                
            # タイトル  
            def choose_word_title(title_lv1):
                if title_lv1:
                    return title_lv1.get_text(strip=True)
                else:
                    return None
            title_lv1 = soup.select_one(".c-heading.heading--lv1")
            title = choose_word_title(title_lv1)  

            # 詳細
            def find_word_description(dt_list, dd_list, target: str, target2: str):
                for dt, dd in zip(dt_list, dd_list):
                    if dt.get_text(strip=True) == target or dt.get_text(strip=True) == target2:
                        return dd.get_text(strip=True)
            description_dt_list = soup.select(".c-definitionList.definitionList--holizonalA01 .definitionList__term")            
            description_dd_list = soup.select(".c-definitionList.definitionList--holizonalA01 .definitionList__description")
            description = find_word_description(description_dt_list, description_dd_list, "依頼の目的・背景", "依頼概要")                      

            # 最低予算
            def find_target_word_min(dt_list, dd_list, target: str):
                for dt, dd in zip(dt_list, dd_list):
                    if dt.get_text(strip=True) == target:
                        dd = dd.text.split()[0]
                        dd = dd.replace(",", "")
                        return int(dd)                                                             
            price_min_dt_list = soup.select(".c-definitionList.definitionList--holizonalA01 .definitionList__term")    
            price_min_dd_list = soup.select(".c-definitionList.definitionList--holizonalA01 .definitionList__description")
            price_min = find_target_word_min(price_min_dt_list, price_min_dd_list, "提示した予算")

            # 最高予算
            def find_target_word_max(dt_list, dd_list, target: str):
                for dt, dd in zip(dt_list, dd_list):
                    if dt.get_text(strip=True) == target:
                        dd = dd.text.split()[3]
                        dd = dd.replace(",", "")
                        return int(dd)                                  
            price_max_dt_list = soup.select(".c-definitionList.definitionList--holizonalA01 .definitionList__term")
            price_max_dd_list = soup.select(".c-definitionList.definitionList--holizonalA01 .definitionList__description")
            price_max = find_target_word_max(price_max_dt_list, price_max_dd_list, "提示した予算")

            # 提案数   
            def choose_word_proposales(exist_proposales):
                if exist_proposales:
                    return int(exist_proposales.text.replace("件", ""))
                else:    
                    return None
            exist_proposales = soup.select_one(".tableSummary__col.tableSummary__col--worksNum .worksummary__text")
            proposales_number = choose_word_proposales(exist_proposales)

            item = SearchedItem(
                title = title,
                description = description,
                price_min = price_min,
                price_max = price_max,
                proposales_number = proposales_number
            ) 
        except Exception as e:
            logger.error(e)
            return None    
        return item

                
                
    

    
