from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from model import get_db
from functools import wraps

projects_bp = Blueprint('projects', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login.login_page'))
        return f(*args, **kwargs)
    return decorated


@projects_bp.route('/admin/projects')
@login_required
def projects_page():
    try:
        return render_template('admin/projects.html')
    except Exception as e:
        print(f"❌ Error in projects_page: {e}")
        return {"error": str(e)}, 500


@projects_bp.route('/api/admin/projects', methods=['GET'])
@login_required
def get_projects():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM projects ORDER BY is_featured DESC, id DESC")
                data = cur.fetchall()
            return jsonify({'success': True, 'data': data if data else []})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in get_projects: {e}")
        return jsonify({'success': False, 'error': str(e), 'data': []}), 500


@projects_bp.route('/api/admin/projects', methods=['POST'])
@login_required
def create_project():
    try:
        data = request.get_json(silent=True) or {}
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO projects (title, description, tech_stack, image_url, demo_url, repo_url, is_featured)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (data.get('title'), data.get('description'), data.get('tech_stack'),
                      data.get('image_url'), data.get('demo_url'), data.get('repo_url'), data.get('is_featured', 0)))
                cur.execute("SELECT * FROM projects ORDER BY id DESC LIMIT 1")
                saved = cur.fetchone()
            conn.commit()
            return jsonify({'success': True, 'message': 'Proyek berhasil ditambahkan', 'data': saved})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in create_project: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@projects_bp.route('/api/admin/projects/<int:pid>', methods=['PUT'])
@login_required
def update_project(pid):
    try:
        data = request.get_json(silent=True) or {}
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE projects SET title=%s, description=%s, tech_stack=%s, image_url=%s,
                    demo_url=%s, repo_url=%s, is_featured=%s WHERE id=%s
                """, (data.get('title'), data.get('description'), data.get('tech_stack'),
                      data.get('image_url'), data.get('demo_url'), data.get('repo_url'),
                      data.get('is_featured', 0), pid))
            conn.commit()
            return jsonify({'success': True, 'message': 'Proyek berhasil diupdate'})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in update_project: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@projects_bp.route('/api/admin/projects/<int:pid>', methods=['DELETE'])
@login_required
def delete_project(pid):
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM projects WHERE id=%s", (pid,))
            conn.commit()
            return jsonify({'success': True, 'message': 'Proyek berhasil dihapus'})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in delete_project: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
