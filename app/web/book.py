import json

from flask import jsonify, make_response, request, render_template, flash
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
from . import web
from ..models.gift import Gift
from ..models.wish import Wish
from ..view_models.book import BookViewModel, BookCollection
from ..view_models.trade import TradeInfo


@web.route('/test')
def test():
    from app.libs.none_local import n
    from flask import request
    print('----------------------------')
    print(n.v)
    n.v = 2
    print(getattr(request, 'v', None))
    setattr(request, 'v', 2)
    print('--------------------------')
    r = {
        'name': '阮松',
        'age': 24
    }
    flash('hello, Tom', category='success')
    return render_template('test.html', data=r)


@web.route('/book/search')
def search():
    # q = request.args['q']
    # page = request.args['page']
    args = request.args
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()
        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
            # result = YuShuBook.search_by_isbn(q)
            # result = BookViewModel.package_single(result, q)
        else:
            yushu_book.search_by_keyword(q, page)
            # result = YuShuBook.search_by_keyword(q, page)
            # result = BookViewModel.package_collection(result, q)
        books.fill(yushu_book, q)

        #     dict 序列化
        # return json.dumps(books, default=lambda o: o.__dict__), 200, {'content-type': 'application/json',
        # 'Access-Control-Allow-Origin': '*'}
        # return jsonify(books.__dict__)
        # return json.dumps(result), 200, {'content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    else:
        # return jsonify(form.errors)
        flash('未查找到符合要求的书籍！')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)
    return render_template('book_detail.html', book=book, wishes=trade_wishes_model,
                           gifts=trade_gifts_model, has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)


@web.route('/hello')
def hello():
    headers = {
        'content-type': 'text/plain',
        # 'content-type': 'application/json',
        # 'location': 'http://www.baidu.com'  # 重定向
    }
    response = make_response('<html></html>', 200)
    response.headers = headers
    return response

    # 简洁版写法
    # return '<html></html>', 301, headers
