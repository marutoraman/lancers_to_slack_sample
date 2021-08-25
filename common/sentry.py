import os
import sentry_sdk

from dotenv import load_dotenv
load_dotenv() #環境変数のロード

if os.environ.get("SENTRY_SDN"):
    print("init sentry")
    sentry_sdk.init(os.environ.get("SENTRY_SDN"))