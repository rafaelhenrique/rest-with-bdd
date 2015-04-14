from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

books = [
    {
        'id': 1,
        'title': u'Python Cookbook',
        'tags': [u'Python', u'Algorithms', u'Development'],
        'authors': [u'David Beazley', u'Brian K. Jones'],
        'publishing': [u"O'Reilly", u'Novatec']
    },
    {
        'id': 2,
        'title': u'Flask Cookbook',
        'tags': [u'Python', u'Algorithms', u'Development', u'Flask'],
        'authors': [u'Shalabh Aggarwal'],
        'publishing': u'PACKT'
    },
    {
        'id': 3,
        'title': u'Flask Web Development',
        'tags': [u'Python', u'Algorithms', u'Development', u'Flask'],
        'authors': [u'Miguel Grinberg'],
        'publishing': u"O'Reilly"
    },
]


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def create_uris(book):
    new_uri = {}
    for field in book:
        if field == 'id':
            new_uri['uri'] = url_for(
                'get_book', book_id=book['id'], _external=True)
        else:
            new_uri[field] = book[field]
    return new_uri


@app.route('/library/api/books', methods=['GET'])
def get_books():
    return jsonify({'books': [create_uris(book) for book in books]})


@app.route('/library/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})


@app.route('/library/api/books', methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.json['title'],
        'tags': request.json['tags'],
        'authors': request.json['authors'],
        'publishing': request.json['publishing'],
    }
    books.append(book)
    return jsonify({'book': book}), 201


@app.route('/library/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if ('title' in request.json and
            not isinstance(request.json['title'], str)):
        abort(400)
    if ('tags' in request.json and
            not isinstance(request.json['tags'], str)):
        abort(400)

    # more things need be validated
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['tags'] = request.json.get('tags', book[0]['tags'])
    return jsonify({'book': book[0]})


@app.route('/library/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
