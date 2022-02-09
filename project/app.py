from config.application_factory import create_app
from models import db
from os.path import exists

app = create_app("config.py")


if __name__ == "__main__":
    if not exists("database.db"):
        print("Creating database tables...")
        db.create_all(app=app)
        print("Done!")
    # different ways to start flask server
    app.run(debug=True)  # localhost
    # app.run(debug=True, host='0.0.0.0')  # host on network
    # app.run(host='0.0.0.0')  # host on network no debug
