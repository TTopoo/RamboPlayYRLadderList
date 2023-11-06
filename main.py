import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
from gevent import pywsgi

app = Flask(__name__, static_folder='static')
game_version = 0

@app.route('/getGameVersion')
def getGameVersion():
    global game_version
    game_version = request.args.get('gameVersion', type=int, default=0)
    page = request.args.get('page', type=int, default=1)
    
    print(game_version, page)
    return jsonify({'game_version': game_version})

@app.route('/')
def index():
    url = "https://api.ok-skins.com/battlecenter/qualifying/v1/rank?seasonId=14&pageNum=1&pageSize=15&startRank=0&version=" + str(game_version)
    response = requests.get(url)
    data = response.json()
    rankings = data["data"]["list"]
    print(url)
    return render_template('index.html', rankings=rankings)

@app.route('/getMoreData')
def getMoreData():
    # 获取更多的排名数据
    page = request.args.get('page', type=int, default=1)
    
    url = "https://api.ok-skins.com/battlecenter/qualifying/v1/rank?seasonId=14&pageNum=" + str(page) + "&pageSize=15&startRank=0&version=" + str(game_version)
    response = requests.get(url)
    data = response.json()
    rankings = data["data"]["list"]
    print(url)
    return render_template('rankings_partial.html', rankings=rankings)

server = pywsgi.WSGIServer(('0.0.0.0', 5005), app)
server.serve_forever()