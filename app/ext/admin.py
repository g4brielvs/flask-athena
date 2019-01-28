from flask_admin import Admin


def configure(app):
    """Adds admin extension to app"""
    app.admin = Admin(
        app,
        "Admin",
        base_template='my_master.html',
        template_mode="bootstrap3")


admin = Admin(name='Αθήνα', base_template='admin/master.html', template_mode='bootstrap3')
