############ Database models ############
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# Using the shortcut UserMixin from Flask-Login allows for user management via 4 methods:
#   1. is_authenticated: Checks to see if the current user is already authenticated,
#       thus allowing them to bypass login screens.
#   2. is_active: If your app supports disabling or temporarily banning accounts, we can check with a if statement
#       if user.is_active() to handle a case where their account exists, but have been banished from the land.
#   3. is_anonymous: Many apps have a case where user accounts aren't entirely black-and-white,
#       and anonymous users have access to interact without authenticating. 
#   4. get_id: Fetches a unique ID identifying the user.

# It's nice to keep logic related to users bundled in our model and out of our routes,
# hence the set_password() and check_password() methods.

############ User account model ############
class User(UserMixin, db.Model):

    __tablename__ = 'flasklogin-users' #change to users?

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(200),
        primary_key=False,
        nullable=False,
        unique=False
    )


    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )


    def set_password(self, password):
        
        # Creates hashed password
        self.password = generate_password_hash(
            password,
            method='sha256'
        )
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


############ Dossier ############
class Dossier(db.Model):
    __tablename__ = 'Dossiers'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String,
        unique=True,
        nullable=True
    )

    protocol = db.Column(
        db.String,
        unique=False,
        nullable=True
    )

    poi = db.Column(
        db.String,
        unique=False,
        nullable=True
    )

    attachment = db.Column(
        db.String,
        unique=False,
        nullable=True
    )

    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )