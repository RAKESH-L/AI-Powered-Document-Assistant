from app import create_app
from config import Config
from flask_cors import CORS


app = create_app()
app.config.from_object(Config)
CORS(app)  # This will enable CORS for all routes of your Flask app


if __name__ == '__main__':
    app.run()
 