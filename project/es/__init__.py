from tools.dp import Singleton
from es.config import doc_schema, search_template
from copy import deepcopy
from tools.utils import logging
from tools.utils import to_pinyin_full
import re
from instance import es_instance as es
from db import get_collection_article
from elasticsearch import helpers
logger = logging.getLogger(__name__)


class GZHSearch(Singleton):
    """
    Manage the index and doc of all public numbers in ES
    """
    def __init__(self):
        self.index_prefix = 'gzh'
        self.doc_type = 'gzh'

    def _index_name(self, nickname):
        """
        :param nickname:
        :return: Generate a special index name according to the pinyin of the public number nickname (the same processing logic is not added for the time being), first convert it to the pinyin form and add the prefix
        """
        return self.index_prefix+'_'+(to_pinyin_full(nickname)).lower()

    def get_all_indices(self):
        """
        :return:Get all indexes related to the public number in es
        """
        pass

    def create_index(self,nickname):
        """
        :param nickname:Pinyin of public name
        :return:Create an index for a public account, such as formatting fields and specifying search tokenizers
        Before indexing the document, you should first map the index, mainly to set the text word segmentation field.
        """
        mapping_body = {}
        mapping_body['properties'] = doc_schema
        index_name = self._index_name(nickname)
        exists = es.indices.exists(index_name)
        if exists is False:
            es.indices.create(index_name)
            es.indices.put_mapping(index=self._index_name(nickname), doc_type=self.doc_type, body=mapping_body)
            logger.info('Index% s created successfully'%(nickname))
        else:
            logger.info('index% s already exists'%(nickname))
        return index_name

    def delete_index(self, nickname):
        """
        :param nickname: Pinyin of public account nickname * Delete all index
        :return:Delete index and all doc under that index
        """
        if nickname is not "*":
            index_name = self._index_name(nickname)
        es.indices.delete(index_name)

    def index_db_docs(self, nickname):
        """
        :param nickname:Public name nickname
        :return: Get all the data of a public account from mongodb Use the bulk operation index to enter es
        """
        # Create index first
        index_name = self.create_index(nickname)
        # Get all articles of this public account from the database
        articles = get_collection_article(nickname,article={"$exists": True},title={"$exists": True})
        articles_cache = []
        # The connection of mongodb will expire after 10 minutes. The index may not be completed during the period, so all the historical articles of the public account are cached
        for article in articles:
            doc = dict((key, article[key]) for key in doc_schema)
            articles_cache.append(doc)
        # Manipulating index documents with bulk
        result = self.index_bulk(index_name,articles_cache)
        return result

    def index_docs(self, index_name, doc_dicts):
        """
        :param index_name:
        :param doc_dicts:
        :return:
        """
        for doc_dict in doc_dicts:
            self.index_doc(index_name, doc_dict)

    def doc_exist(self, index_name, doc_dict):
        """
        :param index_name: index name in es
        :param doc_dict: Document body
        :return:Document body document exists returns 1 document does not exist returns 0
        """
        # Use the link of the article to determine the existence of the document. The number of existence is 1 and the number of non-existence is 0.
        try:
            body = {
                "query":{"match_phrase":{'content_url':doc_dict['content_url']}},
            }
            result = es.count(index=index_name, doc_type=self.doc_type, body=body)['count']
        # If the index corresponding to the public number does not exist, an error occurs, which means that the article has not been indexed
        except :
            result = 0
        return result

    def index_doc(self, index_name, doc_dict):
        """
        :param index_name:index name in es
        :param doc_body:Document body
        :return:New or updated doc
        """
        doc = dict((key, doc_dict[key]) for key in doc_schema)
        # When the public account article is updated, a new article is also generated. Skip the index of the old article directly.
        if self.doc_exist(index_name, doc_dict) == 1:
            return
        try:
            es.index(index=index_name, doc_type=self.doc_type, id=doc['content_url'], body=doc)
            logger.info('Index %d %s %s'%(doc['article_id'], index_name, doc['title']))
            print('Index %d %s %s'%(doc['article_id'], index_name, doc['title']))
        except:
            logger.warning('index document failed:%s %s'%(doc['nickname'], doc['title']))

    def index_bulk(self, index_name, doc_dict_list):
        """
        :param index_name: index name in es
        :param doc_dict_list: The document list doc contains the fields that need to be indexed in es. It can also contain more fields but will be filtered out.
        :return:Using bulk for batch index API will deduplicate according to the specified _id field and support update
        """
        if self.index_prefix not in index_name:
            index_name = self._index_name(index_name)
        actions = []
        for doc_dict in doc_dict_list:
            action = {
                "_index": index_name,
                "_type": self.doc_type,
                "_id": doc_dict['content_url'],
                "_source": doc_dict
            }
            actions.append(action)
        result = helpers.bulk(es, actions)
        return result

    def delete_doc(self, nickname, url):
        """
        :param nickname:
        :param url:
        :return: Delete based on URL
        """
        index_name = self._index_name(nickname)
        es.delete(index=index_name, doc_type=self.doc_type,id=url)

    def index_all_db(self):
        from instance.global_instance import weixindb_instance
        from time import time
        gzhs = weixindb_instance.get_all_nickname()
        for nickname in gzhs:
            begin_time = time()
            print("index%s..."%(nickname))
            self.index_db_docs(nickname)
            print("index%s takes%f seconds"%(nickname, time()-begin_time))

    def search(self, nicknames, search_data, from_size={"from":0,"size":10}, source=None):
        """
        :param nicknames:List of public nicknames
        :param search_data:Search string
        :param source:Fields that need to be included in the returned data
        :return:search for
        """
        # Nickname
        indices = []
        st = deepcopy(search_template)
        dls = self.search_data_preprocess(search_data)
        st.update(dls)
        if source != None:
            st["_source"] = source
        # Updated from and size to support pagination
        try:
            st["from"] = from_size["from"]
            st["size"] = from_size["size"]
        except:
            logger.warning("from_size field error %s"%(str(from_size)))
        if nicknames == []:
            indices = 'gzh*'
        else:
            for nickname in nicknames:
                indices.append(self._index_name(nickname))

        try:
            result = es.search(index=indices, doc_type=self.doc_type, body=st)['hits']
            return result
        except Exception as e:
            logger.critical("Search error may be that some public accounts are not indexed %s"%(str(indices)))
            return "ERROR"

    def search_get_all(self,nicknames,search_data,source):
        """
        :param nicknames:
        :param search_data:
        :param fields:
        :return: Return custom fields in all records in search results
        """
        total = self.search(nicknames=nicknames, search_data=search_data,from_size={"from":0,"size":1},source=source)["total"]
        # Limit the amount of data obtained
        if total>=10000:
            total = 10000
        result_data = []
        hits = self.search(
            nicknames=nicknames,
            search_data=search_data,
            from_size={"from":0,"size":total},
            source=source)['hits']
        for hit in hits:
            result_data.append(hit['_source'])
        return result_data

    def search_data_preprocess(self, search_data):
        """
        :param search_data:
        :return: Preprocess the data to be searched Analyze the search pattern
        The data contains patterns:
        The content contained in double quotes is fully matched using match_phrase, and the content outside the double quotes is matched using word segmentation.
        Sort mode Specify the sort field and lifting method
        Example: "Must contain words" participle pattern -time-1
        Returns query, sort and other field data of the query according to the rules specified in the search data
        """
        sort_mapping = {
            "gzh":"nickname",       #Public name nickname
            "loc":"mov",            #Post location
            "author":"author",      #Author
            "time":"p_date",        #Posting time
            "read":"read_num",      #Reading
            "like":"like",          #Likes
            "comm":"comments",      #Review volume
            "reward":"reward_num",  #Praise
            "length":"article_token_len",#Article words
            "unk":"_score",         #Unknown, sorted by default score
        }
        sort_dir_mapping = {
            '0':"asc",
            '1':"desc",
        }
        # Separate search data, sort fields and sort order
        if len(re.findall('-',search_data))==2:
            part_data = search_data.split('-')
            try:
                sort_dir = sort_dir_mapping[part_data[-1]]
                sort_field = sort_mapping[part_data[-2]]
            except:
                sort_dir = sort_dir_mapping['1']
                sort_field = sort_mapping['unk']
        else:
            sort_dir = sort_dir_mapping['1']
            sort_field = sort_mapping['unk']
        search_data = search_data.split('-')[0]
        # Find out which fields must be completely included
        data_match_phrase = [x.replace('"','') for x in re.findall(r'"\S*?"', search_data)]
        data_match = search_data.replace('"','')
        # Create Elsticsearch search description data that must completely contain fields
        for x in data_match_phrase:
            data_match = data_match.replace(x,'').replace(' ','')
        query_value = {
            "bool": {
                "must": []
            }
        }
        match_phrase_item = {
            "match_phrase": {"article": ""}
        }
        match_item = {
            "match": {"article": ""}
        }
        # Create word segmentation field
        if data_match != '':
            match_item["match"]["article"] = data_match
            query_value["bool"]["must"].append(deepcopy(match_item))
        for item in data_match_phrase:
            match_phrase_item["match_phrase"]["article"]=item
            query_value["bool"]["must"].append(deepcopy(match_phrase_item))

        sort_value = [
            {
                sort_field: {
                    "order": sort_dir
                }
            }
        ]
        return {"query":query_value,"sort":sort_value}
