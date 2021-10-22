from flask import Flask, render_template
from blueprints.users import (
    users_blueprint as users
)

from blueprints.books import books_blueprint
import db

db.init()
app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(books_blueprint)


@app.route('/')
def index():
    return render_template(r'index.html')


if __name__ == '__main__':
    app.run()
