# -*- coding: utf-8 -*-
from datetime import datetime as dt
import datetime
from pytz import timezone
import socket
import ssl
import urllib.error
import urllib.request
import os
import re
import datetime
import urllib.error
from zipfile import ZipFile
import requests
from sqlalchemy.dialects import mysql

def now_timestamp(format="%Y-%m-%d-%H-%M-%S"):
    return dt.now().strftime(format)

def list_to_bool(l:list):
    bool_list=[]
    for item in l:
        bool_list.append(False if item == "0" or item == 0 else True)
    
    return bool_list

def create_proxy_dict(id,password,host,port,proxy_flg=True):
    if proxy_flg:
        proxy_url=f"http://{id}:{password}@{host}:{port}"
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    else:
        return {}

def get_global_ip():
    return socket.gethostbyname(socket.gethostname())

def download_img(url, path):
    if not os.path.exists(path):
        os.mkdir(path)
    ''' URLを指定し、画像を指定のフォルダに配置する '''
    # ファイル名の作成
    values = url.split('/')
    filename = values[-1]
    filename = filename.split('.')[0]
    # ファイルパスの指定
    download_path = os.path.join(os.getcwd(), path, filename)

    # 画像URLからダウンロード
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(download_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)
        raise Exception(f"image download error: {e}")

    return download_path

def get_date_delta(delta):
    now = datetime.datetime.now()
    return now+datetime.timedelta(days=int(delta))

def padding_zero(text,num):
    return ("0"+text)[-num:]


def download_zipfile(url:str, save_path: str):
    try:
        with urllib.request.urlopen(url) as download_file:
            data = download_file.read()
            with open(save_path, mode='wb') as save_file:
                save_file.write(data)
        return True
    except urllib.error.URLError as e:
        print(e)
        return False

def extract_zipfile(zipfile_path: str, save_path: str):
    try:
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        with ZipFile(zipfile_path) as obj_zip:
            # 指定ディレクトリにすべてを保存する
            obj_zip.extractall(save_path)
            return True
    except Exception as e:
        print(f"[error] extract zipfile: {e}")
        return False

def to_cm(inchi: float):
    return inchi * 2.54

def to_kg(pound: float):
    return pound * 0.4535 


def fetch_currency_rate(base: str, to: str):
    res = requests.get("http://fx.mybluemix.net/")
    res.raise_for_status()
    res_dict = res.json()
    try:
        return res_dict["result"]["rate"][base + to]
    except:
        raise Exception(f"exchange currency error: {base}->{to}")


def exchange_to_jpn_from_usd(usd: float, rate: float):
    print(usd)
    return int(float(usd) * rate)


def print_query(query):
    print(query.statement.compile(
            dialect=mysql.dialect(),
            compile_kwargs={"literal_binds": True}))


def re_search(pettern: str, target: str):
    m = re.search(pettern, target)
    if m == None:
        return None
    else:
        try:
            return m.group(1)
        except:
            return None
        

def now_time_delta(**kwargs):
    return dt.now() - datetime.timedelta(**kwargs)


def datetime_to_string(input_datetime, format: str="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strftime(input_datetime, format)


def to_datetime(datetime_str: str, format: str="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(datetime_str, format)

def exists_or_create_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)