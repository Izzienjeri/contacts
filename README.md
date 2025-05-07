# Jack - get requests

curl http://127.0.0.1:5000/contacts

curl http://127.0.0.1:5000/contacts/1


# Sly - POST (creating a contact)

curl -X POST -H "Content-Type: application/json" \-d '{"name": "Sly", "email": "sly@example.com", "is_favorite": true, "phone_numbers": ["072223333"]}' \http://127.0.0.1:5000/contacts


# Hillary (put request) - updating a specific field

curl -X PUT -H "Content-Type: application/json" \-d '{"email": "s@example.com"}' \http://127.0.0.1:5000/contacts/6

# izzie - updating all the fields

curl -X PUT -H "Content-Type: application/json" \-d '{"name": "izzie", "email": "izzie@gmail.com", "is_favorite": false, "phone_numbers": ["0723445555"]}' \http://127.0.0.1:5000/contacts/5

# sam - removing a contact

curl -X DELETE http://127.0.0.1:5000/contacts/4

































