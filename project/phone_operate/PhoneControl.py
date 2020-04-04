from os import system
import random
from threading import Thread


def connect_phone(func):
    """
    The decorator is responsible for connecting the phone before each command
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        system('adb connect '+args[0].phone)
        return func(*args, **kwargs)
    return wrapper


class PhoneControl():
    def __init__(self, phone):
        """
        :param phone:adb Port information needed to operate the phone
        """
        self.phone = phone

    def get_phone(self):
        """
        Get instance phone port information
        """
        return self.phone

    @connect_phone
    def get_screen_cap(self, file_name='screen_cap'):
        """
        Take screenshot
        """
        system('adb -s '+str(self.phone)+' shell screencap -p /sdcard/'+file_name+'.png')
        system('adb -s '+str(self.phone)+' pull /sdcard/'+file_name+'.png'+' ./'+file_name+'.png')
        return file_name+'.png'

    @connect_phone
    def input_tap(self, pos):
        """
        Tap the screen
        pos is the upper-left and lower-right coordinates of a region
        If the pos has been randomized beforehand, it can be just a point. Randomly clicking a position is to prevent being considered as a robot.
        Back to actual click location
        """
        if len(pos) == 2:_pos = pos
        else : _pos = (random.randint(pos[0],pos[2]),random.randint(pos[1],pos[3]))
        command = r'adb -s '+str(self.phone)+' shell input tap {} {}'.format(_pos[0],_pos[1])
        system(command)
        return _pos

    @connect_phone
    def input_swipe(self, x1, x2):
        """
        Swipe from one position to another
        :param x1:Start coordinate, origin is the upper left corner of the screen
        :param x2:End point coordinates, the upper left corner of the screen is the origin
        :return:[x1,x2]
        """
        command = r'adb -s '+str(self.phone)+' shell input swipe {} {} {} {}'.format(x1[0],x1[1],x2[0],x2[1])
        system(command)
        return [x1,x2]

    @connect_phone
    def input_roll(self, dx=0, dy=500):
        """
        Pull the screen
        :param dx:Speed in x direction
        :param dy:Speed in y direction
        :return:[dx, dy]
        """
        command = r'adb -s '+str(self.phone)+' shell input roll {} {}'.format(dx,dy)
        system(command)
        return [dx,dy]

    @connect_phone
    def input_key_event(self, event_cmd):
        """
        Key events such as home menue back volum_up volum_down etc. are defined in the configuration file.
        :param event_cmd:Event ID
        :return:event_cmd
        """
        command = r'adb -s '+str(self.phone)+' shell input keyevent '+event_cmd
        system(command)
        return event_cmd

    @connect_phone
    def input_text(self, text):
        """
        Enter text information May not support Chinese input
        :param text:Text information to be entered
        :return:Text message
        """
        command = r'adb -s '+str(self.phone)+' shell input text {}'.format(text)
        system(command)
        return text

    @connect_phone
    def input_chn(self, text):
        """
        Support Chinese You need to set the ADB keyboard as the default input method and open the soft keyboard in advance
        :param text:Text information to be entered
        :return:Text message
        """
        # adb -s 127.0.0.1:62001 shell am broadcast -a ADB_INPUT_TEXT --es msg "Mighty division"
        # command = r'adb -s '+str(self.phone)+' shell am broadcast -a ADB_INPUT_TEXT --es msg {}'.format(text)
        command = r'adb -s '+str(self.phone)+' shell am broadcast -a ADB_INPUT_TEXT --es msg {}'.format(text)
        system(command)
        return text


class OperateAllPhone():
    """
    Control all phones at a given abd port at the same time
    """
    def __init__(self, phone_list):
        """
        :param phone_list:
        """
        self.phone_list = phone_list
        self.pcs = []
        for ap in self.phone_list:
            self.pcs.append(PhoneControl(ap))


    def key(self, event):
        self.operate_all("input_key_event", (event,))

    def text(self, str_data):
        self.operate_all("input_chn", (str_data,))

    def swap(self, x1, x2):
        self.operate_all("input_swipe", (x1,x2))

    def roll(self, dx, dy):
        self.operate_all("input_roll", (dx,dy))

    def tap(self, pos):
        self.operate_all("input_tap", (pos,))

    def print_menue(self):
        menu = {
            "1":"key (3 back to 4 desktop)",
            "2":"text Enter text",
            # "3":"swipe screen",
            # "4":"roll",
            # "5":"tap touch",
            "6":"quit",
        }
        while True:
            for i in menu:
                print(i, menu[i])
            cmd = input("Enter digital instructions:")
            print(cmd,'-'*10)
            cmd = cmd.split(' ')
            operation = menu[cmd[0]].split(' ')[0]
            if operation == "quit":
                return
            args = cmd[1]
            print(operation, args)
            self.__getattribute__(operation)(args)


    def operate_all(self, operation, args):
        """
        :param operation: PhoneControl instance method string name
        :param args:tuple format parameter
        :return:
        """
        _tasks = []
        for pc in self.pcs:
            _tasks.append(Thread(target=pc.__getattribute__(operation), args=args))
        for t in _tasks:
            t.start()
        for t in _tasks:
            t.join()
        return operation
