class Configuration:
    SECRET_KEY = 'secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'dmalygin228@gmail.com'
    MAIL_DEFAULT_SENDER = 'dmalygin228@gmail.com'
    MAIL_PASSWORD = 'quvycgylkmnygyfj'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/electronic_document_management'

    #DROPZONE_CONFIG
    DROPZONE_MAX_FILES = 10
    DROPZONE_MAX_FILE_SIZE = 10
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = '.pdf, .docx, .doc'

    #DROPZONE_MESSAGE
    DROPZONE_INVALID_FILE_TYPE = 'Вы не можете загрузить файлы данного типа'
    DROPZONE_FILE_TOO_BIG = 'Файл слишком большой {{filesize}}. Максимальный размер файла: {{maxFilesize}}MiB.'
    DROPZONE_SERVER_ERROR = 'Ошибка сервера: {{statusCode}}'
    DROPZONE_BROWSER_UNSUPPORTED = 'Ваш браузер не поддреживает загрузку файлов перетаскиванием'
    DROPZONE_MAX_FILE_EXCEED = 'Максимальное количество файлов загружено'