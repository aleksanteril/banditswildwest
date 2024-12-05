

#KYSELYT PELIN LOGIIKKAA VARTEN #############################

#Kysely jolla saadaan maan vihje jossa matkalaukku sijaitsee ICAO
#def country_hint(case_location):
#    sql_query_country_hint = (f"SELECT hint, name FROM country WHERE iso_country in("
#                          f"SELECT iso_country FROM airport WHERE ident = '{case_location}');")
#    return sql_query_country_hint

#Vakio kysely joka palauttaa maat, aakkosjärjestyksessä
countries = f"SELECT name FROM country WHERE continent = 'EU' ORDER BY name;"

locations = f"SELECT latitude_deg, longitude_deg, name, ident FROM airport WHERE (iso_region = 'US-CO' OR iso_region = 'US-UT') AND type = 'medium_airport';"


def coordinates_icao(icao):
    sql_query_coordinates = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{icao}';"
    return sql_query_coordinates

#Kysely jolla saadaan parametri country avulla kyseisen maan lentokenttien ICAOT järjestyksessä large tyypistä alaspäin
#def country_airports(country):
#    sql_query_airports = (f"SELECT ident FROM airport, country "
#                      f"WHERE airport.iso_country = country.iso_country and country.name = '{country}'"
#                          f" ORDER BY CASE WHEN type = 'large_airport' THEN 1 WHEN type = 'medium_airport' THEN 2 WHEN type = 'small_airport' THEN 3 ELSE 4 END;")
#    return sql_query_airports



#Kysely jolla saadaan etäisyys pelaajan ja jonkun toisen paikan välillä, float metreissä!
def distance_between_player_locations(icao2):
    sql_query_distance = (f"SELECT ST_Distance_Sphere("
                                    f"ST_GeomFromText(("
                                    f"SELECT CONCAT('POINT (',longitude_deg, ' ',latitude_deg,')') FROM airport WHERE ident in(SELECT location FROM game WHERE id = %s)), 4326), "
                                    f"ST_GeomFromText(("
                                    f"SELECT CONCAT('POINT (',longitude_deg, ' ',latitude_deg,')') FROM airport WHERE ident = '{icao2}'), 4326));")
    return sql_query_distance

#Kysely jolla saadaan etäisyys kahden paikan väliltä metreissä float!
def distance_between_locations(icao1, icao2):
    sql_query_distance = (f"SELECT ST_Distance_Sphere("
                                    f"ST_GeomFromText(("
                                    f"SELECT CONCAT('POINT (',longitude_deg, ' ',latitude_deg,')') FROM airport WHERE ident = '{icao1}'), 4326), "
                                    f"ST_GeomFromText(("
                                    f"SELECT CONCAT('POINT (',longitude_deg, ' ',latitude_deg,')') FROM airport WHERE ident = '{icao2}'), 4326));")
    return sql_query_distance


#LOAD KYSELYT ##################

#Kysely jolla kysytään käyttäjän arvot
def load_username():
    sql_query_load_username = (f"SELECT id, location, total_kilometers, travel_count, bandits_captured, bandit_location, money, day_count "
                               f"FROM game WHERE id = %s;")
    return sql_query_load_username


#INSERT KYSELYT ################ UUDEN PELAAJAN LUOMISEEN

#Kysely jolla päivitetään uusi käyttäjä myös suitcase tauluun
#def new_suitcase():
#    sql_query_new_suitcase = (f"INSERT INTO suitcase (id) VALUES (%s);")
#    return sql_query_new_suitcase

#Kysely jolla päivitetään uusi käyttäjä tietokantaan ja asetetaan alkuarvot
def new_username(banditLocation):
    sql_query_new_username = (f"INSERT INTO game (id, location, total_kilometers, travel_count, bandits_captured, bandit_location, money, day_count) VALUES (%s, 'KAPA', 0, 0, 0,'{banditLocation}', 1000, 0);")
    return sql_query_new_username


#CHECK KYSELYT TRUE FALSE ############

#Kysely jolla tarkastetaan löytyykö nimi jo pelin tietokannasta
def check_username():
    sql_query_check_usernames = (f"SELECT id FROM game WHERE id = %s;")
    return sql_query_check_usernames


#FETCH KYSELYT #############

def fetch_user_airportname():
    sql_query_user_airportname = f"SELECT name FROM airport WHERE ident in(SELECT location FROM game WHERE id = %s);"
    return sql_query_user_airportname

#Kysely jolla saadaan käyttäjän maa LOWERcasena
#def fetch_user_country():
#    sql_query_fetch_user_country = (f"SELECT LOWER(name) FROM country WHERE iso_country in("
#                                    f"SELECT iso_country FROM airport WHERE ident in("
#                                    f"SELECT location FROM game WHERE id = %s));")
#    return sql_query_fetch_user_country

#Kysely jolla saadaan käyttäjän matkalaukun maa LOWERcasena
#def fetch_suitcase_country():
#    sql_query_fetch_suitcase_country = (f"SELECT LOWER(name) FROM country WHERE iso_country in("
#                                        f"SELECT iso_country FROM airport WHERE ident in("
#                                        f"SELECT location FROM suitcase WHERE id = %s));")
#    return sql_query_fetch_suitcase_country

#Vakio kysely jolla haetaan tietokannasta ihmiset joilla on vähintään yli 1 matkalaukku ja max 5 ihmistä desc order.
fetch_leaderboards = (f"SELECT id, bandits_captured FROM game WHERE bandits_captured >= 1 order by bandits_captured desc LIMIT 5;")

#Vakio kysely jolla saadaan olemassaolevat käyttäjät
fetch_users = (f"SELECT id FROM game")

#UPDATE KYSELYT #####################

def update_bandit_location(location):
    sql_query_update_bandit_location = (f"UPDATE game SET bandit_location = ('{location}') WHERE id = %s;")
    return sql_query_update_bandit_location

def update_bandits_arrested():
    sql_query_update_bandit_arrested = (f"UPDATE game SET bandits_captured = 1+bandits_captured WHERE id = %s;")
    return sql_query_update_bandit_arrested

def update_player_travel_counter():
    sql_query_update_player_travel = (f"UPDATE game SET travel_count = 1+travel_count WHERE id = %s;")
    return sql_query_update_player_travel

def update_player_day_count():
    sql_query_update_player_day = (f"UPDATE game SET day_count = 1+day_count WHERE id = %s;")
    return sql_query_update_player_day

def update_player_money(money):
    sql_query_update_player_money = (f"UPDATE game SET money = {money}+money WHERE id = %s;")
    return sql_query_update_player_money

def update_player_travel_kilometers(km):
    sql_query_update_player_travel = (f"UPDATE game SET total_kilometers = {km}+total_kilometers WHERE id = %s;")
    return sql_query_update_player_travel

def update_player_location(location):
    sql_query_update_player_location = (f"UPDATE game SET location = ('{location}') WHERE id = %s;")
    return sql_query_update_player_location

#Lisätään pelaajalle kilometrit, co2 määrä, travel count, location tietokantaan talteen
def save_player(kilometers, count, location, bandits_captured, bandits_location):
    sql_query_update_player_travel = (f"UPDATE game SET location = '{location}', total_kilometers = {kilometers}+total_kilometers, travel_count = {count}+travel_count, bandits_captured = {bandits_captured}+bandits_captured, bandit_location = '{bandits_location}' WHERE id = %s;")
    return sql_query_update_player_travel

def player_death():
    sql_query_player_death = (f"DELETE FROM game WHERE id = %s;")
    return sql_query_player_death

#Kysely jolla päivitetään onko pelaaja avannut cluen
#def update_clue_unlocked(int):
#    sql_query_update_clue_unlocked = (f"UPDATE game SET clue_unlocked = {int} WHERE id = %s;")
#    return sql_query_update_clue_unlocked

#Kysely jolla päivitetään peli takaisin alkuun ja lisätään pelaajalle 1 matkalaukku löydetty
def reset_game_state(bandit_location):
    sql_query_reset_game_state = (f"UPDATE game SET location = 'KAPA', total_kilometers = 0, travel_count = 0, bandits_captured = 0, bandit_location = '{bandit_location}', money = 0, day_count = 0 WHERE id = %s;")
    return sql_query_reset_game_state