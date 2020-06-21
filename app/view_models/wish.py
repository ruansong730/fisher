from .book import BookViewModel
from collections import namedtuple

GiftWishCount = namedtuple('GiftWishCount', ['wishes_count', 'book', 'id'])


class MyWishes:
    def __init__(self, gifts, wishes_count):
        self.my_gifts = []
        self.__gift_of_mine = gifts
        self.__wish_count_list = wishes_count

        self.my_gifts = self.__parse(self.__gift_of_mine)

    # def package(self):
    #     return self.my_gifts

    def __parse(self, gifts):
        temp_gifts = []
        for gift in gifts:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
            r = {
                'wishes_count': count,
                'book': BookViewModel(gift.book),
                'id': gift.id
            }
            # my_gift = GiftWishCount(count, BookViewModel(gift.book), gift.id)
            return r
