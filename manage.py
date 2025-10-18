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
    admin_username = os.environ.get("ADMIN_USERNAME")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    if admin_username is None or admin_password is None:
        print(
            "ERROR: ADMIN_USERNAME and ADMIN_PASSWORD environment variables must be set."
        )
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


@app.cli.command("create-test-user")
def create_test_user():
    """
    Creates test user from environment variables.
    Checks if the user already exists.
    """
    test_user_username = os.environ.get("TEST_USERNAME")
    test_user_password = os.environ.get("TEST_PASSWORD")
    if test_user_username is None or test_user_password is None:
        print(
            "ERROR: TEST_USERNAME and TEST_PASSWORD environment variables must be set."
        )
        return
    with app.app_context():
        if User.query.filter_by(username=test_user_password).first():
            print("ERROR: Test user already exists.")
            return
        test_user = User(username=test_user_username, is_admin=False)
        test_user.set_password(test_user_password)
        db.session.add(test_user)
        db.session.commit()
        print("Test user created.")


@app.cli.command("delete-test-user")
def delete_test_user():
    """
    Deletes test user (username=$TEST_USERNAME).
    Checks if the user exists before deleting.
    """
    test_user_username = os.environ.get("TEST_USERNAME")
    if not test_user_username:
        print("ERROR: TEST_USERNAME environment variable must be set.")
        return
    with app.app_context():
        test_user = User.query.filter_by(username=test_user_username).first()
        if not test_user:
            print("ERROR: Test user does not exist.")
            return
        db.session.delete(test_user)
        db.session.commit()


if __name__ == "__main__":
    app.run()
