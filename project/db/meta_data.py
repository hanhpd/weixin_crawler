from instance import db_instance
from copy import copy
col = db_instance['crawler_metadata']
"""
Used to record the update history of a public account, the update date, 
the number of loadings of the historical article list (one is usually a 10-day posting list), and the total number of articles
"""
meta_data_scheme = {
    "nickname"          : "",# Public Account Nickname
    "update_log_list"    : "",# date,deepth,article_num
}


def insert_article_metadata(nickname, update_log):
    """
    :param nickname: Updated public nickname
    :param update_log: Update verbose log
    :return: One public account occupies one line of records
    """
    metadata = col.find_one({'nickname':nickname})
    if type(metadata) is dict:
        metadata['update_log_list'].append(update_log)
        col.update_one({'nickname':nickname},{"$set":metadata})
    # metadata does not exist
    else:
        metadata = copy(meta_data_scheme)
        metadata['nickname'] = nickname
        metadata['update_log_list'] = [update_log]
        col.insert_one(metadata)


def get_article_metadata(nickname=None, all=True):
    """
    :param nickname:Specify the account log None for all accounts
    :param all:True all logs False: Last updated log
    :return: Get the log information of the public account article flat crawl
    """
    data = {}
    metadata = []
    if nickname is not None:
        metadata = [col.find_one({'nickname':nickname})]
    else:
        for md in col.find():
            metadata.append(md)
    for item in metadata:
        if all:data[item['nickname']] = item['update_log_list']
        else :data[item['nickname']] = item['update_log_list'][-1]
    return data


def delete_article_metadata(nickname):
    """
    :param nickname: Public name nickname
    :return: Delete the WeChat crawl log information of the specified public account
    """
    col.delete_one({'nickname':nickname})


def update_history():
    """
    :return:Create metadata by manually crawling articles for this before
    """
    from db import WeixinDB
    from datetime import datetime
    wxdb = WeixinDB()
    nicknames = wxdb.get_all_nickname(is_count=True)
    for item in nicknames:
        if item[0] not in ['queue','crawler_metadata']:
            insert_article_metadata(item[0],{'date':datetime.now(),'articles_num':item[1]})


if __name__ == "__main__":
    update_history()
