from flask import Flask, render_template, request
import pandas as pd
import os

# Bu dosyanın bulunduğu klasörü al
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_url_path='/static', static_folder='static')
# CSV yükle
df = pd.read_csv(os.path.join(BASE_DIR, "song.csv"))
df.dropna(subset=["track_name", "track_artist", "track_album_name"], inplace=True)

# Spotify link oluştur
def get_spotify_link(track_id):
    return f"https://open.spotify.com/track/{track_id}"

# Öneri fonksiyonu
def get_mood_based_songs(mood):
    if mood == "mutlu":
        filtered = df[(df['valence'] > 0.7) & (df['energy'] > 0.7)]
    elif mood == "üzgün":
        filtered = df[(df['valence'] < 0.4) & (df['energy'] < 0.5)]
    elif mood == "sakin":
        filtered = df[(df['tempo'] < 100) & (df['acousticness'] > 0.5)]
    elif mood == "enerjik":
        filtered = df[(df['tempo'] > 120) & (df['danceability'] > 0.7)]
    elif mood == "romantik":
        filtered = df[(df["valence"] > 0.4) & (df["valence"] < 0.7) & (df["acousticness"] > 0.4) & (df["energy"] < 0.6)]
    elif mood == "yaz":
        filtered = df[(df['valence'] > 0.7) & (df['danceability'] > 0.7) & (df['energy'] > 0.6)]
    else:
        filtered = df

    result = filtered.sample(n=6) if not filtered.empty else df.sample(n=6)
    result["spotify_link"] = result["track_id"].apply(get_spotify_link)
    return result

# Ana sayfa - mood seçimi
@app.route('/')
def home():
    moods = {
        "mutlu": "😊",
        "üzgün": "😢",
        "sakin": "😌",
        "enerjik": "😎",
        "romantik": "💖",
        "yaz": "☀️"
    }
    return render_template("moods.html", moods=moods)

# Şarkı öneri sayfası
@app.route('/recommendation')
def recommendation():
    mood = request.args.get("mood")
    recommended = get_mood_based_songs(mood).to_dict(orient="records")
    return render_template("recommendation.html", songs=recommended, mood=mood)

# Yüz ifadesi sayfası
@app.route('/face')
def face():
    return render_template("face.html")

@app.route('/test')
def test():
    return "Bu sayfa çalışıyor mu?"


if __name__ == '__main__':
    app.run(debug=True)
