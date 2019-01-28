#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from config import Config

from .ext.admin import admin
from .ext.babel import babel
from .ext.cors import cors
from .ext.db import db
from .ext.db import ma
from .ext.debug import debug
from .ext.mail import mail
from .ext.migrate import migrate
from .ext.security import security, security_context_processor
from .ext.swagger import swagger

from .cli import register_commands

from .core import bp as core

from .core.models import user_datastore

BLUEPRINTS = (
    core,
)

def create_app():
    """Create a new Flask app"""

    app = Flask(__name__)
    app.config.from_object(Config)

    # extensions
    admin.init_app(app)
    cors.init_app(app)
    babel.init_app(app)
    db.init_app(app)
    ma.init_app(ma)
    mail.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    security_ctx = security.init_app(app, user_datastore)
    security_ctx.context_processor(security_context_processor)

    # blueprints
    blueprint_factory(app, BLUEPRINTS)

    # commands
    register_commands(app)

    return app

def blueprint_factory(app, blueprints):
    """Configure a blueprint factory"""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
