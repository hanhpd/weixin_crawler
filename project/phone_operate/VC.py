from phone_operate.OCR import OCR
from phone_operate.PhoneControl import PhoneControl
import numpy as np


class VC(PhoneControl, OCR):
    """
    Click_by_loc and click_by_words are the most important external interfaces based on the given text or location information.
    """
    def __init__(self, phone):
        """
        :param phone:adb Port information needed to operate the phone
        """
        # I don't understand the writing.Refer to https://stackoverflow.com/questions/11179008/python-inheritance-typeerror-object-init-takes-no-parameters
        PhoneControl.__init__(self,phone=phone)

    def click_by_words(self,words,tap=True):
        """
        Click on the area where the specified words are located
        :param words:Target text
        :return:Actual clicked position
        """
        # Screenshot
        pic_name = self.get_screen_cap()
        # COR identifies ui_words
        ui_words = VC.ocr(pic_name ,location=True)
        # Find the most similar based on words
        prob, loc_words = VC.find_position(ui_words, words)
        # Click
        loc = loc_words['location']
        pos = [loc['left'],loc['top'],loc['left']+loc['width'],loc['top']+loc['height']]
        if tap is True:
            self.input_tap(pos)
        return pos

    def click_by_loc(self,pos):
        """
        Tap the screen according to the location of the area
        :param pos:Upper-left and lower-right coordinates of the area
        :return:
        """
        acture_pos = self.input_tap(pos)
        return acture_pos

    def get_ui_words(self,location=False,in_str=False,crop=None):
        # Screenshot
        pic_name = self.get_screen_cap()
        # COR identifies ui_words
        ui_words = VC.ocr(pic_name ,location=location, crop=crop)
        # If you don't need position information, you need to return all UI interface characters with a string
        if location==False and in_str==True:
            ui_words_str = ''
            for words in ui_words:
                ui_words_str += words['words']
            ui_words = ui_words_str
        return ui_words

    def x_ray(self, keys, crop=None):
        """
        Return a list of their positions according to the given keywords and give a similarity greater than 0.9
        :param keys:('key1','key2',...)
        :param crop:Focus cropping area The information in the tuple is (left, upper, right, lower) The upper left corner is the origin
        :return:{'key1':{'pos':[x1,y1,x2,y2],'prob':0.998},'key1':{'pos':[x1,y1,x2,y2],'prob':0.998},...}
        """
        x_ray_data = {}
        # Screenshot
        pic_name = self.get_screen_cap()
        # Get ui_words of pictures
        ui_words = VC.ocr(pic_name ,location=True, crop=crop)
        for key in keys:
            x_ray_data[key] = {}
            # Find most similar words
            prob, loc_words = VC.find_position(ui_words, key)
            loc = loc_words['location']
            # Length and width are converted to the lower right corner coordinates
            pos = [loc['left'],loc['top'],loc['left']+loc['width'],loc['top']+loc['height']]
            x_ray_data[key]['pos'] = pos
            x_ray_data[key]['prob'] = prob
        return x_ray_data

    @staticmethod
    def ui_words2vocb(ui_words):
        """
        Get dictionary based on screenshot text information for next creation of one_hot vector
        :param ui_words:Results from ocr
        :return:Dictionary for now without stop words
        """
        vocab = ''
        for words in ui_words:
            vocab+=words['words']
        vocab = set(vocab)
        return vocab

    @staticmethod
    def find_position(ui_words, dest_words):
        """
        According to the ui_words identified by cor, find the location most similar to the specified target dest_words
        :param ui_words:
        :param dest_words:
        :return:The first return value is the similarity, and the second return value is the corresponding OCR information, including text and location information.
        0.998, {'location': {'width': 119, 'top': 1863, 'left': 345, 'height': 40}, 'words': 'Address book'}
        """
        vocab = VC.ui_words2vocb(ui_words)
        dictionary = list(vocab)
        vec_len = len(dictionary)
        keys = range(vec_len)
        dictionary = dict(zip(dictionary, keys))
        # Calculate the one-hot vector of words in each row of the UI interface
        ui_words_vec = []
        for words in ui_words:
            words_vec = np.zeros(vec_len)
            for word in words['words']:
                words_vec[dictionary[word]]+=1
            ui_words_vec.append(words_vec)
        ui_words_vec = np.array(ui_words_vec)

        # One-hot word vector based on dictionary computer target words
        dest_words_vec = np.zeros(vec_len)
        for word in dest_words:
            if word not in dictionary:continue
            dest_words_vec[dictionary[word]]+=1

        #Calculate cosine angle
        cos_sim = []
        for vec in ui_words_vec:
            cs = VC.cos_sim(dest_words_vec,vec)
            cos_sim.append(cs)

        #Finding the most likely click locations
        max_index = cos_sim.index(max(cos_sim))
        return cos_sim[max_index], ui_words[max_index]

    @staticmethod
    def cos_sim(a,b):
        """
        Calculate the cosine similarity of two vectors, the closer the result is to 1, the more similar
        :param a:
        :param b:
        :return:
        """
        cs = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
        return cs
