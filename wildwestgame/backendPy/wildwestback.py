from flask import Flask
import database #Database yhteys import, ja kysely funktiot
import kyselyt

class Player:
    def __init__(self, id):
        bool = database.check_query(kyselyt.check_username(), (id,))
        if bool: #Jos käyttäjä on olemassa ladataan aiemmat arvot
            dataList = database.query(kyselyt.load_username(), (id,))
            data = dataList[0]
        else: #Jos käyttäjä ei olemassa asetetaan vakioarvot ja ladataan ne
            database.update(kyselyt.new_username(), (id,))
            dataList = database.query(kyselyt.load_username(), (id,))
            data = dataList[0]
        self.name = data[0]
        self.location = data[1]
        self.travelCount = data[2]
        self.travelKm = data[3]
        self.banditsArrested = data[4]

    #Tallentaa tämänhetkiset arvot tietokantaan
    def saveStats(self):
        query = kyselyt.save_player(self.travelKm, self.travelCount, self.location, self.banditsArrested)
        database.update(query, (self.name,))
        return


app = Flask(__name__)

@app.route('/load/<username>')
def load(username):
    global player
    player = Player(username)
    response = {
        "Name": player.name,
        "Location": player.location,
        "TravelKm": player.travelKm,
        "TravelCount": player.travelCount,
        "BanditsArrested": player.banditsArrested,
        "status": 200
    }
    return response




#@app.route('/save/<command>')
#def menu(command):


#@app.route('/save')
#def save():
    #player.saveStats()

#Pelin logiikka pyörii täällä


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)