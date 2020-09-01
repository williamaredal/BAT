############ Routes for user authentication ############
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user

from .forms import SignupForm, LoginForm
from .models import db, User
from .import login_manager


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


############ User Loader ############
@login_manager.user_loader
def load_user(user_id):

    # Checks on every page weather the user is logged in
    if user_id is not None:
        return User.query.get(user_id)
    
    # If user is logged inn, nothing changes
    return None


############ Unauthorized User Handler ############
@login_manager.unauthorized_handler
def unauthorized():

    # Checks and redirects unauthorized users to login page
    flash('You must be authenticated to view this page.')
    return redirect(url_for('auth_bp.login'))


############ Login ############
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # Checks if user already is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))
    
    # If user is not already authenticated
    form = LoginForm()

    # Checks if information filled in form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # Checks if the user exist and the password in the form matches the user's password
        if user and user.check_password(password=form.password.data):
            login_user(user)

            # next_page is a parameter stored in the query string of the current user, so they can return to their previous activity
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.dashboard'))
        
        # If either the user doesn't exist or the form password does not match the user's password 
        flash('Invalid.')
        return redirect(url_for('auth_bp.login'))
    
    return render_template(
        'login.jinja2',
        form=form,
        title='Auth',
        template='login-page',
        body="Authentication"
    )


############ Signup ############
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()

    # The information filled out in the form is validated to check if filled out correctly
    if form.validate_on_submit():

        # Checks if there is an existing user with that username
        existing_user = User.query.filter_by(username=form.username.data).first()

        # If none, a user is created
        if existing_user is None:

            user  = User(
                username=form.username.data,
                password=form.password.data,
            )

            # Sets password and adds the user to the database
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            # Logs in as newly created user
            login_user(user)

            return redirect(url_for('main_bp.dashboard'))

        # If there is a user with that username, they're alerted
        flash('A user already exists with that username.')
    
    return render_template(
        'signup.jinja2',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )