from flask import request
from flask_restful import Resource
from models import db, Contact, PhoneNumber

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

        contact = Contact(
            name=data['name'],
            email=data['email'],
            is_favorite=data.get('is_favorite', False)
        )
        db.session.add(contact)
        db.session.flush() 

        for phone in phones:
            db.session.add(PhoneNumber(number=phone, contact_id=contact.id))

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

    # update a specific contact
    def put(self, id):
        
        contact = Contact.query.get_or_404(id)
        data = request.get_json()

        contact.name = data.get('name', contact.name)
        contact.email = data.get('email', contact.email)
        contact.is_favorite = data.get('is_favorite', contact.is_favorite)

        if 'phone_numbers' in data:
            PhoneNumber.query.filter_by(contact_id=contact.id).delete()
            for phone in data['phone_numbers']:
                db.session.add(PhoneNumber(number=phone, contact_id=contact.id))

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


