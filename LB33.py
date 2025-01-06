from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

# Начальный список книг
books = {
    1: {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "price": "10.99",
        "genre": "Fiction"
    },
    2: {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "price": "8.99",
        "genre": "Dystopian"
    },
    3: {
        "id": 3,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "price": "12.99",
        "genre": "Fiction"
    }
}

users = {"admin": "password"}  # Легкое хранение пользователей


# Функция для базовой аутентификации
def check_auth(username, password):
    return username in users and users[username] == password


def authenticate():
    return jsonify({"message": "Authentication required"}), 401


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/books', methods=['GET', 'POST'])
@requires_auth
def manage_books():
    if request.method == 'POST':
        book = request.get_json()  # Получаем JSON из запроса

        # Проверка наличия необходимых полей
        if 'id' not in book or 'title' not in book or 'author' not in book or 'price' not in book or 'genre' not in book:
            return jsonify({"error": "Missing book data"}), 400

        # Добавление книги в каталог
        books[book['id']] = book
        return jsonify(book), 201

    # Возвращение списка всех книг
    return jsonify(list(books.values()))


@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@requires_auth
def book_detail(id):
    if request.method == 'GET':
        book = books.get(id)
        if book is None:
            return jsonify({"error": "Book not found"}), 404
        return jsonify(book)

    elif request.method == 'PUT':
        book = request.get_json()

        if id not in books:
            return jsonify({"error": "Book not found"}), 404

        # Обновление данных книги
        books[id] = book
        return jsonify(book)

    elif request.method == 'DELETE':
        if id in books:
            del books[id]
            return jsonify({"result": "Book deleted"})
        return jsonify({"error": "Book not found"}), 404


if __name__ == '__main__':
    app.run(port=6000, debug=True)  # Запуск сервера на порту 6000