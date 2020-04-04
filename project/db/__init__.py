from instance import db_instance


"""
Define the fields of a public number article in mongodb
"""
article_scheme = {
    "nickname"          : "" ,#Public name nickname string
    "title"             : "" ,#Article title string
    "article_id"        : 0  ,#Article id of a public account int
    "content_url"       : "" ,#Article real url url
    "source_url"        : "" ,#Article URL url
    "digest"            : "" ,#Artificial summary string
    "machine_digest"    : "" ,#Automatic summary string
    "cover"             : "" ,#Cover url url
    "p_date"            : 0  ,#release time datetime
    "with_ad"           : False ,#With or without ads bool
    "pic_num"           : 0 ,#Number of illustrations int
    "video_num"         : 0 ,#Number of videos int
    "read_num"          : 0 ,#Reading int
    "like_num"          : 0 ,#Likes int
    "comment_id"        : "" ,#Comment id string
    "comment_num"       : 0 ,#Number of reviews int
    "comments"          : {} ,#Featured review content dict
    "reward_num"        : 0 ,#Praise quantity int
    "author"            : "" ,#Author string
    "mov"               : 0 ,#Main vice int
    "title_emotion"     : 0 ,#Title emotion int
    "title_token"       : [] ,#Title participle list
    "title_token_len"   : 0 ,#Participle length int
    "human_digest_token": [] ,#Artificial summary word segmentation list
    "article"           : "" ,#Text content markdown
    "article_token"     : [] ,#Text segmentation list
    "article_token_len" : 0 ,#Text segmentation length int
    "c_date"            : 0 ,#Crawl time
}

def update_article_from_template(article_seg):
    """
    :param article_seg: Contains part or all of an article
    :return:Extract data in article_seg based on the fields specified in article_scheme
    """
    article = {}
    for key in article_scheme:
        if key in article_seg:
            article[key] = article_seg[key]
    return article


def insert_one(nickname, article):
    """
    :param nickname:
    :param article: dict data
    :return: insert a public account article data in the nickname collection
    """
    col = db_instance[nickname]
    return col.insert_one(article).inserted_id

def update_one(nickname, articel):
    """
    :param nickname:
    :param articel:
    :return: Update article data based on content_url in article
    """
    op_result = ''
    # The deleted article does not have the content_url attribute and returns directly to the bureau
    if articel["content_url"] is "":
        op_result = 'ERROR'
        return op_result
    col = db_instance[nickname]
    result = col.find_one({"content_url":articel['content_url']})
    if type(result) is dict:
        # Data can be updated
        col.update_one({"content_url":articel['content_url']},
                       {"$set":articel})
        op_result = 'UPDATE'
    else:
        # Data does not exist call insert
        insert_one(nickname, articel)
        op_result = 'INSERT'
    return op_result


def insert_many(nickname, articles, check_exist=True):
    """
    :param nickname:
    :param articles:article lsit
    :param check_exist: if not need to determine weight based on content_url
    :return: insert a list of articles in the nickname collection
    """
    # Whether there are updated records
    has_update = False
    if check_exist==False:
        col = db_instance[nickname]
        col.insert_many(articles)
    else:
        for article in articles:
            result = update_one(nickname, article)
            if result == 'UPDATE':
                has_update = True
    return has_update


def count(nickname):
    """
    :param nickname:
    :return: Count the number of articles in the current public account
    """
    return db_instance[nickname].count()


def delete(nickname, **kwargs):
    """
    :param nickname:
    :param kwargs: Dictionary filter
    :return: Delete articles according to the matching information provided in match
    """
    col = db_instance[nickname]
    col.delete_many(kwargs)


def find_one(nickname,content_url):
    """
    :param nickname:
    :param content_url:
    :return:
    """
    col = db_instance[nickname]
    result = col.find_one({'content_url':content_url})
    return result


def drop_collection(nickname):
    """
    :param nickname:
    :return: Delete collection
    """
    db_instance.drop_collection(nickname)
    return nickname


def get_collection_article(nickname,**kwargs):
    """
    :param nickname: 
    :param kwargs: For example, find all the data where the article field does not exist {"article": {"$ exists": False}}
    :return: Returns all or part of the data of a public account in the form of a generator
    """
    col = db_instance[nickname]
    articles = col.find(kwargs)
    for article in articles:
        yield article

class WeixinDB():
    """
    Provide methods for all WeChat data, visible to all programs
    """
    def __init__(self):
        pass

    @staticmethod
    def get_all_nickname(is_count=False):
        """
        :param is_count:Do you need to calculate the amount of data in the collection
        :return: A public number is a collection that returns all collection names
        """
        nicknames = db_instance.collection_names()
        if is_count is False:
            return nicknames
        else:
            nicknames_count = []
            for nickname in nicknames:
                nicknames_count.append((nickname,count(nickname)))
        return nicknames_count
