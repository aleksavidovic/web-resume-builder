import os
from resume_builder import create_app, db
from resume_builder.models import User

app = create_app()

@app.cli.command("create-admin")
def create_admin():
    """
    Creates admin user from environment variables.
    Checks if the user already exists.
    """
    admin_username = os.environ.get('ADMIN_USERNAME')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    if admin_username is None or admin_password is None:
        print("ERROR: ADMIN_USERNAME and ADMIN_PASSWORD environment variables must be set.")
        return
    # check if exists already
    with app.app_context():
        if User.query.filter_by(username=admin_username).first():
            print("ERROR: Admin already exists")
            return
        admin = User(username=admin_username, is_admin=True)
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print("Admin created.")


if __name__ == "__main__":
    app.run()

