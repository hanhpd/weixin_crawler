# import eventlet
# eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO
import redis
from configs.auth import REDIS_HOST,REDIS_PORT,REDIS_DB


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='[[',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string=']]',
    ))


# Define as a common instance object commonly used by web servers to facilitate direct import by other programs
app = CustomFlask('WeixinCrawler',template_folder="./ui/templates",static_folder="./ui/static")
# app = CustomFlask('WeixinCrawler',template_folder="./templates",static_folder="./static")
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
socketio = SocketIO(app, async_mode='gevent')
the_redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
