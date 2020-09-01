############ Authenticated page routes ############
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required, logout_user
from sqlalchemy import Table
import json

from .forms import TerminalForm
from .functions import Refractor
from .models import db, Dossier


main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# The magic here is all contained within the @login_required decorator. When this decorator is present on a route, the following things happen:
#   The @login_manager.user_loader route we created determines whether or not the user is authorized to view the page (logged in).
#       If the user is logged in, they'll be permitted to view the page.
#   If the user is not logged in, the user will be redirected as per the logic in the route decorated with @login_manager.unauthorized_handler.
#   The name of the route the user attempted to access will be stored in the URL as ?url=[name-of-route] — this what allows next to work.

############ Dashboard Route ############
@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TerminalForm()

    if form.validate_on_submit():
        # Finds variable(s) and command in terminalText separated by keyword
        terminalString = str(form.terminal.data)
        keyword = ' -'
        variable, keyword, command = terminalString.partition(keyword)


        # Logout function, as it requires a redirect not permissable in the Refractor function.
        if command and command.lower() == "logout":
            logout_user()
            
            return redirect(url_for('auth_bp.login'))


        # Make function, as it requires a redirect not permissable in the Refractor function.
        elif command and command.lower() in ["make", "m"]:
            dossier_title = variable

            return redirect(
                url_for(
                    'dossier_bp.make',
                    dossier_title=dossier_title
                    ))


        # Update function, as it requires a redirect not permissable in the Refractor function.
        elif command and command.lower() in ["update", "u"]:
            search = Dossier.query.filter_by(title=variable).first()

            # If the query returns no results, the user is notified
            if search is None:
                flash('Found no dossier with title: '+ variable)
                returnResults = []

            else:
                # Loads the data from the queried dossier and passes them to the update page
                dossierTitle = search.title
                dossierProtocol = search.protocol
                dossierPoi = search.poi
                dossierAttachment = search.attachment

                return redirect(
                    url_for(
                        'dossier_bp.update',
                        dossier_title=dossierTitle,
                        dossier_protocol=dossierProtocol,
                        dossier_poi=dossierPoi,
                        dossier_attachment=dossierAttachment,
                        ))


        else:
            returnResults = Refractor(command, variable)
    
    # If form terminal is empty/not valid
    else:
        returnResults = []

    return render_template(
        'dashboard.jinja2',
        title='BAT',
        template='dashboard-template',
        current_user=current_user,
        form=form,
        results=returnResults
    )


############ Logout Route ############
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))