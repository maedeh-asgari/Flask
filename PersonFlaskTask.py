from flask import Flask, session, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///person.db"

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    age = db.Column(db.Integer)
    email = db.Column(db.String(500))

    def __repr__(self):
        return f'{self.name}-{self.lastname}-{self.age}-{self.email}'


@app.route('/')
def main():
    p1 = Person(name='Maedeh', lastname='Asgari', age=23, email='maedeh@gmail.com')
    db.session.add(p1)
    db.session.commit()
    p2 = Person(name='Helia', lastname='Ahmadi', age=18, email='helia@gmail.com')
    db.session.add(p2)
    db.session.commit()
    persons = Person.query.all()
    return render_template('base.html', persons=persons)


@app.before_request
def dbconnection():
    db.create_all()
    print("Database was created")


if __name__ == '__main__':
    app.run(debug=True)
