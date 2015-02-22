from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from PIL import Image
from PIL import ImageChops
from random import choice

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(40), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def pic(self):
        vidush = Image.open('app/static/original.jpg')
        copy = vidush.copy()
        copy = vidush.resize((50, 50))
        hex = '1234567890abcdef'
        color = '#' + choice(hex) + choice(hex) + choice(hex) + choice(hex) + choice(hex) + choice(hex)
        colpic = Image.new('RGB', (50, 50), color)
        vidushcopy = ImageChops.multiply(copy, colpic)
        file_location = 'app/static/' + self.username + '.jpg'
        vidushcopy.save(file_location)
        return 'static/' + self.username + '.jpg'

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))