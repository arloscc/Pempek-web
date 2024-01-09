from flask import Flask, render_template,session,request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = '!@#$%'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'

mysql = MySQL(app)


@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s",(email,passwd))
        result = cur.fetchone()
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
    
@app.route('/admin',methods=['GET','POST'])
def loginAdmin():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE email = %s AND password = %s",(email,passwd))
        result = cur.fetchone()
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect(url_for('home'))
        else:
            return render_template('dashboard.html')
    else:
        return render_template('login.html')
    
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form and 'inpConPass' in request.form and request.form['inpPass'] == request.form['inpConPass']:
        user = request.form['inpUser']
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        alamat = request.form['inpAlamat']
        no = request.form['inpNo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (id, username, password, email, alamat, nomor_telepon) VALUES (NULL, %s,%s,%s,%s,%s)",(user,passwd,email,alamat,no))
        try:
            mysql.connection.commit()
            return redirect(url_for('login'))
        except:
            return render_template('register.html')
    else:
        return render_template('register.html')

@app.route('/home')
def home():
    if 'is_logged_in' in session:
        return render_template('home.html')
    else:
        return redirect(url_for("login"))
    

@app.route('/Variant')
def Variant():
    if 'is_logged_in' in session:
        return render_template('Variant.html')
    else:
        return redirect(url_for("login"))
    


@app.route('/logout')
def logout():
    session.pop('is_logged_in',None)
    session.pop('username',None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
