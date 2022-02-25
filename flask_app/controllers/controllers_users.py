from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


#show login + reg page
@app.route('/')
def index():
    return render_template('index.html')

#save user into db
@app.route('/register',methods=['POST'])
def register():
    if User.is_valid(request.form) == False:
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save(data)
    #login action
    session['user_id']=user_id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user= User.get_by_id(data),recipes=Recipe.get_all())


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid Email', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Email', 'login')
        return redirect('/')
    session['user_id' ] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')








