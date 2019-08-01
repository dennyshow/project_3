import os
from flask import Flask, render_template, redirect, requ
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'diy_cookery'
app.config["MONGO_URI"] = "mongodb+srv://root:r00tUser@myfirstcluster-q10cc.mongodb.net/diy_cookery?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    return "Hello World"
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)