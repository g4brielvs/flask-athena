#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template

from flask_security import current_user, login_required, utils

from app.ext.admin import admin
from app.ext.db import db

from .models import Role, User, user_datastore
from .views import RoleAdmin, UserAdmin

"""
The 'core' blueprint is responsable for managing user authentication, roles 
and permissions and handling errors
"""

from flask import Blueprint

bp = Blueprint('core', __name__)

# Executes before the first request is processed.
@bp.before_app_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = utils.hash_password('athena')
    if not user_datastore.get_user('user@athena.com'):
        user_datastore.create_user(email='user@athena.com', password=encrypted_password)
    if not user_datastore.get_user('admin@athena.com'):
        user_datastore.create_user(email='admin@athena.com', password=encrypted_password)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('user@athena.com', 'end-user')
    user_datastore.add_role_to_user('admin@athena.com', 'admin')
    db.session.commit()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

admin.add_view(RoleAdmin(Role, db.session, category='Admin'))
admin.add_view(UserAdmin(User, db.session, category='Admin'))
