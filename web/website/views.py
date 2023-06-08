from flask import Blueprint, render_template, request
import requests

views = Blueprint('views', __name__)

# NewsAPI configuration
API_KEY = 'ee9484b6aec54eb082867c878a2444a7'  # Replace with your NewsAPI key

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


from flask_login import current_user, login_required

@views.route('/news', methods=['GET', 'POST'])
@login_required
def index():
    selected_countries = request.form.getlist('countries')
    search_keyword = request.form.get('search_keyword')

    if not selected_countries and not search_keyword:
        filtered_news = get_news()
    else:
        filtered_news = get_filtered_news(selected_countries, search_keyword)

    return render_template('news.html', filtered_news=filtered_news, user=current_user)


def get_news(selected_countries=None):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': '',
        'apiKey': API_KEY
    }

    if selected_countries:
        params['country'] = ','.join(selected_countries)

    response = requests.get(url, params=params)
    news_data = response.json()

    if response.status_code == 200:
        articles = news_data['articles']
        news = []
        for article in articles:
            news_article = {
                'headline': article['title'],
                'content': article['description'],
                'url': article['url']
            }
            news.append(news_article)

        return news

    return []  # Return empty list if there's an error or no news available


def get_filtered_news(selected_countries=None, search_keyword=None):
    news = get_news(selected_countries)

    if not search_keyword:
        return news

    filtered_news = []
    for article in news:
        if article['headline'] and search_keyword.lower() in article['headline'].lower():
            filtered_news.append(article)
        elif article['content'] and search_keyword.lower() in article['content'].lower():
            filtered_news.append(article)

    return filtered_news
