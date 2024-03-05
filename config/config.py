#!/usr/bin/env python3
import os


class Config:
    SECRET_KEY = 'SECRET_KEY'
    DATABASE_USERNAME = 'user'
    DATABASE_PASSWORD = "123456"
    DATABASE_NAME = 'database'
    UPLOAD_DIR = os.path.join(os.getcwd(), 'static', 'upload')
    UPLOAD_EXTENSION = ('png', 'jpg', 'jpeg', 'gif')
    UPLOAD_MSG = ('about', 'article')
    # Article list thumbnail, the following three data need to correspond
    THUMBNAIL_WIDTH = 400
    THUMBNAIL_HEIGHT = 225
    THUMBNAIL_RATIO = 9 / 16
    # Say list thumbnail, the following three data need to correspond
    SAY_THUMBNAIL_WIDTH = 400
    SAY_THUMBNAIL_HEIGHT = 400
    SAY_THUMBNAIL_RATIO = 1
    # In the list display of the management background, the length of the displayed title is replaced by ellipses.
    ADMIN_CUT_STRING_LENGTH = 20
    LIST_STYLE = ['card', 'row']
    # logo
    LOGO_WIDTH = 200
    LOGO_HEIGHT = 200
    LOGO_RATIO = 1
    # language
    LANGUAGE = [
        {"key": "english", "title": "English"},
        {"key": "spanish", "title": "Español"},
        {"key": "traditional_chinese", "title": "繁體中文"},
        {"key": "simplified_chinese", "title": "简体中文"},
        {"key": "japanese", "title": "日本語"}
    ]


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
