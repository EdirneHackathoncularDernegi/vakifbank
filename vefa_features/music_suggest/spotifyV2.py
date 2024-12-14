from flask import Flask, request, redirect, url_for, jsonify
import requests
import json
import os

app = Flask(__name__)

# Spotify Developer bilgileri
CLIENT_ID = "41b6b6d08f7f4a878a7d1bdeba94debf"
CLIENT_SECRET = "8b6bb1ee60cd41ff95e7f824de6c5ff3"
REDIRECT_URI = "http://localhost:5000/callback"

# Spotify yetkilendirme URL'si
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Kullanıcının yetkilendirme yapacağı endpoint
@app.route('/')
def home():
    auth_url = f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-top-read user-read-recently-played"
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Spotify Login</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #1db954;
                color: white;
                text-align: center;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .button {{
                background-color: #1db954;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 50px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
                cursor: pointer;
            }}
            .button:hover {{
                background-color: #1aa34a;
                box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.3);
            }}
        </style>
    </head>
    <body>
        <a href="{auth_url}" class="button">🎵 Spotify ile Giriş Yap</a>
    </body>
    </html>
    """
# Spotify'dan authorization code aldıktan sonra gelen callback
@app.route('/callback')
def callback():
    # Kullanıcıdan dönen 'code' parametresi
    code = request.args.get('code')
    if not code:
        return "Authorization failed. No code received."

    # Access token almak için POST isteği
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)

    if response.status_code != 200:
        return f"Failed to get token: {response.json()}"

    # Access token'ı al
    tokens = response.json()
    access_token = tokens.get("access_token")

    # Kullanıcıdan en çok dinlenen müzikleri al
    top_tracks = get_top_tracks(access_token)
    top_artists = get_top_artists(access_token)

    # Verileri JSON dosyasına kaydet
    data = {
        "top_tracks": top_tracks,
        "top_artists": top_artists
    }
    save_to_json(data, "spotify_data.json")

    # HTML sayfasında sekmeyi kapatan bir JavaScript kodu döndür
    return """
    <h1>Veriler Kaydedildi!</h1>
    <p>Veriler spotify_data.json dosyasına kaydedildi. Sekme otomatik olarak kapanıyor...</p>
    <script>
        setTimeout(() => {
            window.close();
        }, 2000); // 2 saniye bekle ve sekmeyi kapat
    </script>
    """

# Kullanıcının en çok dinlediği şarkıları çek
def get_top_tracks(access_token):
    url = "https://api.spotify.com/v1/me/top/tracks?limit=10"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [{"name": item['name'], "artist": item['artists'][0]['name']} for item in data['items']]
    else:
        print(f"Error fetching top tracks: {response.json()}")
        return []

# Kullanıcının en çok dinlediği sanatçıları çek
def get_top_artists(access_token):
    url = "https://api.spotify.com/v1/me/top/artists?limit=10"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [artist['name'] for artist in data['items']]
    else:
        print(f"Error fetching top artists: {response.json()}")
        return []

# JSON dosyasına veri kaydetme
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Flask uygulamasını başlat
if __name__ == '__main__':
    app.run(debug=True)
