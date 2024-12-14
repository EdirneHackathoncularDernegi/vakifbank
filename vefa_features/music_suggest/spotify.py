import requests
import json

# Spotify API Access Token (OAuth üzerinden alınmış olmalı)
ACCESS_TOKEN = "BQChrKFVHTh5apV8JXmTu4S9wG88UrSNYxms0od8B0DEDr-7wW4kYwlGKY1rb-eg_gYwrzoT97m2lZXfUiX2T0Y6y6IRhIjvEV-i0qbf8QwyhzErRwF77tZZAjjB4m1B0Lw4yVY83SwZDFWmVWzGtjfaXQM_VPfcki1Miyk5UaqKJq6HIfboxkr1OhtPIW4u9aku2iE8MJ8heo7qKnv9ew"

# 1. Kullanıcının en çok dinlediği sanatçıları getir
def get_top_artists():
    url = "https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=10"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        artists = []
        for artist in data['items']:
            artists.append({
                "name": artist['name'],
                "genres": artist['genres']
            })
        return artists
    else:
        print(f"Error: {response.status_code} - {response.json()}")
        return []

# 2. Kullanıcının en çok dinlediği parçaları getir
def get_top_tracks():
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=10"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        tracks = []
        for track in data['items']:
            tracks.append({
                "name": track['name'],
                "artist": track['artists'][0]['name']
            })
        return tracks
    else:
        print(f"Error: {response.status_code} - {response.json()}")
        return []

# 3. Kullanıcının son dinlediği parçaları getir
def get_recently_played():
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=10"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        recent_tracks = []
        for item in data['items']:
            track = item['track']
            recent_tracks.append({
                "name": track['name'],
                "artist": track['artists'][0]['name']
            })
        return recent_tracks
    else:
        print(f"Error: {response.status_code} - {response.json()}")
        return []

# 4. Kullanıcının müzik zevkini analiz et
def analyze_user_music():
    print("Kullanıcının En Çok Dinlediği Sanatçılar:")
    artists = get_top_artists()
    for artist in artists:
        print(f"Sanatçı: {artist['name']}, Türler: {', '.join(artist['genres'])}")
    
    print("\nKullanıcının En Çok Dinlediği Parçalar:")
    tracks = get_top_tracks()
    for track in tracks:
        print(f"Şarkı: {track['name']} - Sanatçı: {track['artist']}")
    
    print("\nKullanıcının En Son Dinlediği Parçalar:")
    recent_tracks = get_recently_played()
    for track in recent_tracks:
        print(f"Şarkı: {track['name']} - Sanatçı: {track['artist']}")

# Kullanıcı müzik analizini çalıştır
if __name__ == "__main__":
    analyze_user_music()
