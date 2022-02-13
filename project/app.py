"""
This file runs the flask server, be sure to read the options below to choose how
to run the server, the built in server is not meant for production use. Please
see the flask documentation for more info on how to deploy the server.

!The first time this runs it will create the database file and ask for a secret key
!to encrypt the jwt tokens
"""
from config.application_factory import create_app
from models import DB
from os.path import exists


APP = create_app("config.py")


if __name__ == "__main__":
    if not exists("database.db"):
        print("Creating database tables...")
        DB.create_all(app=APP)
        print("Done!")

    # ?debug will check for updates to code and refresh server automatically
    APP.run(debug=True)  # ?localhost with debug on
    # APP.run(debug=True, host='0.0.0.0')  # ?host on network with debug on
    # APP.run(host='0.0.0.0')  # ?host on network no debug
