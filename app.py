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
app.secret_key = "SUPER-SECRET"
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


#-------------------------------------------------------------------
if __name__ == '__main__':
    db.user_db(connection)
    db.product_db(connection)
    db.seed_admin_user(connection)
    app.run(debug=True)