"""
Implemented the redis and mongodb queue APIs. The APIs are not consistent. Actually, a consistent API should be provided.
"""
from datetime import datetime
from tools.utils import logging
from instance import db_instance
logger = logging.getLogger(__name__)
from instance import redis_instance
from copy import copy


# redis queue
class RQ():
    """
    Create a queue FIFO using redis
    """
    def __init__(self, q_name):
        """
        : param q_name: Create a queue and insert a __BEGIN at the beginning
        All queue names begin with re__
        """
        self.q_name = 'rq__'+q_name
        self.redis = redis_instance

    def push(self, data):
        """
        :param data:
        :return:1 means the insert was successful 1 means the object already exists
        """
        rq = self.get_rq_data()
        if data not in rq:
            self.redis.lpush(self.q_name,data)
            return 1
        return 0

    def pop(self):
        """
        :return:[] means the queue is empty
        """
        data = self.redis.rpop(self.q_name)
        try:
            rq_j_data = json.loads(data)
        except:
            if data:
                rq_j_data = data.decode('utf8')
            else:
                rq_j_data = []
        return rq_j_data

    def delete_rq(self):
        self.redis.delete(self.q_name)

    def remove(self,data):
        """
        : param data: delete the specified element based on data
        : return: delete queue
        """
        rq_list = self.get_rq_data()
        self.delete_rq()
        for item in reversed(rq_list):
            if item is not data:
                self.push(item)
        rq_list = self.get_rq_data()
        return rq_list

    def get_rq_data(self):
        """
        :return: return the inserted data
        """
        rq_b_data_list = self.redis.lrange(self.q_name,0,-1)
        rq_j_data_list = []
        for rq_b_data in rq_b_data_list:
            try:
                rq_j_data = json.loads(rq_b_data)
            except:
                rq_j_data = rq_b_data.decode('utf8')
            rq_j_data_list.append(rq_j_data)
        return rq_j_data_list


    def get_rqs(self):
        rqs = self.redis.keys("rq__*")
        return rqs


"""
Database queue
"""
data_queue_scheme = {
    "name"          : "",# Queue name
    "queue_type"    : "",# Alternate name
    "update_time"   : 0 ,# Last updated
    "length"        : 0 ,# Queue length
    "ext_data"      : {},# Additional data
    "queue"         : [],# Queue data
}

class DBQ():
    """
    Persistent database queue maintenance, a record is usually a category, a list user in the category maintains members of the category
    The main attributes of the category are meta and data. All DBQs are in the same collection. A DBQ is a record.
    A DBQ instance is queued as a record in the database
    """
    queue_name = 'queue'
    col = db_instance[queue_name]
    def __init__(self, name, queue_type):
        """
        :param name:Queue name
        :param queue_type:Queue type is usually used for identification purposes
        """
        self.name = name
        self.queue_type = queue_type
        self.queue_structure = copy(data_queue_scheme)
        # name, queue_type uniquely identifies a queue
        self.queue_structure['name'] = name
        self.queue_structure['queue_type'] = queue_type
        # Create an empty queue after initialization
        queue_data = DBQ.col.find_one({'name':self.name, 'queue_type':self.queue_type})
        if type(queue_data) is not dict:
            queue_data = copy(self.queue_structure)
            DBQ.col.insert_one(queue_data)

    def add_element(self, element):
        """
        :param element:Element data elemet is a dict must specify id attribute
        :return:Add an element
        """
        queue_data = DBQ.col.find_one({'name':self.name, 'queue_type':self.queue_type})
        # Update
        if type(queue_data) is dict:
            self.update_element(element)
        # insert
        else:
            queue_data = copy(self.queue_structure)
            queue_data['update_time'] = datetime.now()
            queue_data['length'] = 1
            queue_data['queue'] = [element]
            DBQ.col.insert_one(queue_data)
        return queue_data


    def delete_element(self, element):
        """
        :param element:Element data
        :return: Delete the element based on the id in the data
        1 indicates output success
        0 means no element matching id was found
        """
        queue_data = DBQ.col.find_one({'name':self.name, 'queue_type':self.queue_type})

        elements = queue_data['queue']
        for ele in elements:
            if ele['id'] == element['id']:
                elements.remove(ele)
                queue_data['update_time'] = datetime.now()
                queue_data['length'] -= 1
                DBQ.col.update_one({'name':self.name, 'queue_type':self.queue_type},{"$set":queue_data})
                return 1
        return 0

    def update_element(self, element):
        """
        :param element: Element data
        :return:Update the element based on the id in the data
        """
        #Get queue returns dict if present otherwise returns None
        queue_data = DBQ.col.find_one({'name':self.name, 'queue_type':self.queue_type})
        old_list = queue_data['queue']
        # Update queue based on elemet
        result = DBQ.update_dict_list_by_kv(old_list=old_list,element=element)
        queue_data['queue'] = old_list
        queue_data['update_time'] = datetime.now()
        # If it is a new element, the length will increase by 1
        if result == 2:
            queue_data['length'] += 1
        DBQ.col.update_one({'name':self.name, 'queue_type':self.queue_type},{"$set":queue_data})

    def delete_all_element(self):
        """
        :return:Empty the elements in the queue
        """
        queue_data = DBQ.col.find_one({'name':self.name, 'queue_type':self.queue_type})
        queue_data['queue'] = []
        DBQ.col.update_one({'name':self.name, 'queue_type':self.queue_type},{"$set":queue_data})

    def delete_self(self):
        """
        :return:Delete queue yourself
        """
        DBQ.col.delete_one({'name':self.name, 'queue_type':self.queue_type})

    def get_queue(self):
        """
        :return:Get queue list data
        """
        queue_data = DBQ.col.find_one({'name':self.name, 'queue_type':self.queue_type})
        return queue_data['queue']

    def set_ext_data(self, ext_data):
        """
        :param ext_data:dictionary
        :return: Set ext_data
        """
        queue_data = DBQ.col.find_one({'name':self.name, 'queue_type':self.queue_type})
        queue_data['ext_data'] = ext_data
        DBQ.col.update_one({'name':self.name, 'queue_type':self.queue_type},
                           {"$set":queue_data})

    def get_ext_data(self):
        """
        :return: Get ext_data dictionary
        """
        queue_data = DBQ.col.find_one({'name':self.name, 'queue_type':self.queue_type})
        if type(queue_data) is dict:
            return queue_data['ext_data']
        return None

    @staticmethod
    def update_dict_list_by_kv(old_list, element, key='id'):
        """
        :param key:
        :param value:
        :return:Follow a new list according to a key-value pair in a given dictionary to ensure the uniqueness of the elements in the list
        Return 0 for failure
        Return 1 for update
        Return 2 means increase
        """
        if key not in element:
            logger.warning("key does not exist to update list failed%s"%(str(key)))
            return 0
        for ele in old_list:
            if ele[key] == element[key]:
                old_list[old_list.index(ele)] = element
                return 1
        old_list.append(element)
        return 2

    @classmethod
    def get_queue_by_kv(cls, **kwargs):
        """
        :param valye:
        :return:Get the right queue with a specific key-value pair combination
        """
        queue_gen = DBQ.col.find(kwargs)
        queue_list = []
        for queue in queue_gen:
            queue_list.append(queue)
        return queue_list


    @classmethod
    def delete_all_queue(cls):
        """
        :return:Delete all queues
        """
        DBQ.col.delete_many()

    @classmethod
    def delete_queue(cls,name,queue_type):
        """
        :param name: Queue name
        :param queue_type: Queue type
        :return: Gets the queue of the specified name and type
        """
        DBQ.col.delete_one({'name':name,'queue_type':queue_type})
