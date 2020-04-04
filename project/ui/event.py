from ui.ui_instance import socketio
from ui import gc,gzh_category,gzh_setting
from tools.utils import str_to_dict,debug_p
from instance.global_instance import gs


@socketio.on('my_event')
def handle_message(json):
    print('received message: ' + str(json))
    return 'frank'


@socketio.on('connect')
def handle_message_connected():
    # Public account group setting
    cat_data = gzh_category.get_all_cat_data()
    socketio.emit('gzh_category',cat_data)
    # search settings
    search_setting_data = gzh_setting.get_all_settings()
    socketio.emit('search_setting',search_setting_data)
    # Completed public number
    report_data = gc.report_gzh_finished()
    socketio.emit('gzhs_list_data',report_data)
    # Reptile information
    report_data = gc.report_crawler()
    socketio.emit('phone_crawler_data',report_data)


# search for
@socketio.on('search_gzh')
def search_gzh(data):
    search_data = data['search_data']
    page_info = data['page_info']
    from es.view import search_result_pretty
    # Find the list of public numbers to search according to the settings
    nicknames = gzh_setting.search_range_data_preprocess(gzh_category)
    result = gs.search(nicknames=nicknames ,search_data=search_data, from_size=page_info)
    if result == "ERROR":
        return
    result = search_result_pretty(result)
    socketio.emit('search_reult_page',result)


# Add public number
@socketio.on('gzhs_todolist_add')
def on_gzhs_todolist_add(data):
    data = str_to_dict(data,'&','=')
    gc.add_gzh(data)
    report_data = gc.report_gzh_doing()
    socketio.emit('gzhs_todolist_data',report_data)


# Add mobile WeChat crawler
@socketio.on('phone_crawler_add')
def on_phone_crawler_add(data):
    print("click on_phone_crawler_add")
    data = str_to_dict(data,'&','=')
    gc.add_crawler(data)
    report_data = gc.report_crawler()
    socketio.emit('phone_crawler_data',report_data)


# Delete mobile WeChat crawler
@socketio.on('phone_crawler_delete')
def on_phone_crawler_delete(data):
    print("click on_phone_crawler_delete")
    gc.delete_crawler(data)
    report_data = gc.report_crawler()
    socketio.emit('phone_crawler_data',report_data)

# Add public account category
@socketio.on('add_gzh_category')
def add_gzh_category(data):
    cat_name = data
    cat_data = gzh_category.add_cat(cat_name=cat_name)
    socketio.emit('gzh_category',cat_data)


# Delete category
@socketio.on('delete_gzh_category')
def delete_gzh_category(data):
    cat_name = data
    cat_data = gzh_category.delete_cat(cat_name=cat_name)
    socketio.emit('gzh_category',cat_data)


# Public number category
@socketio.on('add_gzh_to_category')
def add_gzh_to_category(data):
    cat_name_raw = data['cat_name_raw']
    nickname = data['nickname']
    import re
    # The front-end select interface directly obtains cat_name, which is laborious, speaks innerhtml, passes it to the backend, and analyzes cat_name.
    cat_name = re.findall(r'data-category="\S*?">',cat_name_raw)[0].split('"')[1]
    cat_data = gzh_category.add_cat_gzh(cat_name=cat_name, nickname=nickname)
    socketio.emit('gzh_category',cat_data)


# Delete category public number
@socketio.on('delete_gzh_from_category')
def delete_gzh_from_category(data):
    cat_name = data['cat_name']
    nickname = data['nickname']
    cat_data = gzh_category.delete_cat_gzh(cat_name=cat_name, nickname=nickname)
    socketio.emit('gzh_category',cat_data)


# Remove search scope element
@socketio.on('search_setting_delete_from_search_range')
def search_setting_delete_from_search_range(data):
    range_type = data['range_type']
    element_name = data['element_name']
    search_setting_data = gzh_setting.delete_from_search_range(range_type=range_type,name=element_name)
    socketio.emit('search_setting',search_setting_data)


# Increase search scope element
@socketio.on('search_setting_add_to_search_range')
def search_setting_add_to_search_range(data):
    range_type = data['range_type']
    element_name = data['element_name']
    search_setting_data = gzh_setting.add_to_search_range(range_type=range_type,name=element_name)
    socketio.emit('search_setting',search_setting_data)


# Change range type
@socketio.on('search_setting_change_range_type')
def search_setting_change_range_type(data):
    range_type = data['range_type']
    search_setting_data = gzh_setting.change_search_range_type(range_type)
    socketio.emit('search_setting',search_setting_data)


# Request index chart option data for the current search data
@socketio.on('search_result_index')
def search_result_index(data):
    search_data = data['cur_search_data']
    # Find the list of public numbers to search according to the settings
    nicknames = gzh_setting.search_range_data_preprocess(gzh_category)
    data = gs.search_get_all(nicknames,search_data,source=['p_date'])
    from es.trend import articles_and_time,draw_bar
    x,y = articles_and_time(raw_data=data)
    chart_option = draw_bar(x,y,search_data)
    socketio.emit("search_result_index",chart_option)


def refresh_report_data():
    import time
    while True:
        # Completed public number
        # report_data = gc.report_gzh_finished()
        # socketio.emit('gzhs_list_data',report_data)
        # Public number being processed
        report_data = gc.report_gzh_doing()
        socketio.emit('gzhs_todolist_data',report_data)
        # Reptile information
        report_data = gc.report_crawler()
        socketio.emit('phone_crawler_data',report_data)
        time.sleep(1)
