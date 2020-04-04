# Chinese and English mixed string to extract the first letters of Chinese characters and retain all non-Chinese characters
def to_pinyin(ch_name):
    """
    Turn Blending into Searching for Pinyin Characters
    INPUT 'Hangzhou frank1 lakeside Intime in77'
    OUTPUT 'hzfrank1hbytin77'
    """
    from pypinyin import lazy_pinyin
    import re
    d1 = re.sub(r'[a-zA-Z0-9]+',' ',ch_name)
    d2 = re.findall(r'[a-zA-Z0-9]+',ch_name)
    d3 = lazy_pinyin(d1)
    d4 = []
    i=0
    for d in d3:
        if d == ' ':
            d4.append(d2[i])
            i+=1
        else:
            d4.append(d[0])
    d4 = ''.join(d4)
    return d4

def to_pinyin_full(ch_name):
    from pypinyin import lazy_pinyin
    return '_'.join(lazy_pinyin(ch_name), )

# String to dictionary support for custom key-value spacers and member spacers
def str_to_dict(s, join_symbol="\n", split_symbol=":"):
    """
    The key and value are connected by split_symbol, and the key and value pairs are connected by join_symbol
    For example: a = b & c = d join_symbol is &, split_symbol is =
    :param s: Original string
    :param join_symbol: Joiner
    :param split_symbol: Delimiter
    :return: dictionary
    """
    s_list = s.split(join_symbol)
    data = dict()
    for item in s_list:
        item = item.strip()
        if item:
            k, v = item.split(split_symbol, 1)
            data[k] = v.strip()
    return data

# Dictionary to string
def dict_to_str(data, join_symbol="&", split_symbol="="):
    s = ''
    for k in data:
        s += str(k)+split_symbol+str(data[k])+join_symbol
    return s[:-2]

# String to dictionary
def dictstr_to_dict(str_data):
    import ast
    return ast.literal_eval(str_data)

# Configure log print format
import logging
from configs import LOGGING_LEVEL
logging_level = {
    'CRITICAL':logging.CRITICAL,
    'FATAL':logging.FATAL,
    'ERROR':logging.ERROR,
    'WARNING':logging.WARNING,
    'WARN':logging.WARN,
    'INFO':logging.INFO,
    'DEBUG':logging.DEBUG,
    'NOTSET':logging.NOTSET,
}
logging.basicConfig(
    format = '%(asctime)s %(levelname)-4s %(message)s',
    level=logging_level[LOGGING_LEVEL],
    datefmt='%d %H:%M:%S')

#Align printing and control print depth through depth
import pprint
pp = pprint.PrettyPrinter(depth=3)
debug_p = pp.pprint


def sub_list(whole_list, part_list):
    """
    :param whole_list:
    :param part_list:
    :return:Find elements other than part_list from the whole list, form a sublist and return
    """
    return [x for x in whole_list if x not in part_list]
