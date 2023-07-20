import sqlite3
import requests
from flask import Flask,render_template, request, url_for,redirect
import json

class Database:
    def query(self,query):
        self.sqlite_connection = sqlite3.connect("database/blog.db")
        self.cursor = self.sqlite_connection.cursor()
        try:
            self.cursor.execute(query)
            record = self.cursor.fetchall()
            self.cursor.close()
            return record
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (self.sqlite_connection):
                self.sqlite_connection.close()
                #print("Соединение с SQLite закрыто")

class Weather:
    def __init__(self):
        self.API_KEY = "bfa47318eadbf7e21019f92b8c72654b"
        self.URL_AP = "http://api.openweathermap.org/geo/1.0/direct"
        self.URL_API = "https://api.openweathermap.org/data/2.5/weather"
    def get_weather(self,lat,lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.API_KEY
        }
        ts = requests.get(self.URL_API, params=params)
        ts = ts.json()
        return ts

    def get_coord(self,city):
        params = {
            "q": city,
            "appid": self.API_KEY
        }
        ts = requests.get(self.URL_AP, params=params)
        ts = ts.json()
        return ts

def open_weather(wea):
    with open("weather.json", "r", encoding='utf-8') as file:
        file = json.load(file)
    return file[wea]

def to_celcia(temp):
    return temp - 273.15

app = Flask(__name__)
database = Database()
weather = Weather()
#database.connect("SELECT * FROM content;")
#database.connect("SELECT * FROM author;")
@app.route('/')
def index():
    news = []
    database_news = database.query("SELECT * FROM post;")
    for new in database_news:
        database_author = database.query("SELECT Author_name FROM author WHERE author_id = {};".format(new[1]))[0][0]
        database_content = database.query("SELECT title, image, text FROM content WHERE content_id = {};".format(new[2]))[0]
        news.append((new[0],database_content,database_author,new[3]))
    #assert news == [], ('Новостей нет')
    return render_template("index.html",all_news=news)

@app.route('/news/<int:id>')
def news_detail(id):
    news = []
    database_news = database.query("SELECT * FROM post;")
    for new in database_news:
        database_author = database.query("SELECT Author_name FROM author WHERE author_id = {};".format(new[1]))[0][0]
        database_content = \
        database.query("SELECT title, image, text FROM content WHERE content_id = {};".format(new[2]))[0]
        news.append((new[0], database_content, database_author, new[3]))
    # assert news == [], ('Новостей нет')
    if len(database_news) < id:
        return f"<h1>404 Not Found</h1>"
    return render_template("post.html", all_news=news,news_id=id-1)

@app.route('/weather', methods=['GET', 'POST'])
def get_weathers():
    tower = ['Москва ', 'Санкт-Петербург ', 'Новосибирск ', 'Екатеринбург ', 'Казань ', 'Нижний Новгород ',
             'Челябинск ', 'Красноярск ', 'Самара ', 'Уфа ', 'Ростов-на-Дону ', 'Омск ', 'Краснодар ', 'Воронеж ',
             'Волгоград ', 'Пермь ']
    city="Москва"
    if request.method == 'POST':
        city = request.form.get('city-c')
        if city is None:
            city = "Москва"
    lon, lat = weather.get_coord(city)[0]["lon"], weather.get_coord(city)[0]["lat"]
    weath = weather.get_weather(lat, lon)
    weath_image = weath["weather"][0]["main"]
    weather_img = open_weather(weath_image)
    weather_info = [round(to_celcia(weath["main"]["temp"]),4),round(to_celcia(weath["main"]["feels_like"]),4),round(weath["wind"]["speed"],4),round(weath["main"]["humidity"],4),round(weath["main"]["pressure"]/1.333,4)]
    return render_template("weathers.html",town=tower, city=city, info=weather_info, img_w = weather_img)

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)