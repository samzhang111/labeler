from flask import Flask, render_template

from server.routes import api
from server.db import init_db

init_db()

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

@app.route('/<page>')
@app.route('/')
def index(page=None):
    return render_template('index.html')

