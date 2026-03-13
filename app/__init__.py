from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
import os

# Initialize extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

def create_app():
    # Get absolute path to project root
    # This works regardless of where script is run from
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_path = os.path.join(project_root, 'app', 'templates')
    static_path = os.path.join(project_root, 'app', 'static')
    visuals_path = os.path.join(project_root, 'visuals')
    
    print(f"📁 Project root: {project_root}")
    print(f"📁 Templates: {templates_path}")
    print(f"📁 Static: {static_path}")
    print(f"📁 Visuals: {visuals_path}")
    print(f"✅ Templates exists: {os.path.exists(templates_path)}")
    print(f"✅ Static exists: {os.path.exists(static_path)}")
    print(f"✅ Visuals exists: {os.path.exists(visuals_path)}")
    
    app = Flask(__name__,
                template_folder=templates_path,
                static_folder=static_path,
                static_url_path='/static')
    
    app.config['SECRET_KEY'] = 'chainpulse-2024'
    app.config['PROJECT_ROOT'] = project_root
    app.config['DATA_PATH'] = os.path.join(project_root, 'data', 'powerbi')
    app.config['MODELS_PATH'] = os.path.join(project_root, 'models')
    app.config['VISUALS_PATH'] = visuals_path
    app.config['UPLOAD_PATH'] = os.path.join(project_root, 'uploads')
    app.config['BACKUP_PATH'] = os.path.join(project_root, 'backups')
    app.config['LOGS_PATH'] = os.path.join(project_root, 'logs')
    app.config['CONFIG_PATH'] = os.path.join(project_root, 'config')
    
    # Create folders
    for folder in ['uploads', 'backups', 'logs', 'config']:
        os.makedirs(os.path.join(project_root, folder), exist_ok=True)
    
    # Custom route to serve visuals files
    @app.route('/visuals/<path:filename>')
    def serve_visuals(filename):
        return send_from_directory(visuals_path, filename)
    
    # Initialize extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please login to access ChainPulse'
    login_manager.login_message_category = 'info'
    
    # Initialize SocketIO
    socketio.init_app(app)
    
    # Note: WebSocket manager removed - real-time features disabled
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.auth import get_user_by_id
        return get_user_by_id(user_id)
    
    # Make current_user available in all templates
    @app.context_processor
    def inject_user():
        from flask_login import current_user
        return dict(current_user=current_user)
    
    from app.routes import main
    app.register_blueprint(main)
    
    # Initialize SQLite database
    from app.database import init_db
    try:
        init_db()
        print("✅ SQLite database ready")
    except Exception as e:
        print(f"⚠️ DB init error: {e}")
    
    # Register upload blueprint
    from app.upload_routes import upload
    app.register_blueprint(upload)
    
    # Register auth blueprint
    from app.auth_routes import auth as auth_bp
    app.register_blueprint(auth_bp)
    
    return app