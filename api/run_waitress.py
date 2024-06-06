from waitress import serve
from API import app  # Import the Flask app from API2.py

serve(app, host='0.0.0.0', port=5000)
