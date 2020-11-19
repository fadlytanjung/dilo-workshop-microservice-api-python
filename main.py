import os

from dotenv import load_dotenv
from app import create_app, db

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('ENV') or 'development')

if __name__ == '__main__':
    app.run(debug=True,host=os.getenv('HOST'),port=os.getenv('PORT'))


