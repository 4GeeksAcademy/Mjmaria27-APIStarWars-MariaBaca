import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, People, Planet, Favorite

# 🔓 Vista pública sin autenticación
class PublicModelView(ModelView):
    def is_accessible(self):
        return True
    def inaccessible_callback(self, name, **kwargs):
        return "Acceso denegado", 403

def setup_admin(app):
    app.secret_key = 'super-secret-123'  # Necesario para sesiones en Flask
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(PublicModelView(User, db.session))
    admin.add_view(PublicModelView(People, db.session))
    admin.add_view(PublicModelView(Planet, db.session))
    admin.add_view(PublicModelView(Favorite, db.session))
