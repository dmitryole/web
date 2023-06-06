from datetime import datetime

import requests
from bs4 import BeautifulSoup

from webapp.model import db, News

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(result.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
    
def get_python_news():
    html = get_html('https://www.python.org/blogs/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        # Происк ul с класом  list-recent-posts и выделение каждого li в список
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time')['datetime']
            try:
                """Парсим строку в формате datetime"""
                published = datetime.strptime(published, '%Y-%m-%d')
            except(ValueError):
                published = datetime.now()
            save_news(title, url, published)

def save_news(title, url, published):
    """Выборка из БД"""
    news_exists = News.query.filter(News.url == url).count()
    print(news_exists)
    if not news_exists:
        """Создаем объект класса News"""
        new_news = News(title=title, url=url, published=published)
        """Кладем в сессию SQLAlchemy"""
        db.session.add(new_news)
        """Проливаем в БД"""
        db.session.commit()