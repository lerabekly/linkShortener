from bd import *
from flask import Flask, render_template, request, session, redirect, flash
from flask_bcrypt import Bcrypt
import os
Flask.secret_key = os.urandom(10)

app = Flask(__name__, template_folder='templates', static_folder='templates/static')
bcrypt = Bcrypt(app)

menu = {'name': 'Главная', 'url': '/index'}, {'name': 'Авторизация', 'url': '/auth'}, {'name' : 'Регистрация', 'url' : '/reg'}
menuAuth = {'name': 'Мои ссылки', 'url':'/links'}, {'name': 'Сократить ссылки', 'url':'/newLinks'}, {'name': 'Выход', 'url':'/logout'}
@app.route("/")
def index():
    return render_template('index.html', menu=menu)

@app.route("/auth")
def auth():
    return render_template("auth.html", menu=menu)

@app.route("/reg")
def reg():
    return render_template("reg.html", menu=menu)

@app.route("/links")
def links():
    if 'auth' in session:
        return render_template("links.html", menu=menuAuth)
    else:
        return redirect(request.host_url + 'auth')

@app.route("/newLinks")
def newLinks():
    if 'auth' in session:
        con = sqlite3.connect(r"bd.db", check_same_thread=False)
        cur = con.cursor()
        accesses= findAccesses(cur)
        print( accesses)
        return render_template("newLinks.html", menu=menuAuth, accesses=accesses)
    else:
        return redirect(request.host_url + 'auth')

@app.route('/logout')
def logout():
    session.pop('auth', None)
    session.pop('name', None)
    return redirect(request.host_url)

@app.route('/reg', methods = ['POST', 'GET'])
def registr():
    if request.method == "POST":
        con = sqlite3.connect(r"bd.db", check_same_thread=False)
        cur = con.cursor()
        login = request.form['username']
        password = request.form['password']
        if findUser(cur, login)!=None:
            print(findUser(cur, login))
            flash(f'Такой логин уже существует')
            return redirect(f'/reg')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            registration(con, cur, login, hashed_password)
            print(findUser(cur, login))
            session['auth'] = True
            session['id'] = findUser(cur, login)[0]
            session['name']= findUser(cur, login)[1]
            return redirect(request.host_url+'links')

@app.route('/auth', methods =['POST', 'GET'])
def authorization():
    if request.method == 'POST':
        con = sqlite3.connect(r"bd.db", check_same_thread=False)
        cur = con.cursor()
        login = request.form['username']
        password = request.form['password']
        if findUser(cur, login) == None:
            flash(f"Пользователь не найден")
            return redirect(f'/auth')
        else:
            hashPass = findUser(cur, login)[2]
            is_valid = bcrypt.check_password_hash(hashPass, password)
            if is_valid == False:
                flash(f"Пароль неверный")
                return redirect(f'/auth')
            else:
                user = findUser(cur, login)
                session['auth']=True
                session['id']=user[0]
                session['name']=user[1]
                return redirect(request.host_url+'links')
@app.route('/newLinks',methods =['POST', 'GET'])
def addLink():



if __name__ == '__main__':
    app.run()



