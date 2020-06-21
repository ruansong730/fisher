from time import sleep

from app.libs.http import Http
from app.models.test import Test1
from . import web
from flask import session, request


@web.route('/session')
def test_session():
    session['test'] = 123
    return ''

@web.route('/record')
def test_reord():
    s = request.remote_addr
    return s

@web.route('/test')
def test_ip():
    from app.models.test import Test
    t1 = Test1()
    t2 = Test1()
    # t1.test = 1
    # t2.test = 2
    t1.test1 = 3
    print(t1.test)
    print(t2.test)
    print(Test1.test)
    pass


@web.route('/get/session')
def get_test_session():
    t = session['_fresh']
    return str(t)

s = 'insert into table values (%s, %s, %s)' % (1,2,3)




