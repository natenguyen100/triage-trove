class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://tsvkcmug:HyBU_E90vwFhxDsYvQqAKlyWkSbXBK-i@ruby.db.elephantsql.com/tsvkcmug'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHMEY_ECHO = True
    SECRET_KEY = "abc123"
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://tsvkcmug:HyBU_E90vwFhxDsYvQqAKlyWkSbXBK-i@ruby.db.elephantsql.com/tsvkcmug'
    WTF_CSRF_ENABLED = False
