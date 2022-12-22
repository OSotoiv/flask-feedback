"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, flash, session, jsonify
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
# from helpers import new_cupcake, pre_fill_form, validate_req
from form import User_Form, Login_Form, Feedback_Form
from sqlalchemy.exc import IntegrityError
from env_keys.env_secrets import APP_CONFIG_KEY

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = APP_CONFIG_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
connect_db(app)


@app.route('/')
def home():
    return render_template('/base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = User_Form()
    if form.validate_on_submit():
        new_user = User.register(form)
        if new_user:
            db.session.add(new_user)
            try:
                db.session.commit()
                session['curr_user'] = new_user.username
            except IntegrityError:
                form.username.errors.append('Username/Email already taken')
                return render_template('register.html', form=form)
        flash('New user made', 'success')
        return redirect(f"/user/{session['curr_user']}")
    return render_template('register.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    """logout user if curr_user is set in session"""
    if 'curr_user' in session:
        session.pop('curr_user')
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """show and submit login form"""
    form = Login_Form()
    if form.validate_on_submit():
        curr_user = User.login(form)
        if curr_user:
            session['curr_user'] = curr_user.username
            return redirect(f"/user/{session['curr_user']}")
        else:
            flash('Username/Password Incorrect', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
def secret(username):
    """GET user info, POST for (UPDATE) user info"""
    if 'curr_user' in session:
        user = User.query.filter_by(username=session['curr_user']).first()
        feedback = user.feedback
        form = User_Form(obj=user)
        if form.validate_on_submit():
            if not user.auth_update(form.password.data):
                form.password.errors.append('wrong password')
                return render_template('users_page.html', form=form, user=user, feedback=feedback)
            try:
                user.update(form)
                # import pdb
                # pdb.set_trace()
                # feedback = Feedback.query.filter_by(
                # username=session['curr_user']).all()
                db.session.add(user)
                db.session.commit()
                session['curr_user'] = user.username
                return redirect(f"/user/{session['curr_user']}")
            except IntegrityError as e:
                print('***********************************************')
                print(e)
                db.session.rollback()
                form.username.errors.append('Username/Email already taken')
                return render_template('users_page.html', form=form, user=user, feedback=feedback)
        else:
            return render_template('users_page.html', form=form, user=user, feedback=feedback)
    else:
        flash('You must be logged in for that!', 'warning')
        return redirect('/login')


@app.route('/feedback/add', methods=['GET', 'POST'])
def feedback():
    if 'curr_user' in session:
        form = Feedback_Form()
        if form.validate_on_submit():
            feedback = Feedback()
            feedback.make(form, session['curr_user'])
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/user/{session['curr_user']}")
        return render_template('feedback_form.html', form=form)
    else:
        flash('You must be logged in for that!', 'warning')
        return redirect('/login')


@app.route('/feedback/<int:id>', methods=['GET', 'POST'])
def edit_feedback(id):
    feed = Feedback.query.get_or_404(id)
    form = Feedback_Form(obj=feed)
    if form.validate_on_submit():
        feed.update(form)
        # import pdb
        # pdb.set_trace()
        db.session.add(feed)
        db.session.commit()
        return redirect(f"/user/{session['curr_user']}")
    else:
        return render_template('edit_feedback.html', form=form, feedback_id=feed.id)


@app.route('/feedback/delete/<int:id>', methods=['POST'])
def delete_feedback(id):
    if 'curr_user' in session:
        feed = Feedback.query.get_or_404(id)

        if feed.user.username == session['curr_user']:
            db.session.delete(feed)
            db.session.commit()
            flash('deleted feedback', 'success')
            return redirect(f"/user/{session['curr_user']}")
        else:
            flash('You must be logged in for that!', 'warning')
            return redirect('/login')
    else:
        flash('You must be logged in for that!', 'warning')
        return redirect('/login')
