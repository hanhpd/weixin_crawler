from tools.data_queue import DBQ
from db.meta_data import get_article_metadata
from tools.utils import sub_list


class GZHCategory():
    """
    Manage the classification of public numbersAccept front-end messages to organize data and feedback results to the front-end
    """
    def __init__(self, queue_type='Public number classification'):
        self.queue_type = queue_type

    def get_all_cat_data(self):
        """
        :return:Returns all current classification data, mild front-end data format
        """
        category = []
        # Get the names of all the public numbers in the database Prepare for adding options
        gzh_list = list(get_article_metadata().keys())
        # Get the category name and all public numbers under that category
        queue = DBQ.get_queue_by_kv(queue_type=self.queue_type)
        for cat in queue:
            data = {}
            data['cat_name'] = cat['name']
            data['cat_members'] = []
            for mem in cat['queue']:
                data['cat_members'].append(mem['id'])
            # Find public numbers that are not in the category as options to be added
            # data['cat_available'] = [x for x in gzh_list if x not in data['cat_members']]
            data['cat_available'] = sub_list(gzh_list, data['cat_members'])
            category.append(data)
        return category

    def add_cat(self, cat_name):
        """
        :param cat_name:Category Name
        :return: Add a category
        """
        DBQ(cat_name,self.queue_type)
        return self.get_all_cat_data()

    def delete_cat(self, cat_name):
        """
        :param cat_name: Category Name
        :return:Delete a category
        """
        DBQ.delete_queue(cat_name,self.queue_type)
        return self.get_all_cat_data()

    def add_cat_gzh(self, nickname, cat_name):
        """
        :param nickname:Public name nickname
        :param cat_name:Category Name
        :return:Add a public number to the specified category
        """
        cat = DBQ(name=cat_name,queue_type=self.queue_type)
        cat.add_element({'id':nickname})
        return self.get_all_cat_data()

    def delete_cat_gzh(self, nickname, cat_name):
        """
        :param nickname:Public name nickname
        :param cat_name: Category Name
        :return:Remove a public number from the specified category
        """
        cat = DBQ(name=cat_name,queue_type=self.queue_type)
        cat.delete_element({'id':nickname})
        return self.get_all_cat_data()
