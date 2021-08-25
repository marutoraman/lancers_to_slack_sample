from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

HEADER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"

def set_driver(is_headless: bool=False):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモードの設定
    if is_headless:
        options.add_argument('--headless')
        
    options.add_argument('--user-agent=' + HEADER_USER_AGENT)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与
    
    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(ChromeDriverManager().install(), options=options)

    
    