from flask import url_for
from flask_security import Security

# Setup Flask-Security
from app.core.models import user_datastore

from app.ext.admin import admin

from flask_admin import helpers as admin_helpers

security = Security()

# define a context processor for merging flask-admin's template context into the
# flask-security views.
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
)
