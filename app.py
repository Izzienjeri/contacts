from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from models import db, Contact, PhoneNumber, SocialPlatform, SocialProfile, Tag
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

@app.before_first_request
def seed_social_platforms():
    platforms = ['TikTok', 'Instagram', 'Facebook', 'Twitter', 'LinkedIn']
    for name in platforms:
        if not SocialPlatform.query.filter_by(name=name).first():
            db.session.add(SocialPlatform(name=name))
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
