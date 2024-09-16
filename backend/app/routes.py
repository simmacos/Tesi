from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def hello():
    return jsonify({'fanculo': 'Son troppo bravo!~'})
