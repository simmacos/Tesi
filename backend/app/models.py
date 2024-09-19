from app import db
from datetime import date

class Utenti(db.Model):
    __tablename__ = 'utenti'

    Username = db.Column(db.String(50), primary_key=True)
    general_xp = db.Column(db.Integer, default=0)
    culture_xp = db.Column(db.Integer, default=0)
    sport_xp = db.Column(db.Integer, default=0)
    wellbeing_xp = db.Column(db.Integer, default=0)
    productivity_xp = db.Column(db.Integer, default=0)
    creativity_xp = db.Column(db.Integer, default=0)

    tasks = db.relationship('Tasks', backref='utente', lazy='dynamic')
    quests = db.relationship('Quests', backref='utente', lazy='dynamic')
    habits = db.relationship('Habits', backref='utente', lazy='dynamic')

    def __repr__(self):
        return f'<Utente {self.Username}>'

class Tasks(db.Model):
    __tablename__ = 'tasks'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titolo = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text)
    difficolta_xp = db.Column(db.Integer, nullable=False)
    completata = db.Column(db.Boolean, default=False)
    data_scadenza = db.Column(db.Date)
    utenti = db.Column(db.String(50), db.ForeignKey('utenti.Username'))

    def __repr__(self):
        return f'<Task {self.titolo}>'

class Quests(db.Model):
    __tablename__ = 'quests'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titolo = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text)
    difficolta_xp = db.Column(db.Integer, nullable=False)
    completata = db.Column(db.Boolean, default=False)
    utenti = db.Column(db.String(50), db.ForeignKey('utenti.Username'))

    def __repr__(self):
        return f'<Quest {self.titolo}>'

class Habits(db.Model):
    __tablename__ = 'habits'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titolo = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text)
    difficolta_xp = db.Column(db.Integer, nullable=False)
    attiva = db.Column(db.Boolean, default=True)
    utenti = db.Column(db.String(50), db.ForeignKey('utenti.Username'))

    def __repr__(self):
        return f'<Habit {self.titolo}>'
