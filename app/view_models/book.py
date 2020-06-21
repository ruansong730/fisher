class BookViewModel:
    def __init__(self, data):
        self.title = data['title']
        self.author = '、'.join(data['author'])
        self.publisher = data['publisher']
        self.image = data['image']
        self.price = '￥' + data['price'] if data['price'] else data['price']
        self.isbn = data['isbn']
        self.summary = data['summary']
        self.pages = data['pages']
        self.binding = data['binding']
        self.pubdate = data['pubdate']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return ' / '.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


class __BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            "book": [],
            "total": 0,
            "keyword": keyword
        }
        if data:
            returned['total'] = 1
            returned['book'] = cls.__cut_book_data(data)
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            "book": [],
            "total": 0,
            "keyword": keyword
        }
        if data:
            returned['total'] = data['total']
            returned['book'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book
