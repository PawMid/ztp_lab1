from flask import request, jsonify
from flask.blueprints import Blueprint
from controllers import user_controller, rental_controller

users_blueprint = Blueprint('users_blueprint', __name__, template_folder=r'../templates')


@users_blueprint.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users_in_system = user_controller.get_all()
        return jsonify(users_in_system)

    if request.method == 'POST':
        name = request.form['name']

        if not user_controller.exist(name=name):
            user_controller.add(name)
            return jsonify(user_controller.by_name(name))

        return "Użytkownik już istnieje", 400


@users_blueprint.route('/users/<int:user_id>', methods=['GET', 'DELETE'])
def users_id(user_id: int):
    if request.method == 'GET':
        if not user_id or not isinstance(user_id, int):
            return 'Brak ID użytkownika lub ID w złym formacie', 400
        elif user_controller.exist(id=user_id):
            user = user_controller.by_id(user_id)
            user['books'] = rental_controller.user_rentals(user_id)
            return jsonify(user)
        else:
            return 'Użytkownik o podanym ID nie istnieje', 404

    if request.method == 'DELETE':
        if not user_id or not isinstance(user_id, int):
            return 'Brak ID użytkownika lub ID w złym formacie', 400
        elif user_controller.exist(id=user_id):
            if rental_controller.user_has_rentals(user_id):
                return 'Nie można usunąć użytkownika z powodu nie zwrócenia wszystkich książek', 403
            else:
                user_controller.delete(user_id)
                return 'Usunięcie użytkownika z systemu zakończyło się powodzeniem', 200
        else:
            return 'Użytkownik o podanym ID nie istnieje', 404
