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
#app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"], storage_uri="memory://")
app.config['SESSION_COOKIE_HTTPONLY'] = False


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' in session:
        
        if not session['username'] == 'admin':
            return f"Your not admin"
        
        users = db.get_all_users(connection)
        
        if request.method == 'POST':
            product = dict()
            product['name'] = request.form['product-name']
            product['price'] = request.form['product-price']
            product['description'] = request.form['product-description']
            
            product['photo'] = request.files['product-photo']
            if product['price'] <='0':
                 flash("Price should be more than zero", "danger")
                 return redirect(url_for('admin'))
            if product['photo']:
                if not validators.allowed_file_size(product['photo']):
                    return f"Unallowed size."
                elif not validators.allowed_file(product['photo'].filename):
                    return f"Unallowed extention."
            
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
                
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], product['photo'].filename)
            
            product['photo'].save(filepath)
            db.add_product(connection,product['name'],product['price'],product['description'],product['photo'].filename)

        products = db.get_all_product(connection)
        return render_template('admin.html',users = users, products = products)
    else:
        return redirect(url_for('login'))
    
@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user_button():
    if request.method == "POST":
        username = request.form['username']
        db.delete_user(connection, username)
    return redirect(url_for('admin'))

@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product_button():
    if request.method == "POST":
        product = request.form['product_name']
        db.delete_product(connection, product)
    return redirect(url_for('admin'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' in session:
        if request.method == 'GET':
            username = request.args.get('username', session['username'])
            if username != session['username']:
                return f"unauthorized"
            data = db.get_user(connection, username)
            return render_template('settings.html', data=data)
        
        elif request.method == 'POST':
            username = request.args.get('username', session['username'])
            if username != session['username']:
                return 'unathoruzed'
            
            photo = request.files.get('profile-photo')

            if photo:
                if not validators.allowed_file_size(photo):
                    return f"Unallowed size."
                elif not validators.allowed_file(photo.filename):
                    return f"Unallowed extention."
                else:
                    db.update_photo(connection, photo.filename, username)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))

            
            user_data = {
                "username": session['username'],
                "fullname": request.form.get('name'),
                "balnaced": request.form.get('balance')
            }
            db.update_user(connection , user_data)
            
            data = db.get_user(connection, username)
            flash("Updated Successfully","success")
            return render_template('settings.html', data=data) 
    else:
        return redirect(url_for('login'))
    
@app.route('/')   
def index():
    if 'username' in session:
        return render_template('index.html',user=session['username'])
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(connection, username)
        
        if user:
            if user[1] == 'admin':#admin
                if utils.is_password_match(password, user[2]):
                    session['username'] = user[1]
                    return redirect(url_for('admin'))
                    
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
            flash("Done","success")
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if 'username' in session:
        if request.method == 'POST':
            query = request.form.get('search-input')  # Get the search input from the form
            products = db.search_product(connection, query)
            
            search_query = escape(request.form['search-input'])
            
            return render_template('shop.html',products=products, search_query = search_query)
        products = db.search_product(connection, "")
        return render_template('shop.html',products=products, search_query = "")
    else:
        return redirect(url_for('login'))
        
@app.route('/product/<product_id>')
def product_detail(product_id):
    
    
    product = db.get_product(connection,product_id)
    
    
    return render_template('product.html',product=product)

@app.route('/payment/<product_id>')
def bought_product(product_id):
    if 'username' not in session:
        return 'NO Hacking'
    user = db.get_user(connection, session['username'])
    
    product = db.get_product(connection, product_id)
    
    if  user[4]==None or product[2] > user[4] :
        flash('Price not reached', "danger")
        return redirect(url_for("shop"))
    else:
        new_balance = user[4] - product[2]
        cursor = connection.cursor()
    
        query = 'UPDATE users SET balnaced = ? WHERE id=?'
        
        cursor.execute(query, (new_balance, user[0]))

        connection.commit()
        flash("Successfully Purchased","success")
        return redirect(url_for('index'))
        

@app.route('/checkout/<product_id>')
def checkout(product_id):
    product = db.get_product(connection,product_id)

    real_price = db.get_product(connection,product[1])
    
    session['Correct_MAC'] = utils.create_mac(real_price[2])
    
    return render_template('checkout.html', product_id=product[0], name=product[1], price=product[2])

@app.route('/confirm_purchase', methods=['POST'])
def confirm_purchase():
    name = request.form['name']
    price = request.form['price']
    
    Possible_Correct_MAC = utils.create_mac(price)

    if 'Correct_MAC' in session and session['Correct_MAC'] == Possible_Correct_MAC:
        return redirect(f'/payment/{name}')
    else:
        flash("Purchase Failed, Please Try Again", "danger")
        return redirect(f'/checkout/{name}')

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