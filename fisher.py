# 开始鱼书的准备
__author__ = '阮松'

# from flask import Flask

from app import create_app

app = create_app()


# app.add_url_rule('/hello', view_func=hello)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=app.config['DEBUG'], threaded=True)
