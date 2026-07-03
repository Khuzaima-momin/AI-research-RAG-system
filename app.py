from flask import Flask
from config import Config
from routes.main_routes import main
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ensure upload folder exists
    os.makedirs("uploads", exist_ok=True)

    app.register_blueprint(main)

    return app


app = create_app()

if __name__ == "__main__":
    print("Starting AI Research Assistant...")
    app.run(debug=True)