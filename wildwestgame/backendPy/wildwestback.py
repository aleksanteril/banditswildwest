from flask import Flask, Response
from flask_cors import CORS
import json
import database #Database yhteys import, ja kysely funktiot
import kyselyt
import random
import requests

class Player:
    def __init__(self, id):
        bool = database.check_query(kyselyt.check_username(), (id,))
        if bool: #Jos käyttäjä on olemassa ladataan aiemmat arvot
            dataList = database.query(kyselyt.load_username(), (id,))
            data = dataList[0]
        else: #Jos käyttäjä ei olemassa asetetaan vakioarvot ja ladataan ne
            database.update(kyselyt.new_username(randomizeBandit()), (id,))
            datalist = database.query(kyselyt.load_username(), (id,))
            data = datalist[0]
        self.name = data[0]
        self.location = data[1]
        self.travelKm = data[2]
        self.travelCount = data[3]
        self.banditsArrested = data[4]
        self.banditLocation = data[5]
        self.money = data[6]
        self.dayCount = data[7]

    #Statsien haku database
    def getStats(self):
        dataList = database.query(kyselyt.load_username(), (self.name,))
        data = dataList[0]
        return data

    def getStatsJson(self):
        response = {
            "name": self.name,
            "location": self.location,
            "travelKm": self.travelKm,
            "travelCount": self.travelCount,
            "banditsArrested": self.banditsArrested,
            "banditLocation": self.banditLocation,
            "money": self.money,
            "dayCount": self.dayCount
        }
        return json.dumps(response)

    def updateBanditsArrested(self):
        self.banditsArrested += 1
        query = kyselyt.update_bandits_arrested()
        database.update(query, (self.name,))
        self.banditLocation = randomizeBandit()
        database.update(kyselyt.update_bandit_location(self.banditLocation), (self.name,))
        return


    def updateTravelCounter(self):
        self.travelCount += 1
        query = kyselyt.update_player_travel_counter()
        database.update(query, (self.name,))
        return

    def updateDayCount(self):
        self.dayCount += 1
        query = kyselyt.update_player_day_count()
        database.update(query, (self.name,))
        return

    def updateMoney(self, money):
        self.money += money
        query = kyselyt.update_player_money(money)
        database.update(query, (self.name,))
        return

    def updateTravelKilometers(self, km):
        self.travelKm += km
        query = kyselyt.update_player_travel_kilometers(km)
        database.update(query, (self.name,))
        return


    def updatePlayerLocation(self, icao):
        self.location = icao
        query = kyselyt.update_player_location(icao)
        database.update(query, (self.name,))
        return



#Palauttaa random bandit location ICAO
def randomizeBandit():
    randomLocation = random.choice(database.query(kyselyt.locations))
    return randomLocation[3] #3. indeksi on ICAO

#Laskee etöisyyden kilometrit kahden paikan välillä
def kilometersBetween(icao1, icao2):
    query = kyselyt.distance_between_locations(icao1, icao2)
    meters = database.query_fetchone(query)
    kilometersRounded = int(meters[0]/1000) #Palautetaan intillä rajusti pyöristetty arvo ja monikon indeksi0
    return kilometersRounded




app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/events')
def events():
    if player.location == player.banditLocation:
        player.updateBanditsArrested()
        player.updateMoney(500)
        response = {
            "image": "../images/bandit2.webp",
            "terminaltext": f"You found a bandit in {player.location}, 500 dollars have been awarded",
            "text": "You finally track down the bandit, the tension thick as you face off. Weapons flash, the fight is intense but short. With skill and determination, you overpower them, securing your victory. Bound and defeated, the bandit has no choice but to come with you as you make your way back to claim justice.",
            "audio": "../sounds/crows.mp3"
        }
    else:
        response = {
            "image": "../images/woundedman.webp",
            "terminaltext": "You stumble across a wounded man",
            "text": "You stumble across a wounded man",
            "audio": "../ sounds / crows.mp3"
        }
    responseJson = json.dumps(response)
    return Response(response=responseJson, status=200, mimetype="application/json")


@app.route('/findweather/<icao>')
def findweather(icao):
    query = kyselyt.coordinates_icao(icao)
    coordinatesTuple = database.query_fetchone(query)
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={coordinatesTuple[0]}&longitude={coordinatesTuple[1]}&current=temperature,is_day,weather_code")
    currentWeather = response.json()['current']
    responseJson = json.dumps(currentWeather)
    return Response(response=responseJson, status=200, mimetype="application/json")


@app.route('/play/<username>')
def play(username):
    global player
    player = Player(username)
    return Response(status=200)

@app.route('/locations')
def locations():
    response = database.query(kyselyt.locations)
    responseJson = json.dumps(response)
    return Response(response=responseJson, status=200, mimetype="application/json")

@app.route('/getstats')
def getstats():
    responseJson = player.getStatsJson()
    print(player.location, player.travelKm, player.travelCount, player.banditLocation, player.banditsArrested, player.money, player.dayCount)
    return Response(response=responseJson, status=200, mimetype="application/json")


@app.route('/playermove/<icao>')
def playerMove(icao):
    kilometers = kilometersBetween(player.location, icao) #Lasketaan km paikkojen välil
    player.updatePlayerLocation(icao) #Päivitetaan sijainti tietokantaan
    player.updateTravelKilometers(kilometers) #Päivitetään km tietokantaan
    player.updateTravelCounter() #Lasketaan 1 travel counteriin
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)