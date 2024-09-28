from flask import Blueprint, jsonify, request
from app.models import Tasks, Quests, Habits, Utenti
from app.utilis import get_end_of_day, calculate_xp
from app import db

insert_bp = Blueprint('insert', __name__)  


@insert_bp.route('/add_task', methods=['POST'])
def add_task():
    try:
        data = request.json
        print(f"Received data: {data}")  # Log dei dati ricevuti

        # Verifica che tutti i campi necessari siano presenti
        required_fields = ['titolo', 'difficolta_xp', 'utenti']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        new_task = Tasks(
            titolo=data['titolo'],
            descrizione=data.get('descrizione', ''),  # Valore di default se non presente
            difficolta_xp=data['difficolta_xp'],
            data_scadenza=get_end_of_day(),
            utenti=data['utenti'],
            skill=data['skill']
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding task: {str(e)}")  # Log dell'errore
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500


@insert_bp.route('/add_quest', methods=['POST'])  # Cambiato da @main.route a @insert_bp.route
def add_quest():
    data = request.json
    new_quest = Quests(
        titolo=data['titolo'],
        descrizione=data.get('descrizione'),
        difficolta_xp=data['difficolta_xp'],
        utenti=data['utenti'],
        skill=data['skill']
    )
    db.session.add(new_quest)
    db.session.commit()
    return jsonify({'message': 'Quest added successfully'}), 201

@insert_bp.route('/add_habit', methods=['POST'])
def add_habit():
    try:
        data = request.json
        print(f"Received data: {data}")  # Log dei dati ricevuti

        required_fields = ['titolo', 'difficolta_xp', 'utenti', 'skill', 'giorni_ripetizione']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        new_habit = Habits(
            titolo=data['titolo'],
            descrizione=data.get('descrizione', ''),
            difficolta_xp=data['difficolta_xp'],
            utenti=data['utenti'],
            skill=data['skill'],
            giorni_ripetizione=data['giorni_ripetizione'],
        )
        db.session.add(new_habit)
        db.session.commit()
        return jsonify({'message': 'Habit added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding habit: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
     
@insert_bp.route('/toggle_task/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    task.completata = not task.completata  # Questo cambia true a false e false a true
    db.session.commit()
    return jsonify({'message': 'Task status toggled successfully'}), 200

@insert_bp.route('/complete_habit/<int:habit_id>', methods=['POST'])
def complete_habit(habit_id):
    try:
        habit = Habits.query.get_or_404(habit_id)
        user = Utenti.query.get_or_404(habit.utenti)
        
        # Calcola gli XP da aggiungere
        skill_xp, general_xp = calculate_xp(habit.difficolta_xp)
        
        # Aggiungi XP all'utente
        if habit.skill == 'GENERAL':
            user.general_xp += skill_xp + general_xp
        else:
            if habit.skill == 'CULTURE':
                user.culture_xp += skill_xp
            elif habit.skill == 'SPORT':
                user.sport_xp += skill_xp
            elif habit.skill == 'WELLBEING':
                user.wellbeing_xp += skill_xp
            elif habit.skill == 'PRODUCTIVITY':
                user.productivity_xp += skill_xp
            elif habit.skill == 'CREATIVITY':
                user.creativity_xp += skill_xp
            elif habit.skill == 'SOCIAL':
                user.social_xp += skill_xp
            
            user.general_xp += general_xp

        db.session.commit()
        return jsonify({'message': 'Habit completed and XP added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error completing habit: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@insert_bp.route('/uncomplete_habit/<int:habit_id>', methods=['POST'])
def uncomplete_habit(habit_id):
    try:
        habit = Habits.query.get_or_404(habit_id)
        user = Utenti.query.get_or_404(habit.utenti)
        
        # Calcola gli XP da rimuovere
        skill_xp, general_xp = calculate_xp(habit.difficolta_xp)
        
        # Rimuovi XP dall'utente
        if habit.skill == 'GENERAL':
            user.general_xp = max(0, user.general_xp - (skill_xp + general_xp))
        else:
            if habit.skill == 'CULTURE':
                user.culture_xp = max(0, user.culture_xp - skill_xp)
            elif habit.skill == 'SPORT':
                user.sport_xp = max(0, user.sport_xp - skill_xp)
            elif habit.skill == 'WELLBEING':
                user.wellbeing_xp = max(0, user.wellbeing_xp - skill_xp)
            elif habit.skill == 'PRODUCTIVITY':
                user.productivity_xp = max(0, user.productivity_xp - skill_xp)
            elif habit.skill == 'CREATIVITY':
                user.creativity_xp = max(0, user.creativity_xp - skill_xp)
            elif habit.skill == 'SOCIAL':
                user.social_xp = max(0, user.social_xp - skill_xp)

            user.general_xp = max(0, user.general_xp - general_xp)

        db.session.commit()
        return jsonify({'message': 'Habit uncompleted and XP deducted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error uncompleting habit: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
    
@insert_bp.route('/delete_habit/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    try:
        habit = Habits.query.get_or_404(habit_id)
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'message': 'Habit deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting habit: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
    
@insert_bp.route('/uncomplete_task/<int:task_id>', methods=['POST'])
def uncomplete_task(task_id):
    try:
        task = Tasks.query.get_or_404(task_id)
        user = Utenti.query.get_or_404(task.utenti)
        
        # Calcola gli XP da rimuovere
        skill_xp, general_xp = calculate_xp(task.difficolta_xp)
        
        # Rimuovi XP dall'utente
        if task.skill == 'GENERAL':
            user.general_xp = max(0, user.general_xp - (skill_xp + general_xp))
        else:
            if task.skill == 'CULTURE':
                user.culture_xp = max(0, user.culture_xp - skill_xp)
            elif task.skill == 'SPORT':
                user.sport_xp = max(0, user.sport_xp - skill_xp)
            elif task.skill == 'WELLBEING':
                user.wellbeing_xp = max(0, user.wellbeing_xp - skill_xp)
            elif task.skill == 'PRODUCTIVITY':
                user.productivity_xp = max(0, user.productivity_xp - skill_xp)
            elif task.skill == 'CREATIVITY':
                user.creativity_xp = max(0, user.creativity_xp - skill_xp)
            elif task.skill == 'SOCIAL':
                user.social_xp = max(0, user.social_xp - skill_xp)

            user.general_xp = max(0, user.general_xp - general_xp)

        task.completata = False
        db.session.commit()
        return jsonify({'message': 'Task uncompleted and XP deducted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error uncompleting task: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
     
@insert_bp.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    try:
        task = Tasks.query.get_or_404(task_id)
        user = Utenti.query.get_or_404(task.utenti)
        
        # Calcola gli XP da aggiungere
        skill_xp, general_xp = calculate_xp(task.difficolta_xp)
        
        # Aggiungi XP all'utente
        if task.skill == 'GENERAL':
            user.general_xp += skill_xp + general_xp
        else:
            if task.skill == 'CULTURE':
                user.culture_xp += skill_xp
            elif task.skill == 'SPORT':
                user.sport_xp += skill_xp
            elif task.skill == 'WELLBEING':
                user.wellbeing_xp += skill_xp
            elif task.skill == 'PRODUCTIVITY':
                user.productivity_xp += skill_xp
            elif task.skill == 'CREATIVITY':
                user.creativity_xp += skill_xp
            elif task.skill == 'SOCIAL':
                user.social_xp += skill_xp
            
            user.general_xp += general_xp

        task.completata = True
        db.session.commit()
        return jsonify({'message': 'Task completed and XP added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error completing task: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
    
@insert_bp.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Tasks.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting task: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@insert_bp.route('/toggle_habit/<int:habit_id>', methods=['POST'])
def toggle_habit(habit_id):
    try:
        habit = Habits.query.get_or_404(habit_id)
        user = Utenti.query.get_or_404(habit.utenti)
        
        # Calcola gli XP
        skill_xp, general_xp = calculate_xp(habit.difficolta_xp)
        
        if not habit.completata:
            # Se l'habit non era completata, la completiamo e aggiungiamo XP
            habit.completata = True
            if habit.skill == 'GENERAL':
                user.general_xp += skill_xp + general_xp
            else:
                setattr(user, f"{habit.skill.lower()}_xp", getattr(user, f"{habit.skill.lower()}_xp") + skill_xp)
                user.general_xp += general_xp
            message = 'Habit completed and XP added successfully'
        else:
            # Se l'habit era già completata, la decomplettiamo e rimuoviamo XP
            habit.completata = False
            if habit.skill == 'GENERAL':
                user.general_xp = max(0, user.general_xp - (skill_xp + general_xp))
            else:
                setattr(user, f"{habit.skill.lower()}_xp", max(0, getattr(user, f"{habit.skill.lower()}_xp") - skill_xp))
                user.general_xp = max(0, user.general_xp - general_xp)
            message = 'Habit uncompleted and XP deducted successfully'

        db.session.commit()
        return jsonify({'message': message}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error toggling habit: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@insert_bp.route('/toggle_quest/<int:quest_id>', methods=['POST'])
def toggle_quest(quest_id):
    try:
        quest = Quests.query.get_or_404(quest_id)
        user = Utenti.query.get_or_404(quest.utenti)
        
        # Calcola gli XP
        skill_xp, general_xp = calculate_xp(quest.difficolta_xp)
        
        if not quest.completata:
            # Se la quest non era completata, la completiamo e aggiungiamo XP
            quest.completata = True
            if quest.skill == 'GENERAL':
                user.general_xp += skill_xp + general_xp
            else:
                setattr(user, f"{quest.skill.lower()}_xp", getattr(user, f"{quest.skill.lower()}_xp") + skill_xp)
                user.general_xp += general_xp
            message = 'Quest completed and XP added successfully'
        else:
            # Se la quest era già completata, la decomplettiamo e rimuoviamo XP
            quest.completata = False
            if quest.skill == 'GENERAL':
                user.general_xp = max(0, user.general_xp - (skill_xp + general_xp))
            else:
                setattr(user, f"{quest.skill.lower()}_xp", max(0, getattr(user, f"{quest.skill.lower()}_xp") - skill_xp))
                user.general_xp = max(0, user.general_xp - general_xp)
            message = 'Quest uncompleted and XP deducted successfully'

        db.session.commit()
        return jsonify({'message': message, 'completata': quest.completata}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error toggling quest: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
    
@insert_bp.route('/save_generated_quests', methods=['POST'])
def save_generated_quests():
    try:
        data = request.json
        print("Received data:", data)  # Log dei dati ricevuti
        user_id = data.get('user_id')
        generated_quests = data.get('quests', [])

        print(f"User ID: {user_id}")
        print(f"Number of quests: {len(generated_quests)}")

        saved_quests = []
        for quest in generated_quests:
            print(f"Processing quest: {quest}")  # Log di ogni quest
            new_quest = Quests(
                titolo=quest['title'],
                descrizione=quest['description'],
                difficolta_xp=quest['difficulty'],
                skill=quest['skill'],
                utenti=user_id,
                completata=False
            )
            db.session.add(new_quest)
            db.session.flush()  # This will populate the id field
            saved_quests.append({
                'id': new_quest.ID,
                'title': new_quest.titolo,
                'description': new_quest.descrizione,
                'difficulty': new_quest.difficolta_xp,
                'skill': new_quest.skill,
                'completed': new_quest.completata
            })
        
        db.session.commit()
        print(f"Saved {len(saved_quests)} quests successfully")
        return jsonify({'quests': saved_quests}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error saving generated quests: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500