from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(20))
    birthdate = db.Column(db.Date, nullable=False)


@app.before_request
def database():
    db.create_all()


@app.route('/persons', methods=['GET'])
def get_persons():
    persons = Person.query.all()
    person_list = [{"id": person.id, "first_name": person.first_name,
                    "last_name": person.last_name, "mobile": person.mobile,
                    "birthdate": person.birthdate.strftime('%Y-%m-%d')} for person in persons]
    return jsonify({"persons": person_list})


@app.route('/persons', methods=['POST'])
def add_person():
    data = request.get_json()
    new_person = Person(
        first_name=data['first_name'],
        last_name=data['last_name'],
        mobile=data['mobile'],
        birthdate=datetime.strptime(data['birthdate'], '%Y-%m-%d')
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({'message': 'person created successfully'})


@app.route('/persons/<int:id>', methods=['PUT'])
def update_person(id):
    person = Person.query.get(id)
    if person is None:
        return jsonify({'message': 'person not found'}), 404

    data = request.get_json()
    person.first_name = data['first_name']
    person.last_name = data['last_name']
    person.mobile = data['mobile']
    person.birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d')
    db.session.commit()
    return jsonify({'message': 'person updated successfully'})


@app.route('/persons/<int:id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get(id)
    if person is None:
        return jsonify({'message': 'person not found'}), 404
    db.session.delete(person)
    db.session.commit()
    return jsonify({'message': 'person deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
