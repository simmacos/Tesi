from flask import Blueprint, jsonify, request
from app.models import Tasks, Quests, Habits
from app.utilis import get_end_of_day
from app import db

insert_bp = Blueprint('insert', __name__)  


@insert_bp.route('/add_task', methods=['POST'])  
def add_task():
    data = request.json
    new_task = Tasks(
        titolo=data['titolo'],
        descrizione=data.get('descrizione'),
        difficolta_xp=data['difficolta_xp'],
        data_scadenza=get_end_of_day(),
        utenti=data['utenti']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

@insert_bp.route('/add_quest', methods=['POST'])  # Cambiato da @main.route a @insert_bp.route
def add_quest():
    data = request.json
    new_quest = Quests(
        titolo=data['titolo'],
        descrizione=data.get('descrizione'),
        difficolta_xp=data['difficolta_xp'],
        utenti=data['utenti']
    )
    db.session.add(new_quest)
    db.session.commit()
    return jsonify({'message': 'Quest added successfully'}), 201

@insert_bp.route('/add_habit', methods=['POST'])  # Cambiato da @main.route a @insert_bp.route
def add_habit():
    data = request.json
    new_habit = Habits(
        titolo=data['titolo'],
        descrizione=data.get('descrizione'),
        difficolta_xp=data['difficolta_xp'],
        utenti=data['utenti']
    )
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({'message': 'Habit added successfully'}), 201
