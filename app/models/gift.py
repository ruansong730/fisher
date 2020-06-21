import base as base
from flask import current_app

from app.spider.yushu_book import YuShuBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship
from app.models.base import db, Base


class Gift(Base):
    # __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_gifts(cls, uid):
        gift = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gift

    @classmethod
    def get_wish_counts(cls, isbn_list):
        #根据传入的的isbn，查询Gift表中的相应礼物，并计算出某个礼物的心愿数量
        count = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(Gift.isbn).all()
        count_list = [{'count': gift[0], 'isbn': gift[1]} for gift in count]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        recent_gift = Gift.query.filter_by(
            launched=False).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).all()
        return recent_gift


# .group_by(
#             Gift.isbn).order_by(
#             Gift.create_time).limit(
#             current_app.config['RECENT_BOOK_COUNT']).distinct()