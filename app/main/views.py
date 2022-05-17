from flask import render_template,request,redirect,url_for,flash, abort, json
from . import main
from .forms import PostForm, UpdateProfile, CommentForm
from app.models import User, Post, Role, Comment, Like
from flask_login import login_required, current_user
from .. import db,photos
import os
import requests,json



@main.route('/')
@main.route('/home')
@login_required
def index():
    req= requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    data = req.content
    json.data = json.loads(data)
    posts = Post.query.all()
    comments = Comment.query.all()
    user = User.query.all()
    
    
    return render_template('index.html', posts = posts, comments=comments,author = current_user, data= json.data)

@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(category=form.category.data, pitch=form.pitch.data, link=form.link.data,author= current_user)
        # flash('Your pitch has been created')
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('pitch.html', title='New Blog',
    form = form, legend='New Blog')

@main.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', category=post.category, post=post)

@main.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.category = form.category.data
        post.pitch = form.pitch.data
        post.link = form.link.data
        db.session.commit()
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.category.data = post.category
        form.pitch.data = post.pitch
    return render_template('pitch.html', title = 'Update Blog', form = form,
    legend='Update Blog')

@main.route('/post/<int:post_id>/comment',methods= ['GET', 'POST'])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(form.text.data,post_id)
        print(comment.author.username)
        return 'author'
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.index', post_id=post.id))
    return render_template('comment.html', title='New Comment', form = form, post_id=post_id, author = current_user)

@main.route("/post/<int:post_id>/delete",  methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(url_for('main.index'))

@main.route("/post/<int:post_id>/delete",  methods=['GET', 'POST'])
@login_required
def delete_comment(comment):
    post = Post.query.get_or_404(comment)
    if comment.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(url_for('main.index'))

counter = 0
@main.route("/like",  methods=['GET', 'POST'])
@login_required
def like():
    global counter
    counter += 1
    return redirect(url_for('main.index',times=str(counter)))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


    



