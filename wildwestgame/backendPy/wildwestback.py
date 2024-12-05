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
        self.money += money  # Päivitä rahamäärä
        if self.money < 0: #jos menee negatiiviseksi asetetaan rahat 0
            self.money = 0
        query = kyselyt.update_player_money(self.money)  # Päivitä tietokantaan
        database.update(query, (self.name,))
        return self.money

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

    def playerLocationName(self):
        query = kyselyt.fetch_user_airportname()
        nameTuple = database.query_fetchone(query, (self.name,))
        return nameTuple[0]

    def death(self):
        query = kyselyt.reset_game_state(randomizeBandit())
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

travel_events = [{  #tapahtumat mitä tapahtuu matkustamisen aikana
            "ID": "woundedman",
            "image": "../images/woundedman.webp",
            "terminaltext": "You stumble across a wounded man",
            "text": "For a moment, my chest ached—not from judgment, but from a deep well of pity. I wondered who he was before the world weighed him down?",
            "audio": "../sounds/hello_there.mp3"
        },
        {
            "ID": "snake", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/snake.webp",
            "terminaltext": "Lore",
            "text": "I was never fond of those things, bloody thing almost bit me. Mom was scared straight.",
            "audio": "../sounds/snake.mp3"
        },
        {
            "ID": "indians", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/indianonhorse.webp",
            "terminaltext": "Close call",
            "text": "Natives ahead! Better keep my head down, don't want any trouble...",
            "audio": "../sounds/horse_running.mp3"
        },
        {
            "ID": "wolf", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/coyote.webp",
            "terminaltext": "Close call",
            "text": "you ride by a wolf, keeping your head down",
            "audio": "../sounds/wolf_howl.mp3"
        },
        {
            "ID": "train", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/train.webp",
            "terminaltext": "Lore",
            "text": "Never liked those things always prefered my horse, luna.",
            "audio": "../sounds/train.mp3"
        },
        {
            "ID": "duel", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/duel.webp",
            "terminaltext": "Gun duel",
            "text": "You got challenged to a duel! thanks to combination of muscle memory and luck, you win.",
            "audio": "../sounds/sus.mp3"
        },
        {
            "ID": "bar-duel", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/drunkenman.webp",
            "terminaltext": "Bar fight",
            "text": "As you were heading off to the road, a drunken man challenged you to a brawl. The saloon was chaos—shouts, breaking glass, and the thud of fists on flesh. You ducked a wild swing, countering with a hard punch to the man’s gut, sending him staggering into a table.",
            "audio": "../sounds/big_swoosh.mp3"
        },
        {
            "ID": "indianscharging", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/indianscharging.webp",
            "terminaltext": "Caution",
            "text": "You barely escape as native indians rush the village",
            "audio": "../sounds/horse_running.mp3"
        },
        {
            "ID": "tumbleweed", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/tumbleweed.webp",
            "terminaltext": "Lore",
            "text": "Jack, a blacksmith, lost everything to bandits. Armed with his father’s revolver, he saved a rancher, earning a horse and boots. Training hard, Jack became a cowboy and soon, a Wild West legend.",
        },
        {
            "ID": "gamble", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/cardgame.webp",
            "terminaltext": "gambling",
            "text": "gambling",
            "audio": "../sounds/dealing_cards.mp3"
        },
        {
            "ID": "generalstore", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/generalstore.webp",
            "terminaltext": "Lore",
            "text": "I could do anything for a bite now, too bad theres no rest for the wicked",
            "audio": "../sounds/tsitsing.mp3"
        },
        {
            "ID": "gunstore", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/gunstore.webp",
            "terminaltext": "Lore",
            "text": "You ride by a gunstore, remembering that you own Rafael money for the custom Colt he made you, but you decide to take care about it later.",
            "audio": "../sounds/tsitsing.mp3"
        },
        {
            "ID": "fleeing", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/fleeing.webp",
            "terminaltext": "Caution",
            "text": "As you were riding fast to your new location you saw faraway a troublesome looking youngbuck but you leaned low in the saddle and rode past, thinking 'not today kid'.",
            "audio": "../sounds/sus.mp3"
        },
        {
            "ID": "horse", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/horse.webp",
            "terminaltext": "Lore",
            "text": "Jack met Luna, a fiery black mare, by chance under the blazing Wild West sun. With a gentle touch and a quiet bond, they clicked instantly. Now, Luna is Jack's trusted steed, carrying him through dust storms and danger—his only companion on the endless roads.",
            "audio": "../sounds/horse_neigh.mp3"
        },
        {
            "ID": "W", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/bedroom.webp",
            "terminaltext": "yea boiii",
            "text": "After an eventful night, you head back to the road.",
            "audio": "../sounds/yeah_boy_meme.mp3"
        }
        ]



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
            "terminaltext": f"You found a bandit in {player.playerLocationName()}, 500 dollars have been awarded",
            "text": "You finally track down the bandit, the tension thick as you face off. Weapons flash, the fight is intense but short. With skill and determination, you overpower them, securing your victory. Bound and defeated, the bandit has no choice but to come with you as you make your way back to claim justice.",
            "audio": "../sounds/pistol_shot.mp3"
        }
    else:
        response = random.choice(travel_events) #Satunnnainen tapahtuma
        situation = random.randint(0, 100)
        if response.get("ID") == "snake": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 80: #kuolamatapaus
                response["text"] = "As you wander through the dusty trails of the Wild West, you suddenly feel a sharp pain in your ankle. Looking down, you see a rattlesnake slithering away, its tail still buzzing."
                response["terminaltext"] = "Death"
                player.death()

        elif response.get("ID") == "indians": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 50: #chänssit "alt" ;) tapahtumalle
                response["text"] = "While riding your steed through a canyon, you hear a wild yell echoing across the rocks. Natives are rushing towards you, your horse spooks and you fall down. You wake up with fewer dollars"
                player.updateMoney(-300)

        elif response.get("ID") == "woundedman": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 70: #chänssit "alt" ;) tapahtumalle
                response["text"] = "The man stated he needed help, so you jumped off your horse and started to help him, under a second and there was a gun under your chin. He steals 200 dollars"
                player.updateMoney(-200)

            elif situation > 50:
                response["text"] = "You find a wounded man you help him get to the doctor, he gives you 50 dollars for helping"
                player.updateMoney(50)

        elif response.get("ID") == "wolf": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 80: #kuolematapaus
                response["text"] = "In an instant, wolf lunged, knocking you off your horse. There was nothing left to be done..." #pelin lopetus tila
                response["terminaltext"] = "Death"
                player.death()

        elif response.get("ID") == "duel": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 80: #kuolematapaus
                response["text"] = "You got challenged to a duel! Unfortunately you got bested."
                response["audio"] = "../sounds/pistol_shot.mp3"
                response["terminaltext"] = "Death"
                player.death()

        elif response.get("ID") == "bar-duel": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 80: #kuolematapaus
                response["text"] = "As you were heading off the bar, a drunken man challenged you to a brawl. But he didnt play fair, he reached for a knife. The knife was thrust forward, and in an instant, your world went dark"
                response["terminaltext"] = "Death"
                player.death()

        elif response.get("ID") == "indianscharging": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 80: #kuolematapaus
                response["text"] = "native indians rushed your location, before you reached your horse the arrow reached you first."
                response["audio"] = "../sounds/man_dying.mp3"
                response["terminaltext"] = "Death"
                player.death()

        elif response.get("ID") == "tumbleweed": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 50:
                response["text"] = "I always loved you claire, I still have nightmares of how it all ended so abruptly. I swear I'll correct the injustices of this world, evil will perish "
                response["terminaltext"] = "Lore"

        elif response.get("ID") == "gamble": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 50:
                response["text"] = "Before hitting the road again you decide to gamble a little. With a sly grin, you lay down your final card. The table fell silent, then erupted in groans. While smiling ear to ear you, collect the pot. 'Victory never felt so sweet.' You win 500 dollars"
                player.updateMoney(+500)

            elif situation > 25:
                response["text"] = "Before hitting the road again you decide to gamble a little. Devastation hits your face as you realize that there's no chance of winning. You lose 500 dollars"
                player.updateMoney(-500)

        elif response.get("ID") == "gunstore": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 50:
                response["text"] = "you decide pay Rafael the money you own for the custom made Colt."
                response["terminaltext"] = "Shopping"
                player.updateMoney(-500)

        elif response.get("ID") == "fleeing": #tunnuksen avulla määritellään muokattavaa tapahtumaa
            if situation > 80: #kuolematapaus
                response["text"] = "Tired and not paying attention to your surroundings a travelling bandit got the best of you."
                response["terminaltext"] = "Death"
                response["audio"] = "../sounds/pistol_shot.mp3"
                player.death()

            elif situation < 40:
                response["text"] = "You stumble acros a young buck, tears running down his eyes as he tells he owns bandits money and that they threaten his family you decide to help him out lending the money he owns to the bandits "
                player.updateMoney(-300)

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