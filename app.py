from flask import Flask
from routes import bp as main_routes

app = Flask(__name__)

# Registering the blueprint
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
