
import hashlib
from flask.globals import request
from flask.helpers import flash
from wtforms.validators import Email
from blog import app, db, bcrypt, images
from blog.forms import RegistratoinForm, LoginForm, PostForm
from flask import render_template, redirect, url_for, request
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail.html', post=post)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistratoinForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        filename = images.save(form.image.data, name=hashlib.md5(form.username.data.encode('utf-8')).hexdigest() + ".")
        user = User(name=form.name.data, avatar=filename, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully!',category="info")
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next', None)
            flash('Logged in Successfully!', category="info")
            return redirect(next_page if next_page else url_for('index'))

        else:
            flash('Username or Password is not Correct!', category='primary')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out!', category="info")
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route("/post/new", methods=['GET', 'POST']) 
@login_required  
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", category="success")
        return redirect(url_for("index"))
    return render_template('create_post.html', tilte="new post", form=form)
