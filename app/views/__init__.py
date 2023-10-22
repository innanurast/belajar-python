from flask import Flask

def create_app():
    app = Flask(__name__) #cara memanggil flask __name__

    return app