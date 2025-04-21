from flask import Blueprint, session, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from form.userform import RegisterForm, UpdateUserForm
from models.user import User
from extensions import db

user_bp = Blueprint(name='user', import_name=__name__,
                    template_folder='templates', static_folder='static')


@user_bp.route('/profile')
@login_required
def user_profile():
    return render_template('user/profile.html')


@user_bp.route('/update-user/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    form = UpdateUserForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        user.name = form.username.data
        try:
            db.session.commit()
            flash('Username is updated successfully!')
            return redirect(url_for('mainpage.index'))
        except:
            flash('There was a problem updating that username')
    return render_template('user/update_user.html', form=form, user=user)


@user_bp.route('/delete-user/<int:id>')
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.name} is deleted successfully.', 'alert-warning')
    except:
        flash('There was a problem deleting that user', 'alert-danger')
    return redirect(url_for('mainpage.index'))
