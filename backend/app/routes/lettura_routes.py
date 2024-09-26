from flask import Blueprint, jsonify
from app.utilis import get_today_range
from app.models import Tasks, Quests, Habits, Utenti
from sqlalchemy import desc
from datetime import datetime
from sqlalchemy import func

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
            'utenti': task.utenti,
            'skill': task.skill
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
        'skill': task.skill,
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
        'skill': quest.skill,
        'utenti': quest.utenti
    } for quest in quests]), 200

from datetime import datetime


@read_bp.route('/habits', methods=['GET'])
def get_habits():
    try:
        today = datetime.now().weekday()  # 0 è lunedì, 6 è domenica
        print(f"Fetching habits for day {today}")
        
        habits = Habits.query.filter(
            func.substring(Habits.giorni_ripetizione, today + 1, 1) == '1'
        ).order_by(desc(Habits.difficolta_xp)).all()
        
        habits_list = [{
            'id': habit.ID,
            'titolo': habit.titolo,
            'descrizione': habit.descrizione,
            'difficolta_xp': habit.difficolta_xp,
            'giorni_ripetizione': habit.giorni_ripetizione,
            'skill': habit.skill,
            'utenti': habit.utenti
        } for habit in habits]
        
        return jsonify(habits_list), 200
    except Exception as e:
        print(f"Error fetching habits: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

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

@read_bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Hello from Flask!"}), 200