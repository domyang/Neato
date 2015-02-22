from flask import render_template, flash, redirect, request, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, RegistrationForm, PostForm
from .models import User, Post
from app import app, db, lm

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POSt'])
def home():
    user = g.user
    author = User.query.first()
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    if user and form.validate_on_submit():
        post = Post(content=form.body.data, author=user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    title = 'Home'
    posts = pagination.items
    return render_template('home.html',
                            form=form,
                            title=title,
                            posts=posts,
                            user=user,
                            pagination=pagination)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    title = "Login"
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Logged in Successfully')
            return redirect(request.args.get("next") or url_for("home"))
        else:
            flash('Unsuccessful Login')
            return redirect(url_for("home"))
    return render_template('login.html',
                        title=title, form=form)
@app.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username=name).first()
    if user is None:
        flash('User not found')
        return redirect(url_for('home'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(author=user).order_by(Post.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    title = name
    posts = pagination.items
    return render_template('user.html',
                            title=title,
                            posts=posts,
                            user=user,
                            pagination=pagination)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(u)
        db.session.commit()
        flash('You can now login')
        return redirect(url_for('login'))
    return render_template('register.html',
                            title = 'register',
                            form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user