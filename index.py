"""
WSGI entry point for Vercel.
"""
import os
import sys
import traceback

from flask import Flask

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_app():
    try:
        from app import app as flask_app
        return flask_app
    except Exception as exc:
        print("❌ Failed to load Flask app, using fallback app.")
        traceback.print_exc()

        fallback_app = Flask(__name__)

        @fallback_app.route('/')
        @fallback_app.route('/<path:path>')
        def fallback_handler(path=None):
            return {
                "error": "Application failed to initialize",
                "type": type(exc).__name__,
                "message": str(exc),
            }, 500

        return fallback_app


app = application = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
