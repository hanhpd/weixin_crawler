from ui.ui_instance import app, socketio, the_redis
from Application.gzh_category import GZHCategory
from Application.gzh_crawler import GZHCrawler
from es.setting import  GZHSearchSetting

# Public account crawler application example
gc = GZHCrawler()
# Public account category management example Mainly serves targeted search
gzh_category = GZHCategory()
# Search setting example Mainly serves the setting of search behavior
gzh_setting = GZHSearchSetting()


def run_webserver():
    socketio.run(app, host= '0.0.0.0')

def run_gzh_crawler():
    import time
    while True:
        # Increase time to prevent high CPU usage
        time.sleep(1)
        gc.run()


# Delay import to prevent recursive import
from ui.router import *
from ui.event import *


