

class Config:
    
    SECRET_KEY = 'secretkey'
    SQLALCHEMY_DATABASE_URI = 'db'
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USERNAME ='email'
    MAIL_PASSWORD ='password'

    # MAIL_SERVER='smtp.mailtrap.io'
    MAIL_PORT = 587
    # MAIL_USERNAME = '5cae7372502387'
    # MAIL_PASSWORD = '43468280f33dbd'

    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    APP_URL ='http://localhost:5000'