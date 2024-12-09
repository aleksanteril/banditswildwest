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
        self.deathCount = data[7]

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
            "deathCount": self.deathCount
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

    #Death count on databasessa day_count mutta käytetään pelissä death_count
    def updateDeathCount(self):
        self.deathCount += 1
        query = kyselyt.update_player_day_count()
        database.update(query, (self.name,))
        return

    def updateMoney(self, money):
        self.money += money  # Päivitä rahamäärä
        if self.money < 0: #jos menee negatiiviseksi asetetaan rahat 0
            self.money = 0
        query = kyselyt.update_player_money(money)  # Päivitä tietokantaan
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

    def playerLocationName(self):
        query = kyselyt.fetch_user_airportname()
        nameTuple = database.query_fetchone(query, (self.name,))
        return nameTuple[0]

    def death(self):
        self.updateDeathCount()
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
            "terminaltext": "You stumble across a wounded man.",
            "text": "For a moment, my chest ached—not from judgment, but from a deep well of pity. I wondered who he was before the world weighed him down.",
            "audio": "../sounds/hello_there.mp3"
        },
        {
            "ID": "snake", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/snake.webp",
            "terminaltext": "Close call on the road with a snake.",
            "text": f"Jack reined his horse to a halt, the sharp buzz of a rattler breaking the trail’s quiet. The snake laid in a roll on the path, its tail flicking a clear warning. Well, the roads yours, friend, Jack muttered, tipping his hat. With a gentle tug, he guided his horse wide, giving the rattler its space before trotting on down the trail.",
            "audio": "../sounds/snake.mp3"
        },
        {
            "ID": "indians", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/indianonhorse.webp",
            "terminaltext": "You ride past Native-Americans.",
            "text": "Jack rode slowly through the pine-studded valley, the soft clop of his horse's hooves muffled by the earth beneath. The afternoon sun bathed the landscape in a golden glow, and the air was heavy with the scent of sagebrush. Ahead, movement caught his eye. A group of riders appeared on the ridge, their silhouettes sharp against the horizon. Native Americans, their horses sleek and surefooted, moved as one with the land. They descended toward him, deliberate but unhurried, their expressions calm yet unreadable.",
            "audio": "../sounds/horse_running.mp3"
        },
        {
            "ID": "wolf", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/coyote.webp",
            "terminaltext": "Even as beatiful as they are, better keep my distance.",
            "text": "Jack rode through the dusky plains, the fading sun painting the horizon in hues of orange and purple. His horse’s steady gait broke the stillness, but then a shadow moved to his left. A wolf stood there, its lean frame silhouetted against the twilight, eyes gleaming like amber fire. It didn’t snarl or retreat—just watched, calm and unafraid.",
            "audio": "../sounds/wolf_howl.mp3"
        },
        {
            "ID": "train", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/train.webp",
            "terminaltext": "Loyalty to companion rather than a soulless machine.",
            "text": " Jack eyed the steam train as it puffed along the tracks, its whistle loud against the quiet plains. He glanced down at Luna, her coat gleaming in the sun. 'Ain't no machine that can replace you, girl' he muttered, stroking her mane. The train may be faster, but Luna was loyal, steady, and true, something no engine could ever match.",
            "audio": "../sounds/Train.mp3"
        },
        {
            "ID": "duel", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/duel.webp",
            "terminaltext": "It's high noon.",
            "text": "The sun dipped low as a man approached, eyes cold. 'Jack,' he said, 'I hear you're fast. Let’s see.' I met his gaze, hand on my Colt. 'You looking for trouble?' He smiled. 'Let’s finish it.' A flash of steel and a sharp crack echoed through the street. The man collapsed, eyes wide in surprise. I holstered my Colt and wiped the dust from my jacket. In the West, some scores were settled quicker than others.",
            "audio": "../sounds/sus.mp3"
        },
        {
            "ID": "bar-duel", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/drunkenman.webp",
            "terminaltext": "Bar fight broke out.",
            "text": "As you were heading off to the road, a drunken man challenged you to a brawl. The saloon was chaos—shouts, breaking glass, and the thud of fists on flesh. You ducked a wild swing, countering with a hard punch to the man’s gut, sending him staggering into a table.",
            "audio": "../sounds/big_swoosh.mp3"
        },
        {
            "ID": "indianscharging", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/indianscharging.webp",
            "terminaltext": "Native Americans rushed your location.",
            "text": f"Native  Americans rode in and chaos erupted. Jack dashed for the alley, breathing heavy. He sprinted for Luna, barely outrunning the gang. Reaching the narrow path, he scrambled up on Luna riding away. The bandits unable to follow. He stopped to catch his breath, the danger fading. With a grim smile, he holstered his Colt. Close escape in the Wild West.",
            "audio": "../sounds/horse_running.mp3"
        },
        {
            "ID": "tumbleweed", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/tumbleweed.webp",
            "terminaltext": "how it all began...",
            "text": "Jack, a blacksmith, lost everything to bandits. Armed with his father’s revolver, he saved a rancher, earning a horse and boots. Training hard, Jack became a cowboy and soon, a Wild West legend.",
        },
        {
            "ID": "gamble", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/cardgame.webp",
            "terminaltext": "Trying your luck on the table, rather than on the road.",
            "text": "Jack leaned against the weathered bar, the worn deck of cards in his hand. 'Might as well kill some time,' he thought, flicking the cards onto the table. The road would still be there when he was done. With a half-smirk, he dealt the first hand, ready for a game before the next long ride ahead",
            "audio": "../sounds/dealing_cards.mp3"
        },
        {
            "ID": "generalstore", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/generalstore.webp",
            "terminaltext": "As the roads strectched longer and longer so did hunger.",
            "text": "Jack muttered to himself, his stomach growling louder than the wind. 'Too bad there's no rest for the wicked in this godforsaken land'. He spurred his horse onward, the dusty trail stretching out before him, knowing the next town was still miles away.",
            "audio": "../sounds/horse_running.mp3"
        },
        {
            "ID": "gunstore", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/gunstore.webp",
            "terminaltext": "You remember that you still own money for Rafael.",
            "text": "You ride past Rafael's gunstore, the sight of it reminding you of the debt you still owe for the custom Colt he crafted just for you. The revolver's smooth grip and polished barrel had been worth every penny, but your pockets were lighter than you'd like. You tell yourself you'll take care of it later, after a few more rides and a few more jobs. For now, you urge your horse forward, knowing Rafael will wait—just like always.",
            "audio": "../sounds/tsitsing.mp3"
        },
        {
            "ID": "fleeing", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/fleeing.webp",
            "terminaltext": "You ride pass a possible troublemaker.",
            "text": "I lowered my head, pulling the brim of my hat down just a little further. The wind bit at my face, but I kept my eyes trained on the road ahead. Up ahead, there was a figure on the horse by the trail rough-looking, with a scowl that could sour the air. He didn’t seem to notice me at first, but I wasn’t taking chances. I nudged the horse into a slow trot, keeping my distance, my body relaxed but alert. As I passed, I kept my gaze steady, barely acknowledging him. No need to make a move; just get past him without a word. Trouble wasn’t something I needed today.",
            "audio": "../sounds/sus.mp3"
        },
        {
            "ID": "horse", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/horse.webp",
            "terminaltext": "How you came about Luna.",
            "text": "Jack met Luna, a fiery black mare, by chance under the blazing Wild West sun. With a gentle touch and a quiet bond, they clicked instantly. Now, Luna is Jack's trusted steed, carrying him through dust storms and danger—his only companion on the endless roads.",
            "audio": "../sounds/horse_neigh.mp3"
        },
        {
            "ID": "W", #Luodaan tunnus jos halutaan että tapahtumalla on enemmän kuin yksi lopputulos
            "image": "../images/bedroom.webp",
            "terminaltext": "You feel well rested.",
            "text": "After an eventful night, you head back to the road.",
            "audio": "../sounds/yeah_boy_meme.mp3"
        }
        ]



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/events/<username>')
def events(username):

    if playerList[username].location == playerList[username].banditLocation:
        playerList[username].updateBanditsArrested()
        playerList[username].updateMoney(500)
        response = {
            "banditFound": True,
            "image": "../images/bandit2.webp",
            "terminaltext": f"You found a bandit in {playerList[username].playerLocationName()}, 500 dollars have been awarded",
            "text": "You finally track down the bandit, the tension thick as you face off. Weapons flash, the fight is intense but short. With skill and determination, you overpower them, securing your victory. Bound and defeated, the bandit has no choice but to come with you as you make your way back to claim justice.",
            "audio": "../sounds/pistol_shot.mp3"
        }
        responseJson = json.dumps(response)
        return Response(response=responseJson, status=200, mimetype="application/json")

    #response = travel_events[7].copy()
    response = random.choice(travel_events) #Satunnnainen tapahtuma
    situation = random.randint(0, 100)

    if response.get("ID") == "snake": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 70: #kuolamatapaus
            response["text"] = "you wander through the dusty trails of the Wild West, you suddenly feel a sharp pain in your ankle. Looking down, you see a rattlesnake slithering away, its tail still buzzing."
            response["terminaltext"] = "Death"
            playerList[username].death()
        else:
            response["text"] = "Jack reined his horse to a halt, the sharp buzz of a rattler breaking the trail’s quiet. The snake laid in a roll on the path, its tail flicking a clear warning. Well, the roads yours, friend, Jack muttered, tipping his hat. With a gentle tug, he guided his horse wide, giving the rattler its space before trotting on down the trail."

    elif response.get("ID") == "indians": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 50 and playerList[username].money >= 300: #chänssit "alt" ;) tapahtumalle
            response["text"] = "While riding your steed through a canyon, you hear a wild yell echoing across the rocks. Natives are rushing towards you, your horse spooks and you fall down. You wake up with 300 dollars less."
            playerList[username].updateMoney(-300)
        else:
            response["text"] = "Jack rode slowly through the pine-studded valley, the soft clop of his horse's hooves muffled by the earth beneath. The afternoon sun bathed the landscape in a golden glow, and the air was heavy with the scent of sagebrush. Ahead, movement caught his eye. A group of riders appeared on the ridge, their silhouettes sharp against the horizon. Native Americans, their horses sleek and surefooted, moved as one with the land. They descended toward him, deliberate but unhurried, their expressions calm yet unreadable."


    elif response.get("ID") == "woundedman": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 70: #chänssit "alt" ;) tapahtumalle
            response["text"] = "The man stated he needed help, so you jumped off your horse and started to help him, under a second and there was a gun under your chin. He steals 200 dollars."
            playerList[username].updateMoney(-200)

        elif situation > 40:
            response["text"] = "As I rode along the road, I spotted a man collapsed by the side, his clothes torn. He groaned, barely conscious, and I could see the pain in his eyes. Without thinking, I dismounted and knelt beside him. 'Hang on, I'll get you help,' I said, lifting him as gently as I could. Supporting him, to the nearest doctor. For your help he gave you 50 dollars."
            playerList[username].updateMoney(50)
        else:
            response["text"] = "For a moment, my chest ached—not from judgment, but from a deep well of pity. I wondered who he was before the world weighed him down?"

    elif response.get("ID") == "wolf": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 70: #kuolematapaus
            response["text"] = f"Under the pale moon, {playerList[username].name} rode his horse through the quiet wilderness. A shadow moved—then leapt. The wolf's cunning was greater than Jack’s speed, and by dawn, the wild claimed its victory." #pelin lopetus tila
            response["terminaltext"] = "Death"
            playerList[username].death()
        else:
            response["text"] = "Jack rode through the dusky plains, the fading sun painting the horizon in hues of orange and purple. His horse’s steady gait broke the stillness, but then a shadow moved to his left. A wolf stood there, its lean frame silhouetted against the twilight, eyes gleaming like amber fire. It didn’t snarl or retreat—just watched, calm and unafraid."


    elif response.get("ID") == "duel": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 70: #kuolematapaus
            response["text"] = "The sun dipped low as a man approached, eyes cold. 'Jack,' he said, 'I hear you're fast. Let’s see.' I met his gaze, hand on my Colt. 'You looking for trouble?' He smiled. 'Let’s finish it.' A blur of motion, a loud crack, and suddenly the world spun. Pain shot through my side as I hit the dirt. I stared up at the sky, breath ragged, knowing the  Wild West had claimed another one."
            response["audio"] = "../sounds/pistol_shot.mp3"
            response["terminaltext"] = "Death"
            playerList[username].death()
        else:
            response["text"] = f"The sun dipped low as a man approached, eyes cold. {playerList[username].name} he said, 'I hear you're fast. Let’s see.' I met his gaze, hand on my Colt. 'You looking for trouble?' He smiled. 'Let’s finish it.' A flash of steel and a sharp crack echoed through the street. The man collapsed, eyes wide in surprise. I holstered my Colt and wiped the dust from my jacket. In the West, some scores were settled quicker than others."


    elif response.get("ID") == "bar-duel": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 70: #kuolematapaus
            response["text"] = "As you were heading off the bar, a drunken man challenged you to a brawl. But he didnt play fair, he reached for a knife. The knife was thrust forward, and in an instant, your world went dark."
            response["terminaltext"] = "Death"
            playerList[username].death()
        else:
            response["text"] = "As you were heading off to the road, a drunken man challenged you to a brawl. The saloon was chaos—shouts, breaking glass, and the thud of fists on flesh. You ducked a wild swing, countering with a hard punch to the man’s gut, sending him staggering into a table."

    elif response.get("ID") == "indianscharging": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 70: #kuolematapaus
            response["text"] = "It was a quiet day when the Native Americans rode into the village, eyes full of menace. They stormed through the streets, shouting orders. I tried to reach Luna, but before I could react, one of them spotted me. A single arrow hit the back of my head, and everything went dark. The wild west had claimed another life, as quickly and ruthlessly as it always did."
            response["audio"] = "../sounds/man_dying.mp3"
            response["terminaltext"] = "Death"
            playerList[username].death()

    elif response.get("ID") == "tumbleweed": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 50:
            response["text"] = "I always loved you claire, I still have nightmares of how it all ended so abruptly. I swear I'll correct the injustices of this world, evil will perish."
            response["terminaltext"] = "Lost but not forgotten."
        else:
            response["text"] = "Jack, a blacksmith, lost everything to bandits. Armed with his father’s revolver, he saved a rancher, earning a horse and boots. Training hard, Jack became a cowboy and soon, a Wild West legend."

    elif response.get("ID") == "gamble": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 80:
            response["text"] = "Before hitting the road again you decide to gamble a little. With a sly grin, you lay down your final card. The table fell silent, then erupted in groans. While smiling ear to ear you, collect the pot. 'Victory never felt so sweet.' You win 500 dollars."
            playerList[username].updateMoney(500)

        elif situation > 30:
            response["text"] = "Before hitting the road again you decide to gamble a little. Devastation hits your face as you realize that there's no chance of winning. You lose 500 dollars."
            playerList[username].updateMoney(-500)
        else:
            response["text"] = f"{playerList[username].name} leaned against the weathered bar, the worn deck of cards in his hand. 'Might as well kill some time,' he thought, flicking the cards onto the table. The road would still be there when he was done. With a half-smirk, he dealt the first hand, ready for a game before the next long ride ahead."

    elif response.get("ID") == "gunstore": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 50 and playerList[username].money >= 500:
            response["text"] = "After weeks on the trail, Jack returned, determined to pay Rafael for the custom Colt. He walked into the shop, pulled the leather pouch from his belt, and said, 'I’ve got your money.' Rafael nodded, a small smile on his face. Jack tipped his hat, knowing he had kept his word. You pay the 500 dollar debt."
            response["terminaltext"] = "Paying debt."
            playerList[username].updateMoney(-500)
        else:
            response["text"] = "You ride past Rafael's gunstore, the sight of it reminding you of the debt you still owe for the custom Colt he crafted just for you. The revolver's smooth grip and polished barrel had been worth every penny, but your pockets were lighter than you'd like. You tell yourself you'll take care of it later, after a few more rides and a few more jobs. For now, you urge your horse forward, knowing Rafael will wait—just like always."

    elif response.get("ID") == "fleeing": #tunnuksen avulla määritellään muokattavaa tapahtumaa
        if situation > 70: #kuolematapaus
            response["text"] = "As the sun set, I rode through the plains, only to find an outlaw blocking my path. 'This is my territory,' he growled. I reached for my Colt, but he was faster. A single shot rang out, and before I could react, the world went black. The wild west had claimed another."
            response["terminaltext"] = "Death"
            response["audio"] = "../sounds/pistol_shot.mp3"
            playerList[username].death()

        elif situation > 40:
            response["text"] = "You stumble acros a young buck, tears running down his eyes as he tells he owns bandits money and that they threaten his family you decide to help him out lending the money he owns to the bandits. You give the fellow 300 dollars."
            playerList[username].updateMoney(-300)
        else:
            response["text"] = "I lowered my head, pulling the brim of my hat down just a little further. The wind bit at my face, but I kept my eyes trained on the road ahead. Up ahead, there was a figure on the horse by the trail rough-looking, with a scowl that could sour the air. He didn’t seem to notice me at first, but I wasn’t taking chances. I nudged the horse into a slow trot, keeping my distance, my body relaxed but alert. As I passed, I kept my gaze steady, barely acknowledging him. No need to make a move; just get past him without a word. Trouble wasn’t something I needed today."

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


playerList = {}
@app.route('/play/<username>')
def play(username):
    #global player
    #player = Player(username)
    playerList[username] = Player(username)
    print(playerList)
    return Response(status=200)

@app.route('/locations')
def locations():
    response = database.query(kyselyt.locations)
    responseJson = json.dumps(response)
    return Response(response=responseJson, status=200, mimetype="application/json")

@app.route('/getstats/<username>')
def getstats(username):
    responseJson = playerList[username].getStatsJson()
    print(playerList)
    print(playerList[username].location, playerList[username].travelKm*0.62, playerList[username].travelCount, playerList[username].banditLocation, playerList[username].banditsArrested, playerList[username].money, playerList[username].deathCount)
    return Response(response=responseJson, status=200, mimetype="application/json")

@app.route('/leaderboard')
def getLeaderboard():
    query = kyselyt.fetch_leaderboards
    stats = database.query(query)
    responseJson = json.dumps(stats)
    return Response(response=responseJson, status=200, mimetype="application/json")

@app.route('/playermove/<icao>/<username>')
def playerMove(icao, username):
    kilometers = kilometersBetween(playerList[username].location, icao) #Lasketaan km paikkojen välil
    playerList[username].updatePlayerLocation(icao) #Päivitetaan sijainti tietokantaan
    playerList[username].updateTravelKilometers(kilometers) #Päivitetään km tietokantaan
    playerList[username].updateTravelCounter() #Lasketaan 1 travel counteriin
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)