"""Models for flask-feedback"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        return f"username:{self.username} fullname:{self.first_name} {self.last_name}"

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    feedback = db.relationship(
        'Feedback', cascade="delete, save-update", backref='user')

    @classmethod
    def register(cls, form):
        hashed = bcrypt.generate_password_hash(
            form.password.data).decode(encoding='utf8')
        return cls(
            username=form.username.data,
            password=hashed,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            # is_admin=True
        )

    @classmethod
    def login(cls, form):
        """login user if username and password are correct"""
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return user
        else:
            return False

    def update(self, form):
        self.username = form.username.data,
        self.email = form.email.data,
        self.first_name = form.first_name.data,
        self.last_name = form.last_name.data,

    def auth_update(self, pwd):
        """checks the password for authentication before updating user"""
        return bcrypt.check_password_hash(self.password, pwd)


class Feedback(db.Model):
    __tabelname__ = 'feedback'

    def __repr__(self):
        return 'Feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    username = db.Column(db.String(), db.ForeignKey(
        'users.username'), nullable=False)

    def make(self, form, username):
        self.title = form.title.data
        self.content = form.content.data
        self.username = username

    def update(self, form):
        self.title = form.title.data
        self.content = form.content.data
