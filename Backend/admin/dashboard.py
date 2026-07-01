from flask import Blueprint, render_template, session, redirect, url_for
from model import get_db
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login.login_page'))
        return f(*args, **kwargs)
    return decorated


@dashboard_bp.route('/admin')
@dashboard_bp.route('/admin/dashboard')
@login_required
def dashboard_page():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) as cnt FROM profiles")
                profiles_count = cur.fetchone()['cnt']
                cur.execute("SELECT COUNT(*) as cnt FROM skills")
                skills_count = cur.fetchone()['cnt']
                cur.execute("SELECT COUNT(*) as cnt FROM experiences")
                exp_count = cur.fetchone()['cnt']
                cur.execute("SELECT COUNT(*) as cnt FROM projects")
                proj_count = cur.fetchone()['cnt']
                cur.execute("SELECT COUNT(*) as cnt FROM contacts WHERE is_read = 0")
                unread_count = cur.fetchone()['cnt']
            stats = {
                'profiles': profiles_count,
                'skills': skills_count,
                'experiences': exp_count,
                'projects': proj_count,
                'unread_messages': unread_count
            }
            return render_template('admin/dashboard.html', stats=stats)
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in dashboard: {e}")
        stats = {
            'profiles': 0,
            'skills': 0,
            'experiences': 0,
            'projects': 0,
            'unread_messages': 0
        }
        return render_template('admin/dashboard.html', stats=stats), 200
