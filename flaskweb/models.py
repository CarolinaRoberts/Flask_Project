from datetime import datetime
from flaskweb import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(500), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    review = db.relationship('Review', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"



class Console(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    console_name = db.Column(db.String(20), nullable=False)
    games = db.relationship('Game', backref='console', lazy=True)

    def __repr__(self):
        return f"Console('{self.console_name}')"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='gamedefault.jpg')
    stock_level = db.Column(db.Integer, nullable=False)
    console_id = db.Column(db.Integer, db.ForeignKey('console.id'), nullable=False)
    age_rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Game('{self.title}', '{self.description}', '{self.price}', '{self.stock_level}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    game_title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"






#class Cart(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    quantity = db.Column(db.Integer)
#    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

#    description = db.Column(db.String(120), nullable=False)
#    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#    price = db.Column(db.Numeric(10,2), nullable=False)
#    image_file = db.Column(db.String(30), nullable=False, default='gamedefault.jpg')
#    stock_level = db.Column(db.Integer, nullable=False)
#    console_id = db.Column(db.Integer, db.ForeignKey('console.id'), nullable=False)
#    age_rating = db.Column(db.Integer, nullable=False)

#    def __repr__(self):
#        return f"Game('{self.title}', '{self.description}', '{self.price}', '{self.stock_level}')"


