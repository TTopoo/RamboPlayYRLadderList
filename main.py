import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
from gevent import pywsgi

app = Flask(__name__, static_folder='static')
game_version = 0

def getLadderApiInfo(seasonId, pageNum, version):
    url = "https://api.ok-skins.com/battlecenter/qualifying/v1/rank?seasonId=" + str(seasonId) + "&pageNum=" + str(pageNum) + "&pageSize=15&startRank=0&version=" + str(version)
    print(seasonId, pageNum, version)
    response = requests.get(url)
    data = response.json()
    return data

@app.route('/getGameVersion')
def getGameVersion():
    global game_version
    game_version = request.args.get('gameVersion', type=int, default=0)
    page = request.args.get('page', type=int, default=1)
    
    print(game_version, page)
    return jsonify({'game_version': game_version})

@app.route('/')
def index():
    data = getLadderApiInfo(seasonId=14, pageNum=1, version=game_version)
    rankings = data["data"]["list"]
    data = getLadderApiInfo(seasonId=14, pageNum=2, version=game_version)
    rankings += data["data"]["list"]
    
    return render_template('index.html', rankings=rankings)

@app.route('/getMoreData')
def getMoreData():
    # 获取更多的排名数据
    page = request.args.get('page', type=int, default=1)
    
    data = getLadderApiInfo(seasonId=14, pageNum=page, version=game_version)
    rankings = data["data"]["list"]
    data = getLadderApiInfo(seasonId=14, pageNum=page+1, version=game_version)
    rankings += data["data"]["list"]

    return render_template('rankings_partial.html', rankings=rankings)

server = pywsgi.WSGIServer(('0.0.0.0', 5005), app)
server.serve_forever()