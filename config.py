class Configuration:
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'dmalygin228@gmail.com'
    MAIL_DEFAULT_SENDER = 'dmalygin228@gmail.com'
    MAIL_PASSWORD = 'quvycgylkmnygyfj'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/electronic_document_management'