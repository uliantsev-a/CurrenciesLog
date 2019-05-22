from project import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128))
    firstname = db.Column(db.String(1000))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.password:
            self.set_password(self.password)

    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)

    def check_password(self, password):
        return check_password_hash(self.password, password)