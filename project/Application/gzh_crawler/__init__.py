from tools.data_queue import RQ
from tools.data_queue import DBQ
from phone_operate.WeixinOperate import WeixinOperate
from configs.crawler import adb_ports

class GZHCrawler():
    """
    There is only one instance object, and singleton pattern can be used in design pattern
    Accepts a public account crawler manager instance as a parameter
    """
    def __init__(self):
        self.gzh_task_rq = RQ('gzh_task_rq')
        self.phone_adb_dbq = DBQ('phone_adb_ports','reptile')
        self.report_crawling_items = []
        # The adb port in the settings file is stored in the crawl queue
        for adb in adb_ports:
            self.phone_adb_dbq.add_element({'id':adb,'nick_name':'unknown','wxuin':'unknown'})

    def report_gzh_finished(self):
        """
        :return:Generate data to report the status of all public accounts, name, update time, etc.
        [{nickname,article_num,update_time,update_num}{}{}]
        Report once requires the number of documents in each collection on a separate computer. Excellent waste of time. Method to be improved.
        """
        # Get the status of the public number in mongdb
        report = {}
        report_data = []
        from db.meta_data import get_article_metadata
        from db import count
        meta_data = get_article_metadata(all=False)
        total_article = 0
        for key in meta_data:
            unit = {}
            unit['nickname'] = key
            unit['article_num'] = count(key)
            unit['update_time'] = meta_data[key]['date'].strftime("%Y/%m/%d %H:%M")
            unit['update_num'] = meta_data[key]['articles_num']
            report_data.append(unit)
            total_article += unit['article_num']
        report['data'] = report_data
        report['meta'] = {}
        report['meta']['total_gzh'] = len(report_data)
        report['meta']['total_article'] = total_article
        return report

    def _report_gzh_doing(self):
        """
        :return:Generate data to report public account status of ongoing tasks
        The data comes from the public number that exists in the task queue and the public number that is currently being processed
        nickname,percent,begin_time,need_time
        """
        report_data = []
        from tools.utils import dictstr_to_dict
        # Public number to be processed in the queue
        gzh_need_todolist = self.gzh_task_rq.get_rq_data()
        for gzh in gzh_need_todolist:
            gzh_task = dictstr_to_dict(gzh)
            unit = {}
            unit['nickname'] = gzh_task['nickname']
            unit['percent'] = 'UNK/UNK'
            unit['begin_time'] = 'UNK'
            unit['need_time'] = 'UNK'
            report_data.append(unit)
        return report_data

    def report_crawler(self):
        adb_ports = self.phone_adb_dbq.get_queue()
        report_data = []
        for adb in adb_ports:
            unit = {}
            unit['adb_port'] = adb['id']
            unit['nick_name'] = adb['nick_name']
            unit['wxuin'] = adb['wxuin']
            report_data.append(unit)
        return report_data

    def report_gzh_doing(self):
        """
        :return:May not be tasked
        """
        try:
            report_data = self._report_gzh_doing()
        except:
            report_data = []
        return report_data

    def add_crawler(self,crawler):
        """
        :param self:
        :return:Add crawler
        """
        self.phone_adb_dbq.add_element({'id':crawler['phone'],'nick_name':'unknown','wxuin':'unknown'})

    def delete_crawler(self,crawler):
        """
        :param crawler:
        :return:Remove crawler
        """
        print(crawler)
        self.phone_adb_dbq.delete_element({'id':crawler['phone']})

    def report_crawling(self,item,num=15):
        """
        :param num: Number of logs
        :param item:{'nickname':**,'percent':'12/1231','speed':0.023,'title':'***'}
        :return:
        """
        from ui.ui_instance import socketio
        self.report_crawling_items = [item] + self.report_crawling_items
        if len(self.report_crawling_items)>num:
            self.report_crawling_items.pop()
        socketio.emit('articles_logger_monitoring',self.report_crawling_items)
        return self.report_crawling_items


    def add_gzh(self,gzh):
        """
        :param gzh:
        :return:Add public number to task queue
        """
        self.gzh_task_rq.push(gzh)

    def delete_gzh(self,gzh):
        """
        :param gzh:
        :return:Delete public number
        """
        pass

    def update_gzh(self,gzh,n):
        """
        :param gzh:
        :return: Update public account article
        """
        pass

    def gzh_report(self,gzh):
        """
        :param gzh:
        :return:Generate a public account historical article data report
        """
        pass

    def gzh_article_list(self,gzh):
        """
        :param gzh:
        :return: Generate a list of all articles in the public account
        """
        pass

    def export_excel(self,gzh,field):
        """
        :param gzh:
        :param field:
        :return:Public field designated excel everywhere
        """
        pass

    def run(self):
        """
        :return:The newly added crawler will automatically obtain the request parameters whenever it receives an article crawl task
        The entire life cycle of the public account crawler needs a background process to monitor the public crawl and update tasks
        run needs to be executed continuously in a process
        """
        # Crawl task
        from tools.utils import dictstr_to_dict
        gzh_task = self.gzh_task_rq.pop()
        if gzh_task == []:
            return
        gzh_task = dictstr_to_dict(gzh_task)
        self.gzh_in_service = gzh_task['nickname']
        print(gzh_task)
        # Get parameters
        adb_ports_raw = self.phone_adb_dbq.get_queue()
        adb_ports = []
        for adb in adb_ports_raw:
            adb_ports.append(adb['id'])
        wo = WeixinOperate(adb_ports)
        if gzh_task['aom'] == 'halfauto':
            wo.get_all_req_data(gzh_task['nickname'], hand=True)
        elif gzh_task['aom'] == 'auto':
            wo.get_all_req_data(gzh_task['nickname'], hand=False)
        # Call reptile
        from crawler import run_crawl
        config = int(gzh_task['range'])
        # from os import system
        # system('python run_crawler.py '+str(config))
        run_crawl(config)
