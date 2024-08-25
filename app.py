from flask import Flask, render_template, request, redirect, url_for, session, flash, abort,jsonify
from urllib.parse import urlparse
import db
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from markupsafe import escape

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "SUPER-SECRET"
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"], storage_uri="memory://")
app.config['SESSION_COOKIE_HTTPONLY'] = False








#-------------------------------------------------------------------
if __name__ == '__main__':
    db.user_db(connection)
    db.product_db(connection)
    db.seed_admin_user(connection)
    app.run(debug=True)