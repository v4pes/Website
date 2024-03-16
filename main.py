import flask, os, json, requests, discord_oauth2, pymongo; from flask import Flask, request ; from discord_oauth2 import DiscordAuth; from pymongo import MongoClient


app = Flask(__name__)
token = os.environ['token']
client_id = 1218497796051701891
client_secret = os.environ['client_secret']
callback_url = "https://2b1375ea-9ea3-435f-b0c5-b5a5f910f0bf-00-18prs5hnxp0s5.spock.replit.dev/callback"
webhook = os.environ['webhook_url']
mongo_url = os.environ['mongo_url']

auth = DiscordAuth(client_id, client_secret, callback_url)

# https://discord.com/oauth2/authorize?client_id=1218497796051701891&response_type=code&redirect_uri=https%3A%2F%2F2b1375ea-9ea3-435f-b0c5-b5a5f910f0bf-00-18prs5hnxp0s5.spock.replit.dev%2Fcallback&scope=identify+guilds.join


@app.route('/home')
def home():
    return 'This is a home webpage test'

@app.route('/callback')
def callback():
    code = request.args.get('code')
    tokens = auth.get_tokens(code)
    access_token = tokens['access_token']
    user_data = auth.get_user_data_from_token(access_token)
    username = user_data['username']
    user_id = user_data['id']
    client = MongoClient(mongo_url)
    db = client.get_database('database')
    users_collection = db.get_collection('users')
    
    insert = users_collection.insert_one({'user_id': user_id, 'username': username, 'access_token': access_token})
    
    fields = [
    {'name': 'Username:', 'value': username, 'inline': True},
    {'name': 'User ID:', 'value': user_id, 'inline': True},
    {'name': 'Access Token:','value': access_token, 'inline': True}
    ]
    embed = {
    "title": "New Auth",
    "description": "A new Auth has been successfully added to the database",
    "color": 0xf3136,
    "fields": fields
    }
    payload = {
    "embeds": [embed]
    }
    json_payload = json.dumps(payload)
    r = requests.post(webhook, data=json_payload, headers={'Content-Type': 'application/json'})
    return 'Authorized'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
