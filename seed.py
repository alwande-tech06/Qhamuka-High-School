"""Seed script — creates the database tables and a default admin profile.

Usage:
    python seed.py

Override the defaults with environment variables before running:
    ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
"""
import os

from app import create_app
from app.models import db, Admin

app = create_app(os.environ.get('FLASK_CONFIG') or 'development')

DEFAULT_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
DEFAULT_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@qhamukahigh.co.za')
DEFAULT_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Qhamuka@2026')


def seed():
    with app.app_context():
        db.create_all()

        existing = Admin.query.filter_by(username=DEFAULT_USERNAME).first()
        if existing:
            print(f'Admin "{DEFAULT_USERNAME}" already exists — nothing to seed.')
            return

        admin_user = Admin(
            username=DEFAULT_USERNAME,
            email=DEFAULT_EMAIL,
            role='Administrator',
        )
        admin_user.set_password(DEFAULT_PASSWORD)
        db.session.add(admin_user)
        db.session.commit()

        print('Default admin created:')
        print(f'  username: {DEFAULT_USERNAME}')
        print(f'  password: {DEFAULT_PASSWORD}')
        print('  >> Change this password after first login.')


if __name__ == '__main__':
    seed()
