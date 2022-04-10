from flask import *
import sqlite3

conn = sqlite3.connect('database.db')
app = Flask(__name__)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        zipcode = request.form['zipcode']
        city = request.form['city']
        country = request.form['country']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, zipcode, city, '
                            'country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)')
                con.commit()
                msg = "Registered Successfully"

            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)


@app.route("/registrationForm")
def registrationForm():
    return render_template("register.html")


@app.route("/")
def root():
    return render_template('homepage.html')


@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'], ))
            userId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
            except:
                conn.rollback()
        conn.close()
        return redirect(url_for('root'))


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')