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

from common.selenium_manager import *
from common.logger import *
from common.utility import datetime_to_string, download_img, exists_or_create_dir, now_time_delta, re_search, to_datetime

from common.logger import set_logger
logger = set_logger(__name__)

class BaseCrawler():
    HEADERS = {"Accept": "*/*",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36}"}
    
    def fetch_html_to_bs(self, url: str, params: dict={}) -> bs:
        res = requests.get(url, headers=self.HEADERS, params=params)
        if not(300 > res.status_code >= 200):
            print(res.text)
            logger.error(f"fetch_html error | status_code: {res.status_code}")
            raise Exception(f"fetch_html error | status_code: {res.status_code}")
        return bs(res.text, "html.parser")
    
    def fetch_html(self, url: str, params: dict={}):
        res = requests.get(url, headers=self.HEADERS, params=params)
        if not(300 > res.status_code >= 200):
            logger.error(f"fetch_html error | status_code: {res.status_code}")
            raise Exception(f"fetch_html error | status_code: {res.status_code}")
        return res