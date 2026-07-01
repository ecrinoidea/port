from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from model import get_db
from functools import wraps

profiles_bp = Blueprint('profiles', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login.login_page'))
        return f(*args, **kwargs)
    return decorated


@profiles_bp.route('/admin/profiles')
@login_required
def profiles_page():
    try:
        return render_template('admin/profiles.html')
    except Exception as e:
        print(f"❌ Error in profiles_page: {e}")
        return {"error": str(e)}, 500


@profiles_bp.route('/api/admin/profiles', methods=['GET'])
@login_required
def get_profiles():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM profiles")
                data = cur.fetchall()
            return jsonify({'success': True, 'data': data if data else []})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in get_profiles: {e}")
        return jsonify({'success': False, 'error': str(e), 'data': []}), 500


@profiles_bp.route('/api/admin/profiles', methods=['POST'])
@login_required
def create_profile():
    try:
        data = request.get_json(silent=True) or {}
        if not data.get('name'):
            return jsonify({'success': False, 'message': 'Nama wajib diisi'}), 400
        
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO profiles (name, title, bio, email, phone, location, github, linkedin, instagram, photo_url)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (data.get('name'), data.get('title'), data.get('bio'),
                      data.get('email'), data.get('phone'), data.get('location'),
                      data.get('github'), data.get('linkedin'), data.get('instagram'), data.get('photo_url')))
                cur.execute("SELECT * FROM profiles ORDER BY id DESC LIMIT 1")
                saved = cur.fetchone()
            conn.commit()
            return jsonify({'success': True, 'message': 'Profil berhasil ditambahkan', 'data': saved})
        finally:
            conn.close()
    except Exception as e:
        print(f'❌ Error in create_profile: {str(e)}')
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@profiles_bp.route('/api/admin/profiles/<int:pid>', methods=['PUT'])
@login_required
def update_profile(pid):
    try:
        data = request.get_json(silent=True) or {}
        if not data.get('name'):
            return jsonify({'success': False, 'message': 'Nama wajib diisi'}), 400
        
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE profiles SET name=%s, title=%s, bio=%s, email=%s, phone=%s,
                    location=%s, github=%s, linkedin=%s, instagram=%s, photo_url=%s WHERE id=%s
                """, (data.get('name'), data.get('title'), data.get('bio'),
                      data.get('email'), data.get('phone'), data.get('location'),
                      data.get('github'), data.get('linkedin'), data.get('instagram'), data.get('photo_url'), pid))
                cur.execute("SELECT * FROM profiles WHERE id=%s", (pid,))
                saved = cur.fetchone()
            conn.commit()
            if not saved:
                return jsonify({'success': False, 'message': 'Profil tidak ditemukan'}), 404
            return jsonify({'success': True, 'message': 'Profil berhasil diupdate', 'data': saved})
        finally:
            conn.close()
    except Exception as e:
        print(f'❌ Error in update_profile: {str(e)}')
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@profiles_bp.route('/api/admin/profiles/<int:pid>', methods=['DELETE'])
@login_required
def delete_profile(pid):
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM profiles WHERE id=%s", (pid,))
            conn.commit()
            return jsonify({'success': True, 'message': 'Profil berhasil dihapus'})
        finally:
            conn.close()
    except Exception as e:
        print(f'❌ Error in delete_profile: {str(e)}')
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
