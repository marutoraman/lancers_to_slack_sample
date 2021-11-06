import os
import sys
import fire

from dotenv import load_dotenv
load_dotenv()

# 独自モジュールのインポートは、これ以降で行う
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common.logger import set_logger
from engine.slack import Slack
from engine.lancers_crawler import *


logger = set_logger(__name__)

SEND_WORKS_LIST_CSV_NAME = "send_works_list.csv"

def crawle(page_limit: int=3):
    pass
    
    
def send_slack(works: list):
    pass
    

def run(page_limit: int=3):
    pass

    
if __name__ == "__main__":
    fire.Fire(run)