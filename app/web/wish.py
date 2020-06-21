from flask import current_app, flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import web
from .. import db
from ..models.wish import Wish
from ..view_models.wish import MyWishes


@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    get_wishes_of_mine = Wish.get_user_wishes(uid)
    wishes_isbn = [wish.isbn for wish in get_wishes_of_mine]
    wishes_count_list = Wish.get_gift_counts(wishes_isbn)
    wishes_model = MyWishes(get_wishes_of_mine, wishes_count_list)
    return render_template('my_wish.html', wishes=wishes_model.my_gifts)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        # 事务
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish():
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish():
    pass


