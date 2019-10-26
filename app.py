from whatsdown import app


@app.route('/')
def home_page():
    return 'Hello doge'


if __name__ == '__main__':
    app.run(debug=True)
