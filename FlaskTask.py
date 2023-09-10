from flask import Flask

app = Flask(__name__)

number = 0


@app.route('/')
def add():
    global number
    number += 1
    return f'New number: {number}'

if __name__ == '__main__':
    app.run(port=5500)
