from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(120), unique=True, nullable=False)
    console = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console
        
    def __repr__(self):
        return '<Game %r>' % self.name
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def __repr__(self):
        return '<User %r>' % self.username