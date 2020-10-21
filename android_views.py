from app import app


@app.route('/api/hello')
def example_view():
    return {"hello": "world", 
            "hell": "o'world" }