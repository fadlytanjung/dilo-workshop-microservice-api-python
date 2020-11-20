from datetime import datetime
from app import db, bcrypt, ma

Column = db.Column
Model = db.Model

class User(Model):
    """ User model for storing user related data """
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(64), unique=True, index=True)
    username = Column(db.String(15), unique=True, index=True)
    name = Column(db.String(64))
    password_hash = Column(db.String(128))
    
    status = Column(db.String(10),default='inactive')
    role = Column(db.Integer, default=1)
    created_at = Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username','email','name','status','role')