from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    # Redirect URI'den gelen token'ı al
    access_token = request.args.get('access_token')
    return f"Access Token: {access_token}"

if __name__ == '__main__':
    app.run(port=8888)
