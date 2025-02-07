from flask import Flask, request
from db import init_db
from auth import auth_bp
from pantry import pantry_bp
from others import others_bp
from prediction import prediction_bp
from recipe_prediction import recipe_bp
from dotenv import load_dotenv
from flask_cors import CORS

# from flask import Response
# import os

load_dotenv()

app = Flask(__name__)

# Configure CORS with a simpler configuration
CORS(app, 
     resources={r"/*": {
         "origins": ["https://fridgepilot.vercel.app", "http://localhost:3000"],
         "methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
         "allow_headers": ["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
         "max_age": 3600,
         "supports_credentials": False  # Changed to False since we're using token-based auth
     }})

# Ensure CORS headers are set for all responses
@app.after_request
def add_cors_headers(response):
    # Get the origin from the request
    origin = request.headers.get('Origin')
    
    # If the origin is in our allowed origins, set the CORS headers
    if origin in ["https://fridgepilot.vercel.app", "http://localhost:3000"]:
        response.headers['Access-Control-Allow-Origin'] = origin
        # Allow all requested headers
        if request.headers.get('Access-Control-Request-Headers'):
            response.headers['Access-Control-Allow-Headers'] = request.headers['Access-Control-Request-Headers']
        response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, POST, OPTIONS, PUT, PATCH, DELETE'
        response.headers['Access-Control-Max-Age'] = '3600'
        response.headers['Access-Control-Allow-Credentials'] = 'false'
        
    return response

init_db()


# @app.after_request
# def add_header(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(pantry_bp, url_prefix="/pantry")
app.register_blueprint(others_bp, url_prefix="/others")
app.register_blueprint(prediction_bp, url_prefix="/prediction")
app.register_blueprint(recipe_bp, url_prefix="/recipe")

if __name__ == "__main__":
    app.run(debug=False)
