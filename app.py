from whatsdown import app
from flask import render_template
import vlc


@app.route('/')
def home_page():
    sad_song = vlc.MediaPlayer('whatsdown/media/chopin_funeral.mp3')
    sad_song.play()
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
