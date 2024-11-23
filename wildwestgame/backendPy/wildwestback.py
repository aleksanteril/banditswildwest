from flask import Flask, Response
from flask_cors import CORS
import json
import database #Database yhteys import, ja kysely funktiot
import kyselyt
import random

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


    def getStats(self):
        dataList = database.query(kyselyt.load_username(), (self.name,))
        data = dataList[0]
        return data


    def updateBanditsArrested(self):
        query = kyselyt.update_bandits_arrested()
        database.update(query, (self.name,))
        self.banditLocation = randomizeBandit()
        database.update(kyselyt.update_bandit_location(self.banditLocation), (self.name,))
        return


    def updateTravelCounter(self):
        query = kyselyt.update_player_travel_counter()
        database.update(query, (self.name,))
        return


    def updateTravelKilometers(self, km):
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

@app.route('/play/<username>')
def play(username):
    global player
    player = Player(username)
    response = {
        "name": player.name,
        "location": player.location,
        "travelKm": player.travelKm,
        "travelCount": player.travelCount,
        "banditsArrested": player.banditsArrested,
        "banditLocation": player.banditLocation
    }
    responseJson = json.dumps(response)
    return Response(response=responseJson, status=200, mimetype="application/json")

@app.route('/locations')
def locations():
    response = database.query(kyselyt.locations)
    responseJson = json.dumps(response)
    return Response(response=responseJson, status=200, mimetype="application/json")

@app.route('/getstats')
def load():
    data = player.getStats()
    print(data[4])
    response = {
        "name": data[0],
        "location": data[1],
        "travelKm": data[2],
        "travelCount": data[3],
        "banditsArrested": data[4],
        "banditLocation": data[5]
    }
    responseJson = json.dumps(response)
    return Response(response=responseJson, status=200, mimetype="application/json")


@app.route('/playermove/<icao>')
def playerMove(icao):
    player.travelKm = kilometersBetween(player.location, icao) #Lasketaan km paikkojen välil
    player.updatePlayerLocation(icao) #Päivitetaan sijainti tietokantaan
    player.updateTravelKilometers(player.travelKm) #Päivitetään km tietokantaan
    player.updateTravelCounter() #Lasketaan 1 travel counteriin
    if player.location == player.banditLocation:  #Palautetaan true ja uusi location jos bandit löytyi
        player.updateBanditsArrested()
        response = {
            "arrest": True,
            "banditLocation": player.banditLocation
        }
    else:                                         #Muuten palautetaan false
        response = {
            "arrest": False
        }
    #player.saveStats()  #Tallennetaan muutokset
    responseJson = json.dumps(response)
    return Response(response=responseJson, status=200, mimetype="application/json")





#@app.route('/save/<command>')
#def menu(command):


#@app.route('/save')
#def save():
    #player.saveStats()

#Pelin logiikka pyörii täällä

locations()
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)