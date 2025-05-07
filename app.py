from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from models import db
from config import Config
from routes import ContactListResource, ContactResource

app = Flask(__name__)
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{Config.MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

api.add_resource(ContactListResource, '/contacts')
api.add_resource(ContactResource, '/contacts/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
