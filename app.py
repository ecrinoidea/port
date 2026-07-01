import os
from flask import Flask, render_template, send_from_directory
from jinja2 import ChoiceLoader, FileSystemLoader

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("🚀 Initializing Flask app...")

# Load config
try:
    from config import Config
    print("✅ Config loaded")
except Exception as e:
    print(f"❌ Error loading config: {e}")
    raise

# Load model functions
try:
    from model import get_profiles, get_skills, get_projects, get_experience
    print("✅ Model functions loaded")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    raise

try:
    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR, 'Frontend'),
        static_url_path='/static',
        template_folder=BASE_DIR
    )
    print("✅ Flask app created")
except Exception as e:
    print(f"❌ Error creating Flask app: {e}")
    raise

# Tambahkan loader untuk root dan Frontend
try:
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(BASE_DIR),
        FileSystemLoader(os.path.join(BASE_DIR, 'Frontend'))
    ])
    print("✅ Jinja2 loaders configured")
except Exception as e:
    print(f"❌ Error configuring Jinja2: {e}")
    raise

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit untuk upload
app.secret_key = Config.SECRET_KEY

@app.route('/health')
def health():
    try:
        from model import get_db
        conn = get_db()
        conn.close()
        return {"status": "ok", "database": "connected"}, 200
    except Exception as e:
        print(f"⚠️  Health check error: {e}")
        return {"status": "ok", "database": f"disconnected: {e}"}, 200

# Halaman utama (public portfolio)
@app.route("/")
def home():
    try:
        profiles    = get_profiles() if get_profiles() else []
        skills      = get_skills() if get_skills() else []
        projects    = get_projects() if get_projects() else []
        experience  = get_experience() if get_experience() else []
        return render_template("index.html",
            profiles=profiles,
            skills=skills,
            projects=projects,
            experience=experience
        )
    except Exception as e:
        print(f"❌ Error in home route: {e}")
        return render_template("index.html",
            profiles=[],
            skills=[],
            projects=[],
            experience=[]
        ), 200  # Return 200 even if there's an error to avoid 500

# Register blueprints untuk admin
print("📦 Loading blueprints...")
try:
    from Backend.utama.utama import utama_bp
    print("✅ utama_bp loaded")
except Exception as e:
    print(f"❌ Error loading utama_bp: {e}")
    raise

try:
    from Backend.admin.login import login_bp
    print("✅ login_bp loaded")
except Exception as e:
    print(f"❌ Error loading login_bp: {e}")
    raise

try:
    from Backend.admin.dashboard import dashboard_bp
    print("✅ dashboard_bp loaded")
except Exception as e:
    print(f"❌ Error loading dashboard_bp: {e}")
    raise

try:
    from Backend.admin.profiles import profiles_bp
    print("✅ profiles_bp loaded")
except Exception as e:
    print(f"❌ Error loading profiles_bp: {e}")
    raise

try:
    from Backend.admin.skills import skills_bp
    print("✅ skills_bp loaded")
except Exception as e:
    print(f"❌ Error loading skills_bp: {e}")
    raise

try:
    from Backend.admin.experience import experience_bp
    print("✅ experience_bp loaded")
except Exception as e:
    print(f"❌ Error loading experience_bp: {e}")
    raise

try:
    from Backend.admin.projects import projects_bp
    print("✅ projects_bp loaded")
except Exception as e:
    print(f"❌ Error loading projects_bp: {e}")
    raise

try:
    from Backend.admin.upload import upload_bp
    print("✅ upload_bp loaded")
except Exception as e:
    print(f"❌ Error loading upload_bp: {e}")
    raise

try:
    from Backend.admin.contact import contact_bp
    print("✅ contact_bp loaded")
except Exception as e:
    print(f"❌ Error loading contact_bp: {e}")
    raise

try:
    app.register_blueprint(utama_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(experience_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(contact_bp)
    print("✅ All blueprints registered")
except Exception as e:
    print(f"❌ Error registering blueprints: {e}")
    raise

# Favicon
@app.route('/favicon.ico')
def favicon():
    try:
        favicon_path = os.path.join(BASE_DIR, 'favicon.ico')
        if os.path.exists(favicon_path):
            return send_from_directory(BASE_DIR, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
        else:
            return '', 204  # No Content
    except Exception as e:
        print(f"⚠️  Favicon error: {e}")
        return '', 204

# Initialize database on first request (for Vercel cold starts)
_db_initialized = False
_db_init_attempted = False

@app.before_request
def init_db_on_startup():
    global _db_initialized, _db_init_attempted
    if not _db_init_attempted:
        _db_init_attempted = True
        try:
            print("🔧 Attempting database initialization...")
            from model import init_db
            init_db()
            _db_initialized = True
            print("✅ Database tables initialized.")
        except Exception as e:
            print(f"⚠️  Database init error (non-critical): {e}")
            # Don't raise - let the app continue even if DB init fails
            _db_initialized = False

# Global error handlers
@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    print(f"❌ Internal server error: {error}")
    return {"error": "Internal server error"}, 500

application = app
print("✅ Flask app fully initialized and ready")

if __name__ == '__main__':
    try:
        from model import init_db
        init_db()
        print("✅ Database tables initialized.")
    except Exception as e:
        print(f"⚠️  Database init error: {e}")

    app.run(debug=True, host='0.0.0.0', port=5000)

