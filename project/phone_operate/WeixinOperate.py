from phone_operate.config import BTN, CROP_RANGE, UI_WORDS
from phone_operate.config import KEY
import time
from random import randint
from phone_operate.PhoneControl import OperateAllPhone
from phone_operate.VC import VC
from instance import redis_instance
from crawler_assist.tidy_req_data import TidyReqData



class WeixinOperate():
    """
    Implement operations on all online phones to get WeChat request parameters
    """
    busy = 0
    def __init__(self, phone_list):
        self.oap = OperateAllPhone(phone_list)
        self.home_weixin = {} #Desktop WeChat location
        self.main_bottom = {} #Position of the four big buttons at the bottom of the WeChat main interface
        self.gzh_folder = {} #Public account folder location
        # Find a mobile phone interface as an eye
        self.vc = VC(phone_list[0])

    def home(self):
        """
        :return:Click the BACK button multiple times to return to the main interface.Why not directly click the HOME button?
        """
        for i in range(7):
            self.oap.key(KEY['BACK_KEYEVENT'])
            time.sleep(0.3)
        return KEY['BACK_KEYEVENT']

    def home_to_gzh_search(self):
        """
        :return:Search from the main interface to the public account
        """
        # Click on the WeChat icon
        self.oap.tap(BTN['EMU_WEIXIN_ICON'])
        time.sleep(0.5)
        # Click on Contacts
        self.oap.tap(BTN['TONGXUNLU_BTN'])
        time.sleep(0.5)
        # Click on the public number
        self.oap.tap(BTN['GZH_FOLDER'])
        time.sleep(0.5)
        # Click search
        self.oap.tap(BTN['SEARCH_BTN'])
        time.sleep(1)
        return 0

    def search_gzh(self, nickname):
        """
        :param nickname:Public name to be searched
        :return:
        """
        # Enter pinyin
        self.oap.text(nickname)
        time.sleep(0.5)
        # Enter account
        self.oap.tap(BTN['FIRST_GZH_SEARCH_RESULT'])
        time.sleep(0.5)
        #Type the main interface
        self.oap.tap(BTN['PROFILE_BTN'])
        time.sleep(0.5)
        # pull up
        self.oap.roll(0,500)
        time.sleep(0.5)
        return 0

    def all_message(self):
        """
        :return:From the public account home page, click and click All Messages.
        """
        # All news
        all_message_pos = self.vc.click_by_words("All news",tap=False)
        self.oap.tap(all_message_pos)
        time.sleep(5)
        self.oap.roll(0,500)
        time.sleep(2)
        return 0

    def click_a_message(self, args=2):
        """
        :return:Randomly click on an article after coming to the history list
        """
        #Get interface article title message
        if args==1:corp = CROP_RANGE['PROFILE_MESSAGE_LIST']
        elif args==2:corp = CROP_RANGE['MESSAGE_LIST']
        ui_words = self.vc.get_ui_words(location=True, crop=corp)
        #Just click on a title
        random_index = randint(1,len(ui_words))-1
        loc = ui_words[random_index]['location']
        pos = [loc['left'],loc['top'],loc['left']+loc['width'],loc['top']+loc['height']]
        self.oap.tap(pos)
        #Wait for the page to finish loading
        time.sleep(5)
        self.oap.roll(0,500)
        time.sleep(1)


    def check_comments(self):
        """
        :return:After successfully opening an article, check the comment information
        """
        # Pull to the end
        for i in range(2):
            self.oap.roll(0,500)
            time.sleep(1)
        time.sleep(2)
        # Check for comments There are comments There are no comments There are ads Three cases
        ui_words_str = self.vc.get_ui_words(location=False,in_str=True,crop=CROP_RANGE['LEAVE_MSG_BOTTOM'])
        # If there is no comment, click the message button
        if UI_WORDS['NO_LEAVING_MSG'] in ui_words_str:
            print('Clicked the message. . .')
            self.oap.tap(BTN['LEAVE_MSG'])
            time.sleep(1)
            self.oap.key(KEY['BACK_KEYEVENT'])

    def get_all_req_data(self, nickname, hand=False):
        """
        Get all the requested data about a public account. The current program uses Baidu API to be limited by the network and concurrency. The effect is very satisfactory.
        :param nickname: Public name nickname
        :return:The final success depends on whether valid data is found in redis
        """
        TidyReqData.flush_data("*.req")
        redis_instance.set('current_nickname',nickname)
        self.home_to_gzh_search()
        self.search_gzh(nickname)
        if hand==False:
            self.all_message()
            self.click_a_message()
            # self.check_comments()
        else:
            input("Please manually or take parameters one by one")
        self.home()

    def get_part_req_data(self, nickname):
        """
        Request data for reads and comments only
        :param nickname:Public name nickname
        :return:The final success depends on whether valid data is found in redis
        """
        TidyReqData.flush_data()
        redis_instance.set('current_nickname',nickname)
        self.home_to_gzh_search()
        self.search_gzh(nickname)
        self.click_a_message(args=1)
        self.check_comments()
        self.home()
