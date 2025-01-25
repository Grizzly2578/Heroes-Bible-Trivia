import json
import flask
from flask import Flask, render_template, request
from threading import Thread

with open("save.json", "r") as f:
  users = json.load(f)


  
app = Flask('')



@app.route('/', methods=['GET'])
def home():
  return "Rise You Monstrosity!"

# @app.route("/interactions")
# @app.route("/interactions/")
# def interactions_():
#   data = request.form.get()
#   print(data)
#   return data
  
# Website Endpoints

@app.route('/shop')
@app.route('/shop/')
def shop():
  return "Hello This website is still work in progress"
  
# API Endpoints
@app.route('/api/')
@app.route('/api')
def api():
  return render_template("index.html")

# @app.route('/api/interactions')
# def interactions():
#     print(flask.request.data)
#     return ""

@app.route('/api/test')
def test():
  return render_template("_index.html")

@app.route('/api/user/', methods=['GET'])
@app.route('/api/user', methods=['GET'])
def api_users():
  with open("save.json", "r") as f:
    users = json.load(f)
  return users

@app.route('/api/user/<user>/', methods=['GET'])
@app.route('/api/user/<user>', methods=['GET'])
def api_user(user):
  with open("save.json", "r") as f:
    users = json.load(f)
  if user not in users:
    return "Unkown User"
  else:
    return {user:users[user]}

@app.route('/api/shop/', methods=['GET'])
@app.route('/api/shop', methods=['GET'])
def api_shop():
  with open("shop.json", "r") as f:
    shop = json.load(f)
  return shop

@app.route('/api/shop/<item>/', methods=['GET'])
@app.route('/api/shop/<item>', methods=['GET'])
def api_shop2(item):
  with open("shop.json", "r") as f:
    shop = json.load(f)
  if item.upper() not in shop:
    return shop
  else:
    return {item.upper():shop[item.upper()]}
    
def run():
  app.run(host='0.0.0.0',port=8082)



def keep_alive():
    t = Thread(target=run)
    t.start()