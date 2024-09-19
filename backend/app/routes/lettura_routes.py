from flask import Blueprint, jsonify
from app.utilis import get_today_range
from app.models import Tasks, Quests, Habits, Utenti
from sqlalchemy import desc

read_bp = Blueprint('read', __name__)

@read_bp.route('/tasks_all', methods=['GET'])
def get_all_tasks():
    tasks = Tasks.query.all()
    return jsonify([
        {
            'id': task.ID,
            'titolo': task.titolo,
            'descrizione': task.descrizione,
            'difficolta_xp': task.difficolta_xp,
            'completata': task.completata,
            'data_scadenza': task.data_scadenza.isoformat() if task.data_scadenza else None,
            'utenti': task.utenti
        } for task in tasks
    ]), 200

@read_bp.route('/tasks', methods=['GET'])
def get_tasks():
    start_of_day, end_of_day = get_today_range()
    print(f"Start of day: {start_of_day}, End of day: {end_of_day}")
    
    tasks = Tasks.query.filter(
        Tasks.data_scadenza.between(start_of_day, end_of_day)
    ).order_by(desc(Tasks.difficolta_xp)).all()
    
    return jsonify([{
        'id': task.ID,
        'titolo': task.titolo,
        'descrizione': task.descrizione,
        'difficolta_xp': task.difficolta_xp,
        'completata': task.completata,
        'data_scadenza': task.data_scadenza.isoformat() if task.data_scadenza else None,
        'Utente': task.utenti
    } for task in tasks]), 200

@read_bp.route('/quests', methods=['GET'])
def get_quests():
    start_of_day, end_of_day = get_today_range()
    
    quests = Quests.query.order_by(desc(Quests.difficolta_xp)).all()
    
    return jsonify([{
        'id': quest.ID,
        'titolo': quest.titolo,
        'descrizione': quest.descrizione,
        'difficolta_xp': quest.difficolta_xp,
        'completata': quest.completata,
        'utenti': quest.utenti
    } for quest in quests]), 200

@read_bp.route('/habits', methods=['GET'])
def get_habits():
    habits = Habits.query.order_by(desc(Habits.difficolta_xp)).all()
    
    return jsonify([{
        'id': habit.ID,
        'titolo': habit.titolo,
        'descrizione': habit.descrizione,
        'difficolta_xp': habit.difficolta_xp,
        'attiva': habit.attiva,
        'utenti': habit.utenti
    } for habit in habits]), 200

@read_bp.route('/user/<username>/general_xp', methods=['GET'])
def get_general_xp(username):
    user = Utenti.query.get_or_404(username)
    return jsonify({
        'username': user.Username,
        'general_xp': user.general_xp
    }), 200

@read_bp.route('/user/<username>/skill_xp', methods=['GET'])
def get_skill_xp(username):
    user = Utenti.query.get_or_404(username)
    return jsonify({
        'username': user.Username,
        'culture_xp': user.culture_xp,
        'sport_xp': user.sport_xp,
        'wellbeing_xp': user.wellbeing_xp,
        'productivity_xp': user.productivity_xp,
        'creativity_xp': user.creativity_xp
    }), 200

@read_bp.route('/user/<username>/culture_xp', methods=['GET'])
def get_culture_xp(username):
    user = Utenti.query.get_or_404(username)
    return jsonify({
        'username': user.Username,
        'culture_xp': user.culture_xp
    }), 200

@read_bp.route('/user/<username>/sport_xp', methods=['GET'])
def get_sport_xp(username):
    user = Utenti.query.get_or_404(username)
    return jsonify({
        'username': user.Username,
        'sport_xp': user.sport_xp
    }), 200

@read_bp.route('/user/<username>/wellbeing_xp', methods=['GET'])
def get_wellbeing_xp(username):
    user = Utenti.query.get_or_404(username)
    return jsonify({
        'username': user.Username,
        'wellbeing_xp': user.wellbeing_xp
    }), 200

@read_bp.route('/user/<username>/productivity_xp', methods=['GET'])
def get_productivity_xp(username):
    user = Utenti.query.get_or_404(username)
    return jsonify({
        'username': user.Username,
        'productivity_xp': user.productivity_xp
    }), 200

@read_bp.route('/user/<username>/creativity_xp', methods=['GET'])
def get_creativity_xp(username):
    user = Utenti.query.get_or_404(username)
    return jsonify({
        'username': user.Username,
        'creativity_xp': user.creativity_xp
    }), 200

