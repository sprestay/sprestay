from app import app
from flask import render_template, redirect, request
import requests, json
from geopy.geocoders import Nominatim, Yandex
from datetime import datetime


key1 = "a6b03560-2414-4f92-aa69-5582ed6fb87f"
key2 = "794106a1-dc57-416d-8d96-e9890c0d8890"
@app.route("/")
def index():
    return render_template("base.html", user='Ignat Egorov')


def get_forecast(data):
    h = datetime.now().hour
    if 5 <= h <= 11:
        info = ['Днем: ', data['day']]
    elif 12 <= h <= 18:
        info = ['Вечером: ', data['evening']]
    elif 19 <= h <= 23:
        info = ['Ночью: ', data['night']]
    elif 0 <= h <=4:
        info = ['Утром: ', data['morning']]
    return info

def get_clothes(data):
    if -10 <= data['feels_like'] <= 5:
        shapka = "шапку"
        kyrtka = "куртку"
    elif data['feels_like'] < -10:
        shapka = "теплую шапку"
        kyrtka = "Пуховик"
    elif 5 < data['feels_like'] <= 15:
        shapka = None
        kyrtka = "легкую куртку"
    elif data['feels_like'] > 15:
        shapka = None
        kyrtka = None

    if data['prec_prob'] < 20:
        zont = None
    elif 20 <= data['prec_prob'] <=50 and data['temp_avg'] > 0:
        zont = "возможно понадобится зонт"
    elif 50 < data['prec_prob'] and data['temp_avg'] > 0:
        zont = "не забудьте зонт!"
    
    result = ""
    if kyrtka:
        result += "Лучше надеть " + kyrtka
        if shapka:
            result += " и " + shapka
        if zont:
            result += ". А так же - " + zont
    else:
        if zont:
            result = str.capitalize(zont)

    if not result:
        result = "Живи и радуйся"
    return result


@app.route('/generate_forecast', methods=['POST'])
def generate_forecast():
    if request.method == "POST" and request.is_xhr:
        geo = Yandex(api_key=key2)
        req = ""
        if request.form['region']:
            req += request.form['region'] + ", "
        req += request.form['city']
        location = geo.geocode(req)
        if not location:
            return "didn`t find"
        lat, lon = location.latitude, location.longitude
        response = json.loads(requests.get("https://api.weather.yandex.ru/v1/forecast",
            headers={"X-Yandex-API-Key": key1},
            params={
                "lat": lat, 
                "lon": lon,
        }).content)
        forecast = get_forecast(response['forecasts'][0]['parts'])
        recomendation = get_clothes(forecast[1])
        return json.dumps([response['fact'], forecast, recomendation])
    return redirect('/')