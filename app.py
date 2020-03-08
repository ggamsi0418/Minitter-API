from flask import Flask, jsonify, request, make_response
from flask.json import JSONEncoder
from functools import wraps
import json


app = Flask(__name__)
app.id_count = 1
app.users = {}
app.tweets = []  # 사용자들의 트윗을 저장할 디렉터리


def json_api(f):
    @wraps(f)
    def inner(*args, **kwds):
        r = f(*args, **kwds)
        result = make_response(json.dumps(
            r, ensure_ascii=False))
        return result
    return inner


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


@app.route("/sign-up", methods=['POST'])
@json_api
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count += 1

    return new_user


@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return '사용자가 존재하지 않습니다.', 400

    if len(tweet) > 300:
        return '300자를 초과했습니다.', 400

    app.tweets.append({
        'user_id': user_id,
        'tweet': tweet
    })

    return '', 200


@app.route('/follow', methods=['POST'])
@json_api
def follow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return '사용자가 존재하지 않습니다.', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)
    user['follow'] = list(user['follow'])

    return user


@app.route('/unfollow', methods=['POST'])
@json_api
def unfollow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_follow = int(payload['unfollow'])

    if user_id not in app.users or user_id_follow not in app.users:
        return '사용자가 존재하지 않습니다.', 400

    user = app.users[user_id]
    user['follow'] = set(user['follow'])
    user.setdefault('follow', set()).discard(user_id_follow)
    user['follow'] = list(user['follow'])

    return user
