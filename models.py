from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)

    phone_numbers = db.relationship('PhoneNumber', backref='contact', cascade="all, delete-orphan")
    social_profiles = db.relationship('SocialProfile', backref='contact', cascade="all, delete-orphan")
    tags = db.relationship('Tag', backref='contact', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_favorite": self.is_favorite,
            "phone_numbers": [p.number for p in self.phone_numbers],
            "social_profiles": [{ "platform": sp.platform.name, "username": sp.username } for sp in self.social_profiles],
            "tags": [tag.name for tag in self.tags]
        }

class PhoneNumber(db.Model):
    __tablename__ = 'phone_numbers'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)

class SocialPlatform(db.Model):
    __tablename__ = 'social_platforms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    profiles = db.relationship('SocialProfile', backref='platform', cascade="all, delete-orphan")

class SocialProfile(db.Model):
    __tablename__ = 'social_profiles'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('social_platforms.id'), nullable=False)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
