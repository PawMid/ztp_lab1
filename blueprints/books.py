from flask import request, jsonify
from flask.blueprints import Blueprint
from controllers import book_controller, rental_controller, user_controller

books_blueprint = Blueprint('book_blueprint', __name__, template_folder=r'../templates')


@books_blueprint.route('/books', methods=['GET'])
def book():
    if request.method == 'GET':
        available = True if request.args.get('available') == '1' else False
        books = book_controller.get_all()
        if not available:
            rented = []
            for book_data in books:
                book_data['rented'] = rental_controller.count_rentals(book_data['id'])
                rented.append(book_data)
            return jsonify(rented)
        else:
            not_rented = []
            for book_data in books:
                count = rental_controller.count_rentals(book_data['id'])
                if book_data['quantity'] - count > 0:
                    book_data['rented'] = count
                    not_rented.append(book_data)
            return jsonify(not_rented)


@books_blueprint.route('/books/<int:id>', methods=['GET'])
def book_details(id: int):
    if request.method == 'GET':
        if book_controller.book_exist(id):
            book_data = book_controller.get_book(id)
            rented_by = rental_controller.book_rented_by(id)
            book_data['rentals'] = rented_by
            return jsonify(book_data)
        else:
            return 'Brak książki w systemie', 404


@books_blueprint.route('/books/rent/<int:book_id>', methods=['PATCH'])
def rent(book_id: int):
    if request.method == 'PATCH':
        user_id = request.headers['user_id']
        try:
            user_id = int(user_id)
        except Exception as e:
            print(e)
            return 'Podany identyfikator użytkownika nie istnieje lub jest nieprawidłowy', 401
        if not book_controller.book_exist(book_id):
            return 'Podany identyfikator książki nie istnieje lub jest nieprawidłowy', 400

        if not user_controller.exist(id=user_id):
            return 'Podany identyfikator użytkownika nie istnieje lub jest nieprawidłowy', 401

        book_data = book_controller.get_book(book_id)
        rented = rental_controller.count_rentals(book_id)

        if book_data['quantity'] - rented > 0:
            rent_id = rental_controller.rent_book(book_id, user_id)
            book_data['rentals'] = rental_controller.get_rental_obj_by_id(rent_id)
            return jsonify(book_data)
        return 'Nie ma dostępnych wolnych egzemplarzy dla podanego identyfikatora książki', 409


@books_blueprint.route('/books/return/<int:book_id>', methods=['PATCH'])
def return_book(book_id: int):
    if request.method == 'PATCH':
        user_id = request.headers['user_id']
        try:
            user_id = int(user_id)
        except Exception as e:
            print(e)
            return 'Podany identyfikator użytkownika nie istnieje lub jest nieprawidłowy', 401
        if not book_controller.book_exist(book_id):
            return 'Podany identyfikator książki nie istnieje lub jest nieprawidłowy', 400

        if not user_controller.exist(id=user_id):
            return 'Podany identyfikator użytkownika nie istnieje lub jest nieprawidłowy', 401

        book_data = book_controller.get_book(book_id)

        if rental_controller.is_rented_by_user(user_id, book_id):
            return_id = rental_controller.return_book(book_id, user_id)
            book_data['rentals'] = rental_controller.get_rental_obj_by_id(return_id)
            return jsonify(book_data)
        return 'Użytkownik nie ma aktualnie wypożyczonych egzemplarzy dla podanego identyfikatora książki', 409
