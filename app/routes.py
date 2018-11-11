'''
Routes module
'''
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms  import LoginForm, RegistrationForm
from app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    '''
    Index page of the website
    '''
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'John'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login route of the website
    '''
    ## checks if user is already logged in and ends up clicking on login link
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    ## creates the login form
    form = LoginForm()
    ## validation on submition for form
    if form.validate_on_submit():
        ## searchs user in db by database
        user = User.query.filter_by(username=form.username.data).first()
        ## if there are no user or if the password provided is incorrect
        ## redirect to index
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        ## app would remember that the user is logged in
        ## by setting current_user to current_user
        login_user(user, remember=form.remember_me.data)
        ## gets the url path assigned to the 'next' argument in the url
        next_page = request.args.get('next')
        ## checks if there is no next_page or if it is not a relative path by checking netloc
        ## netloc: to protect users from malicious url injections and not
        ## redirect them to another malicious website outside the application
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    '''
    Logout route for user
    '''
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
