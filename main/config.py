

class Config:
    
    SECRET_KEY = 'd7659fef2c1feeb0577f780687697ce9'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USERNAME ='20eucs018@skcet.ac.in'
    MAIL_PASSWORD ='Ashwin11@'

    # MAIL_SERVER='smtp.mailtrap.io'
    MAIL_PORT = 587
    # MAIL_USERNAME = '5cae7372502387'
    # MAIL_PASSWORD = '43468280f33dbd'

    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    APP_URL ='http://localhost:5000'