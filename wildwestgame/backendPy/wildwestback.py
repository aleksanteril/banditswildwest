from flask import Flask
import database #Database yhteys import, ja kysely funktiot
import kyselyt


def query_testi(query, params=None):
    kursori = database.yhteys.cursor()
    kursori.execute(query, params)
    tulos = kursori.fetchall()
    return tulos

#Tähän fileen rakennetaan pelin backend logiikka ja flaskilla palvelut
#Endpointit määritetään tähän
kys = "SELECT ident FROM airport, country WHERE airport.iso_country = country.iso_country and country.name = %s ORDER BY CASE WHEN type = 'large_airport' THEN 1 WHEN type = 'medium_airport' THEN 2 WHEN type = 'small_airport' THEN 3 ELSE 4 END;"
print(query_testi(kys, ("finland",)))