"""
This file runs the flask server, be sure to read the options below to choose how
to run the server, the built in server is not meant for production use. Please
see the flask documentation for more info on how to deploy the server.

!The first time this runs it will create the database file and ask for a secret key
!to encrypt the jwt tokens
"""
from config.application_factory import create_app
from models import DB, TokenBlocklist, delete_from_database
from config.config import ACCESS_EXPIRES
from os.path import exists
from datetime import datetime
from flask_apscheduler import APScheduler

SCHEDULER = APScheduler()
APP = create_app("config.py")

# scheduler tasks
@SCHEDULER.task("interval", id="delete_expired_tokens", hours=1, misfire_grace_time=500)
def remove_expired_tokens() -> None:
    """Every hour remove expired tokens as they are no longer valid anyway,
    so there is no need to continue to store them"""
    with APP.app_context():
        tokens = TokenBlocklist.query.all()
        for token in tokens:
            if (datetime.now() - token.revoked_at).seconds >= ACCESS_EXPIRES.seconds:
                delete_from_database(token)


if __name__ == "__main__":
    if not exists("database.db"):
        print("Creating database tables...")
        DB.create_all(app=APP)
        print("Done!")

    SCHEDULER.init_app(APP)

    SCHEDULER.start()

    # ?debug will check for updates to code and refresh server automatically
    APP.run(debug=True)  # ?localhost with debug on
    # APP.run(debug=True, host='0.0.0.0')  # ?host on network with debug on
    # APP.run(host='0.0.0.0')  # ?host on network no debug
