import utils

def connect_to_database(name='database.db'):
    import sqlite3
    return sqlite3.connect(name, check_same_thread=False)

def user_db(connection):
    cursor = connection.cursor()

    cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL UNIQUE,
			password TEXT NOT NULL,
            fullname TEXT ,
            balnaced INTEGER,
            photo_name TEXT,
            owendproduct TEXT
        )
    ''')
    
    connection.commit()

def add_user(connection,username,password):
    cursor = connection.cursor()
    
    encripted_password = utils.hash_password(password)
    
    query = ''' INSERT INTO users (username,password) VALUES(?,?)'''
    
    cursor.execute(query, (username,encripted_password))
    
    connection.commit()

def get_user(connection,username):
    cursor = connection.cursor()
    
    query = ''' SELECT * FROM users WHERE username = ?'''
    
    cursor.execute(query,(username,))
    
    return cursor.fetchone()

def seed_admin_user(connection):##don't understand
    admin_username = 'admin'
    admin_password = 'admin'

    # Check if admin user exists
    admin_user = get_user(connection, admin_username)
    if not admin_user:
        add_user(connection, admin_username, admin_password)
        print("Admin user seeded successfully.")

def search_users(connection, search_query):#admin
    cursor = connection.cursor()
    
    query = '''SELECT username FROM users WHERE username LIKE ?'''
    
    cursor.execute(query, (f"%{search_query}%",))
    
    return cursor.fetchall()

def get_all_users(connection):#admin
    cursor = connection.cursor()
    
    query = 'SELECT * FROM users WHERE username != "admin"'
    
    cursor.execute(query)
    
    return cursor.fetchall()

def delete_user(connection, username):#admin
    cursor = connection.cursor()
    
    query = ''' DELETE FROM users WHERE username = ? '''
    
    cursor.execute(query, (username,)) 
    
    connection.commit()

def update_user(connection , user_data):
    cursor = connection.cursor()
    query = ''' UPDATE users set fullname = ? , balnaced = ? WHERE username = ? '''
    cursor.execute(query,(user_data['fullname'] , user_data['balnaced'] , user_data['username']))
    connection.commit() 

def update_photo(connection, filename , username):
    cursor = connection.cursor()  
    query = '''UPDATE users SET photo_name = ? WHERE username = ?'''
    cursor.execute(query, (filename,username))  
    connection.commit()  

#-------------------------------------------------------------------------------------------------------------
def product_db(connection):
    cursor = connection.cursor()
    
    cursor.execute('''
		CREATE TABLE IF NOT EXISTS products (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			productname TEXT NOT NULL UNIQUE,
            price INTEGER NOT NULL,
            photo TEXT,
            description TEXT
		)
	''')
    
    connection.commit()
    
def add_product(connection,productname,price,description,photo): #adminOnly #see if we remove the photo or not from the adding not in setting
    cursor = connection.cursor()
    
    query = ''' INSERT INTO products (productname,price,description,photo) VALUES(?,?,?,?)'''
    
    cursor.execute(query,(productname,price,description,photo))
    
    connection.commit()

def search_product(connection,search_productname):
    cursor = connection.cursor()
    
    query = '''SELECT * FROM products WHERE productname LIKE ?'''
    
    cursor.execute(query, (f"{search_productname}%",))
    
    return cursor.fetchall()


def get_product(connection,productname):#don't forget if u are using this funct to select the spicific colums u need 
    cursor = connection.cursor()
    
    query = ''' SELECT * FROM products WHERE productname = ?'''
    
    cursor.execute(query,(productname,))
    
    return cursor.fetchone()

def get_all_product(connection):#admin
    cursor = connection.cursor()
    
    query = 'SELECT * FROM products'
    
    cursor.execute(query)
    
    return cursor.fetchall()

def delete_product(connection,productname):#adminOnly
    cursor = connection.cursor()
    
    query = '''DELETE FROM products WHERE productname = ?'''
    
    cursor.execute(query,(productname,))
    
    connection.commit()

def update_product_price(connection , product_data):#adminOnly
    cursor = connection.cursor()
    
    query = ''' UPDATE products SET price = ? WHERE productname = ? '''
    
    cursor.execute(query,(product_data['price'], product_data['description'],product_data['productname']))
    
    connection.commit() 


def update_product_photo(connection, filename , productname):#adminOnly
    cursor = connection.cursor()  
    
    query = '''UPDATE products SET photo = ? WHERE productname = ?'''
    
    cursor.execute(query, (filename,productname))  
    
    connection.commit()  
    #----------------------------------------------------------
    #userLibarry