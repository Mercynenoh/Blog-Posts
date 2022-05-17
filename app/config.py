import os

class Config:
    SECRET_KEY = '6ODmVgnZhk'
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://mercy:today@localhost/blog'
    QUOTES_API_BASE_URL ='https://thesimpsonsquoteapi.glitch.me/quotes'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass



class ProdConfig(Config):
    '''Child
    '''
    pass



    
    
    

class DevConfig(Config):
    ''' child class
    '''
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://mercy:today@localhost/blog'

    DEBUG =True

config_options = {
'development':DevConfig,
'production':ProdConfig
}