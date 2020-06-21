from flask import Flask, current_app

app = Flask(__name__)
# ctx = app.app_context()
# ctx.push()
# a = current_app
# d = current_app.config['DEBUG']
# ctx.pop()

with app.app_context():
    a = current_app
    d = current_app.config['DEBUG']


class A:
    def __enter__(self):
        print('我是enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('我是exit')

    @staticmethod
    def query():
        print('我是查询语句')


with A() as obj_A:
    1/0
    obj_A.query()
    print(obj_A)
