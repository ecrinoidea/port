from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from config import Config

login_bp = Blueprint('login', __name__)


@login_bp.route('/admin/login', methods=['GET'])
def login_page():
    if session.get('admin_logged_in'):
        return redirect(url_for('dashboard.dashboard_page'))
    return render_template('admin/login.html')


@login_bp.route('/admin/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        session['admin_username'] = username
        return jsonify({'success': True, 'message': 'Login berhasil'})
    return jsonify({'success': False, 'message': 'Username atau password salah'}), 401


@login_bp.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login_page'))
