from webapp import db, create_app

"""Инициализируем создание модели"""
db.create_all(app=create_app())
