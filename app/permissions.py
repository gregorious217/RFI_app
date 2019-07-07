from functools import wraps
from app import db, models
from app.models import Project, Team, User, Rfi
from flask_login import current_user
from flask import session, render_template, flash, redirect, url_for, request, send_from_directory

def team_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        proj_id=kwargs['id']
        proj = Project.query.filter_by(id=proj_id).first_or_404()
        team=Team.query.filter_by(project_id=proj.id).all()
        team_emails = [member.email for member in team]
        member=Team.query.filter_by(email=current_user.email).first()
        if not current_user.is_admin:
            if current_user.email not in team_emails:
                flash('User {} does not have permission to view this page. If you believe this is an error please contact project manager or site administrator.'.format(current_user.username))
                return redirect(url_for('index'))
        return f(*args,**kwargs)
    return decorated_function

def design_team_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        proj_id=kwargs['id']
        roles = ['Engineer','Architect','Landscape Architect','Natural','Cultural','PM','CM']
        proj = Project.query.filter_by(id=proj_id).first_or_404()
        team=Team.query.filter_by(project_id=proj.id).all()
        team_emails = [member.email for member in team]
        member=Team.query.filter_by(email=current_user.email).first()
        if not current_user.is_admin:
            if current_user.email not in team_emails or member.role not in roles:
                flash('User {} does not have permission to view this page. If you believe this is an error please contact project manager or site administrator.'.format(current_user.username))
                return redirect(url_for('proj', id=proj_id))
        return f(*args,**kwargs)
    return decorated_function

def construction_team_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        proj_id=kwargs['id']
        roles = ['CM', 'Contractor']
        proj = Project.query.filter_by(id=proj_id).first_or_404()
        team=Team.query.filter_by(project_id=proj.id).all()
        team_emails = [member.email for member in team]
        member=Team.query.filter_by(email=current_user.email).first()
        if not current_user.is_admin:
            if current_user.email not in team_emails or member.role not in roles:
                flash('User {} does not have permission to view this page. If you believe this is an error please contact project manager or site administrator.'.format(current_user.username))
                return redirect(url_for('proj', id=proj_id))
        return f(*args,**kwargs)
    return decorated_function

def construction_manager_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        proj_id=kwargs['id']
        roles = ['CM']
        proj = Project.query.filter_by(id=proj_id).first_or_404()
        team=Team.query.filter_by(project_id=proj.id).all()
        team_emails = [member.email for member in team]
        member=Team.query.filter_by(email=current_user.email).first()
        if not current_user.is_admin:
            if current_user.email not in team_emails or member.role not in roles:
                flash('User {} does not have permission to view this page. If you believe this is an error please contact project manager or site administrator.'.format(current_user.username))
                return redirect(url_for('proj', id=proj_id))
        return f(*args,**kwargs)
    return decorated_function