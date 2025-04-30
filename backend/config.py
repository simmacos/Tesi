import os
from dotenv import load_dotenv

# Ottiene il percorso assoluto della directory corrente
basedir = os.path.abspath(os.path.dirname(__file__))

# Carica le variabili d'ambiente dal file .env se esiste
if os.path.exists(os.path.join(basedir, '.env')):
    load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    
    # Usa DATABASE_URL se fornito (come su Render), altrimenti costruisci l'URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    # Se l'URL inizia con 'postgres://', sostituisci con 'postgresql://'
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Altre configurazioni...
    PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
