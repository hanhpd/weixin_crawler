from tools.data_queue import DBQ
from db.meta_data import get_article_metadata
from tools.utils import sub_list


class GZHSearchSetting():
    """
    Public number search setting service
    Interacts with the front-end settings panel, providing setting parameters for performing searches
    """
    def __init__(self, queue_type='Public account search range setting'):
        self.queue_type = queue_type
        DBQ('No public',self.queue_type)
        DBQ('category',self.queue_type)

    def get_all_settings(self):
        """
        :return:Returns all setting parameters in dictionary form, taking one of the attributes: search range as an example
        The currently selected range type, the elements that have been included and the elements that can still be included under each range type
        setting_data = {
            'search_range':{
                'current_search_range': 'Public number or category',
                'gzh_members': ['Editis', 'Editis', 'Editis', 'Editis'],
                'gzh_available': ['Adis', 'Adis', 'Adis', 'Adis'],
                'cat_members': ['Edits', 'Edits', 'Edits', 'Edits'],
                'cat_available': ['Editis', 'Editis', 'Editis', 'Editis'],
            },
        }
        """
        setting_data = {}
        setting_data['search_range'] = {}
        # Get the full public account list
        all_gzh_list = list(get_article_metadata().keys())
        all_gzh_list.append('All')
        all_cat_list = []
        # Get full directory listing
        cats = DBQ.get_queue_by_kv(queue_type='Public number classification')
        for cat in cats:
            all_cat_list.append(cat['name'])
        # Get the search scope method currently in use
        try:
            if DBQ('No public',self.queue_type).get_ext_data()['inuse'] is True:
                current_search_range = 'No public'
            else:
                current_search_range = 'category'
        except Exception as e:
            current_search_range = 'No public'
        # Get a list of public numbers for existing search scopes
        queue = DBQ.get_queue_by_kv(queue_type=self.queue_type,name='No public')[0]['queue']
        gzh_members = []
        for element in queue:
            gzh_members.append(element['id'])
        gzh_available = sub_list(all_gzh_list, gzh_members)
        # Get a list of categories in the existing range
        queue = DBQ.get_queue_by_kv(queue_type=self.queue_type,name='category')[0]['queue']
        cat_members = []
        for element in queue:
            cat_members.append(element['id'])
        cat_available = sub_list(all_cat_list, cat_members)

        setting_data['search_range']['current_search_range'] = current_search_range
        setting_data['search_range']['gzh_members'] = gzh_members
        setting_data['search_range']['gzh_available'] = gzh_available
        setting_data['search_range']['cat_members'] = cat_members
        setting_data['search_range']['cat_available'] = cat_available
        return setting_data

    def change_search_range_type(self, range_type):
        """
        :param range_type:Range type
        :return:Update search scope type
        """
        DBQ('category',self.queue_type).set_ext_data({'inuse':False})
        DBQ('No public',self.queue_type).set_ext_data({'inuse':False})
        if range_type == 'No public':
            DBQ('No public',self.queue_type).set_ext_data({'inuse':True})
        elif range_type == 'category':
            DBQ('category',self.queue_type).set_ext_data({'inuse':True})
        return self.get_all_settings()

    def delete_from_search_range(self, range_type, name):
        """
        :param range_type:Range type
        :param name:Public account name or category name
        :return: Delete element from specified range update range_type after operation
        """
        if range_type == 'No public':
            DBQ('No public',self.queue_type).delete_element({'id':name})
        elif range_type == 'category':
            DBQ('category',self.queue_type).delete_element({'id':name})
        self.change_search_range_type(range_type)
        return self.get_all_settings()

    def add_to_search_range(self, range_type, name):
        """
        :param range_type:Range type
        :param name:Public account name or category name
        :return: Add element to specified range update range_type after operation
        """
        if range_type == 'No public':
            gzh_queue = DBQ('No public',self.queue_type)
            # If all are returned in the search range
            # if 'all' in self.get_all_settings () ['search_range'] ['gzh_members']: return
            # If you search in all public numbers, only 'all' is left in the queue
            if name == 'All':
                gzh_queue.delete_all_element()
            gzh_queue.add_element({'id':name})
        elif range_type == 'category':
            DBQ('category',self.queue_type).add_element({'id':name})
        self.change_search_range_type(range_type)
        return self.get_all_settings()

    def search_range_data_preprocess(self,gc):
        """
        :parameter gc:GZHCategory instance is used to get the public account member list of the existing directory
        :return:Set the parameters according to the search scope.
        """
        # According to the public number
        search_range = self.get_all_settings()['search_range']
        if search_range['current_search_range'] == "No public":
            if 'All' in search_range['gzh_members']:
                return []
            return search_range['gzh_members']
        # By category
        elif search_range['current_search_range'] == "category":
            gzhs = []
            search_cats = search_range['cat_members']
            all_cats = gc.get_all_cat_data()
            for member in search_cats:
                for cat in all_cats:
                    if member == cat['cat_name']:
                        gzhs = gzhs+cat['cat_members']
                        break
            return list(set(gzhs))
        # All
        else:
            return []
