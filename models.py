"""Database models."""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
  

db = SQLAlchemy()

class User(db.Model, UserMixin): 
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique= False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    picture  = db.Column(db.String(200), default='default.png')

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __str__(self):
        return f"User : {self.username}, Email: {self.email} "

