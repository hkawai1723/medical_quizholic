from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user
from models.questions import Section
from sqlalchemy.sql.expression import func

mainpage_bp = Blueprint(name='mainpage', import_name=__name__,
                        template_folder='templates', static_folder='static')


@mainpage_bp.route('/')
def index():
    random_section = Section.query.order_by(func.rand()).first()
    if current_user.is_authenticated:
        return redirect(url_for('mainpage.dashboard'))
    return render_template('index.html', section=random_section.section_name)


@mainpage_bp.route('/dashboard')
def dashboard():
    random_section = Section.query.order_by(func.rand()).first()
    return render_template('auth/dashboard.html', section=random_section.section_name)
