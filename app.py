import json

import firebase_admin
from flask import Flask, request, jsonify
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin.firestore import SERVER_TIMESTAMP

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__)


@app.route("/blood_seekers", methods=['GET', 'POST'])
def blood():
    class blood_seekers:
        def __init__(self, nameSurname, dateOfSearch, blood, city, hospital, type, contact):
            self.nameSurname = str(nameSurname)
            self.dateOfSearch = str(dateOfSearch)
            self.blood = str(blood)
            self.city = str(city)
            self.hospital = str(hospital)
            self.type = str(type)
            self.contact = str(contact)

    firestore_db = firestore.client()
    transfers = []
    if request.headers.get('key') == key:
        f = firestore_db.collection('Blood_Seekers').order_by('TimeStamp',
                                                              direction=firestore.Query.DESCENDING).get()
        for doc in f:
            nameSurname = str(doc.get('name'))
            city = str(doc.get('city'))
            dateOfSearch = str(doc.get('date'))
            hospital = str(doc.get('hospital'))
            contact = str(doc.get('number'))
            blood = str(doc.get('blood'))
            type = str(doc.get('type'))
            search = blood_seekers(nameSurname, dateOfSearch, blood, city, hospital, type, contact)
            transfers.append(search)

        class PersonEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, blood_seekers):
                    return {'nameSurname': o.nameSurname, 'dateOfSearch': o.dateOfSearch, 'blood': o.blood,
                            'city': o.city, 'hospital': o.hospital, 'type': o.type, 'contact': o.contact}
                return super().default(o)

        jsonified_p = json.dumps(transfers, cls=PersonEncoder, indent=7)
        return jsonified_p
    else:
        return f'error'


@app.route("/cell_seekers")
def cell():
    class cell_seekers:
        def __init__(self, nameSurname, dateOfSearch, age, city, hospital, type, contact):
            self.nameSurname = str(nameSurname)
            self.dateOfSearch = str(dateOfSearch)
            self.age = str(age)
            self.city = str(city)
            self.hospital = str(hospital)
            self.type = str(type)
            self.contact = str(contact)

    firestore_db = firestore.client()
    transfers = []
    if request.headers.get('key') == key:
        f = firestore_db.collection('Cell_Seekers').order_by('TimeStamp', direction=firestore.Query.DESCENDING).get()
        for doc in f:
            nameSurname = str(doc.get('name'))
            city = str(doc.get('city'))
            dateOfSearch = str(doc.get('date'))
            hospital = str(doc.get('hospital'))
            contact = str(doc.get('number'))
            age = str(doc.get('age'))
            type = str(doc.get('type'))
            search = cell_seekers(nameSurname, dateOfSearch, age, city, hospital, type, contact)
            transfers.append(search)

        class PersonEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, cell_seekers):
                    return {'nameSurname': o.nameSurname, 'dateOfSearch': o.dateOfSearch, 'age': o.age,
                            'city': o.city, 'hospital': o.hospital, 'type': o.type, 'contact': o.contact}
                return super().default(o)

        jsonified_p = json.dumps(transfers, cls=PersonEncoder, indent=7)
        return jsonified_p
    else:
        return f'error'


@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST' and request.headers.get('key') == key:
        name = request.json.get('fullName')
        city = request.json.get('city')
        blood = request.json.get('blood')
        number = request.json.get('telephoneNumber')
        email = request.json.get('userEmail')
        transfers = {"name": name, "blood": blood, "city": city, "number": number, "email": email}
        db = firestore.client()
        db.collection('Users').add(transfers)
        oncomplete = {"oncomplete": "oncomplete"}
        return jsonify(oncomplete)
    else:
        return f'error'


@app.route("/cell_search", methods=['GET', 'POST'])
def cell_search():
    if request.method == 'POST' and request.headers.get('key') == key:
        name = request.json.get('name')
        age = request.json.get('age')
        number = request.json.get('number')
        hospital = request.json.get('hospital')
        city = request.json.get('city')
        diseases = request.json.get('diseases')
        userEmail = request.json.get('userEmail')
        date = request.json.get('date')
        transfers = {"name": name, "age": age, "number": number, "hospital": hospital, "city": city,
                     "type": diseases, "userEmail": userEmail, "date": date, "TimeStamp": SERVER_TIMESTAMP}
        transfers2 ={"city": city, "bloodorage": age, "type": diseases, "name": name, "hospital": hospital,
                     "number": number, "userEmail": userEmail, "date": date, "TimeStamp": SERVER_TIMESTAMP}
        db = firestore.client()
        db.collection('Cell_Seekers').add(transfers)
        db.collection('Searches').add(transfers2)
        oncomplete = {"oncomplete": "oncomplete"}
        return jsonify(oncomplete)
    else:
        return f'error'

@app.route("/blood_search", methods=['GET', 'POST'])
def blood_search():
    if request.method == 'POST' and request.headers.get('key') == key:
        city = request.json.get('city')
        blood = request.json.get('blood')
        searchType = request.json.get('type')
        name = request.json.get('patient')
        hospital = request.json.get('hospital')
        number = request.json.get('contact')
        userEmail = request.json.get('userEmail')
        date = request.json.get('date')
        transfers = {"city": city, "blood": blood, "type": searchType, "name": name, "hospital": hospital,
                     "number": number, "userEmail": userEmail, "date": date, "TimeStamp": SERVER_TIMESTAMP}
        transfers2 ={"city": city, "bloodorage": blood, "type": searchType, "name": name, "hospital": hospital,
                     "number": number, "userEmail": userEmail, "date": date, "TimeStamp": SERVER_TIMESTAMP}
        db = firestore.client()
        db.collection('Blood_Seekers').add(transfers)
        db.collection('Searches').add(transfers2)
        oncomplete = {"oncomplete": "oncomplete"}
        return jsonify(oncomplete)
    else:
        return f'error'


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST' and request.headers.get('key') == key:
        userEmail = request.json.get('userEmail')
        date = request.json.get('date')
        firestore_db = firestore.client()
        cell = firestore_db.collection('Cell_Seekers').where(u'userEmail', u'==', userEmail).where(u'date', u'==',
                                                                                                   date).stream()
        for doc in cell:
            cell_id = doc.id
            firestore_db.collection('Cell_Seekers').document(cell_id).delete()
        blood = firestore_db.collection('Blood_Seekers').where(u'userEmail', u'==', userEmail).where(u'date', u'==',
                                                                                                     date).stream()
        for doc2 in blood:
            blood_id = doc2.id
            firestore_db.collection('Blood_Seekers').document(blood_id).delete()
        search =firestore_db.collection('Searches').where(u'userEmail',u'==',userEmail).where(u'date',u'==',date).stream()
        for doc3 in search:
            search_id = doc3.id
            firestore_db.collection('Searches').document(search_id).delete()
        oncomplete = {"oncomplete": "oncomplete"}
        return jsonify(oncomplete)
    else:
        return f'error'


@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST' and request.headers.get('key') == key:
        userEmail = request.json.get('userEmail')
        firestore_db = firestore.client()
        db = firestore_db.collection('Users').where(u'email', u'==', userEmail).stream()
        for doc in db:
            name = doc.get('name')
            number = doc.get('number')
            city = doc.get('city')
            blood = doc.get('blood')
            transfers = {'name': name, 'number': number, 'city': city,
                         'blood': blood}
        return jsonify(transfers)
    else:
        return f'error'

@app.route("/email_update", methods=['GET', 'POST'])
def email_update():
    if request.method == 'POST' and request.headers.get('key') == key:
        email = request.json.get('email')
        user_email = request.json.get('userEmail')
        firestore_db = firestore.client()
        db = firestore_db.collection('Users').where(u'email', u'==', email).stream()
        for doc in db:
            db_id = doc.id
            firestore_db.collection('Users').document(db_id).update({"email": user_email})
        oncomplete = {"oncomplete": "oncomplete"}
        return jsonify(oncomplete)
    else:
        return f'error'


@app.route("/telephone_number_update", methods=['GET', 'POST'])
def telephone_number_update():
    if request.method == 'POST' and request.headers.get('key') == key:
        number = request.json.get('number')
        email = request.json.get('email')
        firestore_db = firestore.client()
        db = firestore_db.collection('Users').where(u'email', u'==', email).stream()
        for doc in db:
            db_id = doc.id
            firestore_db.collection('Users').document(db_id).update({"number": number})
        oncomplete = {"oncomplete": "oncomplete"}
        return jsonify(oncomplete)
    else:
        return f'error'


@app.route("/city_update", methods=['GET', 'POST'])
def city_update():
    if request.method == 'POST' and request.headers.get('key') == key:
        email = request.json.get('email')
        city = request.json.get('city')
        firestore_db = firestore.client()
        db = firestore_db.collection('Users').where(u'email', u'==', email).stream()
        for doc in db:
            db_id = doc.id
            firestore_db.collection('Users').document(db_id).update({"city": city})
        oncomplete = {"oncomplete": "oncomplete"}
        return jsonify(oncomplete)
    else:
        return f'eroor'


@app.route("/searches")
def searches():
    class Searches:
        def __init__(self, nameSurname, dateOfSearch, blood_or_age, city, hospital, type, contact):
            self.nameSurname = str(nameSurname)
            self.dateOfSearch = str(dateOfSearch)
            self.blood_or_age = str(blood_or_age)
            self.city = str(city)
            self.hospital = str(hospital)
            self.type = str(type)
            self.contact = str(contact)

    firestore_db = firestore.client()
    transfers = []
    if request.headers.get('key') == key:
        userEmail=request.headers.get('userEmail')
        f = firestore_db.collection('Searches').order_by('TimeStamp', direction=firestore.Query.DESCENDING).where(u'userEmail', u'==', userEmail).stream()
        for doc in f:
            nameSurname = str(doc.get('name'))
            city = str(doc.get('city'))
            dateOfSearch = str(doc.get('date'))
            hospital = str(doc.get('hospital'))
            contact = str(doc.get('number'))
            blood_or_age = str(doc.get('bloodorage'))
            type = str(doc.get('type'))
            search = Searches(nameSurname, dateOfSearch, blood_or_age, city, hospital, type, contact)
            transfers.append(search)

        class PersonEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, Searches):
                    return {'nameSurname': o.nameSurname, 'dateOfSearch': o.dateOfSearch, 'blood_or_age': o.blood_or_age,
                            'city': o.city, 'hospital': o.hospital, 'type': o.type, 'contact': o.contact}
                return super().default(o)

        jsonified_p = json.dumps(transfers, cls=PersonEncoder, indent=7)
        return jsonified_p
    else:
        return f'error'


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.debug = True
    app.run()
