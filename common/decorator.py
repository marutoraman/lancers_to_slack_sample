import inspect

from common.logger import set_logger

logger = set_logger(__name__)

def logger_passage(func):
    '''
    開始、終了時ログを出力するためのWrapper
    '''
    def passage(*args, **kwargs):
        filename=inspect.getfile(func).split('\\')[-1] #フルパスファイル名からファイル名だけを取得
        logger.info(f"[begin] {filename} - {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"[end] {filename} - {func.__name__}")
        return result
    return passage