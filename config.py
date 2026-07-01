import os
import base64
import tempfile
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / '.env'

load_dotenv(dotenv_path=str(ENV_PATH), override=False)

# Fallback for environments where the app is started from a different working directory
if not os.getenv('SECRET_KEY'):
    load_dotenv(override=False)


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'reyna_secret_porto')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Warn jika menggunakan SECRET_KEY default di production
    if FLASK_ENV == 'production' and SECRET_KEY == 'reyna_secret_porto':
        print("⚠️  WARNING: Using default SECRET_KEY in production! Set SECRET_KEY environment variable.")

    # TiDB
    TIDB_HOST     = os.getenv('TIDB_HOST')
    TIDB_PORT     = int(os.getenv('TIDB_PORT', 4000))
    TIDB_USER     = os.getenv('TIDB_USER')
    TIDB_PASSWORD = os.getenv('TIDB_PASSWORD')
    TIDB_DB       = os.getenv('TIDB_DB', 'db_porto')

    # Pastikan path SSL CA aman atau dukung env var base64 (`TIDB_SSL_CA_B64`)
    raw_ca = os.getenv('TIDB_SSL_CA')
    raw_ca_b64 = os.getenv('TIDB_SSL_CA_B64')

    def _resolve_ca_path(ca_value):
        if not ca_value:
            return None
        candidate = ca_value.strip().strip('"').strip("'")
        if not candidate:
            return None
        if os.path.isabs(candidate):
            return candidate.replace("\\", "/")
        return str((BASE_DIR / candidate).resolve()).replace("\\", "/")

    if raw_ca_b64:
        try:
            ca_bytes = base64.b64decode(raw_ca_b64, validate=True)
            ca_text = ca_bytes.decode('utf-8', errors='ignore')
            if 'BEGIN CERTIFICATE' not in ca_text:
                raise ValueError('TIDB_SSL_CA_B64 does not contain a valid certificate')

            tmp = tempfile.NamedTemporaryFile(delete=False, prefix='tidb_ca_', suffix='.pem')
            tmp.write(ca_bytes)
            tmp.flush()
            tmp.close()
            TIDB_SSL_CA = tmp.name.replace("\\", "/")
        except Exception as e:
            print(f"⚠️  Gagal decode TIDB_SSL_CA_B64: {e}")
            TIDB_SSL_CA = None
    elif raw_ca:
        TIDB_SSL_CA = _resolve_ca_path(raw_ca)
    else:
        TIDB_SSL_CA = None

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY    = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

    # Resend
    RESEND_API_KEY    = os.getenv('RESEND_API_KEY')
    RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev')
    RESEND_TO_EMAIL   = os.getenv('RESEND_TO_EMAIL')

    # Admin
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

