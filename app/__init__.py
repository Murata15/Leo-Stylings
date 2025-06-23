from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
        # ✅ Enable live template reloading
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    app.config["DEBUG"] = True  # Optional: enables full Flask debug mode
    
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serveease.db'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth_routes import auth
    from .routes.main_routes import main
    from .routes.request_routes import request_bp
    from .routes.appointment_routes import appointment
    from .routes.payment_routes import payment
    from .routes.feedback_routes import feedback
    from .routes.file_routes import file_routes
    from .routes.announcement_routes import announcement
    from .routes.admin_routes import admin
    from .routes.service_routes import service_bp

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(request_bp)
    app.register_blueprint(appointment)
    app.register_blueprint(payment)
    app.register_blueprint(feedback)
    app.register_blueprint(file_routes)
    app.register_blueprint(announcement)
    app.register_blueprint(admin)
    app.register_blueprint(service_bp)

    return app
