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
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
    
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form and 'inpConPass' in request.form and request.form['inpPass'] == request.form['inpConPass']:
        user = request.form['inpUser']
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        alamat = request.form['inpAlamat']
        nomor_telepon =  request.form['inpNo']
        #  = request.form['inp']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (id, username, password, email, alamat, nomor_telepon) VALUES (NULL, %s,%s,%s,%s,%s)",(user,passwd,email,alamat,nomor_telepon))
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
    

@app.route('/dashboard')
def dashboard():
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pempek")
        result = cur.fetchall()
        return render_template('dashboard.html',data =result )
    else:
        return redirect(url_for("login"))
    

@app.route('/Variant')
def Variant():
    if 'is_logged_in' in session:
        return render_template('Variant.html')
    else:
        return redirect(url_for("login"))
    
@app.route('/Pesanan',methods=['GET','POST'])
def Pesanan():
    if 'is_logged_in' in session:
        if request.method == "POST":
            data = request.json
            temp = []
            if data['PempekKapal'] != 0:
                resdb = {
                    "nama" : "",
                    "jumlah" : 0,
                    "total" : 0
                }
                resdb['nama'] = "PempekKapal"
                resdb['jumlah'] = data['PempekKapal']
                resdb['total'] = data['PempekKapal'] * 10000
                temp.append(resdb)
            if data['PempekAdaan'] != 0:
                resdb = {
                    "nama" : "",
                    "jumlah" : 0,
                    "total" : 0
                }
                resdb['nama'] = "PempekAdaan"
                resdb['jumlah'] = data['PempekAdaan']
                resdb['total'] = data['PempekAdaan'] * 10000
                temp.append(resdb)
            if data['PempekLenjer'] != 0:
                resdb = {
                    "nama" : "",
                    "jumlah" : 0,
                    "total" : 0
                }
                resdb['nama'] = "PempekLenjer"
                resdb['jumlah'] = data['PempekLenjer']
                resdb['total'] = data['PempekLenjer'] * 10000
                temp.append(resdb)
            if data['PempekTelur'] != 0:
                resdb = {
                    "nama" : "",
                    "jumlah" : 0,
                    "total" : 0
                }
                resdb['nama'] = "PempekTelur"
                resdb['jumlah'] = data['PempekTelur']
                resdb['total'] = data['PempekTelur'] * 10000
                temp.append(resdb)
            if data['PempekTahu'] != 0:
                resdb = {
                    "nama" : "",
                    "jumlah" : 0,
                    "total" : 0
                }
                resdb['nama'] = "PempekTahu"
                resdb['jumlah'] = data['PempekTahu']
                resdb['total'] = data['PempekTahu'] * 10000
                temp.append(resdb)
            if data['PempekLenggang'] != 0:
                resdb = {
                    "nama" : "",
                    "jumlah" : 0,
                    "total" : 0
                }
                resdb['nama'] = "PempekLenggang"
                resdb['jumlah'] = data['PempekLenggang']
                resdb['total'] = data['PempekLenggang'] * 10000
                temp.append(resdb)
            cur = mysql.connection.cursor()
            cur.execute("START TRANSACTION")
            for j in temp:
                cur.execute(
                    "INSERT INTO pempek (id ,username,Pempek,Jumlah	,Total) VALUES ('',%s,%s,%s,%s)",
                    (
                    session['username'],
                    j["nama"],
                    j["jumlah"],
                    j["total"]
                ),
            )
            try:
                mysql.connection.commit()
                return {"status": "success"}
            except:
                return {"status": "failed"}
        
    



@app.route('/logout')
def logout():
    session.pop('is_logged_in')
    session.pop('username')
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
