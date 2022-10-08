
from flask import Flask, render_template, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# mysql.init_app(app)
# cursor = mysql.get_db().cursor() 
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'Ruturaj'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ruturajadmin2001'
app.config['MYSQL_DATABASE_DB'] = 'datacamp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/admin')
def showAdmin():
    return render_template('admin.html')

@app.route('/api/search',methods=['POST'])
def searchQuery():
    try:
        product = request.form['product']
        query = "SELECT * FROM grocery_store WHERE Product_name LIKE %s"
        cursor.execute(query, ('%'+product+'%',))
        data = cursor.fetchall()
        if len(data) > 0:
            print("Hellloooo")
            return render_template('results.html',products=str(data))
        else:
            return render_template('index.html',message='No results found!')

    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/insert',methods=['POST'])
def insertQuery():
    try:
        productName = request.form['productName']
        productAddr = request.form['productAddr']

        query = "INSERT INTO grocery_store (Product_name, Product_location) VALUES (%s, %s)"
        values = (productName, productAddr)

        cursor.execute(query, values)
        conn.commit()

        
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == "__main__":
    app.run()