import base as base

from app.spider.yushu_book import YuShuBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, func, desc
from sqlalchemy.orm import relationship
from app.models.base import db, Base


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        # 根据传入的的isbn，查询Wish表中的相应礼物，并计算出某个礼物的心愿数量
        count = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{'count': wish[0], 'isbn': wish[1]} for wish in count]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
