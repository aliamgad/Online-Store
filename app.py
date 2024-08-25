import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort,jsonify
from urllib.parse import urlparse
import db
import utils
import validators
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from markupsafe import escape

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
connection = db.connect_to_database()
app.secret_key = "3abas"
#app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"], storage_uri="memory://")
app.config['SESSION_COOKIE_HTTPONLY'] = False


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    #admin = db.get_user(connection,session['username'])
   #if not admin:
    #    return f"fuck you"
    users = db.get_all_users(connection)
       
    if request.method == 'POST':
        product = dict()
        product['name'] = request.form['product-name']
        product['price'] = request.form['product-price']
        product['description'] = request.form['product-description']
        db.add_product(connection,product['name'],product['price'],product['description'])
        
    return render_template('admin.html',users = users)  


@app.route('/setting', methods=['GET', 'POST',])
def setting():
    if 'username' in session:
        if request.method == 'GET':
            username = request.args.get('username', session['username'])
            if username != session['username']:
                return f"unauthorized"
            data = db.get_user(connection, username)
            return render_template('setting.html', data=data)
        
        elif request.method == 'POST':
            form_type = request.form.get('form_name')
            username = request.args.get('username', session['username'])
            if username != session['username']:
                return 'unathoruzed'
            if form_type == 'upload_photo':
                photo = request.files.get('profile-photo')

                if photo:
                    if not validators.allowed_file_size(photo):
                        return f"Unallowed size."
                    elif not validators.allowed_file(photo.filename):
                        return f"Unallowed extention."
                    else:
                        db.update_photo(connection, photo.filename, username)
                        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))

            elif form_type == 'update_user_data':
                user_data = {
                    #"username": session['username'],
                    "fullname": request.form.get('name'),
                    "balanced": request.form.get('balance')
                }
                db.update_user(connection , user_data)
            
            data = db.get_user(connection, username)
            return render_template('setting.html', data=data) 
    else:
        return redirect(url_for('login'))
    
@app.route('/')   
def index():
    if 'username' in session:
        #if session['username'] == 'admin':
            #return list(db.get_all_users(connection))
        #else:
            return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(connection, username)

        if user:
            if utils.is_password_match(password, user[2]):
                session['username'] = user[1]
                return redirect(url_for('index'))
            else:
                flash("Password dose not match", "danger")
                return render_template('login.html')

        else:
            flash("Invalid username", "danger")
            return render_template('login.html')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not utils.is_strong_password(password):
            flash(
                "Sorry You Entered a weak Password Please Choose a stronger one", "danger")
            return render_template('register.html')

        user = db.get_user(connection, username)
        if user:
            flash(
                "Username already exists. Please choose a different username.", "danger")
            return render_template('register.html')
        else:
            db.add_user(connection, username, password)
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

#-------------------------------------------------------------------
if __name__ == '__main__':
    db.user_db(connection)
    db.product_db(connection)
    db.seed_admin_user(connection)
    app.run(debug=True)