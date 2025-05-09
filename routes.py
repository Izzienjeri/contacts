from flask import request
from flask_restful import Resource
from models import db, Contact, PhoneNumber, SocialPlatform, SocialProfile, Tag

class ContactListResource(Resource):
    def get(self):
        query = request.args.get('q')
        if query:
            contacts = Contact.query.filter(Contact.name.like(f"%{query}%")).all()
        else:
            contacts = Contact.query.all()
        return {
            "message": "Contacts retrieved successfully",
            "contacts": [contact.to_dict() for contact in contacts]
        }, 200

    def post(self):
        data = request.get_json()
        phones = data.get('phone_numbers', [])
        profiles = data.get('social_profiles', [])  # List of { platform, username }
        tags = data.get('tags', [])  

        contact = Contact(
            name=data['name'],
            email=data['email'],
            is_favorite=data.get('is_favorite', False)
        )
        db.session.add(contact)
        db.session.flush()  # Get contact.id

        for phone in phones:
            db.session.add(PhoneNumber(number=phone, contact_id=contact.id))

        for profile in profiles:
            platform_name = profile['platform']
            platform = SocialPlatform.query.filter_by(name=platform_name).first()
            if platform:
                db.session.add(SocialProfile(
                    username=profile['username'],
                    contact_id=contact.id,
                    platform_id=platform.id
                ))

        for tag_name in tags:
            db.session.add(Tag(name=tag_name, contact_id=contact.id))

        db.session.commit()
        return {
            "message": "Contact created successfully",
            "contact": contact.to_dict()
        }, 201

class ContactResource(Resource):
    def get(self, id):
        contact = Contact.query.get_or_404(id)
        return {
            "message": "Contact retrieved successfully",
            "contact": contact.to_dict()
        }, 200

    def put(self, id):
        contact = Contact.query.get_or_404(id)
        data = request.get_json()

        contact.name = data.get('name', contact.name)
        contact.email = data.get('email', contact.email)
        contact.is_favorite = data.get('is_favorite', contact.is_favorite)

        # Update phone numbers
        if 'phone_numbers' in data:
            PhoneNumber.query.filter_by(contact_id=contact.id).delete()
            for phone in data['phone_numbers']:
                db.session.add(PhoneNumber(number=phone, contact_id=contact.id))

        # Update social profiles
        if 'social_profiles' in data:
            SocialProfile.query.filter_by(contact_id=contact.id).delete()
            for profile in data['social_profiles']:
                platform = SocialPlatform.query.filter_by(name=profile['platform']).first()
                if platform:
                    db.session.add(SocialProfile(
                        username=profile['username'],
                        contact_id=contact.id,
                        platform_id=platform.id
                    ))

        # Update tags
        if 'tags' in data:
            Tag.query.filter_by(contact_id=contact.id).delete()
            for tag_name in data['tags']:
                db.session.add(Tag(name=tag_name, contact_id=contact.id))

        db.session.commit()
        return {
            "message": "Contact updated successfully",
            "contact": contact.to_dict()
        }, 200

    def delete(self, id):
        contact = Contact.query.get_or_404(id)
        db.session.delete(contact)
        db.session.commit()
        return {
            "message": "Contact deleted successfully"
        }, 200
