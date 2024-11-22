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
        self.travelCount = data[2]
        self.travelKm = data[3]
        self.banditsArrested = data[4]
        self.banditLocation = data[5]

    #Tallentaa tämänhetkiset arvot tietokantaan
    def saveStats(self):
        query = kyselyt.save_player(self.travelKm, self.travelCount, self.location, self.banditsArrested, self.banditLocation)
        database.update(query, (self.name,))
        return

    #Haetaan random paikka rosvolle
    def randomizeBandit(self):
        self.banditLocation = randomizeBandit()
        return


#Palauttaa random bandit location ICAO
def randomizeBandit():
    randomLocation = random.choice(database.query(kyselyt.locations))
    return randomLocation[3] #3. indeksi on ICAO


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/load/<username>')
def load(username):
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


@app.route('/updatelocation/<icao>')
def updateLocation(icao):
    database.update(kyselyt.update_player_location(icao), (player.name,))
    return Response(status=200)



#@app.route('/save/<command>')
#def menu(command):


#@app.route('/save')
#def save():
    #player.saveStats()

#Pelin logiikka pyörii täällä

locations()
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)