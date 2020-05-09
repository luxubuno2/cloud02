from math import *

from flask import  (
    Flask,
    render_template,
    request,
    g,
    session,
    redirect,
    url_for
)
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import pymongo 
from pymongo import MongoClient 



### Tạo APP
app = Flask(__name__)
#, static_url_path='', static_folder='/static'
app.secret_key = "adtekdev"

### LIÊN KẾT TỚI DB MONGO
MONGO_URI = 'mongodb+srv://tobobibo:tantran032@cluster0-8xed9.mongodb.net/test?retryWrites=true&w=majority'
cluster = MongoClient(MONGO_URI)

db =  cluster.ATN_Company

### CODE Flask - Python Web

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def  home():
    return render_template("home.html", username=session['username'], fullname=session['fullname'])

@app.route('/login', methods=['GET', 'POST'])
def  login():

    if session.get('logged_in_flag'):
        if session['logged_in_flag']:
            return redirect(url_for('home'))

    query_parameters = request.args
    vusername = query_parameters.get("username")
    vpassword = query_parameters.get("password")

    collection = db.account
    ### ch-eck Account / Tài khoản USER
    results = collection.find({"_id":vusername, "password": vpassword}) 


    if  results.count() == 1:
        session['logged_in_flag'] = True
        session['username'] = results[0]["_id"]
        session['fullname'] = results[0]["FullName"]
        return render_template("home.html", username=results[0]["_id"], fullname=results[0]["FullName"])
    else:
        session['logged_in_flag'] = False
        return render_template("login.html", mesg = "")

@app.route('/logout', methods=['GET', 'POST'])
def  logout():
    #if session.get('logged_in_flag'):
    if 'logged_in_flag' in session:
        session['logged_in_flag'] = False
    return ""


@app.route('/product')
def  product():
    collection = db.product 
    lproduct = collection.find()
    return render_template("product.html", productList = lproduct)


@app.route('/orderList', methods=['GET', 'POST'])
def order():
    collection = db.order 
    lorder = collection.find()
    return render_template("order.html", orderList = lorder)

@app.route('/addOrder', methods=['GET', 'POST'])
def addOrder():
    if ("shop" in request.args  and "date" in request.args and "product" in request.args and "number" in request.args):
        shop = request.args.get("shop")
        date = request.args.get("date")
        product = request.args.get("product")
        num = request.args.get("number")
        newOrder = {"shop" : shop, "date" : date, "product": product, "number": num}
        collection = db.order 
        collection.insert_one(newOrder)
    return render_template("addOrder.html")