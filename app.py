import os

from pymongo import MongoClient
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

client = MongoClient("mongodb://localhost:27017/mongodbpeople")
db = client['mongodbpeople']

from api import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
