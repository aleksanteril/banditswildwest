import mysql.connector

#Yhteyden luonti
connection = False
while not connection:
    try:
        yhteys = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                database="waldo_game", #input("Database: "),
                user="aleksanteri", #input("User: "),
                password="m4ks4", #input("Password: "),
                autocommit=True
                )
        connection = True
    except:
        print("\nERR: TARKISTA SYÖTETYT ARVOT")
        connection = False



#Yleisiä kyselyita varten, palauttaa arvon !listana jossa alkiot monikkoja!
def query(query, params=None):
    kursori = yhteys.cursor()
    kursori.execute(query, params)
    tulos = kursori.fetchall()
    return tulos

#Arvojen muuttamista varten ei palauta mitään
def update(query, params=None):
    kursori = yhteys.cursor()
    kursori.execute(query, params)
    return

#Kyselyä varten, mutta haluamme vain ensimmäisen arvon tulokseen KÄYTÄ VAIN JOS TIEDÄT ETTÄ TULEE 1 ARVO
def query_fetchone(query, params=None):
    kursori = yhteys.cursor()
    kursori.execute(query, params)
    tulos = kursori.fetchone()
    return tulos

#Kyselyä varten jos tarvitsee tarkistaa löytyykö tieto esim.
def check_query(query, params=None):
    kursori = yhteys.cursor()
    kursori.execute(query, params)
    tulos = kursori.fetchall()
    if kursori.rowcount > 0:
        return True
    else:
        return False
