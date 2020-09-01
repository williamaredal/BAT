from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import  current_user, login_required

from .forms import MakeForm, UpdateForm
from .models import db, Dossier
from .import login_manager


# Blueprint Configuration
dossier_bp = Blueprint(
    'dossier_bp', __name__,
    template_folder='templates',
    static_folder='static'
)



@dossier_bp.route('/make', methods=['GET', 'POST'])
@login_required
def make():
    # Fetches dossier title from terminal call, if none exists it returns None
    dossier_title = request.args.get('dossier_title', None)

    form = MakeForm(
        title=dossier_title
        )

    # The information filled out in the form is validated to check if filled out correctly
    if form.validate_on_submit():

        # Checks if there is an existing user with that username
        existing_dossier = Dossier.query.filter_by(title=form.title.data).first()

        # If none match, a new dossier is created
        if existing_dossier is None:
            dossier = Dossier(
                title=form.title.data,
                protocol=form.protocol.data,
                poi=form.poi.data,
                attachment=form.attachment.data
            )

            db.session.add(dossier)
            db.session.commit()

            return redirect(url_for('main_bp.dashboard'))
        
        # If there is a dossier with the same title, they're alerted
        flash('There aleady exists a dossier with that title.')


    return render_template(
        'make.jinja2',
        form=form,
        template='login-template',
        title='Make'
    )


@dossier_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():

    # Fills the update form with the dossier's existing information
    dossier_title = request.args.get('dossier_title')
    dossier_protocol = request.args.get('dossier_protocol')
    dossier_poi = request.args.get('dossier_poi')
    dossier_attachment = request.args.get('dossier_attachment')

    form = UpdateForm(
        title=dossier_title,
        protocol=dossier_protocol,
        poi=dossier_poi,
        attachment=dossier_attachment
        )
    
    # The information filled out in the form is validated to check if filled out correctly
    if form.validate_on_submit():

        old_dossier = Dossier.query.filter_by(title=form.title.data).first()

        # Updates the dossier to have the new data submitted in the form
        old_dossier.title = form.title.data
        old_dossier.protocol = form.protocol.data      
        old_dossier.poi = form.poi.data      
        old_dossier.attachment = form.attachment.data

        db.session.commit()

        return redirect(url_for('main_bp.dashboard'))
    

    return render_template(
        'update.jinja2',
        form=form,
        template='login-template',
        title='Update',
    )