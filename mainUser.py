from flask import Flask

flaskApp = Flask(__name__)

if __name__ == '__main__':
    from api.tasks.user import *
    flaskApp.run(host='127.0.0.1', port=5000, use_reloader=True)
