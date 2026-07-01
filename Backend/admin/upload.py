import os
import cloudinary
import cloudinary.uploader
from flask import Blueprint, request, jsonify, session, redirect, url_for
from config import Config
from functools import wraps

upload_bp = Blueprint('upload', __name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME') or Config.CLOUDINARY_CLOUD_NAME,
    api_key=os.getenv('CLOUDINARY_API_KEY') or Config.CLOUDINARY_API_KEY,
    api_secret=os.getenv('CLOUDINARY_API_SECRET') or Config.CLOUDINARY_API_SECRET
)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login.login_page'))
        return f(*args, **kwargs)
    return decorated


@upload_bp.route('/api/admin/upload', methods=['POST'])
@login_required
def upload_image():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'Tidak ada file yang diupload'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Nama file kosong'}), 400

        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in allowed_extensions:
            return jsonify({'success': False, 'message': 'Format file tidak didukung. Gunakan: png, jpg, jpeg, gif, webp'}), 400

        # Check if Cloudinary is configured
        if not Config.CLOUDINARY_CLOUD_NAME or not Config.CLOUDINARY_API_KEY:
            return jsonify({'success': False, 'message': 'Cloudinary belum dikonfigurasi'}), 500

        result = cloudinary.uploader.upload(
            file,
            folder='portofolio',
            resource_type='image'
        )
        return jsonify({
            'success': True,
            'url': result['secure_url'],
            'public_id': result['public_id'],
            'message': 'Gambar berhasil diupload ke Cloudinary'
        })
    except Exception as e:
        print(f'❌ Upload error: {str(e)}')
        return jsonify({'success': False, 'message': f'Upload gagal: {str(e)}'}), 500
