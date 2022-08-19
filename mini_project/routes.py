from mini_project import app,db,bcrypt
from flask import render_template,url_for,redirect,flash,request
from mini_project.forms import RegistrationForm,LoginForm
from mini_project.models import User
from flask_login import login_user,logout_user,current_user,login_required
import psycopg2



POSTGRESQL_URI="postgres://kxyxqccj:6hzGd6qlulzViWmhmfLxUUmzGgd7Hl25@john.db.elephantsql.com:5432/kxyxqccj"

connetion= psycopg2.connect(POSTGRESQL_URI)
try:
    with connetion:
        with connetion.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE Account (name TEXT,clg_name TEXT,age INT,height INT,weight INT,email TEXT,gender TEXT,game_name TEXT,tournament TEXT);"
                )
except psycopg2.errors.DuplicateTable:
    pass

import psycopg2

POSTGRESQL_URI="postgres://kxyxqccj:6hzGd6qlulzViWmhmfLxUUmzGgd7Hl25@john.db.elephantsql.com:5432/kxyxqccj"

connetion= psycopg2.connect(POSTGRESQL_URI)

cur= connetion.cursor()

sql = 'select name from account '

cur.execute(sql)

results = cur.fetchall()

teams=(results)
matches=[]
team1=0
while team1<len(teams):
    team2=team1+1    # start
    while team2<len(teams):
        matches.append((teams[team1],teams[team2]))
        team2+=1
    team1+=1
for i in matches: 
    print (i)


for i in matches: 
    try:
        with connetion:
            with connetion.cursor() as cursor:
                cursor.execute(
                "CREATE TABLE Schedule (Player1 TEXT,Player2 TEXT );"
                )
    except psycopg2.errors.DuplicateTable:
        pass

    with connetion:
        with connetion.cursor() as cursor:
            sql ='INSERT INTO Schedule (Player1 ,Player2) VALUES (%s, %s)'
            cursor = connetion.cursor()
            cursor.execute(sql, i)
            connetion.commit()



@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html',title='Home')


@app.route('/account',methods=['POST','GET'])
@login_required
def account():
    if request.method == 'POST':
        print(request.form)
        with connetion:
            with connetion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Account VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                    (
                        request.form.get("name"),
                        request.form.get("clg_name"),
                        float(request.form.get("age")),
                        float(request.form.get("height")),
                        float(request.form.get("weight")),
                        request.form.get("email"),
                        request.form.get("gender"),
                        request.form.get("game_name"),
                        request.form.get("tournament")
                    )
                )
        return redirect(url_for('show_schedule'))
    return render_template('account.html',title='Account')
@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password=form.password.data)
        flash(f'Account created successfully for {form.username.data}',category='success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)
@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        login_user(user)
        if form.email.data==user.email and form.password.data==user.password:
            flash(f'Login sucessful for {form.email.data}',category='success')
            return redirect(url_for('account'))

        else:
            flash(f'Login Unsucessful for {form.email.data}',category='danger')

    return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/schedule")
def show_schedule():
    with connetion:
        with connetion.cursor() as cursor:
            sql='SELECT * from Schedule  '
            cursor.execute(sql)
            abc=[]
            abc= cursor.fetchall()
            print(abc)
        return render_template("schedule.jinja2", entries=abc)

@app.route('/rules')
def rules():
    return render_template('rules.html',title='Rules')